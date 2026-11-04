// Every block's React variant (r/react/lucide) type-checks under strict
// TypeScript and renders pixel-identical to the HTML block, also after the
// same interactions.
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { build } from 'esbuild';
import { root, dist, registry, freshDir, run, bin, json, serve, browser, open, shot, stableDiff, keep, blockNames, requireBuild } from './lib/env.mjs';

let dir, server, b, names;
before(async () => {
  requireBuild();
  names = await blockNames();
  dir = await freshDir('react-blocks');
  await fs.mkdir(path.join(dir, 'src/blocks'), { recursive: true });
  await fs.mkdir(path.join(dir, 'src/types'));
  for (const f of ['elements.d.ts', 'react.d.ts']) await fs.copyFile(path.join(dist, 'types', f), path.join(dir, 'src/types', f));
  for (const n of names) {
    const item = await json(path.join(registry, 'react/lucide', `${n}.json`));
    await fs.writeFile(path.join(dir, 'src/blocks', `${n}.tsx`), item.files[0].content);
  }
  await fs.writeFile(path.join(dir, 'src/main.tsx'), [
    ...names.map((n, i) => `import B${i} from "./blocks/${n}";`),
    'import { StrictMode } from "react";',
    'import { createRoot } from "react-dom/client";',
    `const blocks: Record<string, () => React.JSX.Element> = { ${names.map((n, i) => `"${n}": B${i}`).join(', ')} };`,
    'const Block = blocks[document.documentElement.dataset.block!];',
    'createRoot(document.body).render(<StrictMode><Block /></StrictMode>);',
  ].join('\n'));
  await fs.writeFile(path.join(dir, 'tsconfig.json'), JSON.stringify({
    compilerOptions: { strict: true, target: 'ES2022', module: 'ESNext', moduleResolution: 'Bundler', jsx: 'react-jsx', lib: ['ES2022', 'DOM', 'DOM.Iterable'], noEmit: true, types: [] },
    include: ['src'],
  }));
  // One page per block: the HTML page's head (stylesheets, external scripts,
  // no inline scripts or styles: the component brings those) and an empty body.
  for (const n of names) {
    const html = await fs.readFile(path.join(root, 'packages/blocks', `${n}.html`), 'utf8');
    let head = html.match(/<head>([\s\S]*?)<\/head>/)[1].replace(/<style>[\s\S]*?<\/style>/g, '').replace(/<script>([\s\S]*?)<\/script>/g, (m, s) => (s.includes('URLSearchParams') ? m : ''));
    const body = html.match(/<body[\s\S]*<\/body>/)[0];
    head += [...body.matchAll(/<script\s[^>]*src="[^"]+"[^>]*><\/script>/g)].map((m) => m[0]).join('');
    const attrs = html.match(/<body([^>]*)>/)[1];
    const lang = html.match(/<html([^>]*)>/)[1];
    await fs.writeFile(path.join(dir, `${n}.html`), `<!doctype html><html data-block="${n}"${lang}><head><base href="/packages/blocks/">${head}<script type="module" src="/packages/tests/.tmp/react-blocks/app.js"></script></head><body${attrs}></body></html>`);
  }
  server = await serve();
  b = await browser();
});
after(async () => {
  await b?.close();
  await server?.close();
});

test('React blocks type-check (strict)', () => {
  run(bin('tsc'), ['-p', dir]);
});

test('React blocks render like the HTML blocks', async () => {
  await build({ entryPoints: [path.join(dir, 'src/main.tsx')], bundle: true, format: 'esm', outfile: path.join(dir, 'app.js'), define: { 'process.env.NODE_ENV': '"development"' }, logLevel: 'error' });
  const failures = [];
  for (const n of names) {
    const errors = [];
    const d = await stableDiff(b, async () => {
      const shots = [];
      for (const [kind, url] of [['html', server.url(path.join(root, 'packages/blocks', `${n}.html`))], ['react', server.url(path.join(dir, `${n}.html`))]]) {
        const { page, errors: e } = await open(b, url);
        shots.push(await shot(page));
        // React's development build reports invalid markup as console errors.
        errors.push(...e.map((x) => `${kind}: ${x}`));
        await page.close();
      }
      return shots;
    });
    if (d.pixels > 0 || errors.length) { failures.push(`${n}: ${d.size ?? `${d.pixels} px`} ${[...new Set(errors)].join(' | ')}`); await keep(`react-${n}`, ...d.shots); }
  }
  assert.deepEqual(failures, []);
});

// The same action on both editions must leave the same picture.
const INTERACTIONS = [
  ['sidebar-07', (p) => p.click('[data-sidebar-toggle]')],
  ['sidebar-07', (p) => p.click('[popovertarget]')],
  ['sidebar-13', (p) => p.click('[commandfor]')],
  ['calendar-32', (p) => p.click('[commandfor]')],
  ['calendar-12', (p) => p.selectOption('#lang', { index: 2 })],
  ['calendar-22', (p) => p.click('auvyx-date-picker button, auvyx-date-picker input')],
  ['calendar-29', async (p) => { const i = p.locator('input').first(); await i.fill('next friday'); await i.press('Enter'); }],
  ['dashboard-01', (p) => p.click('[data-sidebar-toggle]')],
];

test('React blocks behave like the HTML blocks', async () => {
  const failures = [];
  for (const [n, act] of INTERACTIONS) {
    const errors = [];
    const d = await stableDiff(b, async () => {
      const shots = [];
      for (const url of [server.url(path.join(root, 'packages/blocks', `${n}.html`)), server.url(path.join(dir, `${n}.html`))]) {
        const { page, errors: e } = await open(b, url);
        await act(page);
        await page.waitForTimeout(700);
        shots.push(await shot(page, false));
        errors.push(...e);
        await page.close();
      }
      return shots;
    });
    if (d.pixels > 0 || errors.length) { failures.push(`${n} (${act}): ${d.size ?? `${d.pixels} px`} ${[...new Set(errors)].join(' | ')}`); await keep(`react-act-${n}`, ...d.shots); }
  }
  assert.deepEqual(failures, []);
});

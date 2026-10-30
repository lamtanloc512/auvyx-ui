// dist/ui/: the bundle split per component.
//  - every block renders identically with base.css + all component files;
//  - every component, installed with the CLI alone (its files, dependencies
//    and ui/index.css, no auvyx.min.css/js), renders its docs examples like
//    the full bundle, on load and after opening them;
//  - tools/ui-deps.json is up to date.
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { root, dist, registry, cli, freshDir, run, serve, browser, open, shot, stableDiff, keep, blockNames, componentDocs, requireBuild } from './lib/env.mjs';

// Rendering noise between two loads of the same page stays below this
// (antialiasing of images and text at sub-pixel offsets).
const NOISE = 300;

let server, b;
before(async () => {
  requireBuild();
  server = await serve();
  b = await browser();
});
after(async () => {
  await b?.close();
  await server?.close();
});

test('blocks render identically with the split files', async () => {
  const dir = await freshDir('split-blocks');
  const files = [];
  for (const f of await fs.readdir(path.join(dist, 'ui'))) {
    if (!f.endsWith('.css')) continue;
    const order = Number((await fs.readFile(path.join(dist, 'ui', f), 'utf8')).match(/order (\d+)/)[1]);
    files.push([order, f]);
  }
  files.sort((x, y) => x[0] - y[0]);
  const links = files.map(([, f]) => `<link rel="stylesheet" href="/packages/ui/dist/ui/${f}" />`).join('');
  const failures = [];
  for (const n of await blockNames()) {
    const html = await fs.readFile(path.join(root, 'packages/blocks', `${n}.html`), 'utf8');
    const split = html.replace('<link rel="stylesheet" href="../ui/dist/auvyx.min.css" />', links).replace('<head>', '<head><base href="/packages/blocks/">');
    assert.ok(split.includes(links), `${n}: bundle link not found`);
    await fs.writeFile(path.join(dir, `${n}.html`), split);
    const d = await stableDiff(b, async () => {
      const shots = [];
      for (const url of [server.url(path.join(root, 'packages/blocks', `${n}.html`)), server.url(path.join(dir, `${n}.html`))]) {
        const { page } = await open(b, url);
        shots.push(await shot(page));
        await page.close();
      }
      return shots;
    });
    if (d.pixels > 0) { failures.push(`${n}: ${d.size ?? `${d.pixels} px`}`); await keep(`split-${n}`, ...d.shots); }
  }
  assert.deepEqual(failures, []);
});

const TRIGGER = '[aria-haspopup]:not([disabled]), [popovertarget], [commandfor], [role=tab][aria-selected=false], details > summary, [data-sidebar-toggle]';
const PAGE_STYLE = '<style>.t-ex{padding:2rem;display:flex;flex-wrap:wrap;gap:1rem;align-items:center;justify-content:center;border-bottom:1px dashed #ccc}</style>';

test('components installed with the CLI render like the bundle', async () => {
  const dir = await freshDir('split-components');
  const docs = await componentDocs();
  const template = path.join(registry, '{framework}/{icons}/{name}.json');
  const bundle = `<link rel="stylesheet" href="/packages/ui/dist/auvyx.min.css"><script src="/packages/ui/dist/auvyx.min.js" defer></script>`;
  const failures = [];
  for (const [name, c] of Object.entries(docs)) {
    const project = path.join(dir, name);
    await fs.mkdir(project);
    run('node', [cli, 'init', '--registry', template], { cwd: project });
    const out = run('node', [cli, 'add', name], { cwd: project });
    const scripts = out.split('\n').map((l) => l.trim()).filter((l) => l.startsWith('<script'));
    const examples = c.examples.map((e) => `<section class="t-ex">${e.html}</section>`).join('\n');
    const page = (head) => `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">${head}${PAGE_STYLE}</head><body>${examples}</body></html>`;
    await fs.writeFile(path.join(project, 'full.html'), page(bundle));
    await fs.writeFile(path.join(project, 'installed.html'), page(`<link rel="stylesheet" href="auvyx/ui/index.css">${scripts.join('')}`));
    const errors = [];
    // One screenshot pair on load, one after opening the first trigger.
    const capture = (act) => async () => {
      const shots = [];
      for (const v of ['full', 'installed']) {
        const { page: p, errors: e } = await open(b, server.url(path.join(project, `${v}.html`)));
        if (act) {
          const trigger = p.locator(TRIGGER).filter({ visible: true }).first();
          if (await trigger.count()) {
            await trigger.click({ timeout: 3000 }).catch((err) => e.push(`click: ${err.message.split('\n')[0]}`));
            await p.waitForTimeout(600);
          }
        }
        shots.push(await shot(p, !act));
        errors.push(...e.map((x) => `${v}: ${x}`));
        await p.close();
      }
      return shots;
    };
    const d1 = await stableDiff(b, capture(false), { tolerance: NOISE });
    const d2 = await stableDiff(b, capture(true), { tolerance: NOISE });
    if (d1.pixels > NOISE || d2.pixels > NOISE || errors.length) {
      failures.push(`${name}: load ${d1.size ?? d1.pixels} px, after a click ${d2.size ?? d2.pixels} px ${[...new Set(errors)].join(' | ')}`);
      await keep(`component-${name}`, ...(d2.pixels > NOISE ? d2.shots : d1.shots));
    }
  }
  assert.deepEqual(failures, []);
});

test('tools/ui-deps.json is up to date', () => {
  run('node', [path.join(root, 'packages/ui/tools/ui-deps.mjs'), '--check']);
});

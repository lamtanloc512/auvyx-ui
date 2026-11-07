// The docs output: llms.txt links only to Markdown exports that exist, and
// every component's reference notes made it into its export.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { root, requireBuild } from './lib/env.mjs';

const out = path.join(root, 'packages/docs/out');
const SITE = 'https://ui.auvyx.org/';

test('llms.txt links to existing exports', async () => {
  requireBuild();
  const llms = await fs.readFile(path.join(out, 'llms.txt'), 'utf8');
  const links = [...llms.matchAll(/\]\((.+?)\)/g)].map((m) => m[1]);
  assert.ok(links.length > 60, 'llms.txt lists the guides and components');
  await fs.access(path.join(out, 'llms-full.txt'));
  for (const link of links) {
    assert.ok(link.startsWith(SITE), `${link} is on the site`);
    assert.match(link, /\.(md|json)$/, `${link} is a Markdown export or a registry index`);
    await fs.access(path.join(out, link.slice(SITE.length)));
  }
});

test('component reference notes are in the exports', async () => {
  for (const f of await fs.readdir(path.join(root, 'packages/docs/src/data/notes'))) {
    const md = await fs.readFile(path.join(out, 'md/components', f.replace(/\.html$/, '.md')), 'utf8');
    assert.match(md, /^## Usage$/m, `${f}: notes exported`);
  }
});

// The Create page's dialogs (Copy CSS, Open Preset, Initialize Project) must
// open on screen: a leftover translate from the page-enter animation once
// made each dialog the containing block of its fixed panel and collapsed it.
test('Create page dialogs open on screen', async () => {
  const { serve, browser, open } = await import('./lib/env.mjs');
  const server = await serve();
  const b = await browser();
  try {
    const { page, errors } = await open(b, server.url(path.join(out, 'index.html')) + '#create', { width: 1440, height: 900 });
    for (const [trigger, id] of [['[data-cr=show-css]', 'cr-css'], ['[commandfor=cr-open]', 'cr-open'], ['[data-cr=show-init]', 'cr-init']]) {
      await page.locator(`#cr-panel ${trigger}`).first().click();
      await page.waitForTimeout(400);
      const box = await page.evaluate((id) => document.querySelector(`#${id} > div`).getBoundingClientRect().toJSON(), id);
      assert.ok(box.top >= 0 && box.bottom <= 900 && box.height > 150, `${id} panel on screen: ${JSON.stringify(box)}`);
      await page.keyboard.press('Escape');
      await page.waitForTimeout(300);
    }
    assert.deepEqual(errors, []);
  } finally {
    await b.close();
    await server.close();
  }
});

test('Create page: theme presets and the theme editor restyle the preview', async () => {
  const { serve, browser, open } = await import('./lib/env.mjs');
  const server = await serve();
  const b = await browser();
  try {
    const { page, errors } = await open(b, server.url(path.join(out, 'index.html')) + '#create', { width: 1440, height: 900 });
    const frameVar = (name) => page.evaluate((n) => getComputedStyle(document.getElementById('cr-frame').contentDocument.documentElement).getPropertyValue(`--${n}`).trim(), name);
    const input = (sel, value) => page.$eval(sel, (el, v) => { el.value = v; el.dispatchEvent(new Event('input', { bubbles: true })); }, value);
    // A preset sets colors, font and radius together.
    await page.click('#cr-panel [popovertarget=cr-preset]');
    assert.ok((await page.locator('[data-preset]').count()) >= 10, 'at least ten presets');
    await page.click('[data-preset="0"]');
    await page.waitForTimeout(400);
    assert.equal(await frameVar('primary'), 'oklch(0.55 0.16 245)');
    assert.equal(await frameVar('radius'), '0.75rem');
    // The editor changes single tokens, sliders and shadows live.
    await page.click('#cr-panel [data-cr=edit]');
    await input('[data-tok=primary]', '#e11d48');
    await input('#cr-r-radius', '1.25');
    await input('#cr-r-sh-opacity', '0.4');
    await page.waitForTimeout(300);
    assert.match(await frameVar('primary'), /^oklch\(0\.586 0\.22\d? 17\.\d+\)$/);
    assert.equal(await frameVar('radius'), '1.25rem');
    assert.match(await frameVar('shadow-sm'), /\/ 0\.4\)/);
    // Dark mode edits the dark colors.
    await page.click('#cr-panel [data-cr=mode][data-mode=dark]');
    await page.waitForTimeout(400);
    assert.equal(await page.inputValue('[data-tok-text=primary]'), 'oklch(0.7 0.152 245)');
    // The exported CSS carries the edits and the @theme inline block for Tailwind source.
    await page.click('#cr-panel [data-cr=show-css]');
    const cssText = await page.locator('#cr-css-body').innerText();
    assert.match(cssText, /--radius: 1\.25rem;/);
    assert.match(cssText, /@theme inline \{\s+--shadow-2xs: var\(--shadow-2xs\);/);
    assert.deepEqual(errors, []);
  } finally {
    await b.close();
    await server.close();
  }
});

// tweakcn's full export starts with @import and `@custom-variant dark (&:is(.dark *));`: the
// :root block must still read as light, and the long paste must leave Apply on screen.
test('Create page: a full tweakcn export imports', async () => {
  const { serve, browser, open } = await import('./lib/env.mjs');
  const server = await serve();
  const b = await browser();
  try {
    const { page, errors } = await open(b, server.url(path.join(out, 'index.html')) + '#create', { width: 1440, height: 900 });
    const vars = (pairs) => pairs.map(([k, v]) => `  --${k}: ${v};`).join('\n');
    const light = [['background', 'oklch(0.985 0 0)'], ['primary', 'oklch(0.46 0.22 266)'], ['radius', '0.5rem'], ['font-sans', 'Geist, sans-serif']];
    const filler = Array.from({ length: 40 }, (_, i) => [`chart-x${i}`, 'oklch(0.5 0 0)']);
    const src = `@import "tailwindcss";\n\n@custom-variant dark (&:is(.dark *));\n\n:root {\n${vars([...light, ...filler])}\n}\n\n.dark {\n${vars([['background', 'oklch(0 0 0)'], ['primary', 'oklch(0.46 0.22 266)']])}\n}\n\n@theme inline {\n  --color-primary: var(--primary);\n}\n\n@layer base {\n  * {\n    @apply border-border outline-ring/50;\n  }\n}\n`;
    await page.locator('#cr-panel [commandfor=cr-import]').click();
    await page.fill('#cr-theme-src', src);
    const apply = page.locator('#cr-import [data-cr=import]');
    const box = await apply.boundingBox();
    assert.ok(box && box.y + box.height <= 900, `Apply on screen: ${JSON.stringify(box)}`);
    await apply.click();
    await page.waitForTimeout(800);
    const frameVar = (name) => page.frameLocator('#cr-frame').locator('html').evaluate((el, n) => getComputedStyle(el).getPropertyValue(`--${n}`).trim(), name);
    assert.equal(await frameVar('radius'), '0.5rem');
    assert.equal(await frameVar('primary'), 'oklch(0.46 0.22 266)');
    assert.equal(await frameVar('background'), 'oklch(0.985 0 0)');
    assert.deepEqual(errors, []);
  } finally {
    await b.close();
    await server.close();
  }
});

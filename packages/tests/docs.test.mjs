// The docs output: llms.txt links only to Markdown exports that exist, and
// every component's reference notes made it into its export.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { root, requireBuild } from './lib/env.mjs';

const out = path.join(root, 'packages/docs/out');
const SITE = 'https://auvyx-ui.vercel.app/';

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

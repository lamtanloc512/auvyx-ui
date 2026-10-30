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

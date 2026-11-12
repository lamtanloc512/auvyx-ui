// auvyx.ai.json: every component has a contract whose root really exists in
// its examples and in the CSS, and every component sits in one intent group.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { root, requireBuild } from './lib/env.mjs';

const out = path.join(root, 'packages/docs/out');

test('auvyx.ai.json covers every component, rooted in the examples and the CSS', async () => {
  requireBuild();
  const ai = JSON.parse(await fs.readFile(path.join(out, 'auvyx.ai.json'), 'utf8'));
  const comps = JSON.parse(await fs.readFile(path.join(root, 'packages/docs/src/data/components.json'), 'utf8'));
  const css = await fs.readFile(path.join(root, 'packages/ui/dist/auvyx.min.css'), 'utf8');
  const names = ai.components.map((c) => c.name);

  assert.deepEqual([...names].sort(), Object.keys(comps).sort(), 'one contract per component');
  const grouped = Object.values(ai.groups).flat();
  assert.deepEqual([...grouped].sort(), [...names].sort(), 'every component is in exactly one group');
  assert.ok(ai.rules.length >= 8, 'design rules are included');

  const problems = [];
  for (const c of ai.components) {
    if (!c.root?.selector) { problems.push(`${c.name}: no root selector`); continue; }
    if (!c.snippet) problems.push(`${c.name}: no snippet`);
    const cls = c.root.class;
    if (cls) {
      if (!new RegExp(`\\.${cls}(?![\\w-])`).test(css)) problems.push(`${c.name}: .${cls} is not in auvyx.min.css`);
      const used = [c.snippet, ...comps[c.name].examples.map((ex) => ex.html)].some((html) => new RegExp(`class="([^"]* )?${cls}( [^"]*)?"`).test(html));
      if (!used) problems.push(`${c.name}: neither the snippet nor an example uses .${cls}`);
    }
    for (const [k, v] of Object.entries(c.attributes)) {
      if (!k.startsWith('data-')) problems.push(`${c.name}: attribute ${k} is not data-*`);
      if (v.length > 16) problems.push(`${c.name}: ${k} lists ${v.length} values`);
    }
    if (c.element && !c.element.tag.startsWith('auvyx-')) problems.push(`${c.name}: element ${c.element.tag}`);
  }
  assert.deepEqual(problems, []);
});

// The prefixed build (dist/ax/, packages/ui/tools/prefix.mjs): every class prefixed ax- in the CSS and wherever the JS
// names a class, nothing else.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import postcss from 'postcss';
import { mapSelectorClasses, prefixCss, prefixJs } from '../ui/tools/prefix.mjs';

const ui = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../ui');
const read = (f) => fs.readFileSync(path.join(ui, f), 'utf8');
const ax = (n) => `ax-${n}`;

test('selectors: classes renamed, attributes, strings and escapes kept', () => {
  const r = (s) => mapSelectorClasses(s, ax);
  assert.equal(r('.btn:hover > .card'), '.ax-btn:hover > .ax-card');
  assert.equal(r('dialog.command[data-x=".no"]'), 'dialog.ax-command[data-x=".no"]');
  assert.equal(r('.px-2\\.5'), '.ax-px-2\\.5');
  assert.equal(r(':is(.dark *) .x'), ':is(.ax-dark *) .ax-x');
});

test('CSS: dark kept, keyframes untouched, other classes prefixed', () => {
  const { css, classes } = prefixCss('.dark .btn{a:b}@keyframes spin{from{c:d}}.card .card-title{e:f}');
  assert.equal(css, '.dark .ax-btn{a:b}@keyframes spin{from{c:d}}.ax-card .ax-card-title{e:f}');
  assert.deepEqual([...classes].sort(), ['btn', 'card', 'card-title']);
});

test('JS: selectors, class lists and generated markup renamed; event names and prose kept', () => {
  const classes = new Set(['tabs', 'input', 'select', 'active', 'toast', 'chart']);
  const src = [
    "el.querySelector('.tabs > button');",
    "el.classList.add('active');",
    "el.addEventListener('input', f); el.addEventListener('select', g);",
    "box.className = 'toast';",
    "x.innerHTML = `<div class=\"toast\">${t}</div>`;",
    "register('tabs', '.tabs:not([data-tabs-initialized])', init);",
    "throw new Error('Chart.js is required before calling basecoat.chart().');",
    "list.filter((className) => className !== 'chart');",
  ].join('\n');
  const out = prefixJs(src, classes);
  assert.match(out, /querySelector\("\.ax-tabs > button"\)/);
  assert.match(out, /classList\.add\("ax-active"\)/);
  assert.match(out, /addEventListener\('input', f\); el\.addEventListener\('select', g\)/);
  assert.match(out, /className = "ax-toast"/);
  assert.match(out, /class="ax-toast"/);
  assert.match(out, /register\('tabs', "\.ax-tabs:not/);
  assert.match(out, /basecoat\.chart\(\)/);
  assert.match(out, /className !== "ax-chart"/);
});

test('dist/ax: no class left unprefixed (dark aside), JS registers prefixed selectors', () => {
  for (const file of ['dist/ax/auvyx.min.css', ...fs.readdirSync(path.join(ui, 'dist/ax/styles')).map((f) => `dist/ax/styles/${f}`)]) {
    const loose = new Set();
    postcss.parse(read(file)).walkRules((rule) => {
      if (rule.parent?.type === 'atrule' && /keyframes$/.test(rule.parent.name)) return;
      mapSelectorClasses(rule.selector, (c) => { if (!c.startsWith('ax-') && c !== 'dark') loose.add(c); return null; });
    });
    assert.deepEqual([...loose], [], file);
  }
  const js = read('dist/ax/auvyx.js');
  assert.match(js, /"\.ax-tabs:not\(\[data-tabs-initialized\]\)"/);
  assert.doesNotMatch(js, /['"]\.tabs:not/);
});

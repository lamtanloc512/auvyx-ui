// Find each component's dependencies for dist/ui/ and write tools/ui-deps.json.
//
//   node packages/ui/build.mjs && node packages/ui/tools/ui-deps.mjs [--check]
//
// For every component, its docs examples are rendered in Chromium with
// base.css and every component's CSS as separate stylesheets (and
// auvyx.min.js). A component is a dependency when one of its rules matches an
// element in the examples, ignoring states (:hover, :checked, open…) so rules
// for those count too. The result is what the examples need to render as on
// the docs. Run it again when components or examples change; the ui build
// reads the JSON (and warns about components missing from it). --check writes
// nothing and exits 1 when the JSON is out of date (CI runs it).
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../..');
const dist = path.join(root, 'packages/ui/dist');
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const docs = JSON.parse(await fs.readFile(path.join(root, 'packages/docs/src/data/components.json'), 'utf8'));
const { components } = JSON.parse(await fs.readFile(path.join(dist, 'ui/manifest.json'), 'utf8'));
const cssFiles = Object.values(components).flatMap((c) => c.css).map((f) => path.basename(f, '.css'));
const sheets = await Promise.all(['base', ...cssFiles].map(async (k) => [k, await fs.readFile(path.join(dist, 'ui', `${k}.css`), 'utf8')]));
const tmp = path.join(root, 'packages/ui/.tmp/deps');
await fs.mkdir(tmp, { recursive: true });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
const deps = {};
for (const name of Object.keys(components)) {
  const examples = (docs[name]?.examples ?? []).map((e) => `<section>${e.html}</section>`).join('\n');
  // Inline, so the page may read the rules (file:// stylesheets are opaque).
  const links = sheets.map(([k, css]) => `<style data-k="${k}">${css}</style>`).join('');
  const file = path.join(tmp, `${name}.html`);
  await fs.writeFile(file, `<!doctype html><html><head>${links}<script src="${path.join(dist, 'auvyx.min.js')}" defer></script></head><body>${examples}</body></html>`);
  await page.goto(`file://${file}`, { waitUntil: 'load' });
  await page.waitForTimeout(300);
  const used = await page.evaluate(() => {
    // Drop pseudo-elements and state pseudo-classes, keep structural ones.
    const STATE = /::?(?:before|after|placeholder|marker|backdrop|selection|file-selector-button|details-content|picker\([^)]*\)|picker-icon|checkmark|scroll-marker|scroll-button\([^)]*\)|column|-webkit-[\w-]+|-moz-[\w-]+)|:(?:hover|focus|focus-visible|focus-within|active|checked|disabled|enabled|invalid|valid|user-invalid|open|popover-open|modal|indeterminate|placeholder-shown|target|visited|link|any-link|autofill|read-only|read-write|default|required|optional|in-range|out-of-range|empty|state\([^)]*\))/g;
    const matches = (sel) => {
      // Top-level commas only: :is(a, b) stays one part.
      const parts = [];
      let depth = 0, start = 0;
      for (let i = 0; i < sel.length; i++) {
        if (sel[i] === '(' || sel[i] === '[') depth++;
        else if (sel[i] === ')' || sel[i] === ']') depth--;
        else if (sel[i] === ',' && depth === 0) { parts.push(sel.slice(start, i)); start = i + 1; }
      }
      parts.push(sel.slice(start));
      for (const part of parts) {
        const s = part.replace(STATE, '').replace(/:(?:is|where|not|has)\(\s*\)/g, '').trim() || '*';
        // Page-level rules (tokens on :root, html, body) say nothing about the examples.
        if (/^(?::root|html|body|\*|\.dark)(?:[\s>~+]*(?::root|html|body|\*|\.dark))*$/.test(s)) continue;
        try { if (document.querySelector(s.replace(/>\s*$/, ''))) return true; } catch { /* selectors the browser cannot query */ }
      }
      return false;
    };
    const walk = (rules, parent = '') => {
      for (const r of rules) {
        if (r.selectorText !== undefined) {
          // Nested rules: resolve & against the parent selector.
          const sel = parent && r.selectorText.includes('&') ? r.selectorText.replaceAll('&', `:is(${parent})`) : parent && !r.selectorText.includes('&') ? `:is(${parent}) ${r.selectorText}` : r.selectorText;
          if (matches(sel)) return true;
          if (r.cssRules?.length && walk(r.cssRules, sel)) return true;
        } else if (r.cssRules && walk(r.cssRules, parent)) return true;
      }
      return false;
    };
    return [...document.querySelectorAll('style[data-k]')].filter((l) => l.sheet && walk(l.sheet.cssRules)).map((l) => l.dataset.k);
  });
  // popover.native.css belongs to popover.
  deps[name] = [...new Set(used.map((k) => k.split('.')[0]))].filter((k) => k !== 'base' && k !== name).sort();
}
await browser.close();
await fs.rm(path.join(root, 'packages/ui/.tmp'), { recursive: true, force: true });
const json = JSON.stringify(deps, null, 2) + '\n';
if (process.argv.includes('--check')) {
  const saved = await fs.readFile(path.join(here, 'ui-deps.json'), 'utf8').catch(() => '');
  if (saved !== json) {
    const old = saved ? JSON.parse(saved) : {};
    for (const k of new Set([...Object.keys(old), ...Object.keys(deps)])) {
      if (JSON.stringify(old[k]) !== JSON.stringify(deps[k])) console.error(`${k}: recorded ${JSON.stringify(old[k] ?? null)}, found ${JSON.stringify(deps[k] ?? null)}`);
    }
    console.error('ui-deps.json is out of date: run node packages/ui/tools/ui-deps.mjs');
    process.exit(1);
  }
  console.log(`ui-deps.json is up to date (${Object.keys(deps).length} components)`);
} else {
  await fs.writeFile(path.join(here, 'ui-deps.json'), json);
  console.log(Object.entries(deps).map(([k, v]) => `${k}: ${v.join(' ')}`).join('\n'));
}

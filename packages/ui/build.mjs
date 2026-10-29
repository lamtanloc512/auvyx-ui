// Build @auvyx/ui: one CSS file + one optional JS file, Bootstrap-style.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { gzipSync } from 'node:zlib';
import { transform, build } from 'esbuild';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const dist = path.join(here, 'dist');
// Same browser baseline as upstream (Tailwind v4). esbuild minifies because
// Lightning CSS --minify can drop rules (parcel-bundler/lightningcss#1235).
const cssTargets = ['chrome111', 'safari16.4', 'firefox128'];

// JS is behavior-only and opt-in. accordion/popover are excluded: the native
// variants in src/css/native/ cover them without JS. chart needs Chart.js.
const jsComponents = ['basecoat', 'combobox', 'command', 'copy', 'drawer', 'dropdown-menu', 'range', 'select', 'sidebar', 'tabs', 'toast'];

// Size budgets (gzip bytes). CI fails when a change blows past them.
// CSS budget sized for the full shadcn component set (~61 components); tighten once complete.
const budgets = { 'auvyx.min.css': 36_000, 'auvyx.min.js': 12_000 };

await fs.rm(dist, { recursive: true, force: true });
await fs.mkdir(dist, { recursive: true });

// CSS
const cssOut = path.join(dist, 'auvyx.css');
execFileSync(path.join(root, 'node_modules/.bin/tailwindcss'), ['-i', path.join(here, 'src/auvyx.css'), '-o', cssOut], { stdio: 'inherit' });
const { code: minCss, warnings } = await transform(await fs.readFile(cssOut, 'utf8'), { loader: 'css', minify: true, target: cssTargets });
if (warnings.length) throw new Error(warnings.map((w) => w.text).join('; '));
const { version } = JSON.parse(await fs.readFile(path.join(here, 'package.json'), 'utf8'));
const banner = `/*! @auvyx/ui v${version} | MIT | based on Basecoat (MIT) */\n`;
await fs.writeFile(path.join(dist, 'auvyx.min.css'), banner + minCss);

// JS: concatenate the IIFE sources, then minify as one script.
const jsSrc = (await Promise.all(jsComponents.map((c) => fs.readFile(path.join(root, 'src/js', `${c}.js`), 'utf8')))).join('\n');
await fs.writeFile(path.join(dist, 'auvyx.js'), banner + jsSrc);
const { code: minJs } = await transform(jsSrc, { loader: 'js', minify: true, target: 'es2020' });
await fs.writeFile(path.join(dist, 'auvyx.min.js'), banner + minJs);

// Source channel: inline every relative @import of auvyx.source.css into one
// uncompiled file for projects that already run Tailwind v4.
async function inline(file, seen = new Set()) {
  const abs = path.resolve(file);
  if (seen.has(abs)) return '';
  seen.add(abs);
  const out = [];
  for (const line of (await fs.readFile(abs, 'utf8')).split('\n')) {
    const m = line.match(/^\s*@import\s+["'](\.{1,2}\/[^"']+)["']\s*;\s*$/);
    out.push(m ? (await inline(path.join(path.dirname(abs), m[1]), seen)).replace(/\n+$/, '') : line);
  }
  return out.join('\n');
}
const bundleHeader = `/*! @auvyx/ui v${version} source bundle | MIT | import after "tailwindcss" */\n`;
await fs.writeFile(path.join(dist, 'auvyx.bundle.css'), bundleHeader + (await inline(path.join(here, 'src/auvyx.source.css'))));

// Report + budgets
let failed = false;
for (const [file, limit] of Object.entries(budgets)) {
  const buf = await fs.readFile(path.join(dist, file));
  const gz = gzipSync(buf, { level: 9 }).length;
  const ok = gz <= limit;
  failed ||= !ok;
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${file.padEnd(16)} ${(buf.length / 1024).toFixed(1).padStart(7)} kB raw  ${(gz / 1024).toFixed(1).padStart(6)} kB gzip  (budget ${(limit / 1024).toFixed(0)} kB)`);
}
if (failed) process.exit(1);

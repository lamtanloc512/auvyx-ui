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

// JS is behavior-only and opt-in. accordion/popover are kept for upstream
// markup; they skip the native variants (src/css/native/), which need no JS.
// chart ships separately (auvyx.chart.min.js) because it needs Chart.js.
const jsComponents = ['basecoat', 'accordion', 'combobox', 'command', 'copy', 'drawer', 'dropdown-menu', 'popover', 'range', 'select', 'sidebar', 'tabs', 'toast'];

// Size budgets (gzip bytes). CI fails when a change blows past them.
// CSS budget sized for the full shadcn component set (~61 components); tighten once complete.
const budgets = { 'auvyx.min.css': 41_000, 'auvyx.min.js': 24_000 };


// Tailwind inlines shadow values; route them through --shadow-* so themes from
// tweakcn / the shadcn generator (which define --shadow-2xs … --shadow-2xl) apply.
// Unset vars fall back to the original value, so nothing changes by default.
const SHADOWS = [['2xs', /^0 1px var\(/], ['xs', /^0 1px 2px 0 /], ['sm', /^0 1px 3px 0 /], ['md', /^0 4px 6px -1px /],
  ['lg', /^0 10px 15px -3px /], ['xl', /^0 20px 25px -5px /], ['2xl', /^0 25px 50px -12px /]];
function linkShadows(css) {
  return css.replace(/--tw-shadow:\s*([^;}]+)/g, (all, value) => {
    const v = value.trim();
    const hit = SHADOWS.find(([, re]) => re.test(v));
    return hit ? `--tw-shadow: var(--shadow-${hit[0]}, ${v})` : all;
  });
}

await fs.rm(dist, { recursive: true, force: true });
await fs.mkdir(dist, { recursive: true });

// CSS
const cssOut = path.join(dist, 'auvyx.css');
execFileSync(path.join(root, 'node_modules/.bin/tailwindcss'), ['-i', path.join(here, 'src/auvyx.css'), '-o', cssOut], { stdio: 'inherit' });
await fs.writeFile(cssOut, linkShadows(await fs.readFile(cssOut, 'utf8')));
const { code: minCss, warnings } = await transform(await fs.readFile(cssOut, 'utf8'), { loader: 'css', minify: true, target: cssTargets });
if (warnings.length) throw new Error(warnings.map((w) => w.text).join('; '));
const { version } = JSON.parse(await fs.readFile(path.join(here, 'package.json'), 'utf8'));
const banner = `/*! @auvyx/ui v${version} | MIT | based on Basecoat (MIT) */\n`;
await fs.writeFile(path.join(dist, 'auvyx.min.css'), banner + minCss);

// JS: concatenate the IIFE sources, then minify as one script.
const basecoatJs = (await Promise.all(jsComponents.map((c) => fs.readFile(path.join(root, 'src/js', `${c}.js`), 'utf8')))).join('\n');
// Light-DOM custom elements (@auvyx/elements), bundled as one IIFE.
const elements = await build({ entryPoints: [path.join(root, 'packages/elements/src/index.js')], bundle: true, format: 'iife', write: false, target: 'es2022' });
const jsSrc = `${basecoatJs}\n${elements.outputFiles[0].text}`;
await fs.writeFile(path.join(dist, 'auvyx.js'), banner + jsSrc);
const { code: minJs } = await transform(jsSrc, { loader: 'js', minify: true, target: 'es2022' });
await fs.writeFile(path.join(dist, 'auvyx.min.js'), banner + minJs);

// Style packs: the same bundle built on each Basecoat style pack (Create page / opt-in).
// Fork-added components keep Vega visuals for now (see TODO.md).
{
  const styles = ['vega', 'nova', 'maia', 'lyra', 'mira', 'luma', 'sera', 'rhea'];
  const tmp = path.join(here, '.tmp');
  await fs.mkdir(tmp, { recursive: true });
  await fs.mkdir(path.join(dist, 'styles'), { recursive: true });
  for (const style of styles) {
    const entry = path.join(tmp, `auvyx-${style}.css`);
    await fs.writeFile(entry, [
      '@import "tailwindcss" source(none);',
      `@import "../../../src/css/basecoat-${style}.css";`,
      '@import "../../../src/css/extra/index.css";',
      '@import "../../../src/css/native/index.css";',
      '@import "../../../src/css/layout/index.css";',
      '@import "../src/themes.css";',
    ].join('\n'));
    const raw = path.join(tmp, `auvyx-${style}.out.css`);
    execFileSync(path.join(root, 'node_modules/.bin/tailwindcss'), ['-i', entry, '-o', raw], { stdio: 'ignore' });
    const { code } = await transform(linkShadows(await fs.readFile(raw, 'utf8')), { loader: 'css', minify: true, target: cssTargets });
    await fs.writeFile(path.join(dist, 'styles', `auvyx-${style}.min.css`), banner + code);
  }
}

// Corners fallback (Monoco, bundled): only acts where CSS corner-shape is unsupported.
{
  const out = await build({ entryPoints: [path.join(root, 'packages/elements/src/corners.js')], bundle: true, format: 'iife', minify: true, write: false, target: 'es2020' });
  await fs.writeFile(path.join(dist, 'auvyx.corners.min.js'), `/*! @auvyx/ui corners | MIT | includes Monoco (MIT, Monokai) */\n` + out.outputFiles[0].text);
}

// Chart runtime (needs Chart.js + auvyx.min.js): separate so pages without charts skip it.
{
  const { code } = await transform(await fs.readFile(path.join(root, 'src/js/chart.js'), 'utf8'), { loader: 'js', minify: true, target: 'es2020' });
  await fs.writeFile(path.join(dist, 'auvyx.chart.min.js'), banner + code);
}

// Elements as standalone ES modules, for picking only what a page uses.
await fs.mkdir(path.join(dist, 'elements'), { recursive: true });
for (const file of await fs.readdir(path.join(root, 'packages/elements/src'))) {
  if (file === 'corners.js') continue; // bundled with Monoco as auvyx.corners.min.js
  const { code } = await transform(await fs.readFile(path.join(root, 'packages/elements/src', file), 'utf8'), { loader: 'js', minify: true, format: 'esm', target: 'es2022' });
  const relinked = code.replace(/(["'])\.\/([\w-]+)\.js\1/g, '$1./$2.min.js$1');
  await fs.writeFile(path.join(dist, 'elements', file.replace(/\.js$/, '.min.js')), banner + relinked);
}

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

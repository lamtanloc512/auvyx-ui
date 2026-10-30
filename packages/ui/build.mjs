// Build @auvyx/ui: one CSS file + one optional JS file, Bootstrap-style.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { gzipSync } from 'node:zlib';
import { transform, build } from 'esbuild';
import { writeTypes } from './tools/types.mjs';
import { splitCss } from './tools/ui-split.mjs';
import { ELEMENTS } from '../elements/api.mjs';

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
      '@import "../../../src/css/layout/index.css";',
      '@import "../../../src/css/motion/index.css";',
      `@import "../../../src/css/basecoat-${style}.css";`,
      '@import "../../../src/css/extra/index.css";',
      '@import "../../../src/css/native/index.css";',
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

// Per-component JS modules: load only the behavior a page uses.
// Each file is a classic script that works on its own: Basecoat components
// carry the core registry (skipped when another module already set it up),
// elements carry their dependencies. `detect` finds a module's components in a
// page once it has run; the docs use it to label pages that need JavaScript.
// `kind: "enhance"` modules are optional: the markup works without them.
const JS_MODULES = {
  accordion: { src: 'src/js/accordion.js', core: true, detect: '[data-accordion-initialized]', note: 'Only for the upstream markup; <details name> accordions need no JS.' },
  combobox: { src: 'src/js/combobox.js', core: true, detect: '[data-combobox-initialized]' },
  command: { src: 'src/js/command.js', core: true, detect: '[data-command-initialized]' },
  drawer: { src: 'src/js/drawer.js', core: true, detect: '[data-drawer-initialized]' },
  'dropdown-menu': { src: 'src/js/dropdown-menu.js', core: true, detect: '[data-dropdown-menu-initialized]', note: 'Only for the upstream markup; the native popover variant needs no JS.' },
  popover: { src: 'src/js/popover.js', core: true, detect: '[data-popover-initialized]', note: 'Only for the upstream markup; the native popover variant needs no JS.' },
  select: { src: 'src/js/select.js', core: true, detect: '[data-select-initialized]' },
  sidebar: { src: 'src/js/sidebar.js', core: true, detect: '[data-sidebar-initialized]' },
  slider: { src: 'src/js/range.js', core: true, detect: '[data-range-initialized]' },
  tabs: { src: 'src/js/tabs.js', core: true, detect: '[data-tabs-initialized]' },
  // Toast demos call the page's #toaster, which sits outside the demo.
  toast: { src: 'src/js/toast.js', core: true, detect: '[data-toaster-initialized], [data-toast-initialized], [onclick*="toast("], [hx-target="#toaster"]' },
  copy: { src: 'src/js/copy.js', detect: '[data-copy]' },
  calendar: { src: 'packages/elements/src/calendar.js', element: true, detect: 'auvyx-calendar' },
  'context-menu': { src: 'packages/elements/src/context-menu.js', element: true, detect: 'auvyx-context-menu' },
  'data-table': { src: 'packages/elements/src/data-table.js', element: true, detect: 'auvyx-data-table' },
  'date-picker': { src: 'packages/elements/src/date-picker.js', element: true, detect: 'auvyx-date-picker' },
  resizable: { src: 'packages/elements/src/resizable.js', element: true, detect: 'auvyx-resizable' },
  menu: { src: 'packages/elements/src/menu.js', element: true, kind: 'enhance', detect: '[data-popover][popover]:has([role="menu"]), .navigation-menu', note: 'Adds arrow-key navigation and focus handling to native menus; they open and close without it.' },
};
{
  const core = await fs.readFile(path.join(root, 'src/js/basecoat.js'), 'utf8');
  if (!core.trimStart().startsWith('(() => {')) throw new Error('basecoat.js must start with its IIFE so modules can guard it');
  await fs.mkdir(path.join(dist, 'js'), { recursive: true });
  const manifest = {};
  for (const [name, mod] of Object.entries(JS_MODULES)) {
    let src;
    if (mod.element) {
      src = (await build({ entryPoints: [path.join(root, mod.src)], bundle: true, format: 'iife', write: false, target: 'es2022' })).outputFiles[0].text;
    } else {
      src = await fs.readFile(path.join(root, mod.src), 'utf8');
      // Core once per page, then this component; init right away when loaded after the DOM is ready.
      if (mod.core) src = `if (!window.basecoat) ${core.trim()}
${src}
if (document.readyState !== 'loading') { window.basecoat.initAll(); window.basecoat.start(); }`;
    }
    const { code } = await transform(src, { loader: 'js', minify: true, target: 'es2022' });
    const file = `js/${name}.min.js`;
    await fs.writeFile(path.join(dist, file), banner + code);
    manifest[name] = { file, kind: mod.kind || 'required', detect: mod.detect, gzip: gzipSync(banner + code, { level: 9 }).length, ...(mod.note && { note: mod.note }) };
  }
  await fs.writeFile(path.join(dist, 'js/manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
}

// Web Components edition: <auvyx-*> wrappers (packages/elements/src/wc) around
// the HTML edition's markup. Each file carries the core, the component's
// behavior and the element, so one script is enough. The HTML edition above
// is unchanged; this is an opt-in layer for frameworks.
const WC_MODULES = {
  tabs: { behavior: 'src/js/tabs.js', element: 'packages/elements/src/wc/tabs.js', tag: 'auvyx-tabs' },
  select: { behavior: 'src/js/select.js', element: 'packages/elements/src/wc/select.js', tag: 'auvyx-select' },
  combobox: { behavior: 'src/js/combobox.js', element: 'packages/elements/src/wc/combobox.js', tag: 'auvyx-combobox' },
  command: { behavior: 'src/js/command.js', element: 'packages/elements/src/wc/command.js', tag: 'auvyx-command' },
  'dropdown-menu': { behavior: 'src/js/dropdown-menu.js', element: 'packages/elements/src/wc/dropdown-menu.js', tag: 'auvyx-dropdown-menu' },
  popover: { behavior: 'src/js/popover.js', element: 'packages/elements/src/wc/popover.js', tag: 'auvyx-popover' },
  accordion: { behavior: 'src/js/accordion.js', element: 'packages/elements/src/wc/accordion.js', tag: 'auvyx-accordion' },
  sidebar: { behavior: 'src/js/sidebar.js', element: 'packages/elements/src/wc/sidebar.js', tag: 'auvyx-sidebar' },
  toast: { behavior: 'src/js/toast.js', element: 'packages/elements/src/wc/toaster.js', tag: 'auvyx-toaster' },
  slider: { behavior: 'src/js/range.js', element: 'packages/elements/src/wc/slider.js', tag: 'auvyx-slider' },
  drawer: { behavior: 'src/js/drawer.js', element: 'packages/elements/src/wc/drawer.js', tag: 'auvyx-drawer' },
};
{
  const core = await fs.readFile(path.join(root, 'src/js/basecoat.js'), 'utf8');
  await fs.mkdir(path.join(dist, 'wc'), { recursive: true });
  const manifest = {};
  for (const [name, mod] of Object.entries(WC_MODULES)) {
    const element = (await build({ entryPoints: [path.join(root, mod.element)], bundle: true, format: 'iife', write: false, target: 'es2022' })).outputFiles[0].text;
    const behavior = await fs.readFile(path.join(root, mod.behavior), 'utf8');
    const src = `if (!window.basecoat) ${core.trim()}\n${behavior}\n${element}`;
    const { code } = await transform(src, { loader: 'js', minify: true, target: 'es2022' });
    const file = `wc/${name}.min.js`;
    await fs.writeFile(path.join(dist, file), banner + code);
    const el = ELEMENTS.find((e) => e.tag === mod.tag);
    const api = {
      props: Object.fromEntries(el.properties.map((p) => [p.name, p.description])),
      events: Object.fromEntries(el.events.map((e) => [e.name, e.description])),
      methods: Object.fromEntries((el.methods || []).map((m) => [`${m.name}${m.signature.split(' =>')[0]}`, m.description])),
    };
    manifest[name] = { file, tag: mod.tag, api, gzip: gzipSync(banner + code, { level: 9 }).length };
  }
  await fs.writeFile(path.join(dist, 'wc/manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
}

// Custom Elements Manifest and TypeScript types (DOM, React 19, Vue 3) from packages/elements/api.mjs.
await writeTypes(dist, version);

// Per-component files (dist/ui/): the bundle's CSS split per component, each
// component's behavior as readable JS, and a manifest with dependencies.
// `auvyx add <component>` installs these (see packages/blocks/tools/build_registry.mjs).
{
  const docs = JSON.parse(await fs.readFile(path.join(root, 'packages/docs/src/data/components.json'), 'utf8'));
  const names = [...Object.keys(docs), 'chart'];
  const sizes = await splitCss(root, dist, names, linkShadows);
  // Behavior per component, from the same sources as dist/js/ (not minified).
  const UI_JS = { 'code-block': ['copy'], menubar: ['menu'], 'navigation-menu': ['menu'], 'range-calendar': ['calendar'] };
  const jsFor = (name) => UI_JS[name] ?? (JS_MODULES[name] ? [name] : []);
  const core = await fs.readFile(path.join(root, 'src/js/basecoat.js'), 'utf8');
  for (const mod of new Set(names.flatMap(jsFor))) {
    const m = JS_MODULES[mod];
    let src;
    if (m.element) src = (await build({ entryPoints: [path.join(root, m.src)], bundle: true, format: 'iife', write: false, target: 'es2022' })).outputFiles[0].text;
    else {
      src = await fs.readFile(path.join(root, m.src), 'utf8');
      if (m.core) src = `// Basecoat core, once per page.\nif (!window.basecoat) ${core.trim()}\n\n${src.trim()}\n\n// Loaded after the DOM is ready: initialize now.\nif (document.readyState !== 'loading') { window.basecoat.initAll(); window.basecoat.start(); }\n`;
    }
    await fs.writeFile(path.join(dist, 'ui', `${mod}.js`), `/* @auvyx/ui v${version} | MIT | based on Basecoat (MIT) */\n${src}`);
  }
  // Dependencies: the components whose rules the examples use (tools/ui-deps.mjs finds them in a browser).
  const deps = JSON.parse(await fs.readFile(path.join(here, 'tools/ui-deps.json'), 'utf8'));
  const stale = names.filter((n) => !deps[n]);
  if (stale.length) console.warn(`ui: no dependencies recorded for ${stale.join(', ')}; run node packages/ui/tools/ui-deps.mjs`);
  const manifest = {};
  for (const name of names) {
    manifest[name] = {
      // The component's file, then its zero-JS variant's (popover.native.css…).
      css: Object.keys(sizes).filter((f) => f === name || f.startsWith(`${name}.`)).map((f) => `ui/${f}.css`),
      js: jsFor(name).map((m) => `ui/${m}.js`),
      dependencies: deps[name] ?? [],
    };
  }
  await fs.writeFile(path.join(dist, 'ui/manifest.json'), JSON.stringify({ base: 'ui/base.css', components: manifest }, null, 2) + '\n');
}

// Elements as standalone ES modules, for picking only what a page uses.
await fs.mkdir(path.join(dist, 'elements'), { recursive: true });
for (const file of await fs.readdir(path.join(root, 'packages/elements/src'))) {
  if (file === 'corners.js' || file === 'wc') continue; // corners: bundled with Monoco; wc: the Web Components edition above
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

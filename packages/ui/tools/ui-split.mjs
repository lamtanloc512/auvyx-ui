// Split the compiled CSS into one file per component: dist/ui/<name>.css,
// plus dist/ui/base.css (preflight, theme, tokens, themes, motion, layout and
// the rules every component shares). Together they are exactly auvyx.css.
//
// The CSS is compiled once, from a copy of the sources with a marker rule at
// the start of each component's piece; the output is then cut at the markers.
// So every rule is compiled as in the bundle and lands in exactly one file.
// Pieces are whole source files, or sections of a file starting at one of
// its `/* Title */` comments (style packs, chat.css, menus.css).
import fs from 'node:fs/promises';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

// Structure files whose name is not the component's.
const FILES = {
  'components/collapsible.css': 'base', // styles every <details>
  'components/radio.css': 'radio-group',
  'components/range.css': 'slider',
  'components/scrollbar.css': 'scroll-area',
  'extra/components/web-components.css': 'base',
  'base/base.css': 'base',
  'motion/index.css': 'base',
  'layout/index.css': 'base',
  'extra/tokens.css': 'base',
  // The zero-JS variants cascade after every component: files of their own.
  'native/popover.css': 'popover.native',
  'native/accordion.css': 'accordion.native',
  'native/dialog.css': 'dialog.native',
};
// Files split at section comments: title (text before any ':') -> component.
const SECTIONS = {
  'styles/vega.css': { Radio: 'radio-group', Slider: 'slider' },
  'extra/styles/vega.css': {
    'Toggle Group': 'toggle-group', 'Copy feedback': 'code-block', 'Native menu items': 'base',
    'Sidebar extensions': 'sidebar', Typography: 'typography',
  },
  'extra/components/chat.css': { 'Shimmer for in-progress text (trace running, attachment uploading)': 'base' },
  'extra/components/menus.css': { 'Native menus': 'base' },
};
const slug = (title) => title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const MARK = 'auvyx-split';
const marker = (key) => `.${MARK}[data-key="${key}"] { --${MARK}: 1; }`;

// Titles that open a section in a split file: the configured ones, and any
// whose slug is a component name.
function sectionKey(file, line, components) {
  const m = line.match(/^ {0,2}\/\* (.+?) \*\/$/);
  if (!m) return null;
  const map = SECTIONS[file];
  const full = m[1];
  const title = full.split(':')[0];
  return map[full] ?? map[title] ?? (components.has(slug(title)) ? slug(title) : null);
}

async function copyTree(from, to, transform) {
  for (const entry of await fs.readdir(from, { withFileTypes: true })) {
    const src = path.join(from, entry.name);
    const dst = path.join(to, entry.name);
    if (entry.isDirectory()) await copyTree(src, dst, transform);
    else {
      await fs.mkdir(to, { recursive: true });
      await fs.writeFile(dst, transform(src, await fs.readFile(src, 'utf8')));
    }
  }
}

// Top-level statements of compiled CSS: { head, body } blocks and `head;` statements.
function statements(css) {
  const out = [];
  let depth = 0, start = 0, quote = null;
  for (let i = 0; i < css.length; i++) {
    const c = css[i];
    if (quote) { if (c === '\\') i++; else if (c === quote) quote = null; continue; }
    if (c === '"' || c === "'") { quote = c; continue; }
    if (c === '/' && css[i + 1] === '*') { const end = css.indexOf('*/', i + 2); if (depth === 0) start = end + 2; i = end + 1; continue; }
    if (c === '{') depth++;
    else if (c === '}' && --depth === 0) { out.push(css.slice(start, i + 1).trim()); start = i + 1; }
    else if (c === ';' && depth === 0) { out.push(css.slice(start, i + 1).trim()); start = i + 1; }
  }
  return out.filter(Boolean);
}
const inner = (block) => block.slice(block.indexOf('{') + 1, block.lastIndexOf('}'));
const head = (s) => s.slice(0, s.indexOf('{')).trim();

/**
 * @param {string} root repository root
 * @param {string} dist packages/ui/dist
 * @param {string[]} names component names (the docs' list); pieces named otherwise are an error
 * @param {(css: string) => string} post applied to each output file (shadow links)
 * @returns {Promise<Record<string, { bytes: number, order: number }>>} per file
 */
export async function splitCss(root, dist, names, post = (s) => s) {
  const components = new Set(names);
  const tmp = path.join(root, 'packages/ui/.tmp/split');
  await fs.rm(tmp, { recursive: true, force: true });
  const cssRoot = path.join(root, 'src/css');
  const used = new Set();
  const keyOf = (rel) => {
    const key = FILES[rel] ?? path.basename(rel, '.css');
    if (key !== 'base' && !components.has(key.split('.')[0])) throw new Error(`ui-split: ${rel} maps to unknown component "${key}"`);
    used.add(key);
    return key;
  };
  await copyTree(cssRoot, path.join(tmp, 'src/css'), (file, text) => {
    const rel = path.relative(cssRoot, file).split(path.sep).join('/');
    // Entry files only import; style packs other than Vega are not in the bundle.
    if (!/^(components|extra\/components|native|base|motion|layout)\/|^(styles|extra\/styles)\/vega\.css$|^extra\/tokens\.css$/.test(rel) || /index\.css$/.test(rel) && !/^(motion|layout)\//.test(rel)) return text;
    if (!/@layer components|@layer base/.test(text)) return text;
    if (SECTIONS[rel] && !rel.startsWith('styles/') && !rel.startsWith('extra/styles/')) {
      // A structure file with sections: the part before the first one is the file's own component.
      return `@layer components { ${marker('base')} }\n` + text.split('\n').map((line) => {
        const key = sectionKey(rel, line, components);
        if (key) used.add(key);
        return key ? `  ${marker(key)}\n${line}` : line;
      }).join('\n');
    }
    if (SECTIONS[rel]) {
      let first = true;
      return text.split('\n').map((line) => {
        const key = sectionKey(rel, line, components);
        if (!key) return line;
        used.add(key);
        // The first title may sit above the layer (styles/vega.css).
        const block = first && !line.startsWith('  ') ? `@layer components { ${marker(key)} }\n${line}` : `  ${marker(key)}\n${line}`;
        first = false;
        return block;
      }).join('\n');
    }
    return `@layer components { ${marker(keyOf(rel))} }\n${text}`;
  });
  await copyTree(path.join(root, 'packages/ui/src'), path.join(tmp, 'packages/ui/src'), (file, text) => {
    // themes.css (tokens and named themes) belongs to base; it comes last.
    return path.basename(file) === 'themes.css' ? `@layer components { ${marker('base')} }\n${text}` : text;
  });
  const out = path.join(tmp, 'out.css');
  execFileSync(path.join(root, 'node_modules/.bin/tailwindcss'), ['-i', path.join(tmp, 'packages/ui/src/auvyx.css'), '-o', out], { stdio: 'ignore' });
  const css = await fs.readFile(out, 'utf8');

  // Cut the output at the markers. Tailwind's own statements (layer order,
  // theme, preflight, @property and their fallbacks) are always base.
  const files = { base: [] };
  let key = 'base';
  const markRe = new RegExp(`^\\.${MARK}\\[data-key="([\\w.-]+)"\\]`);
  for (const st of statements(css)) {
    if (/^@layer (theme|base|properties|utilities)\b|^@layer [\w, ]+;|^@property /.test(st)) { files.base.push(st); continue; }
    if (head(st) !== '@layer components') { (files[key] ??= []).push(st); continue; }
    let rules = [];
    const flush = () => { if (rules.length) (files[key] ??= []).push(`@layer components {\n  ${rules.join('\n  ')}\n}`); rules = []; };
    for (const rule of statements(inner(st))) {
      const m = rule.match(markRe);
      if (m) { flush(); key = m[1]; continue; }
      rules.push(rule.replace(/\n/g, '\n  '));
    }
    flush();
  }
  if (css.includes(MARK) && Object.values(files).flat().some((s) => s.includes(MARK))) throw new Error('ui-split: marker left in output');
  for (const k of Object.keys(files)) if (k !== 'base' && !components.has(k.split('.')[0])) throw new Error(`ui-split: unknown component "${k}"`);

  // Components override each other at equal specificity like in the bundle
  // only when loaded in bundle order: each file records its place, and the
  // CLI keeps ui/index.css importing them in that order.
  await fs.mkdir(path.join(dist, 'ui'), { recursive: true });
  const sizes = {};
  let order = 0;
  for (const [k, parts] of Object.entries(files)) {
    if (!parts.length) continue;
    const text = `/* @auvyx/ui ${k} | order ${order++} */\n` + post(parts.join('\n\n') + '\n');
    await fs.writeFile(path.join(dist, 'ui', `${k}.css`), text);
    sizes[k] = { bytes: text.length, order: order - 1 };
  }
  await fs.rm(path.join(root, 'packages/ui/.tmp'), { recursive: true, force: true });
  return sizes;
}

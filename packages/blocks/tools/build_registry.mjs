// Build a shadcn-style registry from block HTML pages.
//
//   node packages/blocks/tools/build_registry.mjs [--src dir] [--out dir] [--cdn url]
//
// Each block page becomes r/<framework>/<icons>/<name>.json, one per
// framework (html, react) and icon library (lucide, tabler, hugeicons, ph, ri):
//   html:  blocks/<name>.html  fragment: block <style>, <body> markup, block scripts
//          pages/<name>.html   standalone page with CDN links
//   react: blocks/<name>.tsx   React 19 component (tools/html-to-react.mjs)
// plus an index.json per folder listing every item. r/<icons>/ and r/<name>.json
// stay as copies of the HTML items for registries configured before
// frameworks and icon libraries existed. Other registries built on Auvyx (Beamui, for one) reuse this
// script: point --src at their blocks folder (HTML pages plus registry.json)
// and --out at the directory their endpoint serves. Each registry.json entry
// may carry a free-form `meta` object, copied into the item as is.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { convertIcons, ICON_SETS } from '../../docs/tools/icon-convert.mjs';
import { toReact } from './html-to-react.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../..');

const args = Object.fromEntries(
  process.argv.slice(2).reduce((acc, a, i, all) => (a.startsWith('--') ? [...acc, [a.slice(2), all[i + 1]]] : acc), []),
);
const src = path.resolve(args.src ?? path.join(here, '..'));
const out = path.resolve(args.out ?? path.join(src, 'dist/r'));
const version = JSON.parse(await fs.readFile(path.join(root, 'packages/ui/package.json'), 'utf8')).version;
const cdn = args.cdn ?? `https://cdn.jsdelivr.net/npm/@auvyx/ui@${version}/dist`;

// Theme toggle used by the docs previews (?theme=dark); not part of the block.
const isPreviewScript = (s) => s.includes('prefers-color-scheme') && s.includes('URLSearchParams');
// Always loaded by the user's layout; not a per-block requirement.
const BASE_ASSETS = new Set(['auvyx.min.css', 'auvyx.min.js']);

function parse(html) {
  const head = html.match(/<head>([\s\S]*?)<\/head>/)?.[1] ?? '';
  const body = html.match(/<body[^>]*>([\s\S]*?)<\/body>/)?.[1] ?? '';
  const styles = [...head.matchAll(/<style>([\s\S]*?)<\/style>/g)].map((m) => m[1]);
  const inline = [...head.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]).filter((s) => !isPreviewScript(s));
  const scripts = [...head.matchAll(/<script\b[^>]*\bsrc="([^"]+)"/g)].map((m) => m[1]);
  const title = head.match(/<title>([^<·]*)/)?.[1].trim();
  return { styles, inline, scripts, body, title };
}

const dedent = (s) => {
  const lines = s.replace(/^\n+|\s+$/g, '').split('\n');
  const pad = Math.min(...lines.filter((l) => l.trim()).map((l) => l.match(/^ */)[0].length));
  return lines.map((l) => l.slice(pad)).join('\n');
};

const toCdn = (s) => s.replaceAll('../ui/dist', cdn);

function fragment({ styles, inline, body }) {
  const parts = [];
  if (styles.length) parts.push(`<style>\n${styles.map(dedent).join('\n')}\n</style>`);
  parts.push(dedent(body));
  for (const s of inline) parts.push(`<script>\n${dedent(s)}\n</script>`);
  return parts.join('\n') + '\n';
}

const meta = JSON.parse(await fs.readFile(path.join(src, 'registry.json'), 'utf8'));
await fs.rm(out, { recursive: true, force: true });
await fs.mkdir(out, { recursive: true });

const items = [];
for (const [name, info] of Object.entries(meta).sort(([a], [b]) => a.localeCompare(b))) {
  const html = await fs.readFile(path.join(src, `${name}.html`), 'utf8');
  const page = parse(html);
  const scripts = page.scripts.filter((s) => !BASE_ASSETS.has(path.basename(s))).map(toCdn);
  items.push({
    page,
    name,
    type: 'registry:block',
    title: info.title ?? page.title ?? name,
    description: info.description ?? '',
    categories: [info.category].filter(Boolean),
    meta: { ...info.meta, version, ...(scripts.length && { scripts }) },
    registryDependencies: info.registryDependencies ?? [],
    files: [
      { path: `blocks/${name}.html`, type: 'registry:block', target: `blocks/${name}.html`, content: fragment(page) },
      { path: `pages/${name}.html`, type: 'registry:page', target: `pages/${name}.html`, content: toCdn(html) },
    ],
  });
}

const FRAMEWORKS = ['html', 'react'];
const json = (v) => JSON.stringify(v, null, 2) + '\n';
const write = async (file, v) => {
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, json(v));
};

function variant(item, framework, icons) {
  const { page, ...rest } = item;
  const meta = { ...rest.meta, framework, icons };
  if (framework === 'html') return { ...rest, meta, files: rest.files.map((f) => ({ ...f, content: convertIcons(f.content, icons) })) };
  // Scripts inside <body> run after the markup, like the head's.
  const bodyScripts = [...page.body.matchAll(/<script>([\s\S]*?)<\/script>/g)].map((m) => m[1]);
  if (/<script\b(?![^>]*>[\s\S]*?<\/script>)|<script\s[^>]*>/.test(page.body)) throw new Error('external <script> in <body>');
  const content = toReact(item.name, {
    title: item.title,
    description: item.description,
    styles: convertIcons(page.styles.map(dedent).join('\n'), icons),
    body: convertIcons(dedent(page.body.replace(/\s*<script>[\s\S]*?<\/script>/g, '')), icons),
    scripts: [...page.inline, ...bodyScripts].map((s) => convertIcons(dedent(s), icons)),
  });
  // Blocks with <auvyx-*> elements need their JSX types.
  const deps = content.includes('<auvyx-') ? [...rest.registryDependencies, '@auvyx/react-types'] : rest.registryDependencies;
  return { ...rest, meta, registryDependencies: deps, files: [{ path: `blocks/${item.name}.tsx`, type: 'registry:block', target: `blocks/${item.name}.tsx`, content }] };
}

// JSX types for <auvyx-*> elements, installed next to React blocks that use
// them (from packages/ui/dist/types, so the ui build runs first).
async function reactTypes() {
  const types = path.join(root, 'packages/ui/dist/types');
  const elements = await fs.readFile(path.join(types, 'elements.d.ts'), 'utf8');
  const react = (await fs.readFile(path.join(types, 'react.d.ts'), 'utf8')).replace("from './elements'", "from './auvyx-elements'");
  return {
    name: 'react-types',
    type: 'registry:lib',
    title: 'React types',
    description: 'TypeScript JSX types for <auvyx-*> elements (React 19).',
    categories: [],
    meta: { version, framework: 'react' },
    registryDependencies: [],
    files: [
      { path: 'types/auvyx-elements.d.ts', type: 'registry:lib', target: 'types/auvyx-elements.d.ts', content: elements },
      { path: 'types/auvyx-react.d.ts', type: 'registry:lib', target: 'types/auvyx-react.d.ts', content: react },
    ],
  };
}
const ownRegistry = args.src === undefined;
const typesItem = ownRegistry ? await reactTypes() : null;

// Components (registry:ui) from packages/ui/dist/ui: their CSS split from the
// bundle, their behavior, and the components their examples use. `base`
// (tokens, preflight, layout, motion) comes with every one. The same items
// serve every framework and icon library.
async function uiItems() {
  const ui = path.join(root, 'packages/ui/dist/ui');
  const { components } = JSON.parse(await fs.readFile(path.join(ui, 'manifest.json'), 'utf8'));
  const docs = JSON.parse(await fs.readFile(path.join(root, 'packages/docs/src/data/components.json'), 'utf8'));
  const file = async (rel, type) => ({ path: rel, type, target: rel, content: await fs.readFile(path.join(ui, '..', rel), 'utf8') });
  const items = [{
    name: 'base',
    type: 'registry:style',
    title: 'Base',
    description: 'Tokens, themes, preflight, layout primitives and motion. Every component needs it.',
    categories: ['ui'],
    meta: { version, order: 0 },
    registryDependencies: [],
    files: [await file('ui/base.css', 'registry:style')],
  }];
  for (const [name, c] of Object.entries(components)) {
    const files = await Promise.all([...c.css, ...c.js].map((f) => file(f, 'registry:ui')));
    items.push({
      name,
      type: 'registry:ui',
      title: docs[name]?.title ?? 'Chart',
      description: docs[name]?.description ?? 'Chart.js styles: tooltips and legends.',
      categories: ['ui'],
      meta: { version, docs: `https://auvyx-ui.vercel.app/#c-${name}` },
      registryDependencies: ['base', ...c.dependencies],
      files,
    });
  }
  return items;
}
const uiList = ownRegistry ? await uiItems() : [];

for (const framework of FRAMEWORKS) {
  for (const icons of ICON_SETS) {
    const index = [];
    for (const item of items) {
      let v;
      try {
        v = variant(item, framework, icons);
      } catch (e) {
        throw new Error(`${item.name} (${framework}, ${icons}): ${e.message}`);
      }
      await write(path.join(out, framework, icons, `${item.name}.json`), v);
      if (framework === 'html') {
        await write(path.join(out, icons, `${item.name}.json`), v);
        if (icons === 'lucide') await write(path.join(out, `${item.name}.json`), v);
      }
      index.push({ name: v.name, type: v.type, title: v.title, description: v.description, categories: v.categories, meta: { ...meta[item.name].meta, framework, icons } });
    }
    for (const item of uiList) {
      await write(path.join(out, framework, icons, `${item.name}.json`), { ...item, meta: { ...item.meta, framework, icons } });
      index.push({ name: item.name, type: item.type, title: item.title, description: item.description, categories: item.categories, meta: { framework, icons } });
    }
    if (framework === 'react' && typesItem) {
      await write(path.join(out, framework, icons, `${typesItem.name}.json`), { ...typesItem, meta: { ...typesItem.meta, icons } });
      index.push({ name: typesItem.name, type: typesItem.type, title: typesItem.title, description: typesItem.description, categories: [], meta: { framework, icons } });
    }
    const list = { name: 'auvyx', version, framework, icons, items: index };
    await write(path.join(out, framework, icons, 'index.json'), list);
    if (framework === 'html') {
      await write(path.join(out, icons, 'index.json'), list);
      if (icons === 'lucide') await write(path.join(out, 'index.json'), list);
    }
  }
}
console.log(`registry: ${items.length} blocks + ${uiList.length} ui items x ${FRAMEWORKS.length} frameworks x ${ICON_SETS.length} icon libraries -> ${path.relative(root, out)}`);

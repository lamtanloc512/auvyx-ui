// Build a shadcn-style registry from block HTML pages.
//
//   node packages/blocks/tools/build_registry.mjs [--src dir] [--out dir] [--cdn url]
//
// Each block page becomes r/<icons>/<name>.json, one per icon library
// (lucide, tabler, hugeicons, ph, ri), with two files:
//   - blocks/<name>.html       fragment: block <style>, <body> markup, block scripts
//   - pages/<name>.html        standalone page with CDN links
// plus r/<icons>/index.json listing every item. r/<name>.json and r/index.json
// stay as the Lucide copies for registries configured before icon libraries
// existed. Other registries built on Auvyx (Beamui, for one) reuse this
// script: point --src at their blocks folder (HTML pages plus registry.json)
// and --out at the directory their endpoint serves. Each registry.json entry
// may carry a free-form `meta` object, copied into the item as is.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { convertIcons, ICON_SETS } from '../../docs/tools/icon-convert.mjs';

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

const info = (item) => ({ meta: meta[item.name].meta ?? {} });
const json = (v) => JSON.stringify(v, null, 2) + '\n';
for (const icons of ICON_SETS) {
  const dir = path.join(out, icons);
  await fs.mkdir(dir, { recursive: true });
  const index = [];
  for (const item of items) {
    const variant = {
      ...item,
      meta: { ...item.meta, icons },
      files: item.files.map((f) => ({ ...f, content: convertIcons(f.content, icons) })),
    };
    await fs.writeFile(path.join(dir, `${item.name}.json`), json(variant));
    if (icons === 'lucide') await fs.writeFile(path.join(out, `${item.name}.json`), json(variant));
    index.push({ name: item.name, type: item.type, title: item.title, description: item.description, categories: item.categories, meta: { ...info(item).meta, icons } });
  }
  await fs.writeFile(path.join(dir, 'index.json'), json({ name: 'auvyx', version, icons, items: index }));
  if (icons === 'lucide') await fs.writeFile(path.join(out, 'index.json'), json({ name: 'auvyx', version, icons, items: index }));
}
console.log(`registry: ${items.length} items x ${ICON_SETS.length} icon libraries -> ${path.relative(root, out)}`);

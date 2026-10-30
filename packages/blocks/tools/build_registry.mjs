// Build a shadcn-style registry from block HTML pages.
//
//   node packages/blocks/tools/build_registry.mjs [--src dir] [--out dir] [--tier free|pro] [--cdn url]
//
// Each block page becomes r/<name>.json with two files:
//   - blocks/<name>.html       fragment: block <style>, <body> markup, block scripts
//   - pages/<name>.html        standalone page with CDN links
// plus r/index.json listing every item. The same script builds a private
// (pro) registry: point --src at the private blocks folder and --out at the
// directory your authenticated endpoint serves.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../..');

const args = Object.fromEntries(
  process.argv.slice(2).reduce((acc, a, i, all) => (a.startsWith('--') ? [...acc, [a.slice(2), all[i + 1]]] : acc), []),
);
const src = path.resolve(args.src ?? path.join(here, '..'));
const out = path.resolve(args.out ?? path.join(src, 'dist/r'));
const tier = args.tier ?? 'free';
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

const index = [];
for (const [name, info] of Object.entries(meta).sort(([a], [b]) => a.localeCompare(b))) {
  const html = await fs.readFile(path.join(src, `${name}.html`), 'utf8');
  const page = parse(html);
  const scripts = page.scripts.filter((s) => !BASE_ASSETS.has(path.basename(s))).map(toCdn);
  const item = {
    name,
    type: 'registry:block',
    title: info.title ?? page.title ?? name,
    description: info.description ?? '',
    categories: [info.category].filter(Boolean),
    meta: { tier: info.tier ?? tier, version, ...(scripts.length && { scripts }) },
    registryDependencies: info.registryDependencies ?? [],
    files: [
      { path: `blocks/${name}.html`, type: 'registry:block', target: `blocks/${name}.html`, content: fragment(page) },
      { path: `pages/${name}.html`, type: 'registry:page', target: `pages/${name}.html`, content: toCdn(html) },
    ],
  };
  await fs.writeFile(path.join(out, `${name}.json`), JSON.stringify(item, null, 2) + '\n');
  index.push({ name, type: item.type, title: item.title, description: item.description, categories: item.categories, meta: { tier: item.meta.tier } });
}

await fs.writeFile(path.join(out, 'index.json'), JSON.stringify({ name: 'auvyx', version, items: index }, null, 2) + '\n');
console.log(`registry: ${index.length} ${tier} items -> ${path.relative(root, out)}`);

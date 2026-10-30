// Shared by icons.mjs and the signature generator: find stroke icons in the
// docs sources and give each a canonical signature (elements and attributes,
// sorted) that the browser can recompute from the live DOM.
import fs from 'node:fs';
import path from 'node:path';

export const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../../..');
const ELEMENT = /<(path|circle|rect|line|polyline|polygon|ellipse)\b([^>]*?)\/?>(?:<\/\1>)?/g;

export function signature(body) {
  return [...body.matchAll(ELEMENT)]
    .map(([, tag, attrs]) => `${tag}(${[...attrs.matchAll(/([\w-]+)="([^"]*)"/g)].map(([, k, v]) => `${k}=${v}`).sort().join(',')})`)
    .sort()
    .join('');
}

export function sourceFiles() {
  const blocks = path.join(ROOT, 'packages/blocks');
  return [
    'packages/docs/src/create-preview.html', 'packages/docs/src/index.html', 'packages/docs/src/create.js',
    'packages/docs/src/data/components.json',
    ...fs.readdirSync(blocks).filter((f) => f.endsWith('.html')).map((f) => `packages/blocks/${f}`),
  ].map((f) => path.join(ROOT, f));
}

// Stroke icons only: <svg stroke="currentColor">…</svg>, plus the icon bodies
// the docs JS keeps as strings ('<path …/><circle …/>').
export function scan() {
  const found = new Map();
  for (const file of sourceFiles()) {
    let text = fs.readFileSync(file, 'utf8');
    if (file.endsWith('.json')) text = text.replace(/\\"/g, '"').replace(/\\n/g, '\n');
    for (const m of text.matchAll(/<svg\b([^>]*)>([\s\S]*?)<\/svg>/g)) {
      if (/stroke="currentColor"/.test(m[1])) found.set(signature(m[2]), { body: m[2].trim(), file });
    }
    for (const m of text.matchAll(/'((?:<(?:path|circle|rect|line|polyline|polygon|ellipse)\b[^'<>]*\/>)+)'/g)) found.set(signature(m[1]), { body: m[1], file });
  }
  found.delete('');
  return found;
}

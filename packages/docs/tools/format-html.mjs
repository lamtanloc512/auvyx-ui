// Format HTML with Prettier, keeping each <svg>…</svg> icon on one line
// (Basecoat docs convention) so icons don't balloon the snippet.
//
//   node format-html.mjs --json in.json out.json   # array of HTML strings
//   node format-html.mjs --files a.html b.html     # whole documents, in place
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const prettier = await import(path.join(root, 'node_modules/prettier/index.mjs'));
const OPTS = { parser: 'html', printWidth: 100, htmlWhitespaceSensitivity: 'ignore', bracketSameLine: true };

async function format(html) {
  const icons = [];
  // Only leaf-ish icons: an <svg> without nested <svg>, short enough to read on one line.
  const masked = html.replace(/<svg\b[^>]*>(?:(?!<svg\b)[\s\S])*?<\/svg>/g, (m) => {
    if (m.length > 1200) return m;
    icons.push(m.replace(/\s*\n\s*/g, ' ').replace(/>\s+</g, '><'));
    return `<i data-icon-slot="${icons.length - 1}"></i>`;
  });
  // attr="" -> attr (boolean style, e.g. popover, data-popover, checked); equivalent in HTML.
  let out = await prettier.format(masked.replace(/(\s[\w:-]+)=""/g, '$1'), OPTS);
  out = out.replace(/<i data-icon-slot="(\d+)"><\/i>/g, (_, i) => icons[+i]);
  return out.trimEnd();
}

const [mode, ...args] = process.argv.slice(2);
if (mode === '--json') {
  const [input, output] = args;
  const items = JSON.parse(await fs.readFile(input, 'utf8'));
  const out = [];
  for (const html of items) {
    try { out.push(await format(html)); } catch (e) { out.push(html); console.error('format failed:', e.message.split('\n')[0]); }
  }
  await fs.writeFile(output, JSON.stringify(out));
} else if (mode === '--files') {
  for (const f of args) {
    const src = await fs.readFile(f, 'utf8');
    try { await fs.writeFile(f, (await format(src)) + '\n'); } catch (e) { console.error(f, 'format failed:', e.message.split('\n')[0]); }
  }
} else {
  console.error('usage: format-html.mjs --json in out | --files ...');
  process.exit(2);
}

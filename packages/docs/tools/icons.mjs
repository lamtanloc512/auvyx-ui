// Build icons.json for the Create "Icon Library" option.
//
//   node packages/docs/tools/icons.mjs <out-dir>
//
// Docs, showcase and block icons are inline Lucide SVGs. icon-signatures.json
// names each one by its signature (see icon-scan.mjs); icon-map.json gives the
// same icon's name in Tabler, HugeIcons, Phosphor and Remix. This writes the
// signature table plus those icons' SVG bodies, which icons.js swaps in at
// runtime. A new inline icon fails the build until it is added to
// icon-signatures.json, so no icon silently stays Lucide.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { scan } from './icon-scan.mjs';

const require = createRequire(import.meta.url);
const here = path.dirname(new URL(import.meta.url).pathname);
const SETS = ['tabler', 'hugeicons', 'ph', 'ri']; // same order as icon-map.json values
const signatures = JSON.parse(fs.readFileSync(path.join(here, 'icon-signatures.json'), 'utf8'));
const names = JSON.parse(fs.readFileSync(path.join(here, 'icon-map.json'), 'utf8'));

const unknown = [...scan()].filter(([sig]) => !(sig in signatures));
if (unknown.length) {
  console.error('icons: unknown inline icons. Add each signature to packages/docs/tools/icon-signatures.json with its Lucide name (null if it is not an icon):');
  for (const [sig, { file }] of unknown) console.error(`  ${path.basename(file)}: ${JSON.stringify(sig)}`);
  process.exit(1);
}

const used = [...new Set(Object.values(signatures).filter(Boolean))];
const missing = used.filter((n) => !names[n]);
if (missing.length) {
  console.error(`icons: add ${missing.join(', ')} to packages/docs/tools/icon-map.json`);
  process.exit(1);
}

const sets = {};
for (const [i, set] of SETS.entries()) {
  const data = require(`@iconify-json/${set}/icons.json`);
  const info = require(`@iconify-json/${set}/info.json`);
  const icons = {};
  for (const name of used) {
    let key = names[name][i];
    while (!data.icons[key] && data.aliases?.[key]) key = data.aliases[key].parent;
    const icon = data.icons[key];
    if (!icon) throw new Error(`icons: ${set} has no ${names[name][i]} (for ${name})`);
    icons[name] = [icon.body, icon.width ?? data.width ?? 16, icon.height ?? data.height ?? 16];
  }
  sets[set] = { license: `${info.name}, ${info.license.title}`, icons };
}

const out = path.resolve(process.argv[2] || '.');
const json = JSON.stringify({ signatures, sets });
fs.writeFileSync(path.join(out, 'icons.json'), json);
console.log(`icons: ${used.length} icons x ${SETS.length} sets, ${(json.length / 1024).toFixed(0)} kB`);

// Build icons.json for the Create "Icon Library" option.
//
//   node packages/docs/tools/icons.mjs <out-dir>
//
// Writes the icon signature table plus each icon's SVG body in every other
// set (see icon-convert.mjs); icons.js swaps them in at runtime. A new inline
// icon fails the build until it is added to icon-signatures.json, so no icon
// silently stays Lucide.
import fs from 'node:fs';
import path from 'node:path';
import { scan } from './icon-scan.mjs';
import { iconData, ICON_SETS } from './icon-convert.mjs';

const { signatures, sets, used } = iconData();

const unknown = [...scan()].filter(([sig]) => !(sig in signatures));
if (unknown.length) {
  console.error('icons: unknown inline icons. Add each signature to packages/docs/tools/icon-signatures.json with its Lucide name (null if it is not an icon):');
  for (const [sig, { file }] of unknown) console.error(`  ${path.basename(file)}: ${JSON.stringify(sig)}`);
  process.exit(1);
}

const out = path.resolve(process.argv[2] || '.');
const json = JSON.stringify({ signatures, sets });
fs.writeFileSync(path.join(out, 'icons.json'), json);
console.log(`icons: ${used.length} icons x ${ICON_SETS.length - 1} sets, ${(json.length / 1024).toFixed(0)} kB`);

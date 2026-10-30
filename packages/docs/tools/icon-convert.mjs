// Icon library data and HTML conversion, shared by icons.mjs (docs runtime
// data) and packages/blocks/tools/build_registry.mjs (per-library registry).
//
// Inline icons are Lucide. icon-signatures.json names each one by its
// signature (see icon-scan.mjs); icon-map.json gives that icon's name in the
// other sets, in ICON_SETS order after "lucide".
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { signature } from './icon-scan.mjs';

const require = createRequire(import.meta.url);
const here = path.dirname(new URL(import.meta.url).pathname);

export const ICON_SETS = ['lucide', 'tabler', 'hugeicons', 'ph', 'ri'];

let cached;
export function iconData() {
  if (cached) return cached;
  const signatures = JSON.parse(fs.readFileSync(path.join(here, 'icon-signatures.json'), 'utf8'));
  const names = JSON.parse(fs.readFileSync(path.join(here, 'icon-map.json'), 'utf8'));
  const used = [...new Set(Object.values(signatures).filter(Boolean))];
  const missing = used.filter((n) => !names[n]);
  if (missing.length) throw new Error(`icons: add ${missing.join(', ')} to packages/docs/tools/icon-map.json`);
  const sets = {};
  for (const [i, set] of ICON_SETS.slice(1).entries()) {
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
  return (cached = { signatures, sets, used });
}

// Lucide's root defaults; Iconify bodies carry their own fill and stroke.
const ROOT_ATTRS = /\s(?:viewBox|fill|stroke|stroke-width|stroke-linecap|stroke-linejoin)="[^"]*"/g;

// Swap every known inline Lucide icon in `html` for the `lib` version.
// Unknown SVGs (logos, drawings) are left as they are.
export function convertIcons(html, lib) {
  if (lib === 'lucide') return html;
  const { signatures, sets } = iconData();
  return html.replace(/<svg\b([^>]*)>([\s\S]*?)<\/svg>/g, (svg, attrs, body) => {
    const icon = sets[lib].icons[signatures[signature(body)]];
    if (!icon) return svg;
    return `<svg${attrs.replace(ROOT_ATTRS, '')} viewBox="0 0 ${icon[1]} ${icon[2]}">${icon[0]}</svg>`;
  });
}

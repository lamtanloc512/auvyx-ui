# @auvyx/ui

A drop-in design system with the shadcn/ui look: plain HTML and CSS classes, optional JavaScript, no build step.

Docs: https://ui.auvyx.org

## CDN

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@auvyx/ui@0.2/dist/auvyx.min.css">
<script src="https://cdn.jsdelivr.net/npm/@auvyx/ui@0.2/dist/auvyx.min.js" defer></script>
```

The JavaScript is only needed by components with behavior (select, tabs, dropdown menu…); each component page says so.

## npm

```bash
npm install @auvyx/ui
```

```js
import "@auvyx/ui/css";
import "@auvyx/ui/js";
```

With Tailwind v4, import the source instead so your build compiles it: `@import "tailwindcss"; @import "@auvyx/ui/bundle";`

## What is in the package

| Path | Contents |
| --- | --- |
| `dist/auvyx.min.css`, `dist/auvyx.min.js` | Everything: every component, layout primitives, motion, themes |
| `dist/styles/auvyx-<style>.min.css` | The same bundle in another style pack: vega, nova, maia, lyra, mira, luma, sera, rhea |
| `dist/js/<component>.min.js` | One component's behavior, for pages that need only a few |
| `dist/wc/<component>.min.js` | Web Components edition (`<auvyx-select>`…) for React, Vue and other frameworks |
| `dist/ui/` | The CSS split per component, and each component's readable JS, used by `npx @auvyx/cli add <component>` |
| `dist/ui/src/` | The same CSS pieces as Tailwind v4 source (`@apply`), installed by `npx @auvyx/cli add <component> --css tailwind` |
| `dist/types/`, `dist/custom-elements.json` | TypeScript (DOM, React, Vue) and Custom Elements Manifest |
| `dist/ax/` | Prefixed build: `auvyx.min.css`, `auvyx.min.js`, `auvyx.chart.min.js` and `styles/` with every class as `ax-…` |

## Prefixed build (`ax-`)

For pages whose own CSS already uses names like `.btn`, `.card`, `.alert` or `.dropdown-menu` (Bootstrap, WordPress themes, legacy apps), load the prefixed build. Every Auvyx class becomes `ax-…` in the CSS and in the JavaScript, so neither side styles the other:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@auvyx/ui@0.2/dist/ax/auvyx.min.css">
<script src="https://cdn.jsdelivr.net/npm/@auvyx/ui@0.2/dist/ax/auvyx.min.js" defer></script>

<button class="ax-btn" data-variant="outline">Save</button>
<div class="ax-card">…</div>
```

From npm: `import "@auvyx/ui/ax/auvyx.min.css"; import "@auvyx/ui/ax/auvyx.min.js";`. Style packs are in `dist/ax/styles/`. Only the class names change: `data-*` attributes, ARIA, element names, CSS variables and the `.dark` class stay the same. The per-component modules (`js/`, `wc/`), the docs examples and the registry blocks use the unprefixed names.

Components and blocks can also be copied into your project with [`@auvyx/cli`](https://www.npmjs.com/package/@auvyx/cli).

## License

MIT, see LICENSE.

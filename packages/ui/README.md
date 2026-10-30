# @auvyx/ui

A drop-in design system with the shadcn/ui look: plain HTML and CSS classes, optional JavaScript, no build step. Based on [Basecoat](https://github.com/hunvreus/basecoat).

Docs: https://auvyx-ui.vercel.app

## CDN

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@auvyx/ui@0.1/dist/auvyx.min.css">
<script src="https://cdn.jsdelivr.net/npm/@auvyx/ui@0.1/dist/auvyx.min.js" defer></script>
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
| `dist/ui/` | The CSS split per component, used by `npx @auvyx/cli add <component>` |
| `dist/types/`, `dist/custom-elements.json` | TypeScript (DOM, React, Vue) and Custom Elements Manifest |

Components and blocks can also be copied into your project with [`@auvyx/cli`](https://www.npmjs.com/package/@auvyx/cli).

## License

MIT. Includes Basecoat (MIT, Ronan Berder); see LICENSE.

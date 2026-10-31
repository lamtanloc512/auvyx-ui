# Auvyx UI

A drop-in design system with the shadcn/ui look: plain HTML and CSS classes, optional JavaScript, no build step. Use it from a CDN, from npm, or copy components and blocks into your project with the CLI, the shadcn way.

![screenshot](.github/screenshot.png)

- Docs: [ui.auvyx.org](https://ui.auvyx.org) ([llms.txt](https://ui.auvyx.org/llms.txt))
- npm: [`@auvyx/ui`](https://www.npmjs.com/package/@auvyx/ui), [`@auvyx/cli`](https://www.npmjs.com/package/@auvyx/cli)

## Features

- Semantic HTML components with shadcn/ui's visual language, and blocks (login, signup, sidebar, dashboard, calendar).
- Eight style packs (Vega, Nova, Maia, Lyra, Mira, Luma, Sera, Rhea), shadcn and tweakcn themes, dark mode, motion, squircle corners.
- A zero-JavaScript path on native browser features; small vanilla JavaScript where behavior needs it.
- A Web Components edition with TypeScript, React and Vue types; blocks also ship as React components.
- A shadcn-style registry and CLI: `npx @auvyx/cli add login-01 combobox`.

## Install

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@auvyx/ui@0.1/dist/auvyx.min.css">
<script src="https://cdn.jsdelivr.net/npm/@auvyx/ui@0.1/dist/auvyx.min.js" defer></script>
```

```bash
npm install @auvyx/ui
```

```bash
npx @auvyx/cli init
```

## Repository layout

```text
.
├── packages/
│   ├── ui/         @auvyx/ui: CSS, JS, Web Components, types, per-component files
│   ├── elements/   Custom elements (calendar, date picker, data table…), bundled into ui
│   ├── blocks/     Block pages and the registry builder (HTML and React)
│   ├── cli/        @auvyx/cli
│   ├── docs/       The docs site and public registry (packages/docs/out)
│   └── tests/      Browser checks (Playwright)
├── src/            Component sources: css/, js/, templates/ (Nunjucks and Jinja macros)
└── scripts/        Core CSS build and checks
```

## Development

```bash
npm install
```

```bash
# ui -> registry -> docs, as deployed on Vercel.
npm run auvyx:build
```

```bash
# Serve the docs locally.
python3 -m http.server -d packages/docs/out
```

```bash
# Types, CLI, React blocks against the HTML, split CSS against the bundle (about 15 minutes).
npm run auvyx:test
```

The build needs Python 3 for the block and docs generators. See [CONTRIBUTING.md](CONTRIBUTING.md) for releases.

## License

MIT. See [LICENSE.md](LICENSE.md) and the LICENSE file in each package for the notices it includes.

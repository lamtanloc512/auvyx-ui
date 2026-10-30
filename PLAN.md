# Plan: Auvyx UI as the open foundation

Auvyx UI is the open-source foundation (MIT): CSS, behavior, registry format, CLI, free blocks and docs, shaped like shadcn-svelte. It does not sell anything. Commercial work (paid blocks, licensing, payments, storefront) lives in **Beamui**, which builds on Auvyx.

## Boundary

| Auvyx UI (this repo, public, MIT) | Beamui (separate repo) |
| --- | --- |
| `@auvyx/ui`: CSS, style packs, motion, corners, themes | Paid block sources (private) |
| JS in two editions: HTML (`js/`) and Web Components (`wc/`) | Authenticated registry endpoint |
| Registry format and builder (`packages/blocks/tools/build_registry.mjs`) | Payments, licenses, accounts |
| CLI (`@auvyx/cli`) for any registry, public or private | Storefront, pricing, previews of paid blocks |
| Free blocks and the public registry at `/r/` | Its own `meta` fields (tier, price…) |
| Docs, Create presets, icon libraries | |

### What Auvyx guarantees Beamui

- **Registry item format** (documented in `packages/cli/README.md`): `r/<icons>/<name>.json`, `files[]`, `meta.icons`, `meta.version`, `meta.scripts`; any `meta` from a source `registry.json` entry is copied as is.
- **Builder reuse:** `build_registry.mjs --src <dir> --out <dir>` builds any folder of HTML block pages plus `registry.json`, with every icon library.
- **CLI:** namespaced registries, `{icons}` and `{name}` URL templates, `${ENV}` headers for tokens, refusal to write outside the target directory.
- **Stable CSS API:** class names, `data-*` attributes and tokens (`--primary`, `--radius`, `--corner-shape`, `--motion-*`) follow semver once 1.0 ships.

Auvyx contains no licensing, payment or tier logic. Paid source must never be committed here.

## Done

- [x] Public registry: one item per block and icon library, served by the docs at `/r/`.
- [x] CLI: `init`, `add`, `list`; `--icons`; authenticated registries.
- [x] Docs: shadcn-svelte–style site, Create presets (style, colors, fonts, icons, radius, corners, menu), applied app-wide.
- [x] Icon libraries: Lucide, Tabler, HugeIcons, Phosphor, Remix (docs, previews, registry).
- [x] Motion layer (`src/css/motion`), squircle corners (native + Monoco fallback).
- [x] Per-component JS modules (`dist/js/`) and docs labels for components that need JavaScript.
- [x] Web Components edition for every component with behavior: tabs, select, combobox, command, dropdown-menu, popover, accordion, sidebar, toaster, slider, drawer (`dist/wc/`), tested in React 19 and Vue 3.

## Next (Auvyx)

- [ ] Custom Elements Manifest and generated TypeScript/JSX/Vue types.
- [ ] Registry framework variants: React (JSX) output next to HTML, `--framework` in the CLI.
- [ ] Registry items for components (`registry:ui`), not only blocks.
- [ ] Workspaces and one build (`ui` → `elements` → `blocks` → registry → docs); CI with the Playwright checks used during development.
- [ ] Publish `@auvyx/ui` and `@auvyx/cli` to npm.
- [ ] Retire or merge `site/` (upstream Basecoat docs) into `packages/docs`.

## Beamui (tracked there, listed for context)

- Paid block catalog built as HTML on Auvyx, registry built with `build_registry.mjs`.
- Authenticated registry, licenses, payments, storefront (Astro).

## Risks

- **Licensing:** Basecoat (MIT, Ronan Berder) keeps its notice in `LICENSE.md` and published packages.
- **Free blocks are shadcn/ui ports** (MIT): fine as free items here; paid value has to come from Beamui's own blocks.
- **Two package names** (`basecoat-css`, `@auvyx/ui`) can confuse users; decide which one is public before 1.0.

## Open questions

1. Keep publishing `basecoat-css`, or only `@auvyx/*`?
2. Final domain for docs and the public registry (currently `auvyx-ui.vercel.app`).

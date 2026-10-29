# TODO (fork)

## Deferred

- Style packs for fork-added components (`src/css/extra/`): only Vega visuals
  exist (`src/css/extra/styles/vega.css`). Port Nova, Maia, Lyra, Mira, Luma,
  Sera, Rhea from shadcn `apps/v4/registry/styles/style-*.css`.
- Hover Card: `data-align="center"` relies on anchor positioning; without it
  the card aligns start.
- Docs pages in `site/` for fork-added components (preview lives in
  `packages/ui/preview.html` for now).
- Date Picker: range mode (Calendar already supports mode="range"), month/year dropdowns.
- Menus: submenus (nested popovers) for dropdown, menubar and context menu.
- Navigation Menu: shared animated viewport and indicator arrow from upstream.
- Data Table: server-side mode (emit sort/filter/page events instead of moving rows).
- Elements package: publish separately; add unit tests (current coverage is the
  Playwright suite run against packages/ui/preview.html).

## Mapped, not ported

- Sonner → Basecoat Toast already covers it.
- Direction → native `dir="rtl"`; components use logical properties.

# Changelog

## [Unreleased]

## @auvyx/ui 0.2.0 - 2026-11-13

Upgrading from 0.1: pages that use `<auvyx-data-table>` now load `js/data-table.min.js` next to `auvyx.min.js` (see Changed). CDN links pinned to `@auvyx/ui@0.1` keep serving 0.1.4; move them to `@auvyx/ui@0.2`.

### Changed

- `auvyx.min.js` no longer includes `<auvyx-data-table>` (21.9 kB gzip, was 23.1 kB). Load `js/data-table.min.js` on pages with a data table; `js/manifest.json` marks such modules `"bundled": false`.
- Blocks page: categories grouped under Application, Authentication, Commerce and Content, with category chips and counts. The Agent, Blog and Error categories now show (they were missing).

### Fixed

- The warning alerts in the Drawer, Table and Toast docs (`data-variant="warning"`, which had no rule) now look like warnings.
- Pagination and Spinner had no CSS on the CDN channel: their docs examples, and Skeleton's, sized and laid out everything with Tailwind utilities that `auvyx.min.css` does not contain. They now work with the CDN files alone:
  - `.pagination` on the `<nav>`: a list of `.btn` pages (the current one `aria-current="page"`), inert `aria-disabled` links, a `<span>` ellipsis, and an optional `<p>` summary ("11–20 of 42") that moves the list to the end.
  - `.spinner` on a loader `<svg>` (or an empty `<span>`, drawn as a ring) with `role="status"`: `data-size="sm|lg|xl"`, the icon size inside buttons, badges and input groups, and a pulse instead of a turn under reduced motion.
  - Skeleton shapes: `data-variant="text"` (a line), `"circle"` (a 2.5rem avatar) and `"block"` (a 16:9 media box).
- Corner shapes in Maia and Luma: buttons, fields, badges, tab lists, chips and progress bars are pills there, and Notch or Scoop squared them off into rectangles. They now stay round, as switches and radios already did; corner shapes apply to cards, dialogs and menus, and the Create page says so for those styles. The global `corner-shape` rule moved into `@layer base` so a style pack's component rules can override it.
- Tile: the caption's menu button is clickable before hover (only the preview overlay lets clicks through until it shows).
- React blocks: `chat-01` model select and `projects-02` column headers now render like the HTML blocks.
- Create page: importing a theme or choosing a preset that sets its own letter spacing now uses it; before, an earlier Letter Spacing slider value overrode it.
- Create page: themes with bare HSL channel colors (`222.2 84% 4.9%`, as in tweakcn's Tailwind v3 export and older shadcn registry JSON) are wrapped in `hsl()`, so their colors apply.

### Added

- Alert `data-variant="success"`, `"warning"` and `"info"` next to the default and `destructive`. They read three new theme tokens, `--success`, `--warning` and `--info` (light and dark values; a theme overrides them like any other color), which `auvyx.ai.json` lists with the other tokens.
- `auvyx.ai.json` on the docs site (linked from `llms.txt`): component contracts for agents. Per component: the root selector, owned classes, the data-* and aria-* attributes its examples use with their values, the root's children, the script it needs, its custom element API and a canonical snippet. Top level: design rules, theme tokens and intent groups, so a caller can route a request and send only the relevant contracts. Generated from the same sources as the docs and checked by `packages/tests/ai-contract.test.mjs`.
- `.flyout-menu`, CSS only: a vertical category menu whose panels fly out to the side on hover or keyboard focus, with a short hide delay for diagonal pointer moves; works inside a popover.
- Create page: a Mono Font option (Geist Mono, JetBrains Mono, IBM Plex Mono, Fira Code, Roboto Mono, Source Code Pro, Space Mono, DM Mono) that sets `--font-mono`, and a Letter Spacing slider that sets `--tracking-normal`. Preset codes gain a 12th digit for the mono font; 11-digit codes still open. Imported tweakcn themes' `--letter-spacing` now applies.
- AI chat primitives:
  - `.prompt-input` with `<auvyx-prompt-input>` (`js/prompt-input.min.js`, not in `auvyx.min.js`): a growing textarea, files by picker, drop or paste, Enter to send, suggestions, and a stop state while `streaming`; cancelable `prompt` and `stop` events.
  - `.suggestions` (prompt chips), `.message-actions` (copy, retry, feedback toggles), `.typing` dots and a streaming caret on `.bubble[data-streaming]`, all CSS only.
- `chat-01` (new Chat category): an AI chat page built on those primitives with a demo streamed reply.
- Create page theme presets Vercel and Clean Slate, taken as-is from tweakcn (Apache-2.0): neutral themes with white cards and hairline borders. Pair them with Maia for pill-shaped controls.
- `studio-01` (new Studio category): an image studio Create page with a prompt composer built from a vertical Input Group (pickers, textarea, toolbar) over a hero, and Spotlight / Liked carousels.

- Data Table interactions (`<auvyx-data-table>`, all opt-in, backward compatible):
  - `data-grid` grid keyboard model; `data-sticky` header.
  - Faceted filters (`data-facet`, `data-facet-count`); a page size select; first/last page buttons; `[data-reset]`.
  - Expandable rows (`data-expand` + `tr[data-detail]`); shift-click range selection; inline editing (`td[data-editable]`, cancelable `cellchange`).
  - Columns named by `th[data-key]`; a read/write `state` property with a `statechange` event; server mode (`data-mode="server"`, `data-total`, `refresh()`).
  - Usage notes in the docs.
- `<auvyx-sortable>`: drag and drop between the lists inside it (kanban columns), by pointer (touch after a short press) or keyboard, with screen reader announcements and a cancelable `sort` event. Loaded on its own as `js/sortable.min.js`.
- CSS-only foundation primitives:
  - `.table[data-variant="grid"]`: a spreadsheet-style table with cell lines, column icons, CSS-counter row numbers and a sticky header and footer.
  - `.kanban`: a board of columns and cards (pair with `<auvyx-sortable>` for drag and drop).
  - `.properties`: label and value rows for record pages; rows stack when the list is narrow.
  - `.tile`: a preview with a caption for project thumbnails, galleries and showcases; a caption link makes the whole tile clickable. Lay tiles out with `.auto-grid`. `[data-actions]` adds controls shown on hover or focus: inside the preview it overlays buttons (View site, Duplicate); at the end of the caption it holds a menu trigger. Hovered tiles change background.
- Agent blocks in a new Agent category:
  - `agent-01` context window panel: tokens used with a health level, prompt cache savings, a waffle chart by source with a hover-to-isolate legend, contents by tab, and a working Compact history action.
  - `agent-02` agent runs table built on the new Data Table interactions.
- `projects-02` (Export: export targets as cards and recent exports in a grid table) and `projects-03` (MCP: server cards with a connect button and a copyable URL). The Publish / Export / Studio / MCP tabs link `projects-01`, `projects-02`, `studio-01` and `projects-03`.
- `projects-01` (new Projects category): a workspace of sites with project tiles showing a style preview (logo, typeface, palette), a showcase of site mockups and a What's new card that closes without JavaScript (`<dialog open>` + `<form method="dialog">`).
- CRM blocks in a new CRM category (Application group), built on the foundation primitives:
  - `crm-01` customers in two synced views: a grid data table (row numbers, stage and owner facets, editable ARR, grid keys, totals row) and a kanban board where dragging a card changes the stage.
  - `crm-02` customer record: identity and actions, details and custom fields as `.properties`, stat cards, an activity timeline and contracts in a grid table.
- Online course blocks (Udemy / Domestika style), 10 in a new Courses category: `course-01` catalog with topic pills, filters (rating, level, length, price), sort and a hover preview with Add to cart; `course-02` list rows and Domestika-style cards; `course-03` learning home with a search hero, continue learning, a course carousel and teachers; `course-04` course page with a sticky purchase card, video preview dialog, what you'll learn, expandable curriculum with previews, description, teacher and reviews; `course-05` course player with a progress ring, completion checkboxes, next and previous lesson, collapsible sections with Expand all / Collapse all, a sidebar you can hide for a wider video, Q&A and notes; `course-06` my learning with a weekly goal and status filters; `course-07` teacher profile; `course-08` subscription plans with a monthly or yearly switch; `course-09` certificate of completion; `course-10` course cart with a coupon (`LEARN20`) and payment choice.
- LMS admin blocks (instructor dashboard, in the style of Teachable, Thinkific and Udemy's instructor tools), 8 in a new LMS Admin category, all in a sidebar shell:
  - `admin-01` courses: status tabs with counts, search, category filter, select all with a bulk bar (publish, unpublish, delete), row menus, a New course dialog.
  - `admin-02` curriculum builder: sections and lessons you drag to reorder (or move with arrow keys on the handle, across sections, announced to screen readers), add lessons by type (video, article, quiz, assignment) and name them inline, rename, collapse and add sections, live totals.
  - `admin-03` lesson editor: video upload by drag and drop or file picker with progress, processing and a ready state with replace and remove; a rich text description with a toolbar and word count; resources; publish settings; saved / unsaved state.
  - `admin-04` media library: drop zone and upload queue with progress, type filters, search, grid or list view, a details panel with copy link, multi-select delete.
  - `admin-05` students: KPIs, status tabs, search, course filter, progress bars, bulk actions, CSV export of the visible rows, an invite dialog that validates addresses.
  - `admin-06` analytics: a 7 days / 30 days / 12 months range that updates the KPIs and a revenue bar chart with tooltips, traffic sources, top courses, recent activity.
  - `admin-07` pricing and coupons: free, one-time, subscription or payment plan with the fields each needs and a live preview of the price students see; coupons to create (with a code generator and validation), copy, pause and delete.
  - `admin-08` review moderation: rating summary, filters (needs reply, flagged, 1–2 stars) with counts, inline public replies, flag and hide.
  - New icons mapped for every library: cloud-upload, copy-plus, flag, grip-vertical, heading-2, link, list-checks, list-ordered, paperclip, quote, refresh-cw, reply, tag, ticket-percent, video.
- React blocks: `contenteditable` elements get `suppressContentEditableWarning`, so an editable area converts without a warning.
- Header and footer blocks for six kinds of business, in new Header and Footer categories. On phones every header switches to a bottom tab bar, the usual mobile pattern; its menu tab opens the header's sheet.
  - `header-01` ecommerce: rotating announcement bar, utility bar with currency and language, search, account, wishlist and cart, mega menus.
  - Header search fields show a ⌘K hint; Cmd/Ctrl+K focuses the search, or opens it where it sits under the header.
  - `header-02` online courses: categories menu, rounded search, Plus / Teach links, log in and sign up.
  - `header-03` blog or magazine: masthead with the date, section row, search that opens under the header, dark mode toggle, subscribe.
  - `header-04` spa or wellness: contact and hours bar over a hero; the header turns solid on scroll and has a Book now button.
  - `header-05` beauty: centered logo, mega menu with a featured product, search under the header.
  - `header-06` kids and toys: colorful logo, rounded search, age and category chips.
  - `header-07` marketplace home: store links bar, search with a category select, wishlist and cart counts, an accent nav bar with an All categories label and a Recently viewed popover, then a category menu with flyout panels beside the hero slider, two promo banners and featured categories.
  - `header-08` the same marketplace header on an inner page: All categories opens the flyout category menu as a popover.
  - `header-09` electronics: accent main bar with a categories button, a delivery location dialog, rounded search, hotline, order lookup and cart, then an icon nav of product types.
  - `header-10` grocery delivery: delivery address dialog and next delivery slot, search with popular terms, a cart button with the running total, and a scrolling row of round category icons.
  - `footer-01` to `footer-06` for the same businesses: newsletter signup with validation and a success state, link columns that collapse on phones, social links, payment methods, language and currency, back to top, a teacher call to action and app badges (courses), recent posts and topics (blog), contact details, opening hours with today highlighted and a map (spa), brand values (beauty), a wave edge and safety badges (kids).
  - New icons mapped for every library: baby, facebook, headphones, instagram, leaf, linkedin, puzzle, rabbit, recycle, rss, store, twitter (X), youtube.
- Create: font weight controls. A Font Weight slider next to Font Size shifts regular, medium, semibold and bold together (`--font-weight-normal|medium|semibold|bold`, which every component reads), and Customize theme → Typography sets each one. The Google Fonts link now loads each family's whole weight axis, so any chosen weight renders with real glyphs.

### Fixed

- `course-09`: the copy button sat flush against the certificate number in the React version, which drops the space between them; the row now spaces its items with a gap.
- Bottom navigation badges overlapped the bar's top border.
- Rating filters in `filter-01`, `filter-03` and `search-02` pushed the stars to the far edge of the row. Some blocks used `data-gap` values outside the layout scale (5, 10), which fell back to the default gap; they now use 4 and 12.
- Create: importing tweakcn's full CSS export (the one that starts with `@import "tailwindcss"` and `@custom-variant dark (&:is(.dark *))`) read the `:root` block as dark, so the light colors, radius and fonts were dropped. The import box also grew with a long paste until Apply was off screen; it now keeps a fixed height and scrolls.
- Docs: choosing a style on Create replaced nothing; the style's stylesheet loaded on top of the Vega bundle inside `docs.css`, so whatever the style does not set kept Vega's value (the header's small buttons kept Vega's radius under Maia while the preview, which loads the style alone, did not). The site and block pages now load one component stylesheet, `dist/auvyx.min.css` or the chosen style's bundle in its place, and `docs.css` holds only the docs utilities (41 kB → 5 kB gzip).

## @auvyx/ui 0.1.4 - 2026-11-07

### Added

- Ecommerce blocks (15, in the registry for HTML and React with every icon library):
  - Cart: `cart-01` cart page (quantity steppers, remove, free-shipping progress, promo code, order summary, empty state), `cart-02` empty cart with suggestions, `cart-03` mini cart in a Sheet, `cart-04` mini cart in a Popover.
  - Checkout: `checkout-01` one-page checkout (contact, address, delivery and payment choice cards, summary), `checkout-02` multi-step checkout with a step indicator and review, `checkout-03` order confirmation.
  - Orders: `orders-01` order history with status filters, `orders-02` order details with a delivery tracker and tracking history.
  - Account: `account-01` overview, `account-02` settings (details, password, email preferences), `account-03` address book with an add-address Dialog.
  - Bottom navigation: `bottom-nav-01` tab bar with a cart badge, `bottom-nav-02` floating pill tab bar, `bottom-nav-03` mobile product page with a sticky add-to-cart bar.
- Create: a Corner Smoothing slider for Squircle and Smooth corners (disabled without a radius). It sets `corner-shape: superellipse(k)` for browsers with native `corner-shape` and `--corner-smoothing` for the Monoco fallback (`auvyx.corners.min.js`), which now also maps any `superellipse(k)` to the matching Monoco curve.
- Create: a Font Size slider (12–20px base text). It scales every `--text-*` token the components use, so spacing and radius stay the same, and sets `body { font-size: var(--text-base) }`.
- More ecommerce blocks (12, HTML and React, every icon library):
  - Product cards: `product-card-01` grid cards (badge, rating, colors, wishlist toggle, quick add), `product-card-02` horizontal cards with description and stock, `product-card-03` cards with color swatches.
  - Product: `product-01` product page (gallery, color and size, quantity, add to cart, perks, details, reviews, related products), `product-02` quick view Dialog.
  - Wishlist: `wishlist-01` wishlist grid in the account area (move to cart, remove, empty state), `wishlist-02` wishlist table.
  - Compare: `compare-01` comparison table (sticky labels, remove, highlight differences), `compare-02` compare checkboxes with a floating compare tray.
  - Search: `search-01` product search Command dialog (⌘K) with recent searches, categories and product results, `search-02` results page with filters, sort, filter chips, grid and list views and pagination.
  - Cart: `cart-05` mini cart in a bottom Drawer.
- Interactive product cards: `product-card-04` second photo, side actions and an add-to-cart bar on hover, `product-card-05` hover zones that flip through photos (with arrows and color swatches), `product-card-06` quick add sizes on hover with a confirmation, `product-card-07` lift on hover and Add to cart that turns into a quantity stepper, `product-card-08` editorial card whose details slide up over the photo (an info button opens them on touch screens), `product-card-09` flash sale cards with a stock bar and a countdown. Hover states also open on keyboard focus, and motion is off with `prefers-reduced-motion`.
- Filter and category blocks:
  - Filter: `filter-01` filter sidebar (category with counts, price, color, size, rating, in stock) that filters the grid live, with active chips, a filter count, sort and an empty state; `filter-02` horizontal filter bar with a popover per filter; `filter-03` mobile filters in a bottom Sheet with a live “Show N products” button.
  - Category: `category-01` category landing (hero, subcategory circles, room tiles, featured products, promo, FAQ); `category-02` shop-by-category bento grid with hover zoom; `category-03` category listing with a subcategory tree, pills, sort and load more with progress.
- Checkout success and order tracking blocks: `checkout-04` order success with an animated check, confetti, copyable order number, account creation and a referral link; `checkout-05` mobile payment success with a receipt; `tracking-01` order lookup by number and email with validation; `tracking-02` live delivery with a route map, arrival window, courier contact, editable delivery instructions and history; `tracking-03` an order in two packages with tabs, copyable tracking numbers and notification settings.
- Carousel: optional JavaScript (`js/carousel.min.js`, also in `auvyx.min.js`). Buttons the page provides (`data-carousel="prev|next|play"`), dots (`data-carousel-dots`), a counter (`data-carousel-counter`), mouse dragging, keyboard, `data-loop`, `data-autoplay` (pauses on hover, focus, hidden tabs and reduced motion), a thumbnail strip kept in sync (`data-carousel-for`), the API `goTo()`, `goToSlide()`, `next()`, `prev()`, `play()`, `pause()` and a `carousel:change` event. Without it, carousels still scroll, snap and swipe; the native scroll buttons and markers stay until the page provides its own controls.
- Button docs: examples for icons before and after the text and for icon-only buttons at every size, and how `data-icon="inline-start|inline-end"` trims the padding on the icon side so the button looks evenly spaced. The ecommerce blocks now mark every icon in a text button this way.
- Lightbox: links with `data-lightbox="group"` open their image full screen with the rest of the group (swipe, drag, arrow keys, click to zoom and pan, captions from `data-caption`). Without JavaScript the link opens the image.
- `product-01`: the gallery is a carousel with arrows, dragging, synced thumbnails and a lightbox.
- Review blocks: `reviews-01` reviews with a rating summary whose star bars filter the list, fit and feel scales, a photos filter, sort, helpful votes and store replies; `reviews-02` write a review with a star rating that previews on hover, fit feedback, a character counter, photo upload with previews and a thank-you state; `reviews-03` review highlights with a summary, pro and con tags that filter a scrolling row of reviews.
- React blocks: `<textarea>` is supported in block markup (its text becomes `defaultValue`).
- Create: lock any option. A locked option keeps its value when a theme preset or an imported theme is applied, and Shuffle, Reset and Open Preset leave it alone.
- Docs and `@auvyx/ui` README: the prefixed build (`dist/ax/`, classes `ax-…`) is now documented under Installation.

### Fixed

- Dialog and Sheet close buttons are ghost icon buttons, as upstream: they get the muted background on hover (they only changed opacity before), with each style's size, radius and focus ring; Luma, Sera and Rhea give them a secondary background.
- `tracking-02`: the icons in the map pins sat in the top-left corner; the map's SVG rule also matched them.
- Color swatches in the ecommerce filters were clipped by the accordion, and round swatches, dots, badges and pins turned into rounded squares with squircle corners. They now have room for their focus outline and keep `corner-shape: round`.
- Block styles with a selector list (`a, b { … }`) were dropped when one selector's block class was not used in that block, so some ecommerce blocks lost rules such as the dark-mode image filter. The rules are now one selector each.

## @auvyx/ui 0.1.3 - 2026-11-06

### Added

- A prefixed build in `@auvyx/ui/ax/*` (`dist/ax/auvyx.min.css`, `auvyx.min.js`, `auvyx.chart.min.js` and every style pack in `dist/ax/styles/`). Every class carries an `ax-` prefix (`.btn` becomes `.ax-btn`) in the CSS and wherever the JavaScript finds, creates or toggles classes, so Auvyx UI can sit inside a page whose theme uses the same class names (Bootstrap's `.btn`, `.card`, `.alert`, `.dropdown-menu`). Markup for this build uses the prefixed class names; `data-*` attributes, ARIA and element names are unchanged, and `.dark` stays the color-scheme class. The default build is unchanged.

### Fixed

- Restored the space under a Fieldset `<legend data-variant="label">`. Every style pack set its bottom margin to 0, so the label sat flush against the radio group, checkboxes or description below it; it now uses the same margin as other legends, matching upstream shadcn/ui.
- Fixed charts with `surface: "gradient"` resolving their colors on every draw, which forced a full style recalculation per frame and made resizes (such as opening or closing a Sidebar next to a chart) stutter. The gradient colors are now resolved once per chart render.

## [1.1.0] - 2026-10-23

### Upgrading

- Toast `title`, `description`, `action.label` and `cancel.label` are now escaped as text by default. If you pass HTML in any of them, add `html: true` to your `toaster.toast()` call.

### Added

- Added vertical separators: `<hr aria-orientation="vertical">` renders as a 1px line that fills its row.
- Added single-file `.bundle.css` builds (`dist/basecoat.bundle.css` and `dist/basecoat-{style}.bundle.css`) with every Basecoat import inlined, so the standalone Tailwind CLI can use Basecoat without npm. Based on the standalone CLI setup proposed by [@ytsruh](https://github.com/ytsruh) in [#150](https://github.com/hunvreus/basecoat/pull/150).
- Added an `html: true` option to `toaster.toast()` for callers that need to pass raw HTML in the title, description or action labels.

### Changed

- Toast `title`, `description`, `action.label` and `cancel.label` are now escaped as text by default, matching Sonner. Pass `html: true` to keep the previous raw-HTML behavior.
- Changed the default `--font-sans` to start with `"Geist"`, the family name used by Google Fonts, Bunny Fonts and Fontsource, with `"Geist Sans"` kept as a fallback. The customization docs now install `@fontsource/geist`.
- Updated the docs dependency to `reallysimpledocs@^1.0.14`, so `llms.txt` links to the Markdown version of each page.
- Documented how to use Tailwind utilities with Basecoat's theme colors alongside the CDN build and the Tailwind Play CDN.

### Fixed

- Prevented Escape from dismissing an enclosing dialog while closing an open Combobox popup.
- Fixed long Tooltip text clipping instead of showing an ellipsis across all style packs.
- Locked page scroll while a modal Dialog, Alert Dialog, Command Dialog or Drawer is open.
- Kept a parent Popover, Dropdown Menu, Select or Combobox open when a nested one opens inside it. Sibling components still close each other.
- Scoped Sidebar navigation styles to the sidebar's direct child `nav` (`.sidebar > nav`), so other `nav` elements inside a sidebar, such as a Tabs list, are no longer fixed and stacked.
- Stopped Dialogs and Command Dialogs from closing when a press starts inside the dialog and the drag ends on the backdrop. Updated the Nunjucks and Jinja templates and the docs examples. Based on [#104](https://github.com/hunvreus/basecoat/pull/104) by [@PhilipdeRijk](https://github.com/PhilipdeRijk).
- Fixed iOS auto-zoom when tapping the Combobox input, the Combobox chips input, the Command search input, native Selects, and Input Group inputs and textareas by using `text-base` below the `md` breakpoint, like regular inputs. The compact Lyra and Mira styles keep their smaller sizes.
- Fixed Slider thumb hover and focus rings, the RTL Sidebar submenu chevron, and some dark mode and tooltip arrow styles not applying in the unminified CDN files, because the rules were nested under pseudo-elements.
- Fixed CDN `.min.css` builds occasionally dropping rules (such as hidden Combobox, Command and Select options) by minifying with esbuild instead of Tailwind's minifier.
- Stopped the Toast docs example from pushing its fragment URL into the browser history with HTMX.
- Replaced the `.form` migration snippet in the 1.0.0 notes, which fails in Tailwind v4, with markup that works.

### Contributors

- Thanks to [@ytsruh](https://github.com/ytsruh), [@PhilipdeRijk](https://github.com/PhilipdeRijk), [@sgruendel](https://github.com/sgruendel), [@alexander-posztos](https://github.com/alexander-posztos) and [@Jezda1337](https://github.com/Jezda1337) for their contributions to this release.

## [1.0.2] - 2026-07-06

### Added

- Added `data-size="sm"` support to Alert Dialog for the compact upstream size.

### Changed

- Removed global font smoothing from Basecoat's package CSS so `antialiased` remains an application-level choice.

## [1.0.1] - 2026-06-28

### Added

- Added explicit `force: true` support to `window.basecoat.init()` and `window.basecoat.initAll()` for rehydrating restored DOM after framework or navigation cache restores.

### Fixed

- Reinitialized Basecoat components after HTMX history restores in the docs site.

## [1.0.0] - 2026-06-27

### Breaking Changes

- Removed the CLI workspace from the repo. Template files now ship with `basecoat-css` under `templates/nunjucks` and `templates/jinja`; copy them from `node_modules/basecoat-css/templates/*` instead of installing `basecoat-cli`.

### Added

- Added Nunjucks and Jinja template files to the `basecoat-css` package.
- Added a custom docs 404 page for Cloudflare static asset fallback.

### Changed

- Narrowed dark-mode generated selectors to `html.dark` to reduce broad style recalculation work.
- Switched the docs site to Astro's sitemap integration and updated `robots.txt` to point at the generated sitemap index.

### Fixed

- Updated Scroll Area examples to use Card surfaces so framed examples inherit style-pack radius and border treatment.

## [1.0.0-beta.7] - 2026-06-25

### Added

- Added a beta Drawer component with native `<dialog>` markup, side placement, animated close behavior, backdrop and Escape handling, style-pack visuals, JavaScript entrypoints, and docs.

### Changed

- Updated the docs dependency to `reallysimpledocs@^1.0.2`.
- Marked Chart and Drawer as beta components in the docs navigation.
- Promoted the Chart docs warning from alpha to beta.
- Updated installation CDN examples for `basecoat-css@1.0.0-beta.7`.

### Fixed

- Aligned Drawer examples more closely with upstream shadcn/ui while avoiding Chart API coupling in Drawer docs.

## [1.0.0-beta.6] - 2026-06-23

### Changed

- Updated docs dependency to the published `reallysimpledocs@1.0.0-beta.5` package.
- Refined component documentation examples across the docs site, including Select, Table, Tabs, Switch, and Theme Switcher.
- Clarified CDN and npm installation guidance for default and named style bundles.
- Updated Table examples to avoid inline overlay menus inside scrollable table containers and documented the overflow limitation.

### Fixed

- Fixed dark-mode unchecked Switch thumb colors across all style packs to match upstream shadcn/ui behavior.

## [1.0.0-beta.5] - 2026-06-22

### Added

- Added a dedicated Accordion component with native `<details>` markup, single-item JavaScript behavior, `data-multiple`, disabled item handling, style-pack spacing, and docs.
- Added a dedicated Breadcrumb component with semantic `nav`/`ol` markup, style-pack visuals, collapsed and dropdown examples, and docs.
- Added documented Card action support with `.card-action`.
- Added Combobox clear button, popup trigger, and input-group support, with docs aligned to upstream examples.

### Fixed

- Fixed Combobox single selection reopening immediately after selection and filtering the reopened list to the selected value.
- Improved Combobox multiple chips and remove buttons to match style-pack button sizing more closely.

## [1.0.0-beta.4] - 2026-06-20

### Changed

- Renamed the compact scrollbar utility from `scrollbar-thin` to `scrollbar-sm`; `scrollbar-thin` remains available through the compatibility stylesheet.

## [1.0.0-beta.3] - 2026-06-20

### Breaking Changes

- Changed Button, Badge, Card, Avatar, and Alert visual APIs to use a canonical root class plus data attributes instead of composed visual classes. For example, use `class="btn" data-variant="outline"`, `class="badge" data-variant="secondary"`, `class="card" data-size="sm"`, `class="avatar" data-size="lg"`, and `class="alert" data-variant="destructive"`. Legacy aliases are available only through the optional compatibility stylesheet.
- Changed icon-only Button sizing from `data-icon="only"` plus optional `data-size` to upstream-aligned `data-size="icon|icon-xs|icon-sm|icon-lg"`.

### Added

- Added an opt-in `basecoat-css/compat` stylesheet for pre-1.0 default Basecoat class aliases.
- Added an optional Chart.js helper with `window.basecoat.chart()`, chart CSS, generated tooltips, generated legends, and docs.
- Added shared Alert action layout support for direct child `<footer>` action regions.
- Added dedicated Avatar and Avatar Group component styles and docs.
- Added dedicated Progress component styles and docs with label, controlled, and RTL examples.

## [1.0.0-beta.2] - 2026-06-14

### Breaking Changes

- Removed the `.form` convenience selector for Basecoat 1.0. Use explicit component classes (`label`, `input`, `textarea`, `select`) or compose fields with `.field` / `.fieldset`.
- Changed Combobox markup and behavior to an input-first structure. The visible input now filters options, the hidden input stores the submitted value, single select stores the selected value, and multiple select stores a JSON array.
- Removed Combobox `data-multiple`; use `aria-multiselectable="true"` on the Combobox listbox, matching Select.
- Changed Command markup to the migrated Basecoat structure: `.command-dialog` wraps `.command`, the search input lives in the command header, and items use role-based menu markup with `role="menuitem"`.
- Removed Combobox-specific search-header behavior from Select. Use the dedicated Combobox component for editable/filterable selection.
- Removed built-in document command events for Toast, Sidebar, and Theme. Use element methods instead: `toaster.toast(config)`, `sidebar.open()`, `sidebar.close()`, `sidebar.toggle()`, and `window.basecoat.theme.*`.
- Reworked style loading for style packs. Non-default styles are standalone bundles and should not be loaded on top of the default/Vega bundle.

### Added

- Added standalone style packs: Vega, Nova, Maia, Lyra, Mira, Luma, Sera, and Rhea.
- Added dedicated Empty component styles and docs.
- Added dedicated Item component styles and docs.
- Added dedicated Input Group component styles and docs.
- Added dedicated Spinner docs and examples using `animate-spin` and `size-4` patterns.
- Added style-specific package entrypoints such as `basecoat-css/nova` and styleless base entrypoints for custom themes.
- Added `window.basecoat.refresh(element)` as a generic dispatcher for components that expose `refresh()`.
- Added `refresh()` methods to Command, Select, Combobox, Dropdown Menu, and Tabs for dynamic child lists.
- Added method APIs for Sidebar, Toast, and Theme.
- Added `data-format="object"` to Select and Combobox for opt-in hidden input serialization as `{ value, label }` objects.
- Added `selected` details to Select and Combobox change events and JavaScript properties.
- Added `data-filter="manual"` to Command and Combobox for app-owned remote or local-search result filtering.

### Changed

- Changed `window.basecoat.init(name)` and `window.basecoat.initAll()` to initialize uninitialized components only, instead of forcing global reinitialization.
- Added internal destroy hooks for JavaScript components so removed component roots clean up event listeners and runtime state.
- Reworked component CSS so shared component files own structure and behavior hooks while style-pack files own visual treatment.
- Updated Button, Button Group, Input, Textarea, Select, Combobox, Command, Dialog, Dropdown Menu, Popover, Field, Tabs, Table, Card, Alert, Badge, Kbd, Label, Skeleton, Radio, Switch, Empty, Item, and Input Group toward current shadcn/ui styles.
- Split Native Select documentation from custom Select documentation.
- Updated docs to use Basecoat-specific HTML usage instead of React/shadcn composition APIs.
- Updated docs site styling, navigation, fonts, and style switcher for the 1.0 style system.
- Migrated the docs build to ReallySimpleDocs/Astro while keeping Basecoat's Nunjucks source examples as a pre-render step.
- Changed docs build scripts so local Basecoat package assets are generated before ReallySimpleDocs resolves `basecoat-css`.

### Removed

- Removed the old Form component page. Form layout should now be composed with Field, Fieldset, Input, Textarea, Select, Native Select, Checkbox, Radio, and Switch.

### Fixed

- Fixed destructive Alert descriptions/content using muted text instead of destructive text across all style packs.

### Migration Notes

The `.form` wrapper can't be recreated with `@apply`: Tailwind v4 only applies utilities, not Basecoat's component classes. Wrap each label and control in a `.field` instead:

```html
<div class="field">
  <label for="email">Email</label>
  <input id="email" type="email">
</div>
```

Or add the component class to each element: `class="label"`, `class="input"`, `class="textarea"`, or `class="select"` on a native `<select>`.

To keep the previous document-event command APIs, add bridge listeners in your app:

```js
document.addEventListener('basecoat:toast', (event) => {
  document.getElementById('toaster')?.toast(event.detail?.config || {});
});

document.addEventListener('basecoat:sidebar', (event) => {
  const sidebar = document.getElementById(event.detail?.id || 'sidebar');
  const action = event.detail?.action || 'toggle';
  if (['open', 'close', 'toggle'].includes(action)) sidebar?.[action]();
});

document.addEventListener('basecoat:theme', (event) => {
  const mode = event.detail?.mode;
  mode ? window.basecoat.theme.set(mode) : window.basecoat.theme.toggle();
});
```

"""Ecommerce blocks: cart, mini cart, checkout, orders, account and bottom navigation.

Auvyx originals (shadcn/ui has no ecommerce blocks). Every block is a plain
page built from Auvyx components (card, item, field, badge, sheet, popover,
table, dialog) plus a small block <style>; the scripts are demo behavior
(quantities and totals, steps, filters) that apps replace with their own state.
"""
from common import page, icon, logo, LOGO_CSS

PH = "assets/placeholder.svg"

# Inline Lucide icons (each one is mapped to the other icon libraries in
# packages/docs/tools/icon-map.json and icon-signatures.json).
SHOP_ICONS = {
    "shopping-bag": '<path d="M16 10a4 4 0 0 1-8 0M3.103 6.034h17.794"/><path d="M3.4 5.467a2 2 0 0 0-.4 1.2V20a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6.667a2 2 0 0 0-.4-1.2l-2-2.667A2 2 0 0 0 17 2H7a2 2 0 0 0-1.6.8z"/>',
    "minus": '<path d="M5 12h14"/>',
    "plus": '<path d="M5 12h14"/><path d="M12 5v14"/>',
    "package": '<path d="M11 21.73a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73zm1 .27V12"/><path d="M3.29 7L12 12l8.71-5M7.5 4.27l9 5.15"/>',
    "package-check": '<path d="M12 22V12m4 5l2 2l4-4"/><path d="M21 11.127V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.729l7 4a2 2 0 0 0 2 .001l1.32-.753"/><path d="M3.29 7L12 12l8.71-5M7.5 4.27l8.997 5.148"/>',
    "truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2m10 0H9m10 0h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
    "map-pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "heart": '<path d="M2 9.5a5.5 5.5 0 0 1 9.591-3.676a.56.56 0 0 0 .818 0A5.49 5.49 0 0 1 22 9.5c0 2.29-1.5 4-3 5.5l-5.492 5.313a2 2 0 0 1-3 .019L5 15c-1.5-1.5-3-3.2-3-5.5"/>',
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "circle-check": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "house": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "layout-grid": '<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>',
    "pencil": '<path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497zM15 5l4 4"/>',
    "trash-2": '<path d="M3 6h18"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M10 11v6"/><path d="M14 11v6"/>',
    "gift": '<path d="M12 7v14m8-10v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-8m3.5-4a1 1 0 0 1 0-5A4.8 8 0 0 1 12 7a4.8 8 0 0 1 4.5-5a1 1 0 0 1 0 5"/><rect width="18" height="4" x="3" y="7" rx="1"/>',
    "phone": '<path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233a14 14 0 0 0 6.392 6.384"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"/>',
    "undo-2": '<path d="M9 14L4 9l5-5"/><path d="M4 9h10.5a5.5 5.5 0 0 1 5.5 5.5a5.5 5.5 0 0 1-5.5 5.5H11"/>',
    "download": '<path d="M12 15V3m9 12v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10l5 5l5-5"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "chevron-left": '<path d="m15 18-6-6 6-6"/>',
    "arrow-left": '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "credit-card": '<rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/>',
    "log-out": '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/>',
    "settings": '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "star": '<path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/>',
    "bell": '<path d="M10.268 21a2 2 0 0 0 3.464 0"/><path d="M3.262 15.326A1 1 0 0 0 4 17h16a1 1 0 0 0 .74-1.673C19.41 13.956 18 12.499 18 8A6 6 0 0 0 6 8c0 4.499-1.411 5.956-2.738 7.326"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "eye": '<path d="M2.062 12.348a1 1 0 0 1 0-.696a10.75 10.75 0 0 1 19.876 0a1 1 0 0 1 0 .696a10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/>',
    "arrow-right-left": '<path d="m16 3 4 4-4 4"/><path d="M20 7H4"/><path d="m8 21-4-4 4-4"/><path d="M4 17h16"/>',
    "sliders-horizontal": '<path d="M10 5H3m9 14H3M14 3v4m2 10v4m5-9h-9m9 7h-5m5-14h-7m-6 5v4m0-2H3"/>',
    "trending-up": '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/>',
    "list": '<path d="M3 5h.01"/><path d="M3 12h.01"/><path d="M3 19h.01"/><path d="M8 5h13"/><path d="M8 12h13"/><path d="M8 19h13"/>',
    "rotate-ccw": '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>',
    "shield-check": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12l2 2l4-4"/>',
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "upload": '<path d="M12 3v12"/><path d="m17 8-5-5-5 5"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>',
    "sparkles": '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>',
    "copy": '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
    "share-2": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" x2="15.42" y1="13.51" y2="17.49"/><line x1="15.41" x2="8.59" y1="6.51" y2="10.49"/>',
}


def si(name, **kw):
    return icon(SHOP_ICONS[name], **kw)


def money(v):
    return f"${v:,.2f}"


# ------------------------------------------------------------------ data
PRODUCTS = [
    {"id": "p1", "name": "Everyday Tote", "variant": "Canvas · Natural", "price": 48.00, "qty": 1},
    {"id": "p2", "name": "Merino Crew Sweater", "variant": "Size M · Charcoal", "price": 89.00, "qty": 2},
    {"id": "p3", "name": "Ceramic Pour-Over Set", "variant": "Matte white", "price": 36.50, "qty": 1},
]
CATALOG = [
    ("Everyday Tote", "Canvas · Natural", 48.00),
    ("Merino Crew Sweater", "6 colors", 89.00),
    ("Ceramic Pour-Over Set", "Matte white", 36.50),
    ("Linen Throw Pillow", "3 colors", 32.00),
    ("Leather Card Holder", "Tan", 29.00),
    ("Stoneware Mug", "Set of 2", 24.00),
]
TAX_RATE = 0.08
FREE_SHIPPING = 150.0
SHIPPING = 9.95


def totals(items):
    sub = sum(p["price"] * p["qty"] for p in items)
    ship = 0.0 if sub >= FREE_SHIPPING or sub == 0 else SHIPPING
    tax = round(sub * TAX_RATE, 2)
    return sub, ship, tax, sub + ship + tax


# ------------------------------------------------------------------ CSS
SHOP_CSS = """
  body { background: var(--background); }
  .shop-muted { color: var(--muted-foreground); }
  .shop-page { padding-block: 2rem 4rem; }
  .shop-h1 { margin: 0; font-size: 1.875rem; font-weight: 600; letter-spacing: -0.025em; }
  .shop-h2 { margin: 0; font-size: 1.125rem; font-weight: 600; }
  .shop-lead { margin: 0; color: var(--muted-foreground); font-size: 0.875rem; }
  .shop-header { position: sticky; inset-block-start: 0; z-index: 10; border-block-end: 1px solid var(--border); background: color-mix(in oklab, var(--background) 90%, transparent); backdrop-filter: blur(8px); }
  .shop-header-row { display: flex; align-items: center; gap: 1rem; block-size: 4rem; }
  .shop-nav { display: flex; gap: 1.25rem; font-size: 0.875rem; }
  .shop-nav a { color: var(--muted-foreground); text-decoration: none; }
  .shop-nav a:hover, .shop-nav a[aria-current] { color: var(--foreground); }
  .shop-header-search { flex: 1; max-inline-size: 20rem; margin-inline-start: auto; }
  .shop-header-actions { display: flex; align-items: center; gap: 0.25rem; }
  .shop-cart-btn { position: relative; }
  .shop-count { position: absolute; inset-block-start: -0.25rem; inset-inline-end: -0.25rem; display: inline-flex; align-items: center; justify-content: center; min-inline-size: 1.125rem; block-size: 1.125rem; padding-inline: 0.25rem; border-radius: 999px; background: var(--primary); color: var(--primary-foreground); font-size: 0.6875rem; font-weight: 600; font-variant-numeric: tabular-nums; line-height: 1; }
  .shop-count:empty, .shop-count[data-count='0'] { display: none; }
  @media (width < 48rem) { .shop-nav, .shop-header-search { display: none; } .shop-header-actions { margin-inline-start: auto; } }
  .shop-thumb { flex: none; inline-size: 5rem; block-size: 5rem; border-radius: var(--radius); border: 1px solid var(--border); background: var(--muted); object-fit: cover; }
  .shop-thumb[data-size='sm'] { inline-size: 3.5rem; block-size: 3.5rem; }
  .shop-thumb[data-size='xs'] { inline-size: 2.5rem; block-size: 2.5rem; border-radius: calc(var(--radius) - 2px); }
  html.dark .shop-thumb { filter: brightness(0.5) grayscale(1); }
  html.dark .shop-product-img { filter: brightness(0.5) grayscale(1); }
  .shop-lines { list-style: none; margin: 0; padding: 0; }
  .shop-lines > li { display: flex; gap: 1rem; padding-block: 1.25rem; border-block-end: 1px solid var(--border); }
  .shop-lines > li:first-child { padding-block-start: 0; }
  .shop-lines[data-size='sm'] > li { gap: 0.75rem; padding-block: 0.875rem; }
  .shop-lines[data-size='sm'] > li:last-child { border-block-end: 0; }
  .shop-line-body { flex: 1; min-inline-size: 0; display: flex; flex-direction: column; gap: 0.25rem; }
  .shop-line-top { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; }
  .shop-line-name { margin: 0; font-size: 0.875rem; font-weight: 500; }
  .shop-line-meta { margin: 0; font-size: 0.8125rem; color: var(--muted-foreground); }
  .shop-line-price { margin: 0; font-size: 0.875rem; font-weight: 500; font-variant-numeric: tabular-nums; white-space: nowrap; }
  .shop-line-actions { display: flex; align-items: center; justify-content: space-between; gap: 0.75rem; margin-block-start: auto; padding-block-start: 0.5rem; }
  .shop-qty { display: inline-flex; align-items: center; border: 1px solid var(--input); border-radius: var(--radius); }
  .shop-qty > .btn { border-radius: inherit; }
  .shop-qty > input { inline-size: 2.25rem; block-size: 2rem; border: 0; background: transparent; color: inherit; text-align: center; font: inherit; font-size: 0.875rem; font-variant-numeric: tabular-nums; -moz-appearance: textfield; appearance: textfield; }
  .shop-qty > input::-webkit-inner-spin-button, .shop-qty > input::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
  .shop-qty > input:focus-visible { outline: 2px solid var(--ring); outline-offset: -2px; }
  .shop-qty[data-size='sm'] > input { inline-size: 1.75rem; block-size: 1.75rem; }
  .shop-remove { display: inline-flex; align-items: center; gap: 0.375rem; border: 0; padding: 0; background: none; color: var(--muted-foreground); font: inherit; font-size: 0.8125rem; cursor: pointer; }
  .shop-remove:hover { color: var(--destructive); }
  .shop-remove svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .shop-summary { display: grid; gap: 0.75rem; margin: 0; font-size: 0.875rem; }
  .shop-summary > div { display: flex; justify-content: space-between; gap: 1rem; }
  .shop-summary dt { color: var(--muted-foreground); }
  .shop-summary dd { margin: 0; font-variant-numeric: tabular-nums; }
  .shop-summary > [data-total] { padding-block-start: 0.75rem; border-block-start: 1px solid var(--border); font-size: 1rem; font-weight: 600; }
  .shop-summary > [data-total] dt { color: var(--foreground); }
  .shop-summary > [data-discount] dd { color: var(--primary); }
  .shop-cols { display: grid; gap: 2rem; align-items: start; }
  @media (width >= 56rem) { .shop-cols { grid-template-columns: minmax(0, 1fr) 22rem; gap: 3rem; } .shop-sticky { position: sticky; inset-block-start: 5.5rem; } }
  .shop-note { display: flex; align-items: center; gap: 0.5rem; margin: 0; font-size: 0.8125rem; color: var(--muted-foreground); }
  .shop-note svg { inline-size: 1rem; block-size: 1rem; flex: none; }
  .shop-progress { display: grid; gap: 0.5rem; font-size: 0.8125rem; }
  .shop-progress p { margin: 0; }
  .shop-full { inline-size: 100%; }
  .shop-grid { display: grid; gap: 1.5rem; grid-template-columns: repeat(auto-fill, minmax(min(100%, 13rem), 1fr)); }
  .shop-product { display: flex; flex-direction: column; gap: 0.75rem; }
  .shop-product-img { aspect-ratio: 1; inline-size: 100%; border-radius: var(--radius); background: var(--muted); object-fit: cover; }
  .shop-product h3 { margin: 0; font-size: 0.875rem; font-weight: 500; }
  .shop-product p { margin: 0; font-size: 0.8125rem; color: var(--muted-foreground); }
  .shop-product-foot { display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; }
  .shop-product-foot strong { font-size: 0.875rem; font-weight: 600; font-variant-numeric: tabular-nums; }
  .shop-sheet-lines { flex: 1; overflow-y: auto; }
  .shop-mini { inline-size: min(24rem, calc(100vw - 2rem)); }
  .shop-mini .shop-lines { max-block-size: 18rem; overflow-y: auto; }
  .shop-mini-foot { display: grid; gap: 0.75rem; padding-block-start: 0.75rem; border-block-start: 1px solid var(--border); }
  .shop-mini-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; }
  .shop-row { display: flex; justify-content: space-between; align-items: baseline; gap: 1rem; font-size: 0.875rem; }
  .shop-row strong { font-variant-numeric: tabular-nums; }
  .shop-section-title { margin: 0; font-size: 1rem; font-weight: 600; }
  .shop-steps { display: flex; align-items: center; gap: 0.5rem; list-style: none; margin: 0; padding: 0; font-size: 0.875rem; overflow-x: auto; }
  .shop-steps > li { display: flex; align-items: center; gap: 0.5rem; color: var(--muted-foreground); white-space: nowrap; }
  .shop-steps > li + li::before { content: ''; inline-size: 2rem; block-size: 1px; background: var(--border); }
  .shop-step-num { display: inline-flex; align-items: center; justify-content: center; inline-size: 1.5rem; block-size: 1.5rem; border-radius: 999px; border: 1px solid var(--border); font-size: 0.75rem; font-weight: 600; }
  .shop-step-num svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .shop-steps > li[aria-current] { color: var(--foreground); font-weight: 500; }
  .shop-steps > li[aria-current] .shop-step-num, .shop-steps > li[data-done] .shop-step-num { border-color: var(--primary); background: var(--primary); color: var(--primary-foreground); }
  .shop-steps > li[data-done] { color: var(--foreground); }
  .shop-steps > li .shop-step-num svg, .shop-steps > li[data-done] .shop-step-num span { display: none; }
  .shop-steps > li[data-done] .shop-step-num svg { display: block; }
  .shop-step-actions { display: flex; justify-content: space-between; gap: 0.75rem; }
  .shop-review { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(min(100%, 14rem), 1fr)); }
  .shop-review p { margin: 0; font-size: 0.875rem; }
  .shop-review h3 { margin: 0 0 0.25rem; font-size: 0.875rem; font-weight: 600; }
  .shop-address { margin: 0; font-style: normal; font-size: 0.875rem; line-height: 1.6; }
  .shop-success { display: inline-flex; align-items: center; justify-content: center; inline-size: 3rem; block-size: 3rem; border-radius: 999px; background: color-mix(in oklab, var(--primary) 12%, transparent); color: var(--primary); }
  .shop-success svg { inline-size: 1.5rem; block-size: 1.5rem; }
  .shop-kv { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(min(100%, 9rem), 1fr)); margin: 0; }
  .shop-kv dt { font-size: 0.75rem; color: var(--muted-foreground); }
  .shop-kv dd { margin: 0.25rem 0 0; font-size: 0.875rem; font-weight: 500; }
  .shop-order-head { display: flex; flex-wrap: wrap; align-items: center; gap: 1rem 2rem; }
  .shop-order-head .shop-kv { flex: 1; grid-template-columns: repeat(auto-fit, minmax(min(100%, 6.5rem), 1fr)); }
  .shop-order-actions { display: flex; gap: 0.5rem; }
  .shop-filters { display: flex; flex-wrap: wrap; gap: 0.5rem; }
  .shop-filters .btn[aria-pressed='true'] { background: var(--primary); border-color: var(--primary); color: var(--primary-foreground); }
  .shop-status { gap: 0.25rem; }
  .shop-status::before { content: ''; inline-size: 0.375rem; block-size: 0.375rem; border-radius: 999px; background: currentColor; }
  .shop-status[data-status='processing'] { color: var(--muted-foreground); }
  .shop-status[data-status='shipped'] { color: var(--chart-2, var(--foreground)); }
  .shop-status[data-status='delivered'] { color: var(--primary); }
  .shop-status[data-status='cancelled'] { color: var(--destructive); }
  .shop-tracker { display: grid; grid-template-columns: repeat(4, 1fr); list-style: none; margin: 0; padding: 0; font-size: 0.8125rem; }
  .shop-tracker > li { position: relative; display: flex; flex-direction: column; align-items: center; gap: 0.5rem; text-align: center; color: var(--muted-foreground); }
  .shop-tracker > li::before { content: ''; position: absolute; inset-block-start: 0.875rem; inset-inline: -50% 50%; block-size: 2px; background: var(--border); }
  .shop-tracker > li:first-child::before { display: none; }
  .shop-tracker > li[data-done]::before, .shop-tracker > li[aria-current]::before { background: var(--primary); }
  .shop-tracker-dot { position: relative; display: inline-flex; align-items: center; justify-content: center; inline-size: 1.75rem; block-size: 1.75rem; border-radius: 999px; border: 2px solid var(--border); background: var(--background); }
  .shop-tracker-dot svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .shop-tracker > li[data-done], .shop-tracker > li[aria-current] { color: var(--foreground); }
  .shop-tracker > li[data-done] .shop-tracker-dot { border-color: var(--primary); background: var(--primary); color: var(--primary-foreground); }
  .shop-tracker > li[aria-current] .shop-tracker-dot { border-color: var(--primary); color: var(--primary); }
  .shop-tracker small { display: block; color: var(--muted-foreground); font-size: 0.75rem; }
  .shop-timeline { list-style: none; margin: 0; padding: 0; display: grid; gap: 1.25rem; font-size: 0.875rem; }
  .shop-timeline > li { position: relative; padding-inline-start: 1.5rem; }
  .shop-timeline > li::before { content: ''; position: absolute; inset-inline-start: 0.25rem; inset-block-start: 0.375rem; inline-size: 0.5rem; block-size: 0.5rem; border-radius: 999px; background: var(--border); }
  .shop-timeline > li:first-child::before { background: var(--primary); box-shadow: 0 0 0 4px color-mix(in oklab, var(--primary) 20%, transparent); }
  .shop-timeline > li:not(:last-child)::after { content: ''; position: absolute; inset-inline-start: calc(0.5rem - 0.5px); inset-block: 1.125rem -1rem; inline-size: 1px; background: var(--border); }
  .shop-timeline p { margin: 0; }
  .shop-timeline time { font-size: 0.75rem; color: var(--muted-foreground); }
  .shop-account { display: grid; gap: 2rem; align-items: start; }
  @media (width >= 48rem) { .shop-account { grid-template-columns: 14rem minmax(0, 1fr); } }
  .shop-account-nav ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.125rem; }
  .shop-account-nav a, .shop-account-nav button { display: flex; align-items: center; gap: 0.625rem; inline-size: 100%; padding: 0.5rem 0.75rem; border: 0; border-radius: var(--radius); background: none; color: var(--muted-foreground); font: inherit; font-size: 0.875rem; text-align: start; text-decoration: none; cursor: pointer; }
  .shop-account-nav a:hover, .shop-account-nav button:hover { background: var(--accent); color: var(--accent-foreground); }
  .shop-account-nav a[aria-current] { background: var(--muted); color: var(--foreground); font-weight: 500; }
  .shop-account-nav svg { inline-size: 1rem; block-size: 1rem; flex: none; }
  .shop-account-nav hr { margin: 0.5rem 0; border: 0; border-block-start: 1px solid var(--border); }
  .shop-profile { display: flex; align-items: center; gap: 0.75rem; margin-block-end: 1rem; padding-inline: 0.75rem; }
  .shop-profile p { margin: 0; font-size: 0.875rem; font-weight: 500; }
  .shop-profile small { display: block; font-size: 0.75rem; color: var(--muted-foreground); font-weight: 400; }
  @media (width < 48rem) { .shop-account-nav ul { display: flex; overflow-x: auto; } .shop-account-nav a, .shop-account-nav button { white-space: nowrap; } .shop-account-nav hr, .shop-profile { display: none; } }
  .shop-stats { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(min(100%, 10rem), 1fr)); }
  .shop-stat header p { display: flex; align-items: center; gap: 0.5rem; }
  .shop-stat header p svg { inline-size: 1rem; block-size: 1rem; }
  .shop-stat h3 { margin: 0; font-size: 1.5rem; font-weight: 600; font-variant-numeric: tabular-nums; }
  .shop-addresses { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fill, minmax(min(100%, 16rem), 1fr)); }
  .shop-add-card { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; min-block-size: 12rem; border: 1px dashed var(--border); border-radius: var(--radius); background: none; color: var(--muted-foreground); font: inherit; font-size: 0.875rem; cursor: pointer; }
  .shop-add-card:hover { border-color: var(--ring); color: var(--foreground); }
  .shop-add-card svg { inline-size: 1.25rem; block-size: 1.25rem; }
  .shop-form-grid { display: grid; gap: 1rem; }
  @media (width >= 36rem) { .shop-form-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
  .shop-form-grid select { inline-size: 100%; }
  .shop-form-grid > [data-span='full'] { grid-column: 1 / -1; }
  .shop-switch-row { display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
  .shop-switch-title { font-size: 0.875rem; font-weight: 500; }
  .shop-switch-row small { display: block; font-size: 0.8125rem; color: var(--muted-foreground); }
  .shop-app { max-inline-size: 28rem; min-block-size: 100svh; margin-inline: auto; padding-block-end: calc(5rem + env(safe-area-inset-bottom, 0px)); border-inline: 1px solid var(--border); }
  .shop-app-bar { position: sticky; inset-block-start: 0; z-index: 5; display: flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1rem; background: var(--background); border-block-end: 1px solid var(--border); }
  .shop-app-bar h1 { flex: 1; margin: 0; font-size: 1rem; font-weight: 600; }
  .shop-app-body { display: grid; gap: 1.25rem; padding: 1rem; }
  .shop-chips { display: flex; gap: 0.5rem; overflow-x: auto; scrollbar-width: none; }
  .shop-chips .badge { padding: 0.25rem 0.75rem; }
  .shop-banner { display: grid; gap: 0.25rem; padding: 1.25rem; border-radius: var(--radius); background: var(--primary); color: var(--primary-foreground); }
  .shop-banner p { margin: 0; font-size: 0.875rem; opacity: 0.85; }
  .shop-banner strong { font-size: 1.125rem; }
  .shop-bottom-nav { position: fixed; inset-block-end: 0; inset-inline: 0; z-index: 20; max-inline-size: 28rem; margin-inline: auto; padding-block-end: env(safe-area-inset-bottom, 0px); border-block-start: 1px solid var(--border); background: color-mix(in oklab, var(--background) 92%, transparent); backdrop-filter: blur(8px); }
  .shop-bottom-nav ul { display: grid; grid-auto-columns: 1fr; grid-auto-flow: column; list-style: none; margin: 0; padding: 0; }
  .shop-bottom-nav a { position: relative; display: flex; flex-direction: column; align-items: center; gap: 0.25rem; padding-block: 0.625rem 0.5rem; color: var(--muted-foreground); font-size: 0.6875rem; font-weight: 500; text-decoration: none; -webkit-tap-highlight-color: transparent; }
  .shop-bottom-nav a svg { inline-size: 1.375rem; block-size: 1.375rem; }
  .shop-bottom-nav a[aria-current='page'] { color: var(--foreground); }
  .shop-bottom-nav a[aria-current='page']::before { content: ''; position: absolute; inset-block-start: 0; inline-size: 2rem; block-size: 2px; border-radius: 0 0 2px 2px; background: var(--primary); }
  .shop-bottom-nav a:focus-visible { outline: 2px solid var(--ring); outline-offset: -2px; }
  .shop-nav-icon { position: relative; display: inline-flex; }
  .shop-nav-icon > .shop-count { inset-block-start: -0.375rem; inset-inline-end: -0.625rem; }
  .shop-bottom-nav[data-variant='floating'] { inset-block-end: calc(1rem + env(safe-area-inset-bottom, 0px)); inset-inline: 1rem; max-inline-size: 26rem; padding: 0.375rem; border: 1px solid var(--border); border-radius: 999px; box-shadow: 0 10px 30px -10px rgb(0 0 0 / 0.25); }
  .shop-bottom-nav[data-variant='floating'] a { padding-block: 0.5rem; border-radius: 999px; }
  .shop-bottom-nav[data-variant='floating'] a[aria-current='page'] { background: var(--primary); color: var(--primary-foreground); }
  .shop-bottom-nav[data-variant='floating'] a[aria-current='page']::before { display: none; }
  .shop-bottom-nav[data-variant='floating'] a > span:not(.shop-nav-icon) { display: none; }
  .shop-bottom-nav[data-variant='floating'] a[aria-current='page'] { flex-direction: row; justify-content: center; }
  .shop-bottom-nav[data-variant='floating'] a[aria-current='page'] > span:not(.shop-nav-icon) { display: inline; font-size: 0.75rem; }
  .shop-buy-bar { position: fixed; inset-block-end: 0; inset-inline: 0; z-index: 20; display: flex; align-items: center; gap: 0.75rem; max-inline-size: 28rem; margin-inline: auto; padding: 0.75rem 1rem calc(0.75rem + env(safe-area-inset-bottom, 0px)); border-block-start: 1px solid var(--border); background: var(--background); }
  .shop-buy-bar > div:first-child { display: grid; }
  .shop-buy-bar small { font-size: 0.75rem; color: var(--muted-foreground); }
  .shop-buy-bar strong { font-size: 1.125rem; font-variant-numeric: tabular-nums; }
  .shop-buy-bar > .btn:last-child { flex: 1; }
  .shop-rating { display: flex; align-items: center; gap: 0.25rem; font-size: 0.8125rem; color: var(--muted-foreground); }
  .shop-rating svg { inline-size: 0.875rem; block-size: 0.875rem; fill: currentColor; color: var(--foreground); }
  .shop-swatches { display: flex; gap: 0.5rem; border: 0; margin: 0; padding: 0; }
  .shop-swatches legend { margin-block-end: 0.5rem; font-size: 0.875rem; font-weight: 500; }
  .shop-swatches label { position: relative; display: inline-flex; align-items: center; justify-content: center; min-inline-size: 2.5rem; block-size: 2.25rem; padding-inline: 0.75rem; border: 1px solid var(--input); border-radius: var(--radius); font-size: 0.875rem; cursor: pointer; }
  .shop-swatches input { position: absolute; opacity: 0; pointer-events: none; }
  .shop-swatches label:has(:checked) { border-color: var(--primary); box-shadow: 0 0 0 1px var(--primary); }
  .shop-swatches label:has(:focus-visible) { outline: 2px solid var(--ring); outline-offset: 2px; }
  .shop-gallery { aspect-ratio: 1; inline-size: 100%; background: var(--muted); object-fit: cover; }
  .shop-payment-fields[hidden] { display: none; }

  /* Circles and pills stay round when a style sets --corner-shape (squircle on a 999px radius draws a rounded square). */
  .shop-colors label { corner-shape: round; }
  .shop-dots > span { corner-shape: round; }
  .shop-fx-swatches > button { corner-shape: round; }
  .shop-count { corner-shape: round; }
  .shop-status-icon { corner-shape: round; }
  .shop-map-pin { corner-shape: round; }
  .shop-tracker-dot { corner-shape: round; }
  .shop-step-num { corner-shape: round; }
  .shop-success { corner-shape: round; }
  .shop-stock::before { corner-shape: round; }
  .shop-status::before { corner-shape: round; }
  .shop-subcats img { corner-shape: round; }
  .shop-order-no { corner-shape: round; }
  .shop-tile-go { corner-shape: round; }
  .shop-pills a { corner-shape: round; }
  .shop-timeline > li::before { corner-shape: round; }
  .shop-bottom-nav { corner-shape: round; }
  .shop-bottom-nav a { corner-shape: round; }
""" + LOGO_CSS


# ------------------------------------------------------------------ pieces
def store_header(cart_count=4, current="Shop", cart_button=None, prefix=""):
    links = "".join(
        f'<a href="#"{" aria-current=\"page\"" if t == current else ""}>{t}</a>' for t in ["Shop", "New in", "Collections", "Journal"]
    )
    cart = cart_button or (
        f'<a href="#" class="btn shop-cart-btn" data-variant="ghost" data-size="icon" aria-label="Cart, {cart_count} items">'
        f'{si("shopping-bag")}<span class="shop-count" data-cart-count>{cart_count}</span></a>'
    )
    return f"""<header class="shop-header">
  <div class="wrapper shop-header-row">
    {logo("Acme Store")}
    <nav class="shop-nav" aria-label="Main">{links}</nav>
    <div class="input-group shop-header-search">
      <input type="search" placeholder="Search products..." aria-label="Search products">
      <span data-align="start" aria-hidden="true">{si("search")}</span>
    </div>
    <div class="shop-header-actions">
      <a href="#" class="btn" data-variant="ghost" data-size="icon" aria-label="Wishlist">{si("heart")}</a>
      <a href="#" class="btn" data-variant="ghost" data-size="icon" aria-label="Account">{si("user")}</a>
      {cart}
    </div>
  </div>
</header>"""


def qty(pid, value, size=None, label="Quantity"):
    sz = ' data-size="sm"' if size == "sm" else ""
    bs = "icon-xs" if size == "sm" else "icon-sm"
    return (
        f'<div class="shop-qty"{sz} role="group" aria-label="{label}">'
        f'<button type="button" class="btn" data-variant="ghost" data-size="{bs}" aria-label="Decrease quantity" data-qty-step="-1">{si("minus")}</button>'
        f'<input type="number" id="{pid}-qty" value="{value}" min="1" max="10" inputmode="numeric" aria-label="Quantity" data-qty>'
        f'<button type="button" class="btn" data-variant="ghost" data-size="{bs}" aria-label="Increase quantity" data-qty-step="1">{si("plus")}</button>'
        "</div>"
    )


def cart_line(p, prefix, size=None):
    thumb = ' data-size="sm"' if size == "sm" else ""
    line_total = p["price"] * p["qty"]
    return f"""<li data-line data-price="{p['price']:.2f}">
  <img class="shop-thumb"{thumb} src="{PH}" alt="">
  <div class="shop-line-body">
    <div class="shop-line-top">
      <div>
        <h3 class="shop-line-name"><a href="#" class="shop-link">{p['name']}</a></h3>
        <p class="shop-line-meta">{p['variant']}</p>
      </div>
      <p class="shop-line-price" data-line-total>{money(line_total)}</p>
    </div>
    <div class="shop-line-actions">
      {qty(prefix + p['id'], p['qty'], size)}
      <button type="button" class="shop-remove" data-remove>{si("trash-2")}Remove</button>
    </div>
  </div>
</li>"""


def summary(items, discount=None, rows_extra=""):
    sub, ship, tax, total = totals(items)
    d = ""
    if discount:
        total -= discount[1]
        d = f'<div data-discount><dt>Discount ({discount[0]})</dt><dd>-{money(discount[1])}</dd></div>'
    return f"""<dl class="shop-summary">
  <div><dt>Subtotal</dt><dd data-subtotal>{money(sub)}</dd></div>
  <div><dt>Shipping</dt><dd data-shipping>{"Free" if ship == 0 else money(ship)}</dd></div>
  <div><dt>Estimated tax</dt><dd data-tax>{money(tax)}</dd></div>
  {d}{rows_extra}
  <div data-total><dt>Total</dt><dd data-grand-total>{money(total)}</dd></div>
</dl>"""


# Cart behavior shared by the cart blocks: quantity steppers, remove, and the
# totals, item count and free-shipping progress inside each [data-cart].
CART_JS = """
document.querySelectorAll('[data-cart]').forEach((cart) => {
  const fmt = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });
  const FREE = %(free)s, SHIP = %(ship)s, TAX = %(tax)s;
  const set = (sel, text) => document.querySelectorAll(sel).forEach((el) => { el.textContent = text; });
  const update = () => {
    let sub = 0, count = 0;
    cart.querySelectorAll('[data-line]').forEach((line) => {
      const q = Math.min(10, Math.max(1, parseInt(line.querySelector('[data-qty]').value, 10) || 1));
      line.querySelector('[data-qty]').value = q;
      const price = parseFloat(line.dataset.price);
      sub += price * q;
      count += q;
      const t = line.querySelector('[data-line-total]');
      if (t) t.textContent = fmt.format(price * q);
    });
    const ship = sub === 0 || sub >= FREE ? 0 : SHIP;
    const tax = Math.round(sub * TAX * 100) / 100;
    set('[data-subtotal]', fmt.format(sub));
    set('[data-shipping]', ship ? fmt.format(ship) : 'Free');
    set('[data-tax]', fmt.format(tax));
    set('[data-grand-total]', fmt.format(sub + ship + tax));
    set('[data-item-count]', count + (count === 1 ? ' item' : ' items'));
    document.querySelectorAll('[data-cart-count]').forEach((el) => { el.textContent = count; el.dataset.count = count; });
    const bar = cart.querySelector('[data-free-progress]');
    if (bar) {
      const pct = Math.round(Math.min(sub, FREE) / FREE * 100);
      bar.setAttribute('aria-valuenow', pct);
      bar.querySelector('span').style.width = pct + '%%';
      set('[data-free-label]', sub >= FREE ? 'You have free shipping.' : fmt.format(FREE - sub) + ' away from free shipping.');
    }
    const empty = !cart.querySelector('[data-line]');
    cart.querySelectorAll('[data-cart-filled]').forEach((el) => { el.hidden = empty; });
    cart.querySelectorAll('[data-cart-empty]').forEach((el) => { el.hidden = !empty; });
  };
  cart.addEventListener('click', (e) => {
    const step = e.target.closest('[data-qty-step]');
    if (step) {
      const input = step.parentElement.querySelector('[data-qty]');
      input.value = (parseInt(input.value, 10) || 1) + Number(step.dataset.qtyStep);
      update();
    }
    const remove = e.target.closest('[data-remove]');
    if (remove) { remove.closest('[data-line]').remove(); update(); }
  });
  cart.addEventListener('change', (e) => { if (e.target.matches('[data-qty]')) update(); });
});
""" % {"free": FREE_SHIPPING, "ship": SHIPPING, "tax": TAX_RATE}


# Quantity steppers outside a cart (product pages).
QTY_JS = """
document.querySelectorAll('.shop-qty').forEach((g) => {
  const input = g.querySelector('[data-qty]');
  g.addEventListener('click', (e) => {
    const step = e.target.closest('[data-qty-step]');
    if (step) input.value = Math.min(10, Math.max(1, (parseInt(input.value, 10) || 1) + Number(step.dataset.qtyStep)));
  });
});
"""


def script(js):
    return f"<script>{js}</script>\n"


def count(items):
    return sum(p["qty"] for p in items)


def free_progress(items):
    sub = totals(items)[0]
    pct = round(min(sub, FREE_SHIPPING) / FREE_SHIPPING * 100)
    label = "You have free shipping." if sub >= FREE_SHIPPING else f"{money(FREE_SHIPPING - sub)} away from free shipping."
    return f"""<div class="shop-progress">
  <p class="shop-note">{si("truck")}<span data-free-label>{label}</span></p>
  <div class="progress" role="progressbar" aria-label="Progress to free shipping" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{pct}" data-free-progress><span style="width: {pct}%"></span></div>
</div>"""


EMPTY_CART = f"""<section class="empty" data-cart-empty hidden>
  <header>
    <figure>{si("shopping-bag")}</figure>
    <h3>Your cart is empty</h3>
    <p>Looks like you haven't added anything yet.</p>
  </header>
  <footer>
    <a href="#" class="btn">Continue shopping</a>
  </footer>
</section>"""

blocks = []


def add(bid, title, desc, cat, body, css=SHOP_CSS, scripts="", body_class=""):
    page(bid, title, body, css, body_class=body_class, scripts=scripts)
    blocks.append({"id": bid, "title": title, "description": desc, "category": cat})


# ================================================================== cart
items = PRODUCTS
lines = "\n".join(cart_line(p, "c1-") for p in items)
add("cart-01", "Cart 01", "A cart page with quantity steppers, a promo code and an order summary.", "cart", f"""
{store_header(count(items))}
<main class="wrapper shop-page" data-cart>
  <div class="stack" data-gap="8">
    <div class="stack" data-gap="1">
      <h1 class="shop-h1">Shopping cart</h1>
      <p class="shop-lead" data-item-count>{count(items)} items</p>
    </div>
    <div class="shop-cols" data-cart-filled>
      <section aria-label="Items in your cart">
        <ul class="shop-lines">
          {lines}
        </ul>
      </section>
      <aside class="card shop-sticky" aria-labelledby="c1-summary">
        <header>
          <h2 id="c1-summary">Order summary</h2>
        </header>
        <section class="stack" data-gap="6">
          {free_progress(items)}
          {summary(items)}
          <form class="stack" data-gap="2" onsubmit="event.preventDefault()">
            <label class="label" for="c1-promo">Promo code</label>
            <div class="cluster" data-gap="2">
              <input class="input shop-promo" id="c1-promo" type="text" placeholder="Enter code" autocomplete="off">
              <button type="submit" class="btn" data-variant="outline">Apply</button>
            </div>
          </form>
        </section>
        <footer class="stack" data-gap="3">
          <a href="#" class="btn shop-full" data-size="lg">Checkout</a>
          <p class="shop-note">{si("lock")}Secure checkout. Free returns within 30 days.</p>
        </footer>
      </aside>
    </div>
    {EMPTY_CART}
  </div>
</main>
""", SHOP_CSS + "\n  .shop-promo { flex: 1; min-inline-size: 0; }\n  .shop-link { color: inherit; text-decoration: none; }\n  .shop-link:hover { text-decoration: underline; text-underline-offset: 4px; }", scripts=script(CART_JS))

add("cart-02", "Cart 02", "An empty cart with suggested products.", "cart", f"""
{store_header(0)}
<main class="wrapper shop-page">
  <div class="stack" data-gap="12">
    <section class="empty">
      <header>
        <figure>{si("shopping-bag")}</figure>
        <h3>Your cart is empty</h3>
        <p>Items you add to your cart will show up here. Start with something from the shop.</p>
      </header>
      <footer>
        <div class="cluster" data-gap="2" data-justify="center">
          <a href="#" class="btn">Start shopping</a>
          <a href="#" class="btn" data-variant="outline">{si("heart")}View wishlist</a>
        </div>
      </footer>
    </section>
    <section class="stack" data-gap="4" aria-labelledby="c2-picks">
      <div class="cluster" data-justify="between">
        <h2 class="shop-h2" id="c2-picks">Popular right now</h2>
        <a href="#" class="btn" data-variant="link" data-size="sm">View all{si("arrow-right")}</a>
      </div>
      <div class="shop-grid">
        {"".join(f'''<article class="shop-product">
          <img class="shop-product-img" src="{PH}" alt="">
          <div><h3>{n}</h3><p>{v}</p></div>
          <div class="shop-product-foot"><strong>{money(pr)}</strong><button type="button" class="btn" data-variant="outline" data-size="sm">{si("plus")}Add</button></div>
        </article>''' for n, v, pr in CATALOG[:4])}
      </div>
    </section>
  </div>
</main>
""")

# Mini cart in a sheet, opened from the store header.
sheet_lines = "\n".join(cart_line(p, "c3-", "sm") for p in items)
cart_trigger = (
    f'<button type="button" class="btn shop-cart-btn" data-variant="ghost" data-size="icon" aria-label="Open cart" commandfor="c3-cart" command="show-modal">'
    f'{si("shopping-bag")}<span class="shop-count" data-cart-count>{count(items)}</span></button>'
)
add("cart-03", "Cart 03", "A mini cart in a sheet, opened from the store header.", "cart", f"""
<div data-cart>
  {store_header(count(items), cart_button=cart_trigger)}
  <main class="wrapper shop-page">
    <div class="stack" data-gap="6">
      <div class="stack" data-gap="1">
        <h1 class="shop-h1">New in</h1>
        <p class="shop-lead">Fresh pieces for slower mornings.</p>
      </div>
      <div class="shop-grid">
        {"".join(f'''<article class="shop-product">
          <img class="shop-product-img" src="{PH}" alt="">
          <div><h3>{n}</h3><p>{v}</p></div>
          <div class="shop-product-foot"><strong>{money(pr)}</strong><button type="button" class="btn" data-variant="outline" data-size="sm" commandfor="c3-cart" command="show-modal">{si("plus")}Add</button></div>
        </article>''' for n, v, pr in CATALOG)}
      </div>
    </div>
  </main>
  <dialog id="c3-cart" class="sheet" data-side="right" closedby="any" aria-labelledby="c3-cart-title">
    <header>
      <h2 id="c3-cart-title">Your cart</h2>
      <p data-item-count>{count(items)} items</p>
    </header>
    <section class="shop-sheet-lines">
      <div class="stack" data-gap="4" data-cart-filled>
        {free_progress(items)}
        <ul class="shop-lines" data-size="sm">
          {sheet_lines}
        </ul>
      </div>
      {EMPTY_CART}
    </section>
    <footer>
      <div class="stack" data-gap="3" data-cart-filled>
        {summary(items)}
        <a href="#" class="btn shop-full">Checkout</a>
        <button type="button" class="btn shop-full" data-variant="outline" commandfor="c3-cart" command="close">Continue shopping</button>
      </div>
    </footer>
    <button type="button" aria-label="Close" commandfor="c3-cart" command="close">{si("x")}</button>
  </dialog>
</div>
""", SHOP_CSS + "\n  .shop-link { color: inherit; text-decoration: none; }\n  .shop-link:hover { text-decoration: underline; text-underline-offset: 4px; }", scripts=script(CART_JS))

# Mini cart in a popover.
mini_items = PRODUCTS[:2]
mini_lines = "\n".join(f"""<li data-line data-price="{p['price']:.2f}">
  <img class="shop-thumb" data-size="sm" src="{PH}" alt="">
  <div class="shop-line-body">
    <div class="shop-line-top">
      <div>
        <p class="shop-line-name">{p['name']}</p>
        <p class="shop-line-meta">{p['variant']} · Qty {p['qty']}</p>
      </div>
      <p class="shop-line-price">{money(p['price'] * p['qty'])}</p>
    </div>
  </div>
  <input type="hidden" value="{p['qty']}" data-qty>
  <button type="button" class="btn" data-variant="ghost" data-size="icon-xs" aria-label="Remove {p['name']}" data-remove>{si("x")}</button>
</li>""" for p in mini_items)
popover_cart = f"""<div class="popover" data-cart>
  <button type="button" class="btn shop-cart-btn" data-variant="ghost" data-size="icon" popovertarget="c4-mini" aria-label="Cart">{si("shopping-bag")}<span class="shop-count" data-cart-count>{count(mini_items)}</span></button>
  <div id="c4-mini" class="shop-mini" data-popover popover data-side="bottom" data-align="end">
    <header>
      <h4>Cart</h4>
      <p data-item-count>{count(mini_items)} items</p>
    </header>
    <div class="stack" data-gap="3" data-cart-filled>
      <ul class="shop-lines" data-size="sm">
        {mini_lines}
      </ul>
      <div class="shop-mini-foot">
        <div class="shop-row"><span class="shop-muted">Subtotal</span><strong data-subtotal>{money(totals(mini_items)[0])}</strong></div>
        <p class="shop-note">Shipping and taxes calculated at checkout.</p>
        <div class="shop-mini-actions">
          <a href="#" class="btn" data-variant="outline">View cart</a>
          <a href="#" class="btn">Checkout</a>
        </div>
      </div>
    </div>
    <p class="shop-note" data-cart-empty hidden>{si("shopping-bag")}Your cart is empty.</p>
  </div>
</div>"""
add("cart-04", "Cart 04", "A mini cart in a popover from the header cart button.", "cart", f"""
{store_header(count(mini_items), cart_button=popover_cart)}
<main class="wrapper shop-page">
  <div class="stack" data-gap="6">
    <div class="stack" data-gap="1">
      <h1 class="shop-h1">Collections</h1>
      <p class="shop-lead">Open the cart in the header to see the mini cart.</p>
    </div>
    <div class="shop-grid">
      {"".join(f'''<article class="shop-product">
        <img class="shop-product-img" src="{PH}" alt="">
        <div><h3>{n}</h3><p>{v}</p></div>
        <div class="shop-product-foot"><strong>{money(pr)}</strong></div>
      </article>''' for n, v, pr in CATALOG[:4])}
    </div>
  </div>
</main>
""", SHOP_CSS + "\n  .shop-lines[data-size='sm'] > li { align-items: flex-start; }", scripts=script(CART_JS))


# ================================================================== checkout
def field(label, id_, type_="text", placeholder=None, value=None, autocomplete=None, span=None, required=True):
    ph = f' placeholder="{placeholder}"' if placeholder else ""
    v = f' value="{value}"' if value else ""
    ac = f' autocomplete="{autocomplete}"' if autocomplete else ""
    sp = f' data-span="{span}"' if span else ""
    rq = " required" if required else ""
    return f'<div role="group" class="field"{sp}><label for="{id_}">{label}</label><input id="{id_}" type="{type_}"{ph}{v}{ac}{rq}></div>'


def select(label, id_, options, autocomplete=None, span=None):
    ac = f' autocomplete="{autocomplete}"' if autocomplete else ""
    sp = f' data-span="{span}"' if span else ""
    opts = "".join(f"<option>{o}</option>" for o in options)
    return f'<div role="group" class="field"{sp}><label for="{id_}">{label}</label><select class="select" id="{id_}"{ac}>{opts}</select></div>'


def address_fields(p):
    return f"""<div class="shop-form-grid">
  {field("First name", p + "first", autocomplete="given-name")}
  {field("Last name", p + "last", autocomplete="family-name")}
  {field("Address", p + "address", placeholder="Street and house number", autocomplete="address-line1", span="full")}
  {field("Apartment, suite, etc.", p + "address2", autocomplete="address-line2", span="full", required=False)}
  {field("City", p + "city", autocomplete="address-level2")}
  {select("Country", p + "country", ["United States", "Canada", "United Kingdom", "Vietnam"], autocomplete="country-name")}
  {field("ZIP code", p + "zip", autocomplete="postal-code")}
  {field("Phone", p + "phone", "tel", autocomplete="tel", required=False)}
</div>"""


DELIVERY = [("standard", "Standard", "4–6 business days", "Free"), ("express", "Express", "1–2 business days", "$14.00"), ("pickup", "Store pickup", "Ready tomorrow", "Free")]


def choice_cards(name, p, options, checked=0, label="Options"):
    out = []
    for i, (val, title, desc, price) in enumerate(options):
        c = " checked" if i == checked else ""
        out.append(f"""<label for="{p}{val}">
  <div role="group" class="field" data-orientation="horizontal">
    <section><h3>{title}</h3><p>{desc}</p></section>
    <span class="shop-choice-price">{price}</span>
    <input type="radio" id="{p}{val}" name="{name}" value="{val}" class="input"{c}>
  </div>
</label>""")
    return f'<div role="radiogroup" aria-label="{label}" data-slot="radio-group">' + "\n".join(out) + "</div>"


PAYMENTS = [("card", "Credit card", "Visa, Mastercard, Amex", ""), ("paypal", "PayPal", "You'll be redirected to PayPal", ""), ("cod", "Cash on delivery", "Pay when the order arrives", "")]


def card_fields(p):
    return f"""<div class="shop-form-grid shop-payment-fields" data-payment-fields="card">
  {field("Card number", p + "cc", placeholder="1234 1234 1234 1234", autocomplete="cc-number", span="full")}
  {field("Expiry", p + "exp", placeholder="MM / YY", autocomplete="cc-exp")}
  {field("CVC", p + "cvc", placeholder="123", autocomplete="cc-csc")}
  {field("Name on card", p + "ccname", autocomplete="cc-name", span="full")}
</div>"""


PAYMENT_JS = """
document.querySelectorAll('[data-payment]').forEach((group) => {
  const sync = () => {
    const v = group.querySelector('input:checked')?.value;
    document.querySelectorAll('[data-payment-fields]').forEach((el) => { el.hidden = el.dataset.paymentFields !== v; });
  };
  group.addEventListener('change', sync);
  sync();
});
"""


def order_lines_sm(items):
    return "\n".join(f"""<li>
  <img class="shop-thumb" data-size="sm" src="{PH}" alt="">
  <div class="shop-line-body">
    <div class="shop-line-top">
      <div>
        <p class="shop-line-name">{p['name']}</p>
        <p class="shop-line-meta">{p['variant']} · Qty {p['qty']}</p>
      </div>
      <p class="shop-line-price">{money(p['price'] * p['qty'])}</p>
    </div>
  </div>
</li>""" for p in items)


CHOICE_CSS = "\n  .shop-choice-price { font-size: 0.875rem; font-weight: 500; font-variant-numeric: tabular-nums; }"

add("checkout-01", "Checkout 01", "A one-page checkout: contact, shipping, delivery, payment and the order summary.", "checkout", f"""
<header class="shop-header">
  <div class="wrapper shop-header-row">
    {logo("Acme Store")}
    <p class="shop-note shop-header-secure">{si("lock")}Secure checkout</p>
  </div>
</header>
<main class="wrapper shop-page">
  <form class="shop-cols" onsubmit="event.preventDefault()">
    <div class="stack" data-gap="8">
      <fieldset class="fieldset">
        <legend>Contact</legend>
        <p>We'll send the receipt and shipping updates here.</p>
        {field("Email", "co1-email", "email", "you@example.com", autocomplete="email")}
        <div role="group" class="field" data-orientation="horizontal">
          <input type="checkbox" id="co1-news" class="input" checked>
          <label for="co1-news">Email me with news and offers</label>
        </div>
      </fieldset>
      <fieldset class="fieldset">
        <legend>Shipping address</legend>
        {address_fields("co1-")}
      </fieldset>
      <fieldset class="fieldset">
        <legend>Delivery</legend>
        {choice_cards("co1-delivery", "co1-", DELIVERY, label="Delivery method")}
      </fieldset>
      <fieldset class="fieldset">
        <legend>Payment</legend>
        <p>All transactions are secure and encrypted.</p>
        <div data-payment>{choice_cards("co1-pay", "co1-pay-", PAYMENTS, label="Payment method")}</div>
        {card_fields("co1-")}
      </fieldset>
    </div>
    <aside class="card shop-sticky" aria-labelledby="co1-summary">
      <header>
        <h2 id="co1-summary">Order summary</h2>
        <div class="card-action"><a href="#" class="btn" data-variant="link" data-size="sm">Edit cart</a></div>
      </header>
      <section class="stack" data-gap="6">
        <ul class="shop-lines" data-size="sm">
          {order_lines_sm(PRODUCTS)}
        </ul>
        {summary(PRODUCTS)}
      </section>
      <footer class="stack" data-gap="3">
        <button type="submit" class="btn shop-full" data-size="lg">{si("lock")}Pay {money(totals(PRODUCTS)[3])}</button>
        <p class="shop-note">By placing your order you agree to our Terms and Privacy Policy.</p>
      </footer>
    </aside>
  </form>
</main>
""", SHOP_CSS + CHOICE_CSS + "\n  .shop-header-secure { margin-inline-start: auto; }", scripts=script(PAYMENT_JS))

STEPS = ["Shipping", "Delivery", "Payment", "Review"]
steps_nav = "".join(
    f'<li data-step-label="{i}"{" aria-current=\"step\"" if i == 0 else ""}><span class="shop-step-num"><span>{i + 1}</span>{si("check")}</span>{s}</li>'
    for i, s in enumerate(STEPS))


def step_panel(i, title, body):
    hidden = "" if i == 0 else " hidden"
    back = f'<button type="button" class="btn" data-variant="outline" data-step-go="{i - 1}">{si("arrow-left")}Back</button>' if i else '<a href="#" class="btn" data-variant="ghost">' + si("arrow-left") + 'Return to cart</a>'
    nxt = (f'<button type="button" class="btn" data-step-go="{i + 1}">Continue to {STEPS[i + 1].lower()}{si("arrow-right")}</button>'
           if i < len(STEPS) - 1 else f'<button type="submit" class="btn">{si("lock")}Place order</button>')
    return f"""<section class="card" data-step="{i}" aria-labelledby="co2-step-{i}"{hidden}>
  <header><h2 id="co2-step-{i}" tabindex="-1">{title}</h2></header>
  <section>{body}</section>
  <footer class="shop-step-actions">{back}{nxt}</footer>
</section>"""


REVIEW = f"""<div class="stack" data-gap="6">
  <div class="shop-review">
    <div>
      <h3>Ship to</h3>
      <address class="shop-address">Olivia Martin<br>1234 Market Street, Apt 5<br>San Francisco, CA 94103<br>United States</address>
    </div>
    <div>
      <h3>Delivery</h3>
      <p>Standard · 4–6 business days</p>
      <h3 class="shop-mt">Payment</h3>
      <p>Visa ending in 4242</p>
    </div>
  </div>
  <ul class="shop-lines" data-size="sm">
    {order_lines_sm(PRODUCTS)}
  </ul>
</div>"""

STEP_JS = """
document.querySelectorAll('[data-steps]').forEach((root) => {
  const panels = root.querySelectorAll('[data-step]');
  const labels = root.querySelectorAll('[data-step-label]');
  const go = (n) => {
    panels.forEach((p) => { p.hidden = Number(p.dataset.step) !== n; });
    labels.forEach((l) => {
      const i = Number(l.dataset.stepLabel);
      l.toggleAttribute('data-done', i < n);
      if (i === n) l.setAttribute('aria-current', 'step'); else l.removeAttribute('aria-current');
    });
    root.querySelector(`[data-step="${n}"] h2`)?.focus({ preventScroll: true });
  };
  root.addEventListener('click', (e) => {
    const b = e.target.closest('[data-step-go]');
    if (b) go(Number(b.dataset.stepGo));
  });
});
"""

add("checkout-02", "Checkout 02", "A multi-step checkout with a step indicator and a review step.", "checkout", f"""
<header class="shop-header">
  <div class="wrapper shop-header-row">
    {logo("Acme Store")}
    <p class="shop-note shop-header-secure">{si("lock")}Secure checkout</p>
  </div>
</header>
<main class="wrapper shop-page">
  <form class="shop-cols" data-steps onsubmit="event.preventDefault()">
    <div class="stack" data-gap="6">
      <ol class="shop-steps" aria-label="Checkout steps">{steps_nav}</ol>
      {step_panel(0, "Shipping address", address_fields("co2-"))}
      {step_panel(1, "Delivery method", choice_cards("co2-delivery", "co2-", DELIVERY, label="Delivery method"))}
      {step_panel(2, "Payment", '<div class="stack" data-gap="6"><div data-payment>' + choice_cards("co2-pay", "co2-pay-", PAYMENTS, label="Payment method") + "</div>" + card_fields("co2-") + "</div>")}
      {step_panel(3, "Review your order", REVIEW)}
    </div>
    <aside class="card shop-sticky" aria-labelledby="co2-summary">
      <header>
        <h2 id="co2-summary">Summary</h2>
        <p>{count(PRODUCTS)} items</p>
      </header>
      <section class="stack" data-gap="6">
        <div class="cluster" data-gap="2">
          <input class="input shop-promo" type="text" placeholder="Gift card or discount code" aria-label="Discount code">
          <button type="button" class="btn" data-variant="outline">Apply</button>
        </div>
        {summary(PRODUCTS, discount=("WELCOME10", 10.00))}
      </section>
    </aside>
  </form>
</main>
""", SHOP_CSS + CHOICE_CSS + "\n  .shop-header-secure { margin-inline-start: auto; }\n  .shop-promo { flex: 1; min-inline-size: 0; }\n  .shop-review h3.shop-mt { margin-block-start: 1rem; }\n  [data-step] h2:focus { outline: none; }",
    scripts=script(PAYMENT_JS + STEP_JS))

add("checkout-03", "Checkout 03", "An order confirmation page with the order details and next steps.", "checkout", f"""
{store_header(0)}
<main class="wrapper shop-page" data-size="md">
  <div class="stack" data-gap="8">
    <div class="stack" data-gap="3" data-align="start">
      <span class="shop-success">{si("circle-check")}</span>
      <p class="shop-lead">Order #A-10294</p>
      <h1 class="shop-h1">Thanks for your order, Olivia!</h1>
      <p class="shop-lead">We've sent a confirmation to olivia@example.com. You'll get another email when it ships.</p>
    </div>
    <div class="card">
      <section>
        <dl class="shop-kv">
          <div><dt>Order date</dt><dd>Nov 7, 2026</dd></div>
          <div><dt>Estimated delivery</dt><dd>Nov 12 – Nov 14</dd></div>
          <div><dt>Payment</dt><dd>Visa •••• 4242</dd></div>
          <div><dt>Total</dt><dd>{money(totals(PRODUCTS)[3])}</dd></div>
        </dl>
      </section>
    </div>
    <div class="shop-cols shop-cols-even">
      <section class="card" aria-labelledby="co3-items">
        <header><h2 id="co3-items">Items</h2></header>
        <section class="stack" data-gap="6">
          <ul class="shop-lines" data-size="sm">
            {order_lines_sm(PRODUCTS)}
          </ul>
          {summary(PRODUCTS)}
        </section>
      </section>
      <div class="stack" data-gap="6">
        <section class="card" aria-labelledby="co3-ship">
          <header><h2 id="co3-ship">Shipping to</h2></header>
          <section>
            <address class="shop-address">Olivia Martin<br>1234 Market Street, Apt 5<br>San Francisco, CA 94103<br>United States</address>
          </section>
        </section>
        <section class="card" aria-labelledby="co3-next">
          <header><h2 id="co3-next">What's next</h2></header>
          <section>
            <ul class="shop-next">
              <li>{si("mail")}<span>A confirmation email is on its way.</span></li>
              <li>{si("package")}<span>We pack your order within 24 hours.</span></li>
              <li>{si("truck")}<span>Track the delivery from your account.</span></li>
            </ul>
          </section>
        </section>
      </div>
    </div>
    <div class="cluster" data-gap="2">
      <a href="#" class="btn">{si("package")}Track order</a>
      <a href="#" class="btn" data-variant="outline">Continue shopping</a>
      <button type="button" class="btn" data-variant="ghost">{si("download")}Download invoice</button>
    </div>
  </div>
</main>
""", SHOP_CSS + """
  @media (width >= 56rem) { .shop-cols.shop-cols-even { grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr); } }
  .shop-next { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.875rem; font-size: 0.875rem; }
  .shop-next li { display: flex; gap: 0.75rem; align-items: flex-start; }
  .shop-next svg { inline-size: 1rem; block-size: 1rem; flex: none; margin-block-start: 0.125rem; color: var(--muted-foreground); }""")


# ================================================================== account shell
ACCOUNT_NAV = [("Overview", "house"), ("Orders", "package"), ("Wishlist", "heart"), ("Addresses", "map-pin"), ("Payment methods", "credit-card"), ("Account settings", "settings")]


def account(current, content):
    links = "".join(
        f'<li><a href="#"{" aria-current=\"page\"" if t == current else ""}>{si(i)}{t}</a></li>' for t, i in ACCOUNT_NAV)
    return f"""{store_header(3)}
<main class="wrapper shop-page">
  <div class="shop-account">
    <nav class="shop-account-nav" aria-label="Account">
      <div class="shop-profile">
        <img class="avatar" src="{PH}" alt="">
        <p>Olivia Martin<small>olivia@example.com</small></p>
      </div>
      <ul>
        {links}
        <li><hr></li>
        <li><button type="button">{si("log-out")}Sign out</button></li>
      </ul>
    </nav>
    <div class="stack" data-gap="8">
      {content}
    </div>
  </div>
</main>"""


ORDERS = [
    ("A-10294", "Nov 7, 2026", "processing", "Processing", 274.49, [PRODUCTS[0], PRODUCTS[1], PRODUCTS[2]]),
    ("A-10251", "Oct 28, 2026", "shipped", "Shipped", 52.92, [PRODUCTS[2]]),
    ("A-10188", "Oct 3, 2026", "delivered", "Delivered", 106.27, [PRODUCTS[1]]),
    ("A-10102", "Sep 12, 2026", "delivered", "Delivered", 61.79, [PRODUCTS[0]]),
    ("A-10077", "Aug 30, 2026", "cancelled", "Cancelled", 34.56, [PRODUCTS[0]]),
]


def status_badge(key, label):
    return f'<span class="badge shop-status" data-variant="outline" data-status="{key}">{label}</span>'


recent_rows = "\n".join(
    f'<tr><td><a href="#" class="shop-link">#{n}</a></td><td>{d}</td><td>{status_badge(k, l)}</td><td class="shop-num">{money(t)}</td></tr>'
    for n, d, k, l, t, _ in ORDERS[:3])

add("account-01", "Account 01", "An account overview with stats, recent orders and the default address.", "account", account("Overview", f"""
<div class="stack" data-gap="1">
  <h1 class="shop-h1">Welcome back, Olivia</h1>
  <p class="shop-lead">Manage your orders, addresses and account details.</p>
</div>
<div class="shop-stats">
  <div class="card shop-stat"><header><p>{si("package")}Orders</p><h3>12</h3></header></div>
  <div class="card shop-stat"><header><p>{si("heart")}Wishlist</p><h3>8</h3></header></div>
  <div class="card shop-stat"><header><p>{si("gift")}Reward points</p><h3>1,240</h3></header></div>
</div>
<section class="card" aria-labelledby="a1-recent">
  <header>
    <h2 id="a1-recent">Recent orders</h2>
    <p>Your last three orders.</p>
    <div class="card-action"><a href="#" class="btn" data-variant="outline" data-size="sm">View all</a></div>
  </header>
  <section class="shop-table-wrap">
    <table class="table">
      <thead><tr><th>Order</th><th>Date</th><th>Status</th><th class="shop-num">Total</th></tr></thead>
      <tbody>
        {recent_rows}
      </tbody>
    </table>
  </section>
</section>
<div class="shop-review">
  <section class="card" aria-labelledby="a1-address">
    <header>
      <h2 id="a1-address">Default address</h2>
      <div class="card-action"><a href="#" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Edit address">{si("pencil")}</a></div>
    </header>
    <section><address class="shop-address">Olivia Martin<br>1234 Market Street, Apt 5<br>San Francisco, CA 94103<br>United States</address></section>
  </section>
  <section class="card" aria-labelledby="a1-pay">
    <header>
      <h2 id="a1-pay">Payment method</h2>
      <div class="card-action"><a href="#" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Edit payment method">{si("pencil")}</a></div>
    </header>
    <section class="stack" data-gap="1"><p class="shop-row"><span>Visa •••• 4242</span><span class="badge" data-variant="secondary">Default</span></p><p class="shop-note">Expires 08/28</p></section>
  </section>
</div>
"""), SHOP_CSS + """
  .shop-link { color: inherit; font-weight: 500; text-decoration: none; }
  .shop-link:hover { text-decoration: underline; text-underline-offset: 4px; }
  .shop-num { text-align: end; font-variant-numeric: tabular-nums; }
  .shop-table-wrap { overflow-x: auto; }
  .shop-profile .avatar { inline-size: 2.25rem; block-size: 2.25rem; }""")

add("account-02", "Account 02", "Account settings: personal details, password and email preferences.", "account", account("Account settings", f"""
<div class="stack" data-gap="1">
  <h1 class="shop-h1">Account settings</h1>
  <p class="shop-lead">Update your personal details and how we contact you.</p>
</div>
<form class="card" onsubmit="event.preventDefault()" aria-labelledby="a2-details">
  <header>
    <h2 id="a2-details">Personal details</h2>
    <p>This information appears on your orders and invoices.</p>
  </header>
  <section>
    <div class="shop-form-grid">
      {field("First name", "a2-first", value="Olivia", autocomplete="given-name")}
      {field("Last name", "a2-last", value="Martin", autocomplete="family-name")}
      {field("Email", "a2-email", "email", value="olivia@example.com", autocomplete="email")}
      {field("Phone", "a2-phone", "tel", value="+1 (555) 010-2048", autocomplete="tel", required=False)}
      {field("Date of birth", "a2-dob", "date", required=False)}
    </div>
  </section>
  <footer class="shop-card-actions"><button type="submit" class="btn">Save changes</button></footer>
</form>
<form class="card" onsubmit="event.preventDefault()" aria-labelledby="a2-password">
  <header>
    <h2 id="a2-password">Password</h2>
    <p>Use at least 8 characters with a mix of letters and numbers.</p>
  </header>
  <section>
    <div class="shop-form-grid">
      {field("Current password", "a2-current", "password", autocomplete="current-password", span="full")}
      {field("New password", "a2-new", "password", autocomplete="new-password")}
      {field("Confirm password", "a2-confirm", "password", autocomplete="new-password")}
    </div>
  </section>
  <footer class="shop-card-actions"><button type="submit" class="btn" data-variant="outline">Update password</button></footer>
</form>
<section class="card" aria-labelledby="a2-notify">
  <header>
    <h2 id="a2-notify">Email preferences</h2>
    <p>Choose the emails you want to get.</p>
  </header>
  <section class="stack" data-gap="4">
    {"".join(f'''<div class="shop-switch-row"><label for="a2-n{i}"><span class="shop-switch-title">{t}</span><small>{d}</small></label><input type="checkbox" role="switch" class="input" id="a2-n{i}"{" checked" if on else ""}></div>''' for i, (t, d, on) in enumerate([
        ("Order updates", "Confirmations, shipping and delivery notices.", True),
        ("Back in stock", "When an item on your wishlist is available again.", True),
        ("Newsletter", "New arrivals, stories and offers, twice a month.", False),
    ]))}
  </section>
</section>
<section class="card shop-danger" aria-labelledby="a2-delete">
  <header>
    <h2 id="a2-delete">Delete account</h2>
    <p>Permanently remove your account, order history and saved addresses.</p>
  </header>
  <footer class="shop-card-actions"><button type="button" class="btn" data-variant="destructive">Delete account</button></footer>
</section>
"""), SHOP_CSS + """
  .shop-card-actions { justify-content: flex-end; }
  .shop-danger { border-color: color-mix(in oklab, var(--destructive) 40%, var(--border)); }
  .shop-switch-row > label { flex: 1; cursor: pointer; }
  .shop-profile .avatar { inline-size: 2.25rem; block-size: 2.25rem; }""")

ADDRESSES = [
    ("Home", "Olivia Martin", "1234 Market Street, Apt 5", "San Francisco, CA 94103", "+1 (555) 010-2048", True),
    ("Work", "Olivia Martin", "500 Howard Street, Floor 3", "San Francisco, CA 94105", "+1 (555) 010-7731", False),
    ("Parents", "Daniel Martin", "88 Lakeview Drive", "Portland, OR 97201", "+1 (555) 014-3390", False),
]
addr_cards = "\n".join(f"""<article class="card" data-size="sm">
  <header>
    <h2 class="shop-addr-title">{si("map-pin")}{label}{' <span class="badge" data-variant="secondary">Default</span>' if default else ""}</h2>
  </header>
  <section><address class="shop-address">{name}<br>{l1}<br>{l2}<br>{phone}</address></section>
  <footer class="cluster" data-gap="2">
    <button type="button" class="btn" data-variant="outline" data-size="sm" commandfor="a3-dialog" command="show-modal">{si("pencil")}Edit</button>
    {"" if default else '<button type="button" class="btn" data-variant="ghost" data-size="sm">Set as default</button>'}
    {"" if default else '<button type="button" class="btn shop-push" data-variant="ghost" data-size="icon-sm" aria-label="Delete ' + label + ' address">' + si("trash-2") + "</button>"}
  </footer>
</article>""" for label, name, l1, l2, phone, default in ADDRESSES)

add("account-03", "Account 03", "An address book with a default address and an add-address dialog.", "account", account("Addresses", f"""
<div class="cluster" data-justify="between" data-gap="4">
  <div class="stack" data-gap="1">
    <h1 class="shop-h1">Addresses</h1>
    <p class="shop-lead">Saved addresses for faster checkout.</p>
  </div>
  <button type="button" class="btn" commandfor="a3-dialog" command="show-modal">{si("plus")}Add address</button>
</div>
<div class="shop-addresses">
  {addr_cards}
  <button type="button" class="shop-add-card" commandfor="a3-dialog" command="show-modal">{si("plus")}Add a new address</button>
</div>
<dialog id="a3-dialog" class="dialog" closedby="any" aria-labelledby="a3-dialog-title">
  <div>
    <header>
      <h2 id="a3-dialog-title">Address</h2>
      <p>Add or update a shipping address.</p>
    </header>
    <section>
      <form id="a3-form" class="stack" data-gap="4" onsubmit="event.preventDefault()">
        {field("Label", "a3-label", placeholder="Home, Work…")}
        {address_fields("a3-")}
        <div role="group" class="field" data-orientation="horizontal">
          <input type="checkbox" id="a3-default" class="input">
          <label for="a3-default">Use as my default address</label>
        </div>
      </form>
    </section>
    <footer>
      <button type="button" class="btn" data-variant="outline" commandfor="a3-dialog" command="close">Cancel</button>
      <button type="submit" form="a3-form" class="btn">Save address</button>
    </footer>
    <button type="button" aria-label="Close" commandfor="a3-dialog" command="close">{si("x")}</button>
  </div>
</dialog>
"""), SHOP_CSS + """
  .shop-addr-title { display: flex; align-items: center; gap: 0.5rem; }
  .shop-addr-title svg { inline-size: 1rem; block-size: 1rem; color: var(--muted-foreground); }
  .shop-push { margin-inline-start: auto; }
  .shop-profile .avatar { inline-size: 2.25rem; block-size: 2.25rem; }""")


# ================================================================== orders
def order_card(n, d, k, l, t, its):
    thumbs = "".join(f"""<li>
  <img class="shop-thumb" data-size="sm" src="{PH}" alt="">
  <div class="shop-line-body">
    <p class="shop-line-name">{p['name']}</p>
    <p class="shop-line-meta">{p['variant']} · Qty {p['qty']}</p>
  </div>
  <a href="#" class="btn" data-variant="outline" data-size="sm">{"Buy again" if k in ("delivered", "cancelled") else "View item"}</a>
</li>""" for p in its)
    action = {"processing": "Cancel order", "shipped": "Track package", "delivered": "Return items", "cancelled": "Reorder"}[k]
    note = {"processing": "Preparing your order", "shipped": "Arrives Nov 10", "delivered": f"Delivered on {d}", "cancelled": "Refunded to Visa •••• 4242"}[k]
    note_icon = {"processing": "clock", "shipped": "truck", "delivered": "package-check", "cancelled": "info"}[k]
    return f"""<article class="card" data-order-status="{k}">
  <header class="shop-order-head">
    <dl class="shop-kv">
      <div><dt>Order</dt><dd>#{n}</dd></div>
      <div><dt>Placed</dt><dd>{d}</dd></div>
      <div><dt>Total</dt><dd>{money(t)}</dd></div>
      <div><dt>Status</dt><dd>{status_badge(k, l)}</dd></div>
    </dl>
    <div class="shop-order-actions">
      <a href="#" class="btn" data-variant="outline" data-size="sm">View order</a>
      <button type="button" class="btn" data-variant="ghost" data-size="sm">{si("download")}Invoice</button>
    </div>
  </header>
  <section>
    <ul class="shop-lines shop-order-items" data-size="sm">
      {thumbs}
    </ul>
  </section>
  <footer class="shop-order-foot">
    <p class="shop-note">{si(note_icon)}{note}</p>
    <button type="button" class="btn" data-variant="link" data-size="sm">{action}</button>
  </footer>
</article>"""


ORDER_FILTER_JS = """
document.querySelectorAll('[data-order-filter]').forEach((bar) => {
  const list = document.getElementById(bar.dataset.orderFilter);
  bar.addEventListener('click', (e) => {
    const b = e.target.closest('button[data-filter]');
    if (!b) return;
    bar.querySelectorAll('button[data-filter]').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
    let shown = 0;
    list.querySelectorAll('[data-order-status]').forEach((o) => {
      o.hidden = b.dataset.filter !== 'all' && o.dataset.orderStatus !== b.dataset.filter;
      if (!o.hidden) shown++;
    });
    list.querySelector('[data-orders-empty]').hidden = shown > 0;
  });
});
"""
filters = "".join(
    f'<button type="button" class="btn" data-variant="outline" data-size="sm" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{l}</button>'
    for k, l in [("all", "All"), ("processing", "Processing"), ("shipped", "Shipped"), ("delivered", "Delivered"), ("cancelled", "Cancelled")])

ORDER_CSS = """
  .shop-order-items > li { align-items: center; }
  .shop-order-foot { justify-content: space-between; flex-wrap: wrap; gap: 0.5rem; }
  .shop-profile .avatar { inline-size: 2.25rem; block-size: 2.25rem; }"""

add("orders-01", "Orders 01", "Order history with status filters, items and actions per order.", "orders", account("Orders", f"""
<div class="stack" data-gap="1">
  <h1 class="shop-h1">Orders</h1>
  <p class="shop-lead">Check the status of recent orders, manage returns and download invoices.</p>
</div>
<div class="shop-filters" role="group" aria-label="Filter orders" data-order-filter="o1-list">{filters}</div>
<div class="stack" data-gap="4" id="o1-list">
  {"".join(order_card(*o) for o in ORDERS)}
  <section class="empty" data-orders-empty hidden>
    <header>
      <figure>{si("package")}</figure>
      <h3>No orders here</h3>
      <p>No orders match this status.</p>
    </header>
  </section>
</div>
"""), SHOP_CSS + ORDER_CSS, scripts=script(ORDER_FILTER_JS))

TRACKER = [("Ordered", "Nov 7", True, False), ("Shipped", "Nov 8", True, False), ("Out for delivery", "Nov 10", False, True), ("Delivered", "Est. Nov 10", False, False)]
tracker = "".join(
    f'<li{" data-done" if done else ""}{" aria-current=\"step\"" if cur else ""}><span class="shop-tracker-dot">{si("check") if done else si("truck") if cur else ""}</span><span>{t}<small>{d}</small></span></li>'
    for t, d, done, cur in TRACKER)
EVENTS = [
    ("Out for delivery", "San Francisco, CA", "Nov 10, 8:12 AM"),
    ("Arrived at local facility", "Oakland, CA", "Nov 9, 9:40 PM"),
    ("In transit", "Reno, NV", "Nov 8, 6:05 PM"),
    ("Shipped", "Salt Lake City, UT", "Nov 8, 10:21 AM"),
    ("Order confirmed", "Online", "Nov 7, 3:47 PM"),
]
events = "".join(f'<li><p><strong>{t}</strong></p><p class="shop-muted">{w}</p><time>{d}</time></li>' for t, w, d in EVENTS)

add("orders-02", "Orders 02", "Order details with a delivery tracker, tracking history, items and payment.", "orders", account("Orders", f"""
<div class="stack" data-gap="4">
  <a href="#" class="btn shop-back" data-variant="ghost" data-size="sm">{si("arrow-left")}All orders</a>
  <div class="cluster" data-justify="between" data-gap="4">
    <div class="stack" data-gap="1">
      <div class="cluster" data-gap="3"><h1 class="shop-h1">Order #A-10251</h1>{status_badge("shipped", "Shipped")}</div>
      <p class="shop-lead">Placed on Nov 7, 2026 · 3 items</p>
    </div>
    <div class="cluster" data-gap="2">
      <button type="button" class="btn" data-variant="outline">{si("download")}Invoice</button>
      <button type="button" class="btn" data-variant="outline">{si("undo-2")}Return items</button>
    </div>
  </div>
</div>
<section class="card" aria-labelledby="o2-delivery">
  <header>
    <h2 id="o2-delivery">Arriving today</h2>
    <p>UPS · Tracking 1Z 999 AA1 0123 4567 84</p>
    <div class="card-action"><a href="#" class="btn" data-variant="outline" data-size="sm">Track on UPS</a></div>
  </header>
  <section class="stack" data-gap="8">
    <ol class="shop-tracker" aria-label="Delivery progress">{tracker}</ol>
    <ol class="shop-timeline" aria-label="Tracking history">{events}</ol>
  </section>
</section>
<div class="shop-cols shop-cols-even">
  <section class="card" aria-labelledby="o2-items">
    <header><h2 id="o2-items">Items</h2></header>
    <section class="stack" data-gap="6">
      <ul class="shop-lines" data-size="sm">
        {order_lines_sm(PRODUCTS)}
      </ul>
      {summary(PRODUCTS)}
    </section>
  </section>
  <div class="stack" data-gap="6">
    <section class="card" aria-labelledby="o2-ship">
      <header><h2 id="o2-ship">Shipping address</h2></header>
      <section><address class="shop-address">Olivia Martin<br>1234 Market Street, Apt 5<br>San Francisco, CA 94103<br>United States</address></section>
    </section>
    <section class="card" aria-labelledby="o2-pay">
      <header><h2 id="o2-pay">Payment</h2></header>
      <section class="stack" data-gap="1"><p class="shop-row"><span>Visa •••• 4242</span><span class="shop-muted">Paid</span></p><p class="shop-note">Billing address same as shipping.</p></section>
    </section>
    <section class="card" aria-labelledby="o2-help">
      <header><h2 id="o2-help">Need help?</h2></header>
      <section class="stack" data-gap="2">
        <a href="#" class="btn shop-full" data-variant="outline">{si("mail")}Contact support</a>
        <a href="#" class="btn shop-full" data-variant="ghost">{si("phone")}+1 (555) 010-0000</a>
      </section>
    </section>
  </div>
</div>
"""), SHOP_CSS + """
  @media (width >= 56rem) { .shop-cols.shop-cols-even { grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr); } }
  .shop-back { align-self: flex-start; margin-inline-start: -0.5rem; }
  .shop-profile .avatar { inline-size: 2.25rem; block-size: 2.25rem; }
  @media (width < 36rem) { .shop-tracker > li > span:last-child { font-size: 0.6875rem; } }""")


# ================================================================== bottom navigation
def bottom_nav(items, current, variant=None, cart=0):
    out = []
    for label, ic_ in items:
        badge = f'<span class="shop-count" data-count="{cart}">{cart}</span>' if label == "Cart" and cart else ""
        cur = ' aria-current="page"' if label == current else ""
        out.append(f'<li><a href="#"{cur}><span class="shop-nav-icon">{si(ic_)}{badge}</span><span>{label}</span></a></li>')
    v = f' data-variant="{variant}"' if variant else ""
    return f'<nav class="shop-bottom-nav"{v} aria-label="Primary"><ul>{"".join(out)}</ul></nav>'


NAV_ITEMS = [("Home", "house"), ("Categories", "layout-grid"), ("Wishlist", "heart"), ("Cart", "shopping-bag"), ("Account", "user")]

BOTTOM_NAV_JS = """
document.querySelectorAll('.shop-bottom-nav').forEach((nav) => {
  nav.addEventListener('click', (e) => {
    const a = e.target.closest('a');
    if (!a) return;
    e.preventDefault();
    nav.querySelectorAll('a[aria-current]').forEach((x) => x.removeAttribute('aria-current'));
    a.setAttribute('aria-current', 'page');
  });
});
"""


def app_home(title="Discover"):
    chips = "".join(f'<span class="badge"{" data-variant=\"outline\"" if i else ""}>{c}</span>' for i, c in enumerate(["All", "Home", "Apparel", "Kitchen", "Accessories"]))
    products = "".join(f'''<article class="shop-product">
      <img class="shop-product-img" src="{PH}" alt="">
      <div><h3>{n}</h3><p>{v}</p></div>
      <div class="shop-product-foot"><strong>{money(pr)}</strong><button type="button" class="btn" data-variant="outline" data-size="icon-sm" aria-label="Add {n} to cart">{si("plus")}</button></div>
    </article>''' for n, v, pr in CATALOG[:4])
    return f"""<header class="shop-app-bar">
  <h1>{title}</h1>
  <a href="#" class="btn" data-variant="ghost" data-size="icon" aria-label="Search">{si("search")}</a>
  <a href="#" class="btn" data-variant="ghost" data-size="icon" aria-label="Notifications">{si("bell")}</a>
</header>
<div class="shop-app-body">
  <div class="shop-banner"><p>Members only</p><strong>15% off your first order</strong></div>
  <div class="shop-chips">{chips}</div>
  <div class="shop-grid shop-grid-2">{products}</div>
</div>"""


APP_CSS = SHOP_CSS + "\n  .shop-grid.shop-grid-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }"

add("bottom-nav-01", "Bottom Navigation 01", "A mobile app shell with a bottom tab bar and a cart badge.", "bottom-nav", f"""
<div class="shop-app">
  {app_home()}
</div>
{bottom_nav(NAV_ITEMS, "Home", cart=3)}
""", APP_CSS, scripts=script(BOTTOM_NAV_JS))

add("bottom-nav-02", "Bottom Navigation 02", "A floating pill tab bar that shows the label of the active tab.", "bottom-nav", f"""
<div class="shop-app">
  {app_home("Shop")}
</div>
{bottom_nav(NAV_ITEMS, "Home", variant="floating", cart=3)}
""", APP_CSS + "\n  .shop-app { padding-block-end: calc(6.5rem + env(safe-area-inset-bottom, 0px)); }", scripts=script(BOTTOM_NAV_JS))

sizes = "".join(f'<label><input type="radio" name="bn3-size" value="{s}"{" checked" if s == "M" else ""}{" disabled" if s == "XL" else ""}>{s}</label>' for s in ["XS", "S", "M", "L", "XL"])
add("bottom-nav-03", "Bottom Navigation 03", "A mobile product page with a sticky add-to-cart bar.", "bottom-nav", f"""
<div class="shop-app">
  <header class="shop-app-bar">
    <a href="#" class="btn" data-variant="ghost" data-size="icon" aria-label="Back">{si("chevron-left")}</a>
    <h1>Merino Crew Sweater</h1>
    <a href="#" class="btn shop-cart-btn" data-variant="ghost" data-size="icon" aria-label="Cart">{si("shopping-bag")}<span class="shop-count" data-count="2">2</span></a>
  </header>
  <img class="shop-gallery" src="{PH}" alt="">
  <div class="shop-app-body">
    <div class="stack" data-gap="2">
      <div class="cluster" data-justify="between" data-align="start">
        <div class="stack" data-gap="1">
          <h2 class="shop-h2">Merino Crew Sweater</h2>
          <p class="shop-rating">{si("star")}4.8 <span>· 214 reviews</span></p>
        </div>
        <button type="button" class="btn" data-variant="outline" data-size="icon" aria-label="Add to wishlist">{si("heart")}</button>
      </div>
      <p class="shop-lead">Soft, breathable extra-fine merino in a relaxed fit. Knitted in Portugal.</p>
    </div>
    <fieldset class="shop-swatches">
      <legend>Size</legend>
      {sizes}
    </fieldset>
    <div class="accordion">
      <details>
        <summary>Details and care</summary>
        <section><p class="shop-lead">100% extra-fine merino wool. Machine wash cold on a wool cycle, dry flat.</p></section>
      </details>
      <details>
        <summary>Shipping and returns</summary>
        <section><p class="shop-lead">Free shipping over $150. Free returns within 30 days.</p></section>
      </details>
    </div>
  </div>
  <div class="shop-buy-bar">
    <div><small>Price</small><strong>$89.00</strong></div>
    {qty("bn3", 1)}
    <button type="button" class="btn" data-size="lg">{si("shopping-bag")}Add to cart</button>
  </div>
</div>
""", SHOP_CSS + "\n  .shop-swatches label:has(:disabled) { opacity: 0.5; text-decoration: line-through; cursor: not-allowed; }", scripts=script(QTY_JS))


# ================================================================== catalog data
ITEMS = [
    {"id": "tote", "name": "Everyday Tote", "cat": "Bags", "price": 48.00, "was": None, "rating": 4.7, "reviews": 128, "badge": "New", "colors": [("Natural", "#e8dcc4"), ("Black", "#262626"), ("Olive", "#6b6b3a")], "desc": "Heavy canvas tote with a leather handle and an inner pocket."},
    {"id": "sweater", "name": "Merino Crew Sweater", "cat": "Apparel", "price": 89.00, "was": 119.00, "rating": 4.8, "reviews": 214, "badge": "Sale", "colors": [("Charcoal", "#3f3f46"), ("Oat", "#d6cbb5"), ("Navy", "#1e3a5f")], "desc": "Extra-fine merino in a relaxed fit. Knitted in Portugal."},
    {"id": "pourover", "name": "Ceramic Pour-Over Set", "cat": "Kitchen", "price": 36.50, "was": None, "rating": 4.6, "reviews": 87, "badge": None, "colors": [("White", "#f4f4f5"), ("Sand", "#d8c3a5")], "desc": "Dripper, carafe and two cups in matte stoneware."},
    {"id": "pillow", "name": "Linen Throw Pillow", "cat": "Home", "price": 32.00, "was": 40.00, "rating": 4.5, "reviews": 64, "badge": "Sale", "colors": [("Clay", "#c2856a"), ("Sage", "#9caf88"), ("Ivory", "#f1ead8")], "desc": "Stonewashed linen cover with a feather insert."},
    {"id": "card", "name": "Leather Card Holder", "cat": "Accessories", "price": 29.00, "was": None, "rating": 4.9, "reviews": 301, "badge": "Bestseller", "colors": [("Tan", "#b07a4f"), ("Black", "#262626")], "desc": "Vegetable-tanned leather with four card slots."},
    {"id": "mug", "name": "Stoneware Mug", "cat": "Kitchen", "price": 24.00, "was": None, "rating": 4.4, "reviews": 52, "badge": None, "colors": [("Speckle", "#e7e2d8"), ("Ink", "#2b3442")], "desc": "Set of two hand-glazed mugs, 12 oz."},
    {"id": "lamp", "name": "Arc Table Lamp", "cat": "Home", "price": 129.00, "was": None, "rating": 4.7, "reviews": 39, "badge": "New", "colors": [("Brass", "#b8933f"), ("Black", "#262626")], "desc": "Dimmable LED table lamp with a brushed metal arm."},
    {"id": "scarf", "name": "Wool Blend Scarf", "cat": "Apparel", "price": 45.00, "was": 60.00, "rating": 4.3, "reviews": 28, "badge": "Sale", "colors": [("Camel", "#c19a6b"), ("Grey", "#9ca3af")], "desc": "Soft brushed wool blend, 180 × 30 cm."},
]

CATALOG_CSS = """
  .shop-shot { display: block; aspect-ratio: 4 / 5; inline-size: 100%; object-fit: cover; background: var(--muted); }
  .shop-shot[data-shot='2'] { transform: scaleX(-1); filter: hue-rotate(160deg) saturate(1.6); }
  .shop-shot[data-shot='3'] { filter: sepia(0.6) saturate(1.4); }
  .shop-shot[data-shot='4'] { transform: scaleX(-1); filter: grayscale(1) contrast(1.2); }
  html.dark .shop-shot { opacity: 0.6; }
  .shop-card { position: relative; display: flex; flex-direction: column; gap: 0.75rem; }
  .shop-card-media { position: relative; overflow: hidden; border-radius: var(--radius); background: var(--muted); }
  .shop-card-media > img { display: block; aspect-ratio: 4 / 5; inline-size: 100%; object-fit: cover; transition: transform 300ms ease; }
  .shop-card:hover .shop-card-media > img { transform: scale(1.03); }
  html.dark .shop-card-media > img { filter: brightness(0.5) grayscale(1); }
  html.dark .shop-pdp-main { filter: brightness(0.5) grayscale(1); }
  html.dark .shop-pdp-thumbs img { filter: brightness(0.5) grayscale(1); }
  .shop-card-badge { position: absolute; inset-block-start: 0.75rem; inset-inline-start: 0.75rem; }
  .shop-card-tools { position: absolute; inset-block-start: 0.5rem; inset-inline-end: 0.5rem; display: grid; gap: 0.375rem; }
  .shop-card-tools .btn { background: var(--background); }
  .shop-card-quick { position: absolute; inset-inline: 0.75rem; inset-block-end: 0.75rem; opacity: 0; transform: translateY(0.5rem); transition: opacity 200ms ease, transform 200ms ease; }
  .shop-card:hover .shop-card-quick, .shop-card:focus-within .shop-card-quick { opacity: 1; transform: none; }
  @media (hover: none) { .shop-card-quick { opacity: 1; transform: none; } }
  .shop-card-body { display: grid; gap: 0.25rem; }
  .shop-card-cat { margin: 0; font-size: 0.75rem; color: var(--muted-foreground); text-transform: uppercase; letter-spacing: 0.04em; }
  .shop-card-name { margin: 0; font-size: 0.9375rem; font-weight: 500; }
  .shop-card-name a { color: inherit; text-decoration: none; }
  .shop-card-name a::after { content: ''; position: absolute; inset: 0; }
  .shop-card-name a:focus-visible { outline: none; }
  .shop-card:has(.shop-card-name a:focus-visible) .shop-card-media { outline: 2px solid var(--ring); outline-offset: 2px; }
  .shop-card-tools { z-index: 2; }
  .shop-card-quick { z-index: 2; }
  .shop-card-actions { position: relative; z-index: 1; }
  .shop-dots { position: relative; z-index: 1; }
  .shop-cmp-check { position: relative; z-index: 1; }
  .shop-colors { position: relative; z-index: 1; }
  .shop-price { display: flex; align-items: baseline; gap: 0.5rem; margin: 0; font-variant-numeric: tabular-nums; }
  .shop-price strong { font-size: 0.9375rem; font-weight: 600; }
  .shop-price s { font-size: 0.8125rem; color: var(--muted-foreground); }
  .shop-price[data-size='lg'] strong { font-size: 1.5rem; }
  .shop-price[data-size='lg'] s { font-size: 1rem; }
  .shop-wish[aria-pressed='true'] { color: var(--destructive); }
  .shop-wish[aria-pressed='true'] svg { fill: currentColor; }
  .shop-dots { display: flex; gap: 0.375rem; }
  .shop-dots > span { inline-size: 0.875rem; block-size: 0.875rem; border-radius: 999px; background: var(--dot); box-shadow: inset 0 0 0 1px color-mix(in oklab, var(--foreground) 15%, transparent); }
  .shop-colors { display: flex; flex-wrap: wrap; gap: 0.5rem; border: 0; margin: 0; padding: 0.25rem; }
  .shop-colors legend { margin-block-end: 0.5rem; font-size: 0.875rem; font-weight: 500; }
  .shop-colors legend span { color: var(--muted-foreground); font-weight: 400; }
  .shop-colors label { position: relative; display: inline-flex; inline-size: 1.75rem; block-size: 1.75rem; border-radius: 999px; background: var(--dot); box-shadow: inset 0 0 0 1px color-mix(in oklab, var(--foreground) 15%, transparent); cursor: pointer; }
  .shop-colors input { position: absolute; inset: 0; opacity: 0; margin: 0; cursor: pointer; }
  .shop-colors label:has(:checked) { outline: 2px solid var(--primary); outline-offset: 2px; }
  .shop-colors label:has(:focus-visible) { outline: 2px solid var(--ring); outline-offset: 2px; }
  .shop-colors[data-size='sm'] label { inline-size: 1.25rem; block-size: 1.25rem; }
  .shop-card-actions { display: flex; gap: 0.5rem; }
  .shop-card-actions > .btn:first-child { flex: 1; }
  .shop-cards { display: grid; gap: 2rem 1.5rem; grid-template-columns: repeat(auto-fill, minmax(min(100%, 14rem), 1fr)); }
  .shop-cards[data-layout='list'] { grid-template-columns: 1fr; gap: 1rem; }
  .shop-hcard { display: grid; grid-template-columns: 9rem minmax(0, 1fr); gap: 1.25rem; align-items: start; padding: 1rem; border: 1px solid var(--border); border-radius: var(--radius); }
  .shop-hcard .shop-card-media > img { aspect-ratio: 1; }
  .shop-hcard-body { display: grid; gap: 0.5rem; }
  .shop-hcard-body p { margin: 0; }
  .shop-hcard-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; }
  .shop-hcard-foot { display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem; margin-block-start: 0.25rem; }
  @media (width >= 40rem) { .shop-hcard { grid-template-columns: 12rem minmax(0, 1fr); } }
  .shop-stock { display: inline-flex; align-items: center; gap: 0.375rem; font-size: 0.8125rem; color: var(--muted-foreground); }
  .shop-stock::before { content: ''; inline-size: 0.5rem; block-size: 0.5rem; border-radius: 999px; background: var(--primary); }
  .shop-stock[data-stock='low']::before { background: oklch(0.77 0.16 70); }
  .shop-stock[data-stock='out']::before { background: var(--destructive); }
  .shop-crumbs { font-size: 0.875rem; }
  .shop-pdp { display: grid; gap: 2rem; align-items: start; }
  @media (width >= 56rem) { .shop-pdp { grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr); gap: 3rem; } .shop-pdp-info { position: sticky; inset-block-start: 5.5rem; } }
  .shop-pdp-gallery { display: grid; gap: 0.75rem; }
  .shop-pdp-main { display: block; aspect-ratio: 1; inline-size: 100%; border-radius: var(--radius); background: var(--muted); object-fit: cover; }
  .shop-pdp-carousel .shop-pdp-main { aspect-ratio: 1; cursor: zoom-in; }
  .shop-pdp-carousel > ol > li > a { display: block; overflow: hidden; border-radius: var(--radius); }
  .shop-pdp-carousel [data-carousel] { background: var(--background); }
  .shop-pdp-count { position: absolute; inset-block-end: 0.75rem; inset-inline-end: 0.75rem; z-index: 1; font-variant-numeric: tabular-nums; }
  .shop-pdp-thumbs img { aspect-ratio: 1; }
  .shop-pdp-info { display: grid; gap: 1.5rem; }
  .shop-pdp-title { margin: 0; font-size: 1.875rem; font-weight: 600; letter-spacing: -0.025em; text-wrap: balance; }
  .shop-pdp-buy { display: flex; gap: 0.75rem; }
  .shop-pdp-buy > .btn[data-size='lg'] { flex: 1; }
  .shop-pdp-buy .shop-qty > input { block-size: 2.5rem; }
  .shop-perks { display: grid; gap: 0.75rem; margin: 0; padding: 1rem; list-style: none; border: 1px solid var(--border); border-radius: var(--radius); font-size: 0.875rem; }
  .shop-perks li { display: flex; gap: 0.75rem; align-items: center; }
  .shop-perks svg { inline-size: 1.125rem; block-size: 1.125rem; flex: none; color: var(--muted-foreground); }
  .shop-reviews { display: grid; gap: 2rem; }
  @media (width >= 48rem) { .shop-reviews { grid-template-columns: 16rem minmax(0, 1fr); } }
  .shop-bars { display: grid; gap: 0.5rem; margin: 0; padding: 0; list-style: none; font-size: 0.8125rem; }
  .shop-bars li { display: grid; grid-template-columns: 2rem minmax(0, 1fr) 2.5rem; align-items: center; gap: 0.5rem; }
  .shop-bars li > span:last-child { text-align: end; color: var(--muted-foreground); font-variant-numeric: tabular-nums; }
  .shop-review-list { display: grid; gap: 1.5rem; margin: 0; padding: 0; list-style: none; }
  .shop-review-list li { display: grid; gap: 0.5rem; padding-block-end: 1.5rem; border-block-end: 1px solid var(--border); }
  .shop-review-list p { margin: 0; font-size: 0.875rem; }
  .shop-stars { display: inline-flex; gap: 0.125rem; color: var(--foreground); }
  .shop-stars svg { inline-size: 0.875rem; block-size: 0.875rem; fill: currentColor; }
  .shop-stars svg[data-empty] { fill: none; color: var(--muted-foreground); }
  .shop-section { display: grid; gap: 1.5rem; padding-block-start: 3rem; }
  .shop-qv { inline-size: min(56rem, calc(100vw - 2rem)); max-inline-size: none; }
  .shop-qv-grid { display: grid; gap: 1.5rem; }
  @media (width >= 40rem) { .shop-qv-grid { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); } }
  .shop-qv-grid .shop-pdp-main { aspect-ratio: 4 / 5; }
  .shop-wl-head { display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 1rem; }
  .shop-cmp-wrap { overflow-x: auto; border: 1px solid var(--border); border-radius: var(--radius); }
  .shop-cmp { inline-size: 100%; border-collapse: collapse; font-size: 0.875rem; }
  .shop-cmp th, .shop-cmp td { padding: 0.875rem 1rem; border-block-end: 1px solid var(--border); text-align: start; vertical-align: top; min-inline-size: 13rem; }
  .shop-cmp tr:last-child > * { border-block-end: 0; }
  .shop-cmp tbody th { position: sticky; inset-inline-start: 0; z-index: 1; min-inline-size: 9rem; background: var(--muted); color: var(--muted-foreground); font-weight: 500; }
  .shop-cmp thead th:first-child { position: sticky; inset-inline-start: 0; z-index: 1; background: var(--background); }
  .shop-cmp thead td { position: relative; }
  .shop-cmp-product { display: grid; gap: 0.75rem; }
  .shop-cmp-product img { aspect-ratio: 1; inline-size: 100%; max-inline-size: 10rem; border-radius: var(--radius); background: var(--muted); object-fit: cover; }
  html.dark .shop-cmp-product img { filter: brightness(0.5) grayscale(1); }
  html.dark .shop-tray img { filter: brightness(0.5) grayscale(1); }
  .shop-cmp-product h3 { margin: 0; font-size: 0.9375rem; font-weight: 500; }
  .shop-cmp-remove { position: absolute; inset-block-start: 0.5rem; inset-inline-end: 0.5rem; }
  .shop-cmp[data-highlight] tr[data-diff] > td { background: color-mix(in oklab, var(--primary) 7%, transparent); }
  .shop-cmp[data-highlight] tr:not([data-diff]):not(:first-child) { opacity: 0.55; }
  .shop-cmp svg.shop-yes { inline-size: 1rem; block-size: 1rem; color: var(--primary); }
  .shop-cmp svg.shop-no { inline-size: 1rem; block-size: 1rem; color: var(--muted-foreground); }
  .shop-cmp-check { display: inline-flex; align-items: center; gap: 0.5rem; font-size: 0.8125rem; }
  .shop-tray { position: fixed; inset-block-end: 1rem; inset-inline: 1rem; z-index: 20; display: flex; flex-wrap: wrap; align-items: center; gap: 1rem; max-inline-size: 48rem; margin-inline: auto; padding: 0.75rem 1rem; border: 1px solid var(--border); border-radius: calc(var(--radius) + 4px); background: var(--popover); color: var(--popover-foreground); box-shadow: 0 10px 30px -10px rgb(0 0 0 / 0.3); }
  .shop-tray-slots { display: flex; gap: 0.5rem; flex: 1; }
  .shop-tray-slots > li { position: relative; display: flex; align-items: center; justify-content: center; inline-size: 3rem; block-size: 3rem; border: 1px dashed var(--border); border-radius: var(--radius); color: var(--muted-foreground); font-size: 0.75rem; }
  .shop-tray-slots > li img { inline-size: 100%; block-size: 100%; border-radius: inherit; object-fit: cover; }
  .shop-tray-slots { list-style: none; margin: 0; padding: 0; }
  .shop-tray p { margin: 0; font-size: 0.875rem; }
  .shop-search-trigger { display: flex; align-items: center; gap: 0.5rem; inline-size: 100%; max-inline-size: 22rem; margin-inline-start: auto; padding-inline: 0.75rem; block-size: 2.25rem; border: 1px solid var(--input); border-radius: var(--radius); background: transparent; color: var(--muted-foreground); font: inherit; font-size: 0.875rem; cursor: pointer; }
  .shop-search-trigger:hover { background: var(--accent); }
  .shop-search-trigger svg { inline-size: 1rem; block-size: 1rem; }
  .shop-search-trigger kbd { margin-inline-start: auto; }
  .shop-search .command { inline-size: min(40rem, calc(100vw - 2rem)); }
  .shop-search [role='menuitem'] img { inline-size: 2.5rem; block-size: 2.5rem; border-radius: calc(var(--radius) - 2px); object-fit: cover; background: var(--muted); }
  .shop-search [role='menuitem'] .shop-hit { display: grid; flex: 1; min-inline-size: 0; }
  .shop-search [role='menuitem'] .shop-hit small { color: var(--muted-foreground); font-size: 0.75rem; }
  .shop-search [role='menuitem'] .shop-hit-price { font-variant-numeric: tabular-nums; font-size: 0.8125rem; }
  .shop-search-foot { display: flex; gap: 1rem; padding: 0.625rem 0.75rem; border-block-start: 1px solid var(--border); font-size: 0.75rem; color: var(--muted-foreground); }
  .shop-search-foot span { display: inline-flex; align-items: center; gap: 0.375rem; }
  .shop-results { display: grid; gap: 2rem; align-items: start; }
  @media (width >= 56rem) { .shop-results { grid-template-columns: 15rem minmax(0, 1fr); } }
  .shop-filters-panel { display: grid; gap: 0.25rem; }
  .shop-filters-panel .accordion summary { font-size: 0.875rem; }
  .shop-check-list { display: grid; gap: 0.625rem; padding-block-end: 0.5rem; }
  .shop-check-list label { display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; }
  .shop-check-list label span { margin-inline-start: auto; color: var(--muted-foreground); font-size: 0.75rem; }
  .shop-toolbar { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 0.75rem; }
  .shop-toolbar .select { inline-size: auto; }
  .shop-chip-row { display: flex; flex-wrap: wrap; gap: 0.5rem; }
  .shop-chip-row .badge { gap: 0.25rem; }
  .shop-chip-row .badge svg { inline-size: 0.75rem; block-size: 0.75rem; }
  .shop-range-out { display: flex; justify-content: space-between; font-size: 0.8125rem; color: var(--muted-foreground); font-variant-numeric: tabular-nums; }
  .shop-drawer-lines { overflow-y: auto; max-block-size: 45vh; padding-inline: 1rem; }
  .shop-drawer-foot { display: grid; gap: 0.75rem; }
"""


def stars(r):
    full = int(round(r))
    return '<span class="shop-stars" aria-hidden="true">' + "".join(si("star") if i < full else si("star").replace("<svg ", "<svg data-empty ") for i in range(5)) + "</span>"


def rating(p):
    return f'<p class="shop-rating">{si("star")}{p["rating"]} <span>({p["reviews"]})</span></p>'


def price(p, size=None):
    sz = f' data-size="{size}"' if size else ""
    was = f'<s>{money(p["was"])}</s><span class="sr-only">Was {money(p["was"])}</span>' if p["was"] else ""
    return f'<p class="shop-price"{sz}><strong>{money(p["price"])}</strong>{was}</p>'


def badge(p):
    if not p["badge"]:
        return ""
    v = "destructive" if p["badge"] == "Sale" else "secondary" if p["badge"] == "Bestseller" else ""
    return f'<span class="badge shop-card-badge"{f" data-variant={chr(34)}{v}{chr(34)}" if v else ""}>{p["badge"]}</span>'


def dots(p):
    return '<div class="shop-dots" aria-label="' + f'{len(p["colors"])} colors">' + "".join(f'<span style="--dot: {c}" title="{n}"></span>' for n, c in p["colors"]) + "</div>"


def wish_btn(p, pressed=False, size="icon-sm"):
    return f'<button type="button" class="btn shop-wish" data-variant="outline" data-size="{size}" aria-pressed="{"true" if pressed else "false"}" aria-label="Save {p["name"]} to wishlist" data-wish>{si("heart")}</button>'


def card(p, quick=None, compare=False, wished=False):
    """Grid product card. quick: id of a quick-view dialog to open from the card."""
    q = (f'<button type="button" class="btn" data-variant="outline" data-size="icon-sm" aria-label="Quick view {p["name"]}" commandfor="{quick}" command="show-modal">{si("eye")}</button>' if quick else "")
    cmp = (f'<label class="shop-cmp-check"><input type="checkbox" class="input" data-compare="{p["id"]}"> Compare</label>' if compare else "")
    return f"""<article class="shop-card">
  <div class="shop-card-media">
    <img src="{PH}" alt="">
    {badge(p)}
    <div class="shop-card-tools">{wish_btn(p, wished)}{q}</div>
    <button type="button" class="btn shop-card-quick" data-size="sm">{si("plus")}Quick add</button>
  </div>
  <div class="shop-card-body">
    <p class="shop-card-cat">{p["cat"]}</p>
    <h3 class="shop-card-name"><a href="#">{p["name"]}</a></h3>
    {rating(p)}
    <div class="cluster" data-justify="between">{price(p)}{dots(p)}</div>
    {cmp}
  </div>
</article>"""


WISH_JS = """
document.addEventListener('click', (e) => {
  const b = e.target.closest('[data-wish]');
  if (!b) return;
  const on = b.getAttribute('aria-pressed') !== 'true';
  b.setAttribute('aria-pressed', String(on));
  document.querySelectorAll('[data-wish-count]').forEach((el) => {
    const n = Math.max(0, (parseInt(el.textContent, 10) || 0) + (on ? 1 : -1));
    el.textContent = n;
    el.dataset.count = n;
  });
});
"""

CAT_CSS = SHOP_CSS + CATALOG_CSS


def wish_header(n):
    return store_header(2, cart_button=None).replace(
        f'<a href="#" class="btn" data-variant="ghost" data-size="icon" aria-label="Wishlist">{si("heart")}</a>',
        f'<a href="#" class="btn shop-cart-btn" data-variant="ghost" data-size="icon" aria-label="Wishlist">{si("heart")}<span class="shop-count" data-wish-count data-count="{n}">{n}</span></a>')


# ================================================================== product cards
add("product-card-01", "Product Card 01", "Product cards with badges, rating, colors, a wishlist toggle and quick add.", "product-card", f"""
<main class="wrapper shop-page">
  <div class="stack" data-gap="6">
    <div class="cluster" data-justify="between" data-gap="4">
      <h1 class="shop-h1">Best sellers</h1>
      <a href="#" class="btn" data-variant="link" data-size="sm">Shop all{si("arrow-right")}</a>
    </div>
    <div class="shop-cards">
      {"".join(card(p, wished=(i == 1)) for i, p in enumerate(ITEMS[:8]))}
    </div>
  </div>
</main>
""", CAT_CSS, scripts=script(WISH_JS))


def hcard(p, stock=("in", "In stock")):
    return f"""<article class="shop-hcard shop-card">
  <div class="shop-card-media"><img src="{PH}" alt="">{badge(p)}</div>
  <div class="shop-hcard-body">
    <div class="shop-hcard-top">
      <div class="stack" data-gap="1">
        <p class="shop-card-cat">{p["cat"]}</p>
        <h3 class="shop-card-name"><a href="#">{p["name"]}</a></h3>
        {rating(p)}
      </div>
      {price(p)}
    </div>
    <p class="shop-lead">{p["desc"]}</p>
    <div class="cluster" data-gap="3">{dots(p)}<span class="shop-stock" data-stock="{stock[0]}">{stock[1]}</span></div>
    <div class="shop-hcard-foot shop-card-actions">
      <button type="button" class="btn" data-size="sm">{si("shopping-bag")}Add to cart</button>
      {wish_btn(p)}
      <button type="button" class="btn" data-variant="outline" data-size="icon-sm" aria-label="Compare {p["name"]}">{si("arrow-right-left")}</button>
    </div>
  </div>
</article>"""


STOCKS = [("in", "In stock"), ("low", "Only 3 left"), ("in", "In stock"), ("out", "Out of stock")]
add("product-card-02", "Product Card 02", "Horizontal product cards with description, stock and actions.", "product-card", f"""
<main class="wrapper shop-page" data-size="md">
  <div class="stack" data-gap="6">
    <h1 class="shop-h1">Home &amp; kitchen</h1>
    <div class="shop-cards" data-layout="list">
      {"".join(hcard(p, STOCKS[i]) for i, p in enumerate([ITEMS[2], ITEMS[3], ITEMS[6], ITEMS[5]]))}
    </div>
  </div>
</main>
""", CAT_CSS + "\n  .shop-hcard-foot .btn:first-child { flex: none; }", scripts=script(WISH_JS))


def swatch_card(p, i):
    colors = "".join(f'<label style="--dot: {c}" title="{n}"><input type="radio" name="pc3-{i}" value="{n}" aria-label="{n}"{" checked" if j == 0 else ""}></label>' for j, (n, c) in enumerate(p["colors"]))
    return f"""<article class="shop-card" data-swatch-card>
  <div class="shop-card-media"><img src="{PH}" alt="">{badge(p)}<div class="shop-card-tools">{wish_btn(p)}</div></div>
  <div class="shop-card-body">
    <div class="shop-hcard-top"><h3 class="shop-card-name"><a href="#">{p["name"]}</a></h3>{price(p)}</div>
    <p class="shop-line-meta" data-color-label>{p["colors"][0][0]}</p>
    <fieldset class="shop-colors" data-size="sm"><legend class="sr-only">Color</legend>{colors}</fieldset>
  </div>
  <div class="shop-card-actions"><button type="button" class="btn" data-variant="outline">{si("shopping-bag")}Add to cart</button></div>
</article>"""


SWATCH_JS = """
document.querySelectorAll('[data-swatch-card]').forEach((card) => {
  card.addEventListener('change', (e) => {
    if (e.target.matches('input[type=radio]')) card.querySelector('[data-color-label]').textContent = e.target.value;
  });
});
"""
add("product-card-03", "Product Card 03", "Product cards with color swatches and a full-width add to cart.", "product-card", f"""
<main class="wrapper shop-page">
  <div class="stack" data-gap="6">
    <div class="stack" data-gap="1">
      <h1 class="shop-h1">Pick your color</h1>
      <p class="shop-lead">Every piece comes in seasonal colors.</p>
    </div>
    <div class="shop-cards">
      {"".join(swatch_card(p, i) for i, p in enumerate([ITEMS[0], ITEMS[1], ITEMS[3], ITEMS[4]]))}
    </div>
  </div>
</main>
""", CAT_CSS, scripts=script(WISH_JS + SWATCH_JS))


# ================================================================== product details
def gallery(prefix, n=4, name="Merino Crew Sweater"):
    # Carousel (drag, swipe, arrows), thumbnails kept in sync, and a lightbox on click (js/carousel.js).
    slides = "".join(
        f'<li aria-roledescription="slide" aria-label="{i + 1} of {n}"><a href="{PH}" data-lightbox="{prefix}" data-caption="{name}, photo {i + 1} of {n}">'
        f'<img class="shop-shot shop-pdp-main" src="{PH}" alt="{name}, photo {i + 1}"{f" data-shot={chr(34)}{i + 1}{chr(34)}" if i else ""}></a></li>'
        for i in range(n))
    thumbs = "".join(
        f'<li aria-roledescription="slide" aria-label="{i + 1} of {n}"><button type="button" aria-label="Show photo {i + 1}">'
        f'<img class="shop-shot" src="{PH}" alt=""{f" data-shot={chr(34)}{i + 1}{chr(34)}" if i else ""}></button></li>'
        for i in range(n))
    arrow = lambda d, ic_: f'<button type="button" class="btn rounded-full" data-variant="outline" data-size="icon-sm" data-carousel="{d}" aria-label="{"Previous" if d == "prev" else "Next"} photo">{si(ic_)}</button>'
    return f"""<div class="shop-pdp-gallery">
  <section class="carousel shop-pdp-carousel" id="{prefix}-gallery" data-loop aria-roledescription="carousel" aria-label="{name} photos">
    <ol>{slides}</ol>
    {arrow("prev", "chevron-left")}{arrow("next", "chevron-right")}
    <span class="badge shop-pdp-count" data-variant="secondary" data-carousel-counter>1 / {n}</span>
  </section>
  <section class="carousel shop-pdp-thumbs" data-carousel-for="{prefix}-gallery" aria-label="Thumbnails" style="--per-view: {n}; --carousel-gap: 0.75rem">
    <ol>{thumbs}</ol>
  </section>
</div>"""


def color_picker(p, prefix):
    return (f'<fieldset class="shop-colors" data-color-picker><legend>Color: <span data-color-label>{p["colors"][0][0]}</span></legend>'
            + "".join(f'<label style="--dot: {c}" title="{n}"><input type="radio" name="{prefix}-color" value="{n}" aria-label="{n}"{" checked" if j == 0 else ""}></label>' for j, (n, c) in enumerate(p["colors"]))
            + "</fieldset>")


def size_picker(prefix):
    return (f'<fieldset class="shop-swatches"><legend>Size</legend>'
            + "".join(f'<label><input type="radio" name="{prefix}-size" value="{s_}"{" checked" if s_ == "M" else ""}{" disabled" if s_ == "XL" else ""}>{s_}</label>' for s_ in ["XS", "S", "M", "L", "XL"])
            + "</fieldset>")


PICKER_JS = """
document.querySelectorAll('[data-color-picker]').forEach((f) => {
  f.addEventListener('change', (e) => { f.querySelector('[data-color-label]').textContent = e.target.value; });
});
"""

P = ITEMS[1]
REVIEWS = [
    ("Hannah K.", 5, "Oct 30, 2026", "Soft and warm without being bulky. True to size, I'm usually a medium."),
    ("Marcus L.", 5, "Oct 21, 2026", "Second one I've bought. Still looks new after a winter of wear."),
    ("Priya S.", 4, "Oct 4, 2026", "Lovely color. Slightly longer in the sleeves than I expected."),
]
bars = "".join(f'<li><span>{n} ★</span><div class="progress" role="progressbar" aria-label="{n} star reviews" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{v}"><span style="width: {v}%"></span></div><span>{v}%</span></li>' for n, v in [(5, 82), (4, 12), (3, 4), (2, 1), (1, 1)])
reviews = "".join(f'<li><div class="cluster" data-justify="between"><strong class="shop-line-name">{a}</strong><time class="shop-line-meta">{d}</time></div>{stars(r)}<p>{t}</p></li>' for a, r, d, t in REVIEWS)
crumb_sep = f'<li aria-hidden="true">{si("chevron-right").replace("<svg ", "<svg data-rtl-flip ")}</li>'

add("product-01", "Product 01", "A product page: gallery, variants, quantity, add to cart, details and reviews.", "product", f"""
{store_header(3)}
<main class="wrapper shop-page" data-cart>
  <div class="stack" data-gap="6">
    <nav class="breadcrumb shop-crumbs" aria-label="Breadcrumb"><ol><li><a href="#">Home</a></li>{crumb_sep}<li><a href="#">Apparel</a></li>{crumb_sep}<li><span aria-current="page">{P["name"]}</span></li></ol></nav>
    <div class="shop-pdp">
      {gallery("p1")}
      <div class="shop-pdp-info">
        <div class="stack" data-gap="3">
          <div class="cluster" data-gap="2"><span class="badge" data-variant="destructive">Sale</span><span class="shop-stock" data-stock="low">Only 3 left in M</span></div>
          <h1 class="shop-pdp-title">{P["name"]}</h1>
          <div class="cluster" data-gap="2">{stars(P["rating"])}<a href="#p1-reviews" class="shop-line-meta">{P["rating"]} · {P["reviews"]} reviews</a></div>
          {price(P, "lg")}
          <p class="shop-lead">{P["desc"]} A clean crew neck and ribbed trims make it the sweater you reach for every day.</p>
        </div>
        {color_picker(P, "p1")}
        {size_picker("p1")}
        <div class="shop-pdp-buy">
          {qty("p1", 1)}
          <button type="button" class="btn" data-size="lg">{si("shopping-bag")}Add to cart</button>
          {wish_btn(P, size="icon-lg")}
        </div>
        <ul class="shop-perks">
          <li>{si("truck")}<span>Free shipping on orders over $150</span></li>
          <li>{si("rotate-ccw")}<span>Free returns within 30 days</span></li>
          <li>{si("shield-check")}<span>2-year quality guarantee</span></li>
        </ul>
        <div class="accordion">
          <details open>
            <summary>Details</summary>
            <section><p class="shop-lead">100% extra-fine merino wool, 16.5 micron. Relaxed fit, model is 185 cm and wears M.</p></section>
          </details>
          <details>
            <summary>Care</summary>
            <section><p class="shop-lead">Machine wash cold on a wool cycle. Dry flat. Do not tumble dry.</p></section>
          </details>
          <details>
            <summary>Shipping and returns</summary>
            <section><p class="shop-lead">Ships in 1–2 business days. Return unworn items within 30 days for a full refund.</p></section>
          </details>
        </div>
      </div>
    </div>
    <section class="shop-section" id="p1-reviews" aria-labelledby="p1-reviews-title">
      <h2 class="shop-h2" id="p1-reviews-title">Reviews</h2>
      <div class="shop-reviews">
        <div class="stack" data-gap="4">
          <div class="stack" data-gap="1"><p class="shop-h1">{P["rating"]}</p>{stars(P["rating"])}<p class="shop-line-meta">Based on {P["reviews"]} reviews</p></div>
          <ul class="shop-bars">{bars}</ul>
          <button type="button" class="btn" data-variant="outline">Write a review</button>
        </div>
        <ul class="shop-review-list">{reviews}</ul>
      </div>
    </section>
    <section class="shop-section" aria-labelledby="p1-more">
      <h2 class="shop-h2" id="p1-more">You may also like</h2>
      <div class="shop-cards">{"".join(card(p) for p in [ITEMS[7], ITEMS[0], ITEMS[4], ITEMS[3]])}</div>
    </section>
  </div>
</main>
""", CAT_CSS + "\n  .shop-bars .progress { block-size: 0.5rem; }", scripts=script(QTY_JS + PICKER_JS + WISH_JS))

QV = ITEMS[0]
add("product-02", "Product 02", "Product grid with a quick view dialog: images, color, quantity and add to cart.", "product", f"""
{store_header(3)}
<main class="wrapper shop-page">
  <div class="stack" data-gap="6">
    <div class="stack" data-gap="1">
      <h1 class="shop-h1">New in</h1>
      <p class="shop-lead">Use the eye button on a card for a quick view.</p>
    </div>
    <div class="shop-cards">{"".join(card(p, quick="p2-qv") for p in ITEMS[:4])}</div>
  </div>
  <dialog id="p2-qv" class="dialog" closedby="any" aria-labelledby="p2-qv-title">
    <div class="shop-qv">
      <section>
        <div class="shop-qv-grid">
          <img class="shop-pdp-main" src="{PH}" alt="">
          <div class="stack" data-gap="5">
            <div class="stack" data-gap="2">
              <p class="shop-card-cat">{QV["cat"]}</p>
              <h2 class="shop-pdp-title" id="p2-qv-title">{QV["name"]}</h2>
              {rating(QV)}
              {price(QV, "lg")}
              <p class="shop-lead">{QV["desc"]}</p>
            </div>
            {color_picker(QV, "p2")}
            <div class="shop-pdp-buy">
              {qty("p2", 1)}
              <button type="button" class="btn" data-size="lg" commandfor="p2-qv" command="close">{si("shopping-bag")}Add to cart</button>
            </div>
            <a href="#" class="btn" data-variant="link">View full details{si("arrow-right")}</a>
          </div>
        </div>
      </section>
      <button type="button" aria-label="Close" commandfor="p2-qv" command="close">{si("x")}</button>
    </div>
  </dialog>
</main>
""", CAT_CSS, scripts=script(QTY_JS + PICKER_JS + WISH_JS))


# ================================================================== wishlist
def wish_card(p, i):
    out = i == 2
    return f"""<article class="shop-card" data-wish-item>
  <div class="shop-card-media"><img src="{PH}" alt="">{badge(p)}
    <div class="shop-card-tools"><button type="button" class="btn" data-variant="outline" data-size="icon-sm" aria-label="Remove {p["name"]} from wishlist" data-wish-remove>{si("x")}</button></div>
  </div>
  <div class="shop-card-body">
    <h3 class="shop-card-name"><a href="#">{p["name"]}</a></h3>
    <p class="shop-line-meta">{p["colors"][0][0]} · Size M</p>
    <div class="cluster" data-justify="between">{price(p)}<span class="shop-stock" data-stock="{"out" if out else "in"}">{"Out of stock" if out else "In stock"}</span></div>
  </div>
  <div class="shop-card-actions">{f'<button type="button" class="btn" data-variant="outline">{si("bell")}Notify me</button>' if out else f'<button type="button" class="btn" data-wish-move>{si("shopping-bag")}Move to cart</button>'}</div>
</article>"""


WISHLIST_JS = """
document.querySelectorAll('[data-wishlist]').forEach((list) => {
  const sync = () => {
    const n = list.querySelectorAll('[data-wish-item]').length;
    document.querySelectorAll('[data-wish-count]').forEach((el) => { el.textContent = n; el.dataset.count = n; });
    document.querySelectorAll('[data-wish-label]').forEach((el) => { el.textContent = n + (n === 1 ? ' item' : ' items'); });
    list.querySelectorAll('[data-wish-filled]').forEach((el) => { el.hidden = !n; });
    list.querySelectorAll('[data-wish-empty]').forEach((el) => { el.hidden = !!n; });
  };
  list.addEventListener('click', (e) => {
    const b = e.target.closest('[data-wish-remove], [data-wish-move]');
    if (!b) return;
    if (b.matches('[data-wish-move]')) document.querySelectorAll('[data-cart-count]').forEach((el) => { el.textContent = (parseInt(el.textContent, 10) || 0) + 1; });
    b.closest('[data-wish-item]').remove();
    sync();
  });
});
"""

WISH_EMPTY = f"""<section class="empty" data-wish-empty hidden>
  <header>
    <figure>{si("heart")}</figure>
    <h3>Your wishlist is empty</h3>
    <p>Tap the heart on any product to save it for later.</p>
  </header>
  <footer><a href="#" class="btn">Discover products</a></footer>
</section>"""

wl_items = [ITEMS[1], ITEMS[6], ITEMS[3], ITEMS[4], ITEMS[0]]
add("wishlist-01", "Wishlist 01", "A wishlist grid in the account area with move to cart, remove and an empty state.", "wishlist", account("Wishlist", f"""
<div class="stack" data-gap="6" data-wishlist>
  <div class="shop-wl-head">
    <div class="stack" data-gap="1">
      <h1 class="shop-h1">Wishlist</h1>
      <p class="shop-lead" data-wish-label>{len(wl_items)} items</p>
    </div>
    <div class="cluster" data-gap="2" data-wish-filled>
      <button type="button" class="btn" data-variant="outline">{si("share-2")}Share</button>
      <button type="button" class="btn">{si("shopping-bag")}Add all to cart</button>
    </div>
  </div>
  <div class="shop-cards" data-wish-filled>{"".join(wish_card(p, i) for i, p in enumerate(wl_items))}</div>
  {WISH_EMPTY}
</div>
"""), CAT_CSS + """
  .shop-profile .avatar { inline-size: 2.25rem; block-size: 2.25rem; }
  .shop-wl-head .cluster .btn { flex: none; }""", scripts=script(WISHLIST_JS))

wl_rows = "\n".join(f"""<tr data-wish-item>
  <td><div class="shop-wl-product"><img class="shop-thumb" data-size="sm" src="{PH}" alt=""><div><a href="#" class="shop-line-name shop-link">{p["name"]}</a><p class="shop-line-meta">{p["colors"][0][0]}</p></div></div></td>
  <td>{price(p)}</td>
  <td><span class="shop-stock" data-stock="{st[0]}">{st[1]}</span></td>
  <td class="shop-num"><div class="shop-wl-actions">{f'<button type="button" class="btn" data-size="sm" data-wish-move>Add to cart</button>' if st[0] != "out" else '<button type="button" class="btn" data-variant="outline" data-size="sm">Notify me</button>'}<button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Remove {p["name"]}" data-wish-remove>{si("trash-2")}</button></div></td>
</tr>""" for p, st in zip([ITEMS[2], ITEMS[5], ITEMS[7], ITEMS[6]], [("in", "In stock"), ("low", "Only 2 left"), ("out", "Out of stock"), ("in", "In stock")]))

add("wishlist-02", "Wishlist 02", "A compact wishlist table with price, stock and actions.", "wishlist", f"""
{wish_header(4)}
<main class="wrapper shop-page" data-size="md">
  <div class="stack" data-gap="6" data-wishlist>
    <div class="shop-wl-head">
      <div class="stack" data-gap="1">
        <h1 class="shop-h1">Saved for later</h1>
        <p class="shop-lead" data-wish-label>4 items</p>
      </div>
      <button type="button" class="btn" data-variant="outline" data-wish-filled>{si("share-2")}Share list</button>
    </div>
    <div class="shop-table-wrap" data-wish-filled>
      <table class="table">
        <thead><tr><th>Product</th><th>Price</th><th>Availability</th><th class="shop-num"><span class="sr-only">Actions</span></th></tr></thead>
        <tbody>
          {wl_rows}
        </tbody>
      </table>
    </div>
    {WISH_EMPTY}
  </div>
</main>
""", CAT_CSS + """
  .shop-num { text-align: end; }
  .shop-table-wrap { overflow-x: auto; }
  .shop-link { color: inherit; text-decoration: none; }
  .shop-link:hover { text-decoration: underline; text-underline-offset: 4px; }
  .shop-wl-product { display: flex; align-items: center; gap: 0.75rem; min-inline-size: 14rem; }
  .shop-wl-product p { margin: 0; }
  .shop-wl-actions { display: inline-flex; align-items: center; gap: 0.25rem; }
  .shop-table-wrap .shop-price { white-space: nowrap; }""", scripts=script(WISHLIST_JS))


# ================================================================== compare
CMP = [ITEMS[6], {**ITEMS[6], "id": "lamp2", "name": "Dome Table Lamp", "price": 98.00, "rating": 4.5, "reviews": 61, "badge": None}, {**ITEMS[6], "id": "lamp3", "name": "Globe Floor Lamp", "price": 189.00, "rating": 4.8, "reviews": 22, "badge": "New"}]
CMP_ROWS = [
    ("Rating", [f"{c['rating']} ({c['reviews']})" for c in CMP]),
    ("Material", ["Brushed brass, steel", "Glass, steel", "Opal glass, brass"]),
    ("Dimensions", ["H 45 × W 30 cm", "H 38 × W 25 cm", "H 150 × W 35 cm"]),
    ("Light", ["LED, 2700 K", "LED, 2700 K", "E27 bulb (included)"]),
    ("Dimmable", [True, True, False]),
    ("USB charging", [True, False, False]),
    ("Warranty", ["2 years", "2 years", "2 years"]),
    ("Availability", ["In stock", "In stock", "Ships in 2 weeks"]),
]


def cmp_cell(v):
    if v is True:
        return f'<td>{si("check", cls="shop-yes")}<span class="sr-only">Yes</span></td>'
    if v is False:
        return f'<td>{si("minus", cls="shop-no")}<span class="sr-only">No</span></td>'
    return f"<td>{v}</td>"


cmp_head = "".join(f"""<td data-col="{i}">
  <button type="button" class="btn shop-cmp-remove" data-variant="ghost" data-size="icon-xs" aria-label="Remove {c["name"]} from comparison" data-cmp-remove="{i}">{si("x")}</button>
  <div class="shop-cmp-product"><img src="{PH}" alt=""><h3>{c["name"]}</h3>{price(c)}<button type="button" class="btn" data-size="sm">{si("shopping-bag")}Add to cart</button></div>
</td>""" for i, c in enumerate(CMP))
cmp_rows = "\n".join(
    f'<tr{" data-diff" if len(set(map(str, vals))) > 1 else ""}><th scope="row">{label}</th>' + "".join(cmp_cell(v).replace("<td>", f'<td data-col="{i}">', 1) for i, v in enumerate(vals)) + "</tr>"
    for label, vals in CMP_ROWS)

COMPARE_JS = """
document.querySelectorAll('[data-compare-table]').forEach((t) => {
  const toggle = document.getElementById(t.dataset.compareTable);
  toggle?.addEventListener('change', () => t.toggleAttribute('data-highlight', toggle.checked));
  const diff = () => t.querySelectorAll('tbody tr').forEach((tr) => {
    const vals = [...tr.querySelectorAll('td')].map((td) => td.textContent.trim());
    tr.toggleAttribute('data-diff', new Set(vals).size > 1);
  });
  t.addEventListener('click', (e) => {
    const b = e.target.closest('[data-cmp-remove]');
    if (!b) return;
    t.querySelectorAll(`[data-col="${b.dataset.cmpRemove}"]`).forEach((c) => c.remove());
    const left = t.querySelectorAll('thead td').length;
    document.querySelectorAll('[data-cmp-count]').forEach((el) => { el.textContent = left + (left === 1 ? ' product' : ' products'); });
    diff();
  });
});
"""

add("compare-01", "Compare 01", "A product comparison table with sticky labels, remove and highlight differences.", "compare", f"""
{store_header(3)}
<main class="wrapper shop-page">
  <div class="stack" data-gap="6">
    <div class="shop-wl-head">
      <div class="stack" data-gap="1">
        <h1 class="shop-h1">Compare lamps</h1>
        <p class="shop-lead" data-cmp-count>3 products</p>
      </div>
      <div class="cluster" data-gap="3">
        <label class="shop-cmp-check" for="cmp1-diff"><input type="checkbox" role="switch" class="input" id="cmp1-diff"> Highlight differences</label>
        <button type="button" class="btn" data-variant="outline" data-size="sm">{si("plus")}Add product</button>
      </div>
    </div>
    <div class="shop-cmp-wrap">
      <table class="shop-cmp" data-compare-table="cmp1-diff">
        <thead><tr><th scope="col"><span class="sr-only">Feature</span></th>{cmp_head}</tr></thead>
        <tbody>
          {cmp_rows}
        </tbody>
      </table>
    </div>
  </div>
</main>
""", CAT_CSS, scripts=script(COMPARE_JS))

TRAY_JS = """
document.querySelectorAll('[data-compare-tray]').forEach((tray) => {
  const MAX = 3;
  const slots = tray.querySelectorAll('[data-slot]');
  const boxes = () => [...document.querySelectorAll('[data-compare]')];
  const sync = () => {
    const on = boxes().filter((b) => b.checked);
    slots.forEach((s, i) => {
      const b = on[i];
      s.innerHTML = b ? `<img src="${b.closest('.shop-card').querySelector('img').getAttribute('src')}" alt="${b.closest('.shop-card').querySelector('.shop-card-name').textContent.trim()}">` : String(i + 1);
    });
    boxes().forEach((b) => { b.disabled = !b.checked && on.length >= MAX; });
    tray.hidden = !on.length;
    tray.querySelector('[data-tray-count]').textContent = `${on.length} of ${MAX} selected`;
    tray.querySelector('[data-tray-go]').disabled = on.length < 2;
  };
  document.addEventListener('change', (e) => { if (e.target.matches('[data-compare]')) sync(); });
  tray.querySelector('[data-tray-clear]').addEventListener('click', () => { boxes().forEach((b) => { b.checked = false; }); sync(); });
  sync();
});
"""
add("compare-02", "Compare 02", "Compare checkboxes on product cards with a floating compare tray.", "compare", f"""
{store_header(3)}
<main class="wrapper shop-page shop-tray-space">
  <div class="stack" data-gap="6">
    <div class="stack" data-gap="1">
      <h1 class="shop-h1">Lighting</h1>
      <p class="shop-lead">Select up to three products to compare.</p>
    </div>
    <div class="shop-cards">{"".join(card(p, compare=True) for p in [ITEMS[6], ITEMS[0], ITEMS[2], ITEMS[3]])}</div>
  </div>
</main>
<div class="shop-tray" role="region" aria-label="Compare" data-compare-tray hidden>
  <ul class="shop-tray-slots">{"".join(f'<li data-slot>{i + 1}</li>' for i in range(3))}</ul>
  <p data-tray-count>0 of 3 selected</p>
  <div class="cluster" data-gap="2">
    <button type="button" class="btn" data-variant="ghost" data-size="sm" data-tray-clear>Clear</button>
    <button type="button" class="btn" data-size="sm" data-tray-go disabled>{si("arrow-right-left")}Compare</button>
  </div>
</div>
""", CAT_CSS + "\n  .shop-tray-space { padding-block-end: 8rem; }", scripts=script(TRAY_JS + WISH_JS))


# ================================================================== search
recent = ["merino sweater", "pour over", "linen"]
hits = "".join(f"""<div role="menuitem" data-filter="{p["name"]}" data-keywords="{p["cat"].lower()} {" ".join(n.lower() for n, _ in p["colors"])}">
  <img src="{PH}" alt="">
  <span class="shop-hit"><span>{p["name"]}</span><small>{p["cat"]}</small></span>
  <span class="shop-hit-price">{money(p["price"])}</span>
</div>""" for p in ITEMS)
search_dialog = f"""<dialog id="s1-search" class="command-dialog shop-search" closedby="any" aria-label="Search products">
  <div class="command">
    <header>
      {si("search")}
      <input type="text" id="s1-input" placeholder="Search products, categories..." autocomplete="off" spellcheck="false" aria-autocomplete="list" role="combobox" aria-expanded="true" aria-controls="s1-menu">
    </header>
    <div role="menu" id="s1-menu" aria-orientation="vertical" data-empty="No products found.">
      <div role="group" aria-labelledby="s1-recent">
        <span role="heading" id="s1-recent">Recent searches</span>
        {"".join(f'<div role="menuitem" data-filter="{r}">{si("clock")}<span>{r}</span></div>' for r in recent)}
      </div>
      <div role="group" aria-labelledby="s1-popular">
        <span role="heading" id="s1-popular">Popular categories</span>
        {"".join(f'<div role="menuitem" data-filter="{c}">{si("trending-up")}<span>{c}</span></div>' for c in ["Apparel", "Kitchen", "Home"])}
      </div>
      <hr role="separator">
      <div role="group" aria-labelledby="s1-products">
        <span role="heading" id="s1-products">Products</span>
        {hits}
      </div>
    </div>
    <footer class="shop-search-foot"><span><kbd class="kbd">↑</kbd><kbd class="kbd">↓</kbd> to navigate</span><span><kbd class="kbd">↵</kbd> to select</span><span><kbd class="kbd">Esc</kbd> to close</span></footer>
  </div>
</dialog>"""

SEARCH_JS = """
document.addEventListener('keydown', (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault();
    const d = document.getElementById('s1-search');
    if (d.open) d.close(); else d.showModal();
  }
});
"""
search_trigger = f'<button type="button" class="shop-search-trigger" commandfor="s1-search" command="show-modal">{si("search")}<span>Search products...</span><kbd class="kbd">⌘K</kbd></button>'
s1_header = store_header(3).replace(
    store_header(3)[store_header(3).index('<div class="input-group shop-header-search">'):store_header(3).index('<div class="shop-header-actions">')],
    search_trigger + "\n    ")
add("search-01", "Search 01", "A product search dialog (⌘K) with recent searches, categories and product results.", "search", f"""
{s1_header}
<main class="wrapper shop-page">
  <div class="stack" data-gap="6">
    <div class="stack" data-gap="1">
      <h1 class="shop-h1">Shop</h1>
      <p class="shop-lead">Press <kbd class="kbd">⌘K</kbd> or use the search box in the header.</p>
    </div>
    <div class="shop-cards">{"".join(card(p) for p in ITEMS[:4])}</div>
  </div>
</main>
{search_dialog}
""", CAT_CSS + "\n  @media (width < 48rem) { .shop-search-trigger { max-inline-size: none; } .shop-search-trigger kbd, .shop-search-trigger span { display: none; } .shop-search-trigger { inline-size: auto; border: 0; } }", scripts=script(SEARCH_JS + WISH_JS))


def checks(name, opts):
    return '<div class="shop-check-list">' + "".join(f'<label><input type="checkbox" class="input" name="{name}"{" checked" if c else ""}>{t}<span>{n}</span></label>' for t, n, c in opts) + "</div>"


filters_panel = f"""<aside class="shop-filters-panel" aria-label="Filters">
  <div class="cluster" data-justify="between"><h2 class="shop-section-title">Filters</h2><button type="button" class="btn" data-variant="link" data-size="sm">Clear all</button></div>
  <div class="accordion" data-multiple>
    <details open><summary>Category</summary><section>{checks("cat", [("Apparel", 24, True), ("Accessories", 12, False), ("Home", 18, False), ("Kitchen", 9, False)])}</section></details>
    <details open><summary>Price</summary><section class="stack" data-gap="2">
      <input type="range" class="input" id="s2-price" min="0" max="200" step="5" value="120" aria-label="Maximum price">
      <div class="shop-range-out"><span>$0</span><output for="s2-price" id="s2-price-out">Up to $120</output></div>
    </section></details>
    <details open><summary>Color</summary><section><fieldset class="shop-colors"><legend class="sr-only">Color</legend>{"".join(f'<label style="--dot: {c}" title="{n}"><input type="checkbox" aria-label="{n}"{" checked" if n == "Charcoal" else ""}></label>' for n, c in [("Charcoal", "#3f3f46"), ("Oat", "#d6cbb5"), ("Navy", "#1e3a5f"), ("Clay", "#c2856a"), ("Sage", "#9caf88")])}</fieldset></section></details>
    <details><summary>Rating</summary><section>{checks("rating", [("4 stars and up", 38, False), ("3 stars and up", 52, False)])}</section></details>
  </div>
  <div class="shop-switch-row"><label for="s2-stock">In stock only</label><input type="checkbox" role="switch" class="input" id="s2-stock" checked></div>
</aside>"""

RESULTS_JS = """
const priceIn = document.getElementById('s2-price');
priceIn?.addEventListener('input', () => { document.getElementById('s2-price-out').textContent = 'Up to $' + priceIn.value; });
document.querySelectorAll('[data-layout-toggle]').forEach((g) => {
  g.addEventListener('click', (e) => {
    const b = e.target.closest('button[data-layout-value]');
    if (!b) return;
    g.querySelectorAll('button').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
    document.getElementById(g.dataset.layoutToggle).dataset.layout = b.dataset.layoutValue;
  });
});
"""
pages = "".join(f'<li><a href="#" class="btn" data-variant="{"outline" if n == 1 else "ghost"}" data-size="icon"{" aria-current=\"page\"" if n == 1 else ""}>{n}</a></li>' for n in [1, 2, 3])
add("search-02", "Search 02", "Search results with filters, sort, active filter chips, grid and list views and pagination.", "search", f"""
{store_header(3)}
<main class="wrapper shop-page">
  <div class="stack" data-gap="6">
    <div class="stack" data-gap="1">
      <p class="shop-lead">Search results for</p>
      <h1 class="shop-h1">“sweater”</h1>
    </div>
    <div class="shop-results">
      {filters_panel}
      <div class="stack" data-gap="5">
        <div class="shop-toolbar">
          <p class="shop-lead">Showing 6 of 24 results</p>
          <div class="cluster" data-gap="2">
            <label class="sr-only" for="s2-sort">Sort by</label>
            <select class="select" id="s2-sort"><option>Most relevant</option><option>Newest</option><option>Price: low to high</option><option>Price: high to low</option><option>Top rated</option></select>
            <div class="button-group" role="group" aria-label="Layout" data-layout-toggle="s2-results">
              <button type="button" class="btn" data-variant="outline" data-size="icon" aria-label="Grid view" aria-pressed="true" data-layout-value="grid">{si("layout-grid")}</button>
              <button type="button" class="btn" data-variant="outline" data-size="icon" aria-label="List view" aria-pressed="false" data-layout-value="list">{si("list")}</button>
            </div>
          </div>
        </div>
        <div class="shop-chip-row">
          {"".join(f'<button type="button" class="badge" data-variant="secondary" aria-label="Remove filter {t}">{t}{si("x")}</button>' for t in ["Apparel", "Charcoal", "Up to $120", "In stock"])}
        </div>
        <div class="shop-cards" id="s2-results" data-layout="grid">{"".join(card(p) for p in [ITEMS[1], ITEMS[7], ITEMS[0], ITEMS[4], ITEMS[3], ITEMS[2]])}</div>
        <nav aria-label="Pagination" class="shop-pages"><ul>
          <li><a href="#" class="btn" data-variant="ghost">{si("chevron-left")}<span>Previous</span></a></li>
          {pages}
          <li><a href="#" class="btn" data-variant="ghost"><span>Next</span>{si("chevron-right")}</a></li>
        </ul></nav>
      </div>
    </div>
  </div>
</main>
""", CAT_CSS + """
  .button-group .btn[aria-pressed='true'] { background: var(--accent); color: var(--accent-foreground); }
  .shop-switch-row > label { font-size: 0.875rem; }
  .shop-switch-row { padding-block-start: 1rem; }
  .shop-pages ul { display: flex; justify-content: center; gap: 0.25rem; list-style: none; margin: 0; padding: 0; }
  .shop-cards[data-layout='list'] .shop-card { flex-direction: row; align-items: center; gap: 1rem; padding-block-end: 1rem; border-block-end: 1px solid var(--border); }
  .shop-cards[data-layout='list'] .shop-card-media { inline-size: 7rem; flex: none; }
  .shop-cards[data-layout='list'] .shop-card-body { flex: 1; }
  .shop-cards[data-layout='list'] .shop-card-quick { display: none; }
  @media (width < 56rem) { .shop-filters-panel { display: none; } }""", scripts=script(RESULTS_JS + WISH_JS))


# ================================================================== minicart drawer
drawer_lines = "\n".join(cart_line(p, "c5-", "sm") for p in PRODUCTS)
drawer_trigger = (
    f'<button type="button" class="btn shop-cart-btn" data-variant="ghost" data-size="icon" aria-label="Open cart" commandfor="c5-cart" command="show-modal">'
    f'{si("shopping-bag")}<span class="shop-count" data-cart-count>{count(PRODUCTS)}</span></button>'
)
add("cart-05", "Cart 05", "A mini cart in a bottom drawer, for mobile shops.", "cart", f"""
<div class="shop-app" data-cart>
  <header class="shop-app-bar">
    <h1>Acme Store</h1>
    <a href="#" class="btn" data-variant="ghost" data-size="icon" aria-label="Search">{si("search")}</a>
    {drawer_trigger}
  </header>
  <div class="shop-app-body">
    <div class="shop-banner"><p>Free shipping</p><strong>On every order over $150</strong></div>
    <div class="shop-grid shop-grid-2">{"".join(f'''<article class="shop-product">
      <img class="shop-product-img" src="{PH}" alt="">
      <div><h3>{n}</h3><p>{v}</p></div>
      <div class="shop-product-foot"><strong>{money(pr)}</strong><button type="button" class="btn" data-variant="outline" data-size="icon-sm" aria-label="Add {n} to cart" commandfor="c5-cart" command="show-modal">{si("plus")}</button></div>
    </article>''' for n, v, pr in CATALOG[:4])}</div>
  </div>
  <dialog id="c5-cart" class="drawer" aria-labelledby="c5-cart-title">
    <article>
      <header>
        <h2 id="c5-cart-title">Your cart</h2>
        <p data-item-count>{count(PRODUCTS)} items</p>
      </header>
      <section class="shop-drawer-lines">
        <div class="stack" data-gap="4" data-cart-filled>
          {free_progress(PRODUCTS)}
          <ul class="shop-lines" data-size="sm">
            {drawer_lines}
          </ul>
        </div>
        {EMPTY_CART}
      </section>
      <footer>
        <div class="shop-drawer-foot" data-cart-filled>
          <div class="shop-row"><span class="shop-muted">Subtotal</span><strong data-subtotal>{money(totals(PRODUCTS)[0])}</strong></div>
          <a href="#" class="btn">Checkout · <span data-grand-total>{money(totals(PRODUCTS)[3])}</span></a>
        </div>
        <button type="button" class="btn" data-variant="outline" commandfor="c5-cart" command="close">Continue shopping</button>
      </footer>
    </article>
  </dialog>
</div>
""", APP_CSS + CATALOG_CSS + "\n  .shop-app { padding-block-end: 2rem; }\n  .shop-link { color: inherit; text-decoration: none; }", scripts=script(CART_JS))



# ================================================================== interactive product cards
# Demo images: one placeholder, so the "other" photos are shown as tinted or
# mirrored copies (data-shot). Real shops use their own images.
FX_CSS = """
  .shop-fx-grid { display: grid; gap: 2rem 1.5rem; grid-template-columns: repeat(auto-fill, minmax(min(100%, 15rem), 1fr)); }
  .shop-fx { position: relative; display: flex; flex-direction: column; gap: 0.75rem; }
  .shop-fx-media { position: relative; overflow: hidden; border-radius: var(--radius); background: var(--muted); }
  .shop-fx-media > .shop-shot + .shop-shot { position: absolute; inset: 0; block-size: 100%; }
  .shop-fx-body { display: grid; gap: 0.25rem; }
  .shop-fx-body .cluster { margin-block-start: 0.25rem; }
  .shop-fx-swap > .shop-shot + .shop-shot { opacity: 0; transition: opacity 400ms ease, transform 600ms ease; }
  .shop-fx:hover .shop-fx-swap > .shop-shot + .shop-shot { opacity: 1; }
  .shop-fx-side { position: absolute; inset-block-start: 0.75rem; inset-inline-end: 0.75rem; z-index: 2; display: grid; gap: 0.375rem; }
  .shop-fx-side > .btn { background: var(--background); opacity: 0; transform: translateX(0.75rem); transition: opacity 200ms ease, transform 200ms ease; }
  .shop-fx-side > .btn:nth-child(2) { transition-delay: 50ms; }
  .shop-fx-side > .btn:nth-child(3) { transition-delay: 100ms; }
  .shop-fx:hover .shop-fx-side > .btn { opacity: 1; transform: none; }
  .shop-fx:focus-within .shop-fx-side > .btn { opacity: 1; transform: none; }
  .shop-fx-side > .btn[aria-pressed='true'] { opacity: 1; transform: none; }
  .shop-fx-bar { position: absolute; inset-inline: 0; inset-block-end: 0; z-index: 2; display: flex; padding: 0.75rem; transform: translateY(100%); transition: transform 250ms ease; }
  .shop-fx-bar > .btn { flex: 1; }
  .shop-fx:hover .shop-fx-bar { transform: none; }
  .shop-fx:focus-within .shop-fx-bar { transform: none; }
  @media (hover: none) { .shop-fx-side > .btn { opacity: 1; transform: none; } .shop-fx-bar { transform: none; } }
  .shop-fx-zones { position: absolute; inset: 0; z-index: 1; display: flex; }
  .shop-fx-zones > span { flex: 1; }
  .shop-fx-ticks { position: absolute; inset-inline: 0.75rem; inset-block-start: 0.625rem; z-index: 2; display: flex; gap: 0.25rem; opacity: 0; transition: opacity 200ms ease; }
  .shop-fx-ticks > span { flex: 1; block-size: 2px; border-radius: 2px; background: rgb(255 255 255 / 0.45); }
  .shop-fx-ticks > span[data-on] { background: #fff; }
  .shop-fx:hover .shop-fx-ticks { opacity: 1; }
  .shop-fx-gallery > .shop-shot { transition: opacity 150ms ease; }
  .shop-fx-gallery > .shop-shot:not([data-on]) { opacity: 0; }
  .shop-fx-nav { position: absolute; inset-block-start: 50%; z-index: 2; translate: 0 -50%; background: var(--background); opacity: 0; transition: opacity 200ms ease; }
  .shop-fx-nav[data-dir='prev'] { inset-inline-start: 0.5rem; }
  .shop-fx-nav[data-dir='next'] { inset-inline-end: 0.5rem; }
  .shop-fx:hover .shop-fx-nav { opacity: 1; }
  .shop-fx-nav:focus-visible { opacity: 1; }
  .shop-fx-swatches { display: flex; gap: 0.375rem; }
  .shop-fx-swatches > button { inline-size: 1.25rem; block-size: 1.25rem; padding: 0; border: 0; border-radius: 999px; background: var(--dot); box-shadow: inset 0 0 0 1px color-mix(in oklab, var(--foreground) 15%, transparent); cursor: pointer; }
  .shop-fx-swatches > button[aria-pressed='true'] { outline: 2px solid var(--primary); outline-offset: 2px; }
  .shop-fx-swatches > button:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
  .shop-fx-sizes { position: absolute; inset-inline: 0.5rem; inset-block-end: 0.5rem; z-index: 2; display: grid; gap: 0.5rem; padding: 0.75rem; border-radius: calc(var(--radius) - 2px); background: color-mix(in oklab, var(--background) 92%, transparent); backdrop-filter: blur(8px); opacity: 0; transform: translateY(0.75rem); transition: opacity 200ms ease, transform 200ms ease; }
  .shop-fx:hover .shop-fx-sizes { opacity: 1; transform: none; }
  .shop-fx:focus-within .shop-fx-sizes { opacity: 1; transform: none; }
  .shop-fx-sizes p { margin: 0; font-size: 0.75rem; font-weight: 500; text-align: center; }
  .shop-fx-sizes > div { display: flex; justify-content: center; gap: 0.375rem; }
  .shop-fx-sizes .btn { min-inline-size: 2.25rem; }
  .shop-fx-sizes .btn:disabled { text-decoration: line-through; }
  .shop-fx-done { position: absolute; inset: 0; z-index: 3; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; background: color-mix(in oklab, var(--background) 85%, transparent); backdrop-filter: blur(4px); font-size: 0.875rem; font-weight: 500; }
  .shop-fx-done svg { inline-size: 1.5rem; block-size: 1.5rem; color: var(--primary); }
  .shop-fx-done[hidden] { display: none; }
  @media (hover: none) { .shop-fx-sizes { opacity: 1; transform: none; } .shop-fx-nav { opacity: 1; } .shop-fx-ticks { opacity: 1; } }
  .shop-fx-lift { padding: 0.75rem; border: 1px solid transparent; border-radius: calc(var(--radius) + 4px); transition: transform 200ms ease, box-shadow 200ms ease, border-color 200ms ease; }
  .shop-fx-lift:hover { transform: translateY(-4px); border-color: var(--border); box-shadow: 0 16px 32px -16px rgb(0 0 0 / 0.25); }
  .shop-fx-lift .shop-fx-media > .shop-shot { transition: transform 400ms ease; }
  .shop-fx-lift:hover .shop-fx-media > .shop-shot { transform: scale(1.05); }
  .shop-fx-buy { display: grid; }
  .shop-fx-buy > .shop-qty { inline-size: 100%; justify-content: space-between; }
  .shop-fx-buy > .shop-qty > input { flex: 1; }
  .shop-fx-buy > [hidden] { display: none; }
  .shop-fx-pop { animation: shop-pop 250ms ease; }
  @keyframes shop-pop { from { transform: scale(0.96); opacity: 0.6; } to { transform: none; opacity: 1; } }
  .shop-fx-reveal { color: #fff; }
  .shop-fx-reveal .shop-fx-media > .shop-shot { aspect-ratio: 3 / 4; transition: transform 500ms ease; }
  .shop-fx-reveal:hover .shop-fx-media > .shop-shot { transform: scale(1.06); }
  .shop-fx-panel { position: absolute; inset-inline: 0; inset-block-end: 0; z-index: 2; display: grid; gap: 0.5rem; padding: 3rem 1rem 1rem; background: linear-gradient(to top, rgb(0 0 0 / 0.85), rgb(0 0 0 / 0.55) 60%, transparent); }
  .shop-fx-panel h3 { margin: 0; font-size: 1rem; font-weight: 600; }
  .shop-fx-panel h3 a { color: inherit; text-decoration: none; }
  .shop-fx-more { display: grid; grid-template-rows: 0fr; opacity: 0; transition: grid-template-rows 300ms ease, opacity 300ms ease; }
  .shop-fx-more > div { display: grid; gap: 0.75rem; min-block-size: 0; overflow: hidden; }
  .shop-fx-more p { margin: 0; font-size: 0.8125rem; opacity: 0.85; }
  .shop-fx-reveal:hover .shop-fx-more { grid-template-rows: 1fr; opacity: 1; }
  .shop-fx-reveal:focus-within .shop-fx-more { grid-template-rows: 1fr; opacity: 1; }
  .shop-fx-reveal[data-open] .shop-fx-more { grid-template-rows: 1fr; opacity: 1; }
  .shop-fx-panel .shop-price s { color: rgb(255 255 255 / 0.7); }
  .shop-fx-panel .shop-rating { color: rgb(255 255 255 / 0.8); }
  .shop-fx-panel .shop-rating svg { color: #fff; }
  .shop-fx-info { position: absolute; inset-block-start: 0.75rem; inset-inline-end: 0.75rem; z-index: 3; background: var(--background); }
  @media (hover: hover) { .shop-fx-info { display: none; } }
  .shop-fx-timer { display: flex; gap: 0.375rem; font-variant-numeric: tabular-nums; }
  .shop-fx-timer > span { display: grid; place-items: center; min-inline-size: 2.25rem; padding: 0.25rem; border-radius: calc(var(--radius) - 2px); background: var(--muted); font-size: 0.875rem; font-weight: 600; }
  .shop-fx-timer small { font-size: 0.625rem; font-weight: 400; color: var(--muted-foreground); }
  /* Reduced motion: the hover states still apply, without movement. !important so it wins over every card's transition rules. */
  @media (prefers-reduced-motion: reduce) { .shop-fx * { transition: none !important; animation: none !important; } }
  @media (prefers-reduced-motion: reduce) { .shop-fx-lift { transition: none; } }
  @media (prefers-reduced-motion: reduce) { .shop-fx-lift:hover { transform: none; } }
"""
FX = CAT_CSS + FX_CSS


def shot(n, extra=""):
    return f'<img class="shop-shot" src="{PH}" alt=""{f" data-shot={chr(34)}{n}{chr(34)}" if n > 1 else ""}{extra}>'


def fx_body(p, extra=""):
    return f"""<div class="shop-fx-body">
    <p class="shop-card-cat">{p["cat"]}</p>
    <h3 class="shop-card-name"><a href="#">{p["name"]}</a></h3>
    <div class="cluster" data-justify="between">{price(p)}{rating(p)}</div>
    {extra}
  </div>"""


def fx_header(title, lead):
    return f"""<div class="stack" data-gap="1">
      <h1 class="shop-h1">{title}</h1>
      <p class="shop-lead">{lead}</p>
    </div>"""


def page_fx(bid, title, desc, lead, cards, js, css=""):
    add(bid, title, desc, "product-card", f"""
<main class="wrapper shop-page">
  <div class="stack" data-gap="6">
    {fx_header(desc.split(":")[0], lead)}
    <div class="shop-fx-grid">
      {cards}
    </div>
  </div>
</main>
""", FX + css, scripts=script(js) if js else "")


# 04 — second image on hover, side actions and an add-to-cart bar slide in.
def fx04(p):
    return f"""<article class="shop-fx shop-card">
  <div class="shop-fx-media shop-fx-swap">
    {shot(1)}{shot(2)}
    {badge(p)}
    <div class="shop-fx-side">
      {wish_btn(p)}
      <button type="button" class="btn" data-variant="outline" data-size="icon-sm" aria-label="Quick view {p["name"]}">{si("eye")}</button>
      <button type="button" class="btn" data-variant="outline" data-size="icon-sm" aria-label="Compare {p["name"]}">{si("arrow-right-left")}</button>
    </div>
    <div class="shop-fx-bar"><button type="button" class="btn" data-size="sm">{si("shopping-bag")}Add to cart</button></div>
  </div>
  {fx_body(p, dots(p))}
</article>"""


page_fx("product-card-04", "Product Card 04", "Hover reveal: a second photo, side actions and an add-to-cart bar slide in on hover.",
        "Hover a card (or focus it with the keyboard): the photo changes and the actions slide in.",
        "".join(fx04(p) for p in ITEMS[:4]), WISH_JS)


# 05 — hover zones flip through photos; arrows and swatches pick a photo.
def fx05(p, i):
    n = 4
    shots = "".join(shot(k + 1, " data-on" if k == 0 else "") for k in range(n))
    sw = "".join(f'<button type="button" style="--dot: {c}" aria-label="{name}" aria-pressed="{"true" if j == 0 else "false"}" data-shot-to="{j}"></button>' for j, (name, c) in enumerate(p["colors"]))
    return f"""<article class="shop-fx shop-card" data-gallery>
  <div class="shop-fx-media shop-fx-gallery" aria-roledescription="carousel" aria-label="{p["name"]} photos">
    {shots}
    <div class="shop-fx-zones" aria-hidden="true">{"".join(f'<span data-zone="{k}"></span>' for k in range(n))}</div>
    <div class="shop-fx-ticks" aria-hidden="true">{"".join(f'<span{" data-on" if k == 0 else ""}></span>' for k in range(n))}</div>
    <button type="button" class="btn shop-fx-nav" data-dir="prev" data-variant="outline" data-size="icon-sm" aria-label="Previous photo">{si("chevron-left")}</button>
    <button type="button" class="btn shop-fx-nav" data-dir="next" data-variant="outline" data-size="icon-sm" aria-label="Next photo">{si("chevron-right")}</button>
    {badge(p)}
  </div>
  {fx_body(p, f'<div class="shop-fx-swatches" role="group" aria-label="Colors">{sw}</div>')}
</article>"""


GALLERY_JS = """
document.querySelectorAll('[data-gallery]').forEach((card) => {
  const media = card.querySelector('.shop-fx-gallery');
  const shots = media.querySelectorAll('.shop-shot');
  const ticks = media.querySelectorAll('.shop-fx-ticks > span');
  let i = 0;
  const show = (n) => {
    i = (n + shots.length) % shots.length;
    shots.forEach((s, k) => s.toggleAttribute('data-on', k === i));
    ticks.forEach((t, k) => t.toggleAttribute('data-on', k === i));
  };
  media.addEventListener('pointerover', (e) => { const z = e.target.closest('[data-zone]'); if (z) show(Number(z.dataset.zone)); });
  card.addEventListener('pointerleave', () => show(0));
  card.querySelector('[data-dir=prev]').addEventListener('click', () => show(i - 1));
  card.querySelector('[data-dir=next]').addEventListener('click', () => show(i + 1));
  card.querySelectorAll('[data-shot-to]').forEach((b) => {
    const pick = () => {
      card.querySelectorAll('[data-shot-to]').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      show(Number(b.dataset.shotTo));
    };
    b.addEventListener('click', pick);
    b.addEventListener('pointerenter', () => show(Number(b.dataset.shotTo)));
  });
});
"""
page_fx("product-card-05", "Product Card 05", "Hover gallery: move across the photo to flip through images; arrows and color swatches pick one.",
        "Move the pointer across a photo to flip through it, or use the arrows and swatches.",
        "".join(fx05(p, i) for i, p in enumerate([ITEMS[1], ITEMS[0], ITEMS[3], ITEMS[7]])), GALLERY_JS)


# 06 — size picker on hover; picking a size adds to the cart with a confirmation.
def fx06(p, i):
    sizes = "".join(f'<button type="button" class="btn" data-variant="outline" data-size="xs" data-add-size="{s_}"{" disabled" if (s_ == "XL" and i % 2 == 0) or (s_ == "XS" and i == 1) else ""}>{s_}</button>' for s_ in ["XS", "S", "M", "L", "XL"])
    return f"""<article class="shop-fx shop-card" data-size-card>
  <div class="shop-fx-media">
    {shot(1)}
    {badge(p)}
    <div class="shop-fx-sizes" role="group" aria-label="Quick add {p["name"]}">
      <p>Quick add · pick a size</p>
      <div>{sizes}</div>
    </div>
    <div class="shop-fx-done" role="status" hidden>{si("circle-check")}<span data-done-text>Added to cart</span></div>
  </div>
  {fx_body(p)}
</article>"""


SIZE_JS = """
document.querySelectorAll('[data-size-card]').forEach((card) => {
  const done = card.querySelector('.shop-fx-done');
  let t;
  card.addEventListener('click', (e) => {
    const b = e.target.closest('[data-add-size]');
    if (!b) return;
    done.querySelector('[data-done-text]').textContent = 'Size ' + b.dataset.addSize + ' added to cart';
    done.hidden = false;
    document.querySelectorAll('[data-cart-count]').forEach((el) => { el.textContent = (parseInt(el.textContent, 10) || 0) + 1; el.dataset.count = el.textContent; });
    clearTimeout(t);
    t = setTimeout(() => { done.hidden = true; }, 1600);
  });
});
"""
APPAREL = [ITEMS[1], ITEMS[7], {**ITEMS[1], "id": "tee", "name": "Organic Cotton Tee", "price": 28.00, "was": None, "rating": 4.6, "reviews": 412, "badge": "Bestseller"}, {**ITEMS[7], "id": "coat", "name": "Wool Overshirt", "price": 149.00, "was": None, "rating": 4.8, "reviews": 57, "badge": "New"}]
add("product-card-06", "Product Card 06", "Quick add on hover: pick a size on the photo and get a confirmation.", "product-card", f"""
{store_header(2)}
<main class="wrapper shop-page">
  <div class="stack" data-gap="6">
    {fx_header("Quick add sizes", "Hover a card and pick a size: it goes straight to the cart (watch the cart count).")}
    <div class="shop-fx-grid">
      {"".join(fx06(p, i) for i, p in enumerate(APPAREL))}
    </div>
  </div>
</main>
""", FX, scripts=script(SIZE_JS))


# 07 — the card lifts on hover; Add to cart turns into a quantity stepper.
def fx07(p, i):
    return f"""<article class="shop-fx shop-fx-lift shop-card" data-stepper-card>
  <div class="shop-fx-media">{shot(1)}{badge(p)}<div class="shop-fx-side">{wish_btn(p)}</div></div>
  {fx_body(p)}
  <div class="shop-fx-buy shop-card-actions">
    <button type="button" class="btn" data-variant="outline" data-buy>{si("plus")}Add to cart</button>
    {qty(f"fx7-{i}", 1).replace('min="1"', 'min="0"').replace('class="shop-qty"', 'class="shop-qty" hidden data-stepper')}
  </div>
</article>"""


STEPPER_JS = """
document.querySelectorAll('[data-stepper-card]').forEach((card) => {
  const add = card.querySelector('[data-buy]');
  const step = card.querySelector('[data-stepper]');
  const input = step.querySelector('[data-qty]');
  const bump = (d) => document.querySelectorAll('[data-cart-count]').forEach((el) => {
    const n = Math.max(0, (parseInt(el.textContent, 10) || 0) + d);
    el.textContent = n;
    el.dataset.count = n;
  });
  const swap = (showStep) => {
    add.hidden = showStep;
    step.hidden = !showStep;
    (showStep ? step : add).classList.remove('shop-fx-pop');
    void (showStep ? step : add).offsetWidth;
    (showStep ? step : add).classList.add('shop-fx-pop');
    (showStep ? step.querySelector('[data-qty-step="1"]') : add).focus();
  };
  add.addEventListener('click', () => { input.value = 1; bump(1); swap(true); });
  step.addEventListener('click', (e) => {
    const b = e.target.closest('[data-qty-step]');
    if (!b) return;
    const d = Number(b.dataset.qtyStep);
    const v = (parseInt(input.value, 10) || 0) + d;
    if (v > 10) return;
    input.value = v;
    bump(d);
    if (v <= 0) swap(false);
  });
});
"""
add("product-card-07", "Product Card 07", "Lift on hover and an Add to cart button that turns into a quantity stepper.", "product-card", f"""
{store_header(0)}
<main class="wrapper shop-page">
  <div class="stack" data-gap="6">
    {fx_header("Add, then adjust", "Add to cart becomes a stepper; going down to zero removes the item.")}
    <div class="shop-fx-grid">
      {"".join(fx07(p, i) for i, p in enumerate([ITEMS[2], ITEMS[5], ITEMS[4], ITEMS[6]]))}
    </div>
  </div>
</main>
""", FX, scripts=script(STEPPER_JS + WISH_JS))


# 08 — editorial card: details slide up over the photo; a button opens them on touch.
def fx08(p):
    return f"""<article class="shop-fx shop-fx-reveal shop-card" data-reveal>
  <div class="shop-fx-media">
    {shot(1)}
    <button type="button" class="btn shop-fx-info" data-variant="outline" data-size="icon-sm" aria-expanded="false" aria-label="Show details for {p["name"]}">{si("info")}</button>
    <div class="shop-fx-panel">
      <p class="shop-card-cat">{p["cat"]}</p>
      <h3><a href="#">{p["name"]}</a></h3>
      {price(p)}
      <div class="shop-fx-more"><div>
        <p>{p["desc"]}</p>
        {rating(p)}
        {dots(p)}
        <button type="button" class="btn" data-variant="secondary" data-size="sm">{si("shopping-bag")}Add to cart</button>
      </div></div>
    </div>
  </div>
</article>"""


REVEAL_JS = """
document.querySelectorAll('[data-reveal]').forEach((card) => {
  const b = card.querySelector('.shop-fx-info');
  b.addEventListener('click', () => {
    const open = b.getAttribute('aria-expanded') !== 'true';
    b.setAttribute('aria-expanded', String(open));
    card.toggleAttribute('data-open', open);
  });
});
"""
page_fx("product-card-08", "Product Card 08", "Editorial reveal: details, rating and add to cart slide up over the photo on hover.",
        "Hover a photo for details. On touch screens, the info button opens them.",
        "".join(fx08(p) for p in [ITEMS[6], ITEMS[0], ITEMS[3], ITEMS[1]]), REVEAL_JS,
        "\n  .shop-fx-reveal .shop-card-cat { color: rgb(255 255 255 / 0.75); }\n  .shop-fx-reveal .shop-card-name a::after { content: none; }")


# 09 — flash sale: stock bar and a countdown to the end of the sale.
def fx09(p, sold, left):
    pct = round(sold / (sold + left) * 100)
    return f"""<article class="shop-fx shop-fx-lift shop-card">
  <div class="shop-fx-media">{shot(1)}<span class="badge shop-card-badge" data-variant="destructive">-{round((1 - p["price"] / p["was"]) * 100)}%</span></div>
  {fx_body(p)}
  <div class="stack" data-gap="1">
    <div class="progress" role="progressbar" aria-label="Sold" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{pct}"><span style="width: {pct}%"></span></div>
    <p class="shop-line-meta">{sold} sold · only {left} left</p>
  </div>
  <div class="shop-card-actions"><button type="button" class="btn">{si("shopping-bag")}Buy now</button></div>
</article>"""


# The countdown starts from a fixed time left (a real shop renders its end time);
# it ticks once a second.
TIMER_JS = """
document.querySelectorAll('[data-countdown]').forEach((el) => {
  let left = Number(el.dataset.countdown);
  const parts = el.querySelectorAll('[data-unit]');
  const pad = (n) => String(n).padStart(2, '0');
  const draw = () => {
    const v = [Math.floor(left / 3600), Math.floor(left / 60) % 60, left % 60];
    parts.forEach((p, k) => { p.firstChild.textContent = pad(v[k]); });
  };
  draw();
  setInterval(() => { if (left > 0) { left--; draw(); } }, 1000);
});
"""
SALE = [{**ITEMS[1], "was": 129.00}, {**ITEMS[3]}, {**ITEMS[7]}, {**ITEMS[6], "price": 99.00, "was": 129.00}]
add("product-card-09", "Product Card 09", "Flash sale cards with a discount badge, stock bar and a live countdown.", "product-card", f"""
<main class="wrapper shop-page">
  <div class="stack" data-gap="6">
    <div class="cluster" data-justify="between" data-gap="4">
      {fx_header("Flash sale", "Up to 40% off while stock lasts.")}
      <div class="stack" data-gap="1">
        <p class="shop-line-meta">Ends in</p>
        <div class="shop-fx-timer" data-countdown="22735" role="timer" aria-label="Time left in the sale">
          <span data-unit>06<small>hrs</small></span><span data-unit>18<small>min</small></span><span data-unit>55<small>sec</small></span>
        </div>
      </div>
    </div>
    <div class="shop-fx-grid">
      {"".join(fx09(p, s_, l) for p, (s_, l) in zip(SALE, [(86, 14), (42, 18), (61, 9), (23, 27)]))}
    </div>
  </div>
</main>
""", FX, scripts=script(TIMER_JS))



# ================================================================== filter and category data
# Each card carries its facets as data-* attributes; FILTER_JS reads the form.
SHOP_ITEMS = [
    {**ITEMS[0], "sizes": ["One size"], "stock": "in"},
    {**ITEMS[1], "sizes": ["S", "M", "L"], "stock": "in"},
    {**ITEMS[2], "sizes": ["One size"], "stock": "in"},
    {**ITEMS[3], "sizes": ["One size"], "stock": "out"},
    {**ITEMS[4], "sizes": ["One size"], "stock": "in"},
    {**ITEMS[5], "sizes": ["One size"], "stock": "in"},
    {**ITEMS[6], "sizes": ["One size"], "stock": "in"},
    {**ITEMS[7], "sizes": ["One size"], "stock": "in"},
    {**ITEMS[1], "id": "tee", "name": "Organic Cotton Tee", "price": 28.00, "was": None, "rating": 4.6, "reviews": 412, "badge": "Bestseller", "colors": [("Oat", "#d6cbb5"), ("Black", "#262626"), ("Navy", "#1e3a5f")], "sizes": ["XS", "S", "M", "L", "XL"], "stock": "in"},
    {**ITEMS[7], "id": "coat", "name": "Wool Overshirt", "price": 149.00, "was": None, "rating": 4.8, "reviews": 57, "badge": "New", "colors": [("Camel", "#c19a6b"), ("Charcoal", "#3f3f46")], "sizes": ["S", "M", "L", "XL"], "stock": "in"},
    {**ITEMS[2], "id": "bowl", "name": "Stoneware Bowl Set", "price": 42.00, "was": 56.00, "rating": 4.5, "reviews": 73, "badge": "Sale", "colors": [("Sand", "#d8c3a5"), ("Ink", "#2b3442")], "sizes": ["One size"], "stock": "in"},
    {**ITEMS[3], "id": "throw", "name": "Waffle Knit Throw", "price": 68.00, "was": None, "rating": 4.2, "reviews": 19, "badge": None, "colors": [("Ivory", "#f1ead8"), ("Sage", "#9caf88")], "sizes": ["One size"], "stock": "in"},
]
FACET_COLORS = [("Black", "#262626"), ("Charcoal", "#3f3f46"), ("Oat", "#d6cbb5"), ("Navy", "#1e3a5f"), ("Sage", "#9caf88"), ("Camel", "#c19a6b"), ("Ivory", "#f1ead8"), ("Sand", "#d8c3a5")]
FACET_CATS = ["Apparel", "Accessories", "Bags", "Home", "Kitchen"]
FACET_SIZES = ["XS", "S", "M", "L", "XL", "One size"]


def faceted(p, html):
    attrs = (f' data-product data-cat="{p["cat"]}" data-price="{p["price"]:.2f}" data-rating="{p["rating"]}"'
             f' data-stock="{p["stock"]}" data-colors="{" ".join(n for n, _ in p["colors"])}" data-sizes="{"|".join(p["sizes"])}"')
    return html.replace('<article class="shop-card">', f'<article class="shop-card"{attrs}>', 1)


def fcard(p):
    return faceted(p, card(p))


FILTER_JS = """
document.querySelectorAll('[data-filter-form]').forEach((form) => {
  const grid = document.getElementById(form.dataset.filterForm);
  const cards = [...grid.querySelectorAll('[data-product]')];
  const fmt = (v) => '$' + v;
  const chips = document.querySelectorAll('[data-filter-chips]');
  const run = () => {
    const fd = new FormData(form);
    const cats = fd.getAll('cat'), colors = fd.getAll('color'), sizes = fd.getAll('size');
    const min = parseFloat(fd.get('min')) || 0;
    const maxIn = form.elements.max;
    const max = maxIn && maxIn.value !== '' && Number(maxIn.value) < Number(maxIn.max || Infinity) ? parseFloat(maxIn.value) : Infinity;
    const rating = parseFloat(fd.get('rating')) || 0;
    const stock = fd.get('stock');
    let n = 0;
    for (const c of cards) {
      const d = c.dataset;
      const ok = (!cats.length || cats.includes(d.cat))
        && (!colors.length || d.colors.split(' ').some((x) => colors.includes(x)))
        && (!sizes.length || d.sizes.split('|').some((x) => sizes.includes(x)))
        && Number(d.price) >= min && Number(d.price) <= max
        && Number(d.rating) >= rating && (!stock || d.stock === 'in');
      c.hidden = !ok;
      if (ok) n++;
    }
    const active = [
      ...cats.map((v) => ['cat', v, v]), ...colors.map((v) => ['color', v, v]), ...sizes.map((v) => ['size', v, 'Size ' + v]),
      ...(min || max !== Infinity ? [['price', '', (min ? fmt(min) : '$0') + ' – ' + (max !== Infinity ? fmt(max) : 'any')]] : []),
      ...(rating ? [['rating', '', rating + '★ & up']] : []), ...(stock ? [['stock', '', 'In stock']] : []),
    ];
    document.querySelectorAll('[data-result-count]').forEach((el) => { el.textContent = n + (n === 1 ? ' product' : ' products'); });
    document.querySelectorAll('[data-filter-active]').forEach((el) => { el.textContent = active.length; el.hidden = !active.length; });
    document.querySelectorAll('[data-filter-empty]').forEach((el) => { el.hidden = n > 0; });
    const out = form.querySelector('output[data-max-out]');
    if (out && maxIn) out.textContent = 'Up to ' + fmt(maxIn.value);
    chips.forEach((box) => {
      box.replaceChildren(...active.map(([name, value, label]) => {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'badge';
        b.dataset.variant = 'secondary';
        b.dataset.clear = name;
        b.dataset.value = value;
        b.setAttribute('aria-label', 'Remove filter ' + label);
        b.append(label, document.querySelector('[data-chip-icon] svg').cloneNode(true));
        return b;
      }));
      box.hidden = !active.length;
    });
  };
  const clear = (name, value) => {
    if (name === 'price') { if (form.elements.min) form.elements.min.value = ''; if (form.elements.max) form.elements.max.value = form.elements.max.max || ''; }
    else form.querySelectorAll(`[name="${name}"]`).forEach((i) => { if (!value || i.value === value) { if (i.type === 'radio' || i.type === 'checkbox') i.checked = false; else i.value = ''; } });
    run();
  };
  form.addEventListener('input', run);
  form.addEventListener('reset', () => setTimeout(run));
  document.addEventListener('click', (e) => {
    const chip = e.target.closest('[data-clear]');
    if (chip) clear(chip.dataset.clear, chip.dataset.value);
  });
  const sort = document.querySelector(`[data-sort="${form.dataset.filterForm}"]`);
  sort?.addEventListener('change', () => {
    const by = {
      'price-asc': (a, b) => a.dataset.price - b.dataset.price,
      'price-desc': (a, b) => b.dataset.price - a.dataset.price,
      rating: (a, b) => b.dataset.rating - a.dataset.rating,
    }[sort.value];
    const list = by ? [...cards].sort(by) : cards;
    grid.prepend(...list);
  });
});
"""

def chip_box():
    # The chip icon is cloned from a hidden copy, so it follows the icon library.
    return f'<span data-chip-icon hidden>{si("x")}</span><div class="shop-chip-row" data-filter-chips hidden></div>'


def filter_checks(name, values, counts=None, p="f"):
    return '<div class="shop-check-list">' + "".join(
        f'<label><input type="checkbox" class="input" name="{name}" value="{v}">{v}{f"<span>{counts[i]}</span>" if counts else ""}</label>' for i, v in enumerate(values)) + "</div>"


def color_checks(name):
    return ('<fieldset class="shop-colors"><legend class="sr-only">Color</legend>'
            + "".join(f'<label style="--dot: {c}" title="{n}"><input type="checkbox" name="{name}" value="{n}" aria-label="{n}"></label>' for n, c in FACET_COLORS)
            + "</fieldset>")


def size_checks(name):
    return ('<fieldset class="shop-swatches shop-swatches-wrap"><legend class="sr-only">Size</legend>'
            + "".join(f'<label><input type="checkbox" name="{name}" value="{s_}">{s_}</label>' for s_ in FACET_SIZES)
            + "</fieldset>")


def rating_radios(name, p):
    return '<div class="shop-check-list" role="radiogroup" aria-label="Rating">' + "".join(
        f'<label><input type="radio" class="input" name="{name}" value="{r}">{stars(r)}<span class="shop-rate-label">{r} &amp; up</span></label>' for r in [4.5, 4, 3.5]) + "</div>"


def price_fields(p):
    return f"""<div class="shop-price-fields">
  <div class="input-group"><input type="number" name="min" id="{p}-min" min="0" step="1" placeholder="Min" aria-label="Minimum price"><span data-align="start">$</span></div>
  <span aria-hidden="true">–</span>
  <div class="input-group"><input type="number" name="max" id="{p}-max" min="0" step="1" placeholder="Max" aria-label="Maximum price"><span data-align="start">$</span></div>
</div>"""


FILTER_CSS = """
  .shop-price-fields { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 0.5rem; color: var(--muted-foreground); }
  .shop-swatches-wrap { flex-wrap: wrap; }
  .shop-check-list .shop-rate-label { margin-inline-start: 0.25rem; color: var(--muted-foreground); font-size: 0.8125rem; }
  .shop-filter-head { display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; }
  .shop-filter-head h2 { display: flex; align-items: center; gap: 0.5rem; }
  .shop-filter-head .badge[hidden] { display: none; }
  .shop-filter-bar { display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem; }
  .shop-filter-pop { inline-size: 16rem; }
  .shop-filter-pop[data-size='lg'] { inline-size: 20rem; }
  .shop-filter-bar .btn svg:last-child { inline-size: 0.875rem; block-size: 0.875rem; color: var(--muted-foreground); }
  .shop-filter-sep { inline-size: 1px; block-size: 1.5rem; background: var(--border); }
  .shop-filter-end { margin-inline-start: auto; }
  .shop-filter-sheet section { display: grid; gap: 0.5rem; }
  .shop-filter-sheet .accordion summary { font-size: 0.9375rem; }
  .shop-filter-sheet footer { display: grid; grid-template-columns: auto 1fr; gap: 0.5rem; }
  .shop-filter-btn { position: relative; }
  .shop-filter-btn .badge { min-inline-size: 1.25rem; padding-inline: 0.25rem; justify-content: center; }
  .shop-filter-btn .badge[hidden] { display: none; }
  .shop-mobile-toolbar { position: sticky; inset-block-start: 3.5rem; z-index: 4; display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; padding: 0.75rem 1rem; background: var(--background); border-block-end: 1px solid var(--border); }
  .shop-mobile-toolbar .select { inline-size: 100%; }
"""
FILTER_ALL = CAT_CSS + FILTER_CSS + """
  .shop-switch-row > label { font-size: 0.875rem; }
  .shop-pages ul { display: flex; justify-content: center; gap: 0.25rem; list-style: none; margin: 0; padding: 0; }"""

FILTER_EMPTY = f"""<section class="empty" data-filter-empty hidden>
  <header>
    <figure>{si("search")}</figure>
    <h3>No products match</h3>
    <p>Try removing a filter or widening the price range.</p>
  </header>
  <footer><button type="reset" class="btn" data-variant="outline" form="{{form}}">Clear filters</button></footer>
</section>"""

n_all = len(SHOP_ITEMS)
cat_counts = [sum(1 for p in SHOP_ITEMS if p["cat"] == c) for c in FACET_CATS]
SORT = '<option value="">Featured</option><option value="price-asc">Price: low to high</option><option value="price-desc">Price: high to low</option><option value="rating">Top rated</option>'

# ================================================================== filter 01: sidebar
add("filter-01", "Filter 01", "A filter sidebar that filters the grid live: category, price, color, size, rating and stock, with chips and sort.", "filter", f"""
{store_header(3)}
<main class="wrapper shop-page">
  <div class="stack" data-gap="6">
    <div class="stack" data-gap="1">
      <h1 class="shop-h1">All products</h1>
      <p class="shop-lead" data-result-count>{n_all} products</p>
    </div>
    <div class="shop-results">
      <form class="shop-filters-panel" id="f1-form" data-filter-form="f1-grid" aria-label="Filters" onsubmit="event.preventDefault()">
        <div class="shop-filter-head">
          <h2 class="shop-section-title">Filters <span class="badge" data-filter-active hidden>0</span></h2>
          <button type="reset" class="btn" data-variant="link" data-size="sm">Clear all</button>
        </div>
        <div class="accordion" data-multiple>
          <details open><summary>Category</summary><section>{filter_checks("cat", FACET_CATS, cat_counts)}</section></details>
          <details open><summary>Price</summary><section>{price_fields("f1")}</section></details>
          <details open><summary>Color</summary><section>{color_checks("color")}</section></details>
          <details><summary>Size</summary><section>{size_checks("size")}</section></details>
          <details><summary>Rating</summary><section>{rating_radios("rating", "f1")}</section></details>
        </div>
        <div class="shop-switch-row"><label for="f1-stock">In stock only</label><input type="checkbox" role="switch" class="input" id="f1-stock" name="stock" value="in"></div>
      </form>
      <div class="stack" data-gap="5">
        <div class="shop-toolbar">
          {chip_box()}
          <div class="cluster shop-filter-end" data-gap="2">
            <label class="sr-only" for="f1-sort">Sort by</label>
            <select class="select" id="f1-sort" data-sort="f1-grid">{SORT}</select>
          </div>
        </div>
        <div class="shop-cards" id="f1-grid">{"".join(fcard(p) for p in SHOP_ITEMS)}</div>
        {FILTER_EMPTY.replace("{form}", "f1-form")}
      </div>
    </div>
  </div>
</main>
""", FILTER_ALL + "\n  @media (width < 56rem) { .shop-filters-panel { display: none; } }", scripts=script(FILTER_JS + WISH_JS))


# ================================================================== filter 02: horizontal bar with popovers
def pop(id_, label, body, size=None):
    sz = f' data-size="{size}"' if size else ""
    return f"""<div class="popover">
  <button type="button" class="btn" data-variant="outline" data-size="sm" popovertarget="{id_}">{label}{si("chevron-down")}</button>
  <div id="{id_}" class="shop-filter-pop"{sz} data-popover popover data-side="bottom" data-align="start">{body}</div>
</div>"""


f2_bar = "".join([
    pop("f2-cat", "Category", filter_checks("cat", FACET_CATS, cat_counts)),
    pop("f2-price", "Price", price_fields("f2"), "lg"),
    pop("f2-color", "Color", color_checks("color")),
    pop("f2-size", "Size", size_checks("size"), "lg"),
    pop("f2-rating", "Rating", rating_radios("rating", "f2")),
])
add("filter-02", "Filter 02", "A horizontal filter bar with a popover per filter, active chips, a result count and sort.", "filter", f"""
{store_header(3)}
<main class="wrapper shop-page">
  <div class="stack" data-gap="5">
    <div class="stack" data-gap="1">
      <h1 class="shop-h1">Shop all</h1>
      <p class="shop-lead">Considered pieces for every room and every day.</p>
    </div>
    <form class="shop-filter-bar" id="f2-form" data-filter-form="f2-grid" aria-label="Filters" onsubmit="event.preventDefault()">
      {f2_bar}
      <label class="btn shop-stock-toggle" data-variant="outline" data-size="sm"><input type="checkbox" class="input" name="stock" value="in">In stock</label>
      <span class="shop-filter-sep" aria-hidden="true"></span>
      <button type="reset" class="btn" data-variant="ghost" data-size="sm">Reset <span class="badge" data-filter-active hidden>0</span></button>
      <div class="cluster shop-filter-end" data-gap="2">
        <p class="shop-lead" data-result-count>{n_all} products</p>
        <label class="sr-only" for="f2-sort">Sort by</label>
        <select class="select" id="f2-sort" data-sort="f2-grid">{SORT}</select>
      </div>
    </form>
    {chip_box()}
    <div class="shop-cards" id="f2-grid">{"".join(fcard(p) for p in SHOP_ITEMS)}</div>
    {FILTER_EMPTY.replace("{form}", "f2-form")}
  </div>
</main>
""", FILTER_ALL + """
  .shop-stock-toggle { gap: 0.5rem; cursor: pointer; }
  .shop-filter-bar .btn .badge[hidden] { display: none; }""", scripts=script(FILTER_JS + WISH_JS))


# ================================================================== filter 03: mobile sheet
f3_items = SHOP_ITEMS[:8]
add("filter-03", "Filter 03", "Mobile filters in a bottom sheet: grouped filters, a live result count and a sticky show-results button.", "filter", f"""
<div class="shop-app">
  <header class="shop-app-bar">
    <a href="#" class="btn" data-variant="ghost" data-size="icon" aria-label="Back">{si("chevron-left")}</a>
    <h1>All products</h1>
    <a href="#" class="btn" data-variant="ghost" data-size="icon" aria-label="Search">{si("search")}</a>
  </header>
  <div class="shop-mobile-toolbar">
    <button type="button" class="btn shop-filter-btn" data-variant="outline" commandfor="f3-sheet" command="show-modal">{si("sliders-horizontal")}Filters <span class="badge" data-filter-active hidden>0</span></button>
    <label class="sr-only" for="f3-sort">Sort by</label>
    <select class="select" id="f3-sort" data-sort="f3-grid">{SORT}</select>
  </div>
  <div class="shop-app-body">
    {chip_box()}
    <p class="shop-lead" data-result-count>{len(f3_items)} products</p>
    <div class="shop-grid shop-grid-2" id="f3-grid">{"".join(fcard(p) for p in f3_items)}</div>
    {FILTER_EMPTY.replace("{form}", "f3-form")}
  </div>
  <dialog id="f3-sheet" class="sheet shop-filter-sheet" data-side="bottom" closedby="any" aria-labelledby="f3-title">
    <header>
      <h2 id="f3-title">Filters</h2>
      <p>Results update as you choose.</p>
    </header>
    <section>
      <form id="f3-form" data-filter-form="f3-grid" onsubmit="event.preventDefault()">
        <div class="accordion" data-multiple>
          <details open><summary>Category</summary><section>{filter_checks("cat", FACET_CATS)}</section></details>
          <details open><summary>Price</summary><section class="stack" data-gap="2">
            <input type="range" class="input" name="max" min="0" max="150" step="5" value="150" aria-label="Maximum price">
            <div class="shop-range-out"><span>$0</span><output data-max-out>Up to $150</output></div>
          </section></details>
          <details><summary>Color</summary><section>{color_checks("color")}</section></details>
          <details><summary>Rating</summary><section>{rating_radios("rating", "f3")}</section></details>
        </div>
        <div class="shop-switch-row"><label for="f3-stock">In stock only</label><input type="checkbox" role="switch" class="input" id="f3-stock" name="stock" value="in"></div>
      </form>
    </section>
    <footer>
      <button type="reset" form="f3-form" class="btn" data-variant="outline">Reset</button>
      <button type="button" class="btn" commandfor="f3-sheet" command="close">Show <span data-result-count>{len(f3_items)} products</span></button>
    </footer>
    <button type="button" aria-label="Close" commandfor="f3-sheet" command="close">{si("x")}</button>
  </dialog>
</div>
""", APP_CSS + CATALOG_CSS + FILTER_CSS + """
  .shop-app { padding-block-end: 2rem; }
  .shop-app-body > .shop-chip-row[hidden] { display: none; }
  .shop-switch-row { padding-block: 1rem; }
  .shop-switch-row > label { font-size: 0.875rem; }
  .shop-filter-sheet { max-block-size: 85svh; }""", scripts=script(FILTER_JS + WISH_JS))


# ================================================================== category pages
CATEGORY_CSS = """
  .shop-hero { position: relative; display: grid; align-items: end; min-block-size: 20rem; overflow: hidden; border-radius: calc(var(--radius) + 4px); color: #fff; }
  .shop-hero > img { position: absolute; inset: 0; inline-size: 100%; block-size: 100%; object-fit: cover; }
  .shop-hero::after { content: ''; position: absolute; inset: 0; background: linear-gradient(to top, rgb(0 0 0 / 0.7), rgb(0 0 0 / 0.1) 70%); }
  .shop-hero-body { position: relative; z-index: 1; display: grid; gap: 0.75rem; max-inline-size: 36rem; padding: 2rem; }
  .shop-hero-body h1 { margin: 0; font-size: clamp(2rem, 5vw, 3rem); font-weight: 600; letter-spacing: -0.03em; line-height: 1.05; }
  .shop-hero-body p { margin: 0; opacity: 0.85; }
  .shop-hero-body .btn { justify-self: start; }
  .shop-subcats { display: flex; gap: 1.25rem; overflow-x: auto; padding-block-end: 0.5rem; scroll-snap-type: x mandatory; list-style: none; margin: 0; padding-inline: 0; }
  .shop-subcats > li { scroll-snap-align: start; }
  .shop-subcats a { display: grid; justify-items: center; gap: 0.5rem; inline-size: 6.5rem; color: inherit; text-decoration: none; font-size: 0.875rem; text-align: center; }
  .shop-subcats img { inline-size: 6.5rem; block-size: 6.5rem; border-radius: 999px; object-fit: cover; background: var(--muted); transition: transform 200ms ease, box-shadow 200ms ease; }
  .shop-subcats a:hover img { transform: scale(1.05); box-shadow: 0 0 0 2px var(--background), 0 0 0 4px var(--primary); }
  .shop-subcats small { color: var(--muted-foreground); font-size: 0.75rem; }
  .shop-tiles { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr)); }
  .shop-tile { position: relative; display: block; overflow: hidden; border-radius: calc(var(--radius) + 4px); color: #fff; text-decoration: none; min-block-size: 14rem; }
  .shop-tile > img { position: absolute; inset: 0; inline-size: 100%; block-size: 100%; object-fit: cover; transition: transform 500ms ease; }
  .shop-tile::after { content: ''; position: absolute; inset: 0; background: linear-gradient(to top, rgb(0 0 0 / 0.65), transparent 60%); }
  .shop-tile:hover > img { transform: scale(1.06); }
  .shop-tile:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
  .shop-tile-body { position: absolute; inset-inline: 0; inset-block-end: 0; z-index: 1; display: flex; align-items: flex-end; justify-content: space-between; gap: 1rem; padding: 1.25rem; }
  .shop-tile-body h3 { margin: 0; font-size: 1.25rem; font-weight: 600; }
  .shop-tile-body p { margin: 0; font-size: 0.8125rem; opacity: 0.85; }
  .shop-tile-go { display: inline-flex; align-items: center; justify-content: center; inline-size: 2.25rem; block-size: 2.25rem; border-radius: 999px; background: #fff; color: #111; transform: translateX(-0.5rem); opacity: 0; transition: transform 200ms ease, opacity 200ms ease; }
  .shop-tile-go svg { inline-size: 1rem; block-size: 1rem; }
  .shop-tile:hover .shop-tile-go { transform: none; opacity: 1; }
  .shop-tile:focus-visible .shop-tile-go { transform: none; opacity: 1; }
  @media (hover: none) { .shop-tile-go { transform: none; opacity: 1; } }
  .shop-bento { display: grid; gap: 1rem; grid-template-columns: repeat(2, minmax(0, 1fr)); grid-auto-rows: 13rem; }
  @media (width >= 48rem) { .shop-bento { grid-template-columns: repeat(4, minmax(0, 1fr)); } .shop-bento > [data-span='wide'] { grid-column: span 2; } .shop-bento > [data-span='tall'] { grid-row: span 2; } .shop-bento > [data-span='big'] { grid-column: span 2; grid-row: span 2; } }
  .shop-bento > .shop-tile { min-block-size: 0; }
  .shop-promo-split { display: grid; gap: 1.5rem; align-items: center; padding: 2rem; border-radius: calc(var(--radius) + 4px); background: var(--muted); }
  @media (width >= 48rem) { .shop-promo-split { grid-template-columns: 1fr 1fr; padding: 2.5rem; } }
  .shop-promo-split img { inline-size: 100%; aspect-ratio: 16 / 10; border-radius: var(--radius); object-fit: cover; }
  .shop-promo-split h2 { margin: 0; font-size: 1.5rem; font-weight: 600; }
  .shop-promo-split p { margin: 0; color: var(--muted-foreground); }
  .shop-tree ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.125rem; }
  .shop-tree ul ul { padding-inline-start: 0.75rem; margin-block: 0.25rem; border-inline-start: 1px solid var(--border); }
  .shop-tree a { display: flex; justify-content: space-between; gap: 0.5rem; padding: 0.375rem 0.625rem; border-radius: calc(var(--radius) - 2px); color: var(--muted-foreground); font-size: 0.875rem; text-decoration: none; }
  .shop-tree a:hover { background: var(--accent); color: var(--accent-foreground); }
  .shop-tree a[aria-current] { background: var(--muted); color: var(--foreground); font-weight: 500; }
  .shop-tree a span { font-size: 0.75rem; font-variant-numeric: tabular-nums; }
  .shop-tree summary { display: flex; align-items: center; gap: 0.375rem; padding: 0.375rem 0.625rem; border-radius: calc(var(--radius) - 2px); font-size: 0.875rem; font-weight: 500; cursor: pointer; list-style: none; }
  .shop-tree summary::-webkit-details-marker { display: none; }
  .shop-tree summary svg { inline-size: 0.875rem; block-size: 0.875rem; transition: transform 150ms ease; }
  .shop-tree details[open] > summary svg { transform: rotate(90deg); }
  .shop-tree summary:hover { background: var(--accent); }
  .shop-pills { display: flex; gap: 0.5rem; overflow-x: auto; scrollbar-width: none; }
  .shop-pills a { flex: none; padding: 0.375rem 0.875rem; border: 1px solid var(--border); border-radius: 999px; color: inherit; font-size: 0.875rem; text-decoration: none; white-space: nowrap; }
  .shop-pills a:hover { background: var(--accent); }
  .shop-pills a[aria-current] { border-color: var(--primary); background: var(--primary); color: var(--primary-foreground); }
  .shop-more { display: grid; justify-items: center; gap: 0.75rem; padding-block-start: 1rem; }
  .shop-more p { margin: 0; font-size: 0.875rem; color: var(--muted-foreground); }
  .shop-more .progress { inline-size: 12rem; }
  .shop-seo { max-inline-size: 48rem; }
  html.dark .shop-tile > img { filter: brightness(0.6); }
  html.dark .shop-hero > img { filter: brightness(0.6); }
"""
CATP = CAT_CSS + FX_CSS + CATEGORY_CSS

SUBCATS = [("Living room", 64, 1), ("Bedroom", 48, 2), ("Kitchen", 72, 3), ("Dining", 31, 4), ("Bath", 26, 1), ("Lighting", 39, 2), ("Textiles", 57, 3), ("Decor", 88, 4)]
subcats = "".join(f'<li><a href="#"><img src="{PH}" alt=""{f" class={chr(34)}shop-shot{chr(34)} data-shot={chr(34)}{s_}{chr(34)}" if s_ > 1 else ""}><span>{n}</span><small>{c} items</small></a></li>' for n, c, s_ in SUBCATS)


def tile(title, sub, n=1, span=None, heading="h3"):
    sp = f' data-span="{span}"' if span else ""
    return f"""<a href="#" class="shop-tile"{sp}>
  {shot(n)}
  <div class="shop-tile-body"><div><{heading}>{title}</{heading}><p>{sub}</p></div><span class="shop-tile-go" aria-hidden="true">{si("arrow-right")}</span></div>
</a>"""


add("category-01", "Category 01", "A category landing page: hero, subcategory circles, rooms, featured products, a promo and an FAQ.", "category", f"""
{store_header(3)}
<main class="wrapper shop-page">
  <div class="stack" data-gap="12">
    <div class="stack" data-gap="4">
      <nav class="breadcrumb shop-crumbs" aria-label="Breadcrumb"><ol><li><a href="#">Home</a></li>{crumb_sep}<li><span aria-current="page">Home &amp; Living</span></li></ol></nav>
      <section class="shop-hero" aria-labelledby="c1-title">
        {shot(3)}
        <div class="shop-hero-body">
          <span class="badge" data-variant="secondary">Autumn edit</span>
          <h1 id="c1-title">Home &amp; Living</h1>
          <p>Natural materials, soft light and pieces made to last. 425 products across every room.</p>
          <a href="#c1-featured" class="btn" data-variant="secondary">Shop the edit{si("arrow-right")}</a>
        </div>
      </section>
    </div>
    <section class="stack" data-gap="4" aria-labelledby="c1-subs">
      <h2 class="shop-h2" id="c1-subs">Shop by category</h2>
      <ul class="shop-subcats">{subcats}</ul>
    </section>
    <section class="stack" data-gap="4" aria-labelledby="c1-rooms">
      <div class="cluster" data-justify="between"><h2 class="shop-h2" id="c1-rooms">Shop by room</h2><a href="#" class="btn" data-variant="link" data-size="sm">All rooms{si("arrow-right")}</a></div>
      <div class="shop-tiles">{tile("Living room", "Sofas, throws and lamps", 2)}{tile("Bedroom", "Linen, pillows and calm", 4)}{tile("Kitchen", "Stoneware and tools", 3)}</div>
    </section>
    <section class="stack" data-gap="4" id="c1-featured" aria-labelledby="c1-feat">
      <div class="cluster" data-justify="between"><h2 class="shop-h2" id="c1-feat">Featured</h2><a href="#" class="btn" data-variant="link" data-size="sm">View all 425{si("arrow-right")}</a></div>
      <div class="shop-cards">{"".join(card(p) for p in [ITEMS[6], ITEMS[3], ITEMS[2], ITEMS[5]])}</div>
    </section>
    <section class="shop-promo-split" aria-labelledby="c1-promo">
      <div class="stack" data-gap="3" data-align="start">
        <span class="badge">Members</span>
        <h2 id="c1-promo">15% off textiles this week</h2>
        <p>Throws, pillows and table linen in seasonal colors. Join free to unlock the price.</p>
        <a href="#" class="btn">Join and save</a>
      </div>
      {shot(2)}
    </section>
    <section class="stack shop-seo" data-gap="4" aria-labelledby="c1-faq">
      <h2 class="shop-h2" id="c1-faq">About Home &amp; Living</h2>
      <div class="accordion">
        <details><summary>How do I care for linen?</summary><section><p class="shop-lead">Wash at 40°C, line dry and iron while slightly damp. Linen softens with every wash.</p></section></details>
        <details><summary>Do you deliver furniture?</summary><section><p class="shop-lead">Large items ship with a two-person crew to the room of your choice, free over $500.</p></section></details>
        <details><summary>Can I return home items?</summary><section><p class="shop-lead">Yes, unused items within 30 days. Textiles must be in their original packaging.</p></section></details>
      </div>
    </section>
  </div>
</main>
""", CATP, scripts=script(WISH_JS))

add("category-02", "Category 02", "Shop by category: a bento grid of image tiles with hover zoom and an arrow that slides in.", "category", f"""
{store_header(3)}
<main class="wrapper shop-page">
  <div class="stack" data-gap="6">
    <div class="cluster" data-justify="between" data-align="end" data-gap="4">
      <div class="stack" data-gap="1">
        <h1 class="shop-h1">Shop by category</h1>
        <p class="shop-lead">Eight departments, one considered collection.</p>
      </div>
      <a href="#" class="btn" data-variant="outline">All products</a>
    </div>
    <div class="shop-bento">
      {tile("New in", "128 products", 1, "big")}
      {tile("Apparel", "212 products", 2, "tall")}
      {tile("Bags", "46 products", 3)}
      {tile("Kitchen", "93 products", 4)}
      {tile("Home", "155 products", 3, "wide")}
      {tile("Accessories", "71 products", 2)}
      {tile("Sale", "Up to 40% off", 4)}
    </div>
  </div>
</main>
""", CATP)

TREE = [
    ("Apparel", True, [("Sweaters", 18, True), ("T-shirts", 24, False), ("Outerwear", 12, False), ("Scarves", 7, False)]),
    ("Home", False, [("Pillows", 21, False), ("Throws", 14, False), ("Lighting", 39, False)]),
    ("Kitchen", False, [("Mugs", 16, False), ("Bowls", 11, False), ("Coffee", 9, False)]),
]
tree = "".join(f"""<li><details{" open" if open_ else ""}><summary>{si("chevron-right")}{name}</summary><ul>{"".join(f'<li><a href="#"{" aria-current=\"page\"" if cur else ""}>{n}<span>{c}</span></a></li>' for n, c, cur in kids)}</ul></details></li>""" for name, open_, kids in TREE)
c3_items = SHOP_ITEMS * 2
c3_cards = "".join(card(p).replace('<article class="shop-card">', '<article class="shop-card" data-more hidden>' if i >= 8 else '<article class="shop-card">', 1) for i, p in enumerate(c3_items))
MORE_JS = """
document.querySelectorAll('[data-load-more]').forEach((btn) => {
  const grid = document.getElementById(btn.dataset.loadMore);
  const total = grid.children.length;
  const sync = () => {
    const shown = grid.querySelectorAll(':scope > :not([hidden])').length;
    btn.closest('.shop-more').querySelector('[data-shown]').textContent = `Showing ${shown} of ${total}`;
    const bar = btn.closest('.shop-more').querySelector('.progress');
    bar.setAttribute('aria-valuenow', Math.round(shown / total * 100));
    bar.querySelector('span').style.width = (shown / total * 100) + '%';
    btn.hidden = shown >= total;
  };
  btn.addEventListener('click', () => {
    const next = [...grid.querySelectorAll(':scope > [hidden]')].slice(0, 4);
    next.forEach((c) => { c.hidden = false; });
    next[0]?.querySelector('a')?.focus({ preventScroll: true });
    sync();
  });
});
"""
pills = "".join(f'<a href="#"{" aria-current=\"page\"" if i == 0 else ""}>{t}</a>' for i, t in enumerate(["Sweaters", "Cardigans", "Crew neck", "V-neck", "Merino", "Cashmere", "Cotton"]))
add("category-03", "Category 03", "A category listing: subcategory tree, pills, sort and a load-more button with progress.", "category", f"""
{store_header(3)}
<main class="wrapper shop-page">
  <div class="stack" data-gap="6">
    <nav class="breadcrumb shop-crumbs" aria-label="Breadcrumb"><ol><li><a href="#">Home</a></li>{crumb_sep}<li><a href="#">Apparel</a></li>{crumb_sep}<li><span aria-current="page">Sweaters</span></li></ol></nav>
    <div class="stack" data-gap="2">
      <h1 class="shop-h1">Sweaters</h1>
      <p class="shop-lead">Merino, cashmere and cotton knits for cool days. {len(c3_items)} products.</p>
    </div>
    <div class="shop-results">
      <nav class="shop-tree shop-filters-panel" aria-label="Categories"><ul>{tree}</ul></nav>
      <div class="stack" data-gap="5">
        <div class="shop-toolbar">
          <nav class="shop-pills" aria-label="Sweater types">{pills}</nav>
          <div class="cluster" data-gap="2">
            <label class="sr-only" for="c3-sort">Sort by</label>
            <select class="select" id="c3-sort">{SORT}</select>
          </div>
        </div>
        <div class="shop-cards" id="c3-grid">{c3_cards}</div>
        <div class="shop-more">
          <p data-shown>Showing 8 of {len(c3_items)}</p>
          <div class="progress" role="progressbar" aria-label="Products shown" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{round(8 / len(c3_items) * 100)}"><span style="width: {8 / len(c3_items) * 100:.4f}%"></span></div>
          <button type="button" class="btn" data-variant="outline" data-load-more="c3-grid">Load more</button>
        </div>
      </div>
    </div>
  </div>
</main>
""", CATP + "\n  .shop-toolbar { flex-wrap: nowrap; }\n  .shop-pills { min-inline-size: 0; }\n  .shop-pills a { display: inline-block; }\n  @media (width < 56rem) { .shop-tree { display: none; } }", scripts=script(MORE_JS + WISH_JS))



# ================================================================== checkout success and order tracking
SUCCESS_CSS = """
  .shop-done { display: grid; justify-items: center; gap: 1rem; text-align: center; }
  .shop-done h1 { margin: 0; font-size: clamp(1.75rem, 4vw, 2.25rem); font-weight: 600; letter-spacing: -0.025em; text-wrap: balance; }
  .shop-done p { margin: 0; color: var(--muted-foreground); max-inline-size: 32rem; text-wrap: pretty; }
  .shop-check-anim { inline-size: 4.5rem; block-size: 4.5rem; color: var(--primary); }
  .shop-check-anim circle { fill: color-mix(in oklab, var(--primary) 12%, transparent); stroke: currentColor; stroke-width: 2; }
  .shop-check-anim path { fill: none; stroke: currentColor; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 30; stroke-dashoffset: 0; animation: shop-draw 500ms ease-out 150ms backwards; }
  .shop-check-anim circle { animation: shop-pop-in 350ms cubic-bezier(0.34, 1.56, 0.64, 1) backwards; transform-origin: center; }
  @keyframes shop-draw { from { stroke-dashoffset: 30; } }
  @keyframes shop-pop-in { from { transform: scale(0.6); opacity: 0; } }
  .shop-confetti { position: absolute; inset: 0; overflow: hidden; pointer-events: none; }
  .shop-confetti > i { position: absolute; inset-block-start: -1rem; inline-size: 0.5rem; block-size: 0.875rem; border-radius: 2px; opacity: 0; animation: shop-fall 1600ms ease-in forwards; }
  @keyframes shop-fall { 0% { opacity: 1; transform: translateY(0) rotate(0); } 100% { opacity: 0; transform: translateY(18rem) rotate(540deg); } }
  @media (prefers-reduced-motion: reduce) { .shop-confetti { display: none; } }
  @media (prefers-reduced-motion: reduce) { .shop-check-anim path { animation: none; } }
  @media (prefers-reduced-motion: reduce) { .shop-check-anim circle { animation: none; } }
  .shop-order-no { display: inline-flex; align-items: center; gap: 0.25rem; padding: 0.25rem 0.25rem 0.25rem 0.75rem; border: 1px dashed var(--border); border-radius: 999px; font-family: var(--font-mono, ui-monospace, monospace); font-size: 0.875rem; }
  .shop-copy svg + svg { display: none; }
  .shop-copy[data-copied] svg { display: none; }
  .shop-copy[data-copied] svg + svg { display: block; color: var(--primary); }
  .shop-success-wrap { position: relative; padding-block: 3rem 2rem; }
  .shop-thumbs { display: flex; }
  .shop-thumbs > img { inline-size: 3rem; block-size: 3rem; border: 2px solid var(--card); border-radius: calc(var(--radius) - 2px); object-fit: cover; background: var(--muted); }
  .shop-thumbs > img + img { margin-inline-start: -0.75rem; }
  html.dark .shop-thumbs > img { filter: brightness(0.5) grayscale(1); }
  .shop-split-2 { display: grid; gap: 1.5rem; }
  @media (width >= 48rem) { .shop-split-2 { grid-template-columns: 1fr 1fr; } }
  .shop-refer { display: grid; gap: 1rem; padding: 1.5rem; border-radius: calc(var(--radius) + 4px); background: var(--primary); color: var(--primary-foreground); }
  .shop-refer h2 { margin: 0; font-size: 1.125rem; font-weight: 600; }
  .shop-refer p { margin: 0; opacity: 0.85; font-size: 0.875rem; }
  .shop-refer .input-group { background: var(--background); color: var(--foreground); border-radius: var(--radius); }
  .shop-mini-steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; list-style: none; margin: 0; padding: 0; font-size: 0.75rem; text-align: center; color: var(--muted-foreground); }
  .shop-mini-steps > li { display: grid; gap: 0.375rem; }
  .shop-mini-steps > li::before { content: ''; block-size: 4px; border-radius: 4px; background: var(--border); }
  .shop-mini-steps > li[data-done]::before { background: var(--primary); }
  .shop-mini-steps > li[data-done] { color: var(--foreground); font-weight: 500; }
  .shop-receipt { display: grid; gap: 0.625rem; margin: 0; font-size: 0.875rem; }
  .shop-receipt > div { display: flex; justify-content: space-between; gap: 1rem; }
  .shop-receipt dt { color: var(--muted-foreground); }
  .shop-receipt dd { margin: 0; font-variant-numeric: tabular-nums; text-align: end; }
  .shop-receipt hr { margin: 0.25rem 0; border: 0; border-block-start: 1px dashed var(--border); }
  .shop-lookup { display: grid; gap: 2rem; max-inline-size: 40rem; margin-inline: auto; }
  .shop-lookup-form { display: grid; gap: 1rem; }
  @media (width >= 40rem) { .shop-lookup-form { grid-template-columns: 1fr 1fr auto; align-items: end; } }
  .shop-lookup-form .field { margin: 0; }
  .shop-error { display: flex; align-items: center; gap: 0.5rem; margin: 0; font-size: 0.875rem; color: var(--destructive); }
  .shop-error svg { inline-size: 1rem; block-size: 1rem; }
  .shop-error[hidden] { display: none; }
  .shop-result[hidden] { display: none; }
  .shop-status-hero { display: flex; align-items: center; gap: 1rem; }
  .shop-status-icon { display: inline-flex; align-items: center; justify-content: center; flex: none; inline-size: 3rem; block-size: 3rem; border-radius: 999px; background: color-mix(in oklab, var(--primary) 12%, transparent); color: var(--primary); }
  .shop-status-icon svg { inline-size: 1.5rem; block-size: 1.5rem; }
  .shop-status-hero h2 { margin: 0; font-size: 1.25rem; font-weight: 600; }
  .shop-status-hero p { margin: 0; font-size: 0.875rem; color: var(--muted-foreground); }
  .shop-map { position: relative; overflow: hidden; border-radius: var(--radius); background: color-mix(in oklab, var(--muted) 70%, var(--background)); aspect-ratio: 16 / 9; }
  .shop-map > svg { position: absolute; inset: 0; inline-size: 100%; block-size: 100%; }
  .shop-map .shop-map-grid { stroke: var(--border); stroke-width: 1; }
  .shop-map .shop-map-road { fill: none; stroke: var(--card); stroke-width: 10; stroke-linecap: round; }
  .shop-map .shop-map-route { fill: none; stroke: var(--primary); stroke-width: 4; stroke-linecap: round; stroke-dasharray: 2 10; }
  .shop-map .shop-map-done { fill: none; stroke: var(--primary); stroke-width: 4; stroke-linecap: round; }
  .shop-map-pin { position: absolute; display: inline-flex; align-items: center; justify-content: center; inline-size: 2.25rem; block-size: 2.25rem; translate: -50% -50%; border-radius: 999px; background: var(--primary); color: var(--primary-foreground); box-shadow: 0 0 0 6px color-mix(in oklab, var(--primary) 20%, transparent); }
  .shop-map-pin svg { inline-size: 1.125rem; block-size: 1.125rem; }
  .shop-map-pin[data-kind='home'] { background: var(--background); color: var(--foreground); box-shadow: 0 0 0 1px var(--border), 0 4px 12px -4px rgb(0 0 0 / 0.3); }
  .shop-map-eta { position: absolute; inset-block-start: 0.75rem; inset-inline-start: 0.75rem; display: grid; padding: 0.5rem 0.75rem; border-radius: var(--radius); background: var(--background); box-shadow: 0 4px 12px -4px rgb(0 0 0 / 0.25); font-size: 0.75rem; }
  .shop-map-eta strong { font-size: 0.9375rem; }
  .shop-courier { display: flex; align-items: center; gap: 0.75rem; }
  .shop-courier > div { flex: 1; min-inline-size: 0; }
  .shop-courier p { margin: 0; font-size: 0.875rem; }
  .shop-courier small { display: block; color: var(--muted-foreground); font-size: 0.75rem; }
  .shop-vsteps { list-style: none; margin: 0; padding: 0; display: grid; }
  .shop-vsteps > li { position: relative; display: grid; grid-template-columns: 1.75rem 1fr; gap: 0 0.875rem; padding-block-end: 1.5rem; }
  .shop-vsteps > li:last-child { padding-block-end: 0; }
  .shop-vsteps > li::before { content: ''; position: absolute; inset-inline-start: calc(0.875rem - 1px); inset-block: 1.75rem 0; inline-size: 2px; background: var(--border); }
  .shop-vsteps > li:last-child::before { display: none; }
  .shop-vsteps > li[data-done]::before { background: var(--primary); }
  .shop-vsteps .shop-tracker-dot { grid-row: span 2; }
  .shop-vsteps > li[data-done] .shop-tracker-dot { border-color: var(--primary); background: var(--primary); color: var(--primary-foreground); }
  .shop-vsteps > li[aria-current] .shop-tracker-dot { border-color: var(--primary); color: var(--primary); }
  .shop-vsteps p { margin: 0; font-size: 0.875rem; font-weight: 500; }
  .shop-vsteps > li:not([data-done]):not([aria-current]) p { color: var(--muted-foreground); font-weight: 400; }
  .shop-vsteps small { color: var(--muted-foreground); font-size: 0.75rem; }
  .shop-pkg-head { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 0.75rem; }
"""
TRACK_CSS = CAT_CSS + SUCCESS_CSS


def copy_btn(target, label):
    return (f'<button type="button" class="btn shop-copy" data-variant="ghost" data-size="icon-xs" data-copy="{target}" aria-label="{label}" data-copied-label="Copied">'
            f'{si("copy")}{si("check")}</button>')


CONFETTI_COLORS = ["var(--primary)", "var(--chart-1, #f97316)", "var(--chart-2, #14b8a6)", "var(--chart-3, #6366f1)", "var(--chart-4, #eab308)", "var(--chart-5, #ec4899)"]
confetti = "".join(
    f'<i style="inset-inline-start: {(i * 37) % 100}%; background: {CONFETTI_COLORS[i % 6]}; animation-delay: {(i * 53) % 400}ms"></i>'
    for i in range(24))
CHECK_SVG = '<svg class="shop-check-anim" viewBox="0 0 52 52" aria-hidden="true"><circle cx="26" cy="26" r="24"/><path d="M15 27l7 7 15-15"/></svg>'
total = totals(PRODUCTS)[3]

add("checkout-04", "Checkout 04", "A celebratory order success page: animated check, order number to copy, delivery estimate, account creation and a referral.", "checkout", f"""
{store_header(0)}
<main class="wrapper shop-page" data-size="md">
  <div class="stack" data-gap="8">
    <section class="shop-success-wrap" aria-labelledby="co4-title">
      <div class="shop-confetti" aria-hidden="true">{confetti}</div>
      <div class="shop-done">
        {CHECK_SVG}
        <h1 id="co4-title">Order confirmed!</h1>
        <p>Thanks, Olivia. We've emailed your receipt to olivia@example.com and we'll let you know when it ships.</p>
        <div class="shop-order-no"><span>Order</span><span id="co4-no">#A-10294</span>{copy_btn("#co4-no", "Copy order number")}</div>
      </div>
    </section>
    <div class="shop-split-2">
      <section class="card" aria-labelledby="co4-arrive">
        <header>
          <h2 id="co4-arrive">Arriving Thu, Nov 12</h2>
          <p>Standard delivery to 1234 Market Street, San Francisco</p>
        </header>
        <section class="stack" data-gap="4">
          <ol class="shop-mini-steps" aria-label="Order progress"><li data-done>Confirmed</li><li>Shipped</li><li>Delivered</li></ol>
          <div class="cluster" data-justify="between" data-gap="3">
            <div class="shop-thumbs">{"".join(f'<img src="{PH}" alt="">' for _ in PRODUCTS)}</div>
            <p class="shop-row"><span class="shop-muted">{count(PRODUCTS)} items ·</span><strong>{money(total)}</strong></p>
          </div>
        </section>
        <footer class="cluster" data-gap="2">
          <a href="#" class="btn" data-size="sm">{si("package")}Track order</a>
          <button type="button" class="btn" data-variant="outline" data-size="sm">{si("download")}Receipt</button>
        </footer>
      </section>
      <form class="card" onsubmit="event.preventDefault()" aria-labelledby="co4-account">
        <header>
          <h2 id="co4-account">Save your details</h2>
          <p>Set a password to track orders and check out faster next time.</p>
        </header>
        <section class="stack" data-gap="3">
          <div role="group" class="field"><label for="co4-email">Email</label><input id="co4-email" type="email" value="olivia@example.com" readonly></div>
          <div role="group" class="field"><label for="co4-pass">Password</label><input id="co4-pass" type="password" autocomplete="new-password" minlength="8" required></div>
        </section>
        <footer><button type="submit" class="btn shop-full">Create account</button></footer>
      </form>
    </div>
    <section class="shop-refer" aria-labelledby="co4-refer">
      <div class="stack" data-gap="1">
        <h2 id="co4-refer">Give $10, get $10</h2>
        <p>Share your link: friends get $10 off their first order and you get $10 when they buy.</p>
      </div>
      <div class="input-group">
        <input type="text" id="co4-link" value="acme.store/r/olivia-m" readonly aria-label="Referral link">
        <span data-align="end">{copy_btn("#co4-link", "Copy referral link").replace('data-copy="#co4-link"', 'data-copy-text="https://acme.store/r/olivia-m"')}</span>
      </div>
    </section>
    <div class="cluster" data-justify="center" data-gap="2">
      <a href="#" class="btn" data-variant="outline">Continue shopping</a>
    </div>
  </div>
</main>
""", TRACK_CSS)

add("checkout-05", "Checkout 05", "A mobile order success screen with a receipt and next steps.", "checkout", f"""
<div class="shop-app">
  <header class="shop-app-bar">
    <a href="#" class="btn" data-variant="ghost" data-size="icon" aria-label="Close">{si("x")}</a>
    <h1>Order placed</h1>
  </header>
  <div class="shop-app-body">
    <section class="shop-done shop-success-wrap" aria-labelledby="co5-title">
      {CHECK_SVG}
      <h1 id="co5-title">Payment successful</h1>
      <p>Order #A-10294 · Nov 7, 2026, 3:47 PM</p>
    </section>
    <ol class="shop-mini-steps" aria-label="Order progress"><li data-done>Paid</li><li>Packed</li><li>On its way</li></ol>
    <section class="card" aria-labelledby="co5-receipt">
      <header><h2 id="co5-receipt">Receipt</h2></header>
      <section>
        <dl class="shop-receipt">
          {"".join(f'<div><dt>{p["name"]} × {p["qty"]}</dt><dd>{money(p["price"] * p["qty"])}</dd></div>' for p in PRODUCTS)}
          <hr>
          <div><dt>Subtotal</dt><dd>{money(totals(PRODUCTS)[0])}</dd></div>
          <div><dt>Shipping</dt><dd>Free</dd></div>
          <div><dt>Tax</dt><dd>{money(totals(PRODUCTS)[2])}</dd></div>
          <hr>
          <div><dt><strong>Paid with Visa •••• 4242</strong></dt><dd><strong>{money(total)}</strong></dd></div>
        </dl>
      </section>
    </section>
    <ul class="shop-perks">
      <li>{si("mail")}<span>Receipt sent to olivia@example.com</span></li>
      <li>{si("truck")}<span>Estimated delivery Thu, Nov 12</span></li>
    </ul>
    <div class="stack" data-gap="2">
      <a href="#" class="btn shop-full" data-size="lg">{si("package")}Track order</a>
      <a href="#" class="btn shop-full" data-variant="ghost">Back to shop</a>
    </div>
  </div>
</div>
""", APP_CSS + CATALOG_CSS + SUCCESS_CSS + "\n  .shop-app { padding-block-end: 2rem; }\n  .shop-success-wrap { padding-block: 1.5rem 0.5rem; }")


# ---------------------------------------------------------------- tracking
def vsteps(steps):
    out = []
    for title, when, state, ic_ in steps:
        attr = " data-done" if state == "done" else ' aria-current="step"' if state == "now" else ""
        dot = si("check") if state == "done" else si(ic_)
        out.append(f'<li{attr}><span class="shop-tracker-dot">{dot}</span><p>{title}</p><small>{when}</small></li>')
    return '<ol class="shop-vsteps">' + "".join(out) + "</ol>"


STEPS_A = [("Order placed", "Nov 7, 3:47 PM", "done", ""), ("Packed", "Nov 8, 9:12 AM", "done", ""), ("Shipped with UPS", "Nov 8, 4:30 PM", "done", ""), ("Out for delivery", "Today, 8:12 AM", "now", "truck"), ("Delivered", "Estimated today, 2–5 PM", "todo", "house")]

LOOKUP_JS = """
document.querySelectorAll('[data-lookup]').forEach((form) => {
  const err = form.querySelector('[data-lookup-error]');
  const result = document.getElementById(form.dataset.lookup);
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const no = form.elements.order.value.trim().replace(/^#/, '').toUpperCase();
    const ok = /^A-\\d{5}$/.test(no) && form.elements.email.value.includes('@');
    err.hidden = ok;
    result.hidden = !ok;
    form.elements.order.toggleAttribute('aria-invalid', !ok);
    if (ok) {
      result.querySelector('[data-lookup-no]').textContent = '#' + no;
      result.querySelector('h2').focus();
    }
  });
});
"""
add("tracking-01", "Tracking 01", "Track an order without an account: order number and email lookup, validation, then the delivery status.", "tracking", f"""
{store_header(0)}
<main class="wrapper shop-page">
  <div class="shop-lookup">
    <div class="stack" data-gap="2">
      <h1 class="shop-h1">Track your order</h1>
      <p class="shop-lead">Enter the order number from your confirmation email. Try <strong>A-10251</strong> with any email.</p>
    </div>
    <form class="card" data-lookup="t1-result" novalidate>
      <section class="stack" data-gap="3">
        <div class="shop-lookup-form">
          <div role="group" class="field"><label for="t1-order">Order number</label><input id="t1-order" name="order" type="text" placeholder="A-10251" autocomplete="off" aria-describedby="t1-error"></div>
          <div role="group" class="field"><label for="t1-email">Email</label><input id="t1-email" name="email" type="email" placeholder="you@example.com" autocomplete="email"></div>
          <button type="submit" class="btn">{si("search")}Track</button>
        </div>
        <p class="shop-error" id="t1-error" data-lookup-error hidden>{si("info")}We couldn't find that order. Check the number (like A-10251) and the email.</p>
      </section>
    </form>
    <section class="card shop-result" id="t1-result" aria-live="polite" hidden>
      <header>
        <div class="shop-status-hero">
          <span class="shop-status-icon">{si("truck")}</span>
          <div><h2 tabindex="-1">Out for delivery</h2><p>Order <span data-lookup-no>#A-10251</span> · arriving today, 2–5 PM</p></div>
        </div>
      </header>
      <section class="stack" data-gap="6">
        <ol class="shop-tracker" aria-label="Delivery progress">{tracker}</ol>
        {vsteps(STEPS_A)}
      </section>
      <footer class="cluster" data-gap="2">
        <a href="#" class="btn" data-variant="outline" data-size="sm">Track on UPS</a>
        <a href="#" class="btn" data-variant="ghost" data-size="sm">{si("mail")}Contact support</a>
      </footer>
    </section>
  </div>
</main>
""", TRACK_CSS + "\n  .shop-result h2:focus { outline: none; }", scripts=script(LOOKUP_JS))

MAP = """<svg viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <g class="shop-map-grid">""" + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="180"/>' for x in range(0, 321, 40)) + "".join(f'<line x1="0" y1="{y}" x2="320" y2="{y}"/>' for y in range(0, 181, 40)) + """</g>
  <path class="shop-map-road" d="M30 150 C 80 150, 90 90, 140 90 S 210 40, 290 40"/>
  <path class="shop-map-done" d="M30 150 C 80 150, 90 90, 140 90"/>
  <path class="shop-map-route" d="M140 90 C 175 90, 210 40, 290 40"/>
</svg>"""

DRIVER_JS = """
document.querySelectorAll('[data-instructions]').forEach((form) => {
  const out = document.getElementById(form.dataset.instructions);
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const v = form.elements.note.value.trim();
    out.textContent = v || 'No instructions yet.';
    form.closest('dialog').close();
  });
});
"""
add("tracking-02", "Tracking 02", "Live delivery tracking: route map, arrival window, courier contact, delivery instructions and history.", "tracking", account("Orders", f"""
<div class="stack" data-gap="4">
  <a href="#" class="btn shop-back" data-variant="ghost" data-size="sm">{si("arrow-left")}Order #A-10251</a>
  <div class="shop-status-hero">
    <span class="shop-status-icon">{si("truck")}</span>
    <div><h1 class="shop-h2">Arriving today, 2:15–2:45 PM</h1><p>Out for delivery · 6 stops away</p></div>
  </div>
</div>
<section class="card" aria-label="Delivery map">
  <section class="stack" data-gap="4">
    <div class="shop-map">
      {MAP}
      <span class="shop-map-pin" style="inset-inline-start: 43.75%; inset-block-start: 50%" title="Courier">{si("truck")}</span>
      <span class="shop-map-pin" data-kind="home" style="inset-inline-start: 90.6%; inset-block-start: 22.2%" title="Your address">{si("house")}</span>
      <div class="shop-map-eta"><span class="shop-muted">Estimated arrival</span><strong>2:15–2:45 PM</strong></div>
    </div>
    <div class="shop-courier">
      <span class="avatar"><img src="{PH}" alt=""><span>DR</span></span>
      <div><p>Daniel R. · UPS</p><small>Tracking 1Z 999 AA1 0123 4567 84</small></div>
      <a href="#" class="btn" data-variant="outline" data-size="icon" aria-label="Call the courier">{si("phone")}</a>
      <a href="#" class="btn" data-variant="outline" data-size="icon" aria-label="Message the courier">{si("mail")}</a>
    </div>
  </section>
</section>
<div class="shop-cols shop-cols-even">
  <section class="card" aria-labelledby="t2-history">
    <header><h2 id="t2-history">Tracking history</h2></header>
    <section><ol class="shop-timeline" aria-label="Tracking history">{events}</ol></section>
  </section>
  <div class="stack" data-gap="6">
    <section class="card" aria-labelledby="t2-instr">
      <header>
        <h2 id="t2-instr">Delivery instructions</h2>
        <div class="card-action"><button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Edit delivery instructions" commandfor="t2-dialog" command="show-modal">{si("pencil")}</button></div>
      </header>
      <section><p class="shop-lead" id="t2-note">Leave at the front desk if no one answers.</p></section>
    </section>
    <section class="card" aria-labelledby="t2-items">
      <header><h2 id="t2-items">In this package</h2></header>
      <section><ul class="shop-lines" data-size="sm">{order_lines_sm(PRODUCTS[:2])}</ul></section>
    </section>
  </div>
</div>
<dialog id="t2-dialog" class="dialog" closedby="any" aria-labelledby="t2-dialog-title">
  <div>
    <header>
      <h2 id="t2-dialog-title">Delivery instructions</h2>
      <p>Tell the courier where to leave your package.</p>
    </header>
    <section>
      <form id="t2-form" data-instructions="t2-note" class="stack" data-gap="2">
        <label class="label" for="t2-text">Instructions</label>
        <input class="input" id="t2-text" name="note" type="text" value="Leave at the front desk if no one answers.">
      </form>
    </section>
    <footer>
      <button type="button" class="btn" data-variant="outline" commandfor="t2-dialog" command="close">Cancel</button>
      <button type="submit" form="t2-form" class="btn">Save</button>
    </footer>
    <button type="button" aria-label="Close" commandfor="t2-dialog" command="close">{si("x")}</button>
  </div>
</dialog>
"""), TRACK_CSS + """
  @media (width >= 56rem) { .shop-cols.shop-cols-even { grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr); } }
  .shop-back { align-self: flex-start; margin-inline-start: -0.5rem; }
  .shop-profile .avatar { inline-size: 2.25rem; block-size: 2.25rem; }
  .shop-courier .avatar { inline-size: 2.5rem; block-size: 2.5rem; }""", scripts=script(DRIVER_JS))

PKGS = [
    ("1", "UPS · 1Z 999 AA1 0123 4567 84", "Out for delivery", [PRODUCTS[0], PRODUCTS[1]], STEPS_A),
    ("2", "USPS · 9400 1000 0000 0000 0000 00", "Preparing to ship", [PRODUCTS[2]], [("Order placed", "Nov 7, 3:47 PM", "done", ""), ("Packed", "Today, 10:05 AM", "now", "package"), ("Shipped", "Expected Nov 9", "todo", "truck"), ("Delivered", "Estimated Nov 13", "todo", "house")]),
]
tabs = "".join(f'<button type="button" role="tab" id="t3-tab-{n}" aria-controls="t3-panel-{n}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">Package {n} <span class="badge" data-variant="{"secondary" if i == 0 else "outline"}">{st}</span></button>' for i, (n, c, st, its, steps) in enumerate(PKGS))
panels = "".join(f"""<div role="tabpanel" id="t3-panel-{n}" aria-labelledby="t3-tab-{n}" tabindex="-1"{" hidden" if i else ""}>
  <div class="shop-split-2">
    <section class="card" aria-label="Package {n} progress">
      <header class="shop-pkg-head">
        <div class="stack" data-gap="1"><h2>{st}</h2><p class="shop-line-meta"><span id="t3-no-{n}">{c}</span></p></div>
        {copy_btn(f"#t3-no-{n}", f"Copy tracking number for package {n}")}
      </header>
      <section>{vsteps(steps)}</section>
    </section>
    <section class="card" aria-label="Package {n} items">
      <header><h2>{len(its)} {"item" if len(its) == 1 else "items"}</h2></header>
      <section><ul class="shop-lines" data-size="sm">{order_lines_sm(its)}</ul></section>
    </section>
  </div>
</div>""" for i, (n, c, st, its, steps) in enumerate(PKGS))
notify = "".join(f'''<div class="shop-switch-row"><label for="t3-n{i}"><span class="shop-switch-title">{t}</span><small>{d}</small></label><input type="checkbox" role="switch" class="input" id="t3-n{i}"{" checked" if on else ""}></div>''' for i, (t, d, on) in enumerate([
    ("Email updates", "olivia@example.com", True),
    ("Text messages", "+1 (555) 010-2048", False),
    ("Delivery day reminder", "A heads-up on the morning of delivery", True),
]))
add("tracking-03", "Tracking 03", "An order shipped in two packages: tabs per package, carrier, copyable tracking numbers, steps and notifications.", "tracking", account("Orders", f"""
<div class="stack" data-gap="1">
  <div class="cluster" data-gap="3"><h1 class="shop-h1">Order #A-10294</h1>{status_badge("shipped", "Partly shipped")}</div>
  <p class="shop-lead">Placed Nov 7, 2026 · shipping in 2 packages</p>
</div>
<div class="tabs" id="t3-tabs">
  <nav role="tablist" aria-orientation="horizontal">{tabs}</nav>
  {panels}
</div>
<section class="card" aria-labelledby="t3-notify">
  <header>
    <h2 id="t3-notify">Shipping notifications</h2>
    <p>Choose how we tell you about these packages.</p>
  </header>
  <section class="stack" data-gap="4">{notify}</section>
</section>
"""), TRACK_CSS + """
  .shop-profile .avatar { inline-size: 2.25rem; block-size: 2.25rem; }
  .shop-switch-row > label { flex: 1; cursor: pointer; }
  .shop-switch-title { font-size: 0.875rem; font-weight: 500; }
  .shop-switch-row small { display: block; font-size: 0.8125rem; color: var(--muted-foreground); }
  .shop-pkg-head h2 { margin: 0; font-size: 1rem; font-weight: 600; }
  .tabs [role='tab'] .badge { margin-inline-start: 0.375rem; }""")



# ================================================================== reviews
REVIEW_CSS = """
  .shop-rv { display: grid; gap: 2rem; align-items: start; }
  @media (width >= 56rem) { .shop-rv { grid-template-columns: 18rem minmax(0, 1fr); gap: 3rem; } .shop-rv-aside { position: sticky; inset-block-start: 5.5rem; } }
  .shop-rv-score { display: flex; align-items: center; gap: 1rem; }
  .shop-rv-score strong { font-size: 3rem; font-weight: 600; line-height: 1; letter-spacing: -0.03em; font-variant-numeric: tabular-nums; }
  .shop-rv-bars { display: grid; gap: 0.25rem; margin: 0; padding: 0; list-style: none; }
  .shop-rv-bars button { display: grid; grid-template-columns: 2.5rem minmax(0, 1fr) 2.25rem; align-items: center; gap: 0.5rem; inline-size: 100%; padding: 0.25rem 0.375rem; border: 0; border-radius: calc(var(--radius) - 4px); background: none; color: inherit; font: inherit; font-size: 0.8125rem; text-align: start; cursor: pointer; }
  .shop-rv-bars button:hover { background: var(--accent); }
  .shop-rv-bars button[aria-pressed='true'] { background: var(--muted); font-weight: 600; }
  .shop-rv-bars button:focus-visible { outline: 2px solid var(--ring); outline-offset: 1px; }
  .shop-rv-bars button > span:first-child { display: inline-flex; align-items: center; gap: 0.25rem; }
  .shop-rv-bars button > span:last-child { text-align: end; color: var(--muted-foreground); font-variant-numeric: tabular-nums; }
  .shop-rv-bars .progress { block-size: 0.5rem; }
  .shop-rv-attrs { display: grid; gap: 0.875rem; margin: 0; }
  .shop-rv-attrs > div { display: grid; gap: 0.375rem; font-size: 0.8125rem; }
  .shop-rv-attrs dt { display: flex; justify-content: space-between; color: var(--muted-foreground); }
  .shop-rv-attrs dd { margin: 0; }
  .shop-rv-scale { position: relative; block-size: 0.375rem; border-radius: 999px; background: var(--muted); }
  .shop-rv-scale > span { position: absolute; inset-block-start: 50%; inline-size: 0.875rem; block-size: 0.875rem; translate: -50% -50%; border-radius: 999px; background: var(--primary); box-shadow: 0 0 0 2px var(--background); corner-shape: round; }
  .shop-rv-scale-labels { display: flex; justify-content: space-between; font-size: 0.6875rem; color: var(--muted-foreground); }
  .shop-rv-list { display: grid; margin: 0; padding: 0; list-style: none; }
  .shop-rv-list > li { display: grid; gap: 0.75rem; padding-block: 1.5rem; border-block-end: 1px solid var(--border); }
  .shop-rv-list > li:first-child { padding-block-start: 0; }
  .shop-rv-head { display: flex; align-items: flex-start; gap: 0.75rem; }
  .shop-rv-head > div { flex: 1; min-inline-size: 0; display: grid; gap: 0.125rem; }
  .shop-rv-head p { margin: 0; font-size: 0.875rem; font-weight: 500; }
  .shop-rv-head small { color: var(--muted-foreground); font-size: 0.75rem; }
  .shop-rv-verified { display: inline-flex; align-items: center; gap: 0.25rem; color: var(--primary); font-size: 0.75rem; }
  .shop-rv-verified svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .shop-rv-list h3 { margin: 0; font-size: 0.9375rem; font-weight: 600; }
  .shop-rv-list p { margin: 0; font-size: 0.875rem; line-height: 1.6; }
  .shop-rv-meta { display: flex; flex-wrap: wrap; gap: 0.5rem 1rem; font-size: 0.75rem; color: var(--muted-foreground); }
  .shop-rv-meta strong { color: var(--foreground); font-weight: 500; }
  .shop-rv-photos { display: flex; gap: 0.5rem; }
  .shop-rv-photos img { inline-size: 4rem; block-size: 4rem; border-radius: calc(var(--radius) - 2px); object-fit: cover; background: var(--muted); }
  .shop-rv-reply { padding: 0.75rem 1rem; border-inline-start: 2px solid var(--primary); border-radius: 0 var(--radius) var(--radius) 0; background: var(--muted); }
  .shop-rv-reply p { font-size: 0.8125rem; }
  .shop-rv-reply strong { display: block; margin-block-end: 0.25rem; font-size: 0.75rem; }
  .shop-rv-help { display: flex; align-items: center; gap: 0.5rem; font-size: 0.8125rem; color: var(--muted-foreground); }
  .shop-rv-help .btn[aria-pressed='true'] { background: var(--primary); border-color: var(--primary); color: var(--primary-foreground); }
  .shop-rv-toolbar { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 0.75rem; padding-block-end: 1rem; border-block-end: 1px solid var(--border); }
  .shop-rv-toolbar .select { inline-size: auto; }
  .shop-rv-toggle { display: inline-flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; }
  .shop-rv-active { display: inline-flex; align-items: center; gap: 0.25rem; }
  .shop-rv-active[hidden] { display: none; }
  .shop-star-input { display: flex; gap: 0.25rem; border: 0; margin: 0; padding: 0; }
  .shop-star-input legend { margin-block-end: 0.5rem; font-size: 0.875rem; font-weight: 500; }
  .shop-star-input label { position: relative; display: inline-flex; padding: 0.125rem; border-radius: calc(var(--radius) - 4px); color: var(--muted-foreground); cursor: pointer; }
  .shop-star-input label svg { inline-size: 2rem; block-size: 2rem; transition: transform 120ms ease, color 120ms ease; }
  .shop-star-input label:hover svg { transform: scale(1.12); }
  .shop-star-input label[data-on] { color: oklch(0.8 0.16 80); }
  .shop-star-input label[data-on] svg { fill: currentColor; }
  .shop-star-input input { position: absolute; opacity: 0; inline-size: 1px; block-size: 1px; }
  .shop-star-input label:has(:focus-visible) { outline: 2px solid var(--ring); outline-offset: 1px; }
  .shop-star-text { margin-block-end: 0.625rem; margin-inline-start: 0.5rem; font-size: 0.875rem; font-weight: 500; }
  .shop-seg { display: grid; grid-template-columns: repeat(3, 1fr); padding: 0.25rem; border-radius: var(--radius); background: var(--muted); }
  .shop-seg label { position: relative; padding: 0.5rem; border-radius: calc(var(--radius) - 4px); font-size: 0.8125rem; text-align: center; cursor: pointer; color: var(--muted-foreground); }
  .shop-seg label:has(:checked) { background: var(--background); color: var(--foreground); font-weight: 500; box-shadow: 0 1px 3px rgb(0 0 0 / 0.1); }
  .shop-seg label:has(:focus-visible) { outline: 2px solid var(--ring); outline-offset: 1px; }
  .shop-seg input { position: absolute; opacity: 0; }
  .shop-seg-wrap { display: grid; gap: 0.5rem; }
  .shop-drop { display: grid; justify-items: center; gap: 0.375rem; padding: 1.5rem; border: 1px dashed var(--border); border-radius: var(--radius); color: var(--muted-foreground); font-size: 0.875rem; text-align: center; cursor: pointer; }
  .shop-drop:hover { border-color: var(--ring); background: var(--accent); }
  .shop-drop[data-over] { border-color: var(--primary); background: color-mix(in oklab, var(--primary) 6%, transparent); }
  .shop-drop:has(:focus-visible) { outline: 2px solid var(--ring); outline-offset: 2px; }
  .shop-drop svg { inline-size: 1.25rem; block-size: 1.25rem; }
  .shop-drop strong { color: var(--foreground); font-weight: 500; }
  .shop-previews { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0; padding: 0; list-style: none; }
  .shop-previews li { position: relative; }
  .shop-previews img { inline-size: 4.5rem; block-size: 4.5rem; border-radius: calc(var(--radius) - 2px); object-fit: cover; }
  .shop-previews button { position: absolute; inset-block-start: -0.375rem; inset-inline-end: -0.375rem; display: inline-flex; align-items: center; justify-content: center; inline-size: 1.25rem; block-size: 1.25rem; padding: 0; border: 0; border-radius: 999px; background: var(--foreground); color: var(--background); cursor: pointer; corner-shape: round; }
  .shop-previews button svg { inline-size: 0.75rem; block-size: 0.75rem; }
  .shop-count-line { display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--muted-foreground); }
  .shop-count-line[data-warn] span:last-child { color: var(--destructive); }
  .shop-rv-done[hidden] { display: none; }
  .shop-tags { display: flex; flex-wrap: wrap; gap: 0.5rem; }
  .shop-tags button { display: inline-flex; align-items: center; gap: 0.375rem; padding: 0.375rem 0.75rem; border: 1px solid var(--border); border-radius: 999px; background: none; color: inherit; font: inherit; font-size: 0.8125rem; cursor: pointer; corner-shape: round; }
  .shop-tags button span { color: var(--muted-foreground); font-size: 0.75rem; }
  .shop-tags button[data-tone='con'] { border-style: dashed; }
  .shop-tags button[aria-pressed='true'] { border-color: var(--primary); background: var(--primary); color: var(--primary-foreground); }
  .shop-tags button[aria-pressed='true'] span { color: inherit; opacity: 0.8; }
  .shop-tags button:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
  .shop-summary-ai { display: grid; gap: 0.75rem; padding: 1.25rem; border: 1px solid var(--border); border-radius: calc(var(--radius) + 4px); background: color-mix(in oklab, var(--muted) 50%, transparent); }
  .shop-summary-ai p { margin: 0; font-size: 0.875rem; line-height: 1.6; }
  .shop-summary-ai h2 { display: flex; align-items: center; gap: 0.5rem; margin: 0; font-size: 1rem; font-weight: 600; }
  .shop-summary-ai h2 svg { inline-size: 1rem; block-size: 1rem; }
  .shop-reel-wrap { display: grid; gap: 1rem; }
  .shop-reel { display: grid; grid-auto-flow: column; grid-auto-columns: min(20rem, 85%); gap: 1rem; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; padding: 1px 1px 0.25rem; }
  .shop-reel > .card { scroll-snap-align: start; }
  .shop-reel > .card[hidden] { display: none; }
  .shop-reel .card p { margin: 0; font-size: 0.875rem; line-height: 1.6; }
  .shop-reel .card mark { background: color-mix(in oklab, var(--primary) 15%, transparent); color: inherit; border-radius: 2px; padding-inline: 0.125rem; }
"""
RV_CSS = CAT_CSS + REVIEW_CSS

RVS = [
    {"name": "Hannah K.", "r": 5, "d": "Oct 30, 2026", "t": "My new everyday sweater", "b": "Soft and warm without being bulky. I wore it all week and it still looks new. True to size, I'm usually a medium.", "size": "M", "fit": "True to size", "help": 24, "photos": 2, "reply": None},
    {"name": "Marcus L.", "r": 5, "d": "Oct 21, 2026", "t": "Second one I've bought", "b": "Still looks new after a winter of wear. The charcoal goes with everything.", "size": "L", "fit": "True to size", "help": 17, "photos": 0, "reply": None},
    {"name": "Priya S.", "r": 4, "d": "Oct 4, 2026", "t": "Lovely color, long sleeves", "b": "The oat color is beautiful in daylight. Slightly longer in the sleeves than I expected, so I fold them once.", "size": "S", "fit": "Runs large", "help": 9, "photos": 1, "reply": "Thanks Priya! Our sleeves run about 2 cm long by design. If you'd like a shorter fit, the Organic Cotton Tee pairs nicely underneath."},
    {"name": "Tom W.", "r": 3, "d": "Sep 18, 2026", "t": "Good, but it pilled a little", "b": "Comfortable and warm. After a month there's some pilling under the arms, which a comb took care of.", "size": "XL", "fit": "True to size", "help": 6, "photos": 0, "reply": "Sorry about that, Tom. Light pilling is normal for fine merino in the first weeks; it settles after a few washes. Reach out if it doesn't."},
    {"name": "Ana R.", "r": 2, "d": "Aug 27, 2026", "t": "Too small for me", "b": "Nice quality, but it fit a size small across the shoulders. The exchange was quick and easy.", "size": "M", "fit": "Runs small", "help": 4, "photos": 0, "reply": None},
]
DIST = [(5, 82, 176), (4, 12, 26), (3, 4, 8), (2, 1, 2), (1, 1, 2)]


def rv_item(v, i):
    photos = f'<div class="shop-rv-photos">{"".join(shot(k + 1) .replace("shop-shot", "shop-shot shop-rv-photo") for k in range(v["photos"]))}</div>' if v["photos"] else ""
    reply = f'<div class="shop-rv-reply"><strong>Response from Acme Store</strong><p>{v["reply"]}</p></div>' if v["reply"] else ""
    return f"""<li data-review data-rating="{v["r"]}" data-helpful="{v["help"]}" data-date="{len(RVS) - i}" data-photos="{v["photos"]}">
  <div class="shop-rv-head">
    <span class="avatar"><span>{"".join(w[0] for w in v["name"].split())}</span></span>
    <div><p>{v["name"]}</p><small class="shop-rv-verified">{si("circle-check")}Verified purchase</small></div>
    <time class="shop-line-meta">{v["d"]}</time>
  </div>
  <div class="stack" data-gap="2">{stars(v["r"])}<h3>{v["t"]}</h3><p>{v["b"]}</p></div>
  {photos}
  <div class="shop-rv-meta"><span>Size bought: <strong>{v["size"]}</strong></span><span>Fit: <strong>{v["fit"]}</strong></span></div>
  {reply}
  <div class="shop-rv-help"><span>Helpful?</span><button type="button" class="btn" data-variant="outline" data-size="xs" aria-pressed="false" data-helpful-btn>Yes · <span data-helpful-count>{v["help"]}</span></button><button type="button" class="btn" data-variant="ghost" data-size="xs">Report</button></div>
</li>"""


REVIEWS_JS = """
document.querySelectorAll('[data-reviews]').forEach((root) => {
  const list = root.querySelector('.shop-rv-list');
  const items = [...list.querySelectorAll('[data-review]')];
  const bars = root.querySelectorAll('[data-star-filter]');
  const photos = root.querySelector('[data-photos-only]');
  const sort = root.querySelector('[data-review-sort]');
  const active = root.querySelector('.shop-rv-active');
  let star = 0;
  const run = () => {
    let n = 0;
    items.forEach((it) => {
      const ok = (!star || Number(it.dataset.rating) === star) && (!photos.checked || Number(it.dataset.photos) > 0);
      it.hidden = !ok;
      if (ok) n++;
    });
    bars.forEach((b) => b.setAttribute('aria-pressed', String(Number(b.dataset.starFilter) === star)));
    active.hidden = !star;
    active.querySelector('[data-star-label]').textContent = star + ' stars';
    root.querySelector('[data-review-count]').textContent = n + (n === 1 ? ' review' : ' reviews');
    root.querySelector('[data-review-empty]').hidden = n > 0;
  };
  bars.forEach((b) => b.addEventListener('click', () => { const v = Number(b.dataset.starFilter); star = star === v ? 0 : v; run(); }));
  active.querySelector('button').addEventListener('click', () => { star = 0; run(); });
  photos.addEventListener('change', run);
  sort.addEventListener('change', () => {
    const key = { helpful: (a, b) => b.dataset.helpful - a.dataset.helpful, newest: (a, b) => b.dataset.date - a.dataset.date, high: (a, b) => b.dataset.rating - a.dataset.rating, low: (a, b) => a.dataset.rating - b.dataset.rating }[sort.value];
    list.prepend(...[...items].sort(key));
  });
  list.addEventListener('click', (e) => {
    const b = e.target.closest('[data-helpful-btn]');
    if (!b) return;
    const on = b.getAttribute('aria-pressed') !== 'true';
    b.setAttribute('aria-pressed', String(on));
    const c = b.querySelector('[data-helpful-count]');
    c.textContent = Number(c.textContent) + (on ? 1 : -1);
  });
});
"""

ATTRS = [("Fit", "Runs small", "Runs large", 52), ("Softness", "Rough", "Very soft", 88), ("Warmth", "Light", "Very warm", 70)]
bars_html = "".join(f'<li><button type="button" data-star-filter="{n}" aria-pressed="false" aria-label="Show {n}-star reviews ({c})"><span>{n} {si("star")}</span><span class="progress" role="presentation"><span style="width: {pct}%"></span></span><span>{c}</span></button></li>' for n, pct, c in DIST)
attrs_html = "".join(f'<div><dt><span>{a}</span></dt><dd><div class="shop-rv-scale" role="img" aria-label="{a}: {v}% toward {hi}"><span style="inset-inline-start: {v}%"></span></div><div class="shop-rv-scale-labels"><span>{lo}</span><span>{hi}</span></div></dd></div>' for a, lo, hi, v in ATTRS)

add("reviews-01", "Reviews 01", "Product reviews: rating summary with clickable star bars, fit and feel scales, photo filter, sort, helpful votes and store replies.", "reviews", f"""
<main class="wrapper shop-page">
  <section class="shop-rv" data-reviews aria-labelledby="rv1-title">
    <aside class="shop-rv-aside stack" data-gap="6">
      <div class="stack" data-gap="2">
        <h2 class="shop-h2" id="rv1-title">Customer reviews</h2>
        <div class="shop-rv-score"><strong>4.8</strong><div class="stack" data-gap="1">{stars(4.8)}<span class="shop-line-meta">Based on 214 reviews</span></div></div>
      </div>
      <ul class="shop-rv-bars" aria-label="Filter by rating">{bars_html}</ul>
      <dl class="shop-rv-attrs">{attrs_html}</dl>
      <div class="stack" data-gap="2">
        <p class="shop-line-meta">Share your thoughts with other customers.</p>
        <a href="#" class="btn" data-variant="outline">{si("pencil")}Write a review</a>
      </div>
    </aside>
    <div class="stack" data-gap="4">
      <div class="shop-rv-toolbar">
        <div class="cluster" data-gap="3">
          <p class="shop-lead" data-review-count>{len(RVS)} reviews</p>
          <span class="badge shop-rv-active" data-variant="secondary" hidden><span data-star-label>5 stars</span><button type="button" class="btn" data-variant="ghost" data-size="icon-xs" aria-label="Clear rating filter">{si("x")}</button></span>
        </div>
        <div class="cluster" data-gap="3">
          <label class="shop-rv-toggle" for="rv1-photos"><input type="checkbox" role="switch" class="input" id="rv1-photos" data-photos-only>With photos</label>
          <label class="sr-only" for="rv1-sort">Sort reviews</label>
          <select class="select" id="rv1-sort" data-review-sort><option value="helpful">Most helpful</option><option value="newest">Newest</option><option value="high">Highest rating</option><option value="low">Lowest rating</option></select>
        </div>
      </div>
      <ul class="shop-rv-list">
        {"".join(rv_item(v, i) for i, v in enumerate(RVS))}
      </ul>
      <section class="empty" data-review-empty hidden>
        <header><figure>{si("star")}</figure><h3>No reviews match</h3><p>Try another rating or turn off “With photos”.</p></header>
      </section>
      <button type="button" class="btn" data-variant="outline">Show more reviews</button>
    </div>
  </section>
</main>
""", RV_CSS + """
  .shop-rv-bars button svg { inline-size: 0.75rem; block-size: 0.75rem; fill: currentColor; vertical-align: -1px; }
  .shop-rv-list .avatar { inline-size: 2.25rem; block-size: 2.25rem; font-size: 0.75rem; }
  .shop-rv-photo { inline-size: 4rem; block-size: 4rem; aspect-ratio: 1; border-radius: calc(var(--radius) - 2px); }""", scripts=script(REVIEWS_JS))

STAR_WORDS = ["Terrible", "Poor", "Okay", "Good", "Excellent"]
star_input = "".join(f'<label title="{w}"><input type="radio" name="rating" value="{i + 1}" required aria-label="{i + 1} star{"s" if i else ""}, {w}">{si("star")}</label>' for i, w in enumerate(STAR_WORDS))
WRITE_JS = """
document.querySelectorAll('[data-review-form]').forEach((form) => {
  const words = %s;
  const stars = form.querySelector('.shop-star-input');
  const labels = [...stars.querySelectorAll('label')];
  const text = form.querySelector('[data-star-text]');
  const paint = (n) => labels.forEach((l, i) => l.toggleAttribute('data-on', i < n));
  const chosen = () => Number(stars.querySelector('input:checked')?.value || 0);
  const show = (n) => { paint(n); text.textContent = n ? words[n - 1] : 'Select a rating'; };
  labels.forEach((l, i) => l.addEventListener('pointerenter', () => show(i + 1)));
  stars.addEventListener('pointerleave', () => show(chosen()));
  stars.addEventListener('change', () => { show(chosen()); form.querySelector('[data-rating-error]').hidden = true; });
  const body = form.elements.body;
  const line = form.querySelector('.shop-count-line');
  const counter = form.querySelector('[data-chars]');
  body.addEventListener('input', () => {
    counter.textContent = body.value.length + ' / ' + body.maxLength;
    line.toggleAttribute('data-warn', body.value.length > 0 && body.value.length < 20);
  });
  const file = form.querySelector('input[type=file]');
  const drop = form.querySelector('.shop-drop');
  const list = form.querySelector('.shop-previews');
  const tpl = form.querySelector('[data-remove-icon] svg');
  let files = [];
  const draw = () => {
    list.replaceChildren(...files.map((f, i) => {
      const li = document.createElement('li');
      const img = document.createElement('img');
      img.src = URL.createObjectURL(f);
      img.alt = f.name;
      const b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('aria-label', 'Remove ' + f.name);
      b.append(tpl.cloneNode(true));
      b.addEventListener('click', () => { files.splice(i, 1); draw(); });
      li.append(img, b);
      return li;
    }));
  };
  const addFiles = (fl) => { files = [...files, ...[...fl].filter((f) => f.type.startsWith('image/'))].slice(0, 4); draw(); };
  file.addEventListener('change', () => { addFiles(file.files); file.value = ''; });
  ['dragenter', 'dragover'].forEach((t) => drop.addEventListener(t, (e) => { e.preventDefault(); drop.setAttribute('data-over', ''); }));
  ['dragleave', 'drop'].forEach((t) => drop.addEventListener(t, () => drop.removeAttribute('data-over')));
  drop.addEventListener('drop', (e) => { e.preventDefault(); addFiles(e.dataTransfer.files); });
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const err = form.querySelector('[data-rating-error]');
    err.hidden = !!chosen();
    if (!chosen()) { stars.querySelector('input').focus(); return; }
    form.hidden = true;
    const done = document.getElementById(form.dataset.reviewForm);
    done.hidden = false;
    done.querySelector('h2').focus();
  });
});
""".replace("%s", "[" + ", ".join(f"'{w}'" for w in STAR_WORDS) + "]")


add("reviews-02", "Reviews 02", "Write a review: star rating with hover preview, fit feedback, a character counter, photo upload with previews and a thank-you state.", "reviews", f"""
<main class="wrapper shop-page" data-size="sm">
  <div class="stack" data-gap="6">
    <div class="cluster" data-gap="4">
      <img class="shop-thumb" src="{PH}" alt="">
      <div class="stack" data-gap="1">
        <p class="shop-line-meta">Write a review</p>
        <h1 class="shop-h2">Merino Crew Sweater</h1>
        <p class="shop-line-meta">Charcoal · Size M · Delivered Nov 10</p>
      </div>
    </div>
    <form class="card" data-review-form="rv2-done" novalidate>
      <section class="stack" data-gap="6">
        <div class="stack" data-gap="1">
          <div class="cluster" data-gap="1" data-align="end">
            <fieldset class="shop-star-input"><legend>Overall rating</legend>{star_input}</fieldset>
            <span class="shop-star-text" data-star-text aria-live="polite">Select a rating</span>
          </div>
          <p class="shop-error" data-rating-error hidden>{si("info")}Choose a star rating.</p>
        </div>
        <div class="shop-seg-wrap">
          <span class="label" id="rv2-fit">How does it fit?</span>
          <div class="shop-seg" role="radiogroup" aria-labelledby="rv2-fit">{"".join(f'<label><input type="radio" name="fit" value="{v}"{" checked" if v == "True to size" else ""}>{v}</label>' for v in ["Runs small", "True to size", "Runs large"])}</div>
        </div>
        <div role="group" class="field"><label for="rv2-title">Title</label><input id="rv2-title" name="title" type="text" placeholder="Sum it up in a few words" maxlength="80"></div>
        <div role="group" class="field">
          <label for="rv2-body">Your review</label>
          <textarea class="textarea" id="rv2-body" name="body" rows="5" maxlength="500" placeholder="What did you like? How do you wear it?"></textarea>
          <div class="shop-count-line"><span>At least 20 characters</span><span data-chars>0 / 500</span></div>
        </div>
        <div class="stack" data-gap="2">
          <span class="label">Photos <span class="shop-muted">(optional, up to 4)</span></span>
          <label class="shop-drop">{si("upload")}<span><strong>Click to upload</strong> or drag photos here</span><span>PNG or JPG</span><input type="file" class="sr-only" accept="image/*" multiple></label>
          <ul class="shop-previews" aria-label="Selected photos"></ul>
          <span data-remove-icon hidden>{si("x")}</span>
        </div>
        <div class="shop-switch-row"><label for="rv2-rec"><span class="shop-switch-title">I'd recommend this product</span></label><input type="checkbox" role="switch" class="input" id="rv2-rec" checked></div>
        <div role="group" class="field"><label for="rv2-name">Display name</label><input id="rv2-name" type="text" value="Olivia M." autocomplete="nickname"></div>
      </section>
      <footer class="cluster" data-justify="end" data-gap="2">
        <button type="button" class="btn" data-variant="outline">Cancel</button>
        <button type="submit" class="btn">Submit review</button>
      </footer>
    </form>
    <section class="card shop-rv-done" id="rv2-done" hidden aria-live="polite">
      <section class="shop-done">
        <span class="shop-success">{si("circle-check")}</span>
        <h2 tabindex="-1" class="shop-h2">Thanks for your review!</h2>
        <p>It will appear on the product page once it has been checked, usually within a day.</p>
        <a href="#" class="btn" data-variant="outline">Back to your orders</a>
      </section>
    </section>
  </div>
</main>
""", RV_CSS + SUCCESS_CSS + """
  .shop-done h2:focus { outline: none; }
  .shop-switch-row > label { flex: 1; cursor: pointer; }
  .shop-switch-title { font-size: 0.875rem; font-weight: 500; }
  .shop-success { display: inline-flex; align-items: center; justify-content: center; inline-size: 3rem; block-size: 3rem; border-radius: 999px; background: color-mix(in oklab, var(--primary) 12%, transparent); color: var(--primary); }
  .shop-success svg { inline-size: 1.5rem; block-size: 1.5rem; }""", scripts=script(WRITE_JS))

TAGS = [("Soft", 86, "pro"), ("Warm", 64, "pro"), ("True to size", 51, "pro"), ("Holds color", 27, "pro"), ("Long sleeves", 18, "con"), ("Some pilling", 9, "con")]
REEL = [
    ("Hannah K.", 5, "Soft and warm without being bulky. True to size, I'm usually a medium.", ["Soft", "Warm", "True to size"]),
    ("Marcus L.", 5, "Still looks new after a winter of wear. The color holds after many washes.", ["Holds color"]),
    ("Priya S.", 4, "Lovely color. Slightly longer in the sleeves than I expected.", ["Long sleeves"]),
    ("Jo P.", 5, "So soft I bought a second color. Fits exactly as described.", ["Soft", "True to size"]),
    ("Tom W.", 3, "Warm and comfortable, some pilling under the arms after a month.", ["Warm", "Some pilling"]),
    ("Lena F.", 5, "Warm enough for autumn walks without a coat.", ["Warm"]),
]
reel = "".join(f'''<article class="card" data-tags="{"|".join(tg)}">
  <header><div class="cluster" data-justify="between">{stars(r)}<span class="shop-line-meta">{n}</span></div></header>
  <section><p>{t}</p></section>
  <footer class="shop-tags-mini">{"".join(f'<span class="badge" data-variant="outline">{x}</span>' for x in tg)}</footer>
</article>''' for n, r, t, tg in REEL)
TAGS_JS = """
document.querySelectorAll('[data-review-tags]').forEach((root) => {
  const reel = root.querySelector('.shop-reel');
  const cards = [...reel.children];
  const count = root.querySelector('[data-reel-count]');
  root.querySelector('.shop-tags').addEventListener('click', (e) => {
    const b = e.target.closest('button[data-tag]');
    if (!b) return;
    const on = b.getAttribute('aria-pressed') !== 'true';
    root.querySelectorAll('button[data-tag]').forEach((x) => x.setAttribute('aria-pressed', String(x === b && on)));
    let n = 0;
    cards.forEach((c) => { c.hidden = on && !c.dataset.tags.split('|').includes(b.dataset.tag); if (!c.hidden) n++; });
    count.textContent = on ? n + ' reviews mention “' + b.dataset.tag + '”' : 'Recent reviews';
    reel.scrollTo({ left: 0 });
  });
  const page = (d) => reel.scrollBy({ left: d * reel.clientWidth * 0.9, behavior: 'smooth' });
  root.querySelector('[data-reel=prev]').addEventListener('click', () => page(-1));
  root.querySelector('[data-reel=next]').addEventListener('click', () => page(1));
});
"""
add("reviews-03", "Reviews 03", "Review highlights: a summary, pro and con tags that filter a scrolling row of reviews, with previous and next buttons.", "reviews", f"""
<main class="wrapper shop-page">
  <section class="stack" data-gap="6" data-review-tags aria-labelledby="rv3-title">
    <div class="cluster" data-justify="between" data-align="end" data-gap="4">
      <div class="stack" data-gap="2">
        <h2 class="shop-h1" id="rv3-title">What customers say</h2>
        <div class="cluster" data-gap="2">{stars(4.8)}<span class="shop-line-meta">4.8 out of 5 · 214 reviews · 96% recommend</span></div>
      </div>
      <a href="#" class="btn" data-variant="outline">See all reviews</a>
    </div>
    <div class="shop-summary-ai">
      <h2>{si("sparkles")}Review summary</h2>
      <p>Customers love how <strong>soft</strong> and <strong>warm</strong> this sweater is and say it fits <strong>true to size</strong> and keeps its color. A few mention <strong>long sleeves</strong> and <strong>light pilling</strong> in the first weeks.</p>
      <div class="shop-tags" role="group" aria-label="Filter reviews by topic">{"".join(f'<button type="button" data-tag="{t}" data-tone="{tone}" aria-pressed="false">{si("check") if tone == "pro" else si("info")}{t}<span>{c}</span></button>' for t, c, tone in TAGS)}</div>
    </div>
    <div class="shop-reel-wrap">
      <div class="cluster" data-justify="between">
        <p class="shop-lead" data-reel-count aria-live="polite">Recent reviews</p>
        <div class="cluster" data-gap="2">
          <button type="button" class="btn" data-variant="outline" data-size="icon-sm" aria-label="Previous reviews" data-reel="prev">{si("chevron-left")}</button>
          <button type="button" class="btn" data-variant="outline" data-size="icon-sm" aria-label="Next reviews" data-reel="next">{si("chevron-right")}</button>
        </div>
      </div>
      <div class="shop-reel" tabindex="0" aria-label="Reviews">{reel}</div>
    </div>
  </section>
</main>
""", RV_CSS + """
  .shop-tags button svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .shop-tags-mini { display: flex; flex-wrap: wrap; gap: 0.25rem; }
  .shop-reel:focus-visible { outline: 2px solid var(--ring); outline-offset: 4px; }""", scripts=script(TAGS_JS))


if __name__ == "__main__":
    from common import register
    register(blocks)
    print(f"shop: {len(blocks)} blocks")

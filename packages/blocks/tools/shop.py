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
  html.dark .shop-thumb, html.dark .shop-product-img { filter: brightness(0.5) grayscale(1); }
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

if __name__ == "__main__":
    from common import register
    register(blocks)
    print(f"shop: {len(blocks)} blocks")

"""Ecommerce blocks: cart, mini cart, checkout, orders, account and bottom navigation.

Auvyx originals (shadcn/ui has no ecommerce blocks). Every block is a plain
page built from Auvyx components (card, item, field, badge, sheet, popover,
table, dialog) plus a small block <style>; the scripts are demo behavior
(quantities and totals, steps, filters) that apps replace with their own state.
"""
import re

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
    "play": '<path d="M5 5a2 2 0 0 1 3.008-1.728l11.997 6.998a2 2 0 0 1 .003 3.458l-12 7A2 2 0 0 1 5 19z"/>',
    "pause": '<rect height="18" rx="1" width="5" x="14" y="3"/><rect height="18" rx="1" width="5" x="5" y="3"/>',
    "book-open": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    "users": '<circle cx="9" cy="7" r="4"/><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><path d="M16 3.128a4 4 0 0 1 0 7.744"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/>',
    "monitor": '<line x1="12" x2="12" y1="17" y2="21"/><line x1="8" x2="16" y1="21" y2="21"/><rect height="14" rx="2" width="20" x="2" y="3"/>',
    "smartphone": '<path d="M12 18h.01"/><rect height="20" rx="2" width="14" x="5" y="2"/>',
    "file-text": '<path d="M10 9H8"/><path d="M14 2v5a1 1 0 0 0 1 1h5"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"/>',
    "chart-column": '<path d="M13 17V5"/><path d="M18 17V9"/><path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="M8 17v-3"/>',
    "calendar": '<path d="M16 2v4"/><path d="M3 10h18"/><path d="M8 2v4"/><rect height="18" rx="2" width="18" x="3" y="4"/>',
    "message-square": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "award": '<path d="m15.477 12.89l1.515 8.526a.5.5 0 0 1-.81.47l-3.58-2.687a1 1 0 0 0-1.197 0l-3.586 2.686a.5.5 0 0 1-.81-.469l1.514-8.526"/><circle cx="12" cy="8" r="6"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20a14.5 14.5 0 0 0 0-20M2 12h20"/>',
    "infinity": '<path d="M6 16c5 0 7-8 12-8a4 4 0 0 1 0 8c-5 0-7-8-12-8a4 4 0 1 0 0 8"/>',
    "captions": '<rect width="18" height="14" x="3" y="5" rx="2" ry="2"/><path d="M7 15h4m4 0h2M7 11h2m4 0h4"/>',
    "graduation-cap": '<path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0zM22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>',
    "volume-2": '<path d="M11 4.702a.705.705 0 0 0-1.203-.498L6.413 7.587A1.4 1.4 0 0 1 5.416 8H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.416a1.4 1.4 0 0 1 .997.413l3.383 3.384A.705.705 0 0 0 11 19.298zM16 9a5 5 0 0 1 0 6m3.364 3.364a9 9 0 0 0 0-12.728"/>',
    "maximize": '<path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3M3 16v3a2 2 0 0 0 2 2h3m8 0h3a2 2 0 0 0 2-2v-3"/>',
    "circle-play": '<path d="M9 9.003a1 1 0 0 1 1.517-.859l4.997 2.997a1 1 0 0 1 0 1.718l-4.997 2.997A1 1 0 0 1 9 14.996z"/><circle cx="12" cy="12" r="10"/>',
    "notebook-pen": '<path d="M13.4 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7.4M2 6h4m-4 4h4m-4 4h4m-4 4h4"/><path d="M21.378 5.626a1 1 0 1 0-3.004-3.004l-5.01 5.012a2 2 0 0 0-.506.854l-.837 2.87a.5.5 0 0 0 .62.62l2.87-.837a2 2 0 0 0 .854-.506z"/>',
    "trophy": '<path d="M10 14.66V17a1 1 0 0 1-1 1a2 2 0 0 0-2 2v2m7-7.34V17a1 1 0 0 0 1 1a2 2 0 0 1 2 2v2m.916-12H19.5A2.5 2.5 0 0 0 22 7.5V5a1 1 0 0 0-1-1h-3M4 22h16"/><path d="M6 9a6 6 0 0 0 12 0V3a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1z"/><path d="M6.084 10H4.5A2.5 2.5 0 0 1 2 7.5V5a1 1 0 0 1 1-1h3"/>',
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
  .shop-nav-icon > .shop-count { inset-block-start: -0.25rem; inset-inline-end: -0.625rem; }
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


BTN = re.compile(r'(<(button|a)\b[^>]*\bclass="[^"]*\bbtn\b[^"]*"[^>]*>)(.*?)(</\2>)', re.S)


def mark_icons(html):
    """Text buttons: tag a leading or trailing icon with data-icon so the button
    trims that side's padding (inline-start / inline-end), as upstream."""
    def fix(m):
        open_, _, inner, close = m.groups()
        if re.search(r'data-size="icon', open_) or "<svg" not in inner:
            return m.group(0)
        text = re.sub(r"<svg\b.*?</svg>", "", inner, flags=re.S)
        if not re.sub(r"<[^>]+>", "", text).strip():
            return m.group(0)
        body = inner.strip()
        if body.startswith("<svg") and "data-icon" not in body[:body.index(">")]:
            inner = inner.replace("<svg", '<svg data-icon="inline-start"', 1)
        body = inner.strip()
        if body.endswith("</svg>"):
            i = inner.rfind("<svg")
            if "data-icon" not in inner[i:inner.index(">", i)]:
                inner = inner[:i] + '<svg data-icon="inline-end"' + inner[i + 4:]
        return open_ + inner + close
    return BTN.sub(fix, html)


def add(bid, title, desc, cat, body, css=SHOP_CSS, scripts="", body_class=""):
    page(bid, title, mark_icons(body), css, body_class=body_class, scripts=scripts)
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
  .shop-check-list label > .shop-stars { margin-inline-start: 0; }
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
          <div class="stack" data-gap="4">
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
      <div class="stack" data-gap="4">
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
      <div class="stack" data-gap="4">
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
  <div class="stack" data-gap="4">
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
      <div class="stack" data-gap="4">
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



# ================================================================== online courses (Udemy / Domestika style)
COURSES = [
    {"id": "brand", "title": "Brand Identity Design from Scratch", "by": "Lena Ortiz", "role": "Brand designer", "cat": "Design", "rating": 4.8, "reviews": 3412, "students": 28940, "hours": 7.5, "lectures": 64, "level": "Beginner", "price": 19.99, "was": 89.99, "badge": "Bestseller", "shot": 1,
     "sub": "Build a complete visual identity: research, logo, color, type and a brand book.", "learn": ["Research a brand and write a creative brief", "Sketch and refine a logo in Illustrator", "Pick a palette and type pairing that fit", "Deliver a brand book clients understand"]},
    {"id": "watercolor", "title": "Expressive Watercolor Botanicals", "by": "Mai Tanaka", "role": "Illustrator", "cat": "Illustration", "rating": 4.9, "reviews": 1288, "students": 9120, "hours": 4.0, "lectures": 31, "level": "Beginner", "price": 14.99, "was": 59.99, "badge": "Highest rated", "shot": 2,
     "sub": "Paint loose, luminous flowers with a limited palette and confident brushwork.", "learn": ["Mix a limited palette", "Control wet-on-wet blooms", "Compose a botanical page", "Scan and clean your art"]},
    {"id": "react", "title": "React 19 and TypeScript: Build Real Apps", "by": "Daniel Rossi", "role": "Senior engineer", "cat": "Development", "rating": 4.7, "reviews": 15211, "students": 112400, "hours": 32.0, "lectures": 248, "level": "Intermediate", "price": 24.99, "was": 129.99, "badge": "Bestseller", "shot": 3,
     "sub": "Hooks, server components, forms and testing, with four portfolio projects.", "learn": ["Model state with hooks and reducers", "Fetch data with server components", "Type props and forms with TypeScript", "Test components with Vitest"]},
    {"id": "photo", "title": "Mobile Photography for Instagram", "by": "Sofia Lind", "role": "Photographer", "cat": "Photography", "rating": 4.6, "reviews": 2204, "students": 17630, "hours": 3.5, "lectures": 27, "level": "Beginner", "price": 0, "was": None, "badge": "Free", "shot": 4,
     "sub": "Compose, shoot and edit striking photos with the phone in your pocket.", "learn": ["Use light and composition", "Shoot portraits and food", "Edit in Lightroom Mobile", "Plan a consistent feed"]},
    {"id": "motion", "title": "Motion Design in After Effects", "by": "Tom Becker", "role": "Motion designer", "cat": "Animation", "rating": 4.8, "reviews": 4103, "students": 31200, "hours": 12.5, "lectures": 96, "level": "Intermediate", "price": 22.99, "was": 99.99, "badge": "New", "shot": 1,
     "sub": "Animate logos, UI and explainer scenes with keyframes, easing and expressions.", "learn": ["Ease keyframes in the graph editor", "Animate shape layers and text", "Use expressions for loops", "Export for web and social"]},
    {"id": "excel", "title": "Data Analysis with Excel and Power BI", "by": "Priya Shah", "role": "Data analyst", "cat": "Business", "rating": 4.5, "reviews": 8840, "students": 64010, "hours": 18.0, "lectures": 140, "level": "All levels", "price": 17.99, "was": 84.99, "badge": None, "shot": 3,
     "sub": "Clean data, build pivot tables and publish interactive dashboards.", "learn": ["Clean data with Power Query", "Summarize with pivot tables", "Model data in Power BI", "Share dashboards with your team"]},
    {"id": "ceramics", "title": "Wheel-Thrown Ceramics at Home", "by": "Hugo Martín", "role": "Ceramist", "cat": "Craft", "rating": 4.9, "reviews": 642, "students": 5230, "hours": 5.5, "lectures": 42, "level": "Beginner", "price": 29.99, "was": None, "badge": "Highest rated", "shot": 2,
     "sub": "Center, throw, trim and glaze bowls and mugs on a tabletop wheel.", "learn": ["Wedge and center clay", "Throw cylinders and bowls", "Trim and add handles", "Glaze and fire safely"]},
    {"id": "copy", "title": "Copywriting That Sells", "by": "Grace Kim", "role": "Copywriter", "cat": "Marketing", "rating": 4.4, "reviews": 1910, "students": 22870, "hours": 6.0, "lectures": 48, "level": "Advanced", "price": 16.99, "was": 74.99, "badge": None, "shot": 4,
     "sub": "Write headlines, landing pages and emails that turn readers into customers.", "learn": ["Find the promise that sells", "Write headlines that hook", "Structure a landing page", "Write a 5-email sequence"]},
]
C = {c["id"]: c for c in COURSES}

COURSE_CSS = """
  .crs-thumb { aspect-ratio: 16 / 9; }
  .crs-grid { display: grid; gap: 1.75rem 1.25rem; grid-template-columns: repeat(auto-fill, minmax(min(100%, 15rem), 1fr)); }
  .crs-card { position: relative; display: flex; flex-direction: column; gap: 0.625rem; }
  .crs-card-media { position: relative; overflow: hidden; border-radius: var(--radius); background: var(--muted); }
  .crs-card-media > img { display: block; transition: transform 300ms ease; }
  .crs-card:hover .crs-card-media > img { transform: scale(1.04); }
  .crs-card-media .badge { position: absolute; inset-block-start: 0.625rem; inset-inline-start: 0.625rem; }
  .crs-dur { position: absolute; inset-block-end: 0.5rem; inset-inline-end: 0.5rem; padding: 0.125rem 0.375rem; border-radius: calc(var(--radius) - 4px); background: rgb(0 0 0 / 0.72); color: #fff; font-size: 0.6875rem; font-weight: 600; font-variant-numeric: tabular-nums; }
  .crs-card h3 { margin: 0; font-size: 0.9375rem; font-weight: 600; line-height: 1.35; }
  .crs-card h3 a { color: inherit; text-decoration: none; }
  .crs-card h3 a::after { content: ''; position: absolute; inset: 0; z-index: 1; }
  .crs-card h3 a:focus-visible { outline: none; }
  .crs-card:has(h3 a:focus-visible) .crs-card-media { outline: 2px solid var(--ring); outline-offset: 2px; }
  .crs-by { margin: 0; font-size: 0.8125rem; color: var(--muted-foreground); }
  .crs-rate { display: flex; align-items: center; gap: 0.375rem; margin: 0; font-size: 0.8125rem; }
  .crs-rate strong { font-weight: 700; color: oklch(0.6 0.15 70); }
  .crs-rate .shop-stars { color: oklch(0.72 0.16 75); }
  .crs-rate span { color: var(--muted-foreground); }
  .crs-meta { display: flex; flex-wrap: wrap; gap: 0.25rem 0.5rem; margin: 0; padding: 0; list-style: none; font-size: 0.75rem; color: var(--muted-foreground); }
  .crs-meta li { display: inline-flex; align-items: center; gap: 0.25rem; }
  .crs-meta li + li::before { content: '·'; margin-inline-end: 0.25rem; }
  .crs-price { display: flex; align-items: baseline; gap: 0.5rem; margin: 0; font-variant-numeric: tabular-nums; }
  .crs-price strong { font-size: 1rem; font-weight: 700; }
  .crs-price s { font-size: 0.8125rem; color: var(--muted-foreground); }
  .crs-price[data-size='lg'] strong { font-size: 2rem; letter-spacing: -0.02em; }
  .crs-price[data-size='lg'] s { font-size: 1rem; }
  .crs-off { font-size: 0.875rem; font-weight: 500; }
  .crs-header { position: sticky; inset-block-start: 0; z-index: 10; border-block-end: 1px solid var(--border); background: color-mix(in oklab, var(--background) 92%, transparent); backdrop-filter: blur(8px); }
  .crs-header-row { display: flex; align-items: center; gap: 1rem; block-size: 4rem; }
  .crs-header-search { flex: 1; max-inline-size: 30rem; }
  .crs-header-search input { border-radius: 999px; }
  .crs-header-nav { display: flex; align-items: center; gap: 0.25rem; margin-inline-start: auto; }
  .crs-header-nav > a:not(.btn) { padding: 0.5rem 0.625rem; color: var(--muted-foreground); font-size: 0.875rem; text-decoration: none; border-radius: var(--radius); }
  .crs-header-nav > a:not(.btn):hover { color: var(--foreground); background: var(--accent); }
  .crs-header .avatar { inline-size: 2rem; block-size: 2rem; font-size: 0.75rem; }
  @media (width < 56rem) { .crs-header-nav > a:not(.btn) { display: none; } }
  @media (width < 40rem) { .crs-header-search { display: none; } .crs-header-nav { margin-inline-start: auto; } }
  .crs-pills { display: flex; gap: 0.5rem; overflow-x: auto; scrollbar-width: none; padding-block: 0.125rem; }
  .crs-pills button { flex: none; padding: 0.4375rem 0.875rem; border: 1px solid var(--border); border-radius: 999px; background: none; color: inherit; font: inherit; font-size: 0.875rem; cursor: pointer; corner-shape: round; }
  .crs-pills button:hover { background: var(--accent); }
  .crs-pills button[aria-pressed='true'] { border-color: var(--foreground); background: var(--foreground); color: var(--background); }
  .crs-pills button:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
  .crs-list-card { display: grid; grid-template-columns: 15rem minmax(0, 1fr) auto; gap: 1.25rem; padding-block: 1.25rem; border-block-end: 1px solid var(--border); position: relative; }
  .crs-list-card .crs-card-media { align-self: start; }
  .crs-list-card p { margin: 0; }
  .crs-list-card .stack { min-inline-size: 0; }
  @media (width < 48rem) { .crs-list-card { grid-template-columns: 8rem minmax(0, 1fr); } .crs-list-card > :last-child { grid-column: 2; } }
  .crs-pop { position: absolute; inset-block-start: 0; inset-inline-start: calc(100% + 0.75rem); z-index: 20; inline-size: 20rem; display: grid; gap: 0.75rem; padding: 1.25rem; border: 1px solid var(--border); border-radius: calc(var(--radius) + 2px); background: var(--popover); color: var(--popover-foreground); box-shadow: 0 16px 40px -12px rgb(0 0 0 / 0.3); opacity: 0; visibility: hidden; transform: translateX(-0.5rem); transition: opacity 150ms ease, transform 150ms ease, visibility 0s 150ms; }
  .crs-card[data-flip] .crs-pop { inset-inline-start: auto; inset-inline-end: calc(100% + 0.75rem); transform: translateX(0.5rem); }
  .crs-card:hover .crs-pop { opacity: 1; visibility: visible; transform: none; transition-delay: 250ms, 250ms, 0s; }
  .crs-card:focus-within .crs-pop { opacity: 1; visibility: visible; transform: none; transition-delay: 0s; }
  .crs-pop::before { content: ''; position: absolute; inset-block-start: 2rem; inset-inline-start: -0.5rem; inline-size: 1rem; block-size: 1rem; rotate: 45deg; background: var(--popover); border-inline-start: 1px solid var(--border); border-block-end: 1px solid var(--border); }
  .crs-card[data-flip] .crs-pop::before { inset-inline-start: auto; inset-inline-end: -0.5rem; border: 0; border-inline-end: 1px solid var(--border); border-block-start: 1px solid var(--border); }
  .crs-pop h4 { margin: 0; font-size: 1rem; font-weight: 600; }
  .crs-pop p { margin: 0; font-size: 0.8125rem; }
  .crs-pop .crs-learn { gap: 0.375rem; }
  .crs-pop-actions { position: relative; z-index: 2; display: flex; gap: 0.5rem; }
  .crs-pop-actions .btn:first-child { flex: 1; }
  @media (hover: none) { .crs-pop { display: none; } }
  @media (width < 64rem) { .crs-pop { display: none; } }
  .crs-learn { display: grid; gap: 0.625rem 1.5rem; margin: 0; padding: 0; list-style: none; font-size: 0.875rem; }
  .crs-learn[data-cols='2'] { grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr)); }
  .crs-learn li { display: flex; gap: 0.625rem; align-items: flex-start; }
  .crs-learn svg { flex: none; inline-size: 1rem; block-size: 1rem; margin-block-start: 0.1875rem; color: var(--primary); }
  .crs-hero { color: #fff; background: oklch(0.2 0.02 270); }
  .crs-hero-in { display: grid; gap: 1rem; padding-block: 2.5rem; }
  @media (width >= 64rem) { .crs-hero-in { padding-inline-end: 24rem; } }
  .crs-hero h1 { margin: 0; font-size: clamp(1.75rem, 3.6vw, 2.25rem); font-weight: 700; letter-spacing: -0.02em; line-height: 1.15; }
  .crs-hero p { margin: 0; }
  .crs-hero .shop-crumbs a { color: oklch(0.82 0.08 280); }
  .crs-hero .shop-crumbs span { color: #fff; }
  .crs-hero .crs-rate span { color: rgb(255 255 255 / 0.75); }
  .crs-hero .crs-meta { color: rgb(255 255 255 / 0.8); font-size: 0.8125rem; }
  .crs-hero .crs-meta svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .crs-hero a.crs-inline { color: oklch(0.82 0.08 280); }
  .crs-detail { display: grid; gap: 2.5rem; align-items: start; padding-block: 2rem 4rem; }
  @media (width >= 64rem) { .crs-detail { grid-template-columns: minmax(0, 1fr) 21rem; } .crs-buy { margin-block-start: -17rem; position: sticky; inset-block-start: 5rem; } }
  .crs-buy { overflow: hidden; padding: 0; }
  .crs-buy > section { padding: 1.25rem; }
  .crs-preview { position: relative; display: block; inline-size: 100%; padding: 0; border: 0; background: #000; cursor: pointer; }
  .crs-preview img { display: block; opacity: 0.85; }
  .crs-preview > span { position: absolute; inset: 0; display: grid; place-content: center; justify-items: center; gap: 0.5rem; color: #fff; font-weight: 600; font-size: 0.875rem; background: linear-gradient(to top, rgb(0 0 0 / 0.65), transparent 70%); }
  .crs-preview > span > span { display: grid; place-items: center; inline-size: 3.5rem; block-size: 3.5rem; border-radius: 999px; background: #fff; color: #111; transition: transform 150ms ease; corner-shape: round; }
  .crs-preview > span > span svg { inline-size: 1.25rem; block-size: 1.25rem; fill: currentColor; margin-inline-start: 0.125rem; }
  .crs-preview:hover > span > span { transform: scale(1.08); }
  .crs-preview:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
  .crs-timer { display: flex; align-items: center; gap: 0.375rem; margin: 0; font-size: 0.8125rem; color: var(--destructive); }
  .crs-timer svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .crs-includes { display: grid; gap: 0.5rem; margin: 0; padding: 0; list-style: none; font-size: 0.8125rem; }
  .crs-includes li { display: flex; gap: 0.625rem; align-items: center; }
  .crs-includes svg { inline-size: 1rem; block-size: 1rem; flex: none; color: var(--muted-foreground); }
  .crs-rating-head { display: flex; align-items: center; gap: 0.5rem; }
  .crs-rating-head svg { inline-size: 1.25rem; block-size: 1.25rem; fill: oklch(0.72 0.16 75); color: oklch(0.72 0.16 75); }
  .crs-box { padding: 1.5rem; border: 1px solid var(--border); border-radius: var(--radius); }
  .crs-curr-head { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.5rem; font-size: 0.875rem; }
  .crs-curr { border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
  .crs-curr > details { border-block-end: 1px solid var(--border); }
  .crs-curr > details:last-child { border-block-end: 0; }
  .crs-curr summary { display: flex; align-items: center; gap: 0.75rem; padding: 0.875rem 1rem; background: var(--muted); font-size: 0.9375rem; font-weight: 600; cursor: pointer; list-style: none; }
  .crs-curr summary::-webkit-details-marker { display: none; }
  .crs-curr summary > svg { inline-size: 1rem; block-size: 1rem; flex: none; transition: transform 150ms ease; }
  .crs-curr details[open] > summary > svg { transform: rotate(180deg); }
  .crs-curr summary small { margin-inline-start: auto; font-size: 0.8125rem; font-weight: 400; color: var(--muted-foreground); white-space: nowrap; }
  .crs-curr summary:focus-visible { outline: 2px solid var(--ring); outline-offset: -2px; }
  .crs-curr ul { list-style: none; margin: 0; padding: 0.5rem 1rem; }
  .crs-lesson { display: flex; align-items: center; gap: 0.75rem; padding-block: 0.5rem; font-size: 0.875rem; }
  .crs-lesson > svg { inline-size: 1rem; block-size: 1rem; flex: none; color: var(--muted-foreground); }
  .crs-lesson > span:first-of-type { flex: 1; }
  .crs-lesson a { color: var(--primary); }
  .crs-lesson time { color: var(--muted-foreground); font-size: 0.8125rem; font-variant-numeric: tabular-nums; }
  .crs-clamp { position: relative; max-block-size: 12rem; overflow: hidden; }
  .crs-clamp::after { content: ''; position: absolute; inset-inline: 0; inset-block-end: 0; block-size: 4rem; background: linear-gradient(transparent, var(--background)); }
  .crs-clamp[data-open] { max-block-size: none; }
  .crs-clamp[data-open]::after { display: none; }
  .crs-prose { display: grid; gap: 0.75rem; font-size: 0.9375rem; line-height: 1.65; }
  .crs-prose p { margin: 0; }
  .crs-prose ul { margin: 0; padding-inline-start: 1.25rem; }
  .crs-teacher { display: grid; gap: 1rem; }
  .crs-teacher-top { display: flex; gap: 1rem; align-items: center; }
  .crs-teacher-top .avatar { inline-size: 5rem; block-size: 5rem; font-size: 1.25rem; }
  .crs-teacher-top h3 { margin: 0; font-size: 1.125rem; }
  .crs-teacher-top h3 a { color: var(--primary); }
  .crs-teacher-top p { margin: 0; color: var(--muted-foreground); font-size: 0.875rem; }
  .crs-facts { display: grid; gap: 0.375rem; margin: 0; padding: 0; list-style: none; font-size: 0.875rem; }
  .crs-facts li { display: flex; gap: 0.625rem; align-items: center; }
  .crs-facts svg { inline-size: 1rem; block-size: 1rem; color: var(--muted-foreground); }
  .crs-video { position: relative; aspect-ratio: 16 / 9; overflow: hidden; border-radius: var(--radius); background: #000; }
  .crs-video > img { position: absolute; inset: 0; inline-size: 100%; block-size: 100%; object-fit: cover; opacity: 0.8; }
  .crs-video-big { position: absolute; inset: 0; margin: auto; display: grid; place-items: center; inline-size: 4.5rem; block-size: 4.5rem; padding: 0; border: 0; border-radius: 999px; background: rgb(255 255 255 / 0.95); color: #111; cursor: pointer; corner-shape: round; transition: transform 150ms ease, opacity 150ms ease; }
  .crs-video-big svg { inline-size: 1.75rem; block-size: 1.75rem; fill: currentColor; margin-inline-start: 0.1875rem; }
  .crs-video-big:hover { transform: scale(1.06); }
  .crs-video-big:focus-visible { outline: 3px solid #fff; outline-offset: 3px; }
  .crs-video[data-playing] .crs-video-big { opacity: 0; pointer-events: none; }
  .crs-controls { position: absolute; inset-inline: 0; inset-block-end: 0; display: grid; gap: 0.5rem; padding: 2rem 1rem 0.75rem; color: #fff; background: linear-gradient(transparent, rgb(0 0 0 / 0.75)); }
  .crs-controls .progress { block-size: 0.25rem; background: rgb(255 255 255 / 0.3); }
  .crs-controls .progress > span { background: var(--primary); }
  .crs-controls-row { display: flex; align-items: center; gap: 0.25rem; font-size: 0.8125rem; font-variant-numeric: tabular-nums; }
  .crs-controls-row .btn { color: #fff; }
  .crs-controls-row .btn:hover { background: rgb(255 255 255 / 0.15); color: #fff; }
  .crs-controls-row time { margin-inline: 0.5rem auto; }
  .crs-play svg + svg { display: none; }
  .crs-play[aria-pressed='true'] svg { display: none; }
  .crs-play[aria-pressed='true'] svg + svg { display: block; }
  .crs-learnpage { display: grid; min-block-size: calc(100svh - 3.5rem); }
  .crs-learnpage[data-side-hidden] > .crs-learn-side { display: none; }
  .crs-stage { position: relative; }
  .crs-side-open { position: absolute; inset-block-start: 0.75rem; inset-inline-end: 0.75rem; z-index: 2; background: var(--background); }
  @media (width >= 64rem) { .crs-learnpage { grid-template-columns: minmax(0, 1fr) 24rem; } }
  @media (width >= 64rem) { .crs-learnpage[data-side-hidden] { grid-template-columns: minmax(0, 1fr); } }
  .crs-learn-main { display: grid; align-content: start; gap: 1.5rem; padding: 1.5rem; min-inline-size: 0; }
  .crs-learn-side { border-inline-start: 1px solid var(--border); background: var(--background); }
  @media (width >= 64rem) { .crs-learn-side { position: sticky; inset-block-start: 3.5rem; block-size: calc(100svh - 3.5rem); overflow-y: auto; } }
  .crs-learn-side-head { position: sticky; inset-block-start: 0; z-index: 1; display: grid; gap: 0.5rem; padding: 1rem; border-block-end: 1px solid var(--border); background: var(--background); }
  .crs-learn-side-head h2 { margin: 0; font-size: 1rem; }
  .crs-learn-side-head p { margin: 0; font-size: 0.8125rem; color: var(--muted-foreground); }
  .crs-learn-side details { border-block-end: 1px solid var(--border); }
  .crs-learn-side summary { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 0.125rem 0.75rem; padding: 0.875rem 1rem; background: var(--muted); cursor: pointer; list-style: none; }
  .crs-learn-side summary > svg { grid-column: 2; grid-row: 1 / span 2; align-self: center; inline-size: 1rem; block-size: 1rem; color: var(--muted-foreground); transition: transform 150ms ease; }
  .crs-learn-side details[open] > summary > svg { transform: rotate(180deg); }
  .crs-learn-side summary > strong { grid-row: 1; grid-column: 1; }
  .crs-learn-side summary > small { grid-row: 2; grid-column: 1; }
  .crs-learn-side summary:hover { background: color-mix(in oklab, var(--muted) 70%, var(--accent)); }
  .crs-learn-side summary:focus-visible { outline: 2px solid var(--ring); outline-offset: -2px; }
  .crs-learn-side summary::-webkit-details-marker { display: none; }
  .crs-learn-side summary strong { font-size: 0.875rem; }
  .crs-learn-side summary small { font-size: 0.75rem; color: var(--muted-foreground); }
  .crs-learn-side ol { list-style: none; margin: 0; padding: 0; }
  .crs-learn-side li { display: flex; gap: 0.75rem; align-items: flex-start; padding: 0.625rem 1rem; }
  .crs-learn-side li[aria-current] { background: var(--accent); }
  .crs-learn-side li > button { display: grid; gap: 0.125rem; flex: 1; padding: 0; border: 0; background: none; color: inherit; font: inherit; font-size: 0.875rem; text-align: start; cursor: pointer; }
  .crs-learn-side li > button small { display: flex; align-items: center; gap: 0.25rem; color: var(--muted-foreground); font-size: 0.75rem; }
  .crs-learn-side li > button small svg { inline-size: 0.75rem; block-size: 0.75rem; }
  .crs-learn-side li > button:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
  .crs-learn-side li > input { margin-block-start: 0.1875rem; }
  .crs-topbar { position: sticky; inset-block-start: 0; z-index: 10; display: flex; align-items: center; gap: 1rem; block-size: 3.5rem; padding-inline: 1rem; background: oklch(0.2 0.02 270); color: #fff; }
  .crs-topbar .block-logo { color: #fff; }
  .crs-topbar h1 { flex: 1; min-inline-size: 0; margin: 0; padding-inline-start: 1rem; border-inline-start: 1px solid rgb(255 255 255 / 0.2); font-size: 0.9375rem; font-weight: 500; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
  .crs-topbar .btn { color: #fff; }
  .crs-topbar .btn:hover { background: rgb(255 255 255 / 0.12); color: #fff; }
  .crs-ring { display: flex; align-items: center; gap: 0.5rem; font-size: 0.8125rem; white-space: nowrap; }
  .crs-ring svg { inline-size: 2rem; block-size: 2rem; rotate: -90deg; }
  .crs-ring circle { fill: none; stroke-width: 3; }
  .crs-ring circle:first-child { stroke: rgb(255 255 255 / 0.25); }
  .crs-ring circle:last-child { stroke: oklch(0.82 0.15 85); stroke-linecap: round; transition: stroke-dashoffset 300ms ease; }
  @media (width < 40rem) { .crs-ring span { display: none; } }
  .crs-notes { display: grid; gap: 0.75rem; margin: 0; padding: 0; list-style: none; }
  .crs-notes li { display: grid; gap: 0.25rem; padding: 0.75rem 1rem; border-radius: var(--radius); background: var(--muted); font-size: 0.875rem; }
  .crs-notes li .badge { justify-self: start; font-variant-numeric: tabular-nums; }
  .crs-qa { display: grid; gap: 1.25rem; margin: 0; padding: 0; list-style: none; }
  .crs-qa li { display: flex; gap: 0.75rem; }
  .crs-qa .avatar { flex: none; inline-size: 2.25rem; block-size: 2.25rem; font-size: 0.75rem; }
  .crs-qa p { margin: 0; font-size: 0.875rem; }
  .crs-qa small { color: var(--muted-foreground); font-size: 0.75rem; }
  .crs-mine { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fill, minmax(min(100%, 16rem), 1fr)); }
  .crs-mine .card { overflow: hidden; padding-block-start: 0; gap: 0.875rem; }
  .crs-mine .card[hidden] { display: none; }
  .crs-mine .card > a { display: block; position: relative; }
  .crs-mine .card > a img { display: block; }
  .crs-mine .card > a::after { content: ''; position: absolute; inset: 0; background: rgb(0 0 0 / 0.35); opacity: 0; transition: opacity 150ms ease; }
  .crs-mine .card > a > span { position: absolute; inset: 0; z-index: 1; display: grid; place-items: center; color: #fff; opacity: 0; transition: opacity 150ms ease; }
  .crs-mine .card > a > span svg { inline-size: 3rem; block-size: 3rem; }
  .crs-mine .card > a:hover::after { opacity: 1; }
  .crs-mine .card > a:hover > span { opacity: 1; }
  .crs-mine .card > a:focus-visible > span { opacity: 1; }
  .crs-mine h3 { margin: 0; font-size: 0.9375rem; }
  .crs-mine .progress { block-size: 0.375rem; }
  .crs-mine-foot { display: flex; justify-content: space-between; align-items: center; gap: 0.5rem; font-size: 0.75rem; color: var(--muted-foreground); }
  .crs-stars-input { display: inline-flex; gap: 0.125rem; color: oklch(0.72 0.16 75); }
  .crs-stars-input svg { inline-size: 0.875rem; block-size: 0.875rem; fill: currentColor; }
  .crs-continue { display: grid; gap: 1.25rem; padding: 1.25rem; border: 1px solid var(--border); border-radius: calc(var(--radius) + 2px); }
  @media (width >= 48rem) { .crs-continue { grid-template-columns: 18rem minmax(0, 1fr); align-items: center; } }
  .crs-continue img { border-radius: var(--radius); }
  .crs-continue h2 { margin: 0; font-size: 1.25rem; }
  .crs-profile { display: grid; gap: 2rem; align-items: start; }
  @media (width >= 56rem) { .crs-profile { grid-template-columns: minmax(0, 1fr) 16rem; } }
  .crs-profile-side { display: grid; justify-items: center; gap: 1rem; text-align: center; }
  .crs-profile-side .avatar { inline-size: 10rem; block-size: 10rem; font-size: 2.5rem; }
  .crs-stat-row { display: flex; flex-wrap: wrap; gap: 2rem; margin: 0; }
  .crs-stat-row dt { font-size: 0.8125rem; color: var(--muted-foreground); }
  .crs-stat-row dd { margin: 0.125rem 0 0; font-size: 1.5rem; font-weight: 700; font-variant-numeric: tabular-nums; }
  .crs-plans { display: grid; gap: 1.25rem; grid-template-columns: repeat(auto-fit, minmax(min(100%, 17rem), 1fr)); align-items: stretch; }
  .crs-plan { position: relative; display: flex; flex-direction: column; gap: 1.25rem; padding: 1.75rem; border: 1px solid var(--border); border-radius: calc(var(--radius) + 4px); background: var(--card); }
  .crs-plan[data-featured] { border-color: var(--primary); box-shadow: 0 0 0 1px var(--primary), 0 20px 40px -24px color-mix(in oklab, var(--primary) 60%, transparent); }
  .crs-plan > .badge { position: absolute; inset-block-start: -0.75rem; inset-inline-start: 1.75rem; }
  .crs-plan h3 { margin: 0; font-size: 1.125rem; }
  .crs-plan p { margin: 0; }
  .crs-plan-price { display: flex; align-items: baseline; gap: 0.25rem; }
  .crs-plan-price strong { font-size: 2.5rem; font-weight: 700; letter-spacing: -0.03em; font-variant-numeric: tabular-nums; }
  .crs-plan-price span { color: var(--muted-foreground); font-size: 0.875rem; }
  .crs-plan ul { display: grid; gap: 0.625rem; margin: 0; padding: 0; list-style: none; font-size: 0.875rem; flex: 1; }
  .crs-plan li { display: flex; gap: 0.625rem; }
  .crs-plan li svg { flex: none; inline-size: 1rem; block-size: 1rem; margin-block-start: 0.1875rem; color: var(--primary); }
  .crs-billing { display: inline-flex; align-items: center; gap: 0.75rem; font-size: 0.875rem; }
  .crs-billing .badge { font-weight: 600; }
  .crs-cert { position: relative; display: grid; gap: 1.5rem; padding: clamp(1.5rem, 5vw, 3.5rem); border: 1px solid var(--border); border-radius: calc(var(--radius) + 4px); background: var(--card); box-shadow: inset 0 0 0 0.5rem var(--background), inset 0 0 0 calc(0.5rem + 1px) var(--border); }
  .crs-cert-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; }
  .crs-cert h2 { margin: 0; font-size: 0.8125rem; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; color: var(--muted-foreground); }
  .crs-cert-name { margin: 0; font-family: var(--font-serif, Georgia, serif); font-size: clamp(2rem, 6vw, 3.25rem); font-weight: 600; letter-spacing: -0.01em; line-height: 1.1; }
  .crs-cert-course { margin: 0; font-size: clamp(1.125rem, 2.5vw, 1.5rem); font-weight: 600; }
  .crs-cert-foot { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-end; gap: 1.5rem; padding-block-start: 1.5rem; border-block-start: 1px solid var(--border); }
  .crs-cert-sign { display: grid; gap: 0.25rem; font-size: 0.8125rem; }
  .crs-cert-sign strong { font-family: var(--font-serif, Georgia, serif); font-size: 1.375rem; font-style: italic; font-weight: 400; }
  .crs-cert-seal { display: grid; place-items: center; inline-size: 6rem; block-size: 6rem; border-radius: 999px; background: var(--primary); color: var(--primary-foreground); box-shadow: 0 0 0 4px var(--background), 0 0 0 5px var(--primary); corner-shape: round; }
  .crs-cert-seal svg { inline-size: 2.75rem; block-size: 2.75rem; }
  .crs-cert-meta { display: grid; gap: 0.125rem; font-size: 0.75rem; color: var(--muted-foreground); }
  .crs-cart-line { display: grid; grid-template-columns: 8rem minmax(0, 1fr) auto; gap: 1rem; padding-block: 1.25rem; border-block-end: 1px solid var(--border); }
  .crs-cart-line p { margin: 0; }
  .crs-cart-line h3 { margin: 0; font-size: 0.9375rem; }
  .crs-cart-actions { display: flex; flex-wrap: wrap; gap: 0.25rem 0.75rem; }
  .crs-cart-actions .btn { padding-inline: 0; }
  .crs-coupon-ok { display: flex; align-items: center; gap: 0.5rem; margin: 0; font-size: 0.8125rem; color: var(--primary); }
  .crs-coupon-ok svg { inline-size: 1rem; block-size: 1rem; }
  .crs-section { display: grid; gap: 1.25rem; }
  .crs-band { display: grid; gap: 1.5rem; align-items: center; padding: clamp(1.5rem, 4vw, 3rem); border-radius: calc(var(--radius) + 6px); color: #fff; background: radial-gradient(120% 120% at 100% 0%, oklch(0.45 0.18 290), oklch(0.22 0.04 275) 60%); }
  @media (width >= 56rem) { .crs-band { grid-template-columns: minmax(0, 1fr) 24rem; } }
  .crs-band h1 { margin: 0; font-size: clamp(2rem, 5vw, 3.25rem); font-weight: 700; letter-spacing: -0.03em; line-height: 1.05; }
  .crs-band p { margin: 0; font-size: 1.0625rem; color: rgb(255 255 255 / 0.85); }
  .crs-band form { display: flex; gap: 0.5rem; padding: 0.375rem; border-radius: 999px; background: #fff; }
  .crs-band form input { flex: 1; min-inline-size: 0; border: 0; padding-inline: 1rem; background: transparent; color: #111; font: inherit; }
  .crs-band form input:focus { outline: none; }
  .crs-band form:focus-within { outline: 3px solid rgb(255 255 255 / 0.5); outline-offset: 2px; }
  .crs-band form .btn { border-radius: 999px; }
  .crs-band-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; text-align: center; }
  .crs-band-stats strong { display: block; font-size: 1.75rem; font-weight: 700; }
  .crs-band-stats span { font-size: 0.8125rem; color: rgb(255 255 255 / 0.75); }
  .crs-teachers { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fill, minmax(min(100%, 11rem), 1fr)); }
  .crs-teacher-tile { position: relative; display: grid; justify-items: center; gap: 0.5rem; padding: 1.25rem 1rem; border: 1px solid var(--border); border-radius: var(--radius); text-align: center; color: inherit; text-decoration: none; transition: border-color 150ms ease, transform 150ms ease; }
  .crs-teacher-tile:hover { border-color: var(--ring); transform: translateY(-2px); }
  .crs-teacher-tile .avatar { inline-size: 4rem; block-size: 4rem; }
  .crs-teacher-tile strong { font-size: 0.9375rem; }
  .crs-teacher-tile small { font-size: 0.75rem; color: var(--muted-foreground); }
  .crs-reel .carousel > ol > li { min-inline-size: 0; }
  html.dark .crs-hero { background: oklch(0.16 0.02 270); }
  html.dark .crs-topbar { background: oklch(0.16 0.02 270); }
"""
CRS = CAT_CSS + FX_CSS + COURSE_CSS


def initials(name):
    return "".join(w[0] for w in name.split()[:2])


def money_or_free(v):
    return "Free" if not v else money(v)


def crs_rate(c):
    return f'<p class="crs-rate"><strong>{c["rating"]}</strong>{stars(c["rating"])}<span>({c["reviews"]:,})</span></p>'


def crs_price(c, size=None):
    sz = f' data-size="{size}"' if size else ""
    was = f'<s>{money(c["was"])}</s><span class="sr-only">Was {money(c["was"])}</span>' if c["was"] else ""
    return f'<p class="crs-price"{sz}><strong>{money_or_free(c["price"])}</strong>{was}</p>'


def crs_badge(c):
    if not c["badge"]:
        return ""
    v = {"Bestseller": ' data-variant="secondary"', "Free": ' data-variant="outline"', "Highest rated": ' data-variant="secondary"'}.get(c["badge"], "")
    return f'<span class="badge"{v}>{c["badge"]}</span>'


def thumb(c, extra=""):
    return f'<img class="shop-shot crs-thumb" src="{PH}" alt=""{f" data-shot={chr(34)}{c["shot"]}{chr(34)}" if c["shot"] > 1 else ""}{extra}>'


def hours(c):
    h = c["hours"]
    return f"{h:g} total hours"


def crs_meta(c):
    return f'<ul class="crs-meta"><li>{hours(c)}</li><li>{c["lectures"]} lectures</li><li>{c["level"]}</li></ul>'


def learn_header(cart=2, current=None):
    nav = "".join(f'<a href="#"{" aria-current=\"page\"" if t == current else ""}>{t}</a>' for t in ["Explore", "Plus", "Teach"])
    return f"""<header class="crs-header">
  <div class="wrapper crs-header-row" data-size="xl">
    {logo("Acme Learn")}
    <form class="input-group crs-header-search" role="search" onsubmit="event.preventDefault()">
      <input type="search" placeholder="What do you want to learn?" aria-label="Search courses">
      <span data-align="start" aria-hidden="true">{si("search")}</span>
    </form>
    <nav class="crs-header-nav" aria-label="Main">
      {nav}
      <a href="#" class="btn" data-variant="ghost" data-size="sm">My learning</a>
      <a href="#" class="btn" data-variant="ghost" data-size="icon" aria-label="Wishlist">{si("heart")}</a>
      <a href="#" class="btn shop-cart-btn" data-variant="ghost" data-size="icon" aria-label="Cart, {cart} courses">{si("shopping-bag")}<span class="shop-count" data-cart-count data-count="{cart}">{cart}</span></a>
      <span class="avatar"><span>OM</span></span>
    </nav>
  </div>
</header>"""


def course_card(c, pop=True):
    learn = "".join(f"<li>{si('check')}<span>{t}</span></li>" for t in c["learn"][:3])
    popup = f"""<div class="crs-pop" role="tooltip" id="pop-{c["id"]}">
      <h4>{c["title"]}</h4>
      <p class="shop-muted">Updated October 2026 · {hours(c)} · {c["level"]}</p>
      <p>{c["sub"]}</p>
      <ul class="crs-learn">{learn}</ul>
      <div class="crs-pop-actions"><button type="button" class="btn" data-add-course="{c["id"]}">Add to cart</button>{wish_btn({"name": c["title"]}, size="icon")}</div>
    </div>""" if pop else ""
    desc = f' aria-describedby="pop-{c["id"]}"' if pop else ""
    return f"""<article class="crs-card" data-course data-cat="{c["cat"]}" data-level="{c["level"]}" data-rating="{c["rating"]}" data-hours="{c["hours"]}" data-price="{c["price"]}" data-students="{c["students"]}">
  <div class="crs-card-media">{thumb(c)}{crs_badge(c)}<span class="crs-dur">{c["hours"]:g}h</span></div>
  <h3><a href="#"{desc}>{c["title"]}</a></h3>
  <p class="crs-by">{c["by"]}</p>
  {crs_rate(c)}
  {crs_price(c)}
  {popup}
</article>"""


ADD_COURSE_JS = """
document.addEventListener('click', (e) => {
  const b = e.target.closest('[data-add-course]');
  if (!b || b.dataset.added) return;
  b.dataset.added = '';
  b.textContent = 'Go to cart';
  b.dataset.variant = 'outline';
  document.querySelectorAll('[data-cart-count]').forEach((el) => { const n = (parseInt(el.textContent, 10) || 0) + 1; el.textContent = n; el.dataset.count = n; });
});
"""
# Udemy-style preview: flip the popover to the other side for cards near the inline end.
POP_JS = """
document.querySelectorAll('.crs-card').forEach((card) => {
  const place = () => {
    const r = card.getBoundingClientRect();
    const rtl = getComputedStyle(card).direction === 'rtl';
    const room = rtl ? r.left : window.innerWidth - r.right;
    card.toggleAttribute('data-flip', room < 340);
  };
  card.addEventListener('pointerenter', place);
  card.addEventListener('focusin', place);
});
"""

CATS = ["All", "Design", "Illustration", "Development", "Photography", "Animation", "Business", "Craft", "Marketing"]
CATALOG_JS = """
document.querySelectorAll('[data-course-filter]').forEach((form) => {
  const grid = document.getElementById(form.dataset.courseFilter);
  const cards = [...grid.querySelectorAll('[data-course]')];
  const pills = document.querySelectorAll('[data-course-cat]');
  const sort = document.querySelector(`[data-course-sort="${form.dataset.courseFilter}"]`);
  let cat = 'All';
  const inRange = (h, r) => { const [a, b] = r.split('-').map(Number); return h >= a && (!b || h < b); };
  const run = () => {
    const fd = new FormData(form);
    const levels = fd.getAll('level'), lengths = fd.getAll('length');
    const rating = Number(fd.get('rating')) || 0;
    const price = fd.get('price') || 'all';
    let n = 0;
    for (const c of cards) {
      const d = c.dataset;
      const ok = (cat === 'All' || d.cat === cat) && (!levels.length || levels.includes(d.level))
        && (!lengths.length || lengths.some((r) => inRange(Number(d.hours), r)))
        && Number(d.rating) >= rating && (price === 'all' || (price === 'free') === (Number(d.price) === 0));
      c.hidden = !ok;
      if (ok) n++;
    }
    document.querySelectorAll('[data-course-count]').forEach((el) => { el.textContent = n + (n === 1 ? ' course' : ' courses'); });
    document.querySelectorAll('[data-course-empty]').forEach((el) => { el.hidden = n > 0; });
  };
  form.addEventListener('input', run);
  form.addEventListener('reset', () => setTimeout(run));
  pills.forEach((p) => p.addEventListener('click', () => {
    cat = p.dataset.courseCat;
    pills.forEach((x) => x.setAttribute('aria-pressed', String(x === p)));
    run();
  }));
  sort?.addEventListener('change', () => {
    const by = { rating: (a, b) => b.dataset.rating - a.dataset.rating, popular: (a, b) => b.dataset.students - a.dataset.students, 'price-asc': (a, b) => a.dataset.price - b.dataset.price, short: (a, b) => a.dataset.hours - b.dataset.hours }[sort.value];
    grid.prepend(...(by ? [...cards].sort(by) : cards));
  });
});
"""
LEVELS = ["Beginner", "Intermediate", "Advanced", "All levels"]
LENGTHS = [("0-3", "0–3 hours"), ("3-6", "3–6 hours"), ("6-17", "6–17 hours"), ("17-", "17+ hours")]
level_count = {l: sum(1 for c in COURSES if c["level"] == l) for l in LEVELS}
course_filters = f"""<form class="shop-filters-panel" id="crs1-form" data-course-filter="crs1-grid" aria-label="Filters" onsubmit="event.preventDefault()">
  <div class="shop-filter-head"><h2 class="shop-section-title">Filter</h2><button type="reset" class="btn" data-variant="link" data-size="sm">Clear</button></div>
  <div class="accordion" data-multiple>
    <details open><summary>Rating</summary><section><div class="shop-check-list" role="radiogroup" aria-label="Rating">{"".join(f'<label><input type="radio" class="input" name="rating" value="{r}">{stars(r)}<span class="shop-rate-label">{r} &amp; up</span></label>' for r in [4.5, 4.0, 3.5])}</div></section></details>
    <details open><summary>Level</summary><section><div class="shop-check-list">{"".join(f'<label><input type="checkbox" class="input" name="level" value="{l}">{l}<span>{level_count[l]}</span></label>' for l in LEVELS)}</div></section></details>
    <details open><summary>Video duration</summary><section><div class="shop-check-list">{"".join(f'<label><input type="checkbox" class="input" name="length" value="{v}">{t}</label>' for v, t in LENGTHS)}</div></section></details>
    <details><summary>Price</summary><section><div class="shop-check-list" role="radiogroup" aria-label="Price">{"".join(f'<label><input type="radio" class="input" name="price" value="{v}"{" checked" if v == "all" else ""}>{t}</label>' for v, t in [("all", "All"), ("paid", "Paid"), ("free", "Free")])}</div></section></details>
  </div>
</form>"""
pills = "".join(f'<button type="button" data-course-cat="{c}" aria-pressed="{"true" if c == "All" else "false"}">{c}</button>' for c in CATS)

add("course-01", "Course 01", "A course catalog: topic pills, filters for rating, level, length and price, sort, and cards with a hover preview.", "course", f"""
{learn_header(current="Explore")}
<main class="wrapper shop-page" data-size="xl">
  <div class="stack" data-gap="6">
    <div class="stack" data-gap="2">
      <h1 class="shop-h1">Explore courses</h1>
      <p class="shop-lead">Learn creative and professional skills from people who do it every day.</p>
    </div>
    <nav class="crs-pills" aria-label="Topics">{pills}</nav>
    <div class="shop-results">
      {course_filters}
      <div class="stack" data-gap="4">
        <div class="shop-toolbar">
          <p class="shop-lead" data-course-count>{len(COURSES)} courses</p>
          <label class="sr-only" for="crs1-sort">Sort by</label>
          <select class="select" id="crs1-sort" data-course-sort="crs1-grid"><option value="">Most relevant</option><option value="popular">Most popular</option><option value="rating">Highest rated</option><option value="price-asc">Lowest price</option><option value="short">Shortest</option></select>
        </div>
        <div class="crs-grid" id="crs1-grid">{"".join(course_card(c) for c in COURSES)}</div>
        <section class="empty" data-course-empty hidden><header><figure>{si("search")}</figure><h3>No courses match</h3><p>Try another topic or clear a filter.</p></header><footer><button type="reset" form="crs1-form" class="btn" data-variant="outline">Clear filters</button></footer></section>
      </div>
    </div>
  </div>
</main>
""", CRS + FILTER_CSS + "\n  @media (width < 56rem) { .shop-filters-panel { display: none; } }\n  .shop-check-list .shop-rate-label { margin-inline-start: 0.25rem; color: var(--muted-foreground); font-size: 0.8125rem; }", scripts=script(CATALOG_JS + POP_JS + ADD_COURSE_JS + WISH_JS))


# ---------------------------------------------------------------- course-02: card styles
def list_card(c):
    return f"""<article class="crs-list-card crs-card" data-course>
  <div class="crs-card-media">{thumb(c)}<span class="crs-dur">{c["hours"]:g}h</span></div>
  <div class="stack" data-gap="1">
    <h3><a href="#">{c["title"]}</a></h3>
    <p class="shop-lead">{c["sub"]}</p>
    <p class="crs-by">{c["by"]}</p>
    {crs_rate(c)}
    {crs_meta(c)}
    <div class="cluster" data-gap="2">{crs_badge(c)}</div>
  </div>
  {crs_price(c)}
</article>"""


def domestika_card(c, pct):
    off = round((1 - c["price"] / c["was"]) * 100) if c["was"] else 0
    return f"""<article class="crs-card crs-dcard">
  <div class="crs-card-media">{thumb(c)}{f'<span class="badge" data-variant="destructive">-{off}%</span>' if off else crs_badge(c)}</div>
  <span class="avatar crs-dcard-avatar"><span>{initials(c["by"])}</span></span>
  <p class="crs-by">A course by <strong>{c["by"]}</strong></p>
  <h3><a href="#">{c["title"]}</a></h3>
  <div class="crs-dcard-stats"><span>{si("users")}{c["students"]:,}</span><span>{si("star")}{pct}% positive</span></div>
  <div class="crs-dcard-buy">{crs_price(c)}<button type="button" class="btn" data-size="sm" data-add-course="{c["id"]}">Add to cart</button></div>
</article>"""


add("course-02", "Course 02", "Course card styles: a list row with details, and Domestika-style cards with the teacher, students and a quick add to cart.", "course", f"""
{learn_header()}
<main class="wrapper shop-page" data-size="xl">
  <div class="stack" data-gap="12">
    <section class="crs-section" aria-labelledby="crs2-a">
      <div class="cluster" data-justify="between"><h2 class="shop-h2" id="crs2-a">Recommended for you</h2><a href="#" class="btn" data-variant="link" data-size="sm">See all{si("arrow-right")}</a></div>
      <div>{"".join(list_card(c) for c in [C["react"], C["brand"], C["excel"]])}</div>
    </section>
    <section class="crs-section" aria-labelledby="crs2-b">
      <div class="cluster" data-justify="between"><h2 class="shop-h2" id="crs2-b">New in illustration and craft</h2><a href="#" class="btn" data-variant="link" data-size="sm">See all{si("arrow-right")}</a></div>
      <div class="crs-grid">{"".join(domestika_card(c, p) for c, p in [(C["watercolor"], 99), (C["ceramics"], 98), (C["motion"], 97), (C["brand"], 98)])}</div>
    </section>
  </div>
</main>
""", CRS + """
  .crs-list-card h3 { font-size: 1rem; }
  .crs-dcard .crs-dcard-avatar { position: relative; z-index: 2; inline-size: 2.75rem; block-size: 2.75rem; margin-block-start: -2rem; margin-inline-start: 0.75rem; box-shadow: 0 0 0 3px var(--background); font-size: 0.8125rem; }
  .crs-dcard .crs-by strong { color: var(--foreground); font-weight: 600; }
  .crs-dcard-stats { display: flex; gap: 1rem; font-size: 0.8125rem; color: var(--muted-foreground); }
  .crs-dcard-stats span { display: inline-flex; align-items: center; gap: 0.375rem; }
  .crs-dcard-stats svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .crs-dcard-buy { position: relative; z-index: 2; display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; margin-block-start: auto; padding-block-start: 0.5rem; border-block-start: 1px solid var(--border); }""", scripts=script(ADD_COURSE_JS))


# ---------------------------------------------------------------- course-03: learning home
def reel_slide(c, i, n):
    return f'<li aria-roledescription="slide" aria-label="{i + 1} of {n}">{course_card(c, pop=False)}</li>'


reel_courses = [C["react"], C["motion"], C["brand"], C["excel"], C["copy"], C["photo"]]
reel = "".join(reel_slide(c, i, len(reel_courses)) for i, c in enumerate(reel_courses))
arrow = lambda d, ic_: f'<button type="button" class="btn rounded-full" data-variant="outline" data-size="icon-sm" data-carousel="{d}" aria-label="{"Previous" if d == "prev" else "Next"} courses">{si(ic_)}</button>'
TEACHERS = [("Lena Ortiz", "Brand designer", "5 courses"), ("Mai Tanaka", "Illustrator", "3 courses"), ("Daniel Rossi", "Senior engineer", "8 courses"), ("Sofia Lind", "Photographer", "4 courses"), ("Hugo Martín", "Ceramist", "2 courses"), ("Grace Kim", "Copywriter", "6 courses")]
add("course-03", "Course 03", "A learning home page: search hero, continue learning, a course carousel with drag and arrows, topics and teachers.", "course", f"""
{learn_header()}
<main class="wrapper shop-page" data-size="xl">
  <div class="stack" data-gap="12">
    <section class="crs-band" aria-labelledby="crs3-title">
      <div class="stack" data-gap="4">
        <h1 id="crs3-title">Learn the skills that shape what you make</h1>
        <p>1,200+ courses taught by working designers, developers and makers. Learn at your pace, on any device.</p>
        <form role="search" onsubmit="event.preventDefault()"><input type="search" placeholder="Try “brand identity” or “watercolor”" aria-label="Search courses"><button type="submit" class="btn">{si("search")}Search</button></form>
      </div>
      <div class="crs-band-stats"><div><strong>1.2k</strong><span>courses</span></div><div><strong>380</strong><span>teachers</span></div><div><strong>4.7</strong><span>average rating</span></div></div>
    </section>
    <section class="crs-continue" aria-labelledby="crs3-cont">
      {thumb(C["react"])}
      <div class="stack" data-gap="3">
        <p class="shop-line-meta">Continue learning · Section 4, lecture 12</p>
        <h2 id="crs3-cont">{C["react"]["title"]}</h2>
        <div class="stack" data-gap="1"><div class="progress" role="progressbar" aria-label="Course progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="42"><span style="width: 42%"></span></div><p class="shop-line-meta">42% complete · 18h 30m left</p></div>
        <div class="cluster" data-gap="2"><a href="#" class="btn">{si("play")}Resume</a><a href="#" class="btn" data-variant="ghost">All my courses</a></div>
      </div>
    </section>
    <section class="crs-section crs-reel" aria-labelledby="crs3-pop">
      <div class="cluster" data-justify="between"><h2 class="shop-h2" id="crs3-pop">Most popular this week</h2><a href="#" class="btn" data-variant="link" data-size="sm">See all{si("arrow-right")}</a></div>
      <section class="carousel" data-items="4" aria-roledescription="carousel" aria-label="Popular courses" style="--carousel-controls-inset: -0.75rem; --carousel-controls-top: 30%">
        <ol>{reel}</ol>
        {arrow("prev", "chevron-left")}{arrow("next", "chevron-right")}
      </section>
    </section>
    <section class="crs-section" aria-labelledby="crs3-topics">
      <h2 class="shop-h2" id="crs3-topics">Browse by topic</h2>
      <nav class="crs-pills" aria-label="Topics">{"".join(f'<button type="button" aria-pressed="false">{c}</button>' for c in CATS[1:])}</nav>
    </section>
    <section class="crs-section" aria-labelledby="crs3-teach">
      <div class="cluster" data-justify="between"><h2 class="shop-h2" id="crs3-teach">Learn from creative pros</h2><a href="#" class="btn" data-variant="link" data-size="sm">All teachers{si("arrow-right")}</a></div>
      <div class="crs-teachers">{"".join(f'<a href="#" class="crs-teacher-tile"><span class="avatar"><span>{initials(n)}</span></span><strong>{n}</strong><small>{r} · {k}</small></a>' for n, r, k in TEACHERS)}</div>
    </section>
  </div>
</main>
""", CRS + "\n  @media (width < 64rem) { .crs-reel .carousel { --per-view: 2.2; } }\n  @media (width < 40rem) { .crs-reel .carousel { --per-view: 1.2; } }", scripts=script(ADD_COURSE_JS))


# ---------------------------------------------------------------- course-04: course page
CURRICULUM = [
    ("Introduction", [("Welcome to the course", "02:14", True), ("What you'll need", "04:05", True), ("How to get the most out of it", "03:30", False)]),
    ("Research and the creative brief", [("Interviewing the client", "11:20", False), ("Mood boards that guide decisions", "09:45", False), ("Writing the brief", "08:12", False), ("Downloadable brief template", "Resource", False)]),
    ("Designing the logo", [("From words to sketches", "14:02", False), ("Refining in Illustrator", "21:37", False), ("Testing at small sizes", "07:48", False)]),
    ("Color, type and the brand book", [("Building a palette", "12:30", False), ("Pairing typefaces", "10:05", False), ("Assembling the brand book", "16:44", True), ("Final project", "Quiz", False)]),
]


def curriculum(sections, open_first=True):
    out = []
    for i, (title, lessons) in enumerate(sections):
        items = "".join(
            f'<li class="crs-lesson">{si("file-text") if d in ("Resource", "Quiz") else si("circle-play")}<span>{t}</span>{"<a href=\"#\" data-preview>Preview</a>" if pv else ""}<time>{d}</time></li>'
            for t, d, pv in lessons)
        mins = sum(int(d.split(":")[0]) for _, d, _ in lessons if ":" in d)
        out.append(f'<details{" open" if i == 0 and open_first else ""}><summary>{si("chevron-down")}<span>{title}</span><small>{len(lessons)} lectures · {mins} min</small></summary><ul>{items}</ul></details>')
    return '<div class="crs-curr" data-curriculum>' + "".join(out) + "</div>"


DETAIL_JS = """
document.querySelectorAll('[data-expand-all]').forEach((b) => {
  const box = document.querySelector('[data-curriculum]');
  b.addEventListener('click', () => {
    const open = b.getAttribute('aria-expanded') !== 'true';
    box.querySelectorAll('details').forEach((d) => { d.open = open; });
    b.setAttribute('aria-expanded', String(open));
    b.textContent = open ? 'Collapse all sections' : 'Expand all sections';
  });
});
document.querySelectorAll('[data-clamp-toggle]').forEach((b) => {
  const box = document.getElementById(b.getAttribute('aria-controls'));
  b.addEventListener('click', () => {
    const open = b.getAttribute('aria-expanded') !== 'true';
    box.toggleAttribute('data-open', open);
    b.setAttribute('aria-expanded', String(open));
    b.firstChild.textContent = open ? 'Show less ' : 'Show more ';
  });
});
document.querySelectorAll('[data-preview]').forEach((a) => a.addEventListener('click', (e) => { e.preventDefault(); document.getElementById('crs4-video').showModal(); }));
"""
VIDEO_JS = """
document.querySelectorAll('.crs-video').forEach((v) => {
  const play = v.querySelector('.crs-play');
  const big = v.querySelector('.crs-video-big');
  const set = (on) => {
    v.toggleAttribute('data-playing', on);
    play.setAttribute('aria-pressed', String(on));
    play.setAttribute('aria-label', on ? 'Pause' : 'Play');
  };
  play.addEventListener('click', () => set(!v.hasAttribute('data-playing')));
  big?.addEventListener('click', () => { set(true); play.focus(); });
});
"""


def video(c, label, pct=0, now="0:00", total="2:14"):
    return f"""<div class="crs-video">
  {thumb(c)}
  <button type="button" class="crs-video-big" aria-label="Play {label}">{si("play")}</button>
  <div class="crs-controls">
    <div class="progress" role="progressbar" aria-label="Video progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{pct}"><span style="width: {pct}%"></span></div>
    <div class="crs-controls-row">
      <button type="button" class="btn crs-play" data-variant="ghost" data-size="icon-sm" aria-pressed="false" aria-label="Play">{si("play")}{si("pause")}</button>
      <button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Rewind 5 seconds">{si("rotate-ccw")}</button>
      <time>{now} / {total}</time>
      <button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Captions">{si("captions")}</button>
      <button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Volume">{si("volume-2")}</button>
      <button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Full screen">{si("maximize")}</button>
    </div>
  </div>
</div>"""


B = C["brand"]
INCLUDES = [("monitor", "7.5 hours on-demand video"), ("file-text", "12 downloadable resources"), ("smartphone", "Access on mobile and TV"), ("infinity", "Full lifetime access"), ("award", "Certificate of completion")]
c4_reviews = [("Hannah K.", 5, "2 weeks ago", "Clear, practical and beautifully paced. I rebranded my own studio while following along."), ("Marco P.", 5, "1 month ago", "The brief template alone was worth it. Lena explains the why behind every decision."), ("Ines R.", 4, "1 month ago", "Great content. I wish the Illustrator part went a little deeper into grids.")]
add("course-04", "Course 04", "A course page: hero, sticky purchase card with a video preview, what you'll learn, curriculum with previews, description, teacher and reviews.", "course", f"""
{learn_header()}
<section class="crs-hero">
  <div class="wrapper crs-hero-in" data-size="xl">
    <nav class="breadcrumb shop-crumbs" aria-label="Breadcrumb"><ol><li><a href="#">Design</a></li>{crumb_sep}<li><a href="#">Branding</a></li>{crumb_sep}<li><span aria-current="page">Brand identity</span></li></ol></nav>
    <h1>{B["title"]}</h1>
    <p>{B["sub"]}</p>
    <div class="cluster" data-gap="3">{crs_badge(B)}{crs_rate(B)}<span class="crs-meta">{B["students"]:,} students</span></div>
    <p>Created by <a href="#" class="crs-inline">{B["by"]}</a></p>
    <ul class="crs-meta"><li>{si("calendar")}Last updated 10/2026</li><li>{si("globe")}English</li><li>{si("captions")}English, Spanish, Vietnamese</li></ul>
  </div>
</section>
<main class="wrapper" data-size="xl">
  <div class="crs-detail">
    <div class="stack" data-gap="8">
      <section class="crs-box" aria-labelledby="crs4-learn">
        <h2 class="shop-h2" id="crs4-learn">What you'll learn</h2>
        <ul class="crs-learn" data-cols="2">{"".join(f"<li>{si('check')}<span>{t}</span></li>" for t in B["learn"] + ["Present work with confidence", "Price and scope branding projects"])}</ul>
      </section>
      <section class="stack" data-gap="4" aria-labelledby="crs4-content">
        <h2 class="shop-h2" id="crs4-content">Course content</h2>
        <div class="crs-curr-head"><span class="shop-muted">4 sections · 14 lectures · 2h 25m total length</span><button type="button" class="btn" data-variant="link" data-size="sm" data-expand-all aria-expanded="false">Expand all sections</button></div>
        {curriculum(CURRICULUM)}
      </section>
      <section class="stack" data-gap="3" aria-labelledby="crs4-req">
        <h2 class="shop-h2" id="crs4-req">Requirements</h2>
        <div class="crs-prose"><ul><li>A computer with Adobe Illustrator (a free trial works)</li><li>Pencil and paper for sketching</li><li>No design experience needed</li></ul></div>
      </section>
      <section class="stack" data-gap="3" aria-labelledby="crs4-desc">
        <h2 class="shop-h2" id="crs4-desc">Description</h2>
        <div class="crs-clamp crs-prose" id="crs4-desc-body">
          <p>A brand is more than a logo. In this course you'll build a complete identity for a real client brief, from the first interview to a brand book you can hand over with confidence.</p>
          <p>We start with research: how to ask the right questions, collect references and turn them into a brief that keeps everyone aligned. Then we sketch, refine and test a logo, choose a palette and a type pairing, and design the touchpoints that make a brand feel consistent.</p>
          <p>Every lesson ends with a short exercise, and the final project is a full brand book in your portfolio.</p>
          <p><strong>Who this course is for:</strong> beginners who want to work in branding, freelancers who want a repeatable process, and founders who want to understand what good branding involves.</p>
        </div>
        <button type="button" class="btn" data-variant="link" data-size="sm" data-clamp-toggle aria-controls="crs4-desc-body" aria-expanded="false">Show more {si("chevron-down")}</button>
      </section>
      <section class="stack" data-gap="4" aria-labelledby="crs4-teacher">
        <h2 class="shop-h2" id="crs4-teacher">Your teacher</h2>
        <div class="crs-teacher">
          <div class="crs-teacher-top"><span class="avatar"><span>LO</span></span><div><h3><a href="#">{B["by"]}</a></h3><p>Brand designer and studio founder</p></div></div>
          <ul class="crs-facts"><li>{si("star")}4.8 instructor rating</li><li>{si("message-square")}9,812 reviews</li><li>{si("users")}64,300 students</li><li>{si("circle-play")}5 courses</li></ul>
          <p class="crs-prose">Lena has spent 12 years building identities for restaurants, festivals and tech start-ups. She runs a small studio in Lisbon and teaches the process she uses with clients every week.</p>
        </div>
      </section>
      <section class="stack" data-gap="4" aria-labelledby="crs4-reviews">
        <h2 class="shop-h2 crs-rating-head" id="crs4-reviews">{si("star")}{B["rating"]} course rating · {B["reviews"]:,} ratings</h2>
        <div class="shop-review">{"".join(f'''<article class="crs-box stack" data-gap="2"><div class="cluster" data-gap="3"><span class="avatar"><span>{initials(n)}</span></span><div><p class="shop-line-name">{n}</p><div class="cluster" data-gap="2">{stars(r)}<small class="shop-line-meta">{w}</small></div></div></div><p>{t}</p></article>''' for n, r, w, t in c4_reviews)}</div>
        <button type="button" class="btn" data-variant="outline">Show all reviews</button>
      </section>
    </div>
    <aside class="card crs-buy" aria-label="Buy this course">
      <button type="button" class="crs-preview" commandfor="crs4-video" command="show-modal">{thumb(B)}<span><span>{si("play")}</span>Preview this course</span></button>
      <section class="stack" data-gap="4">
        <div class="cluster" data-gap="2">{crs_price(B, "lg")}<span class="crs-off">78% off</span></div>
        <p class="crs-timer">{si("clock")}<strong>2 days</strong> left at this price!</p>
        <div class="stack" data-gap="2">
          <div class="cluster" data-gap="2"><button type="button" class="btn shop-grow" data-size="lg" data-add-course="brand">Add to cart</button>{wish_btn({"name": B["title"]}, size="icon-lg")}</div>
          <a href="#" class="btn shop-full" data-variant="outline" data-size="lg">Buy now</a>
        </div>
        <p class="shop-note shop-center">30-day money-back guarantee</p>
        <div class="stack" data-gap="2"><p class="shop-line-name">This course includes:</p><ul class="crs-includes">{"".join(f"<li>{si(i)}<span>{t}</span></li>" for i, t in INCLUDES)}</ul></div>
        <div class="cluster" data-justify="between"><button type="button" class="btn" data-variant="link" data-size="sm">Share</button><button type="button" class="btn" data-variant="link" data-size="sm">Gift this course</button><button type="button" class="btn" data-variant="link" data-size="sm">Apply coupon</button></div>
      </section>
    </aside>
  </div>
</main>
<dialog id="crs4-video" class="dialog" closedby="any" aria-labelledby="crs4-video-title">
  <div class="crs-dialog">
    <header><p class="shop-line-meta">Course preview</p><h2 id="crs4-video-title">{B["title"]}</h2></header>
    <section>{video(B, "the preview")}</section>
    <button type="button" aria-label="Close" commandfor="crs4-video" command="close">{si("x")}</button>
  </div>
</dialog>
""", CRS + """
  .shop-grow { flex: 1; }
  .shop-center { justify-content: center; }
  .crs-dialog { inline-size: min(48rem, calc(100vw - 2rem)); max-inline-size: none; }""", scripts=script(DETAIL_JS + VIDEO_JS + ADD_COURSE_JS + WISH_JS))


# ---------------------------------------------------------------- course-05: learning player
LESSONS = [
    ("Introduction", [("Welcome to the course", "2 min", True), ("What you'll need", "4 min", True), ("How to get the most out of it", "3 min", True)]),
    ("Research and the creative brief", [("Interviewing the client", "11 min", True), ("Mood boards that guide decisions", "10 min", False), ("Writing the brief", "8 min", False)]),
    ("Designing the logo", [("From words to sketches", "14 min", False), ("Refining in Illustrator", "22 min", False), ("Testing at small sizes", "8 min", False)]),
]
flat = [(s, t, d, done) for s, ls in LESSONS for t, d, done in ls]
total_l = len(flat)
done_l = sum(1 for *_, d in flat if d)
side = []
k = 0
for si_, (sec, ls) in enumerate(LESSONS):
    items = []
    for t, d, done in ls:
        cur = k == 4
        items.append(f'<li data-lesson="{k}"{" aria-current=\"true\"" if cur else ""}><input type="checkbox" class="input" aria-label="Mark “{t}” complete"{" checked" if done else ""} data-done><button type="button" data-goto="{k}"><span>{k + 1}. {t}</span><small>{si("circle-play")}{d}</small></button></li>')
        k += 1
    side.append(f'<details{" open" if si_ < 2 else ""}><summary>{si("chevron-down")}<strong>Section {si_ + 1}: {sec}</strong><small data-sec-count>{sum(1 for *_, d in ls if d)} / {len(ls)} · {sum(int(d.split()[0]) for _, d, _ in ls)} min</small></summary><ol>{"".join(items)}</ol></details>')
circ = 2 * 3.14159 * 13
PLAYER_JS = """
(() => {
  const root = document.querySelector('[data-player]');
  if (!root) return;
  const items = [...root.querySelectorAll('[data-lesson]')];
  const title = root.querySelector('[data-lesson-title]');
  const ring = root.querySelector('[data-ring]');
  const label = root.querySelector('[data-progress-label]');
  const C = Number(ring.getAttribute('stroke-dasharray'));
  const sync = () => {
    const done = items.filter((li) => li.querySelector('[data-done]').checked).length;
    ring.setAttribute('stroke-dashoffset', String(C * (1 - done / items.length)));
    label.textContent = `${done} of ${items.length} complete`;
    root.querySelectorAll('details').forEach((d) => {
      const boxes = [...d.querySelectorAll('[data-done]')];
      const c = d.querySelector('[data-sec-count]');
      c.textContent = c.textContent.replace(/^\\d+ \\/ \\d+/, `${boxes.filter((b) => b.checked).length} / ${boxes.length}`);
    });
  };
  const go = (i) => {
    const li = items[Math.max(0, Math.min(items.length - 1, i))];
    items.forEach((x) => x.toggleAttribute('aria-current', x === li));
    if (li.hasAttribute('aria-current')) li.setAttribute('aria-current', 'true');
    li.closest('details').open = true;
    title.textContent = li.querySelector('button span').textContent.replace(/^\\d+\\. /, '');
    root.querySelector('.crs-video')?.removeAttribute('data-playing');
  };
  const current = () => items.findIndex((x) => x.hasAttribute('aria-current'));
  root.addEventListener('change', (e) => { if (e.target.matches('[data-done]')) sync(); });
  // Sections: one button opens or closes them all; it follows the sections' own state.
  const sections = [...root.querySelectorAll('.crs-learn-side details')];
  const all = root.querySelector('[data-sections-toggle]');
  const syncAll = () => {
    const open = sections.every((d) => d.open);
    all.textContent = open ? 'Collapse all' : 'Expand all';
    all.setAttribute('aria-expanded', String(open));
  };
  all.addEventListener('click', () => {
    const open = !sections.every((d) => d.open);
    sections.forEach((d) => { d.open = open; });
    syncAll();
  });
  sections.forEach((d) => d.addEventListener('toggle', syncAll));
  // Hide the whole sidebar for a wider video, and bring it back.
  const page = root.querySelector('.crs-learnpage');
  root.querySelectorAll('[data-side-toggle]').forEach((b) => b.addEventListener('click', () => {
    const hide = !page.hasAttribute('data-side-hidden');
    page.toggleAttribute('data-side-hidden', hide);
    root.querySelector('.crs-side-open').hidden = !hide;
    root.querySelectorAll('[data-side-toggle]').forEach((x) => x.setAttribute('aria-expanded', String(!hide)));
    (hide ? root.querySelector('.crs-side-open') : root.querySelector('.crs-learn-side [data-side-toggle]')).focus();
  }));
  root.addEventListener('click', (e) => {
    const g = e.target.closest('[data-goto]');
    if (g) go(Number(g.dataset.goto));
    const step = e.target.closest('[data-step-lesson]');
    if (step) {
      const i = current();
      if (Number(step.dataset.stepLesson) > 0) items[i].querySelector('[data-done]').checked = true;
      go(i + Number(step.dataset.stepLesson));
      sync();
    }
  });
  const form = root.querySelector('[data-note-form]');
  form?.addEventListener('submit', (e) => {
    e.preventDefault();
    const text = form.elements.note.value.trim();
    if (!text) return;
    const li = document.createElement('li');
    const b = document.createElement('span');
    b.className = 'badge';
    b.dataset.variant = 'outline';
    b.textContent = '4:12 · ' + title.textContent;
    const p = document.createElement('span');
    p.textContent = text;
    li.append(b, p);
    root.querySelector('[data-notes]').prepend(li);
    form.reset();
  });
})();
"""
add("course-05", "Course 05", "A course player: video, progress ring, curriculum with completion checkboxes, next and previous lesson, and tabs for overview, Q&A and notes.", "course", f"""
<div data-player>
  <header class="crs-topbar">
    {logo("Acme Learn")}
    <h1>{B["title"]}</h1>
    <div class="crs-ring"><svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="13"/><circle cx="16" cy="16" r="13" stroke-dasharray="{circ:.2f}" stroke-dashoffset="{circ * (1 - done_l / total_l):.2f}" data-ring/></svg><span data-progress-label>{done_l} of {total_l} complete</span></div>
    <button type="button" class="btn" data-variant="ghost" data-size="icon" aria-label="Share">{si("share-2")}</button>
  </header>
  <div class="crs-learnpage">
    <div class="crs-learn-main">
      <div class="crs-stage">
        {video(B, "the lesson", 35, "3:28", "9:45")}
        <button type="button" class="btn crs-side-open" data-variant="outline" data-size="sm" aria-controls="crs5-side" aria-expanded="true" data-side-toggle hidden>{si("list")}Course content</button>
      </div>
      <div class="cluster" data-justify="between" data-gap="3">
        <div class="stack" data-gap="1"><p class="shop-line-meta">Section 2 · Lecture 5</p><h2 class="shop-h2" data-lesson-title>Mood boards that guide decisions</h2></div>
        <div class="cluster" data-gap="2"><button type="button" class="btn" data-variant="outline" data-step-lesson="-1">{si("chevron-left")}Previous</button><button type="button" class="btn" data-step-lesson="1">Complete and continue{si("chevron-right")}</button></div>
      </div>
      <div class="tabs" id="crs5-tabs">
        <nav role="tablist" aria-orientation="horizontal">
          <button type="button" role="tab" id="crs5-t1" aria-controls="crs5-p1" aria-selected="true" tabindex="0">Overview</button>
          <button type="button" role="tab" id="crs5-t2" aria-controls="crs5-p2" aria-selected="false" tabindex="-1">Q&amp;A</button>
          <button type="button" role="tab" id="crs5-t3" aria-controls="crs5-p3" aria-selected="false" tabindex="-1">Notes</button>
        </nav>
        <div role="tabpanel" id="crs5-p1" aria-labelledby="crs5-t1" tabindex="-1">
          <div class="stack" data-gap="4">
            <p class="crs-prose">Turn your research into two or three mood boards that each tell a different story, then use them to steer the client toward a direction before you draw anything.</p>
            <dl class="crs-stat-row"><div><dt>Skill level</dt><dd class="shop-h2">Beginner</dd></div><div><dt>Students</dt><dd class="shop-h2">{B["students"]:,}</dd></div><div><dt>Lectures</dt><dd class="shop-h2">{B["lectures"]}</dd></div><div><dt>Video</dt><dd class="shop-h2">7.5 hours</dd></div></dl>
          </div>
        </div>
        <div role="tabpanel" id="crs5-p2" aria-labelledby="crs5-t2" tabindex="-1" hidden>
          <ul class="crs-qa">
            <li><span class="avatar"><span>JR</span></span><div class="stack" data-gap="1"><p><strong>How many mood boards do you usually present?</strong></p><p>Three feels like a choice; more becomes noise. Is that the same for small clients?</p><small>Jamie R. · Lecture 5 · 3 replies</small></div></li>
            <li><span class="avatar"><span>LO</span></span><div class="stack" data-gap="1"><p><strong>Teacher answer</strong></p><p>Two or three, yes, even for small clients. Each one should be a clear direction, not a variation.</p><small>Lena Ortiz · Instructor · 2 days ago</small></div></li>
          </ul>
        </div>
        <div role="tabpanel" id="crs5-p3" aria-labelledby="crs5-t3" tabindex="-1" hidden>
          <div class="stack" data-gap="4">
            <form class="stack" data-gap="2" data-note-form>
              <label class="label" for="crs5-note">Create a note at 4:12</label>
              <textarea class="textarea" id="crs5-note" name="note" rows="3" placeholder="What do you want to remember?"></textarea>
              <div class="cluster" data-justify="end"><button type="submit" class="btn" data-size="sm">{si("notebook-pen")}Save note</button></div>
            </form>
            <ul class="crs-notes" data-notes><li><span class="badge" data-variant="outline">2:05 · Interviewing the client</span><span>Ask “what should people feel?” before “what should it look like?”.</span></li></ul>
          </div>
        </div>
      </div>
    </div>
    <aside class="crs-learn-side" id="crs5-side" aria-label="Course content">
      <div class="crs-learn-side-head">
        <div class="cluster" data-justify="between"><h2>Course content</h2><button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Hide course content" aria-controls="crs5-side" aria-expanded="true" data-side-toggle>{si("x")}</button></div>
        <div class="cluster" data-justify="between"><p>{len(LESSONS)} sections · {total_l} lectures</p><button type="button" class="btn" data-variant="link" data-size="sm" data-sections-toggle aria-expanded="false">Expand all</button></div>
      </div>
      {"".join(side)}
    </aside>
  </div>
</div>
""", CRS + """
  .crs-learn-main .tabs [role='tabpanel'] { padding-block-start: 1rem; }
  .crs-stat-row dd.shop-h2 { font-size: 1.125rem; }""", scripts=script(PLAYER_JS + VIDEO_JS))


# ---------------------------------------------------------------- course-06: my learning
MINE = [(C["react"], 42, "progress"), (C["brand"], 100, "done"), (C["watercolor"], 8, "progress"), (C["excel"], 0, "new"), (C["motion"], 100, "done"), (C["photo"], 65, "progress")]


def mine_card(c, pct, state):
    foot = {"done": f'<span class="cluster" data-gap="1">{si("award")}Completed</span><a href="#" class="btn" data-variant="link" data-size="sm">Certificate</a>',
            "new": '<span>Not started</span><span class="crs-stars-input" aria-hidden="true"></span>',
            "progress": f'<span>{pct}% complete</span><span class="crs-stars-input" aria-label="Your rating: 4 stars">{"".join(si("star") for _ in range(4))}</span>'}[state]
    return f"""<article class="card" data-state="{state}">
  <a href="#" aria-label="{"Start" if state == "new" else "Continue"} {c["title"]}">{thumb(c)}<span>{si("circle-play")}</span></a>
  <section class="stack" data-gap="2"><h3>{c["title"]}</h3><p class="crs-by">{c["by"]}</p></section>
  <section class="stack" data-gap="2">
    <div class="progress" role="progressbar" aria-label="Progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{pct}"><span style="width: {pct}%"></span></div>
    <div class="crs-mine-foot">{foot}</div>
  </section>
</article>"""


MINE_JS = """
document.querySelectorAll('[data-mine-filter]').forEach((bar) => {
  const grid = document.getElementById(bar.dataset.mineFilter);
  bar.addEventListener('click', (e) => {
    const b = e.target.closest('button[data-state-filter]');
    if (!b) return;
    bar.querySelectorAll('button').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
    const f = b.dataset.stateFilter;
    grid.querySelectorAll('[data-state]').forEach((c) => { c.hidden = f !== 'all' && c.dataset.state !== f; });
  });
});
"""
add("course-06", "Course 06", "My learning: a weekly goal, stats, and enrolled courses with progress, filters for in progress, not started and completed.", "course", f"""
{learn_header(current=None)}
<main class="wrapper shop-page" data-size="xl">
  <div class="stack" data-gap="8">
    <div class="cluster" data-justify="between" data-align="end" data-gap="4">
      <div class="stack" data-gap="1"><h1 class="shop-h1">My learning</h1><p class="shop-lead">Pick up where you left off.</p></div>
      <div class="crs-box crs-goal">
        <div class="stack" data-gap="1"><p class="shop-line-name">{si("trophy")} Weekly goal</p><p class="shop-line-meta">3 of 5 days · keep your streak going</p></div>
        <div class="crs-week" aria-label="This week: learned on Monday, Tuesday and Thursday">{"".join(f'<span{" data-on" if on else ""}>{d}</span>' for d, on in zip("MTWTFSS", [1, 1, 0, 1, 0, 0, 0]))}</div>
      </div>
    </div>
    <dl class="crs-stat-row"><div><dt>Courses</dt><dd>6</dd></div><div><dt>Hours learned</dt><dd>38.5</dd></div><div><dt>Certificates</dt><dd>2</dd></div><div><dt>Day streak</dt><dd>4</dd></div></dl>
    <div class="crs-pills" role="group" aria-label="Filter courses" data-mine-filter="crs6-grid">{"".join(f'<button type="button" data-state-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{t}</button>' for k, t in [("all", "All courses"), ("progress", "In progress"), ("new", "Not started"), ("done", "Completed")])}</div>
    <div class="crs-mine" id="crs6-grid">{"".join(mine_card(c, p, s_) for c, p, s_ in MINE)}</div>
  </div>
</main>
""", CRS + """
  .crs-goal { display: flex; align-items: center; gap: 1.5rem; padding: 1rem 1.25rem; }
  .crs-goal .shop-line-name { display: flex; align-items: center; gap: 0.375rem; }
  .crs-goal .shop-line-name svg { inline-size: 1rem; block-size: 1rem; color: oklch(0.72 0.16 75); }
  .crs-week { display: flex; gap: 0.375rem; }
  .crs-week span { display: grid; place-items: center; inline-size: 1.75rem; block-size: 1.75rem; border-radius: 999px; border: 1px solid var(--border); font-size: 0.6875rem; font-weight: 600; color: var(--muted-foreground); corner-shape: round; }
  .crs-week span[data-on] { border-color: var(--primary); background: var(--primary); color: var(--primary-foreground); }
  .crs-mine-foot .cluster svg { inline-size: 0.875rem; block-size: 0.875rem; color: var(--primary); }""", scripts=script(MINE_JS))


# ---------------------------------------------------------------- course-07: teacher profile
L_COURSES = [C["brand"], C["copy"], C["motion"]]
add("course-07", "Course 07", "A teacher profile: bio, stats, links, a follow button and the teacher's courses.", "course", f"""
{learn_header()}
<main class="wrapper shop-page" data-size="lg">
  <div class="crs-profile">
    <div class="stack" data-gap="6">
      <div class="stack" data-gap="2">
        <p class="shop-card-cat">Instructor</p>
        <h1 class="shop-h1">Lena Ortiz</h1>
        <p class="shop-lead">Brand designer and founder of Studio Ortiz, Lisbon</p>
        <div class="cluster" data-gap="2"><span class="badge" data-variant="secondary">Top teacher</span><span class="badge" data-variant="outline">Branding</span><span class="badge" data-variant="outline">Typography</span></div>
      </div>
      <dl class="crs-stat-row"><div><dt>Students</dt><dd>64,300</dd></div><div><dt>Reviews</dt><dd>9,812</dd></div><div><dt>Rating</dt><dd>4.8</dd></div><div><dt>Courses</dt><dd>5</dd></div></dl>
      <section class="stack" data-gap="3" aria-labelledby="crs7-about"><h2 class="shop-h2" id="crs7-about">About me</h2>
        <div class="crs-prose"><p>I've spent 12 years building identities for restaurants, festivals and tech start-ups. My studio works with a handful of clients a year, and I teach the same process we use with them.</p><p>My courses are practical: every lesson ends with something you make, and every course ends with a project for your portfolio.</p></div>
      </section>
      <section class="stack" data-gap="4" aria-labelledby="crs7-courses"><h2 class="shop-h2" id="crs7-courses">My courses (5)</h2>
        <div class="crs-grid">{"".join(course_card(c, pop=False) for c in L_COURSES)}</div>
      </section>
    </div>
    <aside class="crs-profile-side">
      <span class="avatar"><span>LO</span></span>
      <button type="button" class="btn shop-full" aria-pressed="false" data-follow>{si("plus")}Follow</button>
      <div class="stack shop-full" data-gap="2">
        <a href="#" class="btn shop-full" data-variant="outline">{si("globe")}Website</a>
        <a href="#" class="btn shop-full" data-variant="outline">{si("mail")}Message</a>
      </div>
      <p class="shop-line-meta">Teaching since 2019 · Replies within a day</p>
    </aside>
  </div>
</main>
""", CRS, scripts=script("""
document.querySelectorAll('[data-follow]').forEach((b) => b.addEventListener('click', () => {
  const on = b.getAttribute('aria-pressed') !== 'true';
  b.setAttribute('aria-pressed', String(on));
  b.lastChild.textContent = on ? 'Following' : 'Follow';
  b.dataset.variant = on ? 'outline' : '';
  if (!on) b.removeAttribute('data-variant');
}));
"""))


# ---------------------------------------------------------------- course-08: plans
PLANS = [
    ("Single courses", 0, 0, "Buy only the courses you want.", ["Lifetime access to each course", "Certificate of completion", "Download resources"], "Browse courses", False, "outline"),
    ("Plus", 12, 96, "Unlimited access for curious people.", ["10,000+ courses, no limits", "New courses every week", "Offline viewing in the app", "Certificates for every course", "Cancel anytime"], "Start 7-day free trial", True, ""),
    ("Teams", 24, 192, "For teams of 5 or more.", ["Everything in Plus", "Admin dashboard and reports", "Assign learning paths", "SSO and invoicing"], "Contact sales", False, "outline"),
]


def plan_card(name, mo, yr, desc, feats, cta, featured, variant):
    price = (f'<div class="crs-plan-price"><strong data-monthly="${mo}" data-yearly="${yr / 12:g}">${yr / 12:g}</strong><span data-monthly="/ month" data-yearly="/ month, billed ${yr} yearly">/ month, billed ${yr} yearly</span></div>'
             if mo else '<div class="crs-plan-price"><strong>From $9.99</strong><span>/ course</span></div>')
    v = f' data-variant="{variant}"' if variant else ""
    return f"""<article class="crs-plan"{" data-featured" if featured else ""}>
  {'<span class="badge">Most popular</span>' if featured else ""}
  <div class="stack" data-gap="1"><h3>{name}</h3><p class="shop-lead">{desc}</p></div>
  {price}
  <ul>{"".join(f"<li>{si('check')}<span>{f}</span></li>" for f in feats)}</ul>
  <a href="#" class="btn"{v} data-size="lg">{cta}</a>
</article>"""


BILLING_JS = """
document.querySelectorAll('[data-billing]').forEach((sw) => {
  const apply = () => {
    const key = sw.checked ? 'yearly' : 'monthly';
    document.querySelectorAll('[data-monthly]').forEach((el) => { el.textContent = el.dataset[key]; });
  };
  sw.addEventListener('change', apply);
});
"""
add("course-08", "Course 08", "Subscription plans with a monthly or yearly switch, a featured plan and an FAQ.", "course", f"""
{learn_header(current="Plus")}
<main class="wrapper shop-page" data-size="lg">
  <div class="stack" data-gap="12">
    <div class="stack shop-center-text" data-gap="3" data-align="center">
      <span class="badge" data-variant="secondary">{si("sparkles")}Acme Learn Plus</span>
      <h1 class="shop-h1">Learn without limits</h1>
      <p class="shop-lead">One subscription, every course. Try it free for 7 days.</p>
      <label class="crs-billing" for="crs8-billing">Monthly <input type="checkbox" role="switch" class="input" id="crs8-billing" data-billing checked> Yearly <span class="badge" data-variant="secondary">Save 33%</span></label>
    </div>
    <div class="crs-plans">{"".join(plan_card(*p) for p in PLANS)}</div>
    <section class="stack" data-gap="4" aria-labelledby="crs8-faq">
      <h2 class="shop-h2" id="crs8-faq">Questions</h2>
      <div class="accordion">
        <details><summary>Can I cancel anytime?</summary><section><p class="shop-lead">Yes. You keep access until the end of the billing period and won't be charged again.</p></section></details>
        <details><summary>Do I keep my certificates?</summary><section><p class="shop-lead">Yes, certificates stay in your account even after you cancel.</p></section></details>
        <details><summary>Is there a student discount?</summary><section><p class="shop-lead">Students get 40% off Plus with a valid school email.</p></section></details>
      </div>
    </section>
  </div>
</main>
""", CRS + "\n  .shop-center-text { text-align: center; }\n  .crs-billing .input { margin-inline: 0.25rem; }\n  .shop-center-text .badge svg { inline-size: 0.875rem; block-size: 0.875rem; }", scripts=script(BILLING_JS))


# ---------------------------------------------------------------- course-09: certificate
CERT_JS = """
document.querySelectorAll('[data-print]').forEach((b) => b.addEventListener('click', () => window.print()));
"""
add("course-09", "Course 09", "A certificate of completion with a verification ID to copy, download, print and share.", "course", f"""
{learn_header()}
<main class="wrapper shop-page" data-size="md">
  <div class="stack" data-gap="6">
    <div class="cluster" data-justify="between" data-gap="3">
      <div class="stack" data-gap="1"><h1 class="shop-h2">Your certificate</h1><p class="shop-line-meta">Completed November 6, 2026 · 7.5 hours</p></div>
      <div class="cluster" data-gap="2">
        <button type="button" class="btn" data-variant="outline" data-print>{si("download")}Download PDF</button>
        <button type="button" class="btn">{si("share-2")}Share</button>
      </div>
    </div>
    <article class="crs-cert" aria-labelledby="crs9-name">
      <div class="crs-cert-top">{logo("Acme Learn")}<div class="crs-cert-meta"><span class="crs-cert-id"><span>Certificate no. <span id="crs9-id">UC-8F3A-29D1</span></span>{copy_btn("#crs9-id", "Copy certificate number")}</span><span>acme.learn/cert/UC-8F3A-29D1</span></div></div>
      <h2>Certificate of completion</h2>
      <p class="crs-cert-name" id="crs9-name">Olivia Martin</p>
      <div class="stack" data-gap="1"><p class="shop-lead">has successfully completed</p><p class="crs-cert-course">{B["title"]}</p><p class="shop-line-meta">14 lectures · 7.5 total hours · Final project approved</p></div>
      <div class="crs-cert-foot">
        <div class="crs-cert-sign"><strong>Lena Ortiz</strong><span class="shop-line-meta">Lena Ortiz, Instructor</span></div>
        <span class="crs-cert-seal" aria-hidden="true">{si("award")}</span>
        <div class="crs-cert-sign"><strong>Acme Learn</strong><span class="shop-line-meta">Issued Nov 6, 2026</span></div>
      </div>
    </article>
    <div class="crs-box cluster" data-justify="between" data-gap="3"><p class="shop-line-name">Add it to your LinkedIn profile</p><a href="#" class="btn" data-variant="outline" data-size="sm">Add to profile</a></div>
  </div>
</main>
""", CRS + SUCCESS_CSS + """
  .crs-cert-id { display: flex; align-items: center; gap: 0.25rem; }
  @media print { .crs-header { display: none; } .crs-cert { box-shadow: none; } }""", scripts=script(CERT_JS))


# ---------------------------------------------------------------- course-10: cart and checkout
CART_C = [C["brand"], C["motion"], C["watercolor"]]
cart_lines = "".join(f"""<li class="crs-cart-line" data-course-line data-price="{c["price"]}" data-was="{c["was"]}">
  {thumb(c)}
  <div class="stack" data-gap="1"><h3>{c["title"]}</h3><p class="crs-by">By {c["by"]}</p>{crs_rate(c)}{crs_meta(c)}
    <div class="crs-cart-actions"><button type="button" class="btn" data-variant="link" data-size="sm" data-remove-course>Remove</button><button type="button" class="btn" data-variant="link" data-size="sm">Save for later</button></div></div>
  {crs_price(c)}
</li>""" for c in CART_C)
sub = sum(c["price"] for c in CART_C)
orig = sum(c["was"] for c in CART_C)
COURSE_CART_JS = """
(() => {
  const root = document.querySelector('[data-course-cart]');
  if (!root) return;
  const fmt = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });
  let coupon = 0;
  const sync = () => {
    const lines = [...root.querySelectorAll('[data-course-line]')];
    const sub = lines.reduce((s, l) => s + Number(l.dataset.price), 0);
    const orig = lines.reduce((s, l) => s + Number(l.dataset.was || l.dataset.price), 0);
    const off = Math.round(sub * coupon * 100) / 100;
    root.querySelector('[data-c-orig]').textContent = fmt.format(orig);
    root.querySelector('[data-c-disc]').textContent = '-' + fmt.format(orig - sub);
    root.querySelector('[data-c-coupon-row]').hidden = !coupon;
    root.querySelector('[data-c-coupon]').textContent = '-' + fmt.format(off);
    root.querySelector('[data-c-total]').textContent = fmt.format(sub - off);
    root.querySelector('[data-c-pay]').textContent = 'Pay ' + fmt.format(sub - off);
    root.querySelectorAll('[data-c-count]').forEach((el) => { el.textContent = lines.length + (lines.length === 1 ? ' course in cart' : ' courses in cart'); });
    document.querySelectorAll('[data-cart-count]').forEach((el) => { el.textContent = lines.length; el.dataset.count = lines.length; });
    root.querySelectorAll('[data-c-filled]').forEach((el) => { el.hidden = !lines.length; });
    root.querySelectorAll('[data-c-empty]').forEach((el) => { el.hidden = !!lines.length; });
  };
  root.addEventListener('click', (e) => {
    const r = e.target.closest('[data-remove-course]');
    if (r) { r.closest('[data-course-line]').remove(); sync(); }
  });
  const form = root.querySelector('[data-coupon-form]');
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const code = form.elements.code.value.trim().toUpperCase();
    const ok = code === 'LEARN20';
    coupon = ok ? 0.2 : 0;
    root.querySelector('[data-coupon-ok]').hidden = !ok;
    root.querySelector('[data-coupon-err]').hidden = ok || !code;
    form.elements.code.toggleAttribute('aria-invalid', !ok && !!code);
    sync();
  });
})();
"""
add("course-10", "Course 10", "A course cart and checkout: remove courses, apply a coupon (try LEARN20), payment choice and a live total.", "course", f"""
{learn_header(cart=3)}
<main class="wrapper shop-page" data-size="xl" data-course-cart>
  <div class="stack" data-gap="6">
    <div class="stack" data-gap="1"><h1 class="shop-h1">Shopping cart</h1><p class="shop-lead" data-c-count>3 courses in cart</p></div>
    <div class="shop-cols" data-c-filled>
      <ul class="shop-lines crs-cart">{cart_lines}</ul>
      <aside class="card shop-sticky" aria-labelledby="crs10-sum">
        <header><h2 id="crs10-sum">Checkout</h2></header>
        <section class="stack" data-gap="4">
          <dl class="shop-summary">
            <div><dt>Original price</dt><dd data-c-orig>{money(orig)}</dd></div>
            <div data-discount><dt>Discounts</dt><dd data-c-disc>-{money(orig - sub)}</dd></div>
            <div data-discount data-c-coupon-row hidden><dt>Coupon LEARN20</dt><dd data-c-coupon>-$0.00</dd></div>
            <div data-total><dt>Total</dt><dd data-c-total>{money(sub)}</dd></div>
          </dl>
          <form class="stack" data-gap="2" data-coupon-form novalidate>
            <label class="label" for="crs10-code">Coupon</label>
            <div class="cluster" data-gap="2"><input class="input shop-grow" id="crs10-code" name="code" type="text" placeholder="Enter coupon" autocomplete="off" aria-describedby="crs10-coupon-msg"><button type="submit" class="btn" data-variant="outline">Apply</button></div>
            <p class="crs-coupon-ok" id="crs10-coupon-msg" data-coupon-ok hidden>{si("circle-check")}LEARN20 applied: 20% off</p>
            <p class="shop-error" data-coupon-err hidden>{si("info")}That coupon isn't valid. Try LEARN20.</p>
          </form>
          <div class="stack" data-gap="2"><span class="label">Payment</span><div data-payment>{choice_cards("crs10-pay", "crs10-pay-", [("card", "Card", "Visa, Mastercard, Amex", ""), ("paypal", "PayPal", "Pay with your PayPal account", ""), ("momo", "MoMo", "Scan to pay with MoMo", "")], label="Payment method")}</div></div>
        </section>
        <footer class="stack" data-gap="3">
          <button type="button" class="btn shop-full" data-size="lg" data-c-pay>Pay {money(sub)}</button>
          <p class="shop-note">{si("lock")}30-day money-back guarantee · Lifetime access</p>
        </footer>
      </aside>
    </div>
    <section class="empty" data-c-empty hidden><header><figure>{si("graduation-cap")}</figure><h3>Your cart is empty</h3><p>Keep exploring to find a course.</p></header><footer><a href="#" class="btn">Explore courses</a></footer></section>
  </div>
</main>
""", CRS + CHOICE_CSS + """
  .shop-grow { flex: 1; min-inline-size: 0; }
  .crs-cart { display: grid; }
  .crs-cart-line > img { border-radius: var(--radius); }
  .crs-cart-line .crs-price { flex-direction: column; align-items: flex-end; gap: 0; }
  @media (width < 40rem) { .crs-cart-line { grid-template-columns: 6rem minmax(0, 1fr); } .crs-cart-line > .crs-price { grid-column: 2; flex-direction: row; align-items: baseline; gap: 0.5rem; } }""", scripts=script(COURSE_CART_JS))


# ================================================================== headers and footers by business
HF_ICONS = {
    "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "instagram": '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8A4 4 0 0 1 16 11.37m1.5-4.87h.01"/>',
    "youtube": '<path d="M2.5 17a24.1 24.1 0 0 1 0-10a2 2 0 0 1 1.4-1.4a49.6 49.6 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24.1 24.1 0 0 1 0 10a2 2 0 0 1-1.4 1.4a49.6 49.6 0 0 1-16.2 0A2 2 0 0 1 2.5 17"/><path d="m10 15l5-3l-5-3z"/>',
    "twitter": '<path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6c2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4c-.9-4.2 4-6.6 7-3.8c1.1 0 3-1.2 3-1.2"/>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2a2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6M2 9h4v12H2z"/><circle cx="4" cy="4" r="2"/>',
    "menu": '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    "arrow-up": '<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>',
    "leaf": '<path d="M11 20a10 10 0 0 0 10-10a25.9 25.9 0 0 0-1.04-7.281a1 1 0 0 0-1.755-.325C15.833 5.5 13 5.5 9.8 6.1A7 7 0 0 0 11 20"/><path d="M2 21a5 5 0 0 1 2.911-4.544C7.613 15.212 8.351 15.24 11 13"/>',
    "baby": '<path d="M10 16c.5.3 1.2.5 2 .5s1.5-.2 2-.5m1-4h.01"/><path d="M19.38 6.813A9 9 0 0 1 20.8 10.2a2 2 0 0 1 0 3.6a9 9 0 0 1-17.6 0a2 2 0 0 1 0-3.6A9 9 0 0 1 12 3c2 0 3.5 1.1 3.5 2.5s-.9 2.5-2 2.5c-.8 0-1.5-.4-1.5-1m-3 5h.01"/>',
    "headphones": '<path d="M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3"/>',
    "flower-2": '<path d="M12 5a3 3 0 1 1 3 3m-3-3a3 3 0 1 0-3 3m3-3v1M9 8a3 3 0 1 0 3 3M9 8h1m5 0a3 3 0 1 1-3 3m3-3h-1m-2 3v-1"/><circle cx="12" cy="8" r="2"/><path d="M12 10v12m0 0c4.2 0 7-1.667 7-5c-4.2 0-7 1.667-7 5m0 0c-4.2 0-7-1.667-7-5c4.2 0 7 1.667 7 5"/>',
    "rabbit": '<path d="M13 16a3 3 0 0 1 2.24 5M18 12h.01"/><path d="M18 21h-8a4 4 0 0 1-4-4a7 7 0 0 1 7-7h.2L9.6 6.4a1 1 0 1 1 2.8-2.8L15.8 7h.2c3.3 0 6 2.7 6 6v1a2 2 0 0 1-2 2h-1a3 3 0 0 0-3 3"/><path d="M20 8.54V4a2 2 0 1 0-4 0v3m-8.388 5.524a3 3 0 1 0-1.6 4.3"/>',
    "recycle": '<path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881a1.79 1.79 0 0 1-.004-1.784L7.196 9.5M11 19h8.203a1.83 1.83 0 0 0 1.556-.89a1.78 1.78 0 0 0 0-1.775l-1.226-2.12"/><path d="m14 16l-3 3l3 3m-5.707-8.404L7.196 9.5L3.1 10.598m6.244-4.787l1.093-1.892A1.83 1.83 0 0 1 11.985 3a1.78 1.78 0 0 1 1.546.888l3.943 6.843"/><path d="m13.378 9.633l4.096 1.098l1.097-4.096"/>',
    "puzzle": '<path d="M15.39 4.39a1 1 0 0 0 1.68-.474a2.5 2.5 0 1 1 3.014 3.015a1 1 0 0 0-.474 1.68l1.683 1.682a2.414 2.414 0 0 1 0 3.414L19.61 15.39a1 1 0 0 1-1.68-.474a2.5 2.5 0 1 0-3.014 3.015a1 1 0 0 1 .474 1.68l-1.683 1.682a2.414 2.414 0 0 1-3.414 0L8.61 19.61a1 1 0 0 0-1.68.474a2.5 2.5 0 1 1-3.014-3.015a1 1 0 0 0 .474-1.68l-1.683-1.682a2.414 2.414 0 0 1 0-3.414L4.39 8.61a1 1 0 0 1 1.68.474a2.5 2.5 0 1 0 3.014-3.015a1 1 0 0 1-.474-1.68l1.683-1.682a2.414 2.414 0 0 1 3.414 0z"/>',
    "rss": '<path d="M4 11a9 9 0 0 1 9 9M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1"/>',
    "store": '<path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4"/><path d="M2 7h20"/><path d="M22 7v3a2 2 0 0 1-2 2a2.7 2.7 0 0 1-1.59-.63a.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 16 12a2.7 2.7 0 0 1-1.59-.63a.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 12 12a2.7 2.7 0 0 1-1.59-.63a.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 8 12a2.7 2.7 0 0 1-1.59-.63a.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 4 12a2 2 0 0 1-2-2V7"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
}
SHOP_ICONS.update(HF_ICONS)

HF_CSS = """
  .hf-demo { min-block-size: 24rem; padding: 3rem 1rem; display: grid; place-items: center; color: var(--muted-foreground); font-size: 0.875rem; background: repeating-linear-gradient(-45deg, var(--muted), var(--muted) 10px, transparent 10px, transparent 20px); }
  .hf-demo p { margin: 0; padding: 0.5rem 1rem; border-radius: var(--radius); background: var(--background); }
  .hf-bar { display: flex; align-items: center; justify-content: center; gap: 0.75rem; min-block-size: 2.25rem; padding: 0.375rem 2.75rem; position: relative; background: var(--biz, var(--primary)); color: var(--biz-fg, var(--primary-foreground)); font-size: 0.8125rem; text-align: center; }
  .hf-bar[hidden] { display: none; }
  .hf-bar a { color: inherit; font-weight: 600; text-underline-offset: 3px; }
  .hf-bar .btn { color: inherit; }
  .hf-bar .btn:hover { background: color-mix(in oklab, currentColor 15%, transparent); color: inherit; }
  .hf-bar-close { position: absolute; inset-inline-end: 0.5rem; }
  .hf-bar-msgs { display: grid; }
  .hf-bar-msgs > span { grid-area: 1 / 1; transition: opacity 250ms ease; }
  .hf-bar-msgs > span:not([data-on]) { opacity: 0; visibility: hidden; }
  .hf-util { border-block-end: 1px solid var(--border); font-size: 0.75rem; color: var(--muted-foreground); }
  .hf-util-row { display: flex; align-items: center; justify-content: space-between; gap: 1rem; min-block-size: 2.25rem; }
  .hf-util a { color: inherit; text-decoration: none; }
  .hf-util a:hover { color: var(--foreground); }
  .hf-util-links { display: flex; align-items: center; gap: 1rem; }
  .hf-util-links span { display: inline-flex; align-items: center; gap: 0.375rem; }
  .hf-util svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .hf-util select { block-size: 1.75rem; padding-block: 0; border: 0; background-color: transparent; font-size: 0.75rem; box-shadow: none; }
  .hf-head { position: sticky; inset-block-start: 0; z-index: 20; border-block-end: 1px solid var(--border); background: color-mix(in oklab, var(--background) 94%, transparent); backdrop-filter: blur(10px); }
  .hf-row { display: flex; align-items: center; gap: 1rem; block-size: 4rem; }
  .hf-row[data-size='lg'] { block-size: 5rem; }
  .hf-nav { display: flex; align-items: center; gap: 0.125rem; }
  .hf-nav > a, .hf-nav > .popover > button { display: inline-flex; align-items: center; gap: 0.25rem; padding: 0.5rem 0.75rem; border: 0; border-radius: var(--radius); background: none; color: var(--muted-foreground); font: inherit; font-size: 0.875rem; font-weight: 500; text-decoration: none; cursor: pointer; }
  .hf-nav > a:hover, .hf-nav > .popover > button:hover, .hf-nav > .popover > button[aria-expanded='true'] { color: var(--foreground); background: var(--accent); }
  .hf-nav > a[aria-current] { color: var(--foreground); }
  .hf-nav > .popover > button svg { inline-size: 0.875rem; block-size: 0.875rem; transition: transform 150ms ease; }
  .hf-nav > a:focus-visible, .hf-nav > .popover > button:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
  .hf-actions { display: flex; align-items: center; gap: 0.25rem; margin-inline-start: auto; }
  .hf-burger { display: none; }
  .hf-mega { inline-size: min(52rem, calc(100vw - 2rem)); padding: 1.25rem; }
  .hf-mega-grid { display: grid; gap: 1.5rem; grid-template-columns: repeat(3, minmax(0, 1fr)) 14rem; }
  .hf-mega h3 { margin: 0 0 0.5rem; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted-foreground); }
  .hf-mega ul { display: grid; gap: 0.125rem; margin: 0; padding: 0; list-style: none; }
  .hf-mega li a { display: block; padding: 0.375rem 0.5rem; margin-inline: -0.5rem; border-radius: calc(var(--radius) - 2px); color: inherit; font-size: 0.875rem; text-decoration: none; }
  .hf-mega li a:hover { background: var(--accent); }
  .hf-mega-promo { position: relative; display: grid; align-content: end; gap: 0.25rem; min-block-size: 12rem; padding: 1rem; overflow: hidden; border-radius: var(--radius); color: #fff; text-decoration: none; }
  .hf-mega-promo img { position: absolute; inset: 0; inline-size: 100%; block-size: 100%; object-fit: cover; }
  .hf-mega-promo::after { content: ''; position: absolute; inset: 0; background: linear-gradient(transparent 30%, rgb(0 0 0 / 0.65)); }
  .hf-mega-promo > :not(img) { position: relative; z-index: 1; }
  .hf-mega-promo strong { font-size: 1rem; }
  .hf-mega-promo span { font-size: 0.8125rem; opacity: 0.9; }
  .hf-catmenu { inline-size: 18rem; padding: 0.375rem; }
  .hf-catmenu a { display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0.625rem; border-radius: calc(var(--radius) - 2px); color: inherit; font-size: 0.875rem; text-decoration: none; }
  .hf-catmenu a:hover { background: var(--accent); }
  .hf-catmenu a svg { inline-size: 1rem; block-size: 1rem; color: var(--muted-foreground); }
  .hf-catmenu a small { margin-inline-start: auto; color: var(--muted-foreground); font-size: 0.75rem; }
  .hf-search { flex: 1; max-inline-size: 36rem; }
  .hf-pill { border-radius: 999px; corner-shape: round; }
  .hf-msearch { padding-block-end: 0.75rem; }
  @media (width >= 64rem) { .hf-msearch { display: none; } }
  .hf-search select { flex: none; inline-size: auto; border: 0; border-inline-end: 1px solid var(--border); border-radius: 0; background-color: transparent; box-shadow: none; font-size: 0.8125rem; }
  .hf-search-combo { display: flex; align-items: center; border: 1px solid var(--input); border-radius: var(--radius); overflow: hidden; }
  .hf-search-combo:focus-within { border-color: var(--ring); box-shadow: 0 0 0 3px color-mix(in oklab, var(--ring) 40%, transparent); }
  .hf-search-combo input { flex: 1; min-inline-size: 0; block-size: 2.5rem; padding-inline: 0.75rem; border: 0; background: transparent; color: inherit; font: inherit; font-size: 0.875rem; }
  .hf-search-combo input:focus { outline: none; }
  .hf-search-combo .btn { border-radius: 0; block-size: 2.5rem; }
  .hf-account { display: flex; align-items: center; gap: 0.5rem; padding: 0.25rem 0.5rem; border-radius: var(--radius); color: inherit; font-size: 0.75rem; line-height: 1.2; text-decoration: none; }
  .hf-account:hover { background: var(--accent); }
  .hf-account svg { inline-size: 1.25rem; block-size: 1.25rem; }
  .hf-account strong { display: block; font-size: 0.8125rem; }
  .hf-sheet nav { display: grid; gap: 0.125rem; }
  .hf-sheet nav > a { padding: 0.625rem 0.75rem; border-radius: var(--radius); color: inherit; font-weight: 500; text-decoration: none; }
  .hf-sheet nav > a:hover { background: var(--accent); }
  .hf-sheet .accordion summary { padding-inline: 0.75rem; font-weight: 500; }
  .hf-sheet .accordion ul { display: grid; gap: 0.125rem; margin: 0; padding: 0 0 0.5rem 0.75rem; list-style: none; }
  .hf-sheet .accordion li a { display: block; padding: 0.5rem 0.75rem; border-radius: var(--radius); color: var(--muted-foreground); font-size: 0.875rem; text-decoration: none; }
  .hf-sheet .accordion li a:hover { background: var(--accent); color: var(--foreground); }
  .hf-sheet > section { display: grid; gap: 1rem; align-content: start; }
  .hf-mast { display: grid; justify-items: center; gap: 0.25rem; padding-block: 1.5rem 1rem; text-align: center; }
  .hf-mast a { color: inherit; text-decoration: none; }
  .hf-mast strong { font-family: var(--font-serif, Georgia, serif); font-size: clamp(2rem, 5vw, 3.25rem); font-weight: 700; letter-spacing: -0.02em; line-height: 1; }
  .hf-mast small { font-size: 0.75rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted-foreground); }
  .hf-catrow { display: flex; justify-content: center; gap: 0.25rem; padding-block: 0.25rem; border-block: 1px solid var(--border); overflow-x: auto; scrollbar-width: none; }
  .hf-catrow a { flex: none; padding: 0.625rem 0.875rem; color: var(--muted-foreground); font-size: 0.8125rem; font-weight: 600; letter-spacing: 0.06em; text-decoration: none; text-transform: uppercase; }
  .hf-catrow a:hover, .hf-catrow a[aria-current] { color: var(--foreground); box-shadow: inset 0 -2px 0 currentColor; }
  .hf-searchbox { display: none; padding-block: 0.75rem; border-block-start: 1px solid var(--border); }
  .hf-head[data-search] .hf-searchbox { display: block; }
  .hf-overlay { position: fixed; inset-inline: 0; inset-block-start: 0; z-index: 30; color: #fff; transition: background-color 250ms ease, color 250ms ease, box-shadow 250ms ease; }
  .hf-overlay[data-scrolled] { background: var(--background); color: var(--foreground); box-shadow: 0 1px 0 var(--border); }
  .hf-overlay .hf-nav > a, .hf-overlay .hf-nav > .popover > button { color: inherit; opacity: 0.85; }
  .hf-overlay .hf-nav > a:hover { opacity: 1; background: color-mix(in oklab, currentColor 12%, transparent); }
  .hf-overlay .btn[data-variant='ghost'] { color: inherit; }
  .hf-overlay .btn[data-variant='ghost']:hover { background: color-mix(in oklab, currentColor 12%, transparent); color: inherit; }
  .hf-overlay .block-logo { color: inherit; }
  .hf-overlay .hf-util { border-color: rgb(255 255 255 / 0.2); color: inherit; opacity: 0.85; }
  .hf-overlay[data-scrolled] .hf-util { display: none; }
  .hf-hero { position: relative; display: grid; align-items: end; min-block-size: 36rem; padding: 8rem 1rem 3rem; color: #fff; }
  .hf-hero > img { position: absolute; inset: 0; inline-size: 100%; block-size: 100%; object-fit: cover; }
  .hf-hero::after { content: ''; position: absolute; inset: 0; background: linear-gradient(rgb(0 0 0 / 0.45), rgb(0 0 0 / 0.15) 40%, rgb(0 0 0 / 0.55)); }
  .hf-hero > div { position: relative; z-index: 1; display: grid; gap: 1rem; max-inline-size: 36rem; }
  .hf-hero h1 { margin: 0; font-family: var(--font-serif, Georgia, serif); font-size: clamp(2.25rem, 6vw, 3.75rem); font-weight: 500; line-height: 1.05; }
  .hf-hero p { margin: 0; opacity: 0.9; }
  .hf-chips { display: flex; justify-content: center; gap: 0.5rem; padding-block: 0.75rem; overflow-x: auto; scrollbar-width: none; }
  .hf-chips a { flex: none; display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; border-radius: 999px; background: var(--chip, var(--muted)); color: var(--chip-fg, var(--foreground)); font-size: 0.875rem; font-weight: 600; text-decoration: none; transition: transform 150ms ease; corner-shape: round; }
  .hf-chips a:hover { transform: translateY(-2px) rotate(-1deg); }
  .hf-chips a svg { inline-size: 1rem; block-size: 1rem; }
  .hf-chips a:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
  .hf-foot { background: var(--foot-bg, var(--muted)); color: var(--foot-fg, var(--foreground)); }
  .hf-foot a:not(.btn, .badge) { color: inherit; text-decoration: none; }
  .hf-foot-cols { display: grid; gap: 2rem; padding-block: 3rem 2rem; }
  @media (width >= 48rem) { .hf-foot-cols { grid-template-columns: minmax(0, 1.4fr) repeat(var(--cols, 4), minmax(0, 1fr)); } }
  .hf-foot-brand { display: grid; gap: 1rem; align-content: start; max-inline-size: 22rem; }
  .hf-foot-brand p { margin: 0; font-size: 0.875rem; color: var(--foot-muted, var(--muted-foreground)); line-height: 1.6; }
  .hf-foot details { border-block-end: 1px solid var(--foot-line, var(--border)); }
  .hf-foot summary { display: flex; align-items: center; justify-content: space-between; padding-block: 0.875rem; font-size: 0.875rem; font-weight: 600; cursor: pointer; list-style: none; }
  .hf-foot summary::-webkit-details-marker { display: none; }
  .hf-foot summary svg { inline-size: 1rem; block-size: 1rem; transition: transform 150ms ease; }
  .hf-foot details[open] > summary svg { transform: rotate(180deg); }
  .hf-foot details ul { display: grid; gap: 0.625rem; margin: 0; padding: 0 0 1rem; list-style: none; font-size: 0.875rem; color: var(--foot-muted, var(--muted-foreground)); }
  .hf-foot details li a:hover { color: var(--foot-fg, var(--foreground)); text-decoration: underline; text-underline-offset: 3px; }
  @media (width >= 48rem) { .hf-foot details { border: 0; } .hf-foot summary { pointer-events: none; padding-block: 0 1rem; } .hf-foot summary svg { display: none; } }
  .hf-social { display: flex; gap: 0.5rem; }
  .hf-social a { display: grid; place-items: center; inline-size: 2.25rem; block-size: 2.25rem; border: 1px solid var(--foot-line, var(--border)); border-radius: 999px; transition: background-color 150ms ease, transform 150ms ease; corner-shape: round; }
  .hf-social a:hover { background: var(--foot-fg, var(--foreground)); color: var(--foot-bg, var(--background)); transform: translateY(-2px); }
  .hf-social a:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
  .hf-social svg { inline-size: 1rem; block-size: 1rem; }
  .hf-bottom { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 1rem; padding-block: 1.25rem; border-block-start: 1px solid var(--foot-line, var(--border)); font-size: 0.8125rem; color: var(--foot-muted, var(--muted-foreground)); }
  .hf-bottom nav { display: flex; flex-wrap: wrap; gap: 1rem; }
  .hf-bottom a:hover { color: var(--foot-fg, var(--foreground)); }
  .hf-pay { display: flex; flex-wrap: wrap; gap: 0.375rem; }
  .hf-pay span { padding: 0.125rem 0.5rem; border: 1px solid var(--foot-line, var(--border)); border-radius: calc(var(--radius) - 4px); background: var(--background); color: var(--foreground); font-size: 0.6875rem; font-weight: 700; letter-spacing: 0.02em; }
  .hf-locale { display: flex; gap: 0.5rem; }
  .hf-locale .select { block-size: 2rem; font-size: 0.8125rem; background-color: transparent; }
  .hf-news { display: grid; gap: 1.25rem; align-items: center; padding-block: 2.5rem; border-block-end: 1px solid var(--foot-line, var(--border)); }
  @media (width >= 48rem) { .hf-news { grid-template-columns: minmax(0, 1fr) minmax(0, 26rem); } }
  .hf-news h2 { margin: 0; font-size: 1.5rem; font-weight: 600; letter-spacing: -0.01em; }
  .hf-news p { margin: 0; color: var(--foot-muted, var(--muted-foreground)); font-size: 0.9375rem; }
  .hf-news form { display: grid; gap: 0.5rem; }
  .hf-news-row { display: flex; gap: 0.5rem; }
  .hf-news-row input { flex: 1; min-inline-size: 0; }
  .hf-news-msg { display: flex; align-items: center; gap: 0.5rem; margin: 0; font-size: 0.8125rem; }
  .hf-news-msg[hidden] { display: none; }
  .hf-news-msg svg { inline-size: 1rem; block-size: 1rem; }
  .hf-news-msg[data-tone='error'] { color: var(--destructive); }
  .hf-news-small { font-size: 0.75rem; color: var(--foot-muted, var(--muted-foreground)); }
  .hf-top { position: fixed; inset-block-end: 1.25rem; inset-inline-end: 1.25rem; z-index: 30; opacity: 0; pointer-events: none; transform: translateY(0.5rem); transition: opacity 200ms ease, transform 200ms ease; }
  .hf-top[data-show] { opacity: 1; pointer-events: auto; transform: none; }
  .hf-values { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(min(100%, 12rem), 1fr)); padding-block: 2rem; border-block-end: 1px solid var(--foot-line, var(--border)); }
  .hf-values div { display: flex; gap: 0.75rem; align-items: center; font-size: 0.875rem; }
  .hf-values svg { flex: none; inline-size: 1.5rem; block-size: 1.5rem; color: var(--biz, var(--primary)); }
  .hf-values strong { display: block; }
  .hf-values span { color: var(--foot-muted, var(--muted-foreground)); font-size: 0.8125rem; }
  .hf-hours { display: grid; gap: 0.375rem; margin: 0; font-size: 0.875rem; }
  .hf-hours div { display: flex; justify-content: space-between; gap: 1rem; }
  .hf-hours dt { color: var(--foot-muted, var(--muted-foreground)); }
  .hf-hours dd { margin: 0; font-variant-numeric: tabular-nums; }
  .hf-hours [data-today] { font-weight: 600; color: var(--foot-fg, var(--foreground)); }
  .hf-hours [data-today] dt { color: inherit; }
  .hf-contact { display: grid; gap: 0.625rem; margin: 0; padding: 0; list-style: none; font-size: 0.875rem; }
  .hf-contact li { display: flex; gap: 0.625rem; align-items: flex-start; }
  .hf-contact svg { flex: none; inline-size: 1rem; block-size: 1rem; margin-block-start: 0.125rem; color: var(--biz, var(--primary)); }
  .hf-map { position: relative; overflow: hidden; min-block-size: 12rem; border-radius: var(--radius); background: color-mix(in oklab, var(--biz, var(--primary)) 10%, var(--background)); }
  .hf-map svg.hf-map-bg { position: absolute; inset: 0; inline-size: 100%; block-size: 100%; color: color-mix(in oklab, var(--biz, var(--primary)) 25%, transparent); }
  .hf-map-pin { position: absolute; inset-block-start: 45%; inset-inline-start: 50%; display: grid; place-items: center; inline-size: 2.5rem; block-size: 2.5rem; translate: -50% -50%; border-radius: 999px; background: var(--biz, var(--primary)); color: #fff; box-shadow: 0 0 0 8px color-mix(in oklab, var(--biz, var(--primary)) 25%, transparent); corner-shape: round; }
  .hf-map-pin svg { inline-size: 1.25rem; block-size: 1.25rem; }
  .hf-map .btn { position: absolute; inset-inline-end: 0.75rem; inset-block-end: 0.75rem; background: var(--background); }
  .hf-wave { display: block; inline-size: 100%; block-size: 3rem; color: var(--foot-bg); }
  .hf-apps { display: flex; flex-wrap: wrap; gap: 0.5rem; }
  .hf-apps a { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.375rem 0.875rem; border: 1px solid var(--foot-line, var(--border)); border-radius: var(--radius); font-size: 0.6875rem; line-height: 1.2; }
  .hf-apps a strong { display: block; font-size: 0.875rem; }
  .hf-apps a svg { inline-size: 1.25rem; block-size: 1.25rem; }
  .hf-tags { display: flex; flex-wrap: wrap; gap: 0.375rem; }
  .hf-posts { display: grid; gap: 0.875rem; margin: 0; padding: 0; list-style: none; }
  .hf-posts a { display: grid; grid-template-columns: 4rem minmax(0, 1fr); gap: 0.75rem; align-items: center; }
  .hf-posts img { inline-size: 4rem; block-size: 3rem; border-radius: calc(var(--radius) - 2px); object-fit: cover; background: var(--muted); }
  .hf-posts strong { display: block; font-size: 0.875rem; font-weight: 500; line-height: 1.35; }
  .hf-posts small { color: var(--foot-muted, var(--muted-foreground)); font-size: 0.75rem; }
  .hf-posts a:hover strong { text-decoration: underline; text-underline-offset: 3px; }
  html.dark .hf-mega-promo img { filter: brightness(0.6); }
  html.dark .hf-hero > img { filter: brightness(0.7); }
  @media (prefers-reduced-motion: reduce) { .hf-bar-msgs > span { transition: none; } }
  .hf-head .block-logo, .hf-overlay .block-logo { flex: none; white-space: nowrap; }
  .hf-foot-dark .btn:not([data-variant]) { background: var(--foot-fg); color: var(--foot-bg); }
  .hf-foot-dark .btn:not([data-variant]):hover { background: color-mix(in oklab, var(--foot-fg) 85%, var(--foot-bg)); }
  @media (width < 48rem) { .hf-foot-cols:has(> details) { gap: 0; } .hf-foot-cols:has(> details) > .hf-foot-brand { margin-block-end: 1.5rem; } }
  @media (width < 64rem) { .hf-nav, .hf-hide-sm { display: none; } .hf-burger { display: inline-flex; } }
  .hf-bnav button { position: relative; display: flex; flex-direction: column; align-items: center; gap: 0.25rem; inline-size: 100%; padding-block: 0.625rem 0.5rem; border: 0; background: none; color: var(--muted-foreground); font: inherit; font-size: 0.6875rem; font-weight: 500; cursor: pointer; -webkit-tap-highlight-color: transparent; }
  .hf-bnav button svg { inline-size: 1.375rem; block-size: 1.375rem; }
  .hf-bnav button:focus-visible { outline: 2px solid var(--ring); outline-offset: -2px; }
  .hf-bnav { max-inline-size: none; }
  .hf-bnav a { padding-block-start: 0.875rem; }
  .hf-bnav button { padding-block-start: 0.875rem; }
  .hf-actions .shop-count { inset-block-start: -0.125rem; inset-inline-end: -0.125rem; }
  @media (width >= 48rem) { .hf-bnav { display: none; } }
  @media (width < 48rem) { .hf-burger.hf-burger { display: none; } body:has(.hf-bnav) { padding-block-end: calc(4rem + env(safe-area-inset-bottom, 0px)); } }
"""


def split_lists(css):
    """One selector per rule, so prune_css can drop each one on its own."""
    def top_split(sel):
        parts, depth, cur = [], 0, ""
        for ch in sel:
            depth += ch == "("
            depth -= ch == ")"
            if ch == "," and depth == 0:
                parts.append(cur.strip())
                cur = ""
            else:
                cur += ch
        return parts + [cur.strip()]

    def rule(r):
        sel, body = r.split("{", 1)
        return " ".join(f"{x} {{{body}" for x in top_split(sel))

    out = []
    for line in css.split("\n"):
        t = line.strip()
        if t.startswith("@media") and t.endswith("}") and t.count("{") >= 2:
            head, inner = t.split("{", 1)
            rules = [r.strip() + " }" for r in inner.rstrip("}").strip().split("}") if r.strip()]
            out.append(f"  {head.strip()} {{ {' '.join(rule(r) for r in rules)} }}")
        elif "{" in t and t.endswith("}") and not t.startswith("@"):
            out.append("\n".join("  " + x.strip() + " }" for x in rule(t).split(" }") if x.strip()))
        else:
            out.append(line)
    return "\n".join(out)


HF_CSS = split_lists(HF_CSS)
HF = CAT_CSS + FX_CSS + HF_CSS

# Behavior shared by the header and footer blocks.
HF_JS = """
// Announcement bar: previous/next messages, dismiss.
document.querySelectorAll('[data-bar]').forEach((bar) => {
  const msgs = [...bar.querySelectorAll('.hf-bar-msgs > span')];
  let i = 0;
  const show = (n) => { i = (n + msgs.length) % msgs.length; msgs.forEach((m, k) => m.toggleAttribute('data-on', k === i)); };
  bar.querySelector('[data-bar-prev]')?.addEventListener('click', () => show(i - 1));
  bar.querySelector('[data-bar-next]')?.addEventListener('click', () => show(i + 1));
  bar.querySelector('[data-bar-close]')?.addEventListener('click', () => { bar.hidden = true; });
});
// Search that opens under the header.
document.querySelectorAll('[data-search-toggle]').forEach((b) => b.addEventListener('click', () => {
  const head = b.closest('.hf-head');
  const open = !head.hasAttribute('data-search');
  head.toggleAttribute('data-search', open);
  b.setAttribute('aria-expanded', String(open));
  if (open) head.querySelector('.hf-searchbox input').focus();
}));
// Header over a hero: solid once the page scrolls.
document.querySelectorAll('[data-overlay]').forEach((h) => {
  const sync = () => h.toggleAttribute('data-scrolled', window.scrollY > 40);
  window.addEventListener('scroll', sync, { passive: true });
  sync();
});
// Newsletter forms: validate the email, then thank.
document.querySelectorAll('[data-newsletter]').forEach((form) => {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const input = form.querySelector('input[type=email]');
    const ok = /^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(input.value.trim());
    input.toggleAttribute('aria-invalid', !ok);
    form.querySelector('[data-news-error]').hidden = ok;
    if (!ok) { input.focus(); return; }
    form.querySelector('[data-news-fields]').hidden = true;
    form.querySelector('[data-news-done]').hidden = false;
  });
});
// Footer link columns: open on wide screens, collapsible on small ones.
(() => {
  const groups = document.querySelectorAll('[data-foot-group]');
  if (!groups.length) return;
  const mq = window.matchMedia('(width >= 48rem)');
  const apply = () => groups.forEach((d) => { d.open = mq.matches; });
  mq.addEventListener('change', apply);
  apply();
})();
// Bottom tab bar: the tapped tab becomes current.
document.querySelectorAll('.hf-bnav').forEach((nav) => nav.addEventListener('click', (e) => {
  const a = e.target.closest('a');
  if (!a) return;
  e.preventDefault();
  nav.querySelectorAll('a[aria-current]').forEach((x) => x.removeAttribute('aria-current'));
  a.setAttribute('aria-current', 'page');
}));
// Back to top.
document.querySelectorAll('[data-to-top]').forEach((b) => {
  const sync = () => b.toggleAttribute('data-show', window.scrollY > 300);
  window.addEventListener('scroll', sync, { passive: true });
  sync();
  b.addEventListener('click', () => window.scrollTo({ top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' }));
});
"""


def demo(text="Page content"):
    return f'<div class="hf-demo"><p>{text}</p></div>'


def bar(msgs, close=True, arrows=True):
    spans = "".join(f'<span{" data-on" if i == 0 else ""}>{m}</span>' for i, m in enumerate(msgs))
    nav = (f'<button type="button" class="btn" data-variant="ghost" data-size="icon-xs" aria-label="Previous message" data-bar-prev>{si("chevron-left")}</button>'
           f'<div class="hf-bar-msgs" aria-live="polite">{spans}</div>'
           f'<button type="button" class="btn" data-variant="ghost" data-size="icon-xs" aria-label="Next message" data-bar-next>{si("chevron-right")}</button>') if arrows and len(msgs) > 1 else f'<div class="hf-bar-msgs">{spans}</div>'
    x = f'<button type="button" class="btn hf-bar-close" data-variant="ghost" data-size="icon-xs" aria-label="Dismiss" data-bar-close>{si("x")}</button>' if close else ""
    return f'<div class="hf-bar" role="region" aria-label="Announcement" data-bar>{nav}{x}</div>'


def social(items=("facebook", "instagram", "youtube", "twitter")):
    names = {"facebook": "Facebook", "instagram": "Instagram", "youtube": "YouTube", "twitter": "X", "linkedin": "LinkedIn"}
    return '<div class="hf-social">' + "".join(f'<a href="#" aria-label="{names[s]}">{si(s)}</a>' for s in items) + "</div>"


def foot_cols(cols):
    return "".join(f'<details data-foot-group open><summary>{t}{si("chevron-down")}</summary><ul>{"".join(f"<li><a href=\"#\">{l}</a></li>" for l in links)}</ul></details>' for t, links in cols)


def newsletter(pid, title, text, cta="Subscribe", note="No spam. Unsubscribe anytime.", done="Thanks! Check your inbox to confirm."):
    return f"""<div class="hf-news">
  <div class="stack" data-gap="2"><h2>{title}</h2><p>{text}</p></div>
  <form data-newsletter novalidate>
    <div data-news-fields class="stack" data-gap="2">
      <div class="hf-news-row"><label class="sr-only" for="{pid}-email">Email</label><input class="input" id="{pid}-email" type="email" placeholder="you@example.com" autocomplete="email" aria-describedby="{pid}-err"><button type="submit" class="btn">{cta}</button></div>
      <p class="hf-news-msg" data-tone="error" id="{pid}-err" data-news-error hidden>{si("info")}Enter a valid email address.</p>
      <span class="hf-news-small">{note}</span>
    </div>
    <p class="hf-news-msg" data-news-done hidden role="status">{si("circle-check")}{done}</p>
  </form>
</div>"""


def sheet(pid, title, groups, links, extra=""):
    acc = "".join(f'<details><summary>{t}</summary><ul>{"".join(f"<li><a href=\"#\">{l}</a></li>" for l in ls)}</ul></details>' for t, ls in groups)
    plain = "".join(f'<a href="#">{l}</a>' for l in links)
    return f"""<dialog id="{pid}" class="sheet hf-sheet" data-side="left" closedby="any" aria-labelledby="{pid}-t">
  <header><h2 id="{pid}-t">{title}</h2></header>
  <section>
    <nav aria-label="Mobile"><div class="accordion">{acc}</div>{plain}</nav>
    {extra}
  </section>
  <button type="button" aria-label="Close menu" commandfor="{pid}" command="close">{si("x")}</button>
</dialog>"""


def burger(pid):
    return f'<button type="button" class="btn hf-burger" data-variant="ghost" data-size="icon" aria-label="Open menu" commandfor="{pid}" command="show-modal">{si("menu")}</button>'


def mega(pid, label, cols, promo_title, promo_text, shot_n=3):
    body = "".join(f'<div><h3>{t}</h3><ul>{"".join(f"<li><a href=\"#\">{l}</a></li>" for l in ls)}</ul></div>' for t, ls in cols)
    return f"""<div class="popover">
  <button type="button" popovertarget="{pid}">{label}{si("chevron-down")}</button>
  <div id="{pid}" class="hf-mega" data-popover popover data-side="bottom" data-align="start">
    <div class="hf-mega-grid">{body}<a href="#" class="hf-mega-promo">{shot(shot_n)}<strong>{promo_title}</strong><span>{promo_text}</span></a></div>
  </div>
</div>"""


def biz_logo(name, ic_):
    return f'<a href="#" class="block-logo"><span class="block-logo-mark">{si(ic_)}</span>{name}</a>'


def hf_bnav(items, current, menu_id, badges=None):
    """Mobile bottom tab bar. The tab named like the sheet opens the sheet."""
    badges = badges or {}
    out = []
    for label, ic_, *menu in items:
        b = badges.get(label)
        badge = f'<span class="shop-count" data-count="{b}">{b}</span>' if b else ""
        inner = f'<span class="shop-nav-icon">{si(ic_)}{badge}</span><span>{label}</span>'
        if menu:
            out.append(f'<li><button type="button" commandfor="{menu_id}" command="show-modal">{inner}</button></li>')
        else:
            cur = ' aria-current="page"' if label == current else ""
            out.append(f'<li><a href="#"{cur}>{inner}</a></li>')
    return f'<nav class="shop-bottom-nav hf-bnav" aria-label="Primary">' + "<ul>" + "".join(out) + "</ul></nav>"


ICON_BTN = lambda ic_, label, extra="": f'<a href="#" class="btn" data-variant="ghost" data-size="icon" aria-label="{label}"{extra}>{si(ic_)}</a>'


def cart_btn(n, ic_="shopping-bag"):
    return f'<a href="#" class="btn shop-cart-btn" data-variant="ghost" data-size="icon" aria-label="Cart, {n} items">{si(ic_)}<span class="shop-count" data-count="{n}">{n}</span></a>'


# ---------------------------------------------------------------- header-01: ecommerce
E_MEGA = [("Women", ["New arrivals", "Dresses", "Knitwear", "Coats and jackets", "Shoes", "Sale"]), ("Men", ["New arrivals", "Shirts", "Knitwear", "Trousers", "Shoes", "Sale"]), ("Home", ["Bedding", "Kitchen", "Lighting", "Decor", "Gifts"])]
add("header-01", "Header 01", "An ecommerce header: rotating announcements, utility bar with locale, search by category, account, wishlist and cart, a mega menu and a mobile menu.", "header", f"""
{bar(["Free shipping on orders over $150", "New season: up to 30% off knitwear · <a href=\"#\">Shop now</a>", "Free returns within 30 days"])}
<div class="hf-util hf-hide-sm"><div class="wrapper hf-util-row" data-size="xl">
  <div class="hf-util-links"><span>{si("truck")}<a href="#">Track order</a></span><span>{si("headphones")}<a href="#">Help</a></span><span>{si("store")}<a href="#">Find a store</a></span></div>
  <div class="hf-util-links"><label class="sr-only" for="h1-cur">Currency</label><select class="select" id="h1-cur"><option>USD $</option><option>EUR €</option><option>VND ₫</option></select><label class="sr-only" for="h1-lang">Language</label><select class="select" id="h1-lang"><option>English</option><option>Tiếng Việt</option></select></div>
</div></div>
<header class="hf-head">
  <div class="wrapper hf-row" data-size="xl" data-row="main">
    {burger("h1-menu")}
    {logo("Acme Store")}
    <form class="hf-search hf-hide-sm" role="search" onsubmit="event.preventDefault()"><div class="hf-search-combo"><label class="sr-only" for="h1-cat">Category</label><select class="select" id="h1-cat"><option>All</option><option>Women</option><option>Men</option><option>Home</option></select><input type="search" placeholder="Search products, brands..." aria-label="Search"><button type="submit" class="btn" aria-label="Search">{si("search")}</button></div></form>
    <div class="hf-actions">
      <a href="#" class="hf-account hf-hide-sm">{si("user")}<span>Hello, sign in<strong>Account</strong></span></a>
      {ICON_BTN("heart", "Wishlist")}
      {cart_btn(3)}
    </div>
  </div>
  <form class="wrapper hf-msearch" role="search" onsubmit="event.preventDefault()"><div class="input-group"><input type="search" placeholder="Search products, brands..." aria-label="Search" id="h1-msearch"><span data-align="start" aria-hidden="true">{si("search")}</span></div></form>
  <div class="wrapper" data-size="xl"><nav class="hf-nav" aria-label="Main">{mega("h1-women", "Women", E_MEGA, "The knit edit", "Soft layers for cool days")}{mega("h1-men", "Men", E_MEGA[::-1][:3], "Weekend shirts", "Linen and cotton, new colors", 2)}<a href="#">Home</a><a href="#">Beauty</a><a href="#">Gifts</a><a href="#" style="color: var(--destructive)">Sale</a></nav></div>
</header>
{sheet("h1-menu", "Menu", E_MEGA, ["Beauty", "Gifts", "Sale", "Track order", "Help"], f'<div class="stack" data-gap="2"><a href="#" class="btn">Sign in</a><a href="#" class="btn" data-variant="outline">Create account</a></div>')}
{hf_bnav([("Home", "house"), ("Categories", "layout-grid", 1), ("Wishlist", "heart"), ("Cart", "shopping-bag"), ("Account", "user")], "Home", "h1-menu", {"Cart": 3})}
{demo()}
""", HF + "\n  .hf-head > .wrapper:last-child { border-block-start: 1px solid var(--border); padding-block: 0.25rem; }\n  @media (width < 64rem) { .hf-head > .wrapper:last-child { display: none; } }", scripts=script(HF_JS))

# ---------------------------------------------------------------- header-02: online courses
CATS2 = [("Design", "layout-grid", 214), ("Development", "monitor", 382), ("Illustration", "pencil", 96), ("Photography", "eye", 121), ("Business", "chart-column", 175), ("Marketing", "trending-up", 88)]
cat_menu = "".join(f'<a href="#">{si(i)}<span>{n}</span><small>{c}</small></a>' for n, i, c in CATS2)
add("header-02", "Header 02", "A header for an online course platform: categories menu, rounded search, Plus and Teach links, and sign in buttons.", "header", f"""
<header class="hf-head">
  <div class="wrapper hf-row" data-size="xl">
    {burger("h2-menu")}
    {biz_logo("Acme Learn", "graduation-cap")}
    <nav class="hf-nav" aria-label="Main"><div class="popover"><button type="button" popovertarget="h2-cats">Categories{si("chevron-down")}</button><div id="h2-cats" class="hf-catmenu" data-popover popover data-side="bottom" data-align="start">{cat_menu}</div></div></nav>
    <form class="input-group hf-search hf-pill hf-hide-sm" role="search" onsubmit="event.preventDefault()"><input type="search" placeholder="What do you want to learn?" aria-label="Search courses"><span data-align="start" aria-hidden="true">{si("search")}</span></form>
    <div class="hf-actions">
      <nav class="hf-nav" aria-label="Secondary"><a href="#">Plus</a><a href="#">Teach on Acme</a></nav>
      {ICON_BTN("shopping-bag", "Cart")}
      <a href="#" class="btn hf-hide-sm" data-variant="outline" data-size="sm">Log in</a>
      <a href="#" class="btn" data-size="sm">Sign up</a>
    </div>
  </div>
  <form class="wrapper hf-msearch" role="search" onsubmit="event.preventDefault()"><div class="input-group hf-pill"><input type="search" placeholder="What do you want to learn?" aria-label="Search" id="h2-msearch"><span data-align="start" aria-hidden="true">{si("search")}</span></div></form>
</header>
{sheet("h2-menu", "Menu", [("Categories", [n for n, _, _ in CATS2])], ["Plus", "Teach on Acme", "Log in"])}
{hf_bnav([("Home", "house"), ("Explore", "layout-grid", 1), ("My learning", "circle-play"), ("Wishlist", "heart"), ("Account", "user")], "Home", "h2-menu")}
{demo()}
""", HF, scripts=script(HF_JS))

# ---------------------------------------------------------------- header-03: blog / magazine
BLOG_CATS = ["Latest", "Design", "Technology", "Culture", "Travel", "Food", "Opinion", "Podcasts"]
add("header-03", "Header 03", "A blog or magazine header: centered masthead with the date, category row, search that opens under the header, theme toggle and subscribe.", "header", f"""
<header class="hf-head" style="position: relative">
  <div class="wrapper hf-row" data-size="lg">
    {burger("h3-menu")}
    <div class="cluster hf-hide-sm" data-gap="1">{ICON_BTN("rss", "RSS feed")}<span class="shop-line-meta">Sunday, November 8, 2026</span></div>
    <div class="hf-actions">
      <button type="button" class="btn" data-variant="ghost" data-size="icon" aria-label="Search" aria-expanded="false" data-search-toggle>{si("search")}</button>
      <button type="button" class="btn" data-variant="ghost" data-size="icon" aria-label="Toggle dark mode" data-theme-toggle>{si("moon")}</button>
      <a href="#" class="btn" data-size="sm">Subscribe</a>
    </div>
  </div>
  <div class="hf-mast"><a href="#"><strong>The Margin</strong></a><small>Ideas, design and the people behind them</small></div>
  <nav class="hf-catrow" aria-label="Sections">{"".join(f'<a href="#"{" aria-current=\"page\"" if c == "Latest" else ""}>{c}</a>' for c in BLOG_CATS)}</nav>
  <div class="hf-searchbox"><form class="wrapper" data-size="md" role="search" onsubmit="event.preventDefault()"><div class="input-group"><input type="search" placeholder="Search articles, authors, topics..." aria-label="Search articles"><span data-align="start" aria-hidden="true">{si("search")}</span></div></form></div>
</header>
{sheet("h3-menu", "Sections", [], BLOG_CATS + ["About", "Newsletter"])}
{hf_bnav([("Home", "house"), ("Sections", "layout-grid", 1), ("Search", "search"), ("Saved", "heart"), ("Account", "user")], "Home", "h3-menu")}
{demo("Article list")}
""", HF + "\n  .hf-head .hf-row { position: relative; }\n  .hf-head .hf-actions { position: absolute; inset-inline-end: 0; }\n  @media (width < 64rem) { .hf-head .hf-actions { position: static; } .hf-catrow { justify-content: flex-start; } }",
    scripts=script(HF_JS + """
document.querySelectorAll('[data-theme-toggle]').forEach((b) => b.addEventListener('click', () => {
  const dark = !document.documentElement.classList.contains('dark');
  document.documentElement.classList.toggle('dark', dark);
  b.setAttribute('aria-pressed', String(dark));
}));
"""))

# ---------------------------------------------------------------- header-04: spa / wellness
SPA = "--biz: oklch(0.52 0.06 150); --biz-fg: #fff;"
add("header-04", "Header 04", "A spa or wellness header over a hero: contact and hours bar, transparent nav that turns solid on scroll, and a Book now button.", "header", f"""
<div style="{SPA}">
  <header class="hf-overlay" data-overlay>
    <div class="hf-util hf-hide-sm"><div class="wrapper hf-util-row" data-size="xl"><div class="hf-util-links"><span>{si("phone")}<a href="#">(555) 014-2290</a></span><span>{si("clock")}Open today 9:00–20:00</span></div><div class="hf-util-links"><span>{si("map-pin")}12 Garden Lane, Portland</span></div></div></div>
    <div class="wrapper hf-row" data-size="xl" data-size-row="lg">
      {burger("h4-menu")}
      {biz_logo("Still Water Spa", "leaf")}
      <nav class="hf-nav" aria-label="Main" style="margin-inline: auto"><a href="#">Treatments</a><a href="#">Packages</a><a href="#">Memberships</a><a href="#">Gift cards</a><a href="#">About</a></nav>
      <div class="hf-actions" style="margin-inline-start: 0"><a href="#" class="btn hf-book" data-size="sm">{si("calendar")}Book now</a></div>
    </div>
  </header>
  <section class="hf-hero">
    {shot(2)}
    <div class="wrapper" data-size="xl" style="max-inline-size: 72rem"><div style="max-inline-size: 36rem" class="stack" data-gap="4"><p class="shop-card-cat" style="color: inherit; opacity: 0.85">Day spa · Portland</p><h1>Slow down. Breathe. Be still.</h1><p>Massage, facials and hot stone rituals in a quiet garden house.</p><div class="cluster" data-gap="2"><a href="#" class="btn hf-book" data-size="lg">Book a treatment</a><a href="#" class="btn" data-variant="outline" data-size="lg" style="background: transparent; color: #fff; border-color: rgb(255 255 255 / 0.6)">View packages</a></div></div></div>
  </section>
  {sheet("h4-menu", "Still Water Spa", [("Treatments", ["Massage", "Facials", "Body rituals", "Hot stone"])], ["Packages", "Memberships", "Gift cards", "About"], '<a href="#" class="btn">Book now</a>')}
{hf_bnav([("Home", "house"), ("Treatments", "leaf", 1), ("Book", "calendar"), ("Gift cards", "gift"), ("Account", "user")], "Home", "h4-menu")}
  {demo("Treatments")}
  {demo("Scroll to see the header turn solid")}
</div>
""", HF + """
  .hf-book { background: var(--biz); color: var(--biz-fg); }
  .hf-book:hover { background: color-mix(in oklab, var(--biz) 85%, black); color: var(--biz-fg); }
  .hf-overlay .hf-row { block-size: 4.5rem; }
  .hf-overlay .block-logo-mark { background: var(--biz); }""", scripts=script(HF_JS))

# ---------------------------------------------------------------- header-05: cosmetics / beauty
BEAUTY = "--biz: oklch(0.62 0.12 10); --biz-fg: #fff;"
B_MEGA = [("Skincare", ["Cleansers", "Serums", "Moisturizers", "Sunscreen", "Masks"]), ("Makeup", ["Foundation", "Concealer", "Lips", "Eyes", "Brushes"]), ("Hair and body", ["Shampoo", "Treatments", "Body care", "Fragrance", "Travel sizes"])]
add("header-05", "Header 05", "A beauty and cosmetics header: soft announcement bar, centered logo, mega menu with a featured product, search, account and bag.", "header", f"""
<div style="{BEAUTY}">
  {bar(["Free samples with every order", "Join Glow Club: 10% off your first order"], close=True)}
  <header class="hf-head">
    <div class="wrapper hf-row hf-beauty-row" data-size="xl">
      <div class="cluster" data-gap="1">{burger("h5-menu")}<button type="button" class="btn" data-variant="ghost" data-size="icon" aria-label="Search" aria-expanded="false" data-search-toggle>{si("search")}</button></div>
      <a href="#" class="hf-beauty-logo">lumière</a>
      <div class="hf-actions">{ICON_BTN("user", "Account")}{ICON_BTN("heart", "Wishlist")}{cart_btn(2)}</div>
    </div>
    <nav class="hf-nav hf-beauty-nav" aria-label="Main">{mega("h5-shop", "Shop", B_MEGA, "Dew Drops serum", "Our bestseller, now in 50 ml", 2)}<a href="#">Bestsellers</a><a href="#">New</a><a href="#">Sets and gifts</a><a href="#">Skin quiz</a><a href="#">Glow Club</a></nav>
    <div class="hf-searchbox"><form class="wrapper" data-size="md" role="search" onsubmit="event.preventDefault()"><div class="input-group"><input type="search" placeholder="Search serums, lipstick, sunscreen..." aria-label="Search products"><span data-align="start" aria-hidden="true">{si("search")}</span></div></form></div>
  </header>
  {sheet("h5-menu", "lumière", B_MEGA, ["Bestsellers", "New", "Sets and gifts", "Skin quiz", "Glow Club"])}
{hf_bnav([("Home", "house"), ("Shop", "layout-grid", 1), ("Skin quiz", "sparkles"), ("Bag", "shopping-bag"), ("Account", "user")], "Home", "h5-menu", {"Bag": 2})}
  {demo()}
</div>
""", HF + """
  .hf-beauty-row { display: grid; grid-template-columns: 1fr auto 1fr; }
  .hf-beauty-row .hf-actions { justify-self: end; }
  @media (width >= 48rem) { .hf-beauty-row .hf-burger { display: inline-flex; } }
  @media (width >= 64rem) { .hf-beauty-row .hf-burger { display: none; } }
  .hf-beauty-logo { color: inherit; font-family: var(--font-serif, Georgia, serif); font-size: 1.75rem; font-style: italic; letter-spacing: 0.02em; text-decoration: none; }
  .hf-beauty-nav { justify-content: center; padding-block-end: 0.5rem; }
  .hf-beauty-nav .hf-mega { --primary: var(--biz); }
  .hf-bar { background: color-mix(in oklab, var(--biz) 14%, var(--background)); color: var(--foreground); }""", scripts=script(HF_JS))

# ---------------------------------------------------------------- header-06: kids / toys
KID_CHIPS = [("0–2 years", "baby", "oklch(0.93 0.06 85)", "oklch(0.35 0.08 70)"), ("3–5 years", "puzzle", "oklch(0.92 0.06 160)", "oklch(0.35 0.08 160)"), ("6–8 years", "sparkles", "oklch(0.92 0.05 250)", "oklch(0.38 0.1 255)"), ("Outdoor play", "sun", "oklch(0.93 0.06 40)", "oklch(0.42 0.12 40)"), ("Books", "book-open", "oklch(0.92 0.05 320)", "oklch(0.4 0.1 320)"), ("Gifts", "gift", "oklch(0.92 0.06 20)", "oklch(0.45 0.14 20)")]
chips = "".join(f'<a href="#" style="--chip: {bg}; --chip-fg: {fg}">{si(i)}{t}</a>' for t, i, bg, fg in KID_CHIPS)
add("header-06", "Header 06", "A playful kids and toys header: free shipping bar, big rounded search, colorful age and category chips, and a mobile menu.", "header", f"""
<div style="--biz: oklch(0.7 0.15 45); --biz-fg: #fff">
  {bar(["🎈 Free shipping over $50 · Free gift wrap", "New: wooden toys that last for years"], close=False)}
  <header class="hf-head hf-kids">
    <div class="wrapper hf-row" data-size="xl" style="block-size: 4.5rem">
      {burger("h6-menu")}
      <a href="#" class="hf-kids-logo"><span>t</span><span>o</span><span>y</span><span>b</span><span>o</span><span>x</span></a>
      <form class="input-group hf-search hf-pill hf-hide-sm" role="search" onsubmit="event.preventDefault()"><input type="search" placeholder="Search toys, books, age..." aria-label="Search toys"><span data-align="start" aria-hidden="true">{si("search")}</span></form>
      <div class="hf-actions">{ICON_BTN("heart", "Wishlist")}{ICON_BTN("user", "Account")}{cart_btn(4)}</div>
    </div>
  <form class="wrapper hf-msearch" role="search" onsubmit="event.preventDefault()"><div class="input-group hf-pill"><input type="search" placeholder="Search toys, books, age..." aria-label="Search" id="h6-msearch"><span data-align="start" aria-hidden="true">{si("search")}</span></div></form>
    <nav class="hf-chips" aria-label="Shop by age and category">{chips}</nav>
  </header>
  {sheet("h6-menu", "toybox", [("Shop by age", ["0–2 years", "3–5 years", "6–8 years", "9+ years"])], ["Outdoor play", "Books", "Gifts", "Sale"])}
{hf_bnav([("Home", "house"), ("Shop", "puzzle", 1), ("Gifts", "gift"), ("Cart", "shopping-bag"), ("Account", "user")], "Home", "h6-menu", {"Cart": 4})}
  {demo()}
</div>
""", HF + """
  .hf-kids .hf-search { block-size: 2.75rem; border-width: 2px; }
  .hf-kids-logo { display: inline-flex; font-size: 1.75rem; font-weight: 800; letter-spacing: -0.04em; text-decoration: none; }
  .hf-kids-logo span:nth-child(1) { color: oklch(0.65 0.18 30); }
  .hf-kids-logo span:nth-child(2) { color: oklch(0.72 0.15 80); }
  .hf-kids-logo span:nth-child(3) { color: oklch(0.62 0.14 160); }
  .hf-kids-logo span:nth-child(4) { color: oklch(0.58 0.16 255); }
  .hf-kids-logo span:nth-child(5) { color: oklch(0.6 0.17 320); }
  .hf-kids-logo span:nth-child(6) { color: oklch(0.65 0.18 30); }
  .hf-kids .shop-count { background: oklch(0.65 0.18 30); }
  .hf-bar { background: var(--biz); color: var(--biz-fg); font-weight: 600; }
  @media (width < 64rem) { .hf-chips { justify-content: flex-start; padding-inline: 1rem; } }""", scripts=script(HF_JS))


# ================================================================== footers
PAY = ["VISA", "Mastercard", "AMEX", "PayPal", "Apple Pay", "MoMo"]
pay = '<div class="hf-pay" aria-label="Payment methods">' + "".join(f"<span>{p}</span>" for p in PAY) + "</div>"
to_top = f'<button type="button" class="btn hf-top" data-variant="outline" data-size="icon" aria-label="Back to top" data-to-top>{si("arrow-up")}</button>'

add("footer-01", "Footer 01", "An ecommerce footer: newsletter with validation, link columns that collapse on mobile, social links, locale, payment methods and back to top.", "footer", f"""
{demo()}
<footer class="hf-foot">
  <div class="wrapper" data-size="xl">
    {newsletter("f1", "Get 10% off your first order", "New arrivals, restocks and members-only offers, twice a month.")}
    <div class="hf-foot-cols" style="--cols: 4">
      <div class="hf-foot-brand">{logo("Acme Store")}<p>Considered pieces for every room and every day. Designed in Portland, made to last.</p>{social()}</div>
      {foot_cols([("Shop", ["New arrivals", "Women", "Men", "Home", "Gift cards", "Sale"]), ("Help", ["Order status", "Shipping", "Returns", "Size guide", "Contact us"]), ("Company", ["About", "Stores", "Careers", "Sustainability", "Press"]), ("Account", ["Sign in", "Create account", "Wishlist", "Rewards"])])}
    </div>
    <div class="hf-bottom"><span>© 2026 Acme Store, Inc.</span><nav aria-label="Legal"><a href="#">Privacy</a><a href="#">Terms</a><a href="#">Cookies</a><a href="#">Accessibility</a></nav>{pay}<div class="hf-locale"><label class="sr-only" for="f1-lang">Language</label><select class="select" id="f1-lang"><option>English</option><option>Tiếng Việt</option></select><label class="sr-only" for="f1-cur">Currency</label><select class="select" id="f1-cur"><option>USD $</option><option>VND ₫</option></select></div></div>
  </div>
</footer>
{to_top}
""", HF, scripts=script(HF_JS))

add("footer-02", "Footer 02", "A footer for an online course platform: teach-on-us call to action, link columns, app download buttons, language and social links.", "footer", f"""
{demo()}
<footer class="hf-foot hf-foot-dark" style="--foot-bg: oklch(0.18 0.02 270); --foot-fg: #fff; --foot-muted: rgb(255 255 255 / 0.65); --foot-line: rgb(255 255 255 / 0.15); --primary: oklch(0.98 0 0); --primary-foreground: oklch(0.18 0.02 270)">
  <div class="wrapper" data-size="xl">
    <div class="hf-news"><div class="stack" data-gap="2"><h2>Teach the world what you know</h2><p>Join 380 teachers earning from their courses on Acme Learn. We help with filming, pricing and promotion.</p></div><div class="cluster" data-gap="2"><a href="#" class="btn" data-size="lg">Become a teacher</a><a href="#" class="btn" data-variant="outline" data-size="lg" style="background: transparent; color: inherit">How it works</a></div></div>
    <div class="hf-foot-cols" style="--cols: 4">
      <div class="hf-foot-brand">{biz_logo("Acme Learn", "graduation-cap")}<p>Creative and professional courses taught by people who do the work every day.</p><div class="hf-apps"><a href="#">{si("smartphone")}<span>Download on the<strong>App Store</strong></span></a><a href="#">{si("play")}<span>Get it on<strong>Google Play</strong></span></a></div></div>
      {foot_cols([("Explore", ["Design", "Development", "Illustration", "Photography", "Business"]), ("Learn", ["Plus subscription", "Gift a course", "Certificates", "For teams"]), ("Teach", ["Become a teacher", "Teacher handbook", "Affiliate program"]), ("Support", ["Help center", "Contact", "Accessibility", "Status"])])}
    </div>
    <div class="hf-bottom"><span>© 2026 Acme Learn</span><nav aria-label="Legal"><a href="#">Terms</a><a href="#">Privacy</a><a href="#">Cookie settings</a></nav><div class="cluster" data-gap="3"><div class="hf-locale"><label class="sr-only" for="f2-lang">Language</label><select class="select" id="f2-lang" style="color: inherit; border-color: var(--foot-line)"><option>English</option><option>Español</option><option>Tiếng Việt</option></select></div>{social(("facebook", "instagram", "youtube", "linkedin"))}</div></div>
  </div>
</footer>
""", HF + "\n  .hf-foot .hf-apps a { color: inherit; }", scripts=script(HF_JS))

POSTS = [("Why slow design is winning again", "Nov 6 · 6 min read", 2), ("Inside the studio: a week with Lena Ortiz", "Nov 3 · 9 min read", 3), ("The best tools for writers in 2026", "Oct 29 · 4 min read", 4)]
posts = "".join(f'<li><a href="#">{shot(n)}<span><strong>{t}</strong><small>{m}</small></span></a></li>' for t, m, n in POSTS)
add("footer-03", "Footer 03", "A blog footer: newsletter signup, about, recent posts, topic tags, social links and RSS.", "footer", f"""
{demo("Article")}
<footer class="hf-foot" style="--foot-bg: var(--background)">
  <div class="wrapper" data-size="lg">
    {newsletter("f3", "The Sunday Margin", "One thoughtful email a week: our best essays, links worth your time and nothing else. 48,000 readers.", "Subscribe", "Free. One email a week.", "You're in. Look for it on Sunday.")}
    <div class="hf-foot-cols" style="--cols: 2; grid-template-columns: repeat(auto-fit, minmax(min(100%, 15rem), 1fr))">
      <div class="hf-foot-brand"><a href="#" style="font-family: var(--font-serif, Georgia, serif); font-size: 1.75rem; font-weight: 700">The Margin</a><p>An independent magazine about design, technology and the people who make things. Reader-supported since 2019.</p>{social(("twitter", "instagram", "linkedin"))}</div>
      <div class="stack" data-gap="3"><h3 class="shop-section-title">Recent posts</h3><ul class="hf-posts">{posts}</ul></div>
      <div class="stack" data-gap="3"><h3 class="shop-section-title">Topics</h3><div class="hf-tags">{"".join(f'<a href="#" class="badge" data-variant="outline">{t}</a>' for t in ["Design", "Technology", "Culture", "Travel", "Food", "Interviews", "Essays", "Podcasts"])}</div></div>
    </div>
    <div class="hf-bottom"><span>© 2026 The Margin</span><nav aria-label="More"><a href="#">About</a><a href="#">Write for us</a><a href="#">Advertise</a><a href="#">Privacy</a><a href="#" class="cluster" data-gap="1">{si("rss")}RSS</a></nav></div>
  </div>
</footer>
""", HF + "\n  .hf-foot { border-block-start: 1px solid var(--border); }\n  .hf-bottom nav a svg { inline-size: 0.875rem; block-size: 0.875rem; }", scripts=script(HF_JS))

HOURS = [("Monday", "Closed"), ("Tue – Fri", "9:00 – 20:00"), ("Saturday", "9:00 – 18:00"), ("Sunday", "10:00 – 16:00")]
hours_html = "".join(f'<div{" data-today" if d == "Tue – Fri" else ""}><dt>{d}</dt><dd>{h}</dd></div>' for d, h in HOURS)
add("footer-04", "Footer 04", "A spa or local business footer: contact details, opening hours with today highlighted, a map with directions, booking and gift cards.", "footer", f"""
{demo()}
<footer class="hf-foot" style="{SPA} --foot-bg: oklch(0.97 0.012 150)">
  <div class="wrapper" data-size="xl">
    <div class="hf-foot-cols" style="grid-template-columns: repeat(auto-fit, minmax(min(100%, 15rem), 1fr))">
      <div class="hf-foot-brand">{biz_logo("Still Water Spa", "leaf")}<p>A quiet garden house for massage, facials and rituals. Come as you are; leave a little lighter.</p><div class="cluster" data-gap="2"><a href="#" class="btn hf-book">{si("calendar")}Book a treatment</a><a href="#" class="btn" data-variant="outline">{si("gift")}Gift cards</a></div></div>
      <div class="stack" data-gap="3"><h3 class="shop-section-title">Visit</h3><ul class="hf-contact"><li>{si("map-pin")}<span>12 Garden Lane<br>Portland, OR 97201</span></li><li>{si("phone")}<a href="#">(555) 014-2290</a></li><li>{si("mail")}<a href="#">hello@stillwater.spa</a></li></ul>{social(("instagram", "facebook"))}</div>
      <div class="stack" data-gap="3"><h3 class="shop-section-title">Opening hours</h3><dl class="hf-hours">{hours_html}</dl><p class="shop-line-meta">Holiday hours may vary.</p></div>
      <div class="hf-map" role="img" aria-label="Map showing 12 Garden Lane"><svg class="hf-map-bg" viewBox="0 0 200 140" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><path d="M0 40h200M0 95h200M60 0v140M140 0v140" stroke="currentColor" stroke-width="6" fill="none"/><path d="M0 120 C60 100 120 130 200 90" stroke="currentColor" stroke-width="10" fill="none" opacity=".6"/></svg><span class="hf-map-pin">{si("leaf")}</span><a href="#" class="btn" data-variant="outline" data-size="sm">{si("map-pin")}Directions</a></div>
    </div>
    <div class="hf-bottom"><span>© 2026 Still Water Spa</span><nav aria-label="Legal"><a href="#">Cancellation policy</a><a href="#">Privacy</a><a href="#">Careers</a></nav></div>
  </div>
</footer>
""", HF + """
  .hf-foot .hf-book { background: var(--biz); color: var(--biz-fg); }
  .hf-foot .hf-book:hover { background: color-mix(in oklab, var(--biz) 85%, black); color: var(--biz-fg); }
  .hf-foot .block-logo-mark { background: var(--biz); }
  html.dark .hf-foot { --foot-bg: oklch(0.2 0.015 150); }""", scripts=script(HF_JS))

VALUES = [("rabbit", "Cruelty-free", "Never tested on animals"), ("leaf", "Clean formulas", "No parabens or sulfates"), ("recycle", "Recyclable", "Glass and refills"), ("truck", "Free shipping", "On orders over $40")]
add("footer-05", "Footer 05", "A beauty footer: brand values strip, newsletter with a welcome discount, link columns, social links and payment methods.", "footer", f"""
{demo()}
<footer class="hf-foot" style="{BEAUTY} --foot-bg: oklch(0.97 0.015 10)">
  <div class="wrapper" data-size="xl">
    <div class="hf-values">{"".join(f'<div>{si(i)}<p class="shop-line-name"><strong>{t}</strong><span>{d}</span></p></div>' for i, t, d in VALUES)}</div>
    {newsletter("f5", "Join Glow Club, get 10% off", "Skin tips, early access to launches and a welcome code for your first order.", "Join", "By joining you agree to our privacy policy.", "Welcome to Glow Club! Your code is on its way.")}
    <div class="hf-foot-cols" style="--cols: 3">
      <div class="hf-foot-brand"><a href="#" class="hf-beauty-logo">lumière</a><p>Effective skincare with honest ingredients, made in small batches in France.</p>{social(("instagram", "youtube", "facebook"))}</div>
      {foot_cols([("Shop", ["Skincare", "Makeup", "Hair and body", "Sets and gifts", "Bestsellers"]), ("Help", ["Shipping", "Returns", "Skin quiz", "FAQ", "Contact"]), ("About", ["Our story", "Ingredients", "Sustainability", "Stockists"])])}
    </div>
    <div class="hf-bottom"><span>© 2026 lumière</span><nav aria-label="Legal"><a href="#">Privacy</a><a href="#">Terms</a></nav>{pay}</div>
  </div>
</footer>
""", HF + """
  .hf-beauty-logo { font-family: var(--font-serif, Georgia, serif); font-size: 1.75rem; font-style: italic; }
  .hf-news .btn[type=submit] { background: var(--biz); color: var(--biz-fg); }
  html.dark .hf-foot { --foot-bg: oklch(0.2 0.02 10); }""", scripts=script(HF_JS))

add("footer-06", "Footer 06", "A playful kids footer: wave edge, club newsletter, colorful columns, safety badges and social links.", "footer", f"""
{demo()}
<footer class="hf-foot hf-kids-foot" style="--foot-bg: oklch(0.32 0.09 265); --foot-fg: #fff; --foot-muted: rgb(255 255 255 / 0.7); --foot-line: rgb(255 255 255 / 0.18); --biz: oklch(0.82 0.15 85)">
  <svg class="hf-wave" viewBox="0 0 1200 48" preserveAspectRatio="none" aria-hidden="true"><path d="M0 48V24C100 0 200 0 300 24s200 24 300 0 200-24 300 0 200 24 300 0v24z" fill="currentColor"/></svg>
  <div class="wrapper" data-size="xl">
    {newsletter("f6", "Join the toybox club 🎉", "Birthday surprises, play ideas and first dibs on new toys.", "Join the club", "For grown-ups only: we never email children.", "Yay! Welcome to the club.")}
    <div class="hf-foot-cols" style="--cols: 3">
      <div class="hf-foot-brand"><a href="#" class="hf-kids-logo"><span>t</span><span>o</span><span>y</span><span>b</span><span>o</span><span>x</span></a><p>Wooden toys, books and outdoor fun, chosen by parents and tested by kids.</p><div class="cluster" data-gap="2"><span class="badge" data-variant="secondary">{si("shield-check")}Safety tested</span><span class="badge" data-variant="secondary">{si("leaf")}FSC wood</span></div></div>
      {foot_cols([("Shop", ["By age", "Outdoor play", "Books", "Gifts", "Sale"]), ("Help", ["Shipping", "Returns", "Gift wrap", "Contact"]), ("About", ["Our story", "Toy safety", "Stores", "Careers"])])}
    </div>
    <div class="hf-bottom"><span>© 2026 toybox</span>{social(("instagram", "facebook", "youtube"))}</div>
  </div>
</footer>
{to_top}
""", HF + """
  .hf-kids-foot { background: transparent; }
  .hf-kids-foot > .wrapper { background: var(--foot-bg); max-inline-size: none; padding-inline: max(1rem, calc((100% - 90rem) / 2 + 1rem)); }
  .hf-wave { color: var(--foot-bg); margin-block-end: -1px; }
  .hf-kids-logo { display: inline-flex; font-size: 1.75rem; font-weight: 800; letter-spacing: -0.04em; }
  .hf-kids-logo span:nth-child(1) { color: oklch(0.75 0.17 30); }
  .hf-kids-logo span:nth-child(2) { color: oklch(0.85 0.15 85); }
  .hf-kids-logo span:nth-child(3) { color: oklch(0.78 0.14 160); }
  .hf-kids-logo span:nth-child(4) { color: oklch(0.75 0.14 230); }
  .hf-kids-logo span:nth-child(5) { color: oklch(0.75 0.15 320); }
  .hf-kids-logo span:nth-child(6) { color: oklch(0.75 0.17 30); }
  .hf-kids-foot .hf-news .btn[type=submit] { background: var(--biz); color: oklch(0.25 0.06 85); }
  .hf-kids-foot .badge svg { inline-size: 0.75rem; block-size: 0.75rem; }""", scripts=script(HF_JS))


# ================================================================== LMS admin (instructor dashboard)
ADM_ICONS = {
    "grip-vertical": '<circle cx="9" cy="12" r="1"/><circle cx="9" cy="5" r="1"/><circle cx="9" cy="19" r="1"/><circle cx="15" cy="12" r="1"/><circle cx="15" cy="5" r="1"/><circle cx="15" cy="19" r="1"/>',
    "ellipsis": '<circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/>',
    "image": '<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>',
    "video": '<path d="m16 13 5.223 3.482a.5.5 0 0 0 .777-.416V7.87a.5.5 0 0 0-.752-.432L16 10.5"/><rect width="14" height="12" x="2" y="6" rx="2"/>',
    "bold": '<path d="M6 12h9a4 4 0 0 1 0 8H7a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h7a4 4 0 0 1 0 8"/>',
    "italic": '<line x1="19" x2="10" y1="4" y2="4"/><line x1="14" x2="5" y1="20" y2="20"/><line x1="15" x2="9" y1="4" y2="20"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "list-ordered": '<path d="M11 5h10m-10 7h10m-10 7h10M4 4h1v5M4 9h2m.5 11H3.4c0-1 2.6-1.925 2.6-3.5a1.5 1.5 0 0 0-2.6-1.02"/>',
    "heading-2": '<path d="M4 12h8m-8 6V6m8 12V6m9 12h-4c0-4 4-3 4-6c0-1.5-2-2.5-4-1"/>',
    "flag": '<path d="M4 22V4a1 1 0 0 1 .4-.8A6 6 0 0 1 8 2c3 0 5 2 7.333 2q2 0 3.067-.8A1 1 0 0 1 20 4v10a1 1 0 0 1-.4.8A6 6 0 0 1 16 16c-3 0-5-2-8-2a6 6 0 0 0-4 1.528"/>',
    "tag": '<path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"/><circle cx="7.5" cy="7.5" r=".5" fill="currentColor"/>',
    "ticket-percent": '<path d="M2 9a3 3 0 1 1 0 6v2a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-2a3 3 0 1 1 0-6V7a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M9 9h.01"/><path d="m15 9-6 6"/><path d="M15 15h.01"/>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/>',
    "eye-off": '<path d="M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49"/><path d="M14.084 14.158a3 3 0 0 1-4.242-4.242"/><path d="M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143"/><path d="m2 2 20 20"/>',
    "cloud-upload": '<path d="M12 13v8m-8-6.101A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="m8 17 4-4 4 4"/>',
    "quote": '<path d="M16 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2a1 1 0 0 1 1 1v1a2 2 0 0 1-2 2a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1a6 6 0 0 0 6-6V5a2 2 0 0 0-2-2zM5 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2a1 1 0 0 1 1 1v1a2 2 0 0 1-2 2a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1a6 6 0 0 0 6-6V5a2 2 0 0 0-2-2z"/>',
    "code": '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>',
    "circle-x": '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6m0-6 6 6"/>',
    "copy-plus": '<path d="M15 12v6m-3-3h6"/><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
    "refresh-cw": '<path d="M3 12a9 9 0 0 1 9-9a9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5m5 4a9 9 0 0 1-9 9a9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
    "list-checks": '<path d="M13 5h8m-8 7h8m-8 7h8M3 17l2 2 4-4M3 7l2 2 4-4"/>',
    "paperclip": '<path d="m16 6-8.414 8.586a2 2 0 0 0 2.829 2.829l8.414-8.586a4 4 0 1 0-5.657-5.657l-8.379 8.551a6 6 0 1 0 8.485 8.485l8.379-8.551"/>',
    "dollar-sign": '<path d="M12 3v18m5-16H9.5a1 1 0 0 0 0 7h5a1 1 0 0 1 0 7H6"/>',
    "reply": '<path d="M20 18v-2a4 4 0 0 0-4-4H4"/><path d="m9 17-5-5 5-5"/>',
    "send": '<path d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"/><path d="m21.854 2.147-10.94 10.939"/>',
    "circle-alert": '<circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/>',
}
SHOP_ICONS.update(ADM_ICONS)

ADM_CSS = """
  body { min-block-size: 100svh; }
  .adm-mark { display: inline-flex; flex: none; align-items: center; justify-content: center; inline-size: 2rem; block-size: 2rem; border-radius: calc(var(--radius) + 2px); background: var(--sidebar-primary); color: var(--sidebar-primary-foreground); }
  .adm-mark svg { inline-size: 1rem; block-size: 1rem; }
  .adm-main { container-type: inline-size; min-inline-size: 0; }
  .adm-header { position: sticky; inset-block-start: 0; z-index: 10; display: flex; align-items: center; gap: 0.5rem; block-size: 3.5rem; padding-inline: 1rem; border-block-end: 1px solid var(--border); background: var(--background); }
  .adm-header > hr { align-self: center; block-size: 1rem; margin-inline-end: 0.25rem; }
  .adm-header .breadcrumb { min-inline-size: 0; }
  .adm-header-end { display: flex; align-items: center; gap: 0.5rem; margin-inline-start: auto; }
  .adm-body { display: grid; grid-template-columns: minmax(0, 1fr); gap: 1.5rem; padding: 1rem; }
  .adm-split > * { min-inline-size: 0; }
  .adm-body > * { min-inline-size: 0; }
  .adm-main .card { min-inline-size: 0; }
  .adm-main .card > section { min-inline-size: 0; }
  .adm-dash > * { min-inline-size: 0; }
  .adm-main .stack > * { min-inline-size: 0; }
  .adm-main .card > section > * { min-inline-size: 0; }
  .adm-top > section { position: relative; overflow-x: auto; }
  @container (width >= 48rem) { .adm-body { padding: 1.5rem; } }
  .adm-title { display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 1rem; }
  .adm-title h1 { margin: 0; font-size: 1.5rem; font-weight: 600; letter-spacing: -0.01em; }
  .adm-title p { margin: 0.25rem 0 0; color: var(--muted-foreground); font-size: 0.875rem; }
  .adm-title > div:last-child { display: flex; flex-wrap: wrap; gap: 0.5rem; }
  .adm-toolbar { display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem; }
  .adm-toolbar .input-group { inline-size: min(100%, 18rem); }
  .adm-toolbar .select { inline-size: auto; }
  .adm-grow { flex: 1; }
  .adm-tabs { display: flex; gap: 0.25rem; overflow-x: auto; border-block-end: 1px solid var(--border); scrollbar-width: none; }
  .adm-tabs button { display: inline-flex; align-items: center; gap: 0.375rem; padding: 0.5rem 0.75rem; border: 0; border-block-end: 2px solid transparent; margin-block-end: -1px; background: none; color: var(--muted-foreground); font: inherit; font-size: 0.875rem; font-weight: 500; white-space: nowrap; cursor: pointer; }
  .adm-tabs button:hover { color: var(--foreground); }
  .adm-tabs button[aria-pressed='true'] { border-color: var(--foreground); color: var(--foreground); }
  .adm-tabs button:focus-visible { outline: 2px solid var(--ring); outline-offset: -2px; border-radius: calc(var(--radius) - 2px); }
  .adm-tabs .badge { min-inline-size: 1.25rem; justify-content: center; padding-inline: 0.375rem; font-variant-numeric: tabular-nums; }
  .adm-table-wrap { position: relative; overflow-x: auto; border: 1px solid var(--border); border-radius: var(--radius); }
  .adm-table-wrap .table { min-inline-size: 48rem; }
  .adm-table-wrap .table th:first-child, .adm-table-wrap .table td:first-child { inline-size: 2.5rem; padding-inline-start: 1rem; }
  .adm-num { text-align: end; font-variant-numeric: tabular-nums; }
  .adm-course { display: flex; align-items: center; gap: 0.75rem; min-inline-size: 16rem; }
  .adm-course img { flex: none; inline-size: 4rem; block-size: 2.5rem; border-radius: calc(var(--radius) - 2px); object-fit: cover; background: var(--muted); }
  .adm-course strong { display: block; font-weight: 500; }
  .adm-course small { color: var(--muted-foreground); font-size: 0.75rem; }
  .adm-course a { color: inherit; text-decoration: none; }
  .adm-course a:hover { text-decoration: underline; text-underline-offset: 3px; }
  .adm-status { gap: 0.375rem; }
  .adm-status::before { content: ''; inline-size: 0.375rem; block-size: 0.375rem; border-radius: 999px; background: var(--muted-foreground); }
  .adm-status[data-status='published']::before { background: oklch(0.65 0.17 150); }
  .adm-status[data-status='review']::before { background: oklch(0.75 0.15 75); }
  .adm-status[data-status='invited']::before { background: oklch(0.6 0.15 255); }
  .adm-rating { display: inline-flex; align-items: center; gap: 0.25rem; }
  .adm-rating svg { inline-size: 0.875rem; block-size: 0.875rem; fill: oklch(0.8 0.16 80); color: oklch(0.8 0.16 80); }
  .adm-bulk { position: sticky; inset-block-end: 1rem; z-index: 5; display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem; justify-self: center; padding: 0.5rem 0.5rem 0.5rem 1rem; border: 1px solid var(--border); border-radius: calc(var(--radius) + 4px); background: var(--popover); color: var(--popover-foreground); box-shadow: 0 10px 30px -10px rgb(0 0 0 / 0.3); font-size: 0.875rem; }
  .adm-bulk[hidden] { display: none; }
  .adm-bulk strong { margin-inline-end: 0.5rem; font-variant-numeric: tabular-nums; }
  .adm-empty-row td { padding-block: 3rem; text-align: center; color: var(--muted-foreground); }
  .adm-row-menu [role='menu'] { min-inline-size: 10rem; }
  .adm-split { display: grid; gap: 1.5rem; align-items: start; }
  @container (width >= 64rem) { .adm-split { grid-template-columns: minmax(0, 1fr) 20rem; } .adm-split > aside { position: sticky; inset-block-start: 5rem; } }
  .adm-split > aside { display: grid; gap: 1rem; }
  .adm-kpis { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(min(100%, 13rem), 1fr)); }
  .adm-kpi { gap: 0.25rem; padding: 1rem 1.25rem; }
  .adm-kpi > p { margin: 0; font-size: 0.8125rem; color: var(--muted-foreground); }
  .adm-kpi > strong { font-size: 1.625rem; font-weight: 600; letter-spacing: -0.01em; font-variant-numeric: tabular-nums; }
  .adm-trend { display: inline-flex; align-items: center; gap: 0.25rem; font-size: 0.75rem; font-weight: 500; color: oklch(0.55 0.15 150); }
  .adm-trend[data-down] { color: var(--destructive); }
  .adm-trend svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .adm-trend[data-down] svg { transform: scaleY(-1); }
  .adm-trend span { color: var(--muted-foreground); font-weight: 400; }
  .adm-bar { display: block; block-size: 0.375rem; min-inline-size: 5rem; border-radius: 999px; background: var(--muted); overflow: hidden; }
  .adm-bar > span { display: block; block-size: 100%; border-radius: inherit; background: var(--primary); }
  .adm-progress { display: flex; align-items: center; gap: 0.5rem; font-size: 0.75rem; font-variant-numeric: tabular-nums; color: var(--muted-foreground); }
  .adm-progress .adm-bar { flex: 1; }
  .adm-person { display: flex; align-items: center; gap: 0.75rem; min-inline-size: 13rem; }
  .adm-person .avatar { flex: none; }
  .adm-person strong { display: block; font-weight: 500; }
  .adm-person small { color: var(--muted-foreground); font-size: 0.75rem; }
  .adm-section-title { margin: 0; font-size: 1rem; font-weight: 600; }
  .adm-muted { color: var(--muted-foreground); }
  .adm-coursenav { display: flex; gap: 0.25rem; overflow-x: auto; border-block-end: 1px solid var(--border); scrollbar-width: none; }
  .adm-coursenav a { padding: 0.5rem 0.75rem; border-block-end: 2px solid transparent; margin-block-end: -1px; color: var(--muted-foreground); font-size: 0.875rem; font-weight: 500; text-decoration: none; white-space: nowrap; }
  .adm-coursenav a:hover { color: var(--foreground); }
  .adm-coursenav a[aria-current] { border-color: var(--foreground); color: var(--foreground); }
  .adm-saved { display: inline-flex; align-items: center; gap: 0.375rem; font-size: 0.8125rem; color: var(--muted-foreground); }
  .adm-saved::before { content: ''; inline-size: 0.5rem; block-size: 0.5rem; border-radius: 999px; background: oklch(0.65 0.17 150); }
  .adm-saved[data-dirty]::before { background: oklch(0.75 0.15 75); }
  html.dark .adm-course img { filter: brightness(0.8); }
"""

ADM_JS = """
// Dropdown row menus close after a choice.
document.querySelectorAll('[data-popover] [role=menuitem]').forEach((m) => m.addEventListener('click', () => m.closest('[popover]')?.hidePopover?.()));
// Tables: status tabs, search, row selection with a bulk bar.
document.querySelectorAll('[data-adm-table]').forEach((root) => {
  const tbody = root.querySelector('tbody');
  const rows = () => [...tbody.querySelectorAll('tr[data-row]')];
  const tabs = [...root.querySelectorAll('[data-tab]')];
  const search = root.querySelector('[data-search]');
  const select = root.querySelector('[data-filter-select]');
  const all = root.querySelector('[data-select-all]');
  const bulk = root.querySelector('[data-bulk]');
  const empty = root.querySelector('[data-empty]');
  let tab = 'all';
  const counts = () => tabs.forEach((t) => {
    const k = t.dataset.tab;
    t.querySelector('.badge').textContent = rows().filter((r) => k === 'all' || r.dataset.status === k).length;
  });
  const apply = () => {
    const q = (search?.value || '').trim().toLowerCase();
    const f = select?.value || 'all';
    let shown = 0;
    rows().forEach((r) => {
      const ok = (tab === 'all' || r.dataset.status === tab) && (!q || r.textContent.toLowerCase().includes(q)) && (f === 'all' || r.dataset.filter === f);
      r.hidden = !ok;
      if (!ok) r.querySelector('[data-select]').checked = false;
      shown += ok;
    });
    if (empty) empty.hidden = shown > 0;
    sync();
  };
  const sync = () => {
    const vis = rows().filter((r) => !r.hidden);
    const sel = vis.filter((r) => r.querySelector('[data-select]').checked);
    vis.forEach((r) => r.toggleAttribute('data-selected', r.querySelector('[data-select]').checked));
    if (all) { all.checked = vis.length > 0 && sel.length === vis.length; all.indeterminate = sel.length > 0 && sel.length < vis.length; }
    if (bulk) { bulk.hidden = !sel.length; bulk.querySelector('[data-bulk-count]').textContent = `${sel.length} selected`; }
  };
  tabs.forEach((t) => t.addEventListener('click', () => {
    tab = t.dataset.tab;
    tabs.forEach((x) => x.setAttribute('aria-pressed', String(x === t)));
    apply();
  }));
  search?.addEventListener('input', apply);
  select?.addEventListener('change', apply);
  all?.addEventListener('change', () => { rows().filter((r) => !r.hidden).forEach((r) => { r.querySelector('[data-select]').checked = all.checked; }); sync(); });
  tbody.addEventListener('change', (e) => { if (e.target.matches('[data-select]')) sync(); });
  const selected = () => rows().filter((r) => !r.hidden && r.querySelector('[data-select]').checked);
  root.querySelectorAll('[data-bulk-status]').forEach((b) => b.addEventListener('click', () => {
    selected().forEach((r) => {
      r.dataset.status = b.dataset.bulkStatus;
      const s = r.querySelector('.adm-status');
      s.dataset.status = b.dataset.bulkStatus;
      s.textContent = b.dataset.label;
      r.querySelector('[data-select]').checked = false;
    });
    counts(); apply();
  }));
  root.querySelector('[data-bulk-delete]')?.addEventListener('click', () => { selected().forEach((r) => r.remove()); counts(); apply(); });
  root.querySelector('[data-bulk-clear]')?.addEventListener('click', () => { rows().forEach((r) => { r.querySelector('[data-select]').checked = false; }); sync(); });
  root.addEventListener('click', (e) => {
    const del = e.target.closest('[data-row-delete]');
    if (del) { del.closest('tr').remove(); counts(); apply(); }
  });
  root.admRefresh = () => { counts(); apply(); };
  counts(); apply();
});
"""


def adm_nav_item(label, ic_, active=False, badge=None):
    cur = ' aria-current="page"' if active else ""
    b = f'<span data-badge>{badge}</span>' if badge else ""
    return f'<li><a href="#"{cur} data-tooltip="{label}" data-side="right">{si(ic_)}<span>{label}</span>{b}</a></li>'


ADM_NAV = [
    ("Overview", [("Dashboard", "chart-column"), ("Courses", "book-open"), ("Media library", "image")]),
    ("Students", [("Students", "users"), ("Reviews", "star", 4), ("Q&A", "message-square", 12)]),
    ("Business", [("Pricing", "tag"), ("Coupons", "ticket-percent"), ("Settings", "settings")]),
]


def adm_shell(active, crumbs, body, end=""):
    groups = ""
    for i, (title, items) in enumerate(ADM_NAV):
        lis = "".join(adm_nav_item(l, ic_, l == active, *b) for l, ic_, *b in items)
        groups += f'<div role="group" aria-labelledby="adm-g{i}"><h3 id="adm-g{i}">{title}</h3><ul>{lis}</ul></div>'
    side = f"""<aside id="adm-sidebar" class="sidebar" data-collapsible="icon"><nav aria-label="Instructor">
  <header><ul><li><a href="#" data-size="lg"><span class="adm-mark">{si("graduation-cap")}</span><span><strong>Acme Learn</strong><small>Instructor</small></span></a></li></ul></header>
  <section>{groups}</section>
  <footer><ul><li><a href="#" data-size="lg"><span class="avatar" data-size="sm"><span>LO</span></span><span><strong>Lena Ortiz</strong><small>lena@acme.learn</small></span></a></li></ul></footer>
</nav></aside>"""
    *parents, cur = crumbs
    crumb = "".join(f'<li><a href="#">{p}</a></li><li aria-hidden="true">{si("chevron-right")}</li>' for p in parents)
    head = (f'<header class="adm-header"><button type="button" class="btn" data-variant="ghost" data-size="icon-sm" data-sidebar-toggle="adm-sidebar" aria-controls="adm-sidebar" aria-label="Toggle sidebar">{si("menu")}</button>'
            f'<hr role="separator" aria-orientation="vertical"><nav class="breadcrumb" aria-label="Breadcrumb"><ol>{crumb}<li><span aria-current="page">{cur}</span></li></ol></nav>'
            f'<div class="adm-header-end">{end}</div></header>')
    return f'{side}<main class="adm-main">{head}<div class="adm-body">{body}</div></main>'


def usd(v):
    return f"${v:,}"


def adm_status(key, label):
    return f'<span class="badge adm-status" data-variant="outline" data-status="{key}">{label}</span>'


def row_menu(pid, items):
    btns = "".join(f'<button type="button" role="menuitem"{f" data-variant={chr(34)}destructive{chr(34)}" if danger else ""}{f" {attr}" if attr else ""}>{si(ic_)}<span>{label}</span></button>' for label, ic_, danger, attr in items)
    return (f'<div class="dropdown-menu adm-row-menu"><button type="button" class="btn" data-variant="ghost" data-size="icon-sm" popovertarget="{pid}" aria-haspopup="menu" aria-label="Actions">{si("ellipsis")}</button>'
            f'<div id="{pid}" data-popover popover data-side="bottom" data-align="end"><div role="menu" aria-label="Actions">{btns}</div></div></div>')


def tabs_filter(items):
    return '<div class="adm-tabs" role="group" aria-label="Filter by status">' + "".join(
        f'<button type="button" data-tab="{k}" aria-pressed="{str(i == 0).lower()}">{l}<span class="badge" data-variant="secondary">0</span></button>' for i, (k, l) in enumerate(items)) + "</div>"


def search_box(ph, label):
    return f'<div class="input-group"><input type="search" placeholder="{ph}" aria-label="{label}" data-search><span data-align="start" aria-hidden="true">{si("search")}</span></div>'


ADM_CSS = split_lists(ADM_CSS)
ADM = SHOP_CSS + ADM_CSS
ADM_SCRIPT = script(ADM_JS)

# ---------------------------------------------------------------- admin-01: courses
A_COURSES = [
    ("Brand Identity Design from Scratch", "Design", "published", "Published", 64, 28940, 412300, 4.8, "2 days ago", 2),
    ("Watercolor Botanicals for Beginners", "Illustration", "published", "Published", 38, 12480, 186200, 4.9, "1 week ago", 3),
    ("Modern Web Typography", "Design", "review", "In review", 22, 0, 0, None, "3 hours ago", 4),
    ("Product Photography at Home", "Photography", "published", "Published", 41, 8930, 97400, 4.7, "3 weeks ago", 1),
    ("Figma for Teams: Design Systems", "Design", "draft", "Draft", 12, 0, 0, None, "Yesterday", 2),
    ("Hand Lettering Masterclass", "Illustration", "published", "Published", 55, 15210, 228150, 4.8, "1 month ago", 3),
    ("Pricing Your Creative Work", "Business", "draft", "Draft", 6, 0, 0, None, "4 days ago", 4),
    ("Motion Design Basics in After Effects", "Animation", "published", "Published", 48, 6120, 73440, 4.6, "2 months ago", 1),
]
a1_rows = "\n".join(f"""<tr data-row data-status="{k}" data-filter="{cat}">
  <td><input type="checkbox" class="input" data-select aria-label="Select {t}"></td>
  <td><div class="adm-course">{shot(n)}<span><a href="#"><strong>{t}</strong></a><small>{cat} · {les} lessons</small></span></div></td>
  <td>{adm_status(k, lab)}</td>
  <td class="adm-num">{f"{st:,}" if st else "—"}</td>
  <td class="adm-num">{usd(rev) if rev else "—"}</td>
  <td>{f'<span class="adm-rating">{si("star")}{r}</span>' if r else '<span class="adm-muted">—</span>'}</td>
  <td class="adm-muted">{upd}</td>
  <td>{row_menu(f"a1-m{i}", [("Edit", "pencil", False, ""), ("Preview", "eye", False, ""), ("Duplicate", "copy-plus", False, ""), ("Delete", "trash-2", True, "data-row-delete")])}</td>
</tr>""" for i, (t, cat, k, lab, les, st, rev, r, upd, n) in enumerate(A_COURSES))

add("admin-01", "Admin 01", "Instructor course list: status tabs with counts, search, row selection with bulk publish and delete, row menus and a new course dialog.", "admin", adm_shell("Courses", ["Instructor", "Courses"], f"""
<div class="adm-title"><div><h1>Courses</h1><p>Create, publish and manage your courses.</p></div>
  <div><button type="button" class="btn" data-variant="outline">{si("upload")}Import</button><button type="button" class="btn" commandfor="a1-new" command="show-modal">{si("plus")}New course</button></div></div>
<div class="stack" data-gap="4" data-adm-table id="a1-table">
  {tabs_filter([("all", "All"), ("published", "Published"), ("draft", "Drafts"), ("review", "In review")])}
  <div class="adm-toolbar">{search_box("Search courses...", "Search courses")}<span class="adm-grow"></span><label class="sr-only" for="a1-cat">Category</label><select class="select" id="a1-cat" data-filter-select><option value="all">All categories</option><option>Design</option><option>Illustration</option><option>Photography</option><option>Business</option><option>Animation</option></select></div>
  <div class="adm-table-wrap"><table class="table">
    <thead><tr><th><input type="checkbox" class="input" data-select-all aria-label="Select all courses"></th><th>Course</th><th>Status</th><th class="adm-num">Students</th><th class="adm-num">Revenue</th><th>Rating</th><th>Updated</th><th><span class="sr-only">Actions</span></th></tr></thead>
    <tbody>
{a1_rows}
      <tr class="adm-empty-row" data-empty hidden><td colspan="8">No courses match your filters.</td></tr>
    </tbody>
  </table></div>
  <div class="adm-bulk" data-bulk hidden role="region" aria-label="Bulk actions"><strong data-bulk-count>0 selected</strong>
    <button type="button" class="btn" data-variant="outline" data-size="sm" data-bulk-status="published" data-label="Published">{si("upload")}Publish</button>
    <button type="button" class="btn" data-variant="outline" data-size="sm" data-bulk-status="draft" data-label="Draft">{si("eye-off")}Unpublish</button>
    <button type="button" class="btn" data-variant="destructive" data-size="sm" data-bulk-delete>{si("trash-2")}Delete</button>
    <button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Clear selection" data-bulk-clear>{si("x")}</button>
  </div>
</div>
<dialog id="a1-new" class="dialog" closedby="any" aria-labelledby="a1-new-t">
  <div>
    <header><h2 id="a1-new-t">New course</h2><p>Give it a working title. You can change everything later.</p></header>
    <section><form id="a1-form" class="stack" data-gap="4">
      <div role="group" class="field"><label for="a1-title">Title</label><input id="a1-title" class="input" required maxlength="80" placeholder="e.g. Logo Design Fundamentals"></div>
      <div role="group" class="field"><label for="a1-newcat">Category</label><select class="select" id="a1-newcat"><option>Design</option><option>Illustration</option><option>Photography</option><option>Business</option><option>Animation</option></select></div>
    </form></section>
    <footer><button type="button" class="btn" data-variant="outline" commandfor="a1-new" command="close">Cancel</button><button type="submit" form="a1-form" class="btn">Create course</button></footer>
  </div>
  <button type="button" aria-label="Close dialog" commandfor="a1-new" command="close">{si("x")}</button>
</dialog>
"""), ADM, scripts=script(ADM_JS + """
document.getElementById('a1-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const t = document.getElementById('a1-title');
  const cat = document.getElementById('a1-newcat').value;
  const root = document.getElementById('a1-table');
  const tr = document.createElement('tr');
  tr.dataset.row = '';
  tr.dataset.status = 'draft';
  tr.innerHTML = '<td><input type="checkbox" class="input" data-select></td><td><div class="adm-course"><img class="shop-shot" src="assets/placeholder.svg" alt=""><span><a href="#"><strong></strong></a><small></small></span></div></td><td><span class="badge adm-status" data-variant="outline" data-status="draft">Draft</span></td><td class="adm-num">—</td><td class="adm-num">—</td><td><span class="adm-muted">—</span></td><td class="adm-muted">Just now</td><td></td>';
  tr.querySelector('strong').textContent = t.value.trim();
  tr.querySelector('small').textContent = `${cat} · 0 lessons`;
  tr.querySelector('[data-select]').setAttribute('aria-label', `Select ${t.value.trim()}`);
  tr.dataset.filter = cat;
  root.querySelector('tbody').prepend(tr);
  root.admRefresh();
  t.value = '';
  document.getElementById('a1-new').close();
});
"""))

# ---------------------------------------------------------------- admin-02: curriculum builder
LESSON_TYPES = {"video": ("Video", "circle-play"), "article": ("Article", "file-text"), "quiz": ("Quiz", "list-checks"), "assignment": ("Assignment", "notebook-pen")}
A_CURR = [
    ("Introduction", [("video", "Welcome to the course", "2:14", True), ("video", "What you'll need", "4:05", True), ("article", "How to get the most out of it", "3 min", False)]),
    ("Research and the creative brief", [("video", "Interviewing the client", "11:20", False), ("video", "Mood boards that guide decisions", "9:48", False), ("assignment", "Write your first brief", "", False), ("quiz", "Check your understanding", "5 questions", False)]),
    ("Designing the logo", [("video", "From words to sketches", "14:02", False), ("video", "Refining in Illustrator", "22:31", False)]),
]


def lesson_li(kind, title, meta, free):
    label, ic_ = LESSON_TYPES[kind]
    fr = '<span class="badge" data-variant="secondary">Free preview</span>' if free else ""
    return f"""<li class="adm-lesson" draggable="true" data-lesson data-kind="{kind}">
  <button type="button" class="adm-grip" aria-label="Move {title}. Use arrow keys">{si("grip-vertical")}</button>
  <span class="adm-lesson-ic" title="{label}">{si(ic_)}</span>
  <span class="adm-lesson-name"><strong>{title}</strong><small>{label}{f" · {meta}" if meta else ""}</small></span>
  {fr}
  <span class="adm-lesson-tools"><a href="#" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Edit {title}">{si("pencil")}</a><button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Delete {title}" data-del-lesson>{si("trash-2")}</button></span>
</li>"""


def add_lesson_menu(pid):
    items = "".join(f'<button type="button" role="menuitem" data-add-kind="{k}">{si(ic_)}<span>{l}</span></button>' for k, (l, ic_) in LESSON_TYPES.items())
    return (f'<div class="dropdown-menu"><button type="button" class="btn" data-variant="ghost" data-size="sm" popovertarget="{pid}" aria-haspopup="menu">{si("plus")}Add lesson</button>'
            f'<div id="{pid}" data-popover popover data-side="bottom" data-align="start"><div role="menu" aria-label="Lesson type">{items}</div></div></div>')


def section_card(i, title, lessons):
    lis = "".join(lesson_li(*l) for l in lessons)
    return f"""<section class="card adm-sec" data-section>
  <header class="adm-sec-head">
    <span class="adm-sec-num">Section <span data-sec-n>{i + 1}</span></span>
    <label class="sr-only" for="a2-s{i}">Section title</label><input class="input adm-sec-title" id="a2-s{i}" value="{title}">
    <span class="adm-muted adm-sec-count" data-sec-count></span>
    <button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Collapse section" aria-expanded="true" data-sec-toggle>{si("chevron-down")}</button>
  </header>
  <ol class="adm-lessons" data-lessons>{lis}</ol>
  <footer class="adm-sec-foot">{add_lesson_menu(f"a2-add{i}")}</footer>
</section>"""


add("admin-02", "Admin 02", "Curriculum builder: sections and lessons you can drag (or move with the keyboard) to reorder, add by type, rename, collapse and delete, with live totals.", "admin", adm_shell("Courses", ["Courses", "Brand Identity Design", "Curriculum"], f"""
<div class="adm-title"><div><h1>Brand Identity Design from Scratch</h1><p>{adm_status("published", "Published")} <span data-curr-summary></span></p></div>
  <div><a href="#" class="btn" data-variant="outline">{si("eye")}Preview</a><button type="button" class="btn">Save changes</button></div></div>
<nav class="adm-coursenav" aria-label="Course settings"><a href="#">Details</a><a href="#" aria-current="page">Curriculum</a><a href="#">Pricing</a><a href="#">Students</a><a href="#">Settings</a></nav>
<div class="stack" data-gap="4" data-curriculum>
  {"".join(section_card(i, t, ls) for i, (t, ls) in enumerate(A_CURR))}
  <button type="button" class="adm-add-section" data-add-section>{si("plus")}Add section</button>
  <p class="sr-only" aria-live="polite" data-curr-live></p>
</div>
"""), ADM + """
  .adm-title p { display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem; }
  .adm-sec { gap: 0; padding: 0; overflow: hidden; }
  .adm-sec-head { display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem 0.75rem 0.75rem 1rem; background: var(--muted); }
  .adm-sec-num { flex: none; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; color: var(--muted-foreground); }
  .adm-sec-title { flex: 1; min-inline-size: 0; block-size: 2.25rem; border-color: transparent; background: transparent; box-shadow: none; font-weight: 600; }
  .adm-sec-title:hover { border-color: var(--input); }
  .adm-sec-title:focus { background: var(--background); }
  .adm-sec-count { flex: none; font-size: 0.75rem; }
  .adm-sec [data-sec-toggle] svg { transition: transform 150ms ease; }
  .adm-sec[data-collapsed] [data-sec-toggle] svg { transform: rotate(-90deg); }
  .adm-sec[data-collapsed] > :is(ol, footer) { display: none; }
  .adm-lessons { display: grid; margin: 0; padding: 0.5rem; list-style: none; min-block-size: 3rem; }
  .adm-lesson { display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem; border-radius: var(--radius); background: var(--card); }
  .adm-lesson:hover { background: var(--accent); }
  .adm-lesson[data-dragging] { opacity: 0.4; }
  .adm-lessons[data-over] { background: color-mix(in oklab, var(--primary) 6%, transparent); outline: 2px dashed color-mix(in oklab, var(--primary) 40%, transparent); outline-offset: -4px; border-radius: var(--radius); }
  .adm-grip { display: grid; place-items: center; flex: none; inline-size: 1.5rem; block-size: 2rem; padding: 0; border: 0; border-radius: calc(var(--radius) - 2px); background: none; color: var(--muted-foreground); cursor: grab; }
  .adm-grip:focus-visible { outline: 2px solid var(--ring); }
  .adm-grip svg { inline-size: 1rem; block-size: 1rem; }
  .adm-lesson-ic { display: grid; place-items: center; flex: none; inline-size: 2rem; block-size: 2rem; border-radius: calc(var(--radius) - 2px); background: var(--muted); color: var(--muted-foreground); }
  .adm-lesson-ic svg { inline-size: 1rem; block-size: 1rem; }
  .adm-lesson-name { flex: 1; min-inline-size: 0; display: grid; }
  .adm-lesson-name strong { overflow: hidden; font-size: 0.875rem; font-weight: 500; text-overflow: ellipsis; white-space: nowrap; }
  .adm-lesson-name small { font-size: 0.75rem; color: var(--muted-foreground); }
  .adm-lesson-name input { block-size: 2rem; }
  .adm-lesson-tools { display: flex; opacity: 0; transition: opacity 150ms ease; }
  .adm-lesson:is(:hover, :focus-within) .adm-lesson-tools { opacity: 1; }
  @media (hover: none) { .adm-lesson-tools { opacity: 1; } }
  .adm-sec-foot { padding: 0 0.5rem 0.5rem; }
  .adm-add-section { display: flex; align-items: center; justify-content: center; gap: 0.5rem; block-size: 3.5rem; border: 2px dashed var(--border); border-radius: var(--radius); background: none; color: var(--muted-foreground); font: inherit; font-size: 0.875rem; font-weight: 500; cursor: pointer; }
  .adm-add-section:hover { border-color: var(--ring); color: var(--foreground); }
  .adm-add-section:focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
  .adm-add-section svg { inline-size: 1rem; block-size: 1rem; }""", scripts=script(ADM_JS + """
(() => {
  const root = document.querySelector('[data-curriculum]');
  const live = root.querySelector('[data-curr-live]');
  const KINDS = { video: ['Video', 'circle-play'], article: ['Article', 'file-text'], quiz: ['Quiz', 'list-checks'], assignment: ['Assignment', 'notebook-pen'] };
  const icon = (k) => root.querySelector(`[data-add-kind="${k}"] svg`).outerHTML;
  const sync = () => {
    const secs = [...root.querySelectorAll('[data-section]')];
    let total = 0;
    secs.forEach((s, i) => {
      const n = s.querySelectorAll('[data-lesson]').length;
      total += n;
      s.querySelector('[data-sec-n]').textContent = i + 1;
      s.querySelector('[data-sec-count]').textContent = `${n} ${n === 1 ? 'lesson' : 'lessons'}`;
    });
    document.querySelector('[data-curr-summary]').textContent = `${secs.length} sections · ${total} lessons`;
  };
  // Drag and drop between and within sections.
  let dragged = null;
  root.addEventListener('dragstart', (e) => {
    dragged = e.target.closest('[data-lesson]');
    if (!dragged) return;
    dragged.setAttribute('data-dragging', '');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', '');
  });
  root.addEventListener('dragend', () => {
    dragged?.removeAttribute('data-dragging');
    root.querySelectorAll('[data-over]').forEach((x) => x.removeAttribute('data-over'));
    dragged = null;
    sync();
  });
  root.addEventListener('dragover', (e) => {
    const list = e.target.closest('[data-lessons]');
    if (!dragged || !list) return;
    e.preventDefault();
    root.querySelectorAll('[data-over]').forEach((x) => x !== list && x.removeAttribute('data-over'));
    list.setAttribute('data-over', '');
    const after = [...list.querySelectorAll('[data-lesson]:not([data-dragging])')].find((li) => e.clientY < li.getBoundingClientRect().top + li.offsetHeight / 2);
    list.insertBefore(dragged, after || null);
  });
  root.addEventListener('drop', (e) => e.preventDefault());
  // Keyboard: arrow keys on the handle move the lesson, across sections too.
  root.addEventListener('keydown', (e) => {
    const grip = e.target.closest('.adm-grip');
    if (!grip || !['ArrowUp', 'ArrowDown'].includes(e.key)) return;
    e.preventDefault();
    const li = grip.closest('[data-lesson]');
    const lists = [...root.querySelectorAll('[data-lessons]')];
    const list = li.parentElement;
    if (e.key === 'ArrowUp') {
      if (li.previousElementSibling) list.insertBefore(li, li.previousElementSibling);
      else if (lists.indexOf(list) > 0) lists[lists.indexOf(list) - 1].append(li);
    } else if (li.nextElementSibling) list.insertBefore(li.nextElementSibling, li);
    else if (lists.indexOf(list) < lists.length - 1) lists[lists.indexOf(list) + 1].prepend(li);
    grip.focus();
    sync();
    const sec = li.closest('[data-section]');
    live.textContent = `${li.querySelector('strong').textContent}: section ${sec.querySelector('[data-sec-n]').textContent}, position ${[...li.parentElement.children].indexOf(li) + 1}`;
  });
  root.addEventListener('click', (e) => {
    const del = e.target.closest('[data-del-lesson]');
    if (del) { const li = del.closest('[data-lesson]'); live.textContent = `${li.querySelector('strong').textContent} deleted`; li.remove(); sync(); return; }
    const tog = e.target.closest('[data-sec-toggle]');
    if (tog) {
      const sec = tog.closest('[data-section]');
      const collapsed = sec.toggleAttribute('data-collapsed');
      tog.setAttribute('aria-expanded', String(!collapsed));
      tog.setAttribute('aria-label', collapsed ? 'Expand section' : 'Collapse section');
      return;
    }
    const kind = e.target.closest('[data-add-kind]')?.dataset.addKind;
    if (kind) {
      const list = e.target.closest('[data-section]').querySelector('[data-lessons]');
      const [label] = KINDS[kind];
      const li = document.createElement('li');
      li.className = 'adm-lesson';
      li.draggable = true;
      li.dataset.lesson = '';
      li.dataset.kind = kind;
      li.innerHTML = `<button type="button" class="adm-grip" aria-label="Move lesson. Use arrow keys">${root.querySelector('.adm-grip svg').outerHTML}</button><span class="adm-lesson-ic" title="${label}">${icon(kind)}</span><span class="adm-lesson-name"><input class="input" aria-label="${label} title" placeholder="New ${label.toLowerCase()} title"><small>${label}</small></span><span class="adm-lesson-tools"><button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Delete lesson" data-del-lesson>${root.querySelector('[data-del-lesson] svg').outerHTML}</button></span>`;
      list.append(li);
      const input = li.querySelector('input');
      let done = false;
      const commit = () => {
        if (done) return;
        done = true;
        const v = input.value.trim() || `Untitled ${label.toLowerCase()}`;
        const strong = document.createElement('strong');
        strong.textContent = v;
        input.replaceWith(strong);
        li.querySelector('.adm-grip').setAttribute('aria-label', `Move ${v}. Use arrow keys`);
      };
      input.addEventListener('keydown', (ev) => { if (ev.key === 'Enter') { ev.preventDefault(); commit(); li.querySelector('.adm-grip').focus(); } });
      // The menu hands focus back to its button as it closes; take it after that.
      requestAnimationFrame(() => { input.focus(); input.addEventListener('blur', commit, { once: true }); });
      sync();
      return;
    }
    if (e.target.closest('[data-add-section]')) {
      const tpl = root.querySelector('[data-section]');
      const sec = tpl.cloneNode(true);
      sec.removeAttribute('data-collapsed');
      sec.querySelector('[data-lessons]').innerHTML = '';
      const n = root.querySelectorAll('[data-section]').length;
      const input = sec.querySelector('.adm-sec-title');
      input.id = `a2-s${n}`;
      input.value = '';
      input.placeholder = 'Section title';
      sec.querySelector('label[for]').htmlFor = input.id;
      const menu = sec.querySelector('[popover]');
      menu.id = `a2-add${n}`;
      sec.querySelector('[popovertarget]').setAttribute('popovertarget', menu.id);
      e.target.closest('[data-add-section]').before(sec);
      sync();
      input.focus();
    }
  });
  sync();
})();
"""))

# ---------------------------------------------------------------- admin-03: lesson editor with video upload
TOOLS = [("bold", "Bold", "bold"), ("italic", "Italic", "italic"), ("heading-2", "Heading", "formatBlock:h3"), ("list", "Bulleted list", "insertUnorderedList"), ("list-ordered", "Numbered list", "insertOrderedList"), ("quote", "Quote", "formatBlock:blockquote"), ("code", "Code", "formatBlock:pre"), ("link", "Link", "createLink")]
toolbar = "".join(f'<button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="{l}" title="{l}" data-cmd="{c}">{si(i)}</button>' + ('<hr role="separator" aria-orientation="vertical">' if i in ("italic", "heading-2", "list-ordered") else "") for i, l, c in TOOLS)
RES = [("Brief template.docx", "48 KB"), ("Mood board examples.pdf", "3.2 MB")]
res = "".join(f'<li data-res>{si("paperclip")}<span><strong>{n}</strong><small>{s}</small></span><button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Remove {n}" data-res-remove>{si("x")}</button></li>' for n, s in RES)

add("admin-03", "Admin 03", "Lesson editor: video upload with drag and drop, progress, processing and replace; a rich text description; downloadable resources; and publish settings with save state.", "admin", adm_shell("Courses", ["Brand Identity Design", "Curriculum", "Mood boards that guide decisions"], f"""
<form class="adm-split" data-lesson-form onsubmit="event.preventDefault()">
  <div class="stack" data-gap="6">
    <div class="adm-title"><div><p class="adm-muted" style="margin: 0">Section 2 · Lesson 5</p><h1>Edit lesson</h1></div><div><span class="adm-saved" data-saved role="status">All changes saved</span></div></div>
    <div role="group" class="field"><label for="a3-title">Lesson title</label><input class="input" id="a3-title" value="Mood boards that guide decisions" maxlength="80" required></div>
    <section class="stack" data-gap="2" aria-labelledby="a3-video-l">
      <h2 class="adm-section-title" id="a3-video-l">Video</h2>
      <div class="adm-upload" data-upload data-state="empty">
        <label class="adm-drop" for="a3-file" data-drop>
          <span class="adm-drop-ic">{si("cloud-upload")}</span>
          <strong>Drag and drop a video, or <span class="adm-link">browse</span></strong>
          <small>MP4, MOV or WebM, up to 4 GB. 1080p or higher recommended.</small>
          <input type="file" id="a3-file" accept="video/*" class="sr-only" data-file>
        </label>
        <div class="adm-uploading" data-uploading>
          <span class="adm-drop-ic">{si("video")}</span>
          <div class="stack" data-gap="2"><div class="cluster" data-justify="between"><strong data-file-name>mood-boards-final.mp4</strong><span class="adm-muted" data-pct>0%</span></div>
          <div class="progress" role="progressbar" aria-label="Upload progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" data-bar><span style="width: 0%"></span></div>
          <small class="adm-muted" data-up-label>Uploading · 412 MB</small></div>
          <button type="button" class="btn" data-variant="ghost" data-size="sm" data-cancel>Cancel</button>
        </div>
        <div class="adm-ready" data-ready>
          <div class="adm-ready-thumb">{shot(2)}<span>{si("play")}</span><small>9:48</small></div>
          <div class="stack" data-gap="1"><strong data-file-name>mood-boards-final.mp4</strong><small class="adm-muted">1080p · 9:48 · 412 MB · Captions: auto-generated</small>
            <div class="cluster" data-gap="2"><label class="btn" data-variant="outline" data-size="sm" for="a3-file">{si("refresh-cw")}Replace</label><button type="button" class="btn" data-variant="ghost" data-size="sm" data-remove-video>{si("trash-2")}Remove</button></div></div>
        </div>
      </div>
      <button type="button" class="btn adm-sample" data-variant="link" data-size="sm" data-sample>Use a sample video</button>
    </section>
    <section class="stack" data-gap="2" aria-labelledby="a3-desc-l">
      <h2 class="adm-section-title" id="a3-desc-l">Description</h2>
      <div class="adm-editor">
        <div class="adm-editor-bar" role="toolbar" aria-label="Formatting" aria-controls="a3-desc">{toolbar}</div>
        <div class="adm-editor-body" id="a3-desc" contenteditable="true" role="textbox" aria-multiline="true" aria-labelledby="a3-desc-l" data-editor><p>Turn your research into two or three <strong>mood boards</strong> that each tell a different story, then use them to steer the client toward a direction before you draw anything.</p><ul><li>Collect 20 to 30 references per board</li><li>Name each board after a feeling, not a style</li></ul></div>
        <div class="adm-editor-foot"><span data-words>0 words</span></div>
      </div>
    </section>
    <section class="stack" data-gap="2" aria-labelledby="a3-res-l">
      <div class="cluster" data-justify="between"><h2 class="adm-section-title" id="a3-res-l">Resources</h2><label class="btn" data-variant="outline" data-size="sm" for="a3-res-file">{si("plus")}Add file</label><input type="file" id="a3-res-file" class="sr-only" multiple data-res-file></div>
      <ul class="adm-res" data-res-list>{res}</ul>
    </section>
  </div>
  <aside>
    <div class="card"><header><h2>Publish</h2></header><section class="stack" data-gap="4">
      <div role="group" class="field"><label for="a3-status">Status</label><select class="select" id="a3-status"><option value="published">Published</option><option value="draft" selected>Draft</option><option value="scheduled">Scheduled</option></select></div>
      <div role="group" class="field" data-orientation="horizontal"><input type="checkbox" role="switch" class="input" id="a3-free"><label for="a3-free">Free preview for everyone</label></div>
      <div role="group" class="field" data-orientation="horizontal"><input type="checkbox" role="switch" class="input" id="a3-dl" checked><label for="a3-dl">Allow resource downloads</label></div>
    </section><footer class="stack" data-gap="2"><button type="submit" class="btn" style="inline-size: 100%" data-save>Save lesson</button><button type="button" class="btn" data-variant="ghost" style="inline-size: 100%">{si("eye")}Preview as student</button></footer></div>
    <nav class="cluster" data-justify="between" aria-label="Lessons"><a href="#" class="btn" data-variant="ghost" data-size="sm">{si("chevron-left")}Previous</a><a href="#" class="btn" data-variant="ghost" data-size="sm">Next{si("chevron-right")}</a></nav>
  </aside>
</form>
"""), ADM + """
  .adm-upload { border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; }
  .adm-upload > [data-uploading], .adm-upload > [data-ready] { display: none; }
  .adm-upload[data-state='uploading'] > [data-drop], .adm-upload[data-state='ready'] > [data-drop] { display: none; }
  .adm-upload[data-state='uploading'] > [data-uploading] { display: grid; }
  .adm-upload[data-state='ready'] > [data-ready] { display: grid; }
  .adm-drop { display: grid; justify-items: center; gap: 0.5rem; padding: 2.5rem 1rem; border: 2px dashed transparent; border-radius: var(--radius); background: color-mix(in oklab, var(--muted) 50%, transparent); text-align: center; cursor: pointer; transition: border-color 150ms ease, background-color 150ms ease; }
  .adm-drop:hover, .adm-drop[data-over] { border-color: var(--ring); background: color-mix(in oklab, var(--primary) 6%, transparent); }
  .adm-drop:focus-within { outline: 2px solid var(--ring); outline-offset: -2px; }
  .adm-drop strong { font-size: 0.9375rem; font-weight: 500; }
  .adm-drop small { color: var(--muted-foreground); font-size: 0.8125rem; }
  .adm-link { color: var(--primary); text-decoration: underline; text-underline-offset: 3px; }
  .adm-drop-ic { display: grid; place-items: center; inline-size: 3rem; block-size: 3rem; border-radius: 999px; background: var(--background); box-shadow: 0 0 0 1px var(--border); color: var(--muted-foreground); }
  .adm-drop-ic svg { inline-size: 1.25rem; block-size: 1.25rem; }
  .adm-uploading { grid-template-columns: auto minmax(0, 1fr) auto; align-items: center; gap: 1rem; padding: 1.25rem; }
  .adm-uploading strong, .adm-ready strong { font-size: 0.875rem; font-weight: 500; overflow-wrap: anywhere; }
  .adm-ready { grid-template-columns: 12rem minmax(0, 1fr); align-items: center; gap: 1rem; padding: 0.75rem; }
  @container (width < 36rem) { .adm-ready { grid-template-columns: 1fr; } }
  .adm-ready-thumb { position: relative; display: grid; place-items: center; aspect-ratio: 16 / 9; overflow: hidden; border-radius: calc(var(--radius) - 2px); }
  .adm-ready-thumb img { position: absolute; inset: 0; inline-size: 100%; block-size: 100%; object-fit: cover; }
  .adm-ready-thumb > span { position: relative; display: grid; place-items: center; inline-size: 2.5rem; block-size: 2.5rem; border-radius: 999px; background: rgb(255 255 255 / 0.9); color: #111; }
  .adm-ready-thumb > span svg { inline-size: 1rem; block-size: 1rem; fill: currentColor; }
  .adm-ready-thumb small { position: absolute; inset-inline-end: 0.375rem; inset-block-end: 0.375rem; padding: 0 0.375rem; border-radius: 4px; background: rgb(0 0 0 / 0.7); color: #fff; font-size: 0.6875rem; }
  .adm-sample { align-self: flex-start; padding-inline: 0; }
  .adm-upload[data-state='ready'] + .adm-sample { display: none; }
  .adm-editor { border: 1px solid var(--input); border-radius: var(--radius); overflow: hidden; }
  .adm-editor:focus-within { border-color: var(--ring); box-shadow: 0 0 0 3px color-mix(in oklab, var(--ring) 40%, transparent); }
  .adm-editor-bar { display: flex; flex-wrap: wrap; align-items: center; gap: 0.125rem; padding: 0.25rem; border-block-end: 1px solid var(--border); background: color-mix(in oklab, var(--muted) 50%, transparent); }
  .adm-editor-bar hr { align-self: stretch; block-size: auto; margin: 0.25rem; }
  .adm-editor-bar .btn[aria-pressed='true'] { background: var(--accent); color: var(--accent-foreground); }
  .adm-editor-body { min-block-size: 10rem; padding: 0.75rem 1rem; font-size: 0.9375rem; line-height: 1.6; outline: none; }
  .adm-editor-body > :first-child { margin-block-start: 0; }
  .adm-editor-body p { margin: 0 0 0.75rem; }
  .adm-editor-body ul { margin: 0 0 0.75rem; padding-inline-start: 1.25rem; list-style: disc; }
  .adm-editor-body ol { margin: 0 0 0.75rem; padding-inline-start: 1.25rem; list-style: decimal; }
  .adm-editor-body h3 { margin: 1rem 0 0.25rem; font-size: 1.0625rem; }
  .adm-editor-body blockquote { margin: 0.5rem 0; padding-inline-start: 1rem; border-inline-start: 3px solid var(--border); color: var(--muted-foreground); }
  .adm-editor-body pre { padding: 0.5rem 0.75rem; border-radius: calc(var(--radius) - 2px); background: var(--muted); font-size: 0.8125rem; white-space: pre-wrap; }
  .adm-editor-body a { color: var(--primary); }
  .adm-editor-foot { display: flex; justify-content: flex-end; padding: 0.375rem 0.75rem; border-block-start: 1px solid var(--border); font-size: 0.75rem; color: var(--muted-foreground); font-variant-numeric: tabular-nums; }
  .adm-res { display: grid; gap: 0.5rem; margin: 0; padding: 0; list-style: none; }
  .adm-res li { display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0.5rem 0.5rem 0.75rem; border: 1px solid var(--border); border-radius: var(--radius); }
  .adm-res li > svg { flex: none; inline-size: 1rem; block-size: 1rem; color: var(--muted-foreground); }
  .adm-res li > span { flex: 1; min-inline-size: 0; display: grid; }
  .adm-res strong { font-size: 0.875rem; font-weight: 500; overflow-wrap: anywhere; }
  .adm-res small { font-size: 0.75rem; color: var(--muted-foreground); }""", scripts=script(ADM_JS + """
(() => {
  const form = document.querySelector('[data-lesson-form]');
  const saved = form.querySelector('[data-saved]');
  const dirty = () => { saved.setAttribute('data-dirty', ''); saved.textContent = 'Unsaved changes'; };
  form.addEventListener('input', dirty);
  form.addEventListener('change', (e) => { if (!e.target.matches('[type=file]')) dirty(); });
  form.addEventListener('submit', () => {
    saved.removeAttribute('data-dirty');
    saved.textContent = `Saved at ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
  });
  // Video: choose or drop a file, watch it upload, then it is ready.
  const up = form.querySelector('[data-upload]');
  const drop = up.querySelector('[data-drop]');
  const bar = up.querySelector('[data-bar]');
  let timer;
  const setPct = (p) => {
    bar.setAttribute('aria-valuenow', String(p));
    bar.firstElementChild.style.width = `${p}%`;
    up.querySelector('[data-pct]').textContent = `${p}%`;
  };
  const start = (name, size) => {
    clearInterval(timer);
    up.querySelectorAll('[data-file-name]').forEach((x) => { x.textContent = name; });
    up.dataset.state = 'uploading';
    up.querySelector('[data-up-label]').textContent = `Uploading · ${size}`;
    let p = 0;
    setPct(0);
    timer = setInterval(() => {
      p = Math.min(100, p + 7 + Math.round(Math.random() * 8));
      setPct(p);
      if (p === 100) {
        clearInterval(timer);
        up.querySelector('[data-up-label]').textContent = 'Processing video…';
        setTimeout(() => { up.dataset.state = 'ready'; dirty(); }, 900);
      }
    }, 180);
  };
  const mb = (b) => (b > 1e9 ? `${(b / 1e9).toFixed(1)} GB` : `${Math.max(1, Math.round(b / 1e6))} MB`);
  form.querySelector('[data-file]').addEventListener('change', (e) => { const f = e.target.files[0]; if (f) start(f.name, mb(f.size)); e.target.value = ''; });
  form.querySelector('[data-sample]').addEventListener('click', () => start('mood-boards-final.mp4', '412 MB'));
  ['dragenter', 'dragover'].forEach((t) => drop.addEventListener(t, (e) => { e.preventDefault(); drop.setAttribute('data-over', ''); }));
  ['dragleave', 'drop'].forEach((t) => drop.addEventListener(t, (e) => { e.preventDefault(); drop.removeAttribute('data-over'); }));
  drop.addEventListener('drop', (e) => { const f = [...e.dataTransfer.files].find((x) => x.type.startsWith('video/')); if (f) start(f.name, mb(f.size)); });
  up.querySelector('[data-cancel]').addEventListener('click', () => { clearInterval(timer); up.dataset.state = 'empty'; });
  up.querySelector('[data-remove-video]').addEventListener('click', () => { up.dataset.state = 'empty'; dirty(); });
  // Rich text: toolbar commands, active states, word count.
  const ed = form.querySelector('[data-editor]');
  const words = form.querySelector('[data-words]');
  const count = () => { const n = ed.innerText.trim().split(/\\s+/).filter(Boolean).length; words.textContent = `${n} ${n === 1 ? 'word' : 'words'}`; };
  const states = () => form.querySelectorAll('[data-cmd]').forEach((b) => {
    const [cmd, arg] = b.dataset.cmd.split(':');
    let on = false;
    try { on = arg ? document.queryCommandValue('formatBlock').toLowerCase() === arg : ['bold', 'italic', 'insertUnorderedList', 'insertOrderedList'].includes(cmd) && document.queryCommandState(cmd); } catch {}
    b.setAttribute('aria-pressed', String(on && ed.contains(document.getSelection().anchorNode)));
  });
  form.querySelectorAll('[data-cmd]').forEach((b) => {
    b.addEventListener('mousedown', (e) => e.preventDefault());
    b.addEventListener('click', () => {
      ed.focus();
      const [cmd, arg] = b.dataset.cmd.split(':');
      if (cmd === 'createLink') { const url = prompt('Link URL', 'https://'); if (url) document.execCommand('createLink', false, url); }
      else if (arg) document.execCommand('formatBlock', false, document.queryCommandValue('formatBlock').toLowerCase() === arg ? 'p' : arg);
      else document.execCommand(cmd);
      states(); count(); dirty();
    });
  });
  ed.addEventListener('input', count);
  document.addEventListener('selectionchange', states);
  count();
  // Resources.
  const list = form.querySelector('[data-res-list]');
  const tpl = list.querySelector('[data-res]');
  form.querySelector('[data-res-file]').addEventListener('change', (e) => {
    [...e.target.files].forEach((f) => {
      const li = tpl.cloneNode(true);
      li.querySelector('strong').textContent = f.name;
      li.querySelector('small').textContent = f.size > 1e6 ? `${(f.size / 1e6).toFixed(1)} MB` : `${Math.max(1, Math.round(f.size / 1e3))} KB`;
      li.querySelector('[data-res-remove]').setAttribute('aria-label', `Remove ${f.name}`);
      list.append(li);
    });
    e.target.value = '';
    dirty();
  });
  list.addEventListener('click', (e) => { const b = e.target.closest('[data-res-remove]'); if (b) { b.closest('li').remove(); dirty(); } });
})();
"""))

# ---------------------------------------------------------------- admin-04: media library
MEDIA = [("video", "welcome-to-the-course.mp4", "86 MB", "2:14", 1, 1), ("video", "interviewing-the-client.mp4", "640 MB", "11:20", 2, 1), ("image", "course-cover.jpg", "1.2 MB", "1920×1080", 3, 2), ("document", "brief-template.docx", "48 KB", "Word", 0, 1),
         ("video", "mood-boards-final.mp4", "412 MB", "9:48", 4, 1), ("image", "logo-sketches.png", "3.8 MB", "2400×1600", 2, 1), ("document", "mood-board-examples.pdf", "3.2 MB", "PDF · 18 pages", 0, 1), ("image", "teacher-portrait.jpg", "640 KB", "1200×1200", 1, 0)]
M_ICON = {"video": "video", "image": "image", "document": "file-text"}


def media_card(i, kind, name, size, meta, n, used):
    thumb = (f'{shot(n)}' if kind != "document" else f'<span class="adm-doc">{si("file-text")}</span>')
    badge = f'<span class="adm-media-kind">{si(M_ICON[kind])}{meta if kind == "video" else ""}</span>'
    return f"""<li data-media data-kind="{kind}" data-name="{name}" data-size="{size}" data-meta="{meta}" data-used="{used}">
  <label class="adm-media">
    <input type="checkbox" class="input" data-select aria-label="Select {name}">
    <span class="adm-media-thumb">{thumb}{badge}</span>
    <span class="adm-media-name"><strong>{name}</strong><small>{size}</small></span>
  </label>
</li>"""


add("admin-04", "Admin 04", "Media library: drag-and-drop upload queue with progress, type filters, search, grid or list view, and a details panel with copy link and delete.", "admin", adm_shell("Media library", ["Instructor", "Media library"], f"""
<div class="adm-title"><div><h1>Media library</h1><p><span data-media-count>8 files</span> · 1.1 GB of 50 GB used</p></div>
  <div><label class="btn" for="a4-file">{si("upload")}Upload</label><input type="file" id="a4-file" class="sr-only" multiple data-file></div></div>
<label class="adm-dropzone" for="a4-file" data-drop>{si("cloud-upload")}<span><strong>Drop files to upload</strong><small>Videos, images and documents. They're processed in the background.</small></span></label>
<ul class="adm-queue" data-queue aria-label="Uploads"></ul>
<div class="adm-split">
  <div class="stack" data-gap="4">
    <div class="adm-toolbar">
      <fieldset class="toggle-group" data-variant="outline" data-size="sm"><legend class="sr-only">File type</legend>
        {"".join(f'<label class="toggle"><input type="radio" name="a4-kind" value="{v}"{" checked" if v == "all" else ""}>{l}</label>' for v, l in [("all", "All"), ("video", "Videos"), ("image", "Images"), ("document", "Documents")])}
      </fieldset>
      {search_box("Search files...", "Search files")}
      <span class="adm-grow"></span>
      <fieldset class="toggle-group" data-variant="outline" data-size="sm"><legend class="sr-only">View</legend><label class="toggle" aria-label="Grid view"><input type="radio" name="a4-view" value="grid" checked>{si("layout-grid")}</label><label class="toggle" aria-label="List view"><input type="radio" name="a4-view" value="list">{si("list")}</label></fieldset>
    </div>
    <ul class="adm-media-grid" data-media-grid data-view="grid">{"".join(media_card(i, *m) for i, m in enumerate(MEDIA))}</ul>
    <p class="adm-muted" data-media-empty hidden>No files match.</p>
  </div>
  <aside class="card adm-details" data-details>
    <div class="adm-details-empty" data-details-empty>{si("image")}<p>Select a file to see its details.</p></div>
    <div class="stack" data-gap="4" data-details-body hidden>
      <span class="adm-media-thumb" data-d-thumb></span>
      <div><strong class="adm-d-name" data-d-name></strong></div>
      <dl class="adm-dl"><div><dt>Type</dt><dd data-d-kind></dd></div><div><dt>Size</dt><dd data-d-size></dd></div><div><dt>Details</dt><dd data-d-meta></dd></div><div><dt>Used in</dt><dd data-d-used></dd></div></dl>
      <div class="input-group"><input readonly aria-label="File link" id="a4-url" data-d-url><span data-align="end">{copy_btn("#a4-url", "Copy link")}</span></div>
      <div class="cluster" data-gap="2"><a href="#" class="btn" data-variant="outline" data-size="sm">{si("download")}Download</a><button type="button" class="btn" data-variant="destructive" data-size="sm" data-d-delete>{si("trash-2")}Delete</button></div>
    </div>
    <div class="stack" data-gap="3" data-details-multi hidden><strong data-multi-count></strong><button type="button" class="btn" data-variant="destructive" data-size="sm" data-d-delete>{si("trash-2")}Delete selected</button></div>
  </aside>
</div>
"""), ADM + SUCCESS_CSS + """
  .adm-dropzone { display: flex; align-items: center; justify-content: center; gap: 1rem; padding: 1.25rem; border: 2px dashed var(--border); border-radius: var(--radius); color: var(--muted-foreground); cursor: pointer; transition: border-color 150ms ease, background-color 150ms ease; }
  .adm-dropzone:hover, .adm-dropzone[data-over] { border-color: var(--ring); background: color-mix(in oklab, var(--primary) 5%, transparent); color: var(--foreground); }
  .adm-dropzone > svg { flex: none; inline-size: 1.5rem; block-size: 1.5rem; }
  .adm-dropzone span { display: grid; }
  .adm-dropzone strong { color: var(--foreground); font-size: 0.875rem; font-weight: 500; }
  .adm-dropzone small { font-size: 0.8125rem; }
  .adm-queue { display: grid; gap: 0.5rem; margin: 0; padding: 0; list-style: none; }
  .adm-queue:empty { display: none; }
  .adm-queue li { display: grid; grid-template-columns: auto minmax(0, 1fr) auto; align-items: center; gap: 0.75rem; padding: 0.625rem 0.75rem; border: 1px solid var(--border); border-radius: var(--radius); font-size: 0.8125rem; }
  .adm-queue li > svg { inline-size: 1rem; block-size: 1rem; color: var(--muted-foreground); }
  .adm-queue li[data-done] > svg { color: oklch(0.6 0.15 150); }
  .adm-queue .stack strong { font-weight: 500; overflow-wrap: anywhere; }
  .adm-queue .progress { block-size: 0.25rem; }
  .adm-queue li > span:last-child { font-variant-numeric: tabular-nums; color: var(--muted-foreground); }
  @container (width >= 64rem) { .adm-split { grid-template-columns: minmax(0, 1fr) 18rem; } }
  .adm-toolbar .toggle-group .toggle svg { inline-size: 1rem; block-size: 1rem; }
  .adm-media-grid { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr)); margin: 0; padding: 0; list-style: none; }
  .adm-media-grid[data-view='list'] { grid-template-columns: 1fr; gap: 0.25rem; }
  .adm-media { position: relative; display: grid; gap: 0.5rem; padding: 0.375rem; border: 1px solid transparent; border-radius: var(--radius); cursor: pointer; }
  .adm-media:hover { background: var(--accent); }
  .adm-media:has(:checked) { border-color: var(--ring); background: color-mix(in oklab, var(--primary) 6%, transparent); }
  .adm-media:has(:focus-visible) { outline: 2px solid var(--ring); outline-offset: 2px; }
  .adm-media > input { position: absolute; inset-block-start: 0.75rem; inset-inline-start: 0.75rem; z-index: 1; opacity: 0; }
  .adm-media > input:not(:checked) { background-color: var(--background); }
  .adm-media:hover > input, .adm-media > input:checked, .adm-media > input:focus-visible { opacity: 1; }
  .adm-media-thumb { position: relative; display: grid; place-items: center; aspect-ratio: 4 / 3; overflow: hidden; border-radius: calc(var(--radius) - 2px); background: var(--muted); }
  .adm-media-thumb img { position: absolute; inset: 0; inline-size: 100%; block-size: 100%; object-fit: cover; }
  .adm-doc { color: var(--muted-foreground); }
  .adm-doc svg { inline-size: 2.5rem; block-size: 2.5rem; stroke-width: 1.5; }
  .adm-media-kind { position: absolute; inset-inline-end: 0.375rem; inset-block-end: 0.375rem; display: inline-flex; align-items: center; gap: 0.25rem; padding: 0.125rem 0.375rem; border-radius: 4px; background: rgb(0 0 0 / 0.7); color: #fff; font-size: 0.6875rem; font-variant-numeric: tabular-nums; }
  .adm-media-kind svg { inline-size: 0.75rem; block-size: 0.75rem; }
  .adm-media-name { display: grid; min-inline-size: 0; padding-inline: 0.125rem; }
  .adm-media-name strong { overflow: hidden; font-size: 0.8125rem; font-weight: 500; text-overflow: ellipsis; white-space: nowrap; }
  .adm-media-name small { font-size: 0.75rem; color: var(--muted-foreground); }
  .adm-media-grid[data-view='list'] .adm-media { grid-template-columns: 4rem minmax(0, 1fr); align-items: center; padding-inline-start: 2.5rem; }
  .adm-media-grid[data-view='list'] .adm-media > input { inset-block-start: 50%; translate: 0 -50%; opacity: 1; }
  .adm-media-grid[data-view='list'] .adm-media-kind { display: none; }
  .adm-media-grid[data-view='list'] .adm-doc svg { inline-size: 1.5rem; block-size: 1.5rem; }
  .adm-details { min-block-size: 16rem; }
  .adm-details-empty { display: grid; place-items: center; align-content: center; gap: 0.5rem; min-block-size: 14rem; color: var(--muted-foreground); font-size: 0.875rem; text-align: center; }
  .adm-details-empty[hidden] { display: none; }
  .adm-details-empty svg { inline-size: 2rem; block-size: 2rem; stroke-width: 1.5; }
  .adm-details-empty p { margin: 0; }
  .adm-details > div { padding-inline: 1rem; }
  .adm-d-name { overflow-wrap: anywhere; font-size: 0.9375rem; }
  .adm-dl { display: grid; gap: 0.5rem; margin: 0; font-size: 0.8125rem; }
  .adm-dl div { display: flex; justify-content: space-between; gap: 1rem; }
  .adm-dl dt { color: var(--muted-foreground); }
  .adm-dl dd { margin: 0; text-align: end; text-transform: capitalize; }
  html.dark .adm-media-thumb img { filter: brightness(0.8); }""", scripts=script(ADM_JS + """
(() => {
  const grid = document.querySelector('[data-media-grid]');
  const items = () => [...grid.querySelectorAll('[data-media]')];
  const search = document.querySelector('[data-search]');
  const empty = document.querySelector('[data-media-empty]');
  const details = document.querySelector('[data-details]');
  const filter = () => {
    const kind = document.querySelector('[name=a4-kind]:checked').value;
    const q = search.value.trim().toLowerCase();
    let n = 0;
    items().forEach((li) => {
      const ok = (kind === 'all' || li.dataset.kind === kind) && li.dataset.name.includes(q);
      li.hidden = !ok;
      n += ok;
    });
    empty.hidden = n > 0;
    document.querySelector('[data-media-count]').textContent = `${items().length} files`;
  };
  const show = () => {
    const sel = items().filter((li) => li.querySelector('[data-select]').checked);
    details.querySelector('[data-details-empty]').hidden = sel.length > 0;
    details.querySelector('[data-details-body]').hidden = sel.length !== 1;
    details.querySelector('[data-details-multi]').hidden = sel.length < 2;
    details.querySelector('[data-multi-count]').textContent = `${sel.length} files selected`;
    if (sel.length !== 1) return;
    const d = sel[0].dataset;
    details.querySelector('[data-d-thumb]').innerHTML = sel[0].querySelector('.adm-media-thumb').innerHTML;
    details.querySelector('[data-d-name]').textContent = d.name;
    details.querySelector('[data-d-kind]').textContent = d.kind;
    details.querySelector('[data-d-size]').textContent = d.size;
    details.querySelector('[data-d-meta]').textContent = d.meta;
    details.querySelector('[data-d-used]').textContent = d.used === '0' ? 'Not used' : `${d.used} ${d.used === '1' ? 'lesson' : 'lessons'}`;
    details.querySelector('[data-d-url]').value = `https://media.acme.learn/${d.name}`;
  };
  document.querySelectorAll('[name=a4-kind]').forEach((r) => r.addEventListener('change', filter));
  search.addEventListener('input', filter);
  document.querySelectorAll('[name=a4-view]').forEach((r) => r.addEventListener('change', () => { grid.dataset.view = r.value; }));
  grid.addEventListener('change', show);
  details.querySelectorAll('[data-d-delete]').forEach((b) => b.addEventListener('click', () => {
    items().filter((li) => li.querySelector('[data-select]').checked).forEach((li) => li.remove());
    show(); filter();
  }));
  // Uploads: a queue with progress; finished files join the library.
  const queue = document.querySelector('[data-queue]');
  const ICON = { video: grid.querySelector('[data-kind=video] .adm-media-kind svg').outerHTML, image: grid.querySelector('[data-kind=image] .adm-media-kind svg').outerHTML, document: grid.querySelector('[data-kind=document] .adm-media-kind svg').outerHTML };
  const kindOf = (f) => (f.type.startsWith('video/') ? 'video' : f.type.startsWith('image/') ? 'image' : 'document');
  const size = (b) => (b > 1e6 ? `${(b / 1e6).toFixed(1)} MB` : `${Math.max(1, Math.round(b / 1e3))} KB`);
  const upload = (files) => files.forEach((f) => {
    const kind = kindOf(f);
    const li = document.createElement('li');
    li.innerHTML = `${ICON[kind]}<div class="stack" data-gap="1"><strong></strong><div class="progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><span style="width: 0%"></span></div></div><span>0%</span>`;
    li.querySelector('strong').textContent = f.name;
    li.querySelector('.progress').setAttribute('aria-label', `Uploading ${f.name}`);
    queue.append(li);
    let p = 0;
    const t = setInterval(() => {
      p = Math.min(100, p + 9 + Math.round(Math.random() * 12));
      li.querySelector('.progress').setAttribute('aria-valuenow', String(p));
      li.querySelector('.progress > span').style.width = `${p}%`;
      li.lastElementChild.textContent = p === 100 ? 'Done' : `${p}%`;
      if (p < 100) return;
      clearInterval(t);
      li.setAttribute('data-done', '');
      const card = grid.querySelector(`[data-kind=${kind}]`)?.cloneNode(true) || grid.querySelector('[data-media]').cloneNode(true);
      Object.assign(card.dataset, { kind, name: f.name, size: size(f.size), meta: kind === 'document' ? 'File' : 'Processing', used: '0' });
      card.querySelector('strong').textContent = f.name;
      card.querySelector('small').textContent = size(f.size);
      const box = card.querySelector('[data-select]');
      box.checked = false;
      box.setAttribute('aria-label', `Select ${f.name}`);
      grid.prepend(card);
      filter();
      setTimeout(() => li.remove(), 2500);
    }, 200);
  });
  document.querySelector('[data-file]').addEventListener('change', (e) => { upload([...e.target.files]); e.target.value = ''; });
  const drop = document.querySelector('[data-drop]');
  ['dragenter', 'dragover'].forEach((t) => drop.addEventListener(t, (e) => { e.preventDefault(); drop.setAttribute('data-over', ''); }));
  ['dragleave', 'drop'].forEach((t) => drop.addEventListener(t, (e) => { e.preventDefault(); drop.removeAttribute('data-over'); }));
  drop.addEventListener('drop', (e) => upload([...e.dataTransfer.files]));
  filter();
})();
"""))

# ---------------------------------------------------------------- admin-05: students
STUDENTS = [("Maya Chen", "maya.chen@example.com", "Brand Identity Design", 100, "Today", "Mar 2, 2026", "active"), ("Daniel Okafor", "d.okafor@example.com", "Brand Identity Design", 64, "Yesterday", "Apr 18, 2026", "active"),
            ("Sofia Rossi", "sofia.r@example.com", "Watercolor Botanicals", 38, "3 days ago", "May 9, 2026", "active"), ("Liam Nguyen", "liam.nguyen@example.com", "Hand Lettering Masterclass", 12, "2 weeks ago", "Jun 1, 2026", "inactive"),
            ("Ava Johnson", "ava.j@example.com", "Watercolor Botanicals", 91, "Today", "Jan 27, 2026", "active"), ("Noah Schmidt", "noah.s@example.com", "Product Photography", 0, "Never", "Nov 2, 2026", "inactive"),
            ("Hana Sato", "hana.sato@example.com", "Brand Identity Design", 47, "5 days ago", "Aug 14, 2026", "active"), ("Lucas Martin", "lucas.m@example.com", "Hand Lettering Masterclass", 100, "1 month ago", "Feb 3, 2026", "inactive")]
COURSE_SHORT = ["Brand Identity Design", "Watercolor Botanicals", "Hand Lettering Masterclass", "Product Photography"]
a5_rows = "\n".join(f"""<tr data-row data-status="{st}" data-filter="{c}">
  <td><input type="checkbox" class="input" data-select aria-label="Select {n}"></td>
  <td><div class="adm-person"><span class="avatar" data-size="sm"><span>{initials(n)}</span></span><span><strong>{n}</strong><small>{e}</small></span></div></td>
  <td>{c}</td>
  <td><div class="adm-progress"><span class="adm-bar"><span style="width: {p}%"></span></span><span>{p}%</span></div></td>
  <td class="adm-muted">{la}</td>
  <td class="adm-muted">{en}</td>
  <td>{row_menu(f"a5-m{i}", [("Message", "mail", False, ""), ("View progress", "chart-column", False, ""), ("Remove from course", "trash-2", True, "data-row-delete")])}</td>
</tr>""" for i, (n, e, c, p, la, en, st) in enumerate(STUDENTS))
A5_KPIS = [("Total students", "71,680", "+1,240", "this month", False), ("Active this week", "8,412", "+6.2%", "vs last week", False), ("Avg. completion", "46%", "+2.1%", "vs last month", False), ("Certificates issued", "12,905", "-3.4%", "vs last month", True)]


def kpi(label, value, delta, note, down=False, attrs=""):
    return (f'<div class="card adm-kpi"{attrs}><p>{label}</p><strong data-kpi-value>{value}</strong>'
            f'<span class="adm-trend"{" data-down" if down else ""} data-kpi-trend>{si("trending-up")}<b data-kpi-delta>{delta}</b><span>{note}</span></span></div>')


add("admin-05", "Admin 05", "Students: KPIs, search, course and activity filters, progress bars, bulk messaging, CSV export and an invite dialog.", "admin", adm_shell("Students", ["Instructor", "Students"], f"""
<div class="adm-title"><div><h1>Students</h1><p>Everyone enrolled in your courses.</p></div>
  <div><button type="button" class="btn" data-variant="outline" data-export>{si("download")}Export CSV</button><button type="button" class="btn" commandfor="a5-invite" command="show-modal">{si("mail")}Invite students</button></div></div>
<div class="adm-kpis">{"".join(kpi(*k) for k in A5_KPIS)}</div>
<div class="stack" data-gap="4" data-adm-table id="a5-table">
  {tabs_filter([("all", "All"), ("active", "Active"), ("inactive", "Inactive"), ("invited", "Invited")])}
  <div class="adm-toolbar">{search_box("Search by name or email...", "Search students")}<span class="adm-grow"></span><label class="sr-only" for="a5-course">Course</label><select class="select" id="a5-course" data-filter-select><option value="all">All courses</option>{"".join(f"<option>{c}</option>" for c in COURSE_SHORT)}</select></div>
  <div class="adm-table-wrap"><table class="table">
    <thead><tr><th><input type="checkbox" class="input" data-select-all aria-label="Select all students"></th><th>Student</th><th>Course</th><th>Progress</th><th>Last active</th><th>Enrolled</th><th><span class="sr-only">Actions</span></th></tr></thead>
    <tbody>
{a5_rows}
      <tr class="adm-empty-row" data-empty hidden><td colspan="7">No students match your filters.</td></tr>
    </tbody>
  </table></div>
  <div class="adm-bulk" data-bulk hidden role="region" aria-label="Bulk actions"><strong data-bulk-count>0 selected</strong>
    <button type="button" class="btn" data-variant="outline" data-size="sm">{si("mail")}Message</button>
    <button type="button" class="btn" data-variant="outline" data-size="sm">{si("award")}Issue certificate</button>
    <button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Clear selection" data-bulk-clear>{si("x")}</button>
  </div>
</div>
<dialog id="a5-invite" class="dialog" closedby="any" aria-labelledby="a5-invite-t">
  <div>
    <header><h2 id="a5-invite-t">Invite students</h2><p>They get an email with a link to join. Separate addresses with commas or new lines.</p></header>
    <section><form id="a5-form" class="stack" data-gap="4" novalidate>
      <div role="group" class="field"><label for="a5-emails">Email addresses</label><textarea class="textarea" id="a5-emails" rows="4" placeholder="ana@example.com, ben@example.com" aria-describedby="a5-err"></textarea><p class="adm-err" id="a5-err" data-err hidden></p></div>
      <div role="group" class="field"><label for="a5-icourse">Course</label><select class="select" id="a5-icourse">{"".join(f"<option>{c}</option>" for c in COURSE_SHORT)}</select></div>
      <div role="group" class="field" data-orientation="horizontal"><input type="checkbox" role="switch" class="input" id="a5-free" checked><label for="a5-free">Give free access</label></div>
    </form></section>
    <footer><button type="button" class="btn" data-variant="outline" commandfor="a5-invite" command="close">Cancel</button><button type="submit" form="a5-form" class="btn">{si("send")}Send invites</button></footer>
  </div>
  <button type="button" aria-label="Close dialog" commandfor="a5-invite" command="close">{si("x")}</button>
</dialog>
"""), ADM + "\n  .adm-err { margin: 0; color: var(--destructive); font-size: 0.8125rem; }", scripts=script(ADM_JS + """
(() => {
  const root = document.getElementById('a5-table');
  document.querySelector('[data-export]').addEventListener('click', () => {
    const rows = [...root.querySelectorAll('tr[data-row]:not([hidden])')].map((r) => {
      const c = r.querySelectorAll('td');
      return [c[1].querySelector('strong').textContent, c[1].querySelector('small').textContent, c[2].textContent, c[3].innerText.trim(), c[4].textContent, c[5].textContent];
    });
    const csv = [['Name', 'Email', 'Course', 'Progress', 'Last active', 'Enrolled'], ...rows].map((r) => r.map((v) => `"${String(v).replaceAll('"', '""')}"`).join(',')).join('\\n');
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }));
    a.download = 'students.csv';
    a.click();
    URL.revokeObjectURL(a.href);
  });
  document.getElementById('a5-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const box = document.getElementById('a5-emails');
    const err = e.target.querySelector('[data-err]');
    const list = box.value.split(/[\\s,;]+/).filter(Boolean);
    const bad = list.filter((m) => !/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(m));
    const msg = !list.length ? 'Add at least one email address.' : bad.length ? `Check ${bad.join(', ')}.` : '';
    err.textContent = msg;
    err.hidden = !msg;
    box.toggleAttribute('aria-invalid', !!msg);
    if (msg) { box.focus(); return; }
    const course = document.getElementById('a5-icourse').value;
    const tpl = root.querySelector('tr[data-row]');
    list.reverse().forEach((m) => {
      const tr = tpl.cloneNode(true);
      tr.hidden = false;
      tr.dataset.status = 'invited';
      tr.dataset.filter = course;
      tr.querySelector('[data-select]').checked = false;
      tr.querySelector('[data-select]').setAttribute('aria-label', `Select ${m}`);
      tr.querySelector('.avatar span').textContent = m[0].toUpperCase();
      tr.querySelector('.adm-person strong').textContent = m.split('@')[0];
      tr.querySelector('.adm-person small').textContent = m;
      const c = tr.querySelectorAll('td');
      c[2].textContent = course;
      c[3].innerHTML = '<span class="badge adm-status" data-variant="outline" data-status="invited">Invited</span>';
      c[4].textContent = '—';
      c[5].textContent = 'Pending';
      c[6].innerHTML = '';
      root.querySelector('tbody').prepend(tr);
    });
    root.admRefresh();
    box.value = '';
    document.getElementById('a5-invite').close();
  });
})();
"""))

# ---------------------------------------------------------------- admin-06: analytics
RANGES = {
    "7d": {"labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "values": [1840, 2210, 1960, 2580, 3120, 2740, 2380], "kpis": ["$16,830", "+8.4%", "1,204", "+5.1%", "47%", "+1.2%", "4.8", "+0.1"]},
    "30d": {"labels": ["W1", "W2", "W3", "W4"], "values": [14200, 16850, 15420, 18930], "kpis": ["$65,400", "+12.6%", "4,870", "+9.8%", "46%", "+2.1%", "4.8", "0.0"]},
    "12m": {"labels": ["Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov"], "values": [42100, 51800, 48300, 55200, 58900, 54100, 61200, 59800, 63400, 66100, 64200, 65400], "kpis": ["$690,500", "+31.2%", "58,320", "+24.5%", "45%", "+4.0%", "4.8", "+0.2"]},
}
TOP = [("Brand Identity Design from Scratch", 412300, 28940, 4.8, 2), ("Hand Lettering Masterclass", 228150, 15210, 4.8, 3), ("Watercolor Botanicals for Beginners", 186200, 12480, 4.9, 3), ("Product Photography at Home", 97400, 8930, 4.7, 1), ("Motion Design Basics", 73440, 6120, 4.6, 1)]
SOURCES = [("Marketplace search", 48), ("Your promotions", 22), ("Direct", 14), ("Social", 11), ("Affiliates", 5)]
ACTIVITY = [("Maya Chen", "completed", "Brand Identity Design", "12 min ago"), ("Daniel Okafor", "left a 5-star review on", "Brand Identity Design", "40 min ago"), ("Sofia Rossi", "enrolled in", "Watercolor Botanicals", "1 hour ago"), ("Hana Sato", "asked a question in", "Brand Identity Design", "3 hours ago")]
top_max = TOP[0][1]
top_rows = "".join(f'<tr><td><div class="adm-course">{shot(n)}<span><strong>{t}</strong><small>{s:,} students · {r}★</small></span></div></td><td class="adm-num">{usd(rev)}</td><td><span class="adm-bar"><span style="width: {round(rev / top_max * 100)}%"></span></span></td></tr>' for t, rev, s, r, n in TOP)
import json as _json
bars = "".join(f'<li style="--h: {round(v / max(RANGES["30d"]["values"]) * 100)}%"><span class="adm-chart-bar" tabindex="0" aria-label="{l}: {usd(v)}"><span class="adm-chart-tip">{usd(v)}</span></span><small>{l}</small></li>' for l, v in zip(RANGES["30d"]["labels"], RANGES["30d"]["values"]))
K = RANGES["30d"]["kpis"]

add("admin-06", "Admin 06", "Instructor analytics: a date range that updates KPIs and a revenue chart with tooltips, top courses, traffic sources and recent activity.", "admin", adm_shell("Dashboard", ["Instructor", "Dashboard"], f"""
<div class="adm-title"><div><h1>Welcome back, Lena</h1><p>Here's how your courses are doing.</p></div>
  <div><fieldset class="toggle-group" data-variant="outline" data-size="sm" data-range><legend class="sr-only">Date range</legend>{"".join(f'<label class="toggle"><input type="radio" name="a6-range" value="{k}"{" checked" if k == "30d" else ""}>{l}</label>' for k, l in [("7d", "7 days"), ("30d", "30 days"), ("12m", "12 months")])}</fieldset></div></div>
<div class="adm-kpis" data-kpis>
  {kpi("Revenue", K[0], K[1], "vs previous period")}
  {kpi("Enrollments", K[2], K[3], "vs previous period")}
  {kpi("Completion rate", K[4], K[5], "vs previous period")}
  {kpi("Average rating", K[6], K[7], "vs previous period")}
</div>
<div class="adm-dash">
  <section class="card adm-chart-card"><header><h2>Revenue</h2><p data-chart-note>Weekly, last 30 days</p></header><section>
    <div class="adm-chart"><div class="adm-chart-grid" aria-hidden="true"><span></span><span></span><span></span><span></span></div><ol class="adm-chart-bars" data-bars aria-label="Revenue by period">{bars}</ol></div>
  </section></section>
  <section class="card"><header><h2>Traffic sources</h2><p>Where new students come from</p></header><section><ul class="adm-sources">{"".join(f'<li><span>{n}</span><span class="adm-bar"><span style="width: {p}%"></span></span><b>{p}%</b></li>' for n, p in SOURCES)}</ul></section></section>
  <section class="card adm-top"><header><h2>Top courses</h2><div class="card-action"><a href="#" class="btn" data-variant="ghost" data-size="sm">View all</a></div></header><section><table class="table"><thead><tr><th>Course</th><th class="adm-num">Revenue</th><th><span class="sr-only">Share</span></th></tr></thead><tbody>{top_rows}</tbody></table></section></section>
  <section class="card"><header><h2>Recent activity</h2></header><section><ul class="adm-feed">{"".join(f'<li><span class="avatar" data-size="sm"><span>{initials(n)}</span></span><p><strong>{n}</strong> {a} <strong>{c}</strong><small>{t}</small></p></li>' for n, a, c, t in ACTIVITY)}</ul></section></section>
</div>
"""), ADM + """
  .adm-dash { display: grid; gap: 1rem; }
  @container (width >= 56rem) { .adm-dash { grid-template-columns: minmax(0, 2fr) minmax(0, 1fr); } }
  .adm-chart { position: relative; block-size: 16rem; }
  .adm-chart-grid { position: absolute; inset: 0 0 1.5rem; display: grid; grid-template-rows: repeat(4, 1fr); }
  .adm-chart-grid span { border-block-start: 1px dashed var(--border); }
  .adm-chart-bars { position: relative; display: flex; align-items: flex-end; gap: 0.5rem; block-size: 100%; margin: 0; padding: 0; list-style: none; }
  .adm-chart-bars li { flex: 1; display: grid; grid-template-rows: minmax(0, 1fr) 1.5rem; justify-items: center; block-size: 100%; }
  .adm-chart-bar { position: relative; align-self: end; inline-size: min(100%, 3rem); block-size: var(--h); border-radius: calc(var(--radius) - 2px) calc(var(--radius) - 2px) 2px 2px; background: var(--chart-1, var(--primary)); transition: block-size 300ms ease, background-color 150ms ease; outline: none; }
  .adm-chart-bar:hover, .adm-chart-bar:focus-visible { background: color-mix(in oklab, var(--chart-1, var(--primary)) 80%, var(--foreground)); }
  .adm-chart-bar:focus-visible { box-shadow: 0 0 0 2px var(--background), 0 0 0 4px var(--ring); }
  .adm-chart-tip { position: absolute; inset-block-end: calc(100% + 0.375rem); inset-inline-start: 50%; translate: -50% 0; padding: 0.25rem 0.5rem; border-radius: calc(var(--radius) - 2px); background: var(--foreground); color: var(--background); font-size: 0.75rem; font-weight: 500; white-space: nowrap; opacity: 0; pointer-events: none; transition: opacity 150ms ease; }
  .adm-chart-bar:is(:hover, :focus-visible) .adm-chart-tip { opacity: 1; }
  .adm-chart-bars small { align-self: end; color: var(--muted-foreground); font-size: 0.75rem; }
  .adm-sources { display: grid; gap: 0.875rem; margin: 0; padding: 0; list-style: none; font-size: 0.875rem; }
  .adm-sources li { display: grid; grid-template-columns: minmax(0, 1fr) 5rem 2.5rem; align-items: center; gap: 0.75rem; }
  .adm-sources b { font-weight: 500; text-align: end; font-variant-numeric: tabular-nums; }
  .adm-top .table td { vertical-align: middle; }
  .adm-top .adm-bar { inline-size: 6rem; }
  .adm-feed { display: grid; gap: 1rem; margin: 0; padding: 0; list-style: none; }
  .adm-feed li { display: flex; gap: 0.75rem; }
  .adm-feed p { margin: 0; font-size: 0.8125rem; line-height: 1.45; }
  .adm-feed strong { font-weight: 500; }
  .adm-feed small { display: block; color: var(--muted-foreground); font-size: 0.75rem; }
  @media (prefers-reduced-motion: reduce) { .adm-chart-bar { transition: none; } }""", scripts=script(ADM_JS + f"""
(() => {{
  const DATA = {_json.dumps(RANGES)};
  const NOTE = {{ '7d': 'Daily, last 7 days', '30d': 'Weekly, last 30 days', '12m': 'Monthly, last 12 months' }};
  const fmt = (v) => `$${{v.toLocaleString('en-US')}}`;
  const draw = (k) => {{
    const d = DATA[k];
    const max = Math.max(...d.values);
    const ol = document.querySelector('[data-bars]');
    ol.innerHTML = d.values.map((v, i) => `<li style="--h: ${{Math.round((v / max) * 100)}}%"><span class="adm-chart-bar" tabindex="0" aria-label="${{d.labels[i]}}: ${{fmt(v)}}"><span class="adm-chart-tip">${{fmt(v)}}</span></span><small>${{d.labels[i]}}</small></li>`).join('');
    document.querySelector('[data-chart-note]').textContent = NOTE[k];
    document.querySelectorAll('[data-kpis] > .adm-kpi').forEach((c, i) => {{
      c.querySelector('[data-kpi-value]').textContent = d.kpis[i * 2];
      const delta = d.kpis[i * 2 + 1];
      c.querySelector('[data-kpi-delta]').textContent = delta;
      c.querySelector('[data-kpi-trend]').toggleAttribute('data-down', delta.startsWith('-'));
    }});
  }};
  document.querySelectorAll('[name=a6-range]').forEach((r) => r.addEventListener('change', () => draw(r.value)));
}})();
"""))

# ---------------------------------------------------------------- admin-07: pricing and coupons
COUPONS = [("LEARN20", "20% off", 412, 1000, "Dec 31, 2026", True), ("BLACKFRIDAY", "40% off", 1280, None, "Nov 30, 2026", True), ("WELCOME10", "$10 off", 96, 500, "No expiry", True), ("SUMMER25", "25% off", 731, 750, "Aug 31, 2026", False)]


def coupon_row(i, code, off, used, limit, exp, active):
    lim = f"{used:,} / {limit:,}" if limit else f"{used:,}"
    return f"""<tr data-coupon>
  <td><span class="adm-code"><code id="a7-c{i}">{code}</code>{copy_btn(f"#a7-c{i}", f"Copy {code}")}</span></td>
  <td>{off}</td><td class="adm-num">{lim}</td><td class="adm-muted">{exp}</td>
  <td><input type="checkbox" role="switch" class="input" aria-label="{code} active"{" checked" if active else ""}></td>
  <td><button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Delete {code}" data-del-coupon>{si("trash-2")}</button></td>
</tr>"""


MODELS = [("free", "Free", "Anyone can enroll"), ("one", "One-time", "Pay once, lifetime access"), ("sub", "Subscription", "Monthly or yearly access"), ("plan", "Payment plan", "Split the price into installments")]
models = "".join(f'<label class="adm-model"><input type="radio" name="a7-model" value="{v}" class="input"{" checked" if v == "one" else ""}><strong>{t}</strong><small>{d}</small></label>' for v, t, d in MODELS)

add("admin-07", "Admin 07", "Course pricing and coupons: pricing models with the fields each needs, a live student-facing price preview, and coupons you can create, copy, pause and delete.", "admin", adm_shell("Pricing", ["Courses", "Brand Identity Design", "Pricing"], f"""
<div class="adm-title"><div><h1>Pricing</h1><p>Brand Identity Design from Scratch</p></div><div><span class="adm-saved" data-saved role="status">All changes saved</span><button type="button" class="btn" data-save>Save pricing</button></div></div>
<div class="adm-split">
  <div class="stack" data-gap="6">
    <section class="card"><header><h2>Pricing model</h2><p>How students pay for this course.</p></header><section class="stack" data-gap="6">
      <fieldset class="adm-models"><legend class="sr-only">Pricing model</legend>{models}</fieldset>
      <div class="adm-price-fields" data-fields>
        <div role="group" class="field" data-for="one sub plan"><label for="a7-cur">Currency</label><select class="select" id="a7-cur" data-cur><option value="USD">USD $</option><option value="EUR">EUR €</option><option value="VND">VND ₫</option></select></div>
        <div role="group" class="field" data-for="one plan"><label for="a7-price">Price</label><input class="input" id="a7-price" type="number" min="0" step="1" value="89" data-price></div>
        <div role="group" class="field" data-for="one"><label for="a7-sale">Sale price <span class="adm-muted">(optional)</span></label><input class="input" id="a7-sale" type="number" min="0" step="1" value="59" data-sale></div>
        <div role="group" class="field" data-for="sub"><label for="a7-month">Monthly</label><input class="input" id="a7-month" type="number" min="0" step="1" value="19" data-month></div>
        <div role="group" class="field" data-for="sub"><label for="a7-year">Yearly</label><input class="input" id="a7-year" type="number" min="0" step="1" value="159" data-year></div>
        <div role="group" class="field" data-for="plan"><label for="a7-n">Installments</label><select class="select" id="a7-n" data-n><option value="2">2</option><option value="3" selected>3</option><option value="4">4</option><option value="6">6</option></select></div>
      </div>
    </section></section>
    <section class="card"><header><h2>Coupons</h2><p>Discount codes students enter at checkout.</p><div class="card-action"><button type="button" class="btn" data-variant="outline" data-size="sm" commandfor="a7-new" command="show-modal">{si("plus")}New coupon</button></div></header><section>
      <div class="adm-table-wrap"><table class="table" style="min-inline-size: 36rem"><thead><tr><th>Code</th><th>Discount</th><th class="adm-num">Used</th><th>Expires</th><th>Active</th><th><span class="sr-only">Delete</span></th></tr></thead><tbody data-coupons>{"".join(coupon_row(i, *c) for i, c in enumerate(COUPONS))}</tbody></table></div>
    </section></section>
  </div>
  <aside><div class="card"><header><h2>Preview</h2><p>What students see on the course page.</p></header><section>
    <div class="adm-preview">{shot(2)}<div class="stack" data-gap="1"><p class="adm-preview-price" data-preview-price></p><p class="adm-muted" data-preview-note></p></div><span class="btn" data-preview-cta>Buy now</span></div>
  </section></div></aside>
</div>
<dialog id="a7-new" class="dialog" closedby="any" aria-labelledby="a7-new-t">
  <div>
    <header><h2 id="a7-new-t">New coupon</h2><p>Codes are not case sensitive.</p></header>
    <section><form id="a7-form" class="stack" data-gap="4" novalidate>
      <div role="group" class="field"><label for="a7-code">Code</label><div class="cluster" data-gap="2" style="flex-wrap: nowrap"><input class="input" id="a7-code" maxlength="20" placeholder="SPRING30" style="text-transform: uppercase" aria-describedby="a7-code-err"><button type="button" class="btn" data-variant="outline" data-gen>{si("refresh-cw")}Generate</button></div><p class="adm-err" id="a7-code-err" data-code-err hidden>Use 4–20 letters or numbers.</p></div>
      <fieldset class="toggle-group" data-variant="outline"><legend>Discount type</legend><label class="toggle"><input type="radio" name="a7-type" value="pct" checked>Percent</label><label class="toggle"><input type="radio" name="a7-type" value="amt">Fixed amount</label></fieldset>
      <div class="adm-price-fields">
        <div role="group" class="field"><label for="a7-val">Amount</label><input class="input" id="a7-val" type="number" min="1" max="100" value="20"></div>
        <div role="group" class="field"><label for="a7-limit">Usage limit</label><input class="input" id="a7-limit" type="number" min="1" placeholder="Unlimited"></div>
        <div role="group" class="field"><label for="a7-exp">Expires</label><input class="input" id="a7-exp" type="date"></div>
      </div>
    </form></section>
    <footer><button type="button" class="btn" data-variant="outline" commandfor="a7-new" command="close">Cancel</button><button type="submit" form="a7-form" class="btn">Create coupon</button></footer>
  </div>
  <button type="button" aria-label="Close dialog" commandfor="a7-new" command="close">{si("x")}</button>
</dialog>
"""), ADM + SUCCESS_CSS + """
  .adm-models { display: grid; gap: 0.75rem; grid-template-columns: repeat(auto-fit, minmax(min(100%, 11rem), 1fr)); margin: 0; padding: 0; border: 0; }
  .adm-model { position: relative; display: grid; gap: 0.125rem; padding: 0.875rem 1rem; padding-inline-end: 2.5rem; border: 1px solid var(--border); border-radius: var(--radius); cursor: pointer; }
  .adm-model:hover { background: var(--accent); }
  .adm-model:has(:checked) { border-color: var(--primary); box-shadow: 0 0 0 1px var(--primary); }
  .adm-model:has(:focus-visible) { outline: 2px solid var(--ring); outline-offset: 2px; }
  .adm-model input { position: absolute; inset-block-start: 0.875rem; inset-inline-end: 0.875rem; }
  .adm-model strong { font-size: 0.875rem; font-weight: 600; }
  .adm-model small { font-size: 0.75rem; color: var(--muted-foreground); }
  .adm-price-fields { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(min(100%, 9rem), 1fr)); }
  .adm-price-fields .field[hidden] { display: none; }
  .adm-err { margin: 0; color: var(--destructive); font-size: 0.8125rem; }
  .adm-code { display: inline-flex; align-items: center; gap: 0.25rem; }
  .adm-code code { padding: 0.125rem 0.375rem; border-radius: calc(var(--radius) - 4px); background: var(--muted); font-size: 0.8125rem; font-weight: 600; letter-spacing: 0.04em; }
  tr[data-coupon]:has([role=switch]:not(:checked)) > td:not(:nth-last-child(-n+2)) { opacity: 0.55; }
  .adm-preview { display: grid; gap: 0.75rem; }
  .adm-preview img { aspect-ratio: 16 / 9; inline-size: 100%; border-radius: calc(var(--radius) - 2px); object-fit: cover; }
  .adm-preview p { margin: 0; }
  .adm-preview-price { display: flex; align-items: baseline; flex-wrap: wrap; gap: 0.5rem; font-size: 1.75rem; font-weight: 700; letter-spacing: -0.02em; }
  .adm-preview-price s { font-size: 1rem; font-weight: 400; color: var(--muted-foreground); }
  .adm-preview-price .badge { font-size: 0.75rem; letter-spacing: 0; }
  .adm-preview .adm-muted { font-size: 0.8125rem; }
  .adm-preview > .btn { inline-size: 100%; pointer-events: none; }""", scripts=script(ADM_JS + """
(() => {
  const $ = (s) => document.querySelector(s);
  const saved = $('[data-saved]');
  const dirty = () => { saved.setAttribute('data-dirty', ''); saved.textContent = 'Unsaved changes'; };
  $('[data-save]').addEventListener('click', () => { saved.removeAttribute('data-dirty'); saved.textContent = 'Saved just now'; });
  const SYM = { USD: (v) => `$${v.toLocaleString('en-US')}`, EUR: (v) => `€${v.toLocaleString('de-DE')}`, VND: (v) => `${v.toLocaleString('vi-VN')} ₫` };
  const preview = () => {
    const model = document.querySelector('[name=a7-model]:checked').value;
    document.querySelectorAll('[data-for]').forEach((f) => { f.hidden = !f.dataset.for.split(' ').includes(model); });
    const f = SYM[$('[data-cur]').value];
    const n = (s) => Math.max(0, Number($(s).value) || 0);
    let price = '', note = '', cta = 'Buy now';
    if (model === 'free') { price = 'Free'; note = 'Enroll for free, no card needed.'; cta = 'Enroll for free'; }
    if (model === 'one') {
      const p = n('[data-price]'), s = n('[data-sale]');
      price = s && s < p ? `${f(s)} <s>${f(p)}</s> <span class="badge" data-variant="secondary">${Math.round((1 - s / p) * 100)}% off</span>` : f(p);
      note = 'One-time payment · Lifetime access';
    }
    if (model === 'sub') {
      const m = n('[data-month]'), y = n('[data-year]');
      price = `${f(m)}<s style="text-decoration: none">/month</s>`;
      note = y && m ? `or ${f(y)}/year, save ${Math.max(0, Math.round((1 - y / (m * 12)) * 100))}%` : '';
      cta = 'Subscribe';
    }
    if (model === 'plan') {
      const p = n('[data-price]'), k = Number($('[data-n]').value);
      price = `${k} × ${f(Math.ceil((p / k) * 100) / 100)}`;
      note = `${f(p)} total, billed monthly`;
      cta = 'Start payment plan';
    }
    $('[data-preview-price]').innerHTML = price;
    $('[data-preview-note]').textContent = note;
    $('[data-preview-cta]').textContent = cta;
  };
  document.querySelectorAll('[name=a7-model], [data-fields] input, [data-fields] select').forEach((el) => el.addEventListener('input', () => { preview(); dirty(); }));
  preview();
  // Coupons.
  const body = $('[data-coupons]');
  body.addEventListener('click', (e) => { const b = e.target.closest('[data-del-coupon]'); if (b) b.closest('tr').remove(); });
  $('[data-gen]').addEventListener('click', () => {
    const A = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    $('#a7-code').value = Array.from({ length: 8 }, () => A[Math.floor(Math.random() * A.length)]).join('');
  });
  let n = body.children.length;
  $('#a7-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const code = $('#a7-code').value.trim().toUpperCase();
    const ok = /^[A-Z0-9]{4,20}$/.test(code);
    $('[data-code-err]').hidden = ok;
    $('#a7-code').toggleAttribute('aria-invalid', !ok);
    if (!ok) { $('#a7-code').focus(); return; }
    const pct = document.querySelector('[name=a7-type]:checked').value === 'pct';
    const v = Number($('#a7-val').value) || 0;
    const limit = Number($('#a7-limit').value) || 0;
    const exp = $('#a7-exp').value ? new Date($('#a7-exp').value + 'T00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'No expiry';
    const tr = body.querySelector('tr').cloneNode(true);
    const id = `a7-c${n++}`;
    const c = tr.querySelectorAll('td');
    const codeEl = c[0].querySelector('code');
    codeEl.id = id;
    codeEl.textContent = code;
    c[0].querySelector('[data-copy]').dataset.copy = `#${id}`;
    c[0].querySelector('[data-copy]').setAttribute('aria-label', `Copy ${code}`);
    c[1].textContent = pct ? `${v}% off` : `$${v} off`;
    c[2].textContent = limit ? `0 / ${limit.toLocaleString('en-US')}` : '0';
    c[3].textContent = exp;
    const sw = c[4].querySelector('[role=switch]');
    sw.checked = true;
    sw.setAttribute('aria-label', `${code} active`);
    c[5].querySelector('button').setAttribute('aria-label', `Delete ${code}`);
    body.prepend(tr);
    e.target.reset();
    $('#a7-new').close();
  });
})();
"""))

# ---------------------------------------------------------------- admin-08: review moderation
A_REVIEWS = [("Maya Chen", 5, "Brand Identity Design", "2 hours ago", "The mood board lesson alone was worth it. I finally have a process I can explain to clients instead of just showing them logos.", None, False),
             ("Tom Becker", 2, "Hand Lettering Masterclass", "Yesterday", "Audio in section 3 is really quiet and the brush recommendations are hard to find outside the US.", None, False),
             ("Ava Johnson", 5, "Watercolor Botanicals", "2 days ago", "Gentle, clear and so calming. The exercises build on each other perfectly.", "Thank you, Ava! Can't wait to see your leaves.", False),
             ("anon_user_42", 1, "Brand Identity Design", "3 days ago", "Buy cheap followers at my site!!! Best prices", None, True),
             ("Daniel Okafor", 4, "Brand Identity Design", "1 week ago", "Great structure. I'd love a bonus lesson on presenting to stakeholders.", None, False)]


def review_item(i, name, r, course, when, text, reply, flagged):
    rep = f'<div class="adm-reply" data-reply-shown><span class="avatar" data-size="sm"><span>LO</span></span><p><strong>Your reply</strong>{reply}</p></div>' if reply else ""
    status = "replied" if reply else "pending"
    return f"""<li class="adm-review" data-review data-rating="{r}" data-state="{status}"{" data-flagged" if flagged else ""}>
  <span class="avatar"><span>{initials(name.replace("_", " "))}</span></span>
  <div class="stack" data-gap="2">
    <div class="adm-review-head"><strong>{name}</strong><span class="adm-stars" aria-label="{r} out of 5 stars">{stars(r)}</span><span class="adm-muted">{course} · {when}</span>
      <span class="badge" data-variant="destructive" data-flag-badge>Flagged</span><span class="badge" data-variant="secondary" data-hidden-badge>Hidden</span></div>
    <p class="adm-review-text">{text}</p>
    {rep}
    <form class="adm-reply-form" data-reply-form hidden><label class="sr-only" for="a8-r{i}">Reply to {name}</label><textarea class="textarea" id="a8-r{i}" rows="3" placeholder="Write a public reply..."></textarea><div class="cluster" data-gap="2"><button type="submit" class="btn" data-size="sm">Post reply</button><button type="button" class="btn" data-variant="ghost" data-size="sm" data-reply-cancel>Cancel</button></div></form>
    <div class="cluster adm-review-actions" data-gap="1">
      <button type="button" class="btn" data-variant="ghost" data-size="sm" data-reply-open{" hidden" if reply else ""}>{si("reply")}Reply</button>
      <button type="button" class="btn" data-variant="ghost" data-size="sm" data-flag aria-pressed="{str(flagged).lower()}">{si("flag")}<span>{"Unflag" if flagged else "Flag"}</span></button>
      <button type="button" class="btn" data-variant="ghost" data-size="sm" data-hide aria-pressed="false">{si("eye-off")}<span>Hide</span></button>
    </div>
  </div>
</li>"""


DIST = [(5, 72), (4, 18), (3, 6), (2, 3), (1, 1)]
add("admin-08", "Admin 08", "Review moderation: rating summary, filters for needs reply, flagged and low ratings, inline public replies, flag and hide.", "admin", adm_shell("Reviews", ["Instructor", "Reviews"], f"""
<div class="adm-title"><div><h1>Reviews</h1><p>Reply to students and keep your course pages clean.</p></div><div><label class="sr-only" for="a8-course">Course</label><select class="select" id="a8-course"><option>All courses</option>{"".join(f"<option>{c}</option>" for c in COURSE_SHORT)}</select></div></div>
<div class="adm-split adm-split-start">
  <div class="stack" data-gap="4" data-reviews>
    <div class="adm-tabs" role="group" aria-label="Filter reviews">{"".join(f'<button type="button" data-rf="{k}" aria-pressed="{str(k == "all").lower()}">{l}<span class="badge" data-variant="secondary">0</span></button>' for k, l in [("all", "All"), ("pending", "Needs reply"), ("flagged", "Flagged"), ("low", "1–2 stars")])}</div>
    <ul class="adm-reviews">{"".join(review_item(i, *r) for i, r in enumerate(A_REVIEWS))}</ul>
    <p class="adm-muted" data-reviews-empty hidden>Nothing here. Nice work.</p>
  </div>
  <aside><div class="card"><header><h2>Average rating</h2></header><section class="stack" data-gap="4">
    <div class="adm-avg"><strong>4.8</strong><span class="adm-stars" aria-label="4.8 out of 5 stars">{stars(4.8)}</span><small class="adm-muted">7,412 reviews</small></div>
    <ul class="adm-dist">{"".join(f'<li><span>{s}★</span><span class="adm-bar"><span style="width: {p}%"></span></span><b>{p}%</b></li>' for s, p in DIST)}</ul>
  </section></div></aside>
</div>
"""), ADM + CATALOG_CSS + REVIEW_CSS + """
  .adm-reviews { display: grid; margin: 0; padding: 0; list-style: none; border: 1px solid var(--border); border-radius: var(--radius); }
  .adm-review { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: 1rem; padding: 1.25rem; }
  .adm-review + .adm-review { border-block-start: 1px solid var(--border); }
  .adm-review[hidden] { display: none; }
  .adm-review[data-hidden] > div > :is(p, .adm-reply) { opacity: 0.5; }
  .adm-review-head { display: flex; flex-wrap: wrap; align-items: center; gap: 0.25rem 0.75rem; font-size: 0.875rem; }
  .adm-review-head .adm-muted { font-size: 0.8125rem; }
  .adm-review-head .badge { display: none; }
  .adm-review[data-flagged] [data-flag-badge], .adm-review[data-hidden] [data-hidden-badge] { display: inline-flex; }
  .adm-stars .shop-stars { color: oklch(0.8 0.16 80); }
  .adm-review-text { margin: 0; font-size: 0.9375rem; line-height: 1.55; }
  .adm-reply { display: flex; gap: 0.75rem; padding: 0.75rem; border-radius: var(--radius); background: var(--muted); }
  .adm-reply p { margin: 0; font-size: 0.875rem; }
  .adm-reply strong { display: block; font-size: 0.8125rem; }
  .adm-reply-form { display: grid; gap: 0.5rem; }
  .adm-reply-form[hidden] { display: none; }
  .adm-review-actions { margin-inline-start: -0.75rem; }
  .adm-review-actions .btn[aria-pressed='true'] { color: var(--destructive); }
  .adm-avg { display: grid; justify-items: start; gap: 0.25rem; }
  .adm-avg > strong { font-size: 2.5rem; font-weight: 700; line-height: 1; letter-spacing: -0.02em; }
  .adm-dist { display: grid; gap: 0.5rem; margin: 0; padding: 0; list-style: none; font-size: 0.8125rem; }
  .adm-dist li { display: grid; grid-template-columns: 2rem minmax(0, 1fr) 2.5rem; align-items: center; gap: 0.5rem; }
  .adm-dist .adm-bar > span { background: oklch(0.8 0.16 80); }
  .adm-dist b { font-weight: 500; text-align: end; font-variant-numeric: tabular-nums; color: var(--muted-foreground); }""", scripts=script(ADM_JS + """
(() => {
  const root = document.querySelector('[data-reviews]');
  const items = () => [...root.querySelectorAll('[data-review]')];
  const tabs = [...root.querySelectorAll('[data-rf]')];
  const TEST = { all: () => true, pending: (r) => r.dataset.state === 'pending', flagged: (r) => r.hasAttribute('data-flagged'), low: (r) => Number(r.dataset.rating) <= 2 };
  let cur = 'all';
  const apply = () => {
    tabs.forEach((t) => { t.querySelector('.badge').textContent = items().filter(TEST[t.dataset.rf]).length; });
    let n = 0;
    items().forEach((r) => { const ok = TEST[cur](r); r.hidden = !ok; n += ok; });
    root.querySelector('[data-reviews-empty]').hidden = n > 0;
  };
  tabs.forEach((t) => t.addEventListener('click', () => { cur = t.dataset.rf; tabs.forEach((x) => x.setAttribute('aria-pressed', String(x === t))); apply(); }));
  root.addEventListener('click', (e) => {
    const r = e.target.closest('[data-review]');
    if (!r) return;
    const form = r.querySelector('[data-reply-form]');
    if (e.target.closest('[data-reply-open]')) { form.hidden = false; form.querySelector('textarea').focus(); }
    if (e.target.closest('[data-reply-cancel]')) { form.hidden = true; r.querySelector('[data-reply-open]').focus(); }
    const flag = e.target.closest('[data-flag]');
    if (flag) {
      const on = r.toggleAttribute('data-flagged');
      flag.setAttribute('aria-pressed', String(on));
      flag.querySelector('span').textContent = on ? 'Unflag' : 'Flag';
      apply();
    }
    const hide = e.target.closest('[data-hide]');
    if (hide) {
      const on = r.toggleAttribute('data-hidden');
      hide.setAttribute('aria-pressed', String(on));
      hide.querySelector('span').textContent = on ? 'Unhide' : 'Hide';
    }
  });
  root.addEventListener('submit', (e) => {
    e.preventDefault();
    const form = e.target;
    const text = form.querySelector('textarea').value.trim();
    if (!text) { form.querySelector('textarea').focus(); return; }
    const r = form.closest('[data-review]');
    const div = document.createElement('div');
    div.className = 'adm-reply';
    div.innerHTML = '<span class="avatar" data-size="sm"><span>LO</span></span><p><strong>Your reply</strong></p>';
    div.querySelector('p').append(text);
    form.before(div);
    form.hidden = true;
    r.querySelector('[data-reply-open]').hidden = true;
    r.dataset.state = 'replied';
    apply();
  });
  apply();
})();
"""))


if __name__ == "__main__":
    from common import register
    register(blocks)
    print(f"shop: {len(blocks)} blocks")

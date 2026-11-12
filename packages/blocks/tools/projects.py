"""projects-01: a workspace of sites. Sidebar, project tiles with a style
preview (logo, typeface, palette), a showcase of site mockups and a What's new
card. Showcases the .tile primitive in .auto-grid; no JavaScript of its own
(the What's new card is a non-modal <dialog open> closed by <form method="dialog">).
"""
from common import page, register, ic
import sidebar as sb

BRAND = "oklch(0.58 0.24 292)"  # violet accent for this block

PROJECTS = [
    # title, when, brand color, font label, font family, palette (fg, bg), logo
    ("Component Update · November", "Just now", BRAND, "Geist", "var(--font-sans)", ("oklch(0.2 0 0)", "white"), True),
    ("Untitled", "5 minutes ago", None, "Serif", "Georgia, serif", ("oklch(0.2 0 0)", "oklch(0.97 0 0)"), False),
    ("Untitled", "3 weeks ago", None, "Serif", "Georgia, serif", ("oklch(0.2 0 0)", "oklch(0.97 0 0)"), False),
]

GLOBE = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>'
CUBE = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2 3 7v10l9 5 9-5V7zm0 3.2 5.9 3.3L12 11.8 6.1 8.5zM5.5 10.3l5.25 2.9v5.9L5.5 16.2zm7.75 8.8v-5.9l5.25-2.9v5.9z"/></svg>'


def site_mark(brand):
    return f'<span class="pj-mark" style="--mark:{brand}">{CUBE}</span>' if brand else f'<span class="pj-mark pj-mark-empty">{GLOBE}</span>'


def project_tile(title, when, brand, font, family, palette, logo):
    fg, bg = palette
    aa_style = f'background:{brand};color:white' if brand else 'background:var(--background);color:color-mix(in oklab, var(--foreground) 25%, transparent)'
    swatch_top = brand or 'oklch(0.96 0 0)'
    preview = (f'<div class="pj-style">'
               f'<div class="pj-logo">{site_mark(brand if logo else None)}</div>'
               f'<div class="pj-aa" style="{aa_style};font-family:{family}"><span>Aa</span><small>{font}</small></div>'
               f'<div class="pj-swatch"><span style="background:{swatch_top}"></span><span style="background:{fg}"></span><span style="background:{bg}"></span></div>'
               f'</div>')
    icon = f'<span class="pj-mini" style="--mark:{brand}">{CUBE}</span>' if brand else GLOBE
    return (f'<figure class="tile" data-ratio="auto">{preview}'
            f'<figcaption>{icon}<a href="#">{title}</a><small>{when}</small></figcaption></figure>')


# Showcase: small site mockups drawn with HTML and CSS (no images needed).
SHOWCASE = [
    ("Component Update · November", "pj-shot-dark", '<p class="pj-shot-kicker">11 · 01 · November 2026</p><p class="pj-shot-h">November Component Update</p><div class="pj-shot-rows"><i></i><i></i><i></i></div>', f'<span class="pj-mini" style="--mark:{BRAND}">{CUBE}</span>'),
    ("Harbourline · Residences by Tidewater", "pj-shot-stone", '<p class="pj-shot-h">Twelve sandstone homes on the harbour headland.</p><p class="pj-shot-sub">Single-level living, private gardens, a short walk to the water.</p>', '<span class="pj-letter">H</span>'),
    ("Linden Pilates Studio", "pj-shot-editorial", '<p class="pj-shot-h">Move in a softer light</p><div class="pj-shot-photo"><i></i><i></i></div>', '<span class="pj-letter" data-tone="sage">L</span>'),
    ("Strata · Run Coaching", "pj-shot-sky", '<p class="pj-shot-h">Every mile coached for the way you live</p><span class="pj-shot-runner"></span>', '<span class="pj-letter" data-tone="ink">S</span>'),
]


def shot_tile(title, cls, inner, icon):
    nav = '<div class="pj-shot-nav"><b></b><i></i><i></i><i></i><i></i><em></em></div>'
    return (f'<figure class="tile" data-ratio="video"><div class="pj-shot {cls}" aria-hidden="true">{nav}{inner}</div>'
            f'<figcaption>{icon}<a href="#">{title}</a></figcaption></figure>')


def item(label, icon_name, active=False, badge=None):
    cur = ' aria-current="page"' if active else ""
    b = f'<span data-badge>{badge}</span>' if badge else ""
    return f'<li><a href="#"{cur} data-tooltip="{label}" data-side="right">{ic(icon_name)}<span>{label}</span>{b}</a></li>'


NAV = (
    f'<header><ul><li><a href="#" data-size="lg">{sb.logo_mark("gallery")}<span><strong>Acme Studio</strong><small>Workspace</small></span></a></li></ul>'
    f'<form class="sb-search" role="search" onsubmit="event.preventDefault()" data-sidebar-hide-collapsed>'
    f'<div class="input-group"><input type="search" placeholder="Search" aria-label="Search sites"><span data-align="inline-start">{ic("search")}</span></div></form></header>'
    '<section>'
    f'<div role="group" aria-label="Actions"><ul>{item("Create site", "plus")}{item("Community", "star")}</ul></div>'
    f'<div role="group" aria-label="Sites"><ul>{item("All sites", "frame", active=True, badge="3")}{item("Created by me", "user")}{item("Shared with me", "send")}</ul></div>'
    f'<div role="group" aria-label="Secondary" class="sb-push"><ul>{item("What’s new", "sparkles")}{item("Help", "life-buoy")}</ul></div>'
    '</section>'
    f'<footer>{sb.nav_user()}</footer>'
)

TABS = [("Publish", "send", True), ("Export", "file", False), ("Studio", "sparkles", False), ("MCP", "terminal", False)]

body = (
    sb.sidebar(NAV, attrs=' data-collapsible="icon"')
    + '<main class="pj-main">'
    + f'<header class="app-header pj-header">{sb.toggle_button()}'
      '<nav class="pj-tabs" aria-label="Workspace">'
      + "".join(f'<a href="#"{" aria-current=\"page\"" if on else ""}>{ic(i)}{t}</a>' for t, i, on in TABS)
      + '</nav></header>'
    + '<div class="pj-body">'
      f'<section aria-labelledby="pj-all"><div class="pj-head"><h1 id="pj-all">All sites</h1>'
      f'<button type="button" class="btn pj-create">{ic("plus")}Create site</button></div>'
      f'<div class="auto-grid" data-min="md">{"".join(project_tile(*p) for p in PROJECTS)}</div></section>'
      f'<section aria-labelledby="pj-showcase"><div class="pj-head"><h2 id="pj-showcase">Showcase</h2></div>'
      f'<div class="auto-grid" data-min="md">{"".join(shot_tile(*s) for s in SHOWCASE)}</div></section>'
    + '</div>'
    + '<dialog class="pj-news" open aria-labelledby="pj-news-title">'
      '<header><p>What’s new</p><form method="dialog"><button type="submit" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Dismiss">'
      f'{ic("x")}</button></form></header>'
      '<div class="pj-news-art" aria-hidden="true"><span>Acme Studio</span><strong>Introducing Studio</strong></div>'
      '<span class="badge" data-variant="secondary">New feature</span>'
      '<h2 id="pj-news-title">On-brand imagery, every time</h2>'
      '<a href="#" class="btn" data-variant="outline" data-size="sm">Read update</a>'
      '</dialog>'
    + '</main>'
)

CSS = sb.SB_CSS + f"""
  .pj-main {{ container-type: inline-size; min-inline-size: 0; position: relative; }}
  .pj-header {{ block-size: 3.25rem; gap: 0.5rem; }}
  .pj-tabs {{ margin-inline-start: auto; display: flex; align-items: stretch; align-self: stretch; gap: 0.25rem; overflow-x: auto; }}
  .pj-tabs a {{ display: inline-flex; align-items: center; gap: 0.5rem; padding-inline: 0.75rem; font-size: 0.875rem; font-weight: 500; color: var(--muted-foreground); text-decoration: none; border-block-end: 2px solid transparent; white-space: nowrap; }}
  .pj-tabs a svg {{ inline-size: 1rem; block-size: 1rem; }}
  .pj-tabs a:hover {{ color: var(--foreground); }}
  .pj-tabs a[aria-current="page"] {{ color: var(--foreground); border-color: var(--foreground); }}
  .pj-body {{ display: flex; flex-direction: column; gap: 2.5rem; padding: 1.75rem 2rem 6rem; }}
  .pj-head {{ display: flex; align-items: center; justify-content: space-between; gap: 1rem; margin-block-end: 1rem; }}
  .pj-head h1, .pj-head h2 {{ margin: 0; font-size: 1.25rem; font-weight: 500; letter-spacing: -0.01em; }}
  .pj-create {{ background: {BRAND}; color: white; }}
  .pj-create:hover {{ background: color-mix(in oklab, {BRAND} 88%, black); }}
  /* Style preview: logo on top, then typeface and palette */
  .pj-style {{ display: grid; grid-template-columns: 1.7fr 1fr; grid-template-rows: 9.5rem 6rem; gap: 0.5rem; background: none; }}
  .pj-logo {{ grid-column: 1 / -1; display: grid; place-items: center; border-radius: inherit; background: var(--background); border: 1px solid var(--border); }}
  .pj-mark {{ display: grid; place-items: center; inline-size: 4.5rem; block-size: 4.5rem; border-radius: 1.25rem; background: var(--mark); color: oklch(0.2 0 0); box-shadow: 0 6px 20px -6px color-mix(in oklab, var(--mark) 60%, transparent); }}
  .pj-mark svg {{ inline-size: 2.75rem; block-size: 2.75rem; }}
  .pj-mark-empty {{ inline-size: 4rem; block-size: 4rem; background: var(--muted); color: var(--foreground); box-shadow: none; }}
  .pj-mark-empty svg {{ inline-size: 1.75rem; block-size: 1.75rem; }}
  .pj-aa {{ position: relative; display: flex; flex-direction: column; justify-content: center; padding-inline: 1rem; border-radius: calc(var(--radius) - 2px); border: 1px solid var(--border); overflow: hidden; }}
  .pj-aa span {{ font-size: 3.25rem; line-height: 1; letter-spacing: -0.03em; }}
  .pj-aa small {{ font-size: 0.6875rem; opacity: 0.85; font-family: var(--font-sans); }}
  .pj-swatch {{ display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; border-radius: calc(var(--radius) - 2px); border: 1px solid var(--border); overflow: hidden; }}
  .pj-swatch span:first-child {{ grid-row: 1; }}
  .pj-swatch span:nth-child(2) {{ grid-row: 2; grid-column: 1; }}
  .pj-swatch span:nth-child(3) {{ grid-row: 1 / -1; grid-column: 2; }}
  .pj-mini {{ display: inline-grid; place-items: center; inline-size: 1.125rem; block-size: 1.125rem; border-radius: 0.3rem; background: var(--mark); color: oklch(0.2 0 0); flex-shrink: 0; }}
  .pj-mini svg {{ inline-size: 0.75rem; block-size: 0.75rem; }}
  .pj-letter {{ display: inline-grid; place-items: center; inline-size: 1.125rem; block-size: 1.125rem; border-radius: 0.3rem; font-size: 0.6875rem; font-weight: 600; background: var(--muted); color: var(--foreground); flex-shrink: 0; }}
  .pj-letter[data-tone="sage"] {{ background: oklch(0.85 0.05 140); color: oklch(0.35 0.05 140); }}
  .pj-letter[data-tone="ink"] {{ background: oklch(0.2 0 0); color: white; }}
  /* Site mockups */
  .pj-shot {{ display: flex; flex-direction: column; gap: 0.5rem; padding: 0.625rem 0.75rem; font-family: var(--font-sans); }}
  .pj-shot-nav {{ display: flex; align-items: center; gap: 0.375rem; }}
  .pj-shot-nav b {{ inline-size: 1.75rem; block-size: 0.3rem; border-radius: 1px; background: currentColor; opacity: 0.9; margin-inline-end: auto; }}
  .pj-shot-nav i {{ inline-size: 1.1rem; block-size: 0.2rem; background: currentColor; opacity: 0.45; }}
  .pj-shot-nav em {{ inline-size: 1.75rem; block-size: 0.5rem; border-radius: 1px; background: currentColor; opacity: 0.8; margin-inline-start: 0.25rem; }}
  .pj-shot p {{ margin: 0; }}
  .pj-shot-h {{ font-size: 1rem; line-height: 1.15; letter-spacing: -0.01em; max-inline-size: 15ch; }}
  .pj-shot .pj-shot-kicker {{ font-size: 0.5rem; letter-spacing: 0.1em; text-transform: uppercase; opacity: 0.6; text-align: center; margin-block-start: 0.75rem; }}
  .pj-shot-sub {{ font-size: 0.5625rem; opacity: 0.75; max-inline-size: 26ch; }}
  .pj-shot-dark {{ background: oklch(0.16 0 0); color: white; }}
  .pj-shot-dark .pj-shot-h {{ text-align: center; align-self: center; max-inline-size: none; font-size: 0.875rem; }}
  .pj-shot-rows {{ display: flex; flex-direction: column; gap: 0.375rem; align-self: center; inline-size: 60%; margin-block-start: 0.5rem; }}
  .pj-shot-rows i {{ block-size: 0.25rem; background: white; opacity: 0.25; }}
  .pj-shot-rows i:first-child {{ inline-size: 40%; opacity: 0.6; }}
  .pj-shot-stone {{ color: white; justify-content: flex-start; background: radial-gradient(circle at 75% 30%, oklch(0.55 0.05 60) 0, transparent 45%), linear-gradient(160deg, oklch(0.42 0.04 50), oklch(0.25 0.03 40)); }}
  .pj-shot.pj-shot-stone .pj-shot-h {{ margin-block-start: auto; font-weight: 300; }}
  .pj-shot-editorial {{ background: oklch(0.985 0.005 90); color: oklch(0.25 0.02 60); }}
  .pj-shot-editorial .pj-shot-h {{ font-family: Georgia, serif; font-size: 1.125rem; max-inline-size: 12ch; }}
  .pj-shot-photo {{ flex: 1; display: grid; grid-template-columns: 1fr 1fr; border-radius: 2px; overflow: hidden; }}
  .pj-shot-photo i:first-child {{ background: radial-gradient(circle at 60% 40%, oklch(0.62 0.08 50), oklch(0.42 0.07 45)); }}
  .pj-shot-photo i:last-child {{ background: radial-gradient(circle at 40% 40%, oklch(0.86 0.06 80), oklch(0.7 0.07 70)); }}
  .pj-shot-sky {{ position: relative; color: white; background: linear-gradient(to bottom, oklch(0.42 0.12 255), oklch(0.62 0.1 230) 55%, oklch(0.72 0.08 80) 56%, oklch(0.6 0.08 70)); }}
  .pj-shot.pj-shot-sky .pj-shot-h {{ font-family: var(--font-mono); font-size: 0.6875rem; text-transform: uppercase; letter-spacing: 0.04em; max-inline-size: 18ch; margin-block-start: 0.75rem; }}
  .pj-shot-runner {{ position: absolute; inset-block-start: 22%; inset-inline-end: 22%; inline-size: 0.9rem; block-size: 2.4rem; border-radius: 0.45rem 0.45rem 0.2rem 0.2rem; background: oklch(0.2 0.02 260); rotate: -18deg; }}
  /* What's new: a non-modal dialog pinned to the corner */
  .pj-news {{ position: fixed; inset: auto 1rem 1rem auto; margin: 0; inline-size: min(19rem, calc(100% - 2rem)); padding: 0.75rem; display: flex; flex-direction: column; align-items: flex-start; gap: 0.625rem; border: 1px solid var(--border); border-radius: calc(var(--radius) + 4px); background: var(--popover); color: var(--popover-foreground); box-shadow: 0 16px 40px -12px rgb(0 0 0 / 0.25); z-index: 20; }}
  .pj-news:not([open]) {{ display: none; }}
  .pj-news > header {{ display: flex; align-items: center; justify-content: space-between; align-self: stretch; }}
  .pj-news > header p {{ margin: 0; font-family: var(--font-mono); font-size: 0.6875rem; letter-spacing: 0.08em; text-transform: uppercase; color: {BRAND}; }}
  .pj-news-art {{ align-self: stretch; aspect-ratio: 16 / 9; display: grid; place-content: center; gap: 0.25rem; text-align: center; border-radius: var(--radius); color: oklch(0.25 0.05 40); background: radial-gradient(circle at 20% 80%, oklch(0.85 0.15 90), transparent 55%), radial-gradient(circle at 80% 20%, oklch(0.7 0.2 30), transparent 60%), linear-gradient(135deg, oklch(0.75 0.18 50), oklch(0.65 0.22 25)); }}
  .pj-news-art span {{ font-size: 0.75rem; font-weight: 500; }}
  .pj-news-art strong {{ font-size: 1.375rem; font-weight: 500; letter-spacing: -0.02em; line-height: 1.1; }}
  .pj-news h2 {{ margin: 0; font-size: 1rem; font-weight: 500; }}
  .pj-news .btn {{ align-self: stretch; }}
  @container (width < 40rem) {{ .pj-body {{ padding: 1.25rem 1rem 6rem; }} .pj-tabs a {{ padding-inline: 0.5rem; }} }}"""

page("projects-01", "Projects 01", body, CSS)

if __name__ == "__main__":
    register([{"id": "projects-01", "title": "Projects 01", "description": "A workspace of sites: project tiles with a style preview (logo, typeface, palette), a showcase of site mockups and a dismissible What’s new card, with no JavaScript of its own.", "category": "projects"}])
    print("wrote projects-01")

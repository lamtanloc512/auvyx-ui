"""studio-01: an image studio "Create" page. A hero with a prompt composer,
then Spotlight / Liked galleries.

Built only from existing foundation: the composer is a vertical .input-group
(selects in a <header>, a <textarea>, a toolbar <footer>), the galleries are
.carousel strips inside .tabs. Art is drawn with CSS gradients (no images).
"""
from common import page, register, icon, ic
import sidebar as sb

I = {
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "image": '<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>',
    "map-pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "arrow-up": '<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>',
    "heart": '<path d="M2 9.5a5.5 5.5 0 0 1 9.591-3.676a.56.56 0 0 0 .818 0A5.49 5.49 0 0 1 22 9.5c0 2.29-1.5 4-3 5.5l-5.492 5.313a2 2 0 0 1-3 .019L5 15c-1.5-1.5-3-3.2-3-5.5"/>',
    "house": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "smile": '<circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" x2="9.01" y1="9" y2="9"/><line x1="15" x2="15.01" y1="9" y2="9"/>',
    "square": '<rect width="18" height="18" x="3" y="3" rx="2"/>',
}


def si(name):
    return icon(I[name])


def item(label, icon_html, active=False, extra=""):
    cur = ' aria-current="page"' if active else ""
    return f'<li><a href="#"{cur} data-tooltip="{label}" data-side="right">{icon_html}<span>{label}</span>{extra}</a></li>'


NAV = (
    f'<header><ul><li><a href="#" data-size="lg">{sb.logo_mark("gallery")}<span><strong>Acme Studio</strong><small>Images</small></span></a></li></ul></header>'
    '<section>'
    f'<div role="group" aria-label="Studio"><ul>{item("Create", si("house"), active=True)}'
    f'{item("Library", ic("book"), extra=f"<span data-badge aria-label=\"Pro only\">{si("lock")}</span>")}</ul></div>'
    + sb.group("Brand", [item("Styles", si("image")), item("Characters", si("smile")), item("Scenes", si("map-pin"))])
    + sb.group("Tools", [item("Upscaler", ic("sparkles"))])
    + '<div class="sb-push" data-sidebar-hide-collapsed><div class="card st-upsell" data-size="sm">'
      f'<header>{si("lock")}<h2>Unlock Studio with Pro</h2><p>Make on-brand imagery and publish it to a live site in one workflow.</p></header>'
      f'<footer><button type="button" class="btn" data-size="sm">{ic("sparkles")}Upgrade to Pro</button></footer></div></div>'
    '</section>'
    f'<footer>{sb.nav_user()}</footer>'
)

TABS = [("Publish", "send", False), ("Export", "file", False), ("Studio", "sparkles", True), ("MCP", "terminal", False)]


def select(label, icon_html, options):
    opts = "".join(f"<option>{o}</option>" for o in options)
    return (f'<label class="st-pick">{icon_html}<span class="sr-only">{label}</span>'
            f'<select class="select" aria-label="{label}"><option value="">{label}</option>{opts}</select></label>')


composer = (
    '<form class="st-composer" onsubmit="event.preventDefault()" aria-label="Create an image">'
    '<div class="input-group" data-orientation="vertical">'
    '<header data-align="start">'
    + select("Style", si("image"), ["Sunlit editorial", "Soft pastel", "Bold graphic"])
    + select("Characters", si("smile"), ["Ava", "Theo", "Mina"])
    + select("Scene", si("map-pin"), ["Courtyard", "Studio backdrop", "Coastline"])
    + '</header>'
    '<textarea rows="3" aria-label="Prompt" placeholder="Describe what you are thinking or add references…"></textarea>'
    '<footer data-align="end">'
    f'<button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Add a reference image">{ic("plus")}</button>'
    f'<button type="button" class="btn st-chip" data-variant="ghost" data-size="sm">{ic("sparkles")}Image model 2</button>'
    f'<button type="button" class="btn st-chip" data-variant="ghost" data-size="sm" aria-label="Aspect ratio 1:1">{si("square")}1:1</button>'
    f'<button type="button" class="btn st-chip" data-variant="ghost" data-size="sm" aria-label="1 image">{si("image")}1</button>'
    f'<button type="button" class="btn st-chip" data-variant="ghost" data-size="sm" aria-label="Resolution 1K">1K</button>'
    f'<button type="submit" class="btn st-send" data-size="icon-sm" aria-label="Generate">{si("arrow-up")}</button>'
    '</footer></div></form>'
)

# Gallery art: CSS gradients standing in for generated images.
ART = [
    ("Speedster in citrus knit", "radial-gradient(circle at 70% 70%, oklch(0.86 0.17 95) 0 18%, transparent 19%), radial-gradient(circle at 35% 40%, oklch(0.55 0.12 40) 0 14%, transparent 15%), linear-gradient(160deg, oklch(0.5 0.2 262), oklch(0.62 0.17 245))"),
    ("Pastel boxer", "radial-gradient(circle at 50% 38%, oklch(0.93 0.03 60) 0 20%, transparent 21%), radial-gradient(circle at 50% 30%, oklch(0.97 0.01 90) 0 30%, transparent 31%), linear-gradient(180deg, oklch(0.85 0.08 340), oklch(0.75 0.12 350))"),
    ("Launch page on velvet", "linear-gradient(white, white) 50% 55% / 62% 50% no-repeat, linear-gradient(oklch(0.25 0 0), oklch(0.25 0 0)) 50% 52% / 66% 58% no-repeat, radial-gradient(circle, oklch(0.8 0.12 350) 0 2px, transparent 3px) 0 0 / 9px 9px, oklch(0.75 0.15 350)"),
    ("Red planet ascent", "radial-gradient(circle at 30% 60%, oklch(0.62 0.16 45) 0 34%, transparent 35%), radial-gradient(circle, white 0 1px, transparent 2px) 0 0 / 23px 19px, linear-gradient(180deg, oklch(0.25 0.05 260), oklch(0.4 0.08 230))"),
    ("Lagoon at noon", "radial-gradient(ellipse at 50% 100%, oklch(0.75 0.12 190) 0 40%, transparent 41%), linear-gradient(180deg, oklch(0.85 0.08 220), oklch(0.7 0.12 210))"),
    ("Citrus still life", "radial-gradient(circle at 35% 55%, oklch(0.8 0.17 70) 0 16%, transparent 17%), radial-gradient(circle at 62% 50%, oklch(0.72 0.19 40) 0 18%, transparent 19%), linear-gradient(180deg, oklch(0.94 0.03 90), oklch(0.86 0.05 80))"),
]


def gallery(label, items):
    slides = "".join(
        f'<li aria-roledescription="slide" aria-label="{i + 1} of {len(items)}"><figure class="st-art" style="background:{bg}"><figcaption>{t}</figcaption>'
        f'<button type="button" class="btn" data-variant="secondary" data-size="icon-sm" aria-label="Like {t}">{si("heart")}</button></figure></li>'
        for i, (t, bg) in enumerate(items))
    return f'<section class="carousel" data-items="4" aria-roledescription="carousel" aria-label="{label}"><ol>{slides}</ol></section>'


body = (
    sb.sidebar(NAV, attrs=' data-collapsible="icon"')
    + '<main class="st-main">'
    + f'<header class="app-header st-header">{sb.toggle_button()}<hr role="separator" aria-orientation="vertical"><h1>Create</h1>'
      '<nav class="st-tabs" aria-label="Workspace">'
      + "".join(f'<a href="#"{" aria-current=\"page\"" if on else ""}>{ic(i)}{t}</a>' for t, i, on in TABS)
      + '</nav><button type="button" class="btn" data-variant="outline" data-size="sm">Feedback</button></header>'
    + '<div class="st-body">'
      '<section class="st-hero" aria-labelledby="st-hero-title">'
      '<div class="st-scene" aria-hidden="true"><i class="st-sun"></i><i class="st-wall"></i><i class="st-door"></i><i class="st-bloom"></i><i class="st-bloom st-bloom-2"></i><i class="st-palm"></i></div>'
      '<h2 id="st-hero-title">Your brand, any image you can imagine</h2>'
      f'{composer}'
      '<p class="st-credit">Style · Sunlit Courtyard</p>'
      '</section>'
      '<div class="tabs st-gallery" id="st-gallery"><nav role="tablist" aria-orientation="horizontal" aria-label="Gallery">'
      '<button type="button" role="tab" id="st-t-1" aria-controls="st-p-1" aria-selected="true" tabindex="0">Spotlight</button>'
      '<button type="button" role="tab" id="st-t-2" aria-controls="st-p-2" aria-selected="false" tabindex="-1">Liked</button></nav>'
      f'<div role="tabpanel" id="st-p-1" aria-labelledby="st-t-1">{gallery("Spotlight", ART)}</div>'
      f'<div role="tabpanel" id="st-p-2" aria-labelledby="st-t-2" hidden>{gallery("Liked", ART[3:5])}</div></div>'
    + '</div></main>'
)

CSS = sb.SB_CSS + """
  .st-main { container-type: inline-size; min-inline-size: 0; }
  .st-header { block-size: 3.25rem; gap: 0.5rem; }
  .st-header h1 { margin: 0; font-size: 0.9375rem; font-weight: 500; }
  .st-tabs { margin-inline-start: auto; display: flex; align-self: stretch; gap: 0.25rem; overflow-x: auto; }
  .st-tabs a { display: inline-flex; align-items: center; gap: 0.5rem; padding-inline: 0.75rem; font-size: 0.875rem; font-weight: 500; color: var(--muted-foreground); text-decoration: none; border-block-end: 2px solid transparent; white-space: nowrap; }
  .st-tabs a svg { inline-size: 1rem; block-size: 1rem; }
  .st-tabs a:hover { color: var(--foreground); }
  .st-tabs a[aria-current="page"] { color: var(--foreground); border-color: var(--foreground); }
  .sidebar > nav li > a > [data-badge] svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .st-upsell { margin: 0.5rem; font-size: 0.8125rem; }
  .st-upsell > header { display: flex; flex-direction: column; align-items: flex-start; gap: 0.375rem; }
  .st-upsell > header svg { inline-size: 1rem; block-size: 1rem; }
  .st-upsell h2 { margin: 0; font-size: 0.875rem; font-weight: 500; }
  .st-upsell p { margin: 0; color: var(--muted-foreground); }
  .st-upsell .btn { inline-size: 100%; }
  .st-body { display: flex; flex-direction: column; gap: 1.5rem; padding: 1rem; }
  /* Hero: CSS-drawn scene behind the title and the composer */
  .st-hero { position: relative; isolation: isolate; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 1.25rem; min-block-size: min(40rem, 72dvh); padding: 4rem 1rem; border-radius: calc(var(--radius) * 2); overflow: hidden; }
  .st-scene { position: absolute; inset: 0; z-index: -1; background: linear-gradient(180deg, oklch(0.62 0.13 235), oklch(0.74 0.11 225) 60%, oklch(0.82 0.07 215)); }
  .st-scene i { position: absolute; display: block; }
  .st-sun { inset-block-start: 12%; inset-inline-end: 16%; inline-size: 7rem; block-size: 7rem; border-radius: 999px; background: radial-gradient(circle, oklch(0.97 0.08 95), oklch(0.9 0.12 85) 55%, transparent 70%); }
  .st-wall { inset-block-end: 0; inset-inline-start: 6%; inline-size: 46%; block-size: 58%; border-radius: 1rem 1rem 0 0; background: linear-gradient(180deg, oklch(0.93 0.03 70), oklch(0.86 0.04 60)); }
  .st-door { inset-block-end: 0; inset-inline-start: 18%; inline-size: 14%; block-size: 34%; border-radius: 0.5rem 0.5rem 0 0; background: linear-gradient(180deg, oklch(0.6 0.22 355), oklch(0.5 0.2 355)); }
  .st-bloom { inset-block-start: 26%; inset-inline-start: -4%; inline-size: 24%; block-size: 50%; border-radius: 45% 55% 50% 50%; background: radial-gradient(circle at 30% 30%, oklch(0.7 0.22 350) 0 6%, transparent 7%) 0 0 / 2.2rem 2.2rem, oklch(0.55 0.2 350 / 0.85); }
  .st-bloom-2 { inset-block-start: auto; inset-block-end: -6%; inset-inline-start: auto; inset-inline-end: -3%; inline-size: 30%; block-size: 36%; }
  .st-palm { inset-block-start: 30%; inset-inline-end: 6%; inline-size: 14%; block-size: 42%; border-radius: 50% 50% 0 0; background: radial-gradient(ellipse at 50% 0, oklch(0.55 0.14 145) 0 40%, transparent 41%), linear-gradient(oklch(0.5 0.06 60), oklch(0.5 0.06 60)) 50% 100% / 6% 60% no-repeat; }
  .st-hero h2 { margin: 0; max-inline-size: 30ch; text-align: center; font-size: clamp(1.5rem, 4cqi, 2.25rem); font-weight: 500; letter-spacing: -0.02em; color: white; text-shadow: 0 1px 12px rgb(0 0 0 / 0.25); }
  .st-composer { inline-size: min(100%, 44rem); }
  .st-composer .input-group { background: var(--background); box-shadow: 0 20px 50px -20px rgb(0 0 0 / 0.45); }
  .st-composer header { gap: 0.5rem; padding: 0.5rem 0.5rem 0; }
  .st-pick { position: relative; flex: 1; min-inline-size: 0; }
  .st-pick > svg { position: absolute; inset-inline-start: 0.625rem; inset-block-start: 50%; translate: 0 -50%; inline-size: 1rem; block-size: 1rem; color: var(--muted-foreground); pointer-events: none; }
  .st-pick .select { inline-size: 100%; padding-inline-start: 2rem; }
  .st-composer textarea { min-block-size: 5rem; padding: 0.75rem 0.875rem; }
  .st-composer footer { gap: 0.125rem; padding: 0.375rem 0.5rem 0.5rem; }
  .st-chip { gap: 0.375rem; padding-inline: 0.5rem; font-size: 0.75rem; color: var(--muted-foreground); }
  .st-chip svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .st-send { margin-inline-start: auto; border-radius: 0.5rem; }
  .st-credit { position: absolute; inset-block-end: 0.75rem; inset-inline-end: 0.75rem; margin: 0; padding: 0.25rem 0.625rem; border-radius: 999px; font-size: 0.75rem; color: white; background: rgb(0 0 0 / 0.3); backdrop-filter: blur(6px); }
  /* Galleries */
  .st-gallery { gap: 1rem; }
  .st-gallery > [role="tablist"] { align-self: flex-start; }
  .st-art { position: relative; margin: 0; aspect-ratio: 1; border-radius: var(--radius); overflow: hidden; background-color: var(--muted); }
  .st-art figcaption { position: absolute; inset: auto 0 0 0; padding: 2rem 0.75rem 0.625rem; font-size: 0.8125rem; color: white; background: linear-gradient(transparent, rgb(0 0 0 / 0.45)); opacity: 0; transition: opacity 0.2s; }
  .st-art .btn { position: absolute; inset-block-start: 0.5rem; inset-inline-end: 0.5rem; opacity: 0; transition: opacity 0.2s; }
  .st-art:is(:hover, :focus-within) :is(figcaption, .btn) { opacity: 1; }
  @container (width < 40rem) {
    .st-composer header { flex-wrap: wrap; }
    .st-pick { flex-basis: 100%; }
    .st-chip:nth-of-type(n+3) { display: none; }
  }
  @media (hover: none) { .st-art :is(figcaption, .btn) { opacity: 1; } }"""

page("studio-01", "Studio 01", body, CSS)

if __name__ == "__main__":
    register([{"id": "studio-01", "title": "Studio 01", "description": "An image studio Create page: a hero with a prompt composer (style, character and scene pickers, model and output options) and Spotlight / Liked galleries, built from Input Group, Tabs and Carousel.", "category": "studio"}])
    print("wrote studio-01")

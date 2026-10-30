"""Sidebar blocks (ports of shadcn sidebar-01..16)."""
import itertools
from common import page, register, ic, ICONS, icon

_ids = itertools.count(1)
uid = lambda p="s": f"{p}{next(_ids)}"

# ------------------------------------------------------------------ data
VERSIONS = ["1.0.1", "1.1.0-alpha", "2.0.0-beta1"]
DOCS = [
    ("Getting Started", ["Installation", "Project Structure"]),
    ("Building Your Application", ["Routing", "Data Fetching", "Rendering", "Caching", "Styling", "Optimizing", "Configuring", "Testing", "Authentication", "Deploying", "Upgrading", "Examples"]),
    ("API Reference", ["Components", "File Conventions", "Functions", "next.config.js Options", "CLI", "Edge Runtime"]),
    ("Architecture", ["Accessibility", "Fast Refresh", "Next.js Compiler", "Supported Browsers", "Turbopack"]),
    ("Community", ["Contribution Guide"]),
]
ACTIVE_DOC = "Data Fetching"
TEAMS = [("Acme Inc", "Enterprise", "gallery"), ("Acme Corp.", "Startup", "audio"), ("Evil Corp.", "Free", "command")]
NAV_MAIN = [
    ("Playground", "terminal", ["History", "Starred", "Settings"]),
    ("Models", "bot", ["Genesis", "Explorer", "Quantum"]),
    ("Documentation", "book", ["Introduction", "Get Started", "Tutorials", "Changelog"]),
    ("Settings", "settings-2", ["General", "Team", "Billing", "Limits"]),
]
PROJECTS = [("Design Engineering", "frame"), ("Sales & Marketing", "pie-chart"), ("Travel", "map")]
SECONDARY = [("Support", "life-buoy"), ("Feedback", "send")]
USER = ("shadcn", "m@example.com", "CN")

# ------------------------------------------------------------------ pieces
def a_item(label, icon_name=None, active=False, badge=None, tooltip=True, href="#", size=None):
    ico = ic(icon_name) if icon_name else ""
    cur = ' aria-current="page"' if active else ""
    tip = f' data-tooltip="{label}" data-side="right"' if tooltip and icon_name else ""
    sz = f' data-size="{size}"' if size else ""
    b = f'<span data-badge>{badge}</span>' if badge else ""
    return f'<li><a href="{href}"{cur}{tip}{sz}>{ico}<span>{label}</span>{b}</a></li>'


def collapsible_item(label, icon_name, subs, open_=False, active_sub=None):
    o = " open" if open_ else ""
    sub = "".join(f'<li><a href="#"{" aria-current=\"page\"" if s == active_sub else ""}><span>{s}</span></a></li>' for s in subs)
    return (f'<li><details{o}><summary data-tooltip="{label}" data-side="right">{ic(icon_name)}<span>{label}</span></summary>'
            f'<ul>{sub}</ul></details></li>')


def group(label, items, gid=None, extra=""):
    gid = gid or uid("g")
    head = f'<h3 id="{gid}">{label}</h3>' if label else ""
    lab = f' aria-labelledby="{gid}"' if label else ' aria-label="Navigation"'
    return f'<div role="group"{lab}{extra}>{head}<ul>{"".join(items)}</ul></div>'


def menu(items, pid, side="bottom", align="start", width="14rem", label="Menu"):
    return (f'<div id="{pid}" data-popover popover data-side="{side}" data-align="{align}" style="min-width:{width}">'
            f'<div role="menu" aria-label="{label}">{items}</div></div>')


def mi(label, icon_name=None, kbd=None, variant=None):
    v = f' data-variant="{variant}"' if variant else ""
    k = f"<kbd>{kbd}</kbd>" if kbd else ""
    return f'<button type="button" role="menuitem"{v}>{ic(icon_name) if icon_name else ""}<span>{label}</span>{k}</button>'


def logo_mark(icon_name="gallery"):
    return f'<span class="sb-mark">{ic(icon_name)}</span>'


def team_switcher():
    pid = uid("team")
    items = '<div role="heading">Teams</div>' + "".join(
        mi(n, None, f"⌘{i + 1}").replace('<span>', f'<span class="sb-mini">{ic(ico)}</span><span>', 1) for i, (n, _, ico) in enumerate(TEAMS)
    ) + '<hr role="separator">' + mi("Add team", "plus")
    return (f'<div class="dropdown-menu">'
            f'<button type="button" data-sidebar-item data-size="lg" popovertarget="{pid}" aria-haspopup="menu">'
            f'{logo_mark()}<span><strong>{TEAMS[0][0]}</strong><small>{TEAMS[0][1]}</small></span>{ic("chevrons-up-down")}</button>'
            f'{menu(items, pid, label="Teams")}</div>')


def version_switcher():
    pid = uid("ver")
    items = "".join(
        f'<button type="button" role="menuitemradio" aria-checked="{"true" if v == VERSIONS[0] else "false"}"><span>v{v}</span><span data-indicator>{ic("check")}</span></button>'
        for v in VERSIONS)
    return (f'<div class="dropdown-menu">'
            f'<button type="button" data-sidebar-item data-size="lg" popovertarget="{pid}" aria-haspopup="menu">'
            f'{logo_mark()}<span><strong>Documentation</strong><small>v{VERSIONS[0]}</small></span>{ic("chevrons-up-down")}</button>'
            f'{menu(items, pid, label="Version")}</div>')


def search_form():
    sid = uid("search")
    return (f'<form class="sb-search" role="search" onsubmit="event.preventDefault()" data-sidebar-hide-collapsed>'
            f'<label for="{sid}" class="sr-only">Search</label>'
            f'<div class="input-group"><input id="{sid}" type="search" placeholder="Search the docs..." aria-label="Search the docs">'
            f'<span data-align="inline-start">{ic("search")}</span></div></form>')


def nav_user(side="right", align="end"):
    pid = uid("user")
    name, email, ini = USER
    av = f'<span class="avatar" data-size="sm"><span>{ini}</span></span>'
    head = f'<div class="sb-user-head">{av}<span><strong>{name}</strong><small>{email}</small></span></div>'
    items = (head + '<hr role="separator">' + mi("Upgrade to Pro", "sparkles") + '<hr role="separator">'
             + mi("Account", "user") + mi("Billing", "credit-card") + mi("Notifications", "bell") + '<hr role="separator">' + mi("Log out", "log-out"))
    return (f'<div class="dropdown-menu">'
            f'<button type="button" data-sidebar-item data-size="lg" popovertarget="{pid}" aria-haspopup="menu">'
            f'{av}<span><strong>{name}</strong><small>{email}</small></span>{ic("chevrons-up-down")}</button>'
            f'{menu(items, pid, side=side, align=align, label="Account")}</div>')


def nav_main_collapsible(open_first=True):
    return group("Platform", [collapsible_item(t, i, subs, open_=open_first and n == 0) for n, (t, i, subs) in enumerate(NAV_MAIN)])


def nav_projects():
    items = [a_item(t, i) for t, i in PROJECTS] + [f'<li><a href="#" data-tooltip="More" data-side="right">{ic("more")}<span>More</span></a></li>']
    return group("Projects", items, extra=" data-sidebar-hide-collapsed")


def nav_secondary():
    return f'<div role="group" aria-label="Secondary" class="sb-push"><ul>{"".join(a_item(t, i, size="sm") for t, i in SECONDARY)}</ul></div>'


def docs_groups(collapsible=False):
    out = []
    for title, items in DOCS:
        lis = "".join(a_item(x, active=(x == ACTIVE_DOC)) for x in items)
        if collapsible:
            out.append(f'<div role="group" aria-label="{title}"><ul><li><details open><summary><span>{title}</span></summary><ul class="sb-flat">{lis}</ul></details></li></ul></div>')
        else:
            out.append(group(title, [a_item(x, active=(x == ACTIVE_DOC)) for x in items]))
    return "".join(out)


def docs_tree():
    """Always-open submenus (sidebar-03/04)."""
    lis = []
    for title, items in DOCS:
        sub = "".join(f'<li><a href="#"{" aria-current=\"page\"" if x == ACTIVE_DOC else ""}><span>{x}</span></a></li>' for x in items)
        lis.append(f'<li><a href="#" class="sb-strong"><span>{title}</span></a><ul>{sub}</ul></li>')
    return group(None, lis)


def toggle_button(target="app-sidebar"):
    return (f'<button type="button" class="btn" data-variant="ghost" data-size="icon-sm" data-sidebar-toggle="{target}" '
            f'aria-controls="{target}" aria-label="Toggle sidebar">{ic("panel-left")}</button>')


def breadcrumb(parent="Building Your Application", current="Data Fetching"):
    return (f'<nav class="breadcrumb sb-crumb" aria-label="Breadcrumb"><ol>'
            f'<li class="sb-hide-sm"><a href="#">{parent}</a></li>'
            f'<li aria-hidden="true" class="sb-hide-sm">{ic("chevron-right")}</li>'
            f'<li><span aria-current="page">{current}</span></li></ol></nav>')


def app_header(target="app-sidebar", crumb=None, right=""):
    return (f'<header class="app-header">{toggle_button(target)}<hr role="separator" aria-orientation="vertical">'
            f'{crumb if crumb is not None else breadcrumb()}{right}</header>')


def placeholder_body(rows=True):
    tiles = '<div class="app-tiles"><div class="app-tile"></div><div class="app-tile"></div><div class="app-tile"></div></div>' if rows else ""
    return f'<div class="app-body">{tiles}<div class="app-panel"></div></div>'


def sidebar(inner, id_="app-sidebar", attrs="", label="Sidebar"):
    return f'<aside id="{id_}" class="sidebar"{attrs}><nav aria-label="{label}">{inner}</nav></aside>'


SB_CSS = """
  body { min-block-size: 100svh; }
  .sb-mark { display: inline-flex; flex: none; align-items: center; justify-content: center; inline-size: 2rem; block-size: 2rem; border-radius: calc(var(--radius) + 2px); background: var(--sidebar-primary); color: var(--sidebar-primary-foreground); }
  .sb-mark svg { inline-size: 1rem; block-size: 1rem; }
  .sb-mini { display: inline-flex; align-items: center; justify-content: center; inline-size: 1.5rem; block-size: 1.5rem; border: 1px solid var(--border); border-radius: calc(var(--radius) - 2px); }
  .sb-mini svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .sb-user-head { display: flex; align-items: center; gap: 0.5rem; padding: 0.375rem 0.5rem; font-size: 0.875rem; }
  .sb-user-head > span:last-child { display: grid; line-height: 1.25; }
  .sb-user-head small { color: var(--muted-foreground); font-size: 0.75rem; }
  .sb-search .input-group { block-size: 2rem; background: var(--background); }
  .sb-push { margin-block-start: auto; }
  .sb-strong { font-weight: 500; }
  .sidebar > nav li > a.sb-strong + ul { display: flex; }
  .app-header { position: sticky; top: 0; z-index: 10; display: flex; align-items: center; gap: 0.5rem; block-size: 4rem; padding-inline: 1rem; border-block-end: 1px solid var(--border); background: var(--background); }
  .app-header > hr[aria-orientation='vertical'] { block-size: 1rem; margin-inline-end: 0.5rem; }
  .app-body { display: flex; flex-direction: column; gap: 1rem; padding: 1rem; }
  .app-tiles { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(min(100%, 12rem), 1fr)); }
  .app-tile { aspect-ratio: 16 / 9; border-radius: 0.75rem; background: color-mix(in oklch, var(--muted) 60%, transparent); }
  .app-panel { flex: 1; min-block-size: 60svh; border-radius: 0.75rem; background: color-mix(in oklch, var(--muted) 60%, transparent); }
  @media (width < 48rem) { .sb-hide-sm { display: none; } }
  .sidebar > nav > header .dropdown-menu, .sidebar > nav > footer .dropdown-menu { display: flex; inline-size: 100%; }
"""

blocks = []


def add(bid, title, desc, body, css="", scripts=""):
    page(bid, title, body, SB_CSS + css, scripts=scripts)
    blocks.append({"id": bid, "title": title, "description": desc, "category": "sidebar"})


# 01 simple grouped
add("sidebar-01", "Sidebar 01", "A simple sidebar with navigation grouped by section.",
    sidebar(f'<header>{version_switcher()}{search_form()}</header><section>{docs_groups()}</section>')
    + f'<main>{app_header()}{placeholder_body()}</main>')

# 02 collapsible sections
add("sidebar-02", "Sidebar 02", "A sidebar with collapsible sections.",
    sidebar(f'<header>{version_switcher()}{search_form()}</header><section>{docs_groups(collapsible=True)}</section>')
    + f'<main>{app_header()}{placeholder_body()}</main>',
    "\n  .sidebar > nav ul.sb-flat { border: 0; padding-inline: 0; }\n  .sidebar > nav details > summary > span { font-weight: 500; font-size: 0.75rem; color: color-mix(in oklch, var(--sidebar-foreground) 70%, transparent); }")

# 03 submenus
LOGO_ITEM = f'<ul><li><a href="#" data-size="lg">{logo_mark()}<span><strong>Documentation</strong><small>v{VERSIONS[0]}</small></span></a></li></ul>'
add("sidebar-03", "Sidebar 03", "A sidebar with submenus.",
    sidebar(f'<header>{LOGO_ITEM}</header><section>{docs_tree()}</section>')
    + f'<main>{app_header()}{placeholder_body()}</main>')

# 04 floating + submenus
add("sidebar-04", "Sidebar 04", "A floating sidebar with submenus.",
    sidebar(f'<header>{LOGO_ITEM}</header><section>{docs_tree()}</section>', attrs=' data-variant="floating"')
    + f'<main>{app_header()}{placeholder_body()}</main>',
    "\n  .sidebar > nav ul ul { border-inline-start: 0; padding-inline-start: 0.5rem; }")

# 05 collapsible submenus + search
def docs_collapsible():
    lis = []
    for n, (title, items) in enumerate(DOCS):
        sub = "".join(f'<li><a href="#"{" aria-current=\"page\"" if x == ACTIVE_DOC else ""}><span>{x}</span></a></li>' for x in items)
        o = " open" if n == 1 else ""
        lis.append(f'<li><details{o}><summary><span>{title}</span></summary><ul>{sub}</ul></details></li>')
    return group(None, lis)


add("sidebar-05", "Sidebar 05", "A sidebar with collapsible submenus.",
    sidebar(f'<header>{LOGO_ITEM}{search_form()}</header><section>{docs_collapsible()}</section>')
    + f'<main>{app_header()}{placeholder_body()}</main>')

# 06 submenus as dropdowns
def docs_dropdowns():
    lis = []
    for title, items in DOCS:
        pid = uid("dd")
        its = "".join(mi(x) for x in items)
        lis.append(f'<li><div class="dropdown-menu"><button type="button" data-sidebar-item popovertarget="{pid}" aria-haspopup="menu"><span>{title}</span>{ic("more")}</button>'
                   f'{menu(its, pid, side="right", align="start", width="12rem", label=title)}</div></li>')
    return group(None, lis)


OPT_IN = ('<footer><div class="card sb-optin" data-size="sm"><header><h2>Subscribe to our newsletter</h2>'
          '<p>Opt-in to receive updates and news about the sidebar.</p></header><section>'
          '<form class="stack" data-gap="2" onsubmit="event.preventDefault()"><label class="sr-only" for="sb6-email">Email</label>'
          '<input class="input" id="sb6-email" type="email" placeholder="Email"><button class="btn" data-size="sm">Subscribe</button></form></section></div></footer>')
add("sidebar-06", "Sidebar 06", "A sidebar with submenus shown as dropdowns.",
    sidebar(f'<header>{LOGO_ITEM}</header><section>{docs_dropdowns()}</section>{OPT_IN}')
    + f'<main>{app_header()}{placeholder_body()}</main>',
    "\n  .sidebar > nav li .dropdown-menu { display: flex; inline-size: 100%; }\n  .sb-optin { box-shadow: none; }\n  .sb-optin .input { block-size: 2rem; }")

# 07 collapses to icons
APP_NAV = f'<header>{team_switcher()}</header><section>{nav_main_collapsible()}{nav_projects()}</section><footer>{nav_user()}</footer>'
add("sidebar-07", "Sidebar 07", "A sidebar that collapses to icons.",
    sidebar(APP_NAV, attrs=' data-collapsible="icon"')
    + f'<main>{app_header(crumb=breadcrumb("Build Your Application", "Data Fetching"))}{placeholder_body()}</main>')

# 08 inset + secondary nav
INSET_NAV = (f'<header><ul><li><a href="#" data-size="lg">{logo_mark("command")}<span><strong>Acme Inc</strong><small>Enterprise</small></span></a></li></ul></header>'
             f'<section>{nav_main_collapsible()}{nav_projects()}{nav_secondary()}</section><footer>{nav_user()}</footer>')
add("sidebar-08", "Sidebar 08", "An inset sidebar with secondary navigation.",
    sidebar(INSET_NAV, attrs=' data-variant="inset"')
    + f'<main>{app_header(crumb=breadcrumb("Build Your Application", "Data Fetching"))}{placeholder_body()}</main>',
    "\n  .sidebar[data-variant='inset'] + main .app-header { border-block-end: 0; background: transparent; position: static; }")

# 09 collapsible nested sidebars (mail)
MAILS = [
    ("William Smith", "09:34 AM", "Meeting Tomorrow", "Hi team, just a reminder about our meeting tomorrow at 10 AM. Please come prepared with your project updates."),
    ("Alice Smith", "Yesterday", "Re: Project Update", "Thanks for the update. The progress looks great so far. Let's schedule a call to discuss the next steps."),
    ("Bob Johnson", "2 days ago", "Weekend Plans", "Hey everyone! I'm thinking of organizing a team outing this weekend. Would you be interested in a hiking trip or a beach day?"),
    ("Emily Davis", "2 days ago", "Re: Question about Budget", "I've reviewed the budget numbers you sent over. Can we set up a quick call to discuss some potential adjustments?"),
    ("Michael Wilson", "1 week ago", "Important Announcement", "Please join us for an all-hands meeting this Friday at 3 PM. We have some exciting news to share about the company's future."),
    ("Sarah Brown", "1 week ago", "Re: Feedback on Proposal", "Thank you for sending over the proposal. I've reviewed it and have some thoughts. Could we schedule a meeting to discuss my feedback?"),
]
mail_items = "".join(f'<a href="#" class="sb-mail"><span class="sb-mail-top"><strong>{n}</strong><small>{d}</small></span><span class="sb-mail-subj">{s}</span><span class="sb-mail-text">{t}</span></a>' for n, d, s, t in MAILS)
rail = (f'<div class="sb-rail"><header><ul><li><a href="#" data-size="lg" data-tooltip="Acme Inc" data-side="right">{logo_mark("command")}<span class="sr-only">Acme Inc</span></a></li></ul></header>'
        f'<section><div role="group" aria-label="Mailboxes"><ul>'
        + "".join(f'<li><a href="#"{" aria-current=\"page\"" if n == "Inbox" else ""} data-tooltip="{n}" data-side="right">{ic(i)}<span class="sr-only">{n}</span></a></li>'
                  for n, i in [("Inbox", "inbox"), ("Drafts", "file"), ("Sent", "send"), ("Junk", "bell"), ("Trash", "trash")])
        + f'</ul></div></section><footer>{nav_user(side="right", align="end").replace("<span><strong>", "<span class=\"sr-only\"><strong>", 1)}</footer></div>')
panel = (f'<div class="sb-panel"><header><div class="cluster" data-justify="between"><strong>Inbox</strong>'
         f'<label class="cluster sb-unread" data-gap="2"><span>Unreads</span><input type="checkbox" role="switch" class="input"></label></div>'
         f'<input class="input" type="search" placeholder="Type to search..." aria-label="Search mail"></header><section>{mail_items}</section></div>')
add("sidebar-09", "Sidebar 09", "Collapsible nested sidebars.",
    f'<aside id="app-sidebar" class="sidebar sb-nested"><nav aria-label="Mail">{rail}{panel}</nav></aside>'
    + f'<main>{app_header(crumb=breadcrumb("All Inboxes", "Inbox"))}<div class="app-body">'
    + "".join('<div class="app-mailrow"></div>' for _ in range(12)) + '</div></main>',
    """
  body { --sidebar-width: 22rem; } /* on body: main (a sibling of the aside) reads it for its margin */
  .sb-nested > nav { flex-direction: row; }
  .sb-rail { display: flex; flex-direction: column; inline-size: 3rem; flex: none; border-inline-end: 1px solid var(--sidebar-border); }
  .sb-rail > header, .sb-rail > footer { padding: 0.5rem; }
  .sb-rail > section { flex: 1; padding: 0.5rem; }
  .sb-rail ul { display: flex; flex-direction: column; gap: 0.25rem; margin: 0; padding: 0; list-style: none; }
  .sb-rail li > a { display: flex; align-items: center; justify-content: center; inline-size: 2rem; block-size: 2rem; padding: 0; }
  .sb-rail .dropdown-menu > button { inline-size: 2rem; block-size: 2rem; padding: 0; justify-content: center; }
  .sb-rail .dropdown-menu > button > svg:last-child { display: none; }
  .sb-panel { display: flex; flex-direction: column; flex: 1; min-inline-size: 0; background: var(--sidebar); }
  .sb-panel > header { display: flex; flex-direction: column; gap: 0.75rem; padding: 1rem; border-block-end: 1px solid var(--sidebar-border); }
  .sb-panel > section { flex: 1; overflow-y: auto; }
  .sb-unread { font-size: 0.875rem; }
  .sb-mail { display: flex; flex-direction: column; gap: 0.5rem; padding: 1rem; border-block-end: 1px solid var(--sidebar-border); color: inherit; text-decoration: none; font-size: 0.875rem; line-height: 1.3; }
  .sb-mail:hover { background: var(--sidebar-accent); }
  .sb-mail-top { display: flex; align-items: center; gap: 0.5rem; }
  .sb-mail-top small { margin-inline-start: auto; font-size: 0.75rem; color: var(--muted-foreground); }
  .sb-mail-subj { font-weight: 500; }
  .sb-mail-text { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; font-size: 0.75rem; color: var(--muted-foreground); }
  .app-mailrow { block-size: 3rem; border-radius: 0.5rem; background: color-mix(in oklch, var(--muted) 60%, transparent); }
""")

# 10 sidebar in a popover (Notion-like)
WORKSPACES = [("Personal Life Management", "🏠"), ("Professional Development", "💼"), ("Creative Projects", "🎨"), ("Home Management", "🏡"), ("Travel & Adventure", "🧳")]
FAVS = [("Project Management & Task Tracking", "📊"), ("Family Recipe Collection & Meal Planning", "🍳"), ("Fitness Tracker & Workout Routines", "💪"), ("Book Notes & Reading List", "📚")]
emoji_item = lambda t, e: f'<li><a href="#"><span class="sb-emoji">{e}</span><span>{t}</span></a></li>'
notion_nav = (f'<header>{team_switcher()}<ul class="sb-quick">' + a_item("Search", "search", tooltip=False) + a_item("Ask AI", "sparkles", tooltip=False)
              + a_item("Home", "home", active=True, tooltip=False) + a_item("Inbox", "inbox", badge="10", tooltip=False) + '</ul></header>'
              f'<section>{group("Favorites", [emoji_item(t, e) for t, e in FAVS])}{group("Workspaces", [emoji_item(t, e) for t, e in WORKSPACES])}'
              f'<div role="group" aria-label="Secondary" class="sb-push"><ul>{a_item("Calendar", "calendar", tooltip=False)}{a_item("Settings", "settings", tooltip=False)}{a_item("Trash", "trash", tooltip=False)}</ul></div></section>')
actions_pid = uid("actions")
actions = (f'<div class="cluster sb-actions" data-gap="2"><span class="sb-edit">Edit Oct 08</span>'
           f'<button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Star">{ic("star")}</button>'
           f'<div class="popover"><button type="button" class="btn" data-variant="ghost" data-size="icon-sm" popovertarget="{actions_pid}" aria-label="More actions">{ic("more")}</button>'
           f'<div id="{actions_pid}" data-popover popover data-side="bottom" data-align="end" class="sb-actions-pop">'
           f'<aside class="sidebar" data-position="static"><nav aria-label="Page actions"><section>'
           + group(None, [a_item("Customize Page", "settings-2", tooltip=False), a_item("Turn into wiki", "file", tooltip=False)])
           + group(None, [a_item("Copy Link", "send", tooltip=False), a_item("Duplicate", "plus", tooltip=False), a_item("Move to", "folder", tooltip=False), a_item("Move to Trash", "trash", tooltip=False)])
           + group(None, [a_item("Undo", "clock", tooltip=False), a_item("View analytics", "pie-chart", tooltip=False), a_item("Notifications", "bell", tooltip=False)])
           + '</section></nav></aside></div></div></div>')
add("sidebar-10", "Sidebar 10", "A sidebar in a popover.",
    sidebar(notion_nav, attrs=' data-variant="sidebar"')
    + f'<main><header class="app-header sb-plain">{toggle_button()}<hr role="separator" aria-orientation="vertical">'
    f'<span class="sb-title">Project Management &amp; Task Tracking</span>{actions}</header>'
    f'<div class="app-body sb-doc"><div class="app-tile sb-wide"></div><div class="app-panel"></div></div></main>',
    """
  .sb-emoji { inline-size: 1rem; text-align: center; }
  .sb-quick { display: flex; flex-direction: column; gap: 0.25rem; margin: 0; padding: 0; list-style: none; }
  .sb-plain { border-block-end: 0; }
  .sb-title { flex: 1; min-inline-size: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 0.875rem; }
  .sb-actions { margin-inline-start: auto; }
  .sb-edit { font-size: 0.875rem; color: var(--muted-foreground); }
  @media (width < 48rem) { .sb-edit { display: none; } }
  .sb-actions-pop { padding: 0 !important; overflow: hidden; }
  .sb-actions-pop .sidebar > nav { --sidebar-width: 14rem; border: 0; background: transparent; }
  .sb-doc { max-inline-size: 48rem; margin-inline: auto; inline-size: 100%; }
  .sb-wide { aspect-ratio: auto; block-size: 6rem; }
""")

# 11 file tree
TREE = [
    ("app", [("api", [("hello", ["route.ts"])]), "page.tsx", "layout.tsx", ("blog", ["page.tsx"])]),
    ("components", [("ui", ["button.tsx", "card.tsx"]), "header.tsx", "footer.tsx"]),
    ("lib", ["util.ts"]),
    ("public", ["favicon.ico", "vercel.svg"]),
    ".eslintrc.json", ".gitignore", "next.config.js", "tailwind.config.js", "package.json", "README.md",
]


def tree(nodes, depth=0):
    out = []
    for n in nodes:
        if isinstance(n, str):
            act = ' aria-current="page"' if n == "button.tsx" else ""
            out.append(f'<li><a href="#"{act}>{ic("file")}<span>{n}</span></a></li>')
        else:
            name, kids = n
            o = " open" if depth == 0 and name in ("app", "components") or name == "ui" else ""
            out.append(f'<li><details{o}><summary>{ic("chevron-right")}{ic("folder")}<span>{name}</span></summary><ul>{tree(kids, depth + 1)}</ul></details></li>')
    return "".join(out)


CHANGES = [("README.md", "M"), ("api/hello/route.ts", "U"), ("app/layout.tsx", "M")]
add("sidebar-11", "Sidebar 11", "A sidebar with a collapsible file tree.",
    sidebar(f'<section>{group("Changes", [a_item(f, "file", badge=s, tooltip=False) for f, s in CHANGES])}'
            f'<div role="group" aria-labelledby="files-h" class="sb-tree"><h3 id="files-h">Files</h3><ul>{tree(TREE)}</ul></div></section>')
    + f'<main>{app_header(crumb=breadcrumb("components", "button.tsx"))}{placeholder_body()}</main>',
    """
  .sb-tree details > summary::after { display: none; }
  .sb-tree details > summary > svg:first-child { transition: rotate 150ms; }
  .sb-tree details[open] > summary > svg:first-child { rotate: 90deg; }
  .sb-tree ul ul { border-inline-start: 0 !important; padding-inline-end: 0 !important; padding-inline-start: 0.75rem !important; }
""")

# 12 calendar
CALS = [("My Calendars", ["Personal", "Work", "Family"]), ("Favorites", ["Holidays", "Birthdays"]), ("Other", ["Travel", "Reminders", "Deadlines"])]
cal_groups = "".join(
    f'<div role="group" aria-label="{t}"><ul><li><details open><summary><span>{t}</span></summary><ul class="sb-checks">'
    + "".join(f'<li><label><input type="checkbox" class="input"{" checked" if i == 0 else ""}><span>{c}</span></label></li>' for i, c in enumerate(cs))
    + '</ul></details></li></ul></div>' for t, cs in CALS)
add("sidebar-12", "Sidebar 12", "A sidebar with a calendar.",
    sidebar(f'<header class="sb-cal-head">{nav_user(side="bottom", align="start")}</header>'
            f'<section><div class="sb-cal"><auvyx-calendar class="calendar" value="2026-11-14"></auvyx-calendar></div>'
            f'<hr role="separator">{cal_groups}</section>'
            f'<footer><ul>{a_item("New Calendar", "plus", tooltip=False)}</ul></footer>')
    + f'<main>{app_header(crumb=breadcrumb("Calendar", "November 2026"))}<div class="app-body"><div class="sb-month">'
    + "".join('<div class="sb-day"></div>' for _ in range(35)) + '</div></div></main>',
    """
  .sb-cal-head { block-size: 4rem; justify-content: center; border-block-end: 1px solid var(--sidebar-border); }
  .sb-cal { padding-inline: 0.25rem; }
  .sb-cal .calendar { --cell-size: 2.0625rem; padding: 0.5rem 0.25rem; }
  .sidebar > nav ul.sb-checks { border: 0; padding: 0; }
  .sb-checks label { display: flex; align-items: center; gap: 0.5rem; padding: 0.375rem 0.5rem; border-radius: calc(var(--radius) - 2px); font-size: 0.875rem; cursor: pointer; }
  .sb-checks label:hover { background: var(--sidebar-accent); }
  .sidebar > nav details > summary > span { font-weight: 500; }
  .sb-month { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 0.5rem; }
  .sb-day { aspect-ratio: 1; border-radius: 0.5rem; background: color-mix(in oklch, var(--muted) 60%, transparent); }
""")

# 13 sidebar in a dialog
SETTINGS = [("Notifications", "bell"), ("Navigation", "map"), ("Home", "home"), ("Appearance", "sparkles"), ("Messages & media", "inbox"),
            ("Language & region", "book"), ("Accessibility", "user"), ("Mark as read", "check"), ("Audio & video", "audio"),
            ("Connected accounts", "send"), ("Privacy & visibility", "settings-2"), ("Advanced", "settings")]
dlg_sidebar = (f'<aside class="sidebar sb-dlg-side" data-position="static"><nav aria-label="Settings"><section>'
               + group(None, [a_item(t, i, active=(t == "Messages & media"), tooltip=False) for t, i in SETTINGS]) + '</section></nav></aside>')
add("sidebar-13", "Sidebar 13", "A sidebar in a dialog.",
    f'<main class="cover"><button type="button" class="btn" commandfor="settings-dlg" command="show-modal">Open Dialog</button></main>'
    f'<dialog id="settings-dlg" class="dialog sb-dlg" closedby="any" aria-label="Settings"><div>'
    f'<div class="sb-dlg-grid">{dlg_sidebar}<div class="sb-dlg-main"><header class="sb-dlg-head">'
    f'<nav class="breadcrumb" aria-label="Breadcrumb"><ol><li class="sb-hide-sm"><a href="#">Settings</a></li><li aria-hidden="true" class="sb-hide-sm">{ic("chevron-right")}</li><li><span aria-current="page">Messages &amp; media</span></li></ol></nav>'
    f'<button type="button" class="btn" data-variant="ghost" data-size="icon-sm" commandfor="settings-dlg" command="close" aria-label="Close">{ic("x")}</button></header>'
    f'<div class="sb-dlg-body">' + "".join('<div class="sb-dlg-row"></div>' for _ in range(10)) + '</div></div></div></div></dialog>',
    """
  .cover > .btn { inline-size: auto; }
  .sb-dlg > div { max-inline-size: min(56rem, calc(100% - 2rem)) !important; padding: 0 !important; overflow: hidden; block-size: min(500px, calc(100svh - 2rem)); }
  .sb-dlg-grid { display: flex; block-size: 100%; }
  .sb-dlg-side { block-size: 100%; }
  .sb-dlg-side > nav { --sidebar-width: 14rem; }
  @media (width < 48rem) { .sb-dlg-side { display: none !important; } }
  .sb-dlg-main { flex: 1; min-inline-size: 0; display: flex; flex-direction: column; }
  .sb-dlg-head { display: flex; align-items: center; justify-content: space-between; block-size: 4rem; padding-inline: 1rem; flex: none; }
  .sb-dlg-body { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 1rem; padding: 0 1rem 1rem; }
  .sb-dlg-row { flex: none; aspect-ratio: 16 / 5; max-block-size: 8rem; border-radius: 0.75rem; background: color-mix(in oklch, var(--muted) 60%, transparent); }
""")

# 14 right side
add("sidebar-14", "Sidebar 14", "A sidebar on the right.",
    sidebar(f'<section>{group("Table of Contents", [a_item(x, active=(x == ACTIVE_DOC)) for x in DOCS[1][1]])}{group("API Reference", [a_item(x) for x in DOCS[2][1]])}</section>', attrs=' data-side="right"', label="On this page")
    + f'<main><header class="app-header">{breadcrumb()}<span class="sb-grow"></span>{toggle_button()}</header>{placeholder_body()}</main>',
    "\n  .sb-grow { flex: 1; }")

# 15 left + right
left = sidebar(notion_nav.replace(team_switcher.__name__, ""), id_="left-sidebar", label="Workspace")
right_nav = (f'<header class="sb-cal-head">{nav_user(side="bottom", align="end")}</header>'
             f'<section><div class="sb-cal"><auvyx-calendar class="calendar" value="2026-11-14"></auvyx-calendar></div><hr role="separator">{cal_groups}</section>'
             f'<footer><ul>{a_item("New Calendar", "plus", tooltip=False)}</ul></footer>')
right = sidebar(right_nav, id_="right-sidebar", attrs=' data-side="right"', label="Calendar")
add("sidebar-15", "Sidebar 15", "A left and a right sidebar.",
    left + right + f'<main><header class="app-header sb-plain">{toggle_button("left-sidebar")}<hr role="separator" aria-orientation="vertical">'
    f'<span class="sb-title">Project Management &amp; Task Tracking</span>{toggle_button("right-sidebar").replace("Toggle sidebar", "Toggle calendar")}</header>'
    f'<div class="app-body sb-doc"><div class="app-tile sb-wide"></div><div class="app-panel"></div></div></main>',
    """
  .sb-emoji { inline-size: 1rem; text-align: center; }
  .sb-quick { display: flex; flex-direction: column; gap: 0.25rem; margin: 0; padding: 0; list-style: none; }
  .sb-plain { border-block-end: 0; }
  .sb-title { flex: 1; min-inline-size: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 0.875rem; }
  .sb-doc { max-inline-size: 48rem; margin-inline: auto; inline-size: 100%; }
  .sb-wide { aspect-ratio: auto; block-size: 6rem; }
  .sb-cal-head { block-size: 4rem; justify-content: center; border-block-end: 1px solid var(--sidebar-border); }
  .sb-cal { padding-inline: 0.25rem; }
  .sb-cal .calendar { --cell-size: 2.0625rem; padding: 0.5rem 0.25rem; }
  .sidebar > nav ul.sb-checks { border: 0; padding: 0; }
  .sb-checks label { display: flex; align-items: center; gap: 0.5rem; padding: 0.375rem 0.5rem; border-radius: calc(var(--radius) - 2px); font-size: 0.875rem; cursor: pointer; }
  .sb-checks label:hover { background: var(--sidebar-accent); }
  .sidebar > nav details > summary > span { font-weight: 500; }
""")

# 16 sticky site header
site_header = (f'<header class="sb-site">{toggle_button()}<hr role="separator" aria-orientation="vertical">{breadcrumb("Build Your Application", "Data Fetching")}'
               f'<form class="sb-site-search" role="search" onsubmit="event.preventDefault()"><div class="input-group"><input type="search" placeholder="Search the docs..." aria-label="Search the docs"><span data-align="inline-start">{ic("search")}</span></div></form></header>')
add("sidebar-16", "Sidebar 16", "A sidebar with a sticky site header.",
    site_header + sidebar(INSET_NAV.replace(' data-size="lg"', ' data-size="lg"', 1)) + f'<main>{placeholder_body()}</main>',
    """
  body { --sidebar-top: 3.5rem; }
  .sb-site { position: sticky; top: 0; z-index: 60; display: flex; align-items: center; gap: 0.5rem; block-size: var(--sidebar-top); padding-inline: 1rem; border-block-end: 1px solid var(--border); background: var(--background); }
  .sb-site > hr[aria-orientation='vertical'] { block-size: 1rem; }
  .sb-site-search { margin-inline-start: auto; inline-size: 100%; max-inline-size: 16rem; }
  .sb-site-search .input-group { block-size: 2rem; }
  @media (width < 40rem) { .sb-site-search { display: none; } }
  .sidebar > nav { block-size: auto; bottom: 0; }
""")

register(blocks)
print(f"wrote {len(blocks)} sidebar blocks")

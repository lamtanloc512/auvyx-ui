"""CRM blocks: crm-01 (customers: grid table and kanban board views), crm-02 (customer record).

They showcase the foundation: .table[data-variant=grid] in <auvyx-data-table>,
.kanban in <auvyx-sortable> and .properties. JS beyond those modules only keeps
the two views in sync.
"""
from common import page, register, icon
import sidebar as sb  # app shell pieces (re-writes the sidebar blocks deterministically)

I = {
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "building": '<rect width="16" height="20" x="4" y="2" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/>',
    "map-pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "calendar": '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "plus": '<path d="M5 12h14"/><path d="M12 5v14"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "filter": '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>',
    "columns": '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M12 3v18"/>',
    "table": '<path d="M12 3v18"/><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M3 15h18"/>',
    "kanban": '<path d="M6 5v11"/><path d="M12 5v6"/><path d="M18 5v14"/>',
    "dollar": '<line x1="12" x2="12" y1="2" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    "flag": '<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" x2="4" y1="22" y2="15"/>',
    "message": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "note": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/>',
    "star": '<path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/>',
    "chevron-left": '<path d="m15 18-6-6 6-6"/>',
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
}


def ci(name):
    return icon(I[name])


STAGES = [("lead", "Lead"), ("qualified", "Qualified"), ("proposal", "Proposal"), ("won", "Won")]
OWNERS = {"ML": "Mara Lindqvist", "TA": "Theo Alvarez", "IM": "Inès Moreau", "RT": "Ren Takahashi"}
# id, company, domain, city, flag, owner, employees, arr, stage, hue
COMPANIES = [
    ("northwind", "Northwind Labs", "northwind.dev", "Berlin, Germany", "🇩🇪", "ML", "200–500", 12000, "lead", 250),
    ("bluefin", "Bluefin Systems", "bluefin.io", "Austin, USA", "🇺🇸", "TA", "50–200", 18500, "qualified", 210),
    ("kestrel", "Kestrel Foods", "kestrel.fr", "Lyon, France", "🇫🇷", "IM", "500–1,000", 47500, "proposal", 30),
    ("orchard", "Orchard Health", "orchard.jp", "Osaka, Japan", "🇯🇵", "RT", "1–50", 3400, "lead", 150),
    ("tidewater", "Tidewater Freight", "tidewater.nl", "Rotterdam, Netherlands", "🇳🇱", "ML", "200–500", 26000, "qualified", 190),
    ("copperline", "Copperline Energy", "copperline.ca", "Calgary, Canada", "🇨🇦", "TA", "1,000+", 84000, "won", 20),
    ("juniper", "Juniper Studio", "juniper.pt", "Lisbon, Portugal", "🇵🇹", "IM", "1–50", 2100, "lead", 320),
    ("halcyon", "Halcyon Bank", "halcyon.sg", "Singapore", "🇸🇬", "RT", "1,000+", 120000, "won", 270),
    ("ridgeway", "Ridgeway Outdoor", "ridgeway.co.nz", "Wellington, New Zealand", "🇳🇿", "ML", "50–200", 9800, "proposal", 100),
    ("lumen", "Lumen Analytics", "lumen.ai", "Toronto, Canada", "🇨🇦", "TA", "200–500", 36000, "qualified", 280),
    ("saffron", "Saffron Kitchens", "saffron.in", "Mumbai, India", "🇮🇳", "RT", "500–1,000", 15200, "lead", 50),
    ("vela", "Vela Mobility", "vela.es", "Madrid, Spain", "🇪🇸", "IM", "200–500", 41000, "proposal", 0),
]
STAGE_LABEL = dict(STAGES)


def money(n):
    return f"${n:,.0f}"


def logo(name, hue, size=""):
    return f'<span class="crm-logo{size}" style="--hue:{hue}" aria-hidden="true">{name[0]}</span>'


def owner(code):
    return f'<span class="crm-owner"><span class="avatar" data-size="xs"><span>{code}</span></span>{OWNERS[code]}</span>'


def stage_badge(stage):
    return f'<span class="badge crm-stage" data-variant="outline" data-stage="{stage}">{STAGE_LABEL[stage]}</span>'


NAV = (
    f'<header><ul><li><a href="#" data-size="lg">{sb.logo_mark("command")}<span><strong>Acme CRM</strong><small>Sales</small></span></a></li></ul></header>'
    '<section>'
    + '<div role="group" aria-label="Workspace"><ul>'
    + sb.a_item("Inbox", "inbox", badge="4") + sb.a_item("Customers", "user", active=True) + sb.a_item("Calendar", "calendar")
    + sb.a_item("Reports", "pie-chart") + '</ul></div>'
    + sb.group("Records", [sb.a_item("Contracts", "file"), sb.a_item("Projects", "folder"), sb.a_item("Agents", "bot")])
    + f'<div role="group" aria-label="Secondary" class="sb-push"><ul>{sb.a_item("Settings", "settings", size="sm")}{sb.a_item("Get Help", "life-buoy", size="sm")}</ul></div>'
    '</section>'
    f'<footer>{sb.nav_user()}</footer>'
)

SHELL_CSS = sb.SB_CSS + """
  .crm-main { container-type: inline-size; min-inline-size: 0; display: flex; flex-direction: column; }
  .sidebar[data-variant='inset'] + main .app-header { background: transparent; }
  .crm-header { block-size: 3rem; position: static; gap: 0.5rem; }
  .crm-header h1 { margin: 0; font-size: 1rem; font-weight: 500; }
  .crm-header .crm-push { margin-inline-start: auto; }
  .crm-logo { display: inline-grid; place-items: center; inline-size: 1.25rem; block-size: 1.25rem; flex-shrink: 0; border-radius: calc(var(--radius) - 4px); font-size: 0.6875rem; font-weight: 600; color: white; background: linear-gradient(135deg, oklch(0.72 0.14 var(--hue)), oklch(0.58 0.17 calc(var(--hue) + 40))); }
  .crm-logo-lg { display: inline-grid; place-items: center; inline-size: 3.5rem; block-size: 3.5rem; border-radius: var(--radius); font-size: 1.5rem; font-weight: 600; color: white; background: linear-gradient(135deg, oklch(0.72 0.14 var(--hue)), oklch(0.58 0.17 calc(var(--hue) + 40))); }
  .crm-owner { display: inline-flex; align-items: center; gap: 0.5rem; }
  .crm-owner .avatar { font-size: 0.625rem; }
  .crm-stage::before { content: ""; inline-size: 0.375rem; block-size: 0.375rem; border-radius: 999px; background: var(--stage, var(--muted-foreground)); }
  [data-stage="lead"] { --stage: oklch(0.7 0.02 260); }
  [data-stage="qualified"] { --stage: oklch(0.68 0.15 240); }
  [data-stage="proposal"] { --stage: oklch(0.75 0.15 75); }
  [data-stage="won"] { --stage: oklch(0.65 0.17 150); }
  .crm-num { text-align: end; font-variant-numeric: tabular-nums; }
  .crm-muted { color: var(--muted-foreground); }"""

# =================================================================== crm-01
th = lambda key, label, icon_name, sort=True, num=False: (
    f'<th data-key="{key}"' + (' aria-sort="none"' if sort else "") + (' data-type="number" class="crm-num"' if num else "") + ">"
    + (f'<button type="button">{ci(icon_name)}{label}</button>' if sort else f"{ci(icon_name)}{label}") + "</th>"
)

rows = "\n".join(
    f'<tr data-key="{cid}">'
    f'<td data-row-number></td>'
    f'<td><input class="input" type="checkbox" data-select aria-label="Select {name}"></td>'
    f'<td><a href="crm-02.html" class="crm-company">{logo(name, hue)}{name}</a></td>'
    f'<td data-value="{STAGE_LABEL[stage]}">{stage_badge(stage)}</td>'
    f'<td data-value="{OWNERS[o]}">{owner(o)}</td>'
    f'<td>{flag} {city}</td>'
    f'<td>{emp}</td>'
    f'<td class="crm-num" data-value="{arr}" data-editable>{money(arr)}</td>'
    f'<td><a href="#" class="crm-link">{ci("link")}{domain}</a></td>'
    f'</tr>'
    for cid, name, domain, city, flag, o, emp, arr, stage, hue in COMPANIES
)


def facet(key, label, values):
    opts = "".join(f'<label class="cluster" data-gap="2"><input class="input" type="checkbox" data-facet="{key}" value="{v}">{v}</label>' for v in values)
    return (f'<div class="dropdown-menu"><button type="button" class="btn" data-variant="outline" data-size="sm" popovertarget="crm-f-{key}">'
            f'{ci("filter")}{label}<span class="badge" data-variant="secondary" data-facet-count="{key}" hidden></span></button>'
            f'<div id="crm-f-{key}" data-popover popover data-align="start"><div class="stack crm-pop" data-gap="2">{opts}</div></div></div>')


COLS = [("owner", "Owner"), ("location", "Location"), ("employees", "Employees"), ("website", "Website")]

table = f"""<auvyx-data-table class="data-table crm-table" data-grid data-sticky>
  <header>
    <div class="input-group crm-search"><input type="search" data-filter placeholder="Search companies…" aria-label="Search companies"><span data-align="start" aria-hidden="true">{ci("search")}</span></div>
    {facet("stage", "Stage", [l for _, l in STAGES])}
    {facet("owner", "Owner", list(OWNERS.values()))}
    <button type="button" class="btn" data-variant="ghost" data-size="sm" data-reset hidden>Reset</button>
    <div class="dropdown-menu crm-push">
      <button type="button" class="btn" data-variant="outline" data-size="sm" popovertarget="crm-cols">{ci("columns")}Columns</button>
      <div id="crm-cols" data-popover popover data-align="end"><div class="stack crm-pop" data-gap="2">
        {"".join(f'<label class="cluster" data-gap="2"><input class="input" type="checkbox" data-column="{k}" checked>{l}</label>' for k, l in COLS)}
      </div></div>
    </div>
  </header>
  <div>
    <table class="table" data-variant="grid">
      <thead><tr>
        <th data-row-number><span class="sr-only">Row</span></th>
        <th><input class="input" type="checkbox" data-select-all aria-label="Select all companies"></th>
        {th("company", "Company", "building")}
        {th("stage", "Stage", "flag")}
        {th("owner", "Owner", "user")}
        {th("location", "Location", "map-pin")}
        {th("employees", "Employees", "users", sort=False)}
        {th("arr", "ARR", "dollar", num=True)}
        {th("website", "Website", "link", sort=False)}
      </tr></thead>
      <tbody>
{rows}
        <tr data-empty hidden><td colspan="9">No companies match.</td></tr>
      </tbody>
      <tfoot><tr>
        <td data-row-number></td><td></td>
        <td data-total-count>{len(COMPANIES)} companies</td><td></td><td></td><td></td><td></td>
        <td class="crm-num" data-total-arr>{money(sum(c[7] for c in COMPANIES))}</td><td></td>
      </tr></tfoot>
    </table>
  </div>
  <footer>
    <span data-selected-count data-template="{{selected}} of {{total}} selected"></span>
    <span class="crm-hint">Double-click ARR to edit · arrow keys move between cells</span>
  </footer>
</auvyx-data-table>"""


def card(c):
    cid, name, domain, city, flag, o, emp, arr, stage, hue = c
    return (f'<li data-key="{cid}"><span class="crm-card-head">{logo(name, hue)}<strong>{name}</strong></span>'
            f'<p>{flag} {city} · {emp}</p>'
            f'<footer><span class="avatar" data-size="xs" title="{OWNERS[o]}"><span>{o}</span></span><span class="crm-num" data-arr="{arr}">{money(arr)}</span></footer></li>')


board = '<auvyx-sortable class="kanban crm-board">' + "".join(
    f'<section aria-labelledby="crm-col-{s}" data-stage="{s}"><header><h3 id="crm-col-{s}">{label}</h3>'
    f'<span class="badge" data-variant="secondary" data-drag-count>{sum(1 for c in COMPANIES if c[8] == s)}</span>'
    f'<span class="crm-col-total" data-col-total>{money(sum(c[7] for c in COMPANIES if c[8] == s))}</span></header>'
    f'<ol>{"".join(card(c) for c in COMPANIES if c[8] == s)}</ol></section>'
    for s, label in STAGES) + "</auvyx-sortable>"

body01 = (
    sb.sidebar(NAV, attrs=' data-variant="inset" data-collapsible="icon"')
    + '<main class="crm-main">'
    + f'<header class="app-header crm-header">{sb.toggle_button()}<hr role="separator" aria-orientation="vertical"><h1>Customers</h1>'
      f'<button type="button" class="btn crm-push" data-size="sm">{ci("plus")}Add company</button></header>'
    + '<div class="tabs crm-views" id="crm-views"><nav role="tablist" aria-orientation="horizontal" aria-label="Views">'
      f'<button type="button" role="tab" id="crm-t-table" aria-controls="crm-p-table" aria-selected="true" tabindex="0">{ci("table")}Table</button>'
      f'<button type="button" role="tab" id="crm-t-board" aria-controls="crm-p-board" aria-selected="false" tabindex="-1">{ci("kanban")}Board</button></nav>'
      f'<div role="tabpanel" id="crm-p-table" aria-labelledby="crm-t-table">{table}</div>'
      f'<div role="tabpanel" id="crm-p-board" aria-labelledby="crm-t-board" hidden><p class="crm-hint crm-board-hint">Drag a card to change its stage, or focus it and press Space, then the arrow keys.</p>{board}</div>'
    + '</div></main>'
)

CSS01 = SHELL_CSS + """
  .crm-views { display: flex; flex-direction: column; gap: 0.75rem; padding: 0.75rem 1rem 1rem; min-block-size: 0; flex: 1; }
  .crm-views > [role='tablist'] { align-self: flex-start; }
  .crm-views [role='tab'] svg { inline-size: 1rem; block-size: 1rem; }
  .crm-table > header { gap: 0.5rem; }
  .crm-table .crm-push, .crm-header .crm-push { margin-inline-start: auto; }
  .crm-search { max-inline-size: 16rem; }
  .crm-table > header .btn svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .crm-table > div:has(> table) { max-block-size: max(20rem, calc(100dvh - 13rem)); border-radius: var(--radius); }
  .crm-pop { padding: 0.5rem; min-inline-size: 11rem; font-size: 0.875rem; }
  .crm-company { display: inline-flex; align-items: center; gap: 0.5rem; color: inherit; text-decoration: none; font-weight: 500; }
  .crm-company:hover { text-decoration: underline; text-underline-offset: 3px; }
  .crm-link { display: inline-flex; align-items: center; gap: 0.375rem; color: var(--muted-foreground); text-decoration: none; }
  .crm-link svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .crm-link:hover { color: var(--foreground); }
  .crm-hint { font-size: 0.75rem; color: var(--muted-foreground); }
  .crm-board-hint { margin: 0 0 0.75rem; }
  .crm-board { --kanban-column: 15rem; }
  .crm-board > section > header { flex-wrap: wrap; }
  .crm-board > section > header > h3::before { content: ""; display: inline-block; inline-size: 0.5rem; block-size: 0.5rem; margin-inline-end: 0.5rem; border-radius: 999px; background: var(--stage); }
  .crm-board .crm-col-total { margin-inline-start: auto; font-size: 0.75rem; font-variant-numeric: tabular-nums; }
  .crm-board > section > ol { min-block-size: 4rem; }
  .crm-card-head { display: flex; align-items: center; gap: 0.5rem; }
  .crm-board li > footer .avatar { font-size: 0.625rem; }"""

JS01 = """<script>
(() => {
  // Keep the two views in sync: a card dropped in a column moves that
  // company to the stage; an ARR edit updates the card and the totals.
  const table = document.querySelector('.crm-table');
  const board = document.querySelector('.crm-board');
  if (!table || !board) return;
  const fmt = (n) => '$' + Math.round(n).toLocaleString('en-US');
  const totals = () => {
    let sum = 0;
    table.querySelectorAll('tbody tr[data-key]').forEach((r) => { sum += +r.cells[7].dataset.value; });
    table.querySelector('[data-total-arr]').textContent = fmt(sum);
    board.querySelectorAll(':scope > section').forEach((col) => {
      let t = 0;
      col.querySelectorAll('[data-arr]').forEach((el) => { t += +el.dataset.arr; });
      col.querySelector('[data-col-total]').textContent = fmt(t);
    });
  };
  board.addEventListener('sort', (e) => {
    const col = e.detail.to.closest('section');
    const row = table.querySelector(`tr[data-key="${e.detail.item.dataset.key}"]`);
    const badge = row?.querySelector('[data-stage]');
    if (badge) {
      badge.dataset.stage = col.dataset.stage;
      badge.textContent = col.querySelector('h3').textContent;
      badge.parentElement.dataset.value = badge.textContent;
    }
    totals();
  });
  table.addEventListener('cellchange', (e) => {
    const value = parseFloat(String(e.detail.value).replace(/[^0-9.]/g, ''));
    e.preventDefault();
    if (Number.isNaN(value)) return;
    const cell = e.detail.row.cells[7];
    cell.dataset.value = String(value);
    cell.textContent = fmt(value);
    const arr = board.querySelector(`li[data-key="${e.detail.rowKey}"] [data-arr]`);
    if (arr) { arr.dataset.arr = String(value); arr.textContent = fmt(value); }
    totals();
  });
})();
</script>
"""

HEAD01 = ('<script src="../ui/dist/js/data-table.min.js" defer></script>\n'
          '<script src="../ui/dist/js/sortable.min.js" defer></script>\n')

page("crm-01", "CRM 01", body01, CSS01, scripts=JS01, head_extra=HEAD01)

# =================================================================== crm-02
cid, name, domain, city, flag, o, emp, arr, stage, hue = COMPANIES[2]  # Kestrel Foods

PROPS = [
    ("building", "Legal name", "Kestrel Foods SAS"),
    ("mail", "Email", '<a href="#">ines@kestrel.fr</a>'),
    ("link", "Website", f'<a href="#">{domain}</a>'),
    ("map-pin", "Location", f"{flag} {city}"),
    ("calendar", "Founded", "March 2014"),
    ("user", "Owner", owner(o)),
    ("users", "Employees", emp),
    ("flag", "Stage", stage_badge(stage)),
]
CUSTOM = [("Industry", "Food &amp; beverage"), ("Health score", "72 / 100"), ("Renewal risk", "Medium"), ("Source", "Referral")]


def props(items):
    return '<dl class="properties">' + "".join(f'<div><dt>{ci(i)}{l}</dt><dd>{v}</dd></div>' for i, l, v in items) + "</dl>"


STATS = [
    ("Response rate", "92%", "Very good", "Share of emails and calls answered within two days."),
    ("Annual value", money(arr), "Proposal", "Value of the proposal sent on Nov 4, billed yearly."),
    ("Invoices", "$12,480", "All paid", "Four invoices over the last year, none overdue."),
    ("Growth", "+12.4%", "Good", "Headcount change over the last quarter."),
]

ACTIVITY = [
    ("message", "Inès Moreau replied to the proposal", "Asked for a two-year term at the same price.", "2h ago"),
    ("note", "Note added by Theo Alvarez", "Procurement wants the security review before Dec 1.", "Yesterday"),
    ("mail", "Proposal sent", "Kestrel Foods · Annual plan · $47,500", "Nov 4"),
    ("calendar", "Discovery call", "45 min with Inès Moreau and their CFO.", "Oct 28"),
    ("star", "Moved to Proposal", "From Qualified, by Inès Moreau.", "Oct 28"),
]

CONTRACTS = [("C-2041", "Pilot", "Signed", "Feb 2025", "$6,000"), ("C-2187", "Annual plan", "Draft", "Dec 2025", "$47,500")]

stats_html = "".join(
    f'<div class="card crm-stat"><header><p>{t}</p><h3>{v}<span class="badge" data-variant="secondary">{b}</span></h3></header><section><p>{d}</p></section></div>'
    for t, v, b, d in STATS)
activity_html = '<ol class="crm-activity">' + "".join(
    f'<li><span class="crm-act-icon">{ci(i)}</span><div><p><strong>{t}</strong></p><p class="crm-muted">{d}</p></div><time>{w}</time></li>'
    for i, t, d, w in ACTIVITY) + "</ol>"
contracts_html = ('<div class="table-container"><table class="table" data-variant="grid"><thead><tr>'
                  f'<th>{ci("note")}Contract</th><th>{ci("flag")}Plan</th><th>Status</th><th>{ci("calendar")}Start</th><th class="crm-num">{ci("dollar")}Value</th></tr></thead><tbody>'
                  + "".join(f'<tr><td>{a}</td><td>{b}</td><td><span class="badge" data-variant="{"secondary" if s == "Draft" else "outline"}">{s}</span></td><td>{d}</td><td class="crm-num">{v}</td></tr>' for a, b, s, d, v in CONTRACTS)
                  + "</tbody></table></div>")

tabs02 = (
    '<div class="tabs crm-record-tabs" id="crm-rt"><nav role="tablist" aria-orientation="horizontal" aria-label="Record">'
    '<button type="button" role="tab" id="crm-rt-1" aria-controls="crm-rp-1" aria-selected="true" tabindex="0">Overview</button>'
    '<button type="button" role="tab" id="crm-rt-2" aria-controls="crm-rp-2" aria-selected="false" tabindex="-1">Activity <span class="badge" data-variant="secondary">5</span></button>'
    '<button type="button" role="tab" id="crm-rt-3" aria-controls="crm-rp-3" aria-selected="false" tabindex="-1">Contracts <span class="badge" data-variant="secondary">2</span></button></nav>'
    f'<div role="tabpanel" id="crm-rp-1" aria-labelledby="crm-rt-1"><div class="crm-stats">{stats_html}</div>'
    f'<section class="card"><header><h3>Recent activity</h3></header><section>{activity_html}</section></section></div>'
    f'<div role="tabpanel" id="crm-rp-2" aria-labelledby="crm-rt-2" hidden>{activity_html}</div>'
    f'<div role="tabpanel" id="crm-rp-3" aria-labelledby="crm-rt-3" hidden>{contracts_html}</div></div>'
)

body02 = (
    sb.sidebar(NAV, attrs=' data-variant="inset" data-collapsible="icon"')
    + '<main class="crm-main">'
    + f'<header class="app-header crm-header">{sb.toggle_button()}<hr role="separator" aria-orientation="vertical">'
      f'<nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="crm-01.html">Customers</a></li><li aria-hidden="true">{ci("chevron-right")}</li><li><span aria-current="page">{name}</span></li></ol></nav></header>'
    + '<div class="crm-record">'
    + '<aside class="crm-aside">'
      f'<div class="crm-ident">{logo(name, hue, "-lg")}<div><h1>{name}</h1><p class="crm-muted">{domain}</p></div></div>'
      f'<div class="cluster" data-gap="2"><button type="button" class="btn" data-variant="outline" data-size="sm">{ci("message")}Message</button>'
      f'<button type="button" class="btn" data-variant="outline" data-size="sm">{ci("mail")}Email</button>'
      f'<button type="button" class="btn" data-variant="outline" data-size="sm">{ci("plus")}Add note</button></div>'
      f'<section><h2>Details</h2>{props(PROPS)}</section>'
      f'<section><h2>Custom fields</h2>{props([("note", l, v) for l, v in CUSTOM])}</section>'
    + '</aside>'
    + f'<div class="crm-content">{tabs02}</div>'
    + '</div></main>'
)

CSS02 = SHELL_CSS + """
  .crm-header nav { min-inline-size: 0; }
  .crm-header .breadcrumb svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .crm-record { display: grid; grid-template-columns: minmax(18rem, 22rem) minmax(0, 1fr); flex: 1; min-block-size: 0; }
  .crm-aside { display: flex; flex-direction: column; gap: 1.25rem; padding: 1.25rem; border-inline-end: 1px solid var(--border); }
  .crm-ident { display: flex; align-items: center; gap: 0.875rem; }
  .crm-ident h1 { margin: 0; font-size: 1.25rem; font-weight: 600; }
  .crm-ident p { margin: 0.125rem 0 0; font-size: 0.875rem; }
  .crm-aside .btn svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .crm-aside h2 { margin: 0 0 0.375rem; font-size: 0.75rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted-foreground); }
  .crm-content { padding: 1rem 1.25rem 1.5rem; min-inline-size: 0; }
  .crm-record-tabs { gap: 1rem; }
  .crm-record-tabs [role='tab'] .badge { margin-inline-start: 0.25rem; }
  .crm-record-tabs [role='tabpanel'] { display: flex; flex-direction: column; gap: 1rem; }
  .crm-record-tabs [role='tabpanel'][hidden] { display: none; }
  .crm-stats { display: grid; gap: 0.75rem; grid-template-columns: repeat(auto-fit, minmax(min(100%, 10.5rem), 1fr)); }
  .crm-stat > header p { margin: 0; font-size: 0.8125rem; color: var(--muted-foreground); }
  .crm-stat > header h3 { margin: 0; display: flex; align-items: center; gap: 0.5rem; font-size: 1.625rem; font-weight: 500; font-variant-numeric: tabular-nums; letter-spacing: -0.01em; }
  .crm-stat > header h3 .badge { font-size: 0.6875rem; font-weight: 400; letter-spacing: 0; }
  .crm-stat > section p { margin: 0; font-size: 0.8125rem; color: var(--muted-foreground); }
  .crm-activity { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; }
  .crm-activity li { display: grid; grid-template-columns: auto minmax(0, 1fr) auto; gap: 0.75rem; padding-block: 0.75rem; border-block-end: 1px solid var(--border); font-size: 0.875rem; }
  .crm-activity li:last-child { border-block-end: 0; }
  .crm-activity p { margin: 0; }
  .crm-activity strong { font-weight: 500; }
  .crm-activity time { font-size: 0.75rem; color: var(--muted-foreground); white-space: nowrap; }
  .crm-act-icon { display: inline-grid; place-items: center; inline-size: 1.75rem; block-size: 1.75rem; border-radius: 999px; background: var(--muted); color: var(--muted-foreground); }
  .crm-act-icon svg { inline-size: 0.875rem; block-size: 0.875rem; }
  @container (width < 52rem) { .crm-record { grid-template-columns: 1fr; } .crm-aside { border-inline-end: 0; border-block-end: 1px solid var(--border); } }"""

page("crm-02", "CRM 02", body02, CSS02)

blocks = [
    {"id": "crm-01", "title": "CRM 01", "description": "Customers in two synced views: a spreadsheet-style data table (row numbers, stage and owner facets, editable ARR, grid keys) and a kanban board you drag cards across to change the stage.", "category": "crm"},
    {"id": "crm-02", "title": "CRM 02", "description": "A customer record: identity and actions, details and custom fields as a properties list, stat cards, an activity timeline and contracts in a grid table.", "category": "crm"},
]

if __name__ == "__main__":
    register(blocks)
    print("crm blocks:", ", ".join(b["id"] for b in blocks))

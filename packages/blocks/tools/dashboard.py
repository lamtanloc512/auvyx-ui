"""dashboard-01: sidebar + KPI cards + interactive area chart + data table."""
import json, math
from common import page, register, ic
import sidebar as sb  # reuses nav pieces (re-writes sidebar blocks deterministically)

CHART_HEAD = ('<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>\n'
              '<script src="../ui/dist/auvyx.chart.min.js" defer></script>\n')

DOC_NAV = [("Dashboard", "home", True), ("Lifecycle", "sparkles", False), ("Analytics", "pie-chart", False), ("Projects", "folder", False), ("Team", "user", False)]
DOCS = [("Data Library", "book"), ("Reports", "file"), ("Word Assistant", "bot")]

nav = (
    f'<header><ul><li><a href="#" data-size="lg">{sb.logo_mark("command")}<span><strong>Acme Inc.</strong></span></a></li></ul></header>'
    '<section>'
    f'<div role="group" aria-label="Quick create"><ul><li class="db-quick"><a href="#" class="db-create" data-tooltip="Quick Create" data-side="right">{ic("plus")}<span>Quick Create</span></a>'
    f'<button type="button" class="btn" data-variant="outline" data-size="icon-sm" aria-label="Inbox" data-sidebar-hide-collapsed>{ic("inbox")}</button></li>'
    + "".join(sb.a_item(t, i, active=a) for t, i, a in DOC_NAV) + '</ul></div>'
    + sb.group("Documents", [sb.a_item(t, i) for t, i in DOCS])
    + f'<div role="group" aria-label="Secondary" class="sb-push"><ul>{sb.a_item("Settings", "settings", size="sm")}{sb.a_item("Get Help", "life-buoy", size="sm")}{sb.a_item("Search", "search", size="sm")}</ul></div>'
    '</section>'
    f'<footer>{sb.nav_user()}</footer>'
)

KPIS = [
    ("Total Revenue", "$1,250.00", "+12.5%", "up", "Trending up this month", "Visitors for the last 6 months"),
    ("New Customers", "1,234", "-20%", "down", "Down 20% this period", "Acquisition needs attention"),
    ("Active Accounts", "45,678", "+12.5%", "up", "Strong user retention", "Engagement exceed targets"),
    ("Growth Rate", "4.5%", "+4.5%", "up", "Steady performance increase", "Meets growth projections"),
]
kpi_html = "".join(
    f'<div class="card db-kpi"><header><p>{t}</p><h2>{v}</h2><div class="card-action"><span class="badge" data-variant="outline">'
    f'{ic("trending-up" if d == "up" else "trending-down")}{c}</span></div></header>'
    f'<footer><p class="db-kpi-trend">{s1} {ic("trending-up" if d == "up" else "trending-down")}</p><p class="db-kpi-note">{s2}</p></footer></div>'
    for t, v, c, d, s1, s2 in KPIS)

# 91 days of visitors (deterministic)
days = []
for i in range(91):
    m, d = (4, i + 1) if i < 30 else (5, i - 29) if i < 61 else (6, i - 60)
    desktop = int(220 + 160 * math.sin(i / 6.0) + 90 * math.sin(i * 1.7) + 40 * math.cos(i * 0.9))
    mobile = int(180 + 120 * math.sin(i / 7.0 + 1) + 70 * math.cos(i * 1.3))
    days.append({"date": f"2024-{m:02d}-{d:02d}", "desktop": max(60, desktop), "mobile": max(50, mobile)})

ROWS = [
    ("Cover page", "Cover page", "In Process", 18, 5, "Eddie Lake"),
    ("Table of contents", "Table of contents", "Done", 29, 24, "Eddie Lake"),
    ("Executive summary", "Narrative", "Done", 10, 13, "Eddie Lake"),
    ("Technical approach", "Narrative", "Done", 27, 23, "Jamik Tashpulatov"),
    ("Design", "Narrative", "In Process", 2, 16, "Jamik Tashpulatov"),
    ("Capabilities", "Narrative", "In Process", 20, 8, "Jamik Tashpulatov"),
    ("Integration with existing systems", "Narrative", "In Process", 19, 21, "Jamik Tashpulatov"),
    ("Innovation and Advantages", "Narrative", "Done", 25, 26, "Assign reviewer"),
    ("Overview of EMR's Innovative Solutions", "Technical content", "Done", 7, 23, "Assign reviewer"),
    ("Advanced Algorithms and Machine Learning", "Narrative", "Done", 30, 28, "Assign reviewer"),
    ("Adaptive Communication Protocols", "Narrative", "Done", 9, 31, "Assign reviewer"),
    ("Advantages Over Current Technologies", "Narrative", "In Process", 12, 0, "Assign reviewer"),
    ("Past Performance", "Narrative", "Done", 22, 33, "Assign reviewer"),
    ("Customer Feedback and Satisfaction Levels", "Narrative", "Done", 15, 34, "Assign reviewer"),
]
def status(s):
    return (f'<span class="badge" data-variant="outline" class="db-status">{ic("check") if s == "Done" else ic("clock")}{s}</span>')

rows = "\n".join(
    f'<tr><td><input class="input" type="checkbox" data-select aria-label="Select {h}"></td><td><a href="#" class="db-link">{h}</a></td>'
    f'<td><span class="badge" data-variant="outline">{t}</span></td><td>{status(s)}</td>'
    f'<td data-value="{tg}" class="db-num">{tg}</td><td data-value="{lm}" class="db-num">{lm}</td>'
    f'<td>{r if r != "Assign reviewer" else "<span class=db-muted>Assign reviewer</span>"}</td></tr>'
    for h, t, s, tg, lm, r in ROWS)

table = f"""<auvyx-data-table class="data-table" data-page-size="10" id="docs-table">
  <header>
    <input class="input" type="search" data-filter placeholder="Filter sections..." aria-label="Filter sections">
  </header>
  <div><table class="table">
    <thead><tr>
      <th><input class="input" type="checkbox" data-select-all aria-label="Select all"></th>
      <th aria-sort="none"><button type="button">Header</button></th>
      <th aria-sort="none"><button type="button">Section Type</button></th>
      <th aria-sort="none"><button type="button">Status</button></th>
      <th aria-sort="none" data-type="number" class="db-num"><button type="button">Target</button></th>
      <th aria-sort="none" data-type="number" class="db-num"><button type="button">Limit</button></th>
      <th>Reviewer</th>
    </tr></thead>
    <tbody>
{rows}
      <tr data-empty hidden><td colspan="7">No results.</td></tr>
    </tbody>
  </table></div>
  <footer>
    <span data-selected-count data-template="{{selected}} of {{total}} row(s) selected."></span>
    <span data-page-status></span>
    <button type="button" class="btn" data-variant="outline" data-size="sm" data-page="prev">Previous</button>
    <button type="button" class="btn" data-variant="outline" data-size="sm" data-page="next">Next</button>
  </footer>
</auvyx-data-table>"""

body = (
    sb.sidebar(nav, attrs=' data-variant="inset" data-collapsible="icon"')
    + '<main class="db-main">'
    + f'<header class="app-header db-header">{sb.toggle_button()}<hr role="separator" aria-orientation="vertical"><h1 class="db-title">Documents</h1>'
      f'<a href="#" class="btn db-gh" data-variant="ghost" data-size="sm">GitHub</a></header>'
    + '<div class="db-body">'
    + f'<div class="db-kpis">{kpi_html}</div>'
    + '<div class="card db-chart"><header><h2>Total Visitors</h2><p><span class="db-wide">Total for the last 3 months</span><span class="db-narrow">Last 3 months</span></p>'
      '<div class="card-action"><fieldset class="toggle-group" data-variant="outline" id="range"><legend>Time range</legend>'
      '<label class="toggle"><input type="radio" name="range" value="90" checked>Last 3 months</label>'
      '<label class="toggle"><input type="radio" name="range" value="30">Last 30 days</label>'
      '<label class="toggle"><input type="radio" name="range" value="7">Last 7 days</label></fieldset></div></header>'
      '<section><div class="db-canvas"><canvas id="visitors" aria-label="Visitors by day"></canvas></div></section></div>'
    + '<div class="tabs db-tabs" id="db-tabs"><nav role="tablist" aria-orientation="horizontal">'
      '<button type="button" role="tab" id="t-outline" aria-controls="p-outline" aria-selected="true" tabindex="0">Outline</button>'
      '<button type="button" role="tab" id="t-perf" aria-controls="p-perf" aria-selected="false" tabindex="-1">Past Performance <span class="badge" data-variant="secondary">3</span></button>'
      '<button type="button" role="tab" id="t-people" aria-controls="p-people" aria-selected="false" tabindex="-1">Key Personnel <span class="badge" data-variant="secondary">2</span></button>'
      '<button type="button" role="tab" id="t-focus" aria-controls="p-focus" aria-selected="false" tabindex="-1">Focus Documents</button></nav>'
      f'<button type="button" class="btn db-add" data-variant="outline" data-size="sm">{ic("plus")}<span class="db-wide">Add Section</span></button>'
      f'<div role="tabpanel" id="p-outline" aria-labelledby="t-outline">{table}</div>'
      + "".join(f'<div role="tabpanel" id="p-{k}" aria-labelledby="t-{k}" hidden><div class="db-empty"></div></div>' for k in ("perf", "people", "focus"))
    + '</div></div></main>'
)

CSS = sb.SB_CSS + """
  .db-main { container-type: inline-size; }
  .sidebar[data-variant='inset'] + main .app-header { background: transparent; }
  .db-header { block-size: 3rem; position: static; }
  .db-title { margin: 0; font-size: 1rem; font-weight: 500; }
  .db-gh { margin-inline-start: auto; }
  .db-body { display: flex; flex-direction: column; gap: 1rem; padding: 1rem; }
  @media (width >= 48rem) { .db-body { gap: 1.5rem; padding: 1.5rem; } }
  .db-kpis { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(min(100%, 15rem), 1fr)); }
  .db-kpi { background: linear-gradient(to top, color-mix(in oklch, var(--primary) 5%, var(--card)), var(--card)); }
  .db-kpi > header > p { margin: 0; font-size: 0.875rem; color: var(--muted-foreground); }
  .db-kpi > header > h2 { margin: 0; font-size: 1.5rem; font-weight: 600; font-variant-numeric: tabular-nums; }
  @container (width >= 40rem) { .db-kpi > header > h2 { font-size: 1.875rem; } }
  .db-kpi .badge svg { inline-size: 0.75rem; block-size: 0.75rem; }
  .db-kpi > footer { flex-direction: column; align-items: flex-start; gap: 0.375rem; font-size: 0.875rem; }
  .db-kpi-trend { margin: 0; display: flex; align-items: center; gap: 0.5rem; font-weight: 500; }
  .db-kpi-trend svg { inline-size: 1rem; block-size: 1rem; }
  .db-kpi-note { margin: 0; color: var(--muted-foreground); }
  .db-canvas { block-size: 250px; }
  .db-canvas .chart { aspect-ratio: auto; block-size: 100%; }
  .db-narrow { display: none; }
  @container (width < 40rem) { .db-wide { display: none; } .db-narrow { display: inline; } .db-chart > header { grid-template-columns: 1fr; } .db-chart .card-action { grid-column: 1; grid-row: auto; justify-self: start; } }
  .db-chart .toggle-group .toggle { font-size: 0.8125rem; }
  .db-tabs { display: grid; grid-template-columns: minmax(0, 1fr) auto; align-items: center; gap: 1rem; }
  .db-tabs > [role='tablist'] { grid-column: 1; justify-self: start; max-inline-size: 100%; overflow-x: auto; }
  .db-tabs > .db-add { grid-column: 2; grid-row: 1; }
  .db-tabs > [role='tabpanel'] { grid-column: 1 / -1; }
  @container (width < 48rem) { .db-tabs > [role='tablist'] > :nth-child(n+3) { display: none; } }
  .db-tabs [role='tab'] .badge { margin-inline-start: 0.25rem; }
  .db-link { color: inherit; text-decoration: none; font-weight: 500; }
  .db-link:hover { text-decoration: underline; }
  .db-muted { color: var(--muted-foreground); }
  .db-num { text-align: end; }
  .db-tabs .badge svg { inline-size: 0.75rem; block-size: 0.75rem; }
  .db-empty { aspect-ratio: 16 / 6; border: 1px dashed var(--border); border-radius: 0.75rem; }
  .db-quick { display: flex; align-items: center; gap: 0.5rem; }
  .sidebar > nav li > a.db-create { flex: 1; background: var(--primary); color: var(--primary-foreground); }
  .sidebar > nav li > a.db-create:hover { background: color-mix(in oklch, var(--primary) 90%, transparent); color: var(--primary-foreground); }
"""

SCRIPT = f"""<script>
const DATA = {json.dumps(days)};
function draw() {{
  const n = +document.querySelector('[name=range]:checked').value;
  const rows = DATA.slice(-n).map(d => ({{ ...d, label: new Date(d.date + 'T00:00').toLocaleDateString(undefined, {{ month: 'short', day: 'numeric' }}) }}));
  window.basecoat.chart('#visitors', {{
    type: 'line', labelKey: 'label', data: rows, legend: false,
    series: {{
      mobile: {{ label: 'Mobile', color: 'var(--chart-1)', surface: 'gradient', dataset: {{ fill: 'origin', tension: 0.35, pointRadius: 0, borderWidth: 1.5 }} }},
      desktop: {{ label: 'Desktop', color: 'var(--chart-2)', surface: 'gradient', dataset: {{ fill: 'origin', tension: 0.35, pointRadius: 0, borderWidth: 1.5 }} }},
    }},
    options: {{ scales: {{ x: {{ ticks: {{ maxTicksLimit: 8, autoSkip: true }} }}, y: {{ stacked: true }} }} }},
  }});
}}
document.getElementById('range').addEventListener('change', draw);
window.addEventListener('DOMContentLoaded', () => window.Chart && window.basecoat?.chart ? draw() : window.addEventListener('load', draw, {{ once: true }}));
</script>
"""

page("dashboard-01", "Dashboard 01", body, CSS, scripts=SCRIPT, head_extra=CHART_HEAD)
register([{"id": "dashboard-01", "title": "Dashboard 01", "description": "A dashboard with sidebar, charts and data table.", "category": "dashboard"}])
print("wrote dashboard-01")

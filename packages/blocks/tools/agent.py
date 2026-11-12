"""Agent blocks: agent-01 (context window panel), agent-02 (agent runs table)."""
import json
from common import page, register, icon

I = {
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "sliders": '<path d="M20 7h-9"/><path d="M14 17H5"/><circle cx="17" cy="17" r="3"/><circle cx="7" cy="7" r="3"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "more-v": '<circle cx="12" cy="12" r="1"/><circle cx="12" cy="5" r="1"/><circle cx="12" cy="19" r="1"/>',
    "minimize": '<path d="m14 10 7-7"/><path d="M20 10h-6V4"/><path d="m3 21 7-7"/><path d="M4 14h6v6"/>',
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "chevrons-left": '<path d="m11 17-5-5 5-5"/><path d="m18 17-5-5 5-5"/>',
    "chevrons-right": '<path d="m6 17 5-5-5-5"/><path d="m13 17 5-5-5-5"/>',
    "chevron-left": '<path d="m15 18-6-6 6-6"/>',
    "columns": '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M12 3v18"/>',
    "filter": '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>',
    "rotate": '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/>',
    "brain": '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/>',
    "message": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "x-circle": '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/>',
    "check-circle": '<path d="M21.801 10A10 10 0 1 1 17 3.335"/><path d="m9 11 3 3L22 4"/>',
    "loader": '<path d="M21 12a9 9 0 1 1-6.219-8.56"/>',
}


def ai(name, **kw):
    return icon(I[name], **kw)


blocks = []

# =================================================================== agent-01
WINDOW = 200_000
CELLS = 400  # 500 tokens per cell
CATS = [
    ("system", "System", 3_200),
    ("tools", "Tools", 11_900),
    ("memory", "Memory", 8_500),
    ("docs", "Docs", 52_200),
    ("history", "History", 69_800),
]
DOCS = [
    ("ledger-v3/schema.sql", "SQL · pinned", 18_400),
    ("MIGRATION_PLAN.md", "Markdown", 12_900),
    ("ledger/accounts.ts", "TypeScript", 9_800),
    ("ledger/postings.ts", "TypeScript", 6_700),
    ("runbooks/backfill.md", "Markdown", 4_400),
]
MEMORY = [
    ("Prefers additive migrations", "Preference · critical", 2_600),
    ("Ledger amounts are integer minor units", "Decision · high", 2_100),
    ("Staging DB is read-only on Fridays", "Constraint · high", 1_900),
    ("Backfill batch size 5,000 rows", "Decision · medium", 1_900),
]
TURNS = [
    ("Turn 47 · Ran migration dry-run", "Tool output · 312 rows", 8_900),
    ("Turn 31 · Read schema diff", "Tool output", 7_400),
    ("Turn 12 · Drafted backfill plan", "Assistant", 5_200),
    ("Turn 50 · Review posting constraints", "User + assistant", 3_100),
    ("44 other turns", "Mixed", 45_200),
]
HISTORY_TURNS = 50


def fmt(n):
    return f"{n / 1000:.1f}K"


def waffle_counts(values, cells, total):
    """Largest-remainder rounding so the cells add up exactly."""
    raw = [v / total * cells for v in values]
    counts = [int(r) for r in raw]
    for i in sorted(range(len(raw)), key=lambda i: raw[i] - counts[i], reverse=True)[: cells - sum(counts)]:
        counts[i] += 1
    return counts


def waffle(cats):
    used = sum(v for _, _, v in cats)
    counts = waffle_counts([v for _, _, v in cats] + [WINDOW - used], CELLS, WINDOW)
    keys = [k for k, _, _ in cats] + ["free"]
    cells = []
    for k, c in zip(keys, counts):
        cells += [k] * c
    return "".join(f'<i data-k="{k}" style="--i:{i}"></i>' for i, k in enumerate(cells))


def legend(cats):
    used = sum(v for _, _, v in cats)
    items = cats + [("free", "Free", WINDOW - used)]
    return "".join(
        f'<li data-k="{k}"><span class="agx-key"><i></i>{label}</span>'
        f'<span class="agx-val"><strong data-val="{k}">{fmt(v)}</strong> <small data-pct="{k}">{round(v / WINDOW * 100)}%</small></span></li>'
        for k, label, v in items
    )


def rows(items, kind):
    top = max(v for *_, v in items)
    glyph = {"docs": "file", "memory": "brain", "history": "message"}[kind]
    return "".join(
        f'<li><span class="agx-row-icon">{ai(glyph)}</span>'
        f'<span class="agx-row-main"><span class="agx-row-title">{t}</span><span class="agx-mono">{m}</span></span>'
        f'<span class="agx-row-size"><span class="agx-mono">{fmt(v)}</span><span class="agx-bar" data-k="{kind}"><span style="inline-size:{v / top * 100:.0f}%"></span></span></span></li>'
        for t, m, v in items
    )


used = sum(v for *_, v in CATS)
hist = dict((k, v) for k, _, v in CATS)["history"]
per_turn = hist / HISTORY_TURNS
headroom = round((WINDOW - used) / per_turn / 10) * 10
pct_used = round(used / WINDOW * 100)

AGENT_CSS = """
  body { background: var(--muted); }
  .agx-stage { min-block-size: 100dvh; display: grid; place-items: center; padding: 2rem 1rem; }
  .agx-panel { --agx-system: oklch(0.78 0.11 300); --agx-tools: oklch(0.72 0.17 150); --agx-memory: oklch(0.74 0.12 220); --agx-docs: oklch(0.78 0.15 75); --agx-history: oklch(0.55 0.21 280); --agx-free: color-mix(in oklab, var(--muted-foreground) 14%, transparent); inline-size: 100%; max-inline-size: 42rem; display: flex; flex-direction: column; gap: 0.5rem; padding: 0.5rem; border: 1px solid var(--border); border-radius: calc(var(--radius) * 2.5); background: color-mix(in oklab, var(--muted) 60%, var(--background)); box-shadow: 0 1px 2px rgb(0 0 0 / 0.04), 0 12px 32px -12px rgb(0 0 0 / 0.12); }
  .dark .agx-panel { --agx-history: oklch(0.62 0.2 280); }
  .agx-head { display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 0.5rem 0.25rem 1rem; }
  .agx-head h1 { margin: 0; font-size: 1.0625rem; font-weight: 500; }
  .agx-head .agx-info { color: var(--muted-foreground); display: inline-flex; }
  .agx-head .agx-info svg { inline-size: 1rem; block-size: 1rem; }
  .agx-push { margin-inline-start: auto; }
  .agx-live { display: inline-flex; align-items: center; gap: 0.375rem; padding: 0.25rem 0.625rem; border-radius: 999px; font-size: 0.8125rem; font-weight: 500; color: oklch(0.55 0.15 150); background: oklch(0.72 0.17 150 / 0.12); }
  .agx-live::before { content: ""; inline-size: 0.5rem; block-size: 0.5rem; border-radius: 999px; background: currentColor; animation: agx-pulse 2s ease-in-out infinite; }
  @keyframes agx-pulse { 50% { opacity: 0.35; } }
  .agx-sheet { border: 1px solid var(--border); border-radius: calc(var(--radius) * 2); background: var(--card); color: var(--card-foreground); padding: 1.25rem; }
  .agx-mono { font-family: var(--font-mono); font-size: 0.75rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted-foreground); }
  .agx-stats { display: grid; grid-template-columns: 1.4fr 1fr; gap: 1.25rem; }
  .agx-stats > section + section { border-inline-start: 1px dashed var(--border); padding-inline-start: 1.25rem; }
  .agx-label { display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; }
  .agx-label > span:first-child { display: inline-flex; align-items: center; gap: 0.5rem; }
  .agx-health { font-family: var(--font-mono); font-size: 0.6875rem; letter-spacing: 0.08em; text-transform: uppercase; padding: 0.125rem 0.5rem; border-radius: 999px; color: oklch(0.55 0.15 150); background: oklch(0.72 0.17 150 / 0.12); }
  .agx-health[data-level="warn"] { color: oklch(0.6 0.15 65); background: oklch(0.78 0.15 75 / 0.16); }
  .agx-health[data-level="critical"] { color: var(--destructive); background: color-mix(in oklab, var(--destructive) 12%, transparent); }
  .agx-big { margin: 0.5rem 0 0.25rem; display: flex; align-items: baseline; gap: 0.5rem; flex-wrap: wrap; }
  .agx-big strong { font-size: clamp(2.25rem, 7vw, 3.25rem); font-weight: 500; letter-spacing: -0.03em; line-height: 1; font-variant-numeric: tabular-nums; }
  .agx-big span { color: var(--muted-foreground); }
  .agx-saved { margin: 0.5rem 0 0.75rem; font-size: 1.5rem; font-weight: 500; font-variant-numeric: tabular-nums; }
  .agx-saved small { font-size: 0.9375rem; font-weight: 400; color: var(--muted-foreground); }
  .agx-stats .progress { margin-block-end: 0.75rem; }
  .agx-waffle { display: grid; grid-template-columns: repeat(50, minmax(0, 1fr)); gap: 3px; margin-block: 1.5rem 1.25rem; }
  .agx-waffle i { aspect-ratio: 1; border-radius: 2px; background: var(--agx-free); transition: background-color 0.4s ease, opacity 0.2s ease; transition-delay: calc(var(--i) * 1.5ms), 0s; }
  .agx-waffle i[data-k="system"], .agx-legend [data-k="system"] i { background: var(--agx-system); }
  .agx-waffle i[data-k="tools"], .agx-legend [data-k="tools"] i { background: var(--agx-tools); }
  .agx-waffle i[data-k="memory"], .agx-legend [data-k="memory"] i { background: var(--agx-memory); }
  .agx-waffle i[data-k="docs"], .agx-legend [data-k="docs"] i { background: var(--agx-docs); }
  .agx-waffle i[data-k="history"], .agx-legend [data-k="history"] i { background: var(--agx-history); }
  .agx-legend [data-k="free"] i { background: var(--agx-free); }
  .agx-panel:has(.agx-legend [data-k="system"]:hover) .agx-waffle i:not([data-k="system"]),
  .agx-panel:has(.agx-legend [data-k="tools"]:hover) .agx-waffle i:not([data-k="tools"]),
  .agx-panel:has(.agx-legend [data-k="memory"]:hover) .agx-waffle i:not([data-k="memory"]),
  .agx-panel:has(.agx-legend [data-k="docs"]:hover) .agx-waffle i:not([data-k="docs"]),
  .agx-panel:has(.agx-legend [data-k="history"]:hover) .agx-waffle i:not([data-k="history"]),
  .agx-panel:has(.agx-legend [data-k="free"]:hover) .agx-waffle i:not([data-k="free"]) { opacity: 0.2; }
  .agx-legend { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 1rem 0.75rem; }
  .agx-legend li { display: flex; flex-direction: column; gap: 0.375rem; cursor: default; }
  .agx-key { display: inline-flex; align-items: center; gap: 0.5rem; font-family: var(--font-mono); font-size: 0.75rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted-foreground); }
  .agx-key i { inline-size: 0.625rem; block-size: 0.625rem; border-radius: 999px; }
  .agx-val strong { font-size: 1.0625rem; font-weight: 500; font-variant-numeric: tabular-nums; }
  .agx-val small { font-family: var(--font-mono); font-size: 0.6875rem; color: var(--muted-foreground); }
  .agx-contents.tabs { display: grid; grid-template-columns: minmax(0, 1fr) auto; align-items: start; gap: 1rem; min-block-size: 20rem; align-content: start; }
  .agx-contents > [role="tabpanel"] { grid-column: 1 / -1; }
  .agx-contents-title h2 { margin: 0 0 0.25rem; font-size: 1rem; font-weight: 500; }
  .agx-contents [role="tablist"] { border-radius: 999px; }
  .agx-contents [role="tab"] { border-radius: 999px; font-family: var(--font-mono); font-size: 0.75rem; letter-spacing: 0.06em; text-transform: uppercase; padding-inline: 0.875rem; }
  .agx-rows { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; }
  .agx-rows li { display: grid; grid-template-columns: auto 1fr auto; align-items: center; gap: 0.75rem; padding-block: 0.625rem; border-block-end: 1px solid var(--border); }
  .agx-rows li:last-child { border-block-end: 0; }
  .agx-row-icon { display: inline-flex; color: var(--muted-foreground); }
  .agx-row-icon svg { inline-size: 1rem; block-size: 1rem; }
  .agx-row-main { display: flex; flex-direction: column; gap: 0.125rem; min-inline-size: 0; }
  .agx-row-title { font-size: 0.875rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .agx-row-main .agx-mono { font-size: 0.6875rem; }
  .agx-row-size { display: flex; flex-direction: column; align-items: flex-end; gap: 0.375rem; }
  .agx-bar { inline-size: 5rem; block-size: 0.25rem; border-radius: 999px; background: var(--agx-free); overflow: hidden; }
  .agx-bar span { display: block; block-size: 100%; border-radius: inherit; }
  .agx-bar[data-k="docs"] span { background: var(--agx-docs); }
  .agx-bar[data-k="memory"] span { background: var(--agx-memory); }
  .agx-bar[data-k="history"] span { background: var(--agx-history); }
  .agx-foot { display: flex; align-items: center; gap: 0.75rem; padding: 0.375rem 0.5rem 0.375rem 0.25rem; }
  .agx-foot .agx-mono { padding-inline-start: 0.75rem; border-inline-start: 1px solid var(--border); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .agx-foot .btn { margin-inline-start: auto; border-radius: 999px; flex-shrink: 0; }
  @media (max-width: 40rem) {
    .agx-stats { grid-template-columns: 1fr; }
    .agx-stats > section + section { border-inline-start: 0; border-block-start: 1px dashed var(--border); padding-inline-start: 0; padding-block-start: 1rem; }
    .agx-legend { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .agx-waffle { grid-template-columns: repeat(25, minmax(0, 1fr)); }
    .agx-contents.tabs { grid-template-columns: 1fr; }
    .agx-foot .agx-mono { display: none; }
  }
  @media (prefers-reduced-motion: reduce) { .agx-live::before { animation: none; } .agx-waffle i { transition: none; } }"""

AGENT01_JS = """<script>
(() => {
  const panel = document.querySelector('[data-context-window]');
  if (!panel) return;
  const state = __STATE__;
  const fmt = (n) => (n / 1000).toFixed(1) + 'K';
  const keys = ['system', 'tools', 'memory', 'docs', 'history'];

  // Largest-remainder rounding so the waffle always has exactly state.cells cells.
  const counts = (values) => {
    const raw = values.map((v) => v / state.window * state.cells);
    const out = raw.map(Math.floor);
    raw.map((r, i) => [r - out[i], i]).sort((a, b) => b[0] - a[0])
      .slice(0, state.cells - out.reduce((a, b) => a + b, 0)).forEach(([, i]) => out[i]++);
    return out;
  };

  const render = () => {
    const values = keys.map((k) => state.used[k]);
    const used = values.reduce((a, b) => a + b, 0);
    const free = state.window - used;
    const pct = Math.round(used / state.window * 100);
    const perTurn = state.used.history / state.turns;
    const cells = [];
    counts([...values, free]).forEach((n, i) => { for (let j = 0; j < n; j++) cells.push(keys[i] || 'free'); });
    panel.querySelectorAll('.agx-waffle i').forEach((cell, i) => { cell.dataset.k = cells[i]; });
    [...keys, 'free'].forEach((k) => {
      const v = k === 'free' ? free : state.used[k];
      panel.querySelector(`[data-val="${k}"]`).textContent = fmt(v);
      panel.querySelector(`[data-pct="${k}"]`).textContent = Math.round(v / state.window * 100) + '%';
    });
    panel.querySelector('[data-used]').textContent = fmt(used);
    panel.querySelector('[data-fill]').textContent = `${pct}% full · ~${Math.round(free / perTurn / 10) * 10} turns of headroom`;
    const health = panel.querySelector('[data-health]');
    health.dataset.level = pct >= 90 ? 'critical' : pct >= 70 ? 'warn' : 'ok';
    health.textContent = pct >= 90 ? 'Critical' : pct >= 70 ? 'Filling' : 'Healthy';
    const waffle = panel.querySelector('.agx-waffle');
    waffle.setAttribute('aria-label', `${fmt(used)} of ${fmt(state.window)} tokens used: ` + keys.map((k) => `${k} ${fmt(state.used[k])}`).join(', '));
    panel.querySelector('[data-history-meta]').textContent = `${state.turns} turns · ${fmt(state.used.history)} · ${Math.round(state.used.history / state.window * 100)}% of window`;
    panel.querySelector('[data-turn]').textContent = `Turn ${state.turn}`;
  };

  // Compaction keeps the last turns verbatim and replaces the rest with one summary.
  panel.querySelector('[data-compact]').addEventListener('click', (e) => {
    const button = e.currentTarget;
    const glyph = panel.querySelector('#agx-panel-history .agx-row-icon').innerHTML;
    const keep = 6;
    const kept = Math.round(state.used.history / state.turns * keep);
    const summary = 2400;
    state.used.history = kept + summary;
    state.turns = keep + 1;
    panel.querySelector('#agx-panel-history .agx-rows').innerHTML =
      `<li><span class="agx-row-icon">${glyph}</span><span class="agx-row-main"><span class="agx-row-title">Summary of turns 1–${state.turn - keep}</span><span class="agx-mono">Compacted · just now</span></span><span class="agx-row-size"><span class="agx-mono">${fmt(summary)}</span><span class="agx-bar" data-k="history"><span style="inline-size:30%"></span></span></span></li>` +
      `<li><span class="agx-row-icon">${glyph}</span><span class="agx-row-main"><span class="agx-row-title">Turns ${state.turn - keep + 1}–${state.turn} kept verbatim</span><span class="agx-mono">${keep} turns</span></span><span class="agx-row-size"><span class="agx-mono">${fmt(kept)}</span><span class="agx-bar" data-k="history"><span style="inline-size:100%"></span></span></span></li>`;
    button.disabled = true;
    button.querySelector('span').textContent = 'History compacted';
    render();
  });
  render();
})();
</script>
"""

state01 = {"window": WINDOW, "cells": CELLS, "turns": HISTORY_TURNS, "turn": 50, "used": {k: v for k, _, v in CATS}}

body01 = f"""
<main class="agx-stage">
  <section class="agx-panel" data-context-window aria-labelledby="agx-title">
    <header class="agx-head">
      <h1 id="agx-title">Context window</h1>
      <span class="agx-info" data-tooltip="Tokens the model sees on the next turn" data-side="bottom" tabindex="0" aria-label="About the context window">{ai("info")}</span>
      <span class="agx-live agx-push">Live</span>
      <button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Context settings">{ai("sliders")}</button>
      <button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Close panel">{ai("x")}</button>
    </header>

    <div class="agx-sheet">
      <div class="agx-stats">
        <section aria-label="Context used">
          <div class="agx-label"><span><span class="agx-mono">Context used</span><span class="agx-health" data-health data-level="warn">Filling</span></span></div>
          <p class="agx-big"><strong data-used>{fmt(used)}</strong><span>/ {WINDOW // 1000}K tokens</span></p>
          <p class="agx-mono" data-fill>{pct_used}% full · ~{headroom} turns of headroom</p>
        </section>
        <section aria-label="Prompt cache">
          <div class="agx-label"><span class="agx-mono">Prompt cache</span><span class="agx-mono">85% hit</span></div>
          <p class="agx-saved">$11.77 <small>saved</small></p>
          <div class="progress" role="progressbar" aria-label="Cache hit rate" aria-valuenow="85" aria-valuemin="0" aria-valuemax="100"><span style="width: 85%"></span></div>
          <p class="agx-mono">144K cached · 2.0K new</p>
        </section>
      </div>
      <div class="agx-waffle" role="img" aria-label="Context usage by source">{waffle(CATS)}</div>
      <ul class="agx-legend">{legend(CATS)}</ul>
    </div>

    <div class="tabs agx-sheet agx-contents" id="agx-tabs">
      <div class="agx-contents-title">
        <h2>Contents</h2>
        <p class="agx-mono" data-history-meta>{HISTORY_TURNS} turns · {fmt(hist)} · {round(hist / WINDOW * 100)}% of window</p>
      </div>
      <nav role="tablist" aria-orientation="horizontal" aria-label="Context contents">
        <button type="button" role="tab" id="agx-tab-docs" aria-controls="agx-panel-docs" aria-selected="false" tabindex="-1">Docs</button>
        <button type="button" role="tab" id="agx-tab-memory" aria-controls="agx-panel-memory" aria-selected="false" tabindex="-1">Memory</button>
        <button type="button" role="tab" id="agx-tab-history" aria-controls="agx-panel-history" aria-selected="true" tabindex="0">History</button>
      </nav>
      <div role="tabpanel" id="agx-panel-docs" aria-labelledby="agx-tab-docs" tabindex="-1" hidden><ul class="agx-rows">{rows(DOCS, "docs")}</ul></div>
      <div role="tabpanel" id="agx-panel-memory" aria-labelledby="agx-tab-memory" tabindex="-1" hidden><ul class="agx-rows">{rows(MEMORY, "memory")}</ul></div>
      <div role="tabpanel" id="agx-panel-history" aria-labelledby="agx-tab-history" tabindex="-1"><ul class="agx-rows">{rows(TURNS, "history")}</ul></div>
    </div>

    <footer class="agx-foot">
      <button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="More actions">{ai("more-v")}</button>
      <span class="agx-mono">Kestrel 2 · <span data-turn>Turn 50</span> · ledger-v3 migration</span>
      <button type="button" class="btn" data-compact>{ai("minimize")}<span>Compact history</span></button>
    </footer>
  </section>
</main>
"""

page("agent-01", "Agent 01", body01, AGENT_CSS, scripts=AGENT01_JS.replace("__STATE__", json.dumps(state01)))
blocks.append({"id": "agent-01", "title": "Agent 01", "description": "A context window panel for an agent: tokens used with a health level, prompt cache savings, a waffle chart by source with a hover-to-isolate legend, the contents by tab and a working Compact history action.", "category": "agent"})

# =================================================================== agent-02
RUNS = [
    ("run_8f2a", "Backfill ledger postings", "Kestrel 2", "succeeded", 182_400, 2.41, 412, "09:12", [("read_file", "ledger/postings.ts", "ok"), ("run_sql", "dry-run backfill · 312 rows", "ok"), ("run_sql", "backfill batch 1/4", "ok")]),
    ("run_8f1c", "Summarize migration plan", "Kestrel 2 Mini", "succeeded", 24_100, 0.08, 38, "09:05", [("read_file", "MIGRATION_PLAN.md", "ok")]),
    ("run_8e97", "Validate account balances", "Kestrel 2", "failed", 96_300, 1.22, 205, "08:51", [("run_sql", "balance check", "ok"), ("run_sql", "constraint violated: postings_amount_check", "error")]),
    ("run_8e40", "Draft rollback runbook", "Kestrel 2", "running", 61_800, 0.74, 132, "08:47", [("search_docs", "rollback", "ok"), ("write_file", "runbooks/rollback.md", "running")]),
    ("run_8dd3", "Classify support tickets", "Kestrel 2 Mini", "succeeded", 48_900, 0.15, 64, "08:30", [("fetch_tickets", "status=open · 120", "ok"), ("label", "120 tickets", "ok")]),
    ("run_8d71", "Generate release notes", "Kestrel 2 Mini", "succeeded", 12_700, 0.04, 21, "08:12", [("git_log", "v3.2.0..HEAD", "ok")]),
    ("run_8c9e", "Refactor posting service", "Kestrel 2", "failed", 143_200, 1.88, 377, "07:58", [("read_file", "ledger/postings.ts", "ok"), ("run_tests", "214 passed · 3 failed", "error")]),
    ("run_8c02", "Index schema for search", "Kestrel 2 Mini", "succeeded", 8_300, 0.02, 15, "07:40", [("read_file", "ledger-v3/schema.sql", "ok")]),
    ("run_8b6f", "Reconcile March statements", "Kestrel 2", "succeeded", 211_900, 2.86, 498, "07:21", [("fetch_statements", "2026-03 · 48 files", "ok"), ("run_sql", "reconcile", "ok"), ("write_file", "reports/march.csv", "ok")]),
    ("run_8b11", "Answer onboarding question", "Kestrel 2 Mini", "succeeded", 5_600, 0.01, 9, "07:02", []),
    ("run_8a8d", "Audit permission changes", "Kestrel 2", "running", 37_400, 0.45, 81, "06:55", [("list_audit_log", "last 24h", "ok"), ("diff_roles", "running", "running")]),
    ("run_8a20", "Translate help center", "Kestrel 2 Mini", "failed", 72_000, 0.22, 140, "06:31", [("fetch_articles", "34 articles", "ok"), ("translate", "rate limited", "error")]),
]
STATUS = {"succeeded": ("Succeeded", "check-circle", "outline"), "failed": ("Failed", "x-circle", "destructive"), "running": ("Running", "loader", "secondary")}


def dur(s):
    return f"{s // 60}m {s % 60:02d}s" if s >= 60 else f"{s}s"


def run_rows():
    out = []
    for rid, task, model, st, tok, cost, secs, start, calls in RUNS:
        label, glyph, variant = STATUS[st]
        steps = "".join(
            f'<li data-status="{s}"><code>{name}</code><span>{arg}</span></li>' for name, arg, s in calls
        ) or "<li><span>No tool calls</span></li>"
        out.append(
            f'<tr data-key="{rid}">'
            f'<td><input class="input" type="checkbox" data-select aria-label="Select {rid}"></td>'
            f'<td><button type="button" data-expand aria-expanded="false" aria-label="Show tool calls for {rid}">{ai("chevron-right")}</button></td>'
            f'<td class="agx-id">{rid}</td>'
            f'<td data-editable>{task}</td>'
            f'<td>{model}</td>'
            f'<td data-value="{label}"><span class="badge agx-status" data-variant="{variant}" data-status="{st}">{ai(glyph)}{label}</span></td>'
            f'<td class="agx-num" data-value="{tok}">{tok:,}</td>'
            f'<td class="agx-num" data-value="{cost}">${cost:.2f}</td>'
            f'<td class="agx-num" data-value="{secs}">{dur(secs)}</td>'
            f'<td class="agx-num">{start}</td>'
            f'</tr>'
            f'<tr data-detail hidden><td colspan="10"><p class="agx-mono">Tool calls · {len(calls)}</p><ol class="agx-calls">{steps}</ol></td></tr>'
        )
    return "".join(out)


def facet(key, label, values):
    pid = f"agx-f-{key}"
    opts = "".join(
        f'<label class="cluster" data-gap="2"><input class="input" type="checkbox" data-facet="{key}" value="{v}">{v}</label>' for v in values
    )
    return (
        f'<div class="dropdown-menu"><button type="button" class="btn" data-variant="outline" data-size="sm" popovertarget="{pid}">'
        f'{ai("filter")}{label}<span data-facet-count="{key}" hidden></span></button>'
        f'<div id="{pid}" data-popover popover data-align="start"><div class="stack agx-pop" data-gap="2">{opts}</div></div></div>'
    )


COLS = [("model", "Model"), ("tokens", "Tokens"), ("cost", "Cost"), ("duration", "Duration"), ("started", "Started")]

RUNS_CSS = """
  .agx-page { padding-block: 2rem 3rem; }
  .agx-page h1 { margin: 0; font-size: 1.5rem; font-weight: 600; letter-spacing: -0.01em; }
  .agx-page .agx-lead { margin: 0; color: var(--muted-foreground); font-size: 0.875rem; }
  .agx-mono { font-family: var(--font-mono); font-size: 0.6875rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted-foreground); margin: 0 0 0.5rem; }
  .agx-kpis { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0.75rem; }
  .agx-kpis > div { border: 1px solid var(--border); border-radius: var(--radius); padding: 0.875rem 1rem; background: var(--card); }
  .agx-kpis strong { display: block; font-size: 1.375rem; font-weight: 500; font-variant-numeric: tabular-nums; }
  .agx-kpis .agx-mono { margin: 0 0 0.25rem; }
  .agx-runs .table-wrap { max-block-size: 34rem; }
  .agx-runs > header { gap: 0.5rem; }
  .agx-runs > header .btn svg { inline-size: 0.875rem; block-size: 0.875rem; }
  .agx-pop { padding: 0.5rem; min-inline-size: 11rem; font-size: 0.875rem; }
  .agx-id { font-family: var(--font-mono); font-size: 0.8125rem; color: var(--muted-foreground); }
  .agx-num { font-variant-numeric: tabular-nums; text-align: end; }
  .agx-runs th.agx-num > button { margin-inline-start: auto; }
  .agx-status svg { inline-size: 0.75rem; block-size: 0.75rem; }
  .agx-status[data-status="succeeded"] { color: oklch(0.55 0.15 150); }
  .agx-status[data-status="running"] svg { animation: agx-spin 1s linear infinite; }
  @keyframes agx-spin { to { rotate: 360deg; } }
  .agx-calls { margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 0.375rem; font-size: 0.8125rem; }
  .agx-calls li { display: flex; align-items: center; gap: 0.625rem; }
  .agx-calls li::before { content: ""; inline-size: 0.5rem; block-size: 0.5rem; border-radius: 999px; background: oklch(0.72 0.17 150); flex-shrink: 0; }
  .agx-calls li[data-status="error"]::before { background: var(--destructive); }
  .agx-calls li[data-status="running"]::before { background: oklch(0.78 0.15 75); }
  .agx-calls code { font-family: var(--font-mono); font-size: 0.75rem; padding: 0.0625rem 0.375rem; border-radius: calc(var(--radius) - 4px); background: var(--muted); color: var(--foreground); }
  .agx-bulk { display: flex; align-items: center; gap: 0.5rem; }
  .agx-bulk[hidden] { display: none; }
  .agx-runs > footer select { inline-size: auto; }
  .agx-hint { font-size: 0.75rem; color: var(--muted-foreground); }
  .agx-hint kbd { font-family: var(--font-mono); }
  @media (max-width: 48rem) { .agx-kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
  @media (prefers-reduced-motion: reduce) { .agx-status[data-status="running"] svg { animation: none; } }"""

AGENT02_JS = """<script>
(() => {
  const table = document.querySelector('.agx-runs');
  const bulk = document.querySelector('[data-bulk]');
  if (!table || !bulk) return;
  table.addEventListener('selectionchange', (e) => {
    const n = e.detail.rows.length;
    bulk.hidden = n === 0;
    bulk.querySelector('[data-bulk-count]').textContent = `${n} selected`;
  });
  // Inline rename: keep the label tidy and refuse empty names.
  table.addEventListener('cellchange', (e) => {
    if (!e.detail.value.trim()) e.preventDefault();
  });
})();
</script>
"""

total_tok = sum(r[4] for r in RUNS)
total_cost = sum(r[5] for r in RUNS)
failed = sum(1 for r in RUNS if r[3] == "failed")
def th_sort(key, label, num=False):
    extra = ' data-type="number" class="agx-num"' if num else ""
    return f'<th aria-sort="none" data-key="{key}"{extra}><button type="button">{label}</button></th>'


body02 = f"""
<main class="wrapper agx-page" data-size="xl">
  <div class="stack" data-gap="6">
    <div class="stack" data-gap="1">
      <h1>Agent runs</h1>
      <p class="agx-lead">Every run today with its tool calls, cost and outcome. Rename a run by double-clicking its task.</p>
    </div>
    <div class="agx-kpis">
      <div><p class="agx-mono">Runs</p><strong>{len(RUNS)}</strong></div>
      <div><p class="agx-mono">Tokens</p><strong>{total_tok / 1000:.0f}K</strong></div>
      <div><p class="agx-mono">Spend</p><strong>${total_cost:.2f}</strong></div>
      <div><p class="agx-mono">Failure rate</p><strong>{failed / len(RUNS) * 100:.0f}%</strong></div>
    </div>
    <auvyx-data-table class="data-table agx-runs" data-page-size="8" data-grid data-sticky>
      <header>
        <input class="input" type="search" data-filter placeholder="Filter runs…" aria-label="Filter runs">
        {facet("status", "Status", ["Succeeded", "Failed", "Running"])}
        {facet("model", "Model", ["Kestrel 2", "Kestrel 2 Mini"])}
        <button type="button" class="btn" data-variant="ghost" data-size="sm" data-reset hidden>{ai("rotate")}Reset</button>
        <div class="agx-bulk" data-bulk hidden>
          <span class="agx-hint" data-bulk-count></span>
          <button type="button" class="btn" data-variant="outline" data-size="sm">{ai("rotate")}Re-run</button>
        </div>
        <div class="dropdown-menu" style="margin-inline-start: auto">
          <button type="button" class="btn" data-variant="outline" data-size="sm" popovertarget="agx-cols">{ai("columns")}Columns</button>
          <div id="agx-cols" data-popover popover data-align="end"><div class="stack agx-pop" data-gap="2">
            {"".join(f'<label class="cluster" data-gap="2"><input class="input" type="checkbox" data-column="{k}" checked>{l}</label>' for k, l in COLS)}
          </div></div>
        </div>
      </header>
      <div class="table-wrap">
        <table class="table">
          <thead>
            <tr>
              <th><input class="input" type="checkbox" data-select-all aria-label="Select all runs"></th>
              <th><span class="sr-only">Expand</span></th>
              {th_sort("run", "Run")}
              {th_sort("task", "Task")}
              {th_sort("model", "Model")}
              {th_sort("status", "Status")}
              {th_sort("tokens", "Tokens", True)}
              {th_sort("cost", "Cost", True)}
              {th_sort("duration", "Duration", True)}
              <th data-key="started" class="agx-num">Started</th>
            </tr>
          </thead>
          <tbody>
            {run_rows()}
            <tr data-empty hidden><td colspan="10">No runs match these filters.</td></tr>
          </tbody>
        </table>
      </div>
      <footer>
        <span data-selected-count data-template="{{selected}} of {{total}} runs selected"></span>
        <span class="agx-hint"><kbd>↑↓←→</kbd> move · <kbd>Space</kbd> select · <kbd>Enter</kbd> edit</span>
        <label class="cluster" data-gap="2">Rows <select class="select" data-page-size aria-label="Rows per page"><option>5</option><option selected>8</option><option>12</option></select></label>
        <span data-page-status></span>
        <button type="button" class="btn" data-variant="outline" data-size="icon-sm" data-page="first" aria-label="First page">{ai("chevrons-left")}</button>
        <button type="button" class="btn" data-variant="outline" data-size="icon-sm" data-page="prev" aria-label="Previous page">{ai("chevron-left")}</button>
        <button type="button" class="btn" data-variant="outline" data-size="icon-sm" data-page="next" aria-label="Next page">{ai("chevron-right")}</button>
        <button type="button" class="btn" data-variant="outline" data-size="icon-sm" data-page="last" aria-label="Last page">{ai("chevrons-right")}</button>
      </footer>
    </auvyx-data-table>
  </div>
</main>
"""

page("agent-02", "Agent 02", body02, RUNS_CSS, scripts=AGENT02_JS, head_extra='<script src="../ui/dist/js/data-table.min.js" defer></script>\n')
blocks.append({"id": "agent-02", "title": "Agent 02", "description": "An agent runs table: status and model facets, sortable cost and tokens, expandable tool-call rows, inline rename, grid keyboard navigation and a bulk re-run bar.", "category": "agent"})

if __name__ == "__main__":
    register(blocks)
    print("agent blocks:", ", ".join(b["id"] for b in blocks))

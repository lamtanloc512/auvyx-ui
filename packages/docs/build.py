"""Build the Auvyx UI docs site into packages/docs/out/.

  python3 packages/docs/build.py

Steps: run packages/ui build, compile docs.css (bundle + the Tailwind
utilities the upstream examples use), assemble index.html with embedded data,
copy dist files and blocks (paths rewritten for the site layout).
"""
import json, pathlib, re, shutil, subprocess, gzip
from html import escape as html_escape

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS = ROOT / "packages/docs"
OUT = DOCS / "out"
UI = ROOT / "packages/ui"
BLOCKS = ROOT / "packages/blocks"

VERSION = json.loads((UI / "package.json").read_text())["version"]
# major.minor: jsDelivr serves the newest published 0.1.x, so the docs never
# link a version npm has not released yet (it waits for approval after a bump).
CDN = f"https://cdn.jsdelivr.net/npm/@auvyx/ui@{'.'.join(VERSION.split('.')[:2])}/dist"


SITE = "https://ui.auvyx.org"


def write_llms(guides_list, comps, blocks):
    """llms.txt (llmstxt.org) plus a Markdown export of every guide and component under md/."""
    md = OUT / "md"
    (md / "components").mkdir(parents=True, exist_ok=True)
    lines = ["# Auvyx UI", "", "> A drop-in design system with the shadcn look: plain HTML and CSS classes, optional JavaScript, a Web Components edition, React blocks and a shadcn-style registry and CLI.", ""]
    lines += ["## Docs", ""]
    for g in guides_list:
        (md / f"{g['slug']}.md").write_text(f"# {g['title']}\n\n> {g['description']}\n\n{g['html'].strip()}\n")
        lines.append(f"- [{g['title']}]({SITE}/md/{g['slug']}.md): {g['description']}")
    lines += ["", "## Components", ""]
    for key, c in comps.items():
        parts = [f"# {c['title']}", "", c["description"], "", f"Install: `npx @auvyx/cli add {key}` (or load auvyx.min.css for every component).", "", "## Examples", ""]
        for ex in c["examples"]:
            parts += [f"### {ex['title']}", "", "```html", ex["html"].strip(), "```", ""]
        if c.get("notes"):
            parts += ["## Usage", "", c["notes"].strip(), ""]
        (md / "components" / f"{key}.md").write_text("\n".join(parts))
        lines.append(f"- [{c['title']}]({SITE}/md/components/{key}.md): {c['description']}")
    lines += ["", "## Blocks", "", f"- [Registry index, HTML]({SITE}/r/html/lucide/index.json): every block and component as a registry item ({len(blocks)} blocks)",
              f"- [Registry index, React]({SITE}/r/react/lucide/index.json): the same items as React 19 components", ""]
    (OUT / "llms.txt").write_text("\n".join(lines))
    # Every export in one file, guides first.
    full = [(md / f"{g['slug']}.md").read_text() for g in guides_list] + [(md / "components" / f"{k}.md").read_text() for k in comps]
    (OUT / "llms-full.txt").write_text("\n\n".join(full))


def run(*cmd, **kw):
    subprocess.run(cmd, check=True, cwd=ROOT, **kw)


def gz(path):
    return f"{len(gzip.compress(path.read_bytes(), 9)) / 1024:.1f} kB"


def code(html):
    e = html.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<div class="d-code"><button type="button" class="btn d-copy" data-variant="outline" data-size="icon-sm" aria-label="Copy code"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="inline-size:1rem;block-size:1rem"><rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg></button><pre><code>{e}</code></pre></div>'


def demo(html):
    return f'<div class="d-preview" style="min-block-size:auto;padding:1.5rem"><div class="d-stage" style="display:block">{html}</div></div>' + code(html)


TILE = '<div style="padding:.75rem 1rem;border:1px solid var(--border);border-radius:calc(var(--radius) - 2px);font-size:.875rem;background:var(--card)">{}</div>'


# Same element ids as Create.syncBlock(), so the docs iframe sync updates them in place.
BLOCK_PRESET = """<script>
      (function () {
        var d = document, r = d.documentElement, p = null, m = null;
        try { p = JSON.parse(localStorage.getItem("auvyx-preset") || "null"); m = localStorage.getItem("auvyx-docs-mode"); } catch (e) {}
        if (m && !/[?&]theme=/.test(location.search)) r.classList.toggle("dark", m === "dark");
        if (!p) return;
        function add(tag, id, attrs) { var el = d.createElement(tag); el.id = id; for (var k in attrs) el[k] = attrs[k]; d.head.appendChild(el); }
        if (p.style) add("link", "d-cr-style", { rel: "stylesheet", href: "../dist/styles/" + p.style });
        if (p.fonts) add("link", "d-cr-fonts", { rel: "stylesheet", href: p.fonts });
        add("style", "d-cr-theme", { textContent: p.css });
      })();
    </script>
    <script src="../icons.js" defer></script>"""


def guides(sizes, js_modules, wc_modules):
    t = lambda s: TILE.format(s)
    return [
        {"slug": "introduction", "title": "Introduction", "description": "A drop-in design system with the shadcn look: plain HTML, optional JavaScript, no build step.", "html": f"""
<p>Auvyx UI gives you shadcn/ui's visual language without React and without a build step. It covers the shadcn/ui components and blocks, adds a zero-JavaScript path built on modern browser features, and ships as a Bootstrap-style CDN bundle.</p>
<h2 class="d-h2">Two ways to use it</h2>
<div class="d-tablewrap"><table><thead><tr><th>Channel</th><th>For</th><th>What you get</th></tr></thead><tbody>
<tr><td><code>auvyx.min.css</code> (CDN)</td><td>Server-rendered apps, prototypes, no build step</td><td>Every component plus layout primitives. No utility classes, so it never clashes with your own Tailwind.</td></tr>
<tr><td><code>auvyx.bundle.css</code> (source)</td><td>Projects that already run Tailwind v4</td><td>The component source. Your build generates every utility you use, and you own the code, the shadcn way.</td></tr>
</tbody></table></div>
<h2 class="d-h2">Principles</h2>
<ul>
<li><strong>Platform first.</strong> Dialogs are <code>&lt;dialog&gt;</code>, popovers use the Popover API, accordions are <code>&lt;details name&gt;</code>, toggles are checkboxes. They work before any script loads.</li>
<li><strong>JavaScript only where it earns its place.</strong> Keyboard models for menus, calendars, data tables, resizable panels. Shipped as light-DOM custom elements, so the same CSS styles them and forms submit natively.</li>
<li><strong>Tokens are the contract.</strong> The shadcn CSS variables (<code>--primary</code>, <code>--radius</code>…) theme everything, including the blocks.</li>
</ul>
<p>Current build: <code>auvyx.min.css</code> {sizes['css']} gzip, optional <code>auvyx.min.js</code> {sizes['js']} gzip.</p>"""},
        {"slug": "installation", "title": "Installation", "description": "Link the CDN files, install from npm, or import the source into Tailwind v4.", "html": f"""
<h2 class="d-h2">CDN</h2><p>Add the stylesheet. Most components need nothing else.</p>
{code(f'<link rel="stylesheet" href="{CDN}/auvyx.min.css">')}
<h2 class="d-h2">JavaScript</h2><p>Some components need JavaScript for their behavior; each component page says so and shows the script to add. Load one module per component you use, or <code>auvyx.min.js</code> ({sizes['js']} gzip) for all of them:</p>
{code(f'<!-- only what the page uses -->' + chr(10) + f'<script src="{CDN}/js/tabs.min.js" defer></script>' + chr(10) + f'<script src="{CDN}/js/select.min.js" defer></script>' + chr(10) + chr(10) + f'<!-- or everything -->' + chr(10) + f'<script src="{CDN}/auvyx.min.js" defer></script>')}
<p>Modules are independent: load any combination, in any order, even after the page has loaded. Components share a small core that only the first module sets up.</p>
<div class="d-tablewrap"><table><thead><tr><th>Module</th><th>Size (gzip)</th><th>Needed for</th></tr></thead><tbody>
{"".join(f'<tr><td><code>js/{n}.min.js</code></td><td>{m["gzip"] / 1024:.1f} kB</td><td>{"Optional: " if m["kind"] == "enhance" else ""}{n.replace("-", " ").capitalize()}{(". " + html_escape(m["note"])) if m.get("note") else ""}</td></tr>' for n, m in js_modules.items())}
</tbody></table></div>
<h2 class="d-h2">JavaScript lifecycle</h2><p>The JavaScript API is <code>window.auvyx</code>: <code>initAll()</code>, <code>init(name)</code>, <code>refresh()</code>, <code>start()</code> / <code>stop()</code> (the observer), <code>theme.get()</code> / <code>set()</code> / <code>toggle()</code>, and <code>chart()</code> with <code>auvyx.chart.min.js</code>. <code>window.basecoat</code> is the same object, kept for existing code.</p><p>Components initialize on page load and whenever new markup is inserted (a <code>MutationObserver</code> watches the page), so HTML swapped in by HTMX, Turbo or your own code works without extra calls. After inserting markup by hand you can also call <code>window.auvyx.initAll()</code>; it only initializes components that are not initialized yet.</p>
<p>When a library restores previously initialized markup from a cache (HTMX history restore, Turbo snapshots), call <code>window.auvyx.initAll({{ force: true }})</code>: it destroys the existing instances and initializes them again, which also resets open menus, focus and other transient state.</p>
<h2 class="d-h2">Editions</h2><p>Auvyx comes in two editions that share the same CSS and the same behavior code. Pick per component; they mix on one page.</p>
<div class="d-tablewrap"><table><thead><tr><th>Edition</th><th>Markup</th><th>Best for</th></tr></thead><tbody>
<tr><td>HTML (default)</td><td>Classes and ARIA, plus a script from <code>js/</code></td><td>Server templates, static sites, HTMX, copy-paste blocks</td></tr>
<tr><td>Web Components</td><td>The same markup wrapped in <code>&lt;auvyx-*&gt;</code>, script from <code>wc/</code></td><td>React, Vue, Svelte, Angular: a <code>value</code> property and a <code>change</code> event</td></tr>
</tbody></table></div>
{code('<!-- HTML edition -->' + chr(10) + '<div class="tabs">…</div>' + chr(10) + f'<script src="{CDN}/js/tabs.min.js" defer></script>' + chr(10) + chr(10) + '<!-- Web Components edition: same markup, wrapped -->' + chr(10) + '<auvyx-tabs value="account">' + chr(10) + '  <div class="tabs">…</div>' + chr(10) + '</auvyx-tabs>' + chr(10) + f'<script src="{CDN}/wc/tabs.min.js" defer></script>')}
<p>Web Components so far: {", ".join(f'<code>&lt;{m["tag"]}&gt;</code> ({m["gzip"] / 1024:.1f} kB)' for m in wc_modules.values())}. Each file includes the component's behavior, so it replaces the matching <code>js/</code> module. In React 19 use <code>onChange</code> / <code>onInput</code> and read <code>e.currentTarget.value</code>, and use the lowercase <code>ontoggle</code> / <code>onselect</code> (React's <code>onToggle</code> and <code>onSelect</code> are its own synthetic events and do not fire for custom elements); in Vue add <code>app.config.compilerOptions.isCustomElement = (tag) =&gt; tag.startsWith('auvyx-')</code>; in Angular add <code>CUSTOM_ELEMENTS_SCHEMA</code>.</p>
<h2 class="d-h2">TypeScript</h2><p>Every <code>&lt;auvyx-*&gt;</code> element ships with types: properties, attributes, events (with their <code>detail</code>) and methods. Import the set you need once, for example in your entry file:</p>
{code('// DOM: querySelector("auvyx-tabs") is typed, addEventListener knows each event' + chr(10) + 'import type {} from "@auvyx/ui/types";' + chr(10) + chr(10) + '// React 19 JSX (also flags onToggle / onSelect, which never fire on custom elements)' + chr(10) + 'import type {} from "@auvyx/ui/types/react";' + chr(10) + chr(10) + '// Vue 3 templates (Volar / vue-tsc)' + chr(10) + 'import type {} from "@auvyx/ui/types/vue";')}
<p>Editors and tools that read the <a href="https://github.com/webcomponents/custom-elements-manifest" target="_blank" rel="noopener">Custom Elements Manifest</a> find it at <code>@auvyx/ui/custom-elements.json</code> (also linked from <code>package.json</code> as <code>customElements</code>).</p>
<h2 class="d-h2">npm</h2>{code('npm install @auvyx/ui' + chr(10) + chr(10) + '/* in your CSS entry */' + chr(10) + '@import "@auvyx/ui";')}
<h2 class="d-h2">Tailwind v4 (source channel)</h2><p>Import after Tailwind. Your build compiles the components and generates the utilities your markup uses.</p>
{code('@import "tailwindcss";' + chr(10) + '@import "@auvyx/ui/bundle";')}
<h2 class="d-h2">Only the components you use</h2><p>Instead of the whole <code>auvyx.min.css</code>, copy single components into your project with the CLI. Each one is its CSS split from the bundle (plain CSS, no Tailwind needed), its JavaScript if it has behavior, and the components its examples use; <code>base.css</code> (tokens, themes, preflight, layout, motion) comes with the first.</p>
{code('npx @auvyx/cli add combobox tabs')}
<p>The CLI keeps <code>ui/index.css</code> importing every installed file in the order they cascade in the bundle, so load that one file (and the <code>ui/*.js</code> files it lists). Components override each other at equal specificity, so that order matters: link files by hand only in the order of the <code>order</code> number on their first line. The same files are on the CDN under <code>dist/ui/</code>, listed in <code>dist/ui/manifest.json</code>.</p>
<h2 class="d-h2">Pick only the elements you use</h2><p>Each custom element also ships as an ES module:</p>
{code(f'<script type="module" src="{CDN}/elements/calendar.min.js"></script>' + chr(10) + f'<script type="module" src="{CDN}/elements/date-picker.min.js"></script>')}
<h2 class="d-h2">Charts</h2>{code('<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>' + chr(10) + f'<script src="{CDN}/auvyx.chart.min.js" defer></script>')}"""},
        {"slug": "theming", "title": "Theming", "description": "Design tokens, dark mode and brand themes, with CSS variables only.", "html": f"""
<p>Every color, radius and font comes from CSS variables named like shadcn's. Themes from the shadcn theme generator or TweakCN can be pasted in as they are.</p>
<h2 class="d-h2">Dark mode</h2><p>Add <code>dark</code> to <code>&lt;html&gt;</code>. Set it before first paint to avoid a flash:</p>
{code('<script>' + chr(10) + '  document.documentElement.classList.toggle("dark",' + chr(10) + '    localStorage.theme === "dark" || (!localStorage.theme && matchMedia("(prefers-color-scheme: dark)").matches));' + chr(10) + '</script>')}
<h2 class="d-h2">Brand themes</h2><p>A theme only overrides the tokens that change. Apply it on any element, not just <code>&lt;html&gt;</code>. Try the theme picker in the header.</p>
{demo('<div class="cluster" data-gap="3">' + ''.join(f'<div data-theme="{t}" class="cluster" data-gap="2"><button class="btn">{t.title() or "Neutral"}</button><span class="badge">Badge</span><input type="checkbox" role="switch" class="input" checked aria-label="{t or "neutral"} switch"></div>' for t in ["", "ocean", "forest"]) + '</div>')}
{code('[data-theme="ocean"] {' + chr(10) + '  --primary: oklch(0.546 0.185 256);' + chr(10) + '  --primary-foreground: oklch(0.985 0 0);' + chr(10) + '  --ring: oklch(0.707 0.12 256);' + chr(10) + '}')}
<h2 class="d-h2">Themes from tweakcn</h2><p>Any theme from <a href="https://tweakcn.com" target="_blank" rel="noopener">tweakcn.com</a> works as exported: open the theme, choose <strong>Code → CSS</strong>, and paste the <code>:root</code> and <code>.dark</code> blocks after the Auvyx stylesheet. Colors, fonts (<code>--font-sans</code>, <code>--font-mono</code>), <code>--radius</code>, <code>--shadow-*</code>, <code>--tracking-normal</code> and <code>--spacing</code> all take effect. Skip the <code>@theme inline</code> block: Auvyx already maps the tokens. Load the theme's Google Fonts yourself, or import it on the <a href="#create">Create</a> page, which adds the font link for you.</p>
{code('<link rel="stylesheet" href="' + CDN + '/auvyx.min.css">' + chr(10) + '<style>' + chr(10) + '  :root { --primary: oklch(0.62 0.19 260); --radius: 0.75rem; --font-sans: Inter, sans-serif; --shadow-sm: 0 1px 3px 0 hsl(0 0% 0% / 0.1); }' + chr(10) + '  .dark { --primary: oklch(0.7 0.16 260); }' + chr(10) + '</style>')}
<h2 class="d-h2">Corner shape (squircles)</h2><p><code>--corner-shape</code> sets the shape of every rounded corner: <code>round</code> (default), <code>squircle</code>, <code>superellipse(1.5)</code>, <code>bevel</code>, <code>scoop</code> or <code>notch</code>. Browsers with CSS <code>corner-shape</code> (Chrome 139+) draw it natively; controls whose shape carries meaning (radios, switches, avatars) stay round. For other browsers, add the optional <code>auvyx.corners.min.js</code> (4 kB, bundles <a href="https://somonoco.com" target="_blank" rel="noopener">Monoco</a>): it clips cards, popovers, dialogs, alerts and sheets to the same shape and redraws their borders on that path, so borders stay continuous at the corners. Tune it with <code>--corner-smoothing</code> (0–1).</p>
{code(':root { --corner-shape: squircle; --radius: 0.875rem; }' + chr(10) + chr(10) + '<script src="' + CDN + '/auvyx.corners.min.js" defer></script>  <!-- optional fallback -->')}
<h2 class="d-h2">Fonts</h2><p>Auvyx ships no font files. <code>--font-sans</code>, <code>--font-heading</code> and <code>--font-mono</code> prefer Geist and Geist Mono when the page has them, then fall back to system stacks. Load the fonts you want (Google Fonts, Fontsource, your own files) and point the tokens at them; the Create page does both for its font presets.</p>
{code(':root {' + chr(10) + '  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;' + chr(10) + '  --font-heading: "Inter", ui-sans-serif, system-ui, sans-serif;' + chr(10) + '  --font-mono: "IBM Plex Mono", ui-monospace, monospace;' + chr(10) + '}')}
<h2 class="d-h2">Tokens</h2><div class="d-tablewrap"><table><thead><tr><th>Token</th><th>Used for</th></tr></thead><tbody>
<tr><td><code>--background</code> / <code>--foreground</code></td><td>Page surface and text</td></tr>
<tr><td><code>--primary</code> / <code>--primary-foreground</code></td><td>Main actions, selected states, focus accents</td></tr>
<tr><td><code>--muted</code> / <code>--muted-foreground</code></td><td>Subtle surfaces and secondary text</td></tr>
<tr><td><code>--accent</code></td><td>Hover and highlighted items in menus and lists</td></tr>
<tr><td><code>--destructive</code></td><td>Errors and dangerous actions</td></tr>
<tr><td><code>--border</code>, <code>--input</code>, <code>--ring</code></td><td>Lines, form controls, focus rings</td></tr>
<tr><td><code>--radius</code></td><td>Corner radius scale (sm, md, lg, xl derive from it)</td></tr>
<tr><td><code>--corner-shape</code></td><td>Corner shape: round, squircle, superellipse(), bevel, scoop, notch</td></tr>
<tr><td><code>--font-sans</code>, <code>--font-heading</code>, <code>--font-mono</code></td><td>Body, heading and code fonts</td></tr>
<tr><td><code>--shadow-2xs…2xl</code>, <code>--tracking-normal</code>, <code>--spacing</code></td><td>Shadow scale, letter spacing, spacing unit (tweakcn tokens)</td></tr>
<tr><td><code>--sidebar-*</code>, <code>--chart-1…5</code></td><td>Sidebar surfaces, chart series</td></tr>
</tbody></table></div>"""},
        {"slug": "motion", "title": "Motion", "description": "One motion language for every component: shared tokens, CSS springs and reduced-motion fallbacks.", "html": f"""
<p>Every Auvyx component moves the same way. Buttons spring back from a press; fields, selects, checkboxes, radios and switches darken on hover, and choices and slider thumbs give under a press; menus and popovers scale in from their trigger, dialogs and sheets enter on an ease-out curve and leave faster, tab panels and accordion content fade in and rise. It is all CSS (transitions, <code>@starting-style</code> and <code>linear()</code> springs), so it works on the CDN build with no script.</p>
{demo("""<div class="cluster" data-gap="3">
  <button class="btn">Press me</button>
  <div class="dropdown-menu">
    <button type="button" class="btn" data-variant="outline" popovertarget="motion-menu">Open menu</button>
    <div id="motion-menu" data-popover popover data-side="bottom" data-align="start">
      <div role="menu">
        <button type="button" role="menuitem">Profile</button>
        <button type="button" role="menuitem">Billing</button>
        <button type="button" role="menuitem">Settings</button>
      </div>
    </div>
  </div>
  <label class="label">
    <input type="checkbox" role="switch" class="input">
    Spring switch
  </label>
</div>""")}
<h2 class="d-h2">Tokens</h2>
<p>Components read these variables. Override them on <code>:root</code>, or on any element to retune a single area.</p>
<div class="d-tablewrap"><table><thead><tr><th>Variable</th><th>Default</th><th>Used for</th></tr></thead><tbody>
<tr><td><code>--motion-fast</code></td><td>120ms</td><td>Exits, hover and color changes</td></tr>
<tr><td><code>--motion-base</code></td><td>200ms</td><td>Popovers, dialogs, tab panels, disclosure</td></tr>
<tr><td><code>--motion-slow</code></td><td>320ms</td><td>Sheets, drawers, toasts</td></tr>
<tr><td><code>--motion-ease-standard</code></td><td><code>cubic-bezier(0.2, 0, 0, 1)</code></td><td>Changes in place</td></tr>
<tr><td><code>--motion-ease-enter</code></td><td><code>cubic-bezier(0.16, 1, 0.3, 1)</code></td><td>Anything appearing</td></tr>
<tr><td><code>--motion-ease-exit</code></td><td><code>cubic-bezier(0.4, 0, 1, 1)</code></td><td>Anything leaving</td></tr>
<tr><td><code>--motion-spring-snappy</code></td><td>388ms</td><td>Presses, switch thumbs</td></tr>
<tr><td><code>--motion-spring-gentle</code>, <code>--motion-spring-playful</code></td><td>520ms, 623ms</td><td>Available for your own transitions</td></tr>
<tr><td><code>--motion-rise</code>, <code>--motion-scale-from</code></td><td>0.5rem, 0.96</td><td>Distance content rises, scale surfaces start from</td></tr>
</tbody></table></div>
<p>Springs are <code>linear()</code> easings sampled from real spring physics (stiffness, damping, mass). Each has a matching <code>-duration</code> variable, the time the spring needs to settle:</p>
{code('.my-chip {' + chr(10) + '  transition: scale var(--motion-spring-playful-duration) var(--motion-spring-playful);' + chr(10) + '}' + chr(10) + '.my-chip:active {' + chr(10) + '  scale: 0.95;' + chr(10) + '}')}
<h2 class="d-h2">What moves</h2>
<div class="d-tablewrap"><table><thead><tr><th>Component</th><th>Enter</th><th>Leave</th></tr></thead><tbody>
<tr><td>Button, toggle, tab</td><td colspan="2">Press to 0.97 (buttons also sink 1px), spring back. Menu triggers (<code>aria-haspopup</code>) stay still.</td></tr>
<tr><td>Dropdown, select, combobox, popover, hover card, tooltip</td><td>Fade and scale from 0.96, growing from the side that faces the trigger</td><td>Fade out, 120ms</td></tr>
<tr><td>Dialog, alert dialog, command dialog</td><td>Panel scales from 0.96, backdrop fades</td><td>120ms</td></tr>
<tr><td>Sheet, drawer</td><td>Slide in, 320ms</td><td>Slide out, 200ms</td></tr>
<tr><td>Accordion, collapsible</td><td colspan="2">Height animates to the content's size; content fades and rises</td></tr>
<tr><td>Tabs, toast</td><td colspan="2">New panel or toast fades and rises 8px</td></tr>
<tr><td>Switch</td><td colspan="2">Thumb travels on the snappy spring</td></tr>
</tbody></table></div>
<h2 class="d-h2">Reduced motion</h2>
<p>With <code>prefers-reduced-motion: reduce</code> nothing moves or scales; state changes become near-instant fades. To turn motion off entirely, for tests or screenshots, set <code>data-motion="off"</code> on <code>&lt;html&gt;</code>:</p>
{code('<html data-motion="off">')}"""},
        {"slug": "layout", "title": "Layout primitives", "description": "Seven named layouts that replace utility classes on the CDN channel.", "html": f"""
<p>The CDN bundle has no utility classes. Pages are laid out with a handful of primitives, configured with <code>data-*</code> attributes or CSS variables for one-off values. None of the names clash with Tailwind.</p>
<div class="d-tablewrap"><table><thead><tr><th>Class</th><th>Does</th><th>Options</th></tr></thead><tbody>
<tr><td><code>.wrapper</code></td><td>Centered page column with side gutter</td><td><code>data-size</code> sm · md · lg · xl · prose</td></tr>
<tr><td><code>.stack</code></td><td>Vertical flow with gap</td><td><code>data-gap</code>, <code>data-align</code></td></tr>
<tr><td><code>.cluster</code></td><td>Horizontal, wraps, centered</td><td><code>data-gap</code>, <code>data-justify</code>, <code>data-align</code></td></tr>
<tr><td><code>.auto-grid</code></td><td>Responsive columns, no breakpoints</td><td><code>data-min</code> xs · sm · md · lg, <code>--min</code></td></tr>
<tr><td><code>.split</code></td><td>Side + main, stacks when narrow</td><td><code>--side</code>, <code>--split-min</code>, <code>data-side="end"</code></td></tr>
<tr><td><code>.switcher</code></td><td>Equal columns that stack below a width</td><td><code>--threshold</code></td></tr>
<tr><td><code>.cover</code></td><td>Full-height, centers its child</td><td><code>data-pad</code></td></tr>
</tbody></table></div>
<h2 class="d-h2">Stack and cluster</h2>{demo('<div class="stack" data-gap="3">' + t('.stack') + '<div class="cluster" data-gap="2" data-justify="between">' + t('.cluster') + t('wraps') + t('data-justify="between"') + '</div></div>')}
<h2 class="d-h2">Auto grid</h2><p>Columns appear as space allows. Resize the window to see it reflow without media queries.</p>{demo('<div class="auto-grid" data-min="xs" data-gap="2">' + ''.join(t(f"Item {i}") for i in range(1, 7)) + '</div>')}
<h2 class="d-h2">Split</h2>{demo('<div class="split" data-gap="3" style="--side: 10rem">' + t('Side, 10rem') + t('Main takes the rest and drops below when it would get narrower than half') + '</div>')}
<h2 class="d-h2">Switcher</h2>{demo('<div class="switcher" data-gap="3" style="--threshold: 30rem">' + t('One') + t('Two') + t('Three') + '</div>')}"""},
        {"slug": "zero-js", "title": "Zero-JS components", "description": "What works without any script, and the browser features behind it.", "html": """
<div class="d-tablewrap"><table><thead><tr><th>Component</th><th>Built on</th></tr></thead><tbody>
<tr><td>Dialog, Alert Dialog, Sheet, Drawer</td><td><code>&lt;dialog&gt;</code> + <code>commandfor</code>/<code>command</code> (Invoker Commands), <code>closedby="any"</code></td></tr>
<tr><td>Popover, Dropdown Menu, Menubar, Navigation Menu</td><td>Popover API + CSS anchor positioning (falls back to centered)</td></tr>
<tr><td>Accordion, Collapsible, Trace steps</td><td><code>&lt;details name&gt;</code>, <code>::details-content</code> animation</td></tr>
<tr><td>Toggle, Toggle Group, Questionnaire</td><td>Native checkbox and radio inputs, submit with forms</td></tr>
<tr><td>Hover Card, Tooltip</td><td><code>:hover</code> / <code>:focus-within</code> with open delay</td></tr>
<tr><td>Input OTP</td><td>One native input drawn as slots; paste and SMS autofill work</td></tr>
<tr><td>Carousel</td><td>CSS scroll snap, <code>::scroll-button()</code>, <code>::scroll-marker</code></td></tr>
<tr><td>Message Scroller</td><td><code>column-reverse</code> pinning + scroll-driven animation</td></tr>
<tr><td>Date Picker</td><td>Without JS: the browser's native date input</td></tr>
</tbody></table></div>
<p>Scripts add keyboard models (arrow keys in menus, roving focus in calendars), hover-to-open for the navigation menu, and the widgets that need state: Select, Combobox, Command, Tabs, Toast, Data Table, Resizable, Calendar.</p>"""},
        {"slug": "templates", "title": "Templates", "description": "Nunjucks and Jinja macros for components with larger markup.", "html": (DOCS / "src/data/guides/templates.html").read_text()},
    ]


CHART_ROWS = [{"month": m, "desktop": d, "mobile": mo} for m, d, mo in
              [("Jan", 186, 80), ("Feb", 305, 200), ("Mar", 237, 120), ("Apr", 73, 190), ("May", 209, 130), ("Jun", 214, 140)]]
SERIES = {"desktop": {"label": "Desktop", "color": "var(--chart-2)"}, "mobile": {"label": "Mobile", "color": "var(--chart-1)"}}


def charts():
    area = {k: {**v, "surface": "gradient", "dataset": {"fill": "origin", "tension": 0.4, "pointRadius": 0}} for k, v in SERIES.items()}
    browsers = [{"label": b, "value": v, "color": f"var(--chart-{i + 1})"} for i, (b, v) in enumerate([("Chrome", 275), ("Safari", 200), ("Firefox", 187), ("Edge", 173), ("Other", 90)])]
    return [
        {"title": "Area Chart", "description": "Visitors, January to June", "config": {"type": "line", "labelKey": "month", "data": CHART_ROWS, "series": {"desktop": area["desktop"]}}},
        {"title": "Area Chart, stacked", "description": "Desktop and mobile visitors", "config": {"type": "line", "labelKey": "month", "data": CHART_ROWS, "series": area, "legend": True, "options": {"scales": {"y": {"stacked": True}}}}},
        {"title": "Bar Chart, multiple", "description": "Desktop vs mobile", "config": {"type": "bar", "labelKey": "month", "data": CHART_ROWS, "series": SERIES, "legend": True}},
        {"title": "Bar Chart, stacked", "description": "Total visitors by month", "config": {"type": "bar", "labelKey": "month", "data": CHART_ROWS, "series": SERIES, "options": {"scales": {"x": {"stacked": True}, "y": {"stacked": True}}}}},
        {"title": "Bar Chart, horizontal", "description": "Desktop visitors", "config": {"type": "bar", "labelKey": "month", "data": CHART_ROWS, "series": {"desktop": SERIES["desktop"]}, "options": {"indexAxis": "y", "scales": {"x": {"grid": {"display": True}, "ticks": {"display": False}}, "y": {"grid": {"display": False}, "ticks": {"display": True}}}}}},
        {"title": "Line Chart", "description": "Smooth line", "config": {"type": "line", "labelKey": "month", "data": CHART_ROWS, "series": {"desktop": {**SERIES["desktop"], "dataset": {"tension": 0.4, "pointRadius": 0, "borderWidth": 2}}}}},
        {"title": "Line Chart, step", "description": "Stepped values", "config": {"type": "line", "labelKey": "month", "data": CHART_ROWS, "series": {"desktop": {**SERIES["desktop"], "dataset": {"stepped": True, "pointRadius": 0, "borderWidth": 2}}}}},
        {"title": "Line Chart, dots", "description": "Two series with points", "config": {"type": "line", "labelKey": "month", "data": CHART_ROWS, "series": {k: {**v, "dataset": {"tension": 0.3, "pointRadius": 3, "borderWidth": 2}} for k, v in SERIES.items()}, "legend": True}},
        {"title": "Donut Chart", "description": "Browser share", "config": {"type": "doughnut", "data": browsers, "legend": True, "options": {"cutout": "62%"}}},
        {"title": "Pie Chart", "description": "Browser share", "config": {"type": "pie", "data": browsers, "legend": True}},
        {"title": "Radar Chart", "description": "Desktop vs mobile by month", "config": {"type": "radar", "labelKey": "month", "data": CHART_ROWS, "series": {k: {**v, "surface": True} for k, v in SERIES.items()}, "legend": True}},
        {"title": "Radial Chart", "description": "Polar area of browser share", "config": {"type": "polarArea", "data": browsers, "legend": True}},
    ]


BLOCK_CATS = [("dashboard", "Dashboard"), ("sidebar", "Sidebar"), ("login", "Login"), ("signup", "Signup"), ("otp", "OTP"), ("calendar", "Calendar")]
FEATURED = ["dashboard-01", "sidebar-07", "sidebar-03", "login-03", "login-04", "calendar-20"]
HEIGHTS = {"dashboard": 58, "sidebar": 50, "login": 46, "signup": 50, "otp": 40, "calendar": 34}
TALL = {"calendar-20": 36, "calendar-21": 38, "calendar-27": 38, "calendar-31": 44, "calendar-03": 34, "signup-02": 54, "signup-03": 54, "signup-01": 54}


def main():
    run("node", "packages/ui/build.mjs")
    # components.json is committed; regenerate it with tools/extract.py (SHADCN_DOCS=<shadcn checkout>/apps/v4/content/docs/components/base).
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "dist").mkdir(parents=True)
    for f in ["auvyx.min.css", "auvyx.min.js", "auvyx.chart.min.js", "auvyx.corners.min.js"]:
        shutil.copy(UI / "dist" / f, OUT / "dist" / f)
    shutil.copytree(UI / "dist" / "elements", OUT / "dist" / "elements")
    shutil.copytree(UI / "dist" / "js", OUT / "dist" / "js")
    shutil.copytree(UI / "dist" / "wc", OUT / "dist" / "wc")
    shutil.copytree(UI / "dist" / "styles", OUT / "dist" / "styles")
    shutil.copytree(UI / "dist" / "types", OUT / "dist" / "types")
    shutil.copytree(UI / "dist" / "ui", OUT / "dist" / "ui")
    shutil.copy(UI / "dist" / "custom-elements.json", OUT / "dist" / "custom-elements.json")
    run("python3", str(DOCS / "tools/showcase.py"))
    shutil.copy(DOCS / "src/create-preview.html", OUT / "create-preview.html")

    sizes = {"css": gz(UI / "dist/auvyx.min.css"), "js": gz(UI / "dist/auvyx.min.js")}
    comps = json.loads((DOCS / "src/data/components.json").read_text())
    # Reference notes (markup structure, JS API) live as HTML next to the extracted data,
    # so re-running tools/extract.py keeps them.
    for f in sorted((DOCS / "src/data/notes").glob("*.html")):
        if f.stem not in comps:
            raise SystemExit(f"notes for unknown component: {f.name}")
        comps[f.stem]["notes"] = f.read_text()
    reg = json.loads((BLOCKS / "registry.json").read_text())
    blocks = []
    for cat, _ in BLOCK_CATS:
        for bid, meta in sorted(reg.items()):
            if meta["category"] == cat:
                blocks.append({"id": bid, **meta, "height": TALL.get(bid, HEIGHTS[cat])})
    js_modules = json.loads((UI / "dist/js/manifest.json").read_text())
    wc_modules = json.loads((UI / "dist/wc/manifest.json").read_text())
    ui_modules = json.loads((UI / "dist/ui/manifest.json").read_text())["components"]
    gd = guides(sizes, js_modules, wc_modules)
    data = {"version": VERSION, "cdn": CDN, "sizes": sizes, "components": comps, "guides": gd,
            "blocks": blocks, "blockCats": [{"id": c, "title": t} for c, t in BLOCK_CATS], "featured": FEATURED,
            "charts": charts(), "jsModules": js_modules, "wcModules": wc_modules, "uiModules": ui_modules}
    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    # docs.css: bundle + utilities used by examples/guides (scanned from the data file).
    scan = DOCS / "src/data/.scan.json"
    scan.write_text(data_json)
    entry = DOCS / "src/docs.css"
    entry.write_text('@import "tailwindcss" source(none);\n@import "../../ui/src/auvyx.source.css";\n@source "./data/.scan.json";\n@source "./index.html";\n@source "./create.js";\n@source "./create-preview.html";\n')
    # Minify with esbuild, not Tailwind's --minify (Lightning CSS can drop rules, see packages/ui/build.mjs).
    run(str(ROOT / "node_modules/.bin/tailwindcss"), "-i", str(entry), "-o", str(OUT / "docs.css"))
    run(str(ROOT / "node_modules/.bin/esbuild"), str(OUT / "docs.css"), "--minify", "--target=chrome111,safari16.4,firefox128", f"--outfile={OUT / 'docs.css'}", "--allow-overwrite", "--log-level=warning")

    html = (DOCS / "src/index.html").read_text().replace("/*DATA*/", data_json).replace("/*CREATE*/", (DOCS / "src/create.js").read_text())
    (OUT / "index.html").write_text(html)

    (OUT / "blocks").mkdir()
    shutil.copytree(BLOCKS / "assets", OUT / "blocks" / "assets")
    for f in BLOCKS.glob("*.html"):
        html = f.read_text().replace("../ui/dist/", "../dist/")
        # Opened directly from the docs, a block follows the docs preset and dark mode.
        # Before </head>: after the block's own theme script, so the docs dark mode wins.
        html = html.replace("  </head>", "    " + BLOCK_PRESET + "\n  </head>", 1)
        (OUT / "blocks" / f.name).write_text(html)

    # Create "Icon Library": icons.js swaps inline Lucide icons using icons.json.
    shutil.copy(DOCS / "src/icons.js", OUT / "icons.js")
    run("node", str(DOCS / "tools/icons.mjs"), str(OUT))

    # Public registry served at /r/<name>.json for `auvyx add`.
    run("node", str(BLOCKS / "tools/build_registry.mjs"), "--out", str(OUT / "r"))

    write_llms(gd, comps, blocks)

    files = sorted(p.relative_to(OUT).as_posix() for p in OUT.rglob("*") if p.is_file())
    total = sum((OUT / f).stat().st_size for f in files)
    print(f"docs: {len(comps)} components, {len(blocks)} blocks, {len(data['charts'])} charts; {len(files)} files, {total / 1024:.0f} kB; docs.css {gz(OUT / 'docs.css')}")


main()

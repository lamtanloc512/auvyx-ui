  // ---------------- create (preset builder)
  // Inlined into the docs IIFE by build.py: uses esc, codeBox, ICON, I, $, CDN from the outer scope.
  // Picks a style pack + tokens, previews them in create-preview.html, and exports CSS / a preset code.
  const Create = (() => {
    const N = (l, c = 0, h = 0, a) => `oklch(${+l.toFixed(3)} ${+c.toFixed(3)} ${+h.toFixed(3)}${a ? ` / ${a}` : ''})`;
    // shadcn v4 neutral lightness per token; tinted bases add chroma peaking at mid lightness.
    const LIGHT = { background: 1, foreground: 0.145, card: 1, 'card-foreground': 0.145, popover: 1, 'popover-foreground': 0.145, primary: 0.205, 'primary-foreground': 0.985, secondary: 0.97, 'secondary-foreground': 0.205, muted: 0.97, 'muted-foreground': 0.556, accent: 0.97, 'accent-foreground': 0.205, border: 0.922, input: 0.922, ring: 0.708, sidebar: 0.985, 'sidebar-foreground': 0.145, 'sidebar-primary': 0.205, 'sidebar-primary-foreground': 0.985, 'sidebar-accent': 0.97, 'sidebar-accent-foreground': 0.205, 'sidebar-border': 0.922, 'sidebar-ring': 0.708 };
    const DARK = { background: 0.145, foreground: 0.985, card: 0.205, 'card-foreground': 0.985, popover: 0.205, 'popover-foreground': 0.985, primary: 0.922, 'primary-foreground': 0.205, secondary: 0.269, 'secondary-foreground': 0.985, muted: 0.269, 'muted-foreground': 0.708, accent: 0.269, 'accent-foreground': 0.985, border: [1, '10%'], input: [1, '15%'], ring: 0.556, sidebar: 0.205, 'sidebar-foreground': 0.985, 'sidebar-primary': 0.922, 'sidebar-primary-foreground': 0.205, 'sidebar-accent': 0.269, 'sidebar-accent-foreground': 0.985, 'sidebar-border': [1, '10%'], 'sidebar-ring': 0.556 };
    const BASES = [['Neutral', 0, 0], ['Stone', 0.013, 58], ['Zinc', 0.018, 286], ['Gray', 0.028, 264], ['Slate', 0.046, 257], ['Mauve', 0.03, 320], ['Olive', 0.03, 120]];
    // Tailwind 600 (500 for the light hues, which take a dark foreground).
    const THEMES = [['Default'], ['Red', 0.577, 0.245, 27.3], ['Orange', 0.646, 0.222, 41.1], ['Amber', 0.769, 0.188, 70.1, 1], ['Yellow', 0.795, 0.184, 86, 1], ['Lime', 0.768, 0.233, 130.9, 1], ['Green', 0.627, 0.194, 149.2], ['Emerald', 0.596, 0.145, 163.2], ['Teal', 0.6, 0.118, 184.7], ['Cyan', 0.609, 0.126, 221.7], ['Sky', 0.588, 0.158, 242], ['Blue', 0.546, 0.245, 262.9], ['Indigo', 0.511, 0.262, 277], ['Violet', 0.541, 0.281, 293], ['Purple', 0.558, 0.288, 302.3], ['Fuchsia', 0.591, 0.293, 322.9], ['Pink', 0.592, 0.249, 0.6], ['Rose', 0.586, 0.253, 17.6]];
    const FONTS = [['Geist', 'sans-serif'], ['Inter', 'sans-serif'], ['Figtree', 'sans-serif'], ['Manrope', 'sans-serif'], ['DM Sans', 'sans-serif'], ['Outfit', 'sans-serif'], ['Plus Jakarta Sans', 'sans-serif'], ['Public Sans', 'sans-serif'], ['Noto Sans', 'sans-serif'], ['Nunito Sans', 'sans-serif'], ['IBM Plex Sans', 'sans-serif'], ['Space Grotesk', 'sans-serif'], ['Lora', 'serif'], ['Playfair Display', 'serif'], ['Merriweather', 'serif'], ['JetBrains Mono', 'monospace'], ['System', 'system']];
    const OPTS = {
      style: { label: 'Style', items: ['Vega', 'Nova', 'Maia', 'Lyra', 'Mira', 'Luma', 'Sera', 'Rhea'] },
      base: { label: 'Base Color', items: BASES.map((b) => b[0]) },
      theme: { label: 'Theme', items: THEMES.map((t) => t[0]) },
      chart: { label: 'Chart Color', items: THEMES.map((t) => t[0]) },
      heading: { label: 'Heading', items: ['Inherit', ...FONTS.map((f) => f[0])] },
      font: { label: 'Font', items: FONTS.map((f) => f[0]) },
      radius: { label: 'Radius', items: ['0', '0.3', '0.45', '0.625', '0.75', '1'], fmt: (v) => (v === '0' ? 'None' : v + 'rem') },
      corners: { label: 'Corners', items: ['Round', 'Squircle', 'Smooth', 'Bevel', 'Scoop', 'Notch'] },
      menu: { label: 'Menu', items: ['Default', 'Translucent'] },
      accent: { label: 'Menu Accent', items: ['Subtle', 'Bold'] },
    };
    const KEYS = Object.keys(OPTS);
    const CORNER_CSS = { Round: 'round', Squircle: 'squircle', Smooth: 'superellipse(1.5)', Bevel: 'bevel', Scoop: 'scoop', Notch: 'notch' };
    const DEFAULT = { style: 0, base: 0, theme: 0, chart: 0, heading: 0, font: 0, radius: 3, corners: 1, menu: 0, accent: 0 };
    const STORE = 'auvyx-create';
    let state = { ...DEFAULT, imported: null };
    try { const s = JSON.parse(localStorage.getItem(STORE) || 'null'); if (s) state = { ...state, ...s }; } catch (e) {}

    const pick = (k) => OPTS[k].items[state[k]] ?? OPTS[k].items[0];
    const fmt = (k, v) => (OPTS[k].fmt ? OPTS[k].fmt(v) : v);

    // ---- preset codes: one base36 digit per option
    const encode = () => KEYS.map((k) => state[k].toString(36)).join('');
    function decode(code) {
      const c = String(code).trim().replace(/^--preset\s+/, '').toLowerCase();
      if (!/^[0-9a-z]+$/.test(c) || c.length !== KEYS.length) return null;
      const out = {};
      for (const [n, k] of KEYS.entries()) { const v = parseInt(c[n], 36); if (v >= OPTS[k].items.length) return null; out[k] = v; }
      return out;
    }

    // ---- tokens
    function baseVars(dark) {
      const [, k, h] = BASES[state.base];
      const tint = (l) => (k ? k * 4 * l * (1 - l) : 0);
      const out = {};
      for (const [name, v] of Object.entries(dark ? DARK : LIGHT)) out[name] = Array.isArray(v) ? N(v[0], 0, 0, v[1]) : N(v, tint(v), h);
      out.destructive = dark ? N(0.704, 0.191, 22.216) : N(0.577, 0.245, 27.325);
      return out;
    }
    function themeVars(dark) {
      const t = THEMES[state.theme];
      if (!t[1]) return {};
      const [, l, c, h, darkFg] = t;
      const L = dark && !darkFg ? Math.min(l + 0.08, 0.72) : l;
      const fg = darkFg ? N(0.21, 0.006, h) : N(0.985, 0, 0);
      const p = N(L, c, h);
      return { primary: p, 'primary-foreground': fg, ring: N(L + 0.1, c * 0.55, h), 'sidebar-primary': p, 'sidebar-primary-foreground': fg, 'sidebar-ring': N(L + 0.1, c * 0.55, h) };
    }
    function chartVars(dark) {
      const t = THEMES[state.chart];
      if (!t[1]) return dark
        ? { 'chart-1': N(0.488, 0.243, 264.376), 'chart-2': N(0.696, 0.17, 162.48), 'chart-3': N(0.769, 0.188, 70.08), 'chart-4': N(0.627, 0.265, 303.9), 'chart-5': N(0.645, 0.246, 16.439) }
        : { 'chart-1': N(0.646, 0.222, 41.116), 'chart-2': N(0.6, 0.118, 184.704), 'chart-3': N(0.398, 0.07, 227.392), 'chart-4': N(0.828, 0.189, 84.429), 'chart-5': N(0.769, 0.188, 70.08) };
      const [, , c, h] = t;
      return Object.fromEntries([0.81, 0.71, 0.62, 0.53, 0.45].map((l, n) => [`chart-${n + 1}`, N(l, c * (0.55 + n * 0.1), h)]));
    }
    function fontStack(name) {
      const f = FONTS.find((x) => x[0] === name);
      if (!f || f[1] === 'system') return 'ui-sans-serif, system-ui, sans-serif';
      const tail = { 'sans-serif': 'ui-sans-serif, system-ui, sans-serif', serif: 'ui-serif, Georgia, serif', monospace: 'ui-monospace, monospace' }[f[1]];
      return `"${f[0]}", ${tail}`;
    }
    function tokens() {
      const light = { ...baseVars(false), ...themeVars(false), ...chartVars(false) };
      const dark = { ...baseVars(true), ...themeVars(true), ...chartVars(true) };
      const shared = { radius: pick('radius') + 'rem', 'corner-shape': CORNER_CSS[pick('corners')], 'font-sans': fontStack(pick('font')) };
      if (state.heading) shared['font-heading'] = fontStack(pick('heading'));
      if (state.imported) {
        Object.assign(shared, state.imported.theme);
        Object.assign(light, state.imported.light);
        Object.assign(dark, state.imported.dark);
        // tweakcn puts fonts/radius in :root next to the colors; keep them shared.
        for (const k of Object.keys(light)) if (/^(font-|radius$|tracking-|letter-spacing$|spacing$|shadow)/.test(k)) { shared[k] = light[k]; delete light[k]; }
        for (const k of Object.keys(dark)) if (/^(font-|radius$|tracking-|letter-spacing$|spacing$)/.test(k)) delete dark[k];
      }
      return { shared, light, dark };
    }
    function css() {
      const { shared, light, dark } = tokens();
      const block = (sel, vars) => `${sel} {\n${Object.entries(vars).map(([k, v]) => `  --${k}: ${v};`).join('\n')}\n}`;
      const out = [block(':root', { ...shared, ...light }), block('.dark', dark)];
      out.push('body {\n  font-family: var(--font-sans);\n}');
      if (shared['font-heading']) out.push('h1, h2, h3, h4, h5, h6 {\n  font-family: var(--font-heading);\n}');
      if (state.menu === 1) out.push(':is([data-popover], .command-dialog > .command) {\n  background-color: color-mix(in oklab, var(--popover) 78%, transparent);\n  backdrop-filter: blur(16px) saturate(1.6);\n}');
      if (state.accent === 1) out.push(':is([data-popover], .command, [role="listbox"]) {\n  --accent: var(--primary);\n  --accent-foreground: var(--primary-foreground);\n}');
      return out.join('\n\n');
    }
    const SYSTEM = /^(ui-|system-ui|-apple-system|sans-serif|serif|monospace|BlinkMacSystemFont|Segoe UI|Helvetica|Arial|Georgia|Times|Courier|Menlo|Consolas|SFMono)/i;
    function fontFamilies() {
      const { shared } = tokens();
      const names = new Set();
      for (const k of ['font-sans', 'font-heading', 'font-serif', 'font-mono']) {
        const first = (shared[k] || '').split(',')[0].trim().replace(/^["']|["']$/g, '');
        if (first && !SYSTEM.test(first)) names.add(first);
      }
      return [...names];
    }
    function fontsHref() {
      const f = fontFamilies();
      return f.length ? `https://fonts.googleapis.com/css2?${f.map((n) => `family=${n.replace(/ /g, '+')}:wght@400;500;600;700`).join('&')}&display=swap` : '';
    }
    const styleFile = () => `auvyx-${pick('style').toLowerCase()}.min.css`;
    function headSnippet() {
      const lines = [];
      const fh = fontsHref();
      if (fh) lines.push('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>', `<link rel="stylesheet" href="${fh.replace(/&/g, '&amp;')}">`);
      lines.push(`<link rel="stylesheet" href="${CDN}/styles/${styleFile()}">`);
      lines.push('<style>', css().replace(/^/gm, '  '), '</style>');
      lines.push(`<script src="${CDN}/auvyx.min.js" defer><\/script>`);
      if (tokens().shared['corner-shape'] !== 'round') lines.push(`<!-- corner-shape is native in Chrome 139+; Monoco draws it elsewhere -->`, `<script src="${CDN}/auvyx.corners.min.js" defer><\/script>`);
      return lines.join('\n');
    }

    // ---- tweakcn / shadcn theme import (CSS or registry JSON)
    function parseVars(body) {
      const out = {};
      for (const m of body.matchAll(/--([\w-]+)\s*:\s*([^;]+);?/g)) out[m[1]] = m[2].trim();
      return out;
    }
    function parseTheme(text) {
      const src = String(text).trim();
      if (!src) throw new Error('Paste a theme first.');
      if (src.startsWith('{')) {
        const j = JSON.parse(src);
        const v = j.cssVars || j;
        if (!v.light && !v.dark) throw new Error('JSON has no cssVars.light / cssVars.dark.');
        return { name: j.name || j.title || 'Imported', theme: v.theme || {}, light: v.light || {}, dark: v.dark || {} };
      }
      const clean = src.replace(/\/\*[\s\S]*?\*\//g, '');
      const blocks = { light: {}, dark: {}, theme: {} };
      for (const m of clean.matchAll(/([^{}]+)\{([^{}]*)\}/g)) {
        const sel = m[1].trim();
        if (/@theme/.test(sel)) continue; // Tailwind @theme inline mapping, not values
        if (/\.dark|\[data-theme=["']?dark/.test(sel)) Object.assign(blocks.dark, parseVars(m[2]));
        else if (/:root|html|\[data-theme/.test(sel)) Object.assign(blocks.light, parseVars(m[2]));
      }
      if (!Object.keys(blocks.light).length && !Object.keys(blocks.dark).length) {
        const loose = parseVars(clean); // bare "--x: y;" lines
        if (!Object.keys(loose).length) throw new Error('No CSS variables found. Copy the CSS from tweakcn\'s Code panel.');
        blocks.light = loose;
      }
      return { name: 'Imported', ...blocks };
    }

    // ---- UI
    const CHECK = '<path d="M20 6 9 17l-5-5"/>';
    const SHUFFLE = '<path d="m18 14 4 4-4 4"/><path d="m18 2 4 4-4 4"/><path d="M2 18h1.973a4 4 0 0 0 3.3-1.7l5.454-8.6a4 4 0 0 1 3.3-1.7H22"/><path d="M2 6h1.972a4 4 0 0 1 3.6 2.2"/><path d="M22 18h-6.041a4 4 0 0 1-3.3-1.8l-.359-.45"/>';
    const UPLOAD = '<path d="M12 3v12"/><path d="m17 8-5-5-5 5"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>';
    const swatch = (k, v) => {
      if (k === 'theme' || k === 'chart') { const t = THEMES[OPTS[k].items.indexOf(v)]; return `<span class="d-sw" style="background:${t[1] ? N(t[1], t[2], t[3]) : 'var(--foreground)'}"></span>`; }
      if (k === 'base') { const b = BASES[OPTS.base.items.indexOf(v)]; return `<span class="d-sw" style="background:${N(0.55, b[1] * 2.2, b[2])}"></span>`; }
      if (k === 'font' || k === 'heading') return `<span class="d-sw-font" style="font-family:${v === 'Inherit' ? 'inherit' : fontStack(v)}">Aa</span>`;
      return '';
    };
    const ROW_ICON = {
      style: '<rect width="18" height="18" x="3" y="3" rx="2"/>',
      radius: '<path d="M4 20V10a6 6 0 0 1 6-6h10"/>',
      corners: '<path d="M4 20v-9l7-7h9"/>',
      menu: '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
      accent: '<path d="m19 11-8-8-8.6 8.6a2 2 0 0 0 0 2.8l5.2 5.2c.8.8 2 .8 2.8 0L19 11Z"/><path d="m5 2 5 5"/><path d="M2 13h15"/><path d="M22 20a2 2 0 1 1-4 0c0-1.6 1.7-2.4 2-4 .3 1.6 2 2.4 2 4Z"/>',
    };
    function row(k) {
      const o = OPTS[k];
      const v = pick(k);
      const items = o.items.map((it, n) => `<button type="button" role="menuitemradio" aria-checked="${n === state[k]}" data-opt="${k}" data-val="${n}" popovertarget="cr-${k}" popovertargetaction="hide">${swatch(k, it)}<span>${esc(fmt(k, it))}</span>${n === state[k] ? ICON(CHECK, '0.875rem') : ''}</button>`).join('');
      const locked = state.imported && /^(base|theme|font|heading|radius)$/.test(k) && hasImported(k);
      return `<div class="dropdown-menu d-cr-row">
        <button type="button" class="d-cr-btn" popovertarget="cr-${k}" aria-haspopup="menu"${locked ? ' data-locked' : ''}>
          <span class="d-cr-text"><span class="d-cr-label">${esc(o.label)}</span><span class="d-cr-val">${esc(locked ? 'From import' : fmt(k, v))}</span></span>
          <span class="d-cr-icon">${swatch(k, v) || ICON(ROW_ICON[k])}</span>
        </button>
        <div id="cr-${k}" data-popover popover data-side="bottom" data-align="start" class="d-cr-pop"><div role="menu" aria-label="${esc(o.label)}">${items}</div></div>
      </div>`;
    }
    function hasImported(k) {
      const all = { ...state.imported.theme, ...state.imported.light };
      return { base: 'background', theme: 'primary', font: 'font-sans', heading: 'font-sans', radius: 'radius' }[k] in all;
    }
    function panel() {
      const imp = state.imported ? `<div class="d-cr-import"><span>${ICON(UPLOAD, '0.875rem')} ${esc(state.imported.name)} theme</span><button type="button" class="btn" data-variant="ghost" data-size="sm" data-cr="clear-import">Clear</button></div>` : '';
      return `${imp}<div class="d-cr-rows">${KEYS.map(row).join('')}</div>
        <button type="button" class="btn d-cr-wide" data-variant="outline" commandfor="cr-import" command="show-modal">${ICON(UPLOAD)}Import tweakcn theme</button>
        <div class="d-cr-preset"><code>--preset ${encode()}</code><button type="button" class="btn d-copy" data-variant="ghost" data-size="icon-sm" aria-label="Copy preset" data-text="--preset ${encode()}">${ICON(I.copy)}</button></div>
        <div class="d-cr-actions">
          <button type="button" class="btn" data-variant="outline" commandfor="cr-open" command="show-modal">Open Preset</button>
          <button type="button" class="btn" data-variant="outline" data-cr="shuffle">${ICON(SHUFFLE)}Shuffle</button>
          <button type="button" class="btn" data-variant="outline" data-cr="reset">Reset</button>
          <button type="button" class="btn" data-variant="outline" commandfor="cr-css" command="show-modal" data-cr="show-css">Copy CSS</button>
        </div>
        <button type="button" class="btn d-cr-wide" commandfor="cr-init" command="show-modal" data-cr="show-init">Initialize Project</button>`;
    }
    const dlg = (id, title, desc, body, foot = '') => `<dialog id="${id}" class="dialog d-cr-dialog" closedby="any" aria-labelledby="${id}-t"><div><header><h2 id="${id}-t">${title}</h2><p>${desc}</p></header><section>${body}</section><footer>${foot}<button type="button" class="btn" data-variant="outline" commandfor="${id}" command="close">Close</button></footer></div></dialog>`;
    function page() {
      return `<div class="d-create">
        <aside class="d-cr-panel dark" id="cr-panel" aria-label="Preset options">${panel()}</aside>
        <div class="d-cr-stage"><iframe id="cr-frame" title="Theme preview" src="create-preview.html"></iframe></div>
      </div>
      ${dlg('cr-open', 'Open Preset', 'Paste a preset code to load its options.', `<input class="input" id="cr-code" placeholder="--preset 0000003100" autocomplete="off" spellcheck="false" aria-label="Preset code"><p class="d-cr-err" id="cr-code-err" hidden>That code is not valid.</p>`, '<button type="button" class="btn" data-cr="open">Open</button>')}
      ${dlg('cr-import', 'Import theme', 'Paste the CSS from tweakcn.com (Code → CSS, the <code>:root</code> and <code>.dark</code> blocks) or a shadcn registry JSON. Colors, fonts, radius, shadows, tracking and spacing apply.', `<textarea class="textarea d-cr-ta" id="cr-theme-src" rows="10" spellcheck="false" placeholder=":root {&#10;  --background: oklch(1 0 0);&#10;  --primary: oklch(0.62 0.19 260);&#10;  …&#10;}&#10;.dark { … }" aria-label="Theme CSS or JSON"></textarea><p class="d-cr-err" id="cr-theme-err" hidden></p>`, '<button type="button" class="btn" data-cr="import">Apply theme</button>')}
      ${dlg('cr-css', 'Theme CSS', 'Paste after the Auvyx stylesheet.', '<div id="cr-css-body"></div>')}
      ${dlg('cr-init', 'Initialize Project', 'Put this in your <code>&lt;head&gt;</code>. Everything is CDN-hosted; no build step.', '<div id="cr-init-body"></div>')}`;
    }

    let frame, mounted = false;
    function save() { try { localStorage.setItem(STORE, JSON.stringify(state)); } catch (e) {} }
    // The preset themes the whole docs app (chrome, component demos, block frames), like shadcn's /create.
    function headTag(doc, id, tag) {
      let el = doc.getElementById(id);
      if (!el) { el = doc.createElement(tag); el.id = id; if (tag === 'link') el.rel = 'stylesheet'; doc.head.append(el); }
      return el;
    }
    function setHref(el, href) { if (href) { if (el.getAttribute('href') !== href) el.setAttribute('href', href); } else el.removeAttribute('href'); }
    // docs.css and auvyx.min.css are the Vega bundle; other styles load their own bundle on top.
    const stylePack = (prefix) => (state.style ? `${prefix}dist/styles/${styleFile()}` : '');
    function syncSite() {
      setHref(headTag(document, 'd-cr-site-style', 'link'), stylePack(''));
      setHref(headTag(document, 'd-cr-site-fonts', 'link'), fontsHref());
      headTag(document, 'd-cr-site', 'style').textContent = css();
    }
    function syncBlock(doc) {
      if (!doc?.head) return;
      setHref(headTag(doc, 'd-cr-style', 'link'), stylePack('../'));
      setHref(headTag(doc, 'd-cr-fonts', 'link'), fontsHref());
      headTag(doc, 'd-cr-theme', 'style').textContent = css();
    }
    function sync() {
      syncSite();
      const doc = frame?.contentDocument;
      if (!doc || !doc.getElementById('sc-theme')) return;
      doc.getElementById('sc-theme').textContent = css();
      const st = doc.getElementById('sc-style');
      const href = `dist/styles/${styleFile()}`;
      if (!st.getAttribute('href').endsWith(href)) st.setAttribute('href', href);
      const fl = doc.getElementById('sc-fonts');
      const fh = fontsHref();
      if (fl.getAttribute('href') !== fh) { if (fh) fl.setAttribute('href', fh); else fl.removeAttribute('href'); }
      doc.documentElement.classList.toggle('dark', document.documentElement.classList.contains('dark'));
      frame.contentWindow.auvyxCorners?.apply();
    }
    function refresh() {
      save();
      const p = $('#cr-panel');
      if (p) p.innerHTML = panel();
      applyTheme(); // re-syncs this page, block frames and charts
    }
    function mount() {
      frame = $('#cr-frame');
      if (!frame) return;
      frame.addEventListener('load', sync);
      sync();
      if (mounted) return;
      mounted = true;
      document.addEventListener('click', (e) => {
        if (!$('#cr-panel')) return;
        const opt = e.target.closest('[data-opt]');
        if (opt) { state[opt.dataset.opt] = +opt.dataset.val; refresh(); return; }
        const a = e.target.closest('[data-cr]');
        if (!a) return;
        const act = a.dataset.cr;
        if (act === 'shuffle') { for (const k of KEYS) if (k !== 'menu' && k !== 'accent') state[k] = Math.floor(Math.random() * OPTS[k].items.length); state.heading = Math.random() < 0.6 ? 0 : state.heading; refresh(); }
        else if (act === 'reset') { state = { ...DEFAULT, imported: null }; refresh(); }
        else if (act === 'clear-import') { state.imported = null; refresh(); }
        else if (act === 'show-css') $('#cr-css-body').innerHTML = codeBox(css(), 'theme.css');
        else if (act === 'show-init') $('#cr-init-body').innerHTML = codeBox(headSnippet(), 'index.html');
        else if (act === 'open') {
          const v = decode($('#cr-code').value);
          $('#cr-code-err').hidden = !!v;
          if (v) { Object.assign(state, v); $('#cr-open').close(); refresh(); }
        } else if (act === 'import') {
          const err = $('#cr-theme-err');
          try { state.imported = parseTheme($('#cr-theme-src').value); err.hidden = true; $('#cr-import').close(); refresh(); }
          catch (x) { err.textContent = x.message; err.hidden = false; }
        }
      });
    }
    return { page, mount, sync, syncBlock, parseTheme, css, encode, decode, get state() { return state; } };
  })();
  window.auvyxCreate = Create;

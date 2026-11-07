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
    // Label -> icons.js set key. Inline icons are Lucide; icons.js swaps the others in.
    const ICON_LIBS = [['Lucide', 'lucide'], ['Tabler', 'tabler'], ['HugeIcons', 'hugeicons'], ['Phosphor', 'ph'], ['Remix', 'ri']];
    // ---- theme presets: complete light + dark themes (colors, font, radius, shadows), like tweakcn's.
    // shadowVars builds the --shadow-* scale from one shadow, as tweakcn's editor does.
    function shadowVars({ color = '0 0% 0%', opacity = 0.1, blur = 3, spread = 0, x = 0, y = 1 }) {
      const c = (o) => `hsl(${color} / ${+Math.min(o, 1).toFixed(2)})`;
      const s1 = `${x}px ${y}px ${blur}px ${spread}px`;
      const two = (y2, b2) => `${s1} ${c(opacity)}, ${x}px ${y2}px ${b2}px ${spread - 1}px ${c(opacity)}`;
      return {
        'shadow-2xs': `${s1} ${c(opacity / 2)}`, 'shadow-xs': `${s1} ${c(opacity / 2)}`,
        'shadow-sm': two(1, 2), shadow: two(1, 2), 'shadow-md': two(2, 4), 'shadow-lg': two(4, 6), 'shadow-xl': two(8, 10),
        'shadow-2xl': `${s1} ${c(opacity * 2.5)}`,
      };
    }
    // One spec -> a full shadcn token set for light and dark.
    // t: neutral tint chroma, h: neutral hue, p: [l, c, h] primary, a: accent hue, ch: chart hues.
    function preset(name, { t = 0.01, h, p, a, ch, radius = '0.625rem', font = 'Inter', heading, shadow = {}, accent, mono }) {
      const [pl, pc, ph] = p;
      const darkText = pl > 0.72;
      const light = {
        background: N(0.99, t * 0.4, h), foreground: N(0.2, t * 2, h),
        card: N(1, 0, 0), 'card-foreground': N(0.2, t * 2, h),
        popover: N(1, 0, 0), 'popover-foreground': N(0.2, t * 2, h),
        primary: N(pl, pc, ph), 'primary-foreground': darkText ? N(0.2, Math.min(pc, 0.06), ph) : N(0.985, 0.01, ph),
        secondary: N(0.955, Math.min(0.02 + t, pc * 0.3), ph), 'secondary-foreground': N(0.3, Math.min(pc, 0.08), ph),
        muted: N(0.96, t, h), 'muted-foreground': N(0.5, t * 2.5, h),
        accent: accent ? N(...accent[0]) : N(0.945, 0.035, a), 'accent-foreground': accent ? N(...accent[1]) : N(0.32, 0.08, a),
        destructive: N(0.577, 0.245, 27.3),
        border: N(0.905, t * 1.5, h), input: N(0.905, t * 1.5, h), ring: N(Math.min(pl + 0.08, 0.8), pc * 0.7, ph),
        sidebar: N(0.975, t * 0.8, h), 'sidebar-foreground': N(0.2, t * 2, h),
        'sidebar-primary': N(pl, pc, ph), 'sidebar-primary-foreground': darkText ? N(0.2, Math.min(pc, 0.06), ph) : N(0.985, 0.01, ph),
        'sidebar-accent': N(0.94, 0.03, a), 'sidebar-accent-foreground': N(0.32, 0.08, a),
        'sidebar-border': N(0.905, t * 1.5, h), 'sidebar-ring': N(Math.min(pl + 0.08, 0.8), pc * 0.7, ph),
      };
      // Neutral primaries flip to near-white in dark mode, as in shadcn's neutral theme.
      const dl = pc < 0.03 ? 0.92 : Math.max(pl, 0.7), dc = pc * 0.95;
      const dark = {
        background: N(0.16, t * 1.6 + 0.004, h), foreground: N(0.965, t * 0.6, h),
        card: N(0.2, t * 1.8 + 0.004, h), 'card-foreground': N(0.965, t * 0.6, h),
        popover: N(0.2, t * 1.8 + 0.004, h), 'popover-foreground': N(0.965, t * 0.6, h),
        primary: N(dl, dc, ph), 'primary-foreground': N(0.18, Math.min(pc, 0.05), ph),
        secondary: N(0.28, Math.min(0.03 + t, pc * 0.35), ph), 'secondary-foreground': N(0.96, 0.01, ph),
        muted: N(0.26, t * 1.6 + 0.004, h), 'muted-foreground': N(0.72, t * 1.5, h),
        accent: accent ? N(...accent[2]) : N(0.3, 0.05, a), 'accent-foreground': accent ? N(...accent[3]) : N(0.95, 0.03, a),
        destructive: N(0.704, 0.191, 22.2),
        border: N(1, 0, 0, '10%'), input: N(1, 0, 0, '15%'), ring: N(dl - 0.1, dc * 0.7, ph),
        sidebar: N(0.19, t * 1.8 + 0.004, h), 'sidebar-foreground': N(0.965, t * 0.6, h),
        'sidebar-primary': N(dl, dc, ph), 'sidebar-primary-foreground': N(0.18, Math.min(pc, 0.05), ph),
        'sidebar-accent': N(0.28, 0.04, a), 'sidebar-accent-foreground': N(0.95, 0.03, a),
        'sidebar-border': N(1, 0, 0, '10%'), 'sidebar-ring': N(dl - 0.1, dc * 0.7, ph),
      };
      ch.forEach((hh, n) => { light[`chart-${n + 1}`] = N(0.72 - n * 0.06, 0.15, hh); dark[`chart-${n + 1}`] = N(0.76 - n * 0.05, 0.14, hh); });
      const stack = (f, tail) => `"${f}", ${tail}`;
      const theme = {
        radius, 'font-sans': mono ? stack(font, 'ui-monospace, monospace') : stack(font, 'ui-sans-serif, system-ui, sans-serif'),
        ...(heading && { 'font-heading': stack(heading, 'ui-serif, Georgia, serif') }),
        ...shadowVars(shadow),
      };
      return { name, theme, light, dark, shadow: { color: '0 0% 0%', opacity: 0.1, blur: 3, spread: 0, x: 0, y: 1, ...shadow } };
    }
    const PRESETS = [
      preset('Ocean', { t: 0.012, h: 235, p: [0.55, 0.16, 245], a: 200, ch: [245, 200, 175, 265, 220], radius: '0.75rem', font: 'Inter', shadow: { opacity: 0.08, blur: 6, y: 2 } }),
      preset('Sunset', { t: 0.012, h: 45, p: [0.565, 0.19, 36], a: 75, ch: [38, 60, 15, 80, 350], radius: '0.75rem', font: 'Outfit', shadow: { color: '20 60% 30%', opacity: 0.1, blur: 8, y: 3 } }),
      preset('Forest', { t: 0.012, h: 140, p: [0.52, 0.13, 152], a: 115, ch: [152, 130, 175, 95, 200], radius: '0.5rem', font: 'Figtree' }),
      preset('Lavender', { t: 0.016, h: 300, p: [0.54, 0.13, 300], a: 350, ch: [300, 330, 270, 355, 240], radius: '1rem', font: 'Plus Jakarta Sans', shadow: { opacity: 0.06, blur: 10, y: 3, spread: 1 } }),
      preset('Midnight', { t: 0.022, h: 275, p: [0.55, 0.22, 278], a: 220, ch: [278, 220, 320, 190, 250], radius: '0.625rem', font: 'Space Grotesk', shadow: { color: '260 60% 10%', opacity: 0.18, blur: 12, y: 4 } }),
      preset('Brutalist', { t: 0, h: 0, p: [0.2, 0, 0], a: 100, ch: [100, 25, 250, 145, 330], radius: '0rem', font: 'JetBrains Mono', mono: true, accent: [[0.93, 0.17, 105], [0.25, 0.05, 105], [0.88, 0.17, 105], [0.2, 0.04, 105]], shadow: { opacity: 1, blur: 0, x: 4, y: 4 } }),
      preset('Rose', { t: 0.01, h: 10, p: [0.56, 0.2, 8], a: 35, ch: [8, 35, 340, 60, 315], radius: '0.75rem', font: 'DM Sans' }),
      preset('Amber', { t: 0.014, h: 75, p: [0.77, 0.165, 70], a: 45, ch: [70, 45, 95, 25, 120], radius: '0.5rem', font: 'Manrope' }),
      preset('Frost', { t: 0.02, h: 250, p: [0.52, 0.1, 235], a: 200, ch: [232, 200, 260, 180, 290], radius: '0.45rem', font: 'IBM Plex Sans', shadow: { color: '220 40% 30%', opacity: 0.08, blur: 4, y: 1 } }),
      preset('Espresso', { t: 0.02, h: 55, p: [0.47, 0.075, 50], a: 75, ch: [50, 75, 30, 95, 15], radius: '0.625rem', font: 'Lora', heading: 'Playfair Display', shadow: { color: '25 40% 20%', opacity: 0.12, blur: 6, y: 2 } }),
      preset('Citrus', { t: 0.012, h: 115, p: [0.8, 0.19, 128], a: 95, ch: [128, 95, 160, 70, 190], radius: '1rem', font: 'Nunito Sans' }),
      preset('Graphite', { t: 0.006, h: 260, p: [0.3, 0.02, 260], a: 260, ch: [260, 220, 290, 200, 240], radius: '0.3rem', font: 'Geist', shadow: { opacity: 0.05, blur: 2, y: 1 } }),
    ];
    const OPTS = {
      style: { label: 'Style', items: ['Vega', 'Nova', 'Maia', 'Lyra', 'Mira', 'Luma', 'Sera', 'Rhea'] },
      base: { label: 'Base Color', items: BASES.map((b) => b[0]) },
      theme: { label: 'Theme', items: THEMES.map((t) => t[0]) },
      chart: { label: 'Chart Color', items: THEMES.map((t) => t[0]) },
      heading: { label: 'Heading', items: ['Inherit', ...FONTS.map((f) => f[0])] },
      font: { label: 'Font', items: FONTS.map((f) => f[0]) },
      icons: { label: 'Icon Library', items: ICON_LIBS.map((l) => l[0]) },
      radius: { label: 'Radius', items: ['0', '0.3', '0.45', '0.625', '0.75', '1'], fmt: (v) => (v === '0' ? 'None' : v + 'rem') },
      corners: { label: 'Corners', items: ['Round', 'Squircle', 'Smooth', 'Bevel', 'Scoop', 'Notch'] },
      menu: { label: 'Menu', items: ['Default', 'Translucent'] },
      accent: { label: 'Menu Accent', items: ['Subtle', 'Bold'] },
    };
    const KEYS = Object.keys(OPTS);
    const CORNER_CSS = { Round: 'round', Squircle: 'squircle', Smooth: 'superellipse(1.5)', Bevel: 'bevel', Scoop: 'scoop', Notch: 'notch' };
    const DEFAULT = { style: 0, base: 0, theme: 0, chart: 0, heading: 0, font: 1, icons: 0, radius: 3, corners: 1, menu: 0, accent: 0, smoothing: 1, fontSize: 16, fontWeight: 0 };
    // Corner smoothing (0–1) for Squircle and Smooth corners. Native: superellipse(1 + s)
    // for Squircle (1 is squircle, the default) and superellipse(1 + s/2) for Smooth;
    // Monoco reads --corner-smoothing. Kept out of the preset code (like the editor).
    const SMOOTH = { Squircle: 1, Smooth: 0.5 };
    // Font size: the base text size in px (16 is the default). Scales every --text-* token
    // the components use, so spacing and radius stay as they are.
    const TEXT = { xs: 0.75, sm: 0.875, base: 1, lg: 1.125, xl: 1.25, '2xl': 1.5, '3xl': 1.875, '4xl': 2.25 };
    const textScale = () => (state.fontSize ?? 16) / 16;
    // Font weight: components read --font-weight-normal|medium|semibold|bold. The panel
    // slider shifts all four; the editor sets each one. Google Fonts serves each family's
    // whole weight axis (WEIGHT_AXIS), so any weight in range renders with real glyphs.
    const WEIGHTS = { normal: 400, medium: 500, semibold: 600, bold: 700 };
    const WEIGHT_AXIS = { Geist: '100..900', Inter: '100..900', 'IBM Plex Sans': '100..700', 'Space Grotesk': '300..700', Lora: '400..700', 'Playfair Display': '400..900', Merriweather: '300..900', 'JetBrains Mono': '100..800' };
    const weightAxis = (name) => WEIGHT_AXIS[name] || (FONTS.some(([f]) => f === name) ? '300..800' : '400;500;600;700');
    const clampWeight = (w) => Math.min(900, Math.max(100, Math.round(w / 50) * 50));
    // Locks: a locked option keeps its value when a theme preset or an imported
    // theme is applied, and Shuffle, Reset and Open Preset leave it alone.
    const THEME_KEYS = ['primary', 'primary-foreground', 'ring', 'sidebar-primary', 'sidebar-primary-foreground', 'sidebar-ring'];
    const isLocked = (k) => !!state.locks?.[k];
    const LOCK = '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>';
    const UNLOCK = '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/>';
    const STORE = 'auvyx-create';
    let state = { ...DEFAULT, imported: null };
    try { const s = JSON.parse(localStorage.getItem(STORE) || 'null'); if (s) state = { ...state, ...s }; } catch (e) {}

    const iconLib = () => ICON_LIBS[state.icons]?.[1] || 'lucide';
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
      const shared = { radius: boxy() ? '0' : pick('radius') + 'rem', 'corner-shape': CORNER_CSS[pick('corners')], 'font-sans': fontStack(pick('font')) };
      if (state.fontWeight) for (const [k, w] of Object.entries(WEIGHTS)) shared[`font-weight-${k}`] = String(clampWeight(w + state.fontWeight));
      if (state.heading) shared['font-heading'] = fontStack(pick('heading'));
      if (state.imported) {
        Object.assign(shared, state.imported.theme);
        Object.assign(light, state.imported.light);
        Object.assign(dark, state.imported.dark);
        // tweakcn puts fonts/radius in :root next to the colors; keep them shared.
        for (const k of Object.keys(light)) if (/^(font-|radius$|tracking-|letter-spacing$|spacing$|shadow)/.test(k)) { shared[k] = light[k]; delete light[k]; }
        for (const k of Object.keys(dark)) if (/^(font-|radius$|tracking-|letter-spacing$|spacing$)/.test(k)) delete dark[k];
        if (boxy()) shared.radius = '0';
        // Locked options keep the user's choice over the imported theme.
        const L = state.locks || {};
        const keep = (vars, from, keys) => { for (const k of keys) if (from[k] !== undefined) vars[k] = from[k]; };
        if (L.base) {
          Object.assign(light, baseVars(false));
          Object.assign(dark, baseVars(true));
          if (!L.theme) { keep(light, state.imported.light || {}, THEME_KEYS); keep(dark, state.imported.dark || {}, THEME_KEYS); }
        }
        if (L.theme) {
          keep(light, { ...baseVars(false), ...themeVars(false) }, THEME_KEYS);
          keep(dark, { ...baseVars(true), ...themeVars(true) }, THEME_KEYS);
        }
        if (L.chart) { Object.assign(light, chartVars(false)); Object.assign(dark, chartVars(true)); }
        if (L.font) shared['font-sans'] = fontStack(pick('font'));
        if (L.heading) { if (state.heading) shared['font-heading'] = fontStack(pick('heading')); else delete shared['font-heading']; }
        if (L.radius) shared.radius = boxy() ? '0' : pick('radius') + 'rem';
      }
      const s = state.smoothing ?? 1;
      const f = SMOOTH[pick('corners')];
      if (f && s !== 1) {
        shared['corner-shape'] = `superellipse(${+(1 + s * f).toFixed(3)})`;
        shared['corner-smoothing'] = s;
      }
      if (textScale() !== 1) for (const [k, v] of Object.entries(TEXT)) shared[`text-${k}`] = `${+(v * textScale()).toFixed(4)}rem`;
      return { shared, light, dark };
    }
    function css() {
      const { shared, light, dark } = tokens();
      const block = (sel, vars) => `${sel} {\n${Object.entries(vars).map(([k, v]) => `  --${k}: ${v};`).join('\n')}\n}`;
      const out = [block(':root', { ...shared, ...light }), block('.dark', dark)];
      const bodyWeight = shared['font-weight-normal'] && shared['font-weight-normal'] !== '400' ? '\n  font-weight: var(--font-weight-normal);' : '';
      out.push(`body {\n  font-family: var(--font-sans);${textScale() !== 1 ? '\n  font-size: var(--text-base);' : ''}${bodyWeight}\n}`);
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
      return f.length ? `https://fonts.googleapis.com/css2?${f.map((n) => `family=${n.replace(/ /g, '+')}:wght@${weightAxis(n)}`).join('&')}&display=swap` : '';
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

    // Blocks come from the registry with the chosen icon library already inlined.
    const cliSnippet = () => `npx @auvyx/cli init --icons ${iconLib()}\nnpx @auvyx/cli add dashboard-01`;

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

    // ---- editor helpers: any CSS color -> #rrggbb (via canvas), #rrggbb -> oklch() / hsl channels
    let ctx2d;
    function toHex(v) {
      ctx2d ??= document.createElement('canvas').getContext('2d', { willReadFrequently: true });
      ctx2d.clearRect(0, 0, 1, 1);
      ctx2d.fillStyle = '#000';
      ctx2d.fillStyle = v;
      ctx2d.fillRect(0, 0, 1, 1);
      const [r, g, b] = ctx2d.getImageData(0, 0, 1, 1).data;
      return '#' + [r, g, b].map((n) => n.toString(16).padStart(2, '0')).join('');
    }
    const rgb = (hex) => [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255);
    function hexToOklch(hex) {
      const [r, g, b] = rgb(hex).map((c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
      const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
      const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
      const q = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
      const L = 0.2104542553 * l + 0.793617785 * m - 0.0040720468 * q;
      const A = 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * q;
      const B = 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * q;
      const C = Math.hypot(A, B);
      return N(L, C, C < 0.0005 ? 0 : (Math.atan2(B, A) * 180 / Math.PI + 360) % 360);
    }
    function hexToHsl(hex) {
      const [r, g, b] = rgb(hex);
      const max = Math.max(r, g, b), min = Math.min(r, g, b), l = (max + min) / 2, d = max - min;
      const sat = d ? d / (1 - Math.abs(2 * l - 1)) : 0;
      const h = !d ? 0 : max === r ? ((g - b) / d + 6) % 6 : max === g ? (b - r) / d + 2 : (r - g) / d + 4;
      return `${Math.round(h * 60)} ${Math.round(sat * 100)}% ${Math.round(l * 100)}%`;
    }
    const TOKEN_GROUPS = [
      ['Primary', ['primary', 'primary-foreground']],
      ['Secondary', ['secondary', 'secondary-foreground']],
      ['Accent', ['accent', 'accent-foreground']],
      ['Base', ['background', 'foreground']],
      ['Card', ['card', 'card-foreground']],
      ['Popover', ['popover', 'popover-foreground']],
      ['Muted', ['muted', 'muted-foreground']],
      ['Destructive', ['destructive']],
      ['Border & input', ['border', 'input', 'ring']],
      ['Chart', ['chart-1', 'chart-2', 'chart-3', 'chart-4', 'chart-5']],
      ['Sidebar', ['sidebar', 'sidebar-foreground', 'sidebar-primary', 'sidebar-primary-foreground', 'sidebar-accent', 'sidebar-accent-foreground', 'sidebar-border', 'sidebar-ring']],
    ];
    const DEFAULT_SHADOW = { color: '0 0% 0%', opacity: 0.1, blur: 3, spread: 0, x: 0, y: 1 };
    let view = 'options', shownMode = null;
    const modeNow = () => (isDark() ? 'dark' : 'light');
    // Edits go into the imported/preset theme; without one they start a Custom theme.
    function custom() {
      state.imported ??= { name: 'Custom', theme: {}, light: {}, dark: {} };
      state.imported.edited = true;
      return state.imported;
    }

    // ---- UI
    const CHECK = '<path d="M20 6 9 17l-5-5"/>';
    const SHUFFLE = '<path d="m18 14 4 4-4 4"/><path d="m18 2 4 4-4 4"/><path d="M2 18h1.973a4 4 0 0 0 3.3-1.7l5.454-8.6a4 4 0 0 1 3.3-1.7H22"/><path d="M2 6h1.972a4 4 0 0 1 3.6 2.2"/><path d="M22 18h-6.041a4 4 0 0 1-3.3-1.8l-.359-.45"/>';
    const SLIDERS = '<path d="M20 7h-9"/><path d="M14 17H5"/><circle cx="17" cy="17" r="3"/><circle cx="7" cy="7" r="3"/>';
    const BACK = '<path d="m15 18-6-6 6-6"/>';
    const CHEVRON = '<path d="m9 18 6-6-6-6"/>';
    const UPLOAD = '<path d="M12 3v12"/><path d="m17 8-5-5-5 5"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>';
    const swatch = (k, v) => {
      if (k === 'theme' || k === 'chart') { const t = THEMES[OPTS[k].items.indexOf(v)]; return `<span class="d-sw" style="background:${t[1] ? N(t[1], t[2], t[3]) : 'var(--foreground)'}"></span>`; }
      if (k === 'base') { const b = BASES[OPTS.base.items.indexOf(v)]; return `<span class="d-sw" style="background:${N(0.55, b[1] * 2.2, b[2])}"></span>`; }
      if (k === 'font' || k === 'heading') return `<span class="d-sw-font" style="font-family:${v === 'Inherit' ? 'inherit' : fontStack(v)}">Aa</span>`;
      return '';
    };
    const ROW_ICON = {
      style: '<rect width="18" height="18" x="3" y="3" rx="2"/>',
      icons: '<path d="M8.3 10a.7.7 0 0 1-.626-1.079L11.4 3a.7.7 0 0 1 1.198-.043L16.3 8.9a.7.7 0 0 1-.572 1.1Z"/><rect x="3" y="14" width="7" height="7" rx="1"/><circle cx="17.5" cy="17.5" r="3.5"/>',
      radius: '<path d="M4 20V10a6 6 0 0 1 6-6h10"/>',
      corners: '<path d="M4 20v-9l7-7h9"/>',
      menu: '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
      accent: '<path d="m19 11-8-8-8.6 8.6a2 2 0 0 0 0 2.8l5.2 5.2c.8.8 2 .8 2.8 0L19 11Z"/><path d="m5 2 5 5"/><path d="M2 13h15"/><path d="M22 20a2 2 0 1 1-4 0c0-1.6 1.7-2.4 2-4 .3 1.6 2 2.4 2 4Z"/>',
    };
    function row(k) {
      const o = OPTS[k];
      const v = pick(k);
      const items = o.items.map((it, n) => `<button type="button" role="menuitemradio" aria-checked="${n === state[k]}" data-opt="${k}" data-val="${n}" popovertarget="cr-${k}" popovertargetaction="hide">${swatch(k, it)}<span>${esc(fmt(k, it))}</span>${n === state[k] ? ICON(CHECK, '0.875rem') : ''}</button>`).join('');
      // Square styles (Lyra, Sera) draw every component with square corners: radius follows.
      const square = k === 'radius' && boxy();
      const locked = square || (state.imported && !isLocked(k) && /^(base|theme|font|heading|radius)$/.test(k) && hasImported(k));
      const pin = isLocked(k);
      const lockBtn = `<button type="button" class="d-cr-lock" data-lock="${k}" aria-pressed="${pin}" aria-label="${pin ? 'Unlock' : 'Lock'} ${esc(o.label)}" title="${pin ? 'Locked: presets, imports and Shuffle keep this' : 'Lock this option'}">${ICON(pin ? LOCK : UNLOCK, '0.875rem')}</button>`;
      return `<div class="dropdown-menu d-cr-row"${pin ? ' data-pinned' : ''}>
        <button type="button" class="d-cr-btn" popovertarget="cr-${k}" aria-haspopup="menu"${locked ? ' data-locked' : ''}${square ? ' disabled title="Square style: corners stay square"' : ''}>
          <span class="d-cr-text"><span class="d-cr-label">${esc(o.label)}</span><span class="d-cr-val">${esc(square ? `None (${pick('style')})` : locked ? 'From theme' : fmt(k, v))}</span></span>
          <span class="d-cr-icon">${swatch(k, v) || ICON(ROW_ICON[k])}</span>
        </button>
        <div id="cr-${k}" data-popover popover data-side="bottom" data-align="start" class="d-cr-pop"><div role="menu" aria-label="${esc(o.label)}">${items}</div></div>
        ${lockBtn}
      </div>`;
    }
    function boxy() {
      return ['Lyra', 'Sera'].includes(pick('style'));
    }
    function hasImported(k) {
      const all = { ...state.imported.theme, ...state.imported.light };
      return { base: 'background', theme: 'primary', font: 'font-sans', heading: 'font-sans', radius: 'radius' }[k] in all;
    }
    const presetDots = (p) => `<span class="d-cr-dots">${[p.light.primary, p.light.accent, p.dark.background].map((c) => `<span class="d-sw" style="background:${c}"></span>`).join('')}</span>`;
    function presetRow() {
      const cur = state.imported?.preset;
      const items = PRESETS.map((p, n) => `<button type="button" role="menuitemradio" aria-checked="${n === cur}" data-preset="${n}" popovertarget="cr-preset" popovertargetaction="hide">${presetDots(p)}<span>${esc(p.name)}</span>${n === cur ? ICON(CHECK, '0.875rem') : ''}</button>`).join('');
      const val = state.imported ? state.imported.name + (state.imported.edited ? ' (edited)' : '') : 'None';
      return `<div class="dropdown-menu d-cr-row">
        <button type="button" class="d-cr-btn" popovertarget="cr-preset" aria-haspopup="menu">
          <span class="d-cr-text"><span class="d-cr-label">Theme Preset</span><span class="d-cr-val">${esc(val)}</span></span>
          <span class="d-cr-icon">${cur != null && PRESETS[cur] ? presetDots(PRESETS[cur]) : `<span class="d-sw" style="background:${tokens().light.primary || 'var(--foreground)'}"></span>`}</span>
        </button>
        <div id="cr-preset" data-popover popover data-side="bottom" data-align="start" class="d-cr-pop"><div role="menu" aria-label="Theme preset">${items}</div></div>
      </div>`;
    }
    const tokLabel = (k) => k.replace(/-/g, ' ').replace(/^./, (c) => c.toUpperCase());
    const tokRow = (k, v) => `<div class="d-cr-tok"><input type="color" id="cr-tok-${k}" data-tok="${k}" value="${toHex(v)}" aria-label="${esc(tokLabel(k))} color"><label for="cr-tok-${k}">${esc(tokLabel(k))}</label><input class="input" data-tok-text="${k}" value="${esc(v)}" aria-label="${esc(tokLabel(k))} value" spellcheck="false" autocomplete="off"></div>`;
    const range = (key, label, min, max, step, value, unit) => `<div class="d-cr-range"><label for="cr-r-${key}"><span>${label}</span><output id="cr-o-${key}">${value}${unit}</output></label><input type="range" class="input" id="cr-r-${key}" data-num="${key}" data-unit="${unit}" min="${min}" max="${max}" step="${step}" value="${value}"></div>`;
    const group = (title, body, open) => `<details class="d-cr-grp"${open ? ' open' : ''}><summary>${ICON(CHEVRON, '0.875rem')}${title}</summary><div>${body}</div></details>`;
    // The tweakcn-style editor: every color token for the current mode, then font, radius, spacing and shadow.
    function editor() {
      const mode = (shownMode = modeNow());
      const { shared, [mode]: set } = tokens();
      const sh = { ...DEFAULT_SHADOW, ...state.imported?.shadow };
      const num = (v, fb) => (Number.isFinite(parseFloat(v)) ? parseFloat(v) : fb);
      const font = FONTS.find(([f]) => (shared['font-sans'] || '').includes(`"${f}"`))?.[0];
      return `<div class="d-cr-edhead">
          <button type="button" class="btn" data-variant="ghost" data-size="sm" data-cr="back">${ICON(BACK)}Back</button>
          <div class="d-cr-seg" role="group" aria-label="Mode to edit">${['light', 'dark'].map((m) => `<button type="button" class="btn" data-size="sm" data-variant="${m === mode ? 'secondary' : 'ghost'}" aria-pressed="${m === mode}" data-cr="mode" data-mode="${m}">${m === 'light' ? 'Light' : 'Dark'}</button>`).join('')}</div>
        </div>
        <p class="d-cr-hint">Colors are edited for ${mode} mode. Font, radius, spacing and shadow apply to both.</p>
        ${TOKEN_GROUPS.map(([title, keys], n) => group(title, keys.map((k) => tokRow(k, set[k] || '')).join(''), n < 2)).join('')}
        ${group('Typography', `<div class="d-cr-range"><label for="cr-font">Font</label><select class="select" id="cr-font" data-font>${font ? '' : '<option selected>Custom</option>'}${FONTS.map(([f]) => `<option${f === font ? ' selected' : ''}>${esc(f)}</option>`).join('')}</select></div>${range('tracking-normal', 'Letter spacing', -0.05, 0.1, 0.005, num(shared['tracking-normal'], 0), 'em')}${Object.entries(WEIGHTS).map(([k, w]) => range(`font-weight-${k}`, `Weight: ${k === 'normal' ? 'regular' : k}`, 100, 900, 50, num(shared[`font-weight-${k}`], w), '')).join('')}`)}
        ${group('Radius &amp; spacing', range('radius', 'Radius', 0, 1.5, 0.025, num(shared.radius, 0.625), 'rem') + range('spacing', 'Spacing', 0.2, 0.32, 0.005, num(shared.spacing, 0.25), 'rem'), true)}
        ${group('Shadow', `<div class="d-cr-tok"><input type="color" id="cr-shc" data-shcolor value="${toHex(`hsl(${sh.color})`)}" aria-label="Shadow color"><label for="cr-shc">Shadow color</label></div>${range('sh-opacity', 'Opacity', 0, 1, 0.01, sh.opacity, '')}${range('sh-blur', 'Blur', 0, 50, 1, sh.blur, 'px')}${range('sh-spread', 'Spread', -10, 10, 1, sh.spread, 'px')}${range('sh-x', 'Offset X', -10, 10, 1, sh.x, 'px')}${range('sh-y', 'Offset Y', -10, 10, 1, sh.y, 'px')}`)}
        <div class="d-cr-actions">
          <button type="button" class="btn" data-variant="outline" data-cr="clear-import">Reset theme</button>
          <button type="button" class="btn" data-variant="outline" commandfor="cr-css" command="show-modal" data-cr="show-css">Copy CSS</button>
        </div>`;
    }
    function panel() {
      if (view === 'edit') return editor();
      const imp = state.imported ? `<div class="d-cr-import"><span>${ICON(UPLOAD, '0.875rem')} ${esc(state.imported.name)} theme</span><button type="button" class="btn" data-variant="ghost" data-size="sm" data-cr="clear-import">Clear</button></div>` : '';
      return `${imp}<div class="d-cr-rows">${presetRow()}${KEYS.map(row).join('')}</div>${sliderRows()}
        <button type="button" class="btn d-cr-wide" data-variant="outline" data-cr="edit">${ICON(SLIDERS)}Customize theme</button>
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
    // Corner smoothing: only Squircle and Smooth corners have it, and only when there is a radius.
    // Panel sliders write straight to state (not part of the preset code).
    const SLIDE = {
      fontSize: { label: 'Font Size', min: 12, max: 20, step: 0.5, show: (v) => `${v}px` },
      fontWeight: { label: 'Font Weight', min: -200, max: 200, step: 50, show: (v) => (v ? `${v > 0 ? '+' : ''}${v}` : 'Default') },
      smoothing: { label: 'Corner Smoothing', min: 0, max: 1, step: 0.05, show: (v) => `${Math.round(v * 100)}%` },
    };
    function slider(k, hint, off = '') {
      const o = SLIDE[k], v = state[k] ?? DEFAULT[k];
      return `<div class="d-cr-range d-cr-slide"><label for="cr-s-${k}"><span>${o.label}</span><output id="cr-so-${k}">${off ? '–' : o.show(v)}</output></label><input type="range" class="input" id="cr-s-${k}" data-slide="${k}" min="${o.min}" max="${o.max}" step="${o.step}" value="${v}"${off ? ` disabled title="${off}"` : ''} aria-describedby="cr-sh-${k}"><p class="d-cr-hint" id="cr-sh-${k}">${off || hint}</p></div>`;
    }
    function sliderRows() {
      const off = !SMOOTH[pick('corners')] ? 'Pick Squircle or Smooth corners' : !parseFloat(tokens().shared.radius) ? 'Set a radius first' : '';
      return slider('fontSize', 'Base text size; every text size scales with it.') + slider('fontWeight', 'Lighter or bolder: shifts regular, medium, semibold and bold together.') + slider('smoothing', 'Native corner-shape in Chrome 139+; drawn with Monoco elsewhere.', off);
    }
    const dlg = (id, title, desc, body, foot = '') => `<dialog id="${id}" class="dialog d-cr-dialog" closedby="any" aria-labelledby="${id}-t"><div><header><h2 id="${id}-t">${title}</h2><p>${desc}</p></header><section>${body}</section><footer>${foot}<button type="button" class="btn" data-variant="outline" commandfor="${id}" command="close">Close</button></footer></div></dialog>`;
    function page() {
      return `<div class="d-create">
        <aside class="d-cr-panel dark" id="cr-panel" aria-label="Preset options">${panel()}</aside>
        <div class="d-cr-stage"><iframe id="cr-frame" data-preview title="Theme preview" src="create-preview.html"></iframe></div>
      </div>
      ${dlg('cr-open', 'Open Preset', 'Paste a preset code to load its options.', `<input class="input" id="cr-code" placeholder="--preset 00000103100" autocomplete="off" spellcheck="false" aria-label="Preset code"><p class="d-cr-err" id="cr-code-err" hidden>That code is not valid.</p>`, '<button type="button" class="btn" data-cr="open">Open</button>')}
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
    // The component stylesheet of the site and of block pages: the Vega bundle, or the chosen
    // style's own bundle in its place (each style stands alone; never layered on Vega).
    const stylePack = (prefix) => (state.style ? `${prefix}dist/styles/${styleFile()}` : `${prefix}dist/auvyx.min.css`);
    // Standalone block pages (opened in a new tab) read this to apply the same preset.
    function publish() {
      try { localStorage.setItem('auvyx-preset', JSON.stringify({ css: css(), style: state.style ? styleFile() : '', fonts: fontsHref(), icons: iconLib() })); } catch (e) {}
    }
    function syncSite() {
      publish();
      setHref(headTag(document, 'd-cr-site-style', 'link'), stylePack(''));
      setHref(headTag(document, 'd-cr-site-fonts', 'link'), fontsHref());
      headTag(document, 'd-cr-site', 'style').textContent = css();
      window.auvyxCorners?.apply();
      window.auvyxIcons?.apply(iconLib());
    }
    function syncBlock(doc) {
      if (!doc?.head) return;
      setHref(headTag(doc, 'd-cr-style', 'link'), stylePack('../'));
      setHref(headTag(doc, 'd-cr-fonts', 'link'), fontsHref());
      headTag(doc, 'd-cr-theme', 'style').textContent = css();
      doc.defaultView?.auvyxIcons?.apply(iconLib());
    }
    // Showcase frames (create-preview.html): the Create stage and the home page.
    function syncPreview(f) {
      const doc = f?.contentDocument;
      if (!doc || !doc.getElementById('sc-theme')) return;
      doc.getElementById('sc-theme').textContent = css();
      setHref(doc.getElementById('sc-style'), `dist/styles/${styleFile()}`);
      setHref(doc.getElementById('sc-fonts'), fontsHref());
      doc.documentElement.classList.toggle('dark', document.documentElement.classList.contains('dark'));
      f.contentWindow.auvyxCorners?.apply();
      f.contentWindow.auvyxIcons?.apply(iconLib());
    }
    function sync() {
      syncSite();
      document.querySelectorAll('iframe[data-preview]').forEach(syncPreview);
      // The editor shows one mode's colors: redraw it when dark mode is toggled.
      if (view === 'edit' && shownMode !== modeNow()) { const p = $('#cr-panel'); if (p) p.innerHTML = panel(); }
    }
    // Editor changes: save and re-theme once per frame, without redrawing the panel (keeps focus and drags).
    let raf = 0;
    function live() {
      save();
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => applyTheme());
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
      frame.addEventListener('load', () => syncPreview(frame));
      sync();
      if (mounted) return;
      mounted = true;
      document.addEventListener('click', (e) => {
        if (!$('#cr-panel')) return;
        const lock = e.target.closest('[data-lock]');
        if (lock) { state.locks = { ...state.locks, [lock.dataset.lock]: !isLocked(lock.dataset.lock) }; refresh(); $(`[data-lock="${lock.dataset.lock}"]`)?.focus(); return; }
        const opt = e.target.closest('[data-opt]');
        if (opt) { state[opt.dataset.opt] = +opt.dataset.val; refresh(); return; }
        const pre = e.target.closest('[data-preset]');
        if (pre) { const n = +pre.dataset.preset; state.imported = { ...structuredClone(PRESETS[n]), preset: n }; refresh(); return; }
        const a = e.target.closest('[data-cr]');
        if (!a) return;
        const act = a.dataset.cr;
        if (act === 'shuffle') { for (const k of KEYS) if (k !== 'menu' && k !== 'accent' && !isLocked(k)) state[k] = Math.floor(Math.random() * OPTS[k].items.length); if (!isLocked('heading')) state.heading = Math.random() < 0.6 ? 0 : state.heading; refresh(); }
        else if (act === 'reset') { const locks = state.locks || {}; const kept = Object.fromEntries(KEYS.filter((k) => locks[k]).map((k) => [k, state[k]])); state = { ...DEFAULT, imported: null, locks, ...kept }; refresh(); }
        else if (act === 'clear-import') { state.imported = null; refresh(); }
        else if (act === 'mode') { if (a.dataset.mode !== modeNow()) $('#d-mode').click(); }
        else if (act === 'edit' || act === 'back') { view = act === 'edit' ? 'edit' : 'options'; refresh(); }
        else if (act === 'show-css') {
          // Tailwind source (auvyx add --css tailwind) compiles shadow-* to fixed values unless @theme inline points them at the variables.
          const sh = Object.keys(tokens().shared).filter((k) => k.startsWith('shadow-'));
          $('#cr-css-body').innerHTML = codeBox(css(), 'theme.css') + (sh.length ? '<p class="d-cr-note">With components installed as Tailwind source (<code>--css tailwind</code>), also add this so <code>shadow-*</code> follows the theme:</p>' + codeBox(`@theme inline {\n${sh.map((k) => `  --${k}: var(--${k});`).join('\n')}\n}`, 'theme.css') : '');
        }
        else if (act === 'show-init') $('#cr-init-body').innerHTML = codeBox(headSnippet(), 'index.html') + '<p class="d-cr-note">Add blocks with your icon library:</p>' + codeBox(cliSnippet(), 'terminal');
        else if (act === 'open') {
          const v = decode($('#cr-code').value);
          $('#cr-code-err').hidden = !!v;
          if (v) { for (const k of KEYS) if (!isLocked(k)) state[k] = v[k]; $('#cr-open').close(); refresh(); }
        } else if (act === 'import') {
          const err = $('#cr-theme-err');
          try { state.imported = parseTheme($('#cr-theme-src').value); err.hidden = true; $('#cr-import').close(); refresh(); }
          catch (x) { err.textContent = x.message; err.hidden = false; }
        }
      });
      const setShadow = (patch) => {
        const t = custom();
        t.shadow = { ...DEFAULT_SHADOW, ...t.shadow, ...patch };
        Object.assign(t.theme, shadowVars(t.shadow));
      };
      document.addEventListener('input', (e) => {
        const el = e.target;
        if (!el.closest?.('#cr-panel')) return;
        if (el.dataset.slide) {
          const k = el.dataset.slide;
          state[k] = +el.value;
          $(`#cr-so-${k}`).textContent = SLIDE[k].show(state[k]);
          live();
          return;
        }
        if (el.dataset.tok) {
          const v = hexToOklch(el.value);
          custom()[modeNow()][el.dataset.tok] = v;
          el.parentElement.querySelector('[data-tok-text]').value = v;
        } else if (el.dataset.num) {
          const k = el.dataset.num, unit = el.dataset.unit, v = +el.value;
          $(`#cr-o-${k}`).textContent = v + unit;
          if (k.startsWith('sh-')) setShadow({ [k.slice(3)]: v });
          else custom().theme[k] = v + unit;
        } else if (el.matches('[data-shcolor]')) setShadow({ color: hexToHsl(el.value) });
        else return;
        live();
      });
      document.addEventListener('change', (e) => {
        const el = e.target;
        if (!el.closest?.('#cr-panel')) return;
        if (el.dataset.tokText) {
          const v = el.value.trim();
          const ok = CSS.supports('color', v);
          el.toggleAttribute('aria-invalid', !ok);
          if (!ok) return;
          custom()[modeNow()][el.dataset.tokText] = v;
          el.parentElement.querySelector('[data-tok]').value = toHex(v);
          live();
        } else if (el.matches('[data-font]')) { custom().theme['font-sans'] = fontStack(el.value); live(); }
      });
    }
    return { page, mount, sync, syncBlock, parseTheme, css, encode, decode, get state() { return state; } };
  })();
  window.auvyxCreate = Create;

// Prefixed build (dist/ax/): every class @auvyx/ui defines gets a prefix (`.btn` -> `.ax-btn`) in the CSS and in the JS that
// finds, creates or toggles those classes, so Auvyx UI can sit inside a page whose theme uses the same names (Bootstrap's
// `.btn`, `.card`, `.alert`, `.dropdown-menu`...) without either styling the other. Markup for this build uses the prefixed
// names; data-* attributes, ARIA and element names do not change. `dark` (the page's color-scheme class) is kept.
import postcss from 'postcss';
import * as acorn from 'acorn';

export const PREFIX = 'ax-';
export const KEEP = new Set(['dark']);

const NAME = /^-?[_a-zA-Z\\]/;

/**
 * Rewrites the class names in one selector (`.btn:hover > .x` -> `.ax-btn:hover > .ax-x`), leaving attribute selectors and
 * strings alone. `rename(name)` returns the new name or null to keep it. Escaped characters (`.px-2\.5`) stay part of the name.
 */
export function mapSelectorClasses(sel, rename) {
  let out = '';
  let i = 0;
  let bracket = 0;
  let quote = null;
  while (i < sel.length) {
    const c = sel[i];
    if (quote) { out += c; if (c === '\\') { out += sel[i + 1] ?? ''; i += 2; continue; } if (c === quote) quote = null; i++; continue; }
    if (c === '"' || c === "'") { quote = c; out += c; i++; continue; }
    if (c === '[') bracket++;
    if (c === ']') bracket--;
    if (c === '\\') { out += c + (sel[i + 1] ?? ''); i += 2; continue; }
    if (c === '.' && bracket === 0 && NAME.test(sel.slice(i + 1, i + 2))) {
      let j = i + 1;
      let name = '';
      while (j < sel.length) {
        if (sel[j] === '\\') { name += sel[j] + (sel[j + 1] ?? ''); j += 2; continue; }
        if (/[\w-]/.test(sel[j])) { name += sel[j]; j++; continue; }
        break;
      }
      const next = rename(name);
      out += '.' + (next ?? name);
      i = j;
      continue;
    }
    out += c;
    i++;
  }
  return out;
}

/** The CSS with every class prefixed (KEEP aside); also the set of the original class names, for the JS. */
export function prefixCss(css, prefix = PREFIX, keep = KEEP) {
  const root = postcss.parse(css);
  const classes = new Set();
  const rename = (name) => {
    if (keep.has(name) || name.startsWith(prefix)) return null;
    classes.add(name.replace(/\\(.)/g, '$1'));
    return prefix + name;
  };
  root.walkRules((rule) => {
    if (rule.parent?.type === 'atrule' && /keyframes$/.test(rule.parent.name)) return;
    rule.selector = mapSelectorClasses(rule.selector, rename);
  });
  return { css: root.toString(), classes };
}

const TAGS = 'a|abbr|article|aside|button|caption|code|details|dialog|div|dl|dt|dd|fieldset|figure|footer|form|h[1-6]|header|hr|img|input|kbd|label|legend|li|main|menu|nav|ol|output|p|pre|section|select|small|span|summary|svg|table|tbody|td|textarea|th|thead|tr|ul';
const SELECTOR_CLASS = new RegExp(`(^|[\\s>+~,(\\]])(${TAGS})?\\.([_a-zA-Z][\\w-]*)`, 'g');
const CLASS_LIST = new Set(['add', 'remove', 'toggle', 'contains', 'replace']);
const SELECTOR_CALL = new Set(['querySelector', 'querySelectorAll', 'closest', 'matches']);

/**
 * The JS with the prefixed names wherever it names a class: selectors (strings handed to querySelector/closest/matches, a
 * component's `selector`, and any string that reads as a selector naming a known class), class lists (`classList.add('x')`,
 * `el.className = 'x y'`, comparisons with a variable named like `className`) and `class="..."` in generated markup. Other
 * strings (event names such as 'input' or 'select', which are also class names) are left alone.
 */
export function prefixJs(js, classes, prefix = PREFIX) {
  const ast = acorn.parse(js, { ecmaVersion: 'latest', sourceType: 'script' });
  const edits = [];
  const known = (name) => classes.has(name);
  const tokens = (s) => s.replace(/(^|\s)([^\s]+)/g, (m, sp, t) => sp + (known(t) ? prefix + t : t));
  const selector = (s) => mapSelectorClasses(s, (n) => (known(n) ? prefix + n : null));
  const classAttr = (s) => s.replace(/\bclass=(["'])([^"']*)\1/g, (m, q, v) => `class=${q}${tokens(v)}${q}`);
  // `.x` at a selector boundary, or after an element name (`dialog.x`); not `name.method()` in prose or code
  const looksLikeSelector = (s) => [...s.matchAll(SELECTOR_CLASS)].some((m) => known(m[3]));
  const literal = (node, f) => {
    if (node?.type !== 'Literal' || typeof node.value !== 'string') return;
    const next = f(node.value);
    if (next !== node.value) edits.push([node.start, node.end, JSON.stringify(next)]);
  };
  const isClassName = (n) => (n?.type === 'Identifier' && /classname|cls/i.test(n.name)) || (n?.type === 'MemberExpression' && n.property?.name === 'className');
  const handled = new Set();
  const visit = (node, parent) => {
    if (!node || typeof node.type !== 'string') return;
    if (node.type === 'CallExpression' && node.callee.type === 'MemberExpression') {
      const prop = node.callee.property?.name;
      const onClassList = node.callee.object?.type === 'MemberExpression' && node.callee.object.property?.name === 'classList';
      if (onClassList && CLASS_LIST.has(prop)) for (const a of node.arguments) { literal(a, tokens); handled.add(a); }
      if (SELECTOR_CALL.has(prop) && node.arguments[0]) { literal(node.arguments[0], selector); handled.add(node.arguments[0]); }
    }
    if (node.type === 'AssignmentExpression' && isClassName(node.left)) { literal(node.right, tokens); handled.add(node.right); }
    if (node.type === 'BinaryExpression' && /^[!=]==?$/.test(node.operator)) {
      if (isClassName(node.left)) { literal(node.right, tokens); handled.add(node.right); }
      if (isClassName(node.right)) { literal(node.left, tokens); handled.add(node.left); }
    }
    if (node.type === 'Property' && !node.computed && (node.key.name === 'selector' || node.key.value === 'selector')) { literal(node.value, selector); handled.add(node.value); }
    if (node.type === 'Literal' && typeof node.value === 'string' && !handled.has(node)) {
      if (/\bclass=/.test(node.value)) literal(node, classAttr);
      else if (looksLikeSelector(node.value)) literal(node, selector);
    }
    if (node.type === 'TemplateElement') {
      const raw = node.value.raw;
      let next = /\bclass=/.test(raw) ? classAttr(raw) : raw;
      if (looksLikeSelector(next)) next = selector(next);
      if (next !== raw) edits.push([node.start, node.end, next]);
    }
    for (const key of Object.keys(node)) {
      if (key === 'type' || key === 'start' || key === 'end') continue;
      const v = node[key];
      if (Array.isArray(v)) v.forEach((c) => visit(c, node));
      else if (v && typeof v.type === 'string') visit(v, node);
    }
  };
  visit(ast, null);
  edits.sort((a, b) => b[0] - a[0]);
  let out = js;
  for (const [s, e, text] of edits) out = out.slice(0, s) + text + out.slice(e);
  return out;
}

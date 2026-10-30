// Convert a block page (parsed by build_registry.mjs) to a React 19 component.
//
// The markup is translated tag by tag, so the output keeps the HTML's layout
// and stays readable: attributes are renamed for JSX, inline styles become
// objects, uncontrolled form state uses defaultValue/defaultChecked, and the
// whitespace JSX would drop between inline content is kept as {" "}. Block
// <style> stays a <style> element; inline scripts run once after mount.
// Anything the converter does not understand throws, so a new block cannot
// ship a silently broken React variant.

const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
// Text-level elements: a line break between them and text renders as a space.
const INLINE = new Set(['a', 'abbr', 'b', 'code', 'em', 'i', 'kbd', 'mark', 's', 'small', 'span', 'strong', 'sub', 'sup', 'time', 'u']);

const RENAME = {
  class: 'className', for: 'htmlFor', tabindex: 'tabIndex', maxlength: 'maxLength', minlength: 'minLength',
  inputmode: 'inputMode', autocomplete: 'autoComplete', colspan: 'colSpan', rowspan: 'rowSpan',
  readonly: 'readOnly', autofocus: 'autoFocus', popovertarget: 'popoverTarget', popovertargetaction: 'popoverTargetAction',
  srcset: 'srcSet', crossorigin: 'crossOrigin', enctype: 'encType', novalidate: 'noValidate', datetime: 'dateTime',
  contenteditable: 'contentEditable', spellcheck: 'spellCheck', 'xlink:href': 'xlinkHref', 'xml:space': 'xmlSpace',
};
const BOOLEAN = new Set(['allowfullscreen', 'async', 'autofocus', 'checked', 'controls', 'default', 'defer', 'disabled', 'formnovalidate', 'hidden', 'inert', 'loop', 'multiple', 'muted', 'novalidate', 'open', 'playsinline', 'readonly', 'required', 'reversed', 'selected']);
const NUMERIC = new Set(['maxLength', 'minLength', 'tabIndex', 'colSpan', 'rowSpan', 'size', 'rows', 'cols', 'span']);
// Valid in React 19 but missing from @types/react; passed through a spread so the file type-checks.
const UNTYPED = new Set(['commandfor', 'command']);
// Inline handlers the blocks use, as React props.
const HANDLERS = { 'onsubmit=event.preventDefault()': 'onSubmit={(e) => e.preventDefault()}' };

const camel = (s) => s.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
const NAMED = { quot: '"', apos: "'", lt: '<', gt: '>', amp: '&', nbsp: '\u00a0', middot: '·', mdash: '—', ndash: '–', hellip: '…', copy: '©', rarr: '→', larr: '←' };
const decode = (s) => s.replace(/&(#x[\da-f]+|#\d+|\w+);/gi, (m, e) => {
  if (e[0] === '#') return String.fromCodePoint(e[1].toLowerCase() === 'x' ? parseInt(e.slice(2), 16) : +e.slice(1));
  if (!(e in NAMED)) throw new Error(`unknown entity ${m}`);
  return NAMED[e];
});
const str = (v) => (/["\\{}]/.test(v) || /&/.test(v) ? `{${JSON.stringify(decode(v))}}` : `"${v}"`);

export const componentName = (name) => name.replace(/(^|-)(\w)/g, (_, __, c) => c.toUpperCase());

function styleObject(css) {
  const entries = css.split(';').map((d) => d.trim()).filter(Boolean).map((d) => {
    const i = d.indexOf(':');
    const prop = d.slice(0, i).trim();
    const key = prop.startsWith('--') ? JSON.stringify(prop) : camel(prop);
    return `${key}: ${JSON.stringify(decode(d.slice(i + 1).trim()))}`;
  });
  // CSS custom properties are not in React's CSSProperties.
  const cast = entries.some((e) => e.startsWith('"--')) ? ' as React.CSSProperties' : '';
  return `{{ ${entries.join(', ')} }${cast}}`;
}

const ATTR = /([^\s"'>/=]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+)))?/g;
const TOKEN = /<!--([\s\S]*?)-->|<(\/?)([a-zA-Z][\w-]*)((?:\s+[^\s"'>/=]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s"'>]+))?)*)\s*(\/?)>|([^<]+)/g;

function tokenize(html) {
  const tokens = [];
  for (const m of html.matchAll(TOKEN)) {
    if (m[1] !== undefined) tokens.push({ kind: 'comment', text: m[1] });
    else if (m[3]) {
      const tag = m[3].toLowerCase();
      if (m[2]) tokens.push({ kind: 'close', tag });
      else {
        // A repeated attribute is ignored by HTML parsers: keep the first.
        const attrs = [...m[4].matchAll(ATTR)].map((a) => ({ name: a[1], value: a[2] ?? a[3] ?? a[4] }))
          .filter((a, i, all) => all.findIndex((b) => b.name.toLowerCase() === a.name.toLowerCase()) === i);
        tokens.push({ kind: 'open', tag, attrs, selfClose: Boolean(m[5]) || VOID.has(tag) });
      }
    } else tokens.push({ kind: 'text', text: m[6] });
  }
  if (tokens.map((t) => (t.kind === 'text' ? t.text : '')).join('').includes('<')) throw new Error('unparsed markup');
  return tokens;
}

function convertAttrs(token, ctx) {
  const { tag, attrs } = token;
  const custom = tag.includes('-');
  const out = [];
  const untyped = [];
  const type = attrs.find((a) => a.name === 'type')?.value;
  for (const { name, value } of attrs) {
    const lower = name.toLowerCase();
    if (lower.startsWith('on')) {
      const handler = HANDLERS[`${lower}=${value}`];
      if (!handler) throw new Error(`unsupported inline handler ${name}="${value}"`);
      out.push(handler);
      continue;
    }
    if (lower === 'style') { out.push(`style=${styleObject(value)}`); continue; }
    if (lower === 'selected' && tag === 'option') { ctx.selected = attrs.find((a) => a.name === 'value')?.value; continue; }
    if (UNTYPED.has(lower)) { untyped.push(`${lower}: ${JSON.stringify(value)}`); continue; }
    let prop = RENAME[lower] ?? name;
    if (custom) prop = lower === 'class' ? 'className' : name;
    else if (lower === 'checked') prop = 'defaultChecked';
    else if (lower === 'value' && (tag === 'textarea' || (tag === 'input' && !['checkbox', 'radio', 'hidden', 'submit', 'button', 'reset'].includes(type)))) prop = 'defaultValue';
    else if (!lower.startsWith('data-') && !lower.startsWith('aria-') && lower.includes('-')) prop = camel(lower);
    if (value === undefined) out.push(BOOLEAN.has(lower) || custom ? prop : `${prop}=""`);
    else if (NUMERIC.has(prop) && /^-?\d+$/.test(value)) out.push(`${prop}={${value}}`);
    else out.push(`${prop}=${str(value)}`);
  }
  if (untyped.length) out.push(`{...{ ${untyped.join(', ')} }}`);
  return out;
}

const inlineSide = (t, side) => {
  if (!t) return false;
  if (t.kind === 'text') return true;
  if (side === 'prev') return (t.kind === 'close' || (t.kind === 'open' && t.selfClose)) && INLINE.has(t.tag);
  return t.kind === 'open' && INLINE.has(t.tag);
};

// Markup to JSX lines (no surrounding fragment).
export function markupToJsx(html) {
  const tokens = tokenize(html);
  const ctx = {};
  let out = '';
  const selects = [];
  tokens.forEach((t, i) => {
    if (t.kind === 'comment') { out += `{/*${t.text.replace(/\*\//g, '* /')}*/}`; return; }
    if (t.kind === 'close') {
      if (t.tag === 'select') {
        const at = selects.pop();
        if (ctx.selected !== undefined) out = out.slice(0, at) + ` defaultValue=${str(ctx.selected)}` + out.slice(at);
        ctx.selected = undefined;
      }
      out += `</${t.tag}>`;
      return;
    }
    if (t.kind === 'open') {
      if (t.tag === 'script' || t.tag === 'textarea' || t.tag === 'pre') throw new Error(`<${t.tag}> in block markup`);
      const attrs = convertAttrs(t, ctx);
      out += `<${t.tag}`;
      if (t.tag === 'select') selects.push(out.length);
      out += `${attrs.length ? ' ' + attrs.join(' ') : ''}${t.selfClose ? ' />' : '>'}`;
      return;
    }
    // Text: JSX trims whitespace that contains a line break; HTML renders it as
    // one space. Keep that space where it can show: between inline content.
    let text = t.text.replace(/[{}>]/g, (c) => ({ '{': '&#123;', '}': '&#125;', '>': '&gt;' })[c]);
    const prev = tokens[i - 1];
    const next = tokens[i + 1];
    if (!text.trim()) {
      if (text.includes('\n') && inlineSide(prev, 'prev') && inlineSide(next, 'next')) text = text.replace(/^(\s*?)(\n)/, '$1{" "}$2');
      out += text;
      return;
    }
    const lead = text.match(/^\s*/)[0];
    const trail = text.match(/\s*$/)[0];
    const body = text.slice(lead.length, text.length - trail.length);
    const raw = t.text.trim();
    const keepLead = lead.includes('\n') && inlineSide(prev, 'prev');
    const keepTrail = trail.includes('\n') && inlineSide(next, 'next');
    // One string keeps one text node, so the browser shapes the line as it does the HTML.
    if (keepLead || keepTrail) out += lead + `{${JSON.stringify(decode((keepLead ? ' ' : '') + raw.replace(/\s+/g, ' ') + (keepTrail ? ' ' : '')))}}` + trail;
    else out += lead + body + trail;
  });
  return out;
}

const indent = (s, pad) => s.split('\n').map((l) => (l.trim() ? pad + l : '')).join('\n');
const template = (s) => '`' + s.replace(/\\/g, '\\\\').replace(/`/g, '\\`').replace(/\$\{/g, '\\${') + '`';

/**
 * @param {string} name block name, e.g. "login-01"
 * @param {{ title?: string, description?: string, styles: string, body: string, scripts: string[] }} block
 *   styles: the block's CSS; body: its markup (both dedented); scripts: inline scripts (dedented)
 */
export function toReact(name, { title, description, styles, body, scripts }) {
  const fn = componentName(name);
  const jsx = [];
  if (styles) jsx.push(`<style>{${template('\n' + indent(styles, '  ') + '\n')}}</style>`);
  jsx.push(markupToJsx(body));
  const head = [
    `// ${title ?? name}${description ? `: ${description}` : ''}`,
    `// Auvyx UI block (React). Needs auvyx.min.css and auvyx.min.js loaded once by the app.`,
  ];
  const lines = [];
  if (scripts.length) {
    // The scripts are plain DOM code from the HTML edition, not typed.
    lines.push('// @ts-nocheck', ...head, `import { useEffect, useRef } from "react";`, '');
    lines.push(`export default function ${fn}() {`);
    lines.push('  const ran = useRef(false);');
    lines.push('  useEffect(() => {');
    lines.push('    // Once per mount, also under StrictMode.');
    lines.push('    if (ran.current) return;');
    lines.push('    ran.current = true;');
    lines.push('    setup();');
    lines.push('  }, []);');
    lines.push('');
  } else {
    lines.push(...head, '');
    lines.push(`export default function ${fn}() {`);
  }
  lines.push('  return (', '    <>', indent(jsx.join('\n'), '      '), '    </>', '  );', '}');
  if (scripts.length) {
    lines.push('', '// Ported from the HTML edition: runs after the markup above is in the document.');
    lines.push('function setup() {', indent(scripts.join('\n'), '  '), '}');
  }
  const src = lines.join('\n') + '\n';
  return src.includes('React.CSSProperties') ? src.replace(/^((?:\/\/.*\n)+)/, '$1import type React from "react";\n') : src;
}

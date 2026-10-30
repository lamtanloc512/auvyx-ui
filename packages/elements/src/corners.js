// Squircle corners fallback (fork addition), powered by Monoco (MIT, somonoco.com).
//
// Browsers with CSS `corner-shape` (Chrome 139+) draw --corner-shape natively and
// this script does nothing. Elsewhere it clips surfaces to the same shape with
// Monoco's SVG clip-path, redrawing on resize.
//
//   <script src=".../auvyx.corners.min.js" defer></script>
//   :root { --corner-shape: squircle; --corner-smoothing: 0.8; }
//
// Only surfaces are clipped (cards, popovers, dialogs, alerts, items, sheets):
// clip-path also clips box-shadow, so focusable controls keep native round
// corners and their focus rings. A surface's border or 1px ring is redrawn by
// Monoco on the squircle path so it stays continuous at the corners; surfaces
// with drop shadows get an SVG fill and drop-shadow filters instead of a clip. Override with data-corners-selector on <html>.
// Set data-corners="force" on <html> to use Monoco even with native support.
import { addCorners, unobserve, Squircle, FigmaSquircle, Flat, Inset, RoundInverse, Round } from '@monokai/monoco';

const DEFAULT_SELECTOR = [
  '.card', '.alert', '.item', '.empty', '.sheet', '.toast > *',
  '.dialog > *', '.alert-dialog > *', '.command-dialog > .command',
  '[data-popover]', '.calendar', '.code-block', '.attachment',
].join(',');

// corner-shape keyword -> Monoco corner type
const TYPES = { squircle: Squircle, 'superellipse(1.5)': FigmaSquircle, bevel: Flat, notch: Inset, scoop: RoundInverse, round: Round };

const root = document.documentElement;
const tracked = new Set();

function shape() {
  return getComputedStyle(root).getPropertyValue('--corner-shape').trim() || 'round';
}

function wanted() {
  if (root.dataset.corners === 'force') return true;
  return !(window.CSS && CSS.supports('corner-shape', 'squircle'));
}

// Inline styles we set on a surface, restored by clear().
const SET = ['clipPath', 'borderColor', 'backgroundColor', 'backgroundImage', 'backgroundOrigin', 'backgroundRepeat', 'boxShadow', 'filter'];

function clear() {
  for (const el of tracked) {
    unobserve(el);
    for (const k of SET) el.style[k] = '';
  }
  tracked.clear();
}

const TRANSPARENT = /^(transparent|rgba\(0, 0, 0, 0\))$/;

// Split a computed box-shadow into its 1px-style ring (spread only, how the
// style packs draw card/popover edges) and the remaining drop shadows.
function shadows(value) {
  const ring = [], drop = [];
  if (!value || value === 'none') return { ring, drop };
  for (const layer of value.split(/,(?![^(]*\))/)) {
    const color = layer.match(/^\s*((?:[a-z-]+\([^)]*\))|#\w+|[a-z]+)/i)?.[1] ?? '';
    const nums = (layer.slice(layer.indexOf(color) + color.length).match(/-?[\d.]+px/g) || []).map(parseFloat);
    if (!color || TRANSPARENT.test(color) || layer.includes('inset')) continue;
    const [x = 0, y = 0, blur = 0, spread = 0] = nums;
    if (!x && !y && !blur && spread > 0) ring.push([spread, color]);
    else if (blur || x || y) drop.push(`drop-shadow(${x}px ${y}px ${blur / 2}px ${color})`);
  }
  return { ring, drop };
}

function apply() {
  clear();
  const s = shape();
  const type = TYPES[s] || (s.startsWith('superellipse') ? FigmaSquircle : null);
  if (!wanted() || !type || type === Round) return;
  const smoothing = parseFloat(getComputedStyle(root).getPropertyValue('--corner-smoothing')) || 1;
  const selector = root.dataset.cornersSelector || DEFAULT_SELECTOR;
  // Read every surface first, then write, so styles are measured before any change.
  const jobs = [];
  for (const el of document.querySelectorAll(selector)) {
    const cs = getComputedStyle(el);
    const radius = parseFloat(cs.borderTopLeftRadius);
    if (!radius) continue;
    const width = parseFloat(cs.borderTopWidth);
    const { ring, drop } = shadows(cs.boxShadow);
    const border = width && cs.borderTopStyle !== 'none' && !TRANSPARENT.test(cs.borderTopColor) ? [[width, cs.borderTopColor]] : [];
    jobs.push({ el, radius, border: [...border, ...ring], drop, background: cs.backgroundColor });
  }
  for (const { el, radius, border, drop, background } of jobs) {
    const opts = { borderRadius: radius, smoothing, cornerType: type };
    // A CSS border or ring would be cut at the corners, so Monoco redraws it as
    // an SVG stroke on the squircle path; the CSS border keeps its width for layout.
    if (border.length) {
      Object.assign(el.style, { borderColor: 'transparent', boxShadow: 'none', backgroundOrigin: 'border-box', backgroundRepeat: 'no-repeat' });
      opts.border = border.length === 1 ? border[0] : border;
    }
    if (drop.length) {
      // clip-path would also clip the shadow: paint the fill as SVG instead and
      // turn the box-shadows into drop-shadow filters that follow the shape.
      Object.assign(el.style, { backgroundColor: 'transparent', filter: drop.join(' ') });
      opts.background = background;
    } else {
      opts.clip = true;
    }
    addCorners(el, opts);
    tracked.add(el);
  }
}

let queued = false;
function schedule() {
  if (queued) return;
  queued = true;
  requestAnimationFrame(() => { queued = false; apply(); });
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', schedule);
else schedule();
// Re-apply when the theme changes (class/data-theme/style on <html>) or content is added.
new MutationObserver(schedule).observe(root, { attributes: true, attributeFilter: ['class', 'style', 'data-theme', 'data-corners'] });
new MutationObserver((records) => { if (records.some((r) => r.addedNodes.length)) schedule(); }).observe(document.body || root, { childList: true, subtree: true });
window.auvyxCorners = { apply, clear };

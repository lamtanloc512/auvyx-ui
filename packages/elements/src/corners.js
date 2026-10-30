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
// corners and their focus rings. Override with data-corners-selector on <html>.
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

function clear() {
  for (const el of tracked) {
    unobserve(el);
    el.style.clipPath = '';
  }
  tracked.clear();
}

function apply() {
  clear();
  const s = shape();
  const type = TYPES[s] || (s.startsWith('superellipse') ? FigmaSquircle : null);
  if (!wanted() || !type || type === Round) return;
  const smoothing = parseFloat(getComputedStyle(root).getPropertyValue('--corner-smoothing')) || 1;
  const selector = root.dataset.cornersSelector || DEFAULT_SELECTOR;
  for (const el of document.querySelectorAll(selector)) {
    const radius = parseFloat(getComputedStyle(el).borderTopLeftRadius);
    if (!radius) continue;
    addCorners(el, { borderRadius: radius, smoothing, cornerType: type, clip: true });
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

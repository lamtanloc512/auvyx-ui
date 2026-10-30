// <auvyx-resizable>: drag or arrow-key the separators between panels (fork addition).
// Panel sizes live in each panel's --size (percent of the group); the CSS
// renders them with or without this script. Emits `resize` with detail.sizes.
class AuvyxResizable extends HTMLElement {
  connectedCallback() {
    if (this._init) return;
    this._init = true;
    this.vertical = this.dataset.orientation === 'vertical';
    this.panels = [...this.children].filter((el) => el.getAttribute('role') !== 'separator');
    this.handles = [...this.children].filter((el) => el.getAttribute('role') === 'separator');
    if (this.panels.length < 2) return;

    // Normalise sizes to percentages that sum to 100.
    const given = this.panels.map((p) => parseFloat(getComputedStyle(p).getPropertyValue('--size')) || 0);
    const missing = given.filter((v) => !v).length;
    const rest = Math.max(0, 100 - given.reduce((a, b) => a + b, 0));
    this.sizes = given.map((v) => v || (missing ? rest / missing : 0));
    const sum = this.sizes.reduce((a, b) => a + b, 0) || 1;
    this.sizes = this.sizes.map((v) => (v / sum) * 100);
    this.apply();

    this.handles.forEach((handle, i) => {
      handle.setAttribute('aria-orientation', this.vertical ? 'horizontal' : 'vertical');
      handle.setAttribute('aria-valuemin', '0');
      handle.setAttribute('aria-valuemax', '100');
      if (this.panels[i].id) handle.setAttribute('aria-controls', this.panels[i].id);
      if (!handle.hasAttribute('tabindex')) handle.tabIndex = 0;
      handle.addEventListener('pointerdown', (e) => this.startDrag(e, i));
      handle.addEventListener('keydown', (e) => this.onKey(e, i));
      handle.addEventListener('dblclick', () => this.resetPair(i));
    });
  }

  minOf(i) {
    const v = parseFloat(this.panels[i].dataset.min);
    return Number.isFinite(v) ? v : 10;
  }

  maxOf(i) {
    const v = parseFloat(this.panels[i].dataset.max);
    return Number.isFinite(v) ? v : 100;
  }

  // Move the boundary after panel i so panel i gets `target` percent.
  setPair(i, target) {
    const pair = this.sizes[i] + this.sizes[i + 1];
    const lo = Math.max(this.minOf(i), pair - this.maxOf(i + 1));
    const hi = Math.min(this.maxOf(i), pair - this.minOf(i + 1));
    const next = Math.min(hi, Math.max(lo, target));
    this.sizes[i] = next;
    this.sizes[i + 1] = pair - next;
    this.apply();
  }

  resetPair(i) {
    const pair = this.sizes[i] + this.sizes[i + 1];
    this.setPair(i, pair / 2);
  }

  apply() {
    this.panels.forEach((p, i) => p.style.setProperty('--size', this.sizes[i].toFixed(3)));
    this.handles?.forEach((h, i) => h.setAttribute('aria-valuenow', String(Math.round(this.sizes[i]))));
    this.dispatchEvent(new CustomEvent('resize', { detail: { sizes: [...this.sizes] } }));
  }

  startDrag(event, i) {
    if (event.button !== 0) return;
    event.preventDefault();
    const handle = event.currentTarget;
    handle.setPointerCapture(event.pointerId);
    handle.setAttribute('data-active', '');
    this.setAttribute('data-dragging', '');
    const rect = this.getBoundingClientRect();
    const total = this.vertical ? rect.height : rect.width;
    const rtl = !this.vertical && getComputedStyle(this).direction === 'rtl';
    const start = this.vertical ? event.clientY : event.clientX;
    const initial = this.sizes[i];
    const move = (e) => {
      const delta = ((this.vertical ? e.clientY : e.clientX) - start) / total * 100;
      this.setPair(i, initial + (rtl ? -delta : delta));
    };
    const end = () => {
      handle.removeEventListener('pointermove', move);
      handle.removeAttribute('data-active');
      this.removeAttribute('data-dragging');
    };
    handle.addEventListener('pointermove', move);
    handle.addEventListener('pointerup', end, { once: true });
    handle.addEventListener('pointercancel', end, { once: true });
  }

  onKey(event, i) {
    const step = event.shiftKey ? 10 : 5;
    const rtl = !this.vertical && getComputedStyle(this).direction === 'rtl';
    const grow = this.vertical ? 'ArrowDown' : rtl ? 'ArrowLeft' : 'ArrowRight';
    const shrink = this.vertical ? 'ArrowUp' : rtl ? 'ArrowRight' : 'ArrowLeft';
    const map = { [grow]: this.sizes[i] + step, [shrink]: this.sizes[i] - step, Home: 0, End: 100, Enter: null };
    if (!(event.key in map)) return;
    event.preventDefault();
    if (event.key === 'Enter') this.resetPair(i);
    else this.setPair(i, map[event.key]);
  }
}

if (!customElements.get('auvyx-resizable')) customElements.define('auvyx-resizable', AuvyxResizable);

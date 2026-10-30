// <auvyx-accordion>: Web Components edition of Accordion (see base.js).
// value: the open item's key (an array when the accordion has data-multiple),
// where an item's key is its <details> data-value, its id, or its position
// ("0", "1"…) when it has neither.
import { AuvyxWrapper } from './base.js';

const keyOf = (details) => details.dataset.value ?? (details.id || String([...details.parentElement.children].filter((c) => c.localName === 'details').indexOf(details)));

class AuvyxAccordion extends AuvyxWrapper {
  static component = 'accordion';
  static rootSelector = '.accordion';
  static relayed = [];

  get items() {
    return this.root ? [...this.root.querySelectorAll(':scope > details')] : [];
  }

  get multiple() {
    return this.root?.hasAttribute('data-multiple') ?? false;
  }

  attach() {
    this._last = this.value;
    // <details> toggle events are async and also fire for changes from code;
    // compare with the last known value instead.
    this._onToggle = (e) => { if (e.target.parentElement === this.root) this.reportValue(); };
    this.root.addEventListener('toggle', this._onToggle, true);
  }

  detach() {
    this.root?.removeEventListener('toggle', this._onToggle, true);
  }

  get value() {
    const open = this.items.filter((d) => d.open).map(keyOf);
    return this.multiple ? open : open[0] ?? null;
  }

  set value(value) {
    if (this.defer(value)) return;
    const keys = new Set((Array.isArray(value) ? value : [value]).filter((v) => v != null).map(String));
    for (const details of this.items) details.open = keys.has(keyOf(details));
    this._last = this.value;
  }
}

if (!customElements.get('auvyx-accordion')) customElements.define('auvyx-accordion', AuvyxAccordion);

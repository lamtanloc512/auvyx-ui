// <auvyx-tabs>: Web Components edition of Tabs (see base.js).
// value: the selected tab's data-value, or its id.
import { AuvyxWrapper, watch } from './base.js';

const keyOf = (tab) => tab.dataset.value ?? tab.id;

class AuvyxTabs extends AuvyxWrapper {
  static component = 'tabs';
  static rootSelector = '.tabs';

  attach() {
    this._last = this.value;
    // The tabs behavior has no event of its own; report aria-selected changes.
    this._unwatch = watch(this.root, ['aria-selected'], () => this.reportValue());
  }

  detach() {
    this._unwatch?.();
  }

  get value() {
    const tab = this.root?.querySelector('[role="tab"][aria-selected="true"]');
    return tab ? keyOf(tab) : null;
  }

  set value(value) {
    if (this.defer(value)) return;
    const tab = [...this.root.querySelectorAll('[role="tab"]')].find((t) => keyOf(t) === String(value));
    if (!tab || !this.root.select) return;
    this.root.select(tab);
    this._last = this.value; // the observer runs later; don't report this change
  }
}

if (!customElements.get('auvyx-tabs')) customElements.define('auvyx-tabs', AuvyxTabs);

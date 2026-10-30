// <auvyx-select>: Web Components edition of Select (see base.js).
// value: the selected option's data-value (an array for multiple selects).
// The behavior's own bubbling `change` (detail.value) reaches listeners on
// <auvyx-select>; setting `value` stays silent.
import { AuvyxWrapper } from './base.js';

class AuvyxSelect extends AuvyxWrapper {
  static component = 'select';
  static rootSelector = '.select';

  get value() {
    return this.root ? this.root.value : null;
  }

  set value(value) {
    if (this.defer(value)) return;
    if (!this.root.select) return;
    this.silently(() => this.root.select(value));
  }
}

if (!customElements.get('auvyx-select')) customElements.define('auvyx-select', AuvyxSelect);

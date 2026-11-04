// <auvyx-combobox>: Web Components edition of Combobox (see base.js).
// value: the selected option's data-value (an array for multiple comboboxes).
import { AuvyxWrapper } from './base.js';

class AuvyxCombobox extends AuvyxWrapper {
  static component = 'combobox';
  static rootSelector = '.combobox';

  get value() {
    return this.root ? this.root.value : null;
  }

  set value(value) {
    if (this.defer(value)) return;
    if (!this.root.setValue) return;
    this.silently(() => this.root.setValue(value));
  }
}

if (!customElements.get('auvyx-combobox')) customElements.define('auvyx-combobox', AuvyxCombobox);

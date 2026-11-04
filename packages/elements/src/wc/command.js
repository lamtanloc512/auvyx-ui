// <auvyx-command>: Web Components edition of Command (see base.js).
// Emits `select` (detail.value: the item's data-value, or its text) when the
// user activates an item, by pointer or keyboard.
import { AuvyxWrapper } from './base.js';

class AuvyxCommand extends AuvyxWrapper {
  static component = 'command';
  static rootSelector = '.command';
  static relayed = [];
  static observedAttributes = [];

  attach() {
    this._onClick = (e) => {
      const item = e.target.closest('[role="menuitem"]');
      if (!item || !this.root.contains(item) || item.matches('[aria-disabled="true"], [data-disabled="true"], [disabled]')) return;
      this.emit('select', { value: item.dataset.value ?? item.textContent.trim() });
    };
    // Enter on the search input clicks the active item, so this covers the keyboard too.
    this.root.addEventListener('click', this._onClick);
  }

  detach() {
    this.root?.removeEventListener('click', this._onClick);
  }

  applyInitial() {}

  restore() {}

  get value() {
    return null;
  }
}

if (!customElements.get('auvyx-command')) customElements.define('auvyx-command', AuvyxCommand);

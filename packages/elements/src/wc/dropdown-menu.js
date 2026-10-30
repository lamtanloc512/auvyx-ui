// <auvyx-dropdown-menu>: Web Components edition of Dropdown Menu (see base.js).
// Wraps the JS markup or the native popover variant. open: whether the menu
// is shown. Also emits `select` (detail.value: the item's data-value, or its
// text) when the user activates a menu item.
import { AuvyxAnchored } from './anchored.js';

class AuvyxDropdownMenu extends AuvyxAnchored {
  static component = 'dropdown-menu';
  static rootSelector = '.dropdown-menu';

  attach() {
    super.attach();
    this._onClick = (e) => {
      const item = e.target.closest('[role^="menuitem"]');
      if (!item || !this.root.contains(item) || item.matches('[aria-disabled="true"], :disabled')) return;
      this.emit('select', { value: item.dataset.value ?? item.textContent.trim() });
    };
    this.root.addEventListener('click', this._onClick);
  }

  detach() {
    super.detach();
    this.root?.removeEventListener('click', this._onClick);
  }

  setOpenJs(open) {
    if (open) this.root.open?.();
    else this.root.close?.();
  }
}

if (!customElements.get('auvyx-dropdown-menu')) customElements.define('auvyx-dropdown-menu', AuvyxDropdownMenu);

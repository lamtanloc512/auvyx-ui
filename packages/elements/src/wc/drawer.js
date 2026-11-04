// <auvyx-drawer>: Web Components edition of Drawer (see base.js).
// Wraps the HTML edition's <dialog class="drawer">. open: whether it is shown.
import { AuvyxOpenWrapper, watch } from './base.js';

class AuvyxDrawer extends AuvyxOpenWrapper {
  static component = 'drawer';
  static rootSelector = 'dialog.drawer';

  attach() {
    this._unwatch = watch(this.root, ['open'], () => this.reportOpen(), false);
  }

  detach() {
    this._unwatch?.();
  }

  isOpen() {
    return Boolean(this.root?.open);
  }

  setOpen(open) {
    if (open) this.root.showModal();
    else this.root.close();
  }
}

if (!customElements.get('auvyx-drawer')) customElements.define('auvyx-drawer', AuvyxDrawer);

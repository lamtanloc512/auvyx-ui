// <auvyx-sidebar>: Web Components edition of Sidebar (see base.js).
// open: whether the sidebar is expanded (data-state="open").
import { AuvyxOpenWrapper } from './base.js';

class AuvyxSidebar extends AuvyxOpenWrapper {
  static component = 'sidebar';
  static rootSelector = '.sidebar';

  attach() {
    this._onState = () => this.reportOpen();
    this.root.addEventListener('basecoat:sidebar', this._onState);
  }

  detach() {
    this.root?.removeEventListener('basecoat:sidebar', this._onState);
  }

  isOpen() {
    return this.root?.dataset.state !== 'collapsed';
  }

  setOpen(open) {
    if (open) this.root.open?.();
    else this.root.close?.();
  }
}

if (!customElements.get('auvyx-sidebar')) customElements.define('auvyx-sidebar', AuvyxSidebar);

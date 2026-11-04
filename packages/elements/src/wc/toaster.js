// <auvyx-toaster>: Web Components edition of Toast (see base.js).
// Wraps the HTML edition's toaster and exposes toast(options), the same
// options as the HTML edition's toaster.toast().
import { AuvyxWrapper } from './base.js';

class AuvyxToaster extends AuvyxWrapper {
  static component = 'toaster';
  static rootSelector = '.toaster';
  static relayed = [];
  static observedAttributes = [];

  applyInitial() {}

  restore() {}

  get value() {
    return null;
  }

  toast(options) {
    return this.root?.toast?.(options);
  }
}

if (!customElements.get('auvyx-toaster')) customElements.define('auvyx-toaster', AuvyxToaster);

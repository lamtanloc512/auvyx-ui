// <auvyx-popover>: Web Components edition of Popover (see base.js).
// Wraps the JS markup or the native popover variant. open: whether the panel is shown.
import { AuvyxAnchored } from './anchored.js';

class AuvyxPopover extends AuvyxAnchored {
  static component = 'popover';
  static rootSelector = '.popover';

  setOpenJs() {
    // The JS popover toggles from its trigger; it has no open/close API.
    this.trigger?.click();
  }
}

if (!customElements.get('auvyx-popover')) customElements.define('auvyx-popover', AuvyxPopover);

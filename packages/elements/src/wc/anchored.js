// Shared by <auvyx-dropdown-menu> and <auvyx-popover>: both wrap either the
// JS markup (trigger aria-expanded) or the zero-JS native variant
// (<div data-popover popover>), and report open/close for both.
import { AuvyxOpenWrapper, watch } from './base.js';

export class AuvyxAnchored extends AuvyxOpenWrapper {
  get trigger() {
    return this.root?.querySelector(':scope > button');
  }

  // Native variant: the panel carries the popover attribute.
  get nativePanel() {
    return this.root?.querySelector(':scope > [data-popover][popover]');
  }

  attach() {
    const panel = this.nativePanel;
    if (panel) {
      this._onToggle = () => this.reportOpen();
      panel.addEventListener('toggle', this._onToggle);
      this._unwatch = () => panel.removeEventListener('toggle', this._onToggle);
    } else {
      this._unwatch = watch(this.trigger, ['aria-expanded'], () => this.reportOpen(), false);
    }
  }

  detach() {
    this._unwatch?.();
  }

  isOpen() {
    const panel = this.nativePanel;
    return panel ? panel.matches(':popover-open') : this.trigger?.getAttribute('aria-expanded') === 'true';
  }

  setOpen(open) {
    const panel = this.nativePanel;
    if (panel) return open ? panel.showPopover() : panel.hidePopover();
    this.setOpenJs(open);
  }
}

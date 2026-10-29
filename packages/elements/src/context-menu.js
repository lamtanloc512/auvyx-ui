// <auvyx-context-menu>: open a native menu popover at the pointer (fork addition).
// Right-click (or long-press where the platform fires contextmenu) on the first
// child opens the menu there; ContextMenu / Shift+F10 opens it at the focused
// element. Everything after opening (keys, dismiss, focus) is native + menu.js.
class AuvyxContextMenu extends HTMLElement {
  connectedCallback() {
    if (this._init) return;
    this._init = true;
    this.menu = this.querySelector('[data-popover][popover]');
    if (!this.menu) return;
    // Where contextmenu fires on pointerdown (Linux, macOS), the following
    // pointerup would light-dismiss a popover opened right away: wait for it.
    let pressed = false;
    this.addEventListener('pointerdown', (e) => { if (e.button === 2) pressed = true; });
    this.addEventListener('contextmenu', (event) => {
      if (this.menu.contains(event.target)) return;
      event.preventDefault();
      const { clientX: x, clientY: y } = event;
      if (!pressed) return this.openAt(x, y);
      window.addEventListener('pointerup', () => {
        pressed = false;
        setTimeout(() => this.openAt(x, y));
      }, { once: true, capture: true });
    });
    this.addEventListener('keydown', (event) => {
      if (this.menu.contains(event.target)) return;
      if (event.key === 'ContextMenu' || (event.shiftKey && event.key === 'F10')) {
        event.preventDefault();
        const r = event.target.getBoundingClientRect();
        this.openAt(r.left, r.bottom);
      }
    });
  }

  openAt(x, y) {
    const menu = this.menu;
    if (menu.matches(':popover-open')) menu.hidePopover();
    Object.assign(menu.style, {
      position: 'fixed',
      inset: 'auto',
      margin: '0',
      positionArea: 'none',
      positionTryFallbacks: 'none',
      left: `${x}px`,
      top: `${y}px`,
    });
    menu.showPopover();
    // Keep it on screen: flip toward the pointer when it would overflow.
    const r = menu.getBoundingClientRect();
    if (r.right > innerWidth - 4) menu.style.left = `${Math.max(4, x - r.width)}px`;
    if (r.bottom > innerHeight - 4) menu.style.top = `${Math.max(4, y - r.height)}px`;
  }
}

if (!customElements.get('auvyx-context-menu')) customElements.define('auvyx-context-menu', AuvyxContextMenu);

// Web Components edition (fork addition).
//
// <auvyx-*> elements wrap the HTML edition's markup unchanged and give
// frameworks a component interface on top of the same behavior:
//
//   <auvyx-tabs value="account">
//     <div class="tabs">…the HTML edition's tabs markup…</div>
//   </auvyx-tabs>
//
// - `value` property and attribute (setting it does not fire `change`, like
//   native inputs)
// - a bubbling `change` event with `detail.value` when the user changes it
// - cleanup on disconnect, and a fresh init when moved or re-attached
// The wrapper is `display: contents`, so layout is the HTML edition's.
export class AuvyxWrapper extends HTMLElement {
  static observedAttributes = ['value'];

  // Subclasses set: component (Basecoat registry name), rootSelector.
  connectedCallback() {
    // Upgraded while the parser is still inside us: wait for the children.
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.isConnected && this.connectedCallback(), { once: true });
      return;
    }
    this.root = this.querySelector(`:scope > ${this.constructor.rootSelector}`);
    if (!this.root) return;
    if (!this._relay) {
      // The behavior's change event starts on the inner root. Stop it in the
      // capture phase, before any listener (frameworks may listen on this
      // element itself), and re-emit it from the element so e.target is
      // <auvyx-*>: React and others only map onChange for events targeting the
      // custom element. Changes caused by a programmatic `value` set are dropped.
      this._relay = (e) => {
        if (e.target !== this.root || !(e instanceof CustomEvent)) return;
        e.stopImmediatePropagation();
        if (!this._silent) this.emitChange(this.value);
      };
      this.addEventListener('change', this._relay, true);
    }
    window.basecoat?.init(this.constructor.component);
    this.attach?.();
    // Frameworks may set `value` before the element is connected; apply it now.
    const initial = this._pending !== undefined ? this._pending : this.getAttribute('value');
    this._pending = undefined;
    if (initial !== null) this.value = initial;
  }

  disconnectedCallback() {
    this.detach?.();
    if (!this.root) return;
    this.root._destroy?.();
    // Let the behavior initialize again if this element is re-attached.
    delete this.root.dataset[`${this.constructor.component.replace(/-(\w)/g, (_, c) => c.toUpperCase())}Initialized`];
    this.root = null;
  }

  attributeChangedCallback(name, previous, next) {
    if (name === 'value' && this.root && next !== null && next !== this.value) this.value = next;
  }

  // For subclasses' `value` setters: remember a value set before connect.
  defer(value) {
    if (this.root) return false;
    this._pending = value;
    return true;
  }

  silently(fn) {
    this._silent = true;
    try { fn(); } finally { this._silent = false; }
  }

  emitChange(value) {
    this.dispatchEvent(new CustomEvent('change', { detail: { value }, bubbles: true }));
  }
}

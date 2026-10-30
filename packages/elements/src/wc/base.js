// Web Components edition (fork addition).
//
// <auvyx-*> elements wrap the HTML edition's markup unchanged and give
// frameworks a component interface on top of the same behavior:
//
//   <auvyx-tabs value="account">
//     <div class="tabs">…the HTML edition's tabs markup…</div>
//   </auvyx-tabs>
//
// Value components (AuvyxWrapper): a `value` property and attribute; a
// bubbling `change` event (detail.value) when the user changes it; setting
// `value` from code fires nothing, like native inputs.
// Open/close components (AuvyxOpenWrapper): an `open` property and boolean
// attribute; a `toggle` event (detail.open) whenever the state changes, like
// <details> and <dialog>.
// Both clean up on disconnect and initialize again when re-attached. The
// wrapper is `display: contents`, so layout is the HTML edition's.
export class AuvyxWrapper extends HTMLElement {
  static observedAttributes = ['value'];
  // Subclasses set: component (Basecoat registry name), rootSelector.
  // Events from the root that are re-emitted from this element.
  static relayed = ['change'];
  // Also relay native (non-custom) events, for wrappers around form controls.
  static relayNative = false;

  connectedCallback() {
    // Upgraded while the parser is still inside us: wait for the children.
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.isConnected && this.connectedCallback(), { once: true });
      return;
    }
    this.setup();
    // Frameworks may replace the markup inside (v-html, keyed re-renders,
    // re-hydration). Follow the new root and carry the state over.
    this._children = new MutationObserver(() => {
      if (this.querySelector(`:scope > ${this.constructor.rootSelector}`) === this.root) return;
      const state = this.root ? this.snapshot() : undefined;
      this.teardown();
      this.setup(state);
    });
    this._children.observe(this, { childList: true });
  }

  disconnectedCallback() {
    this._children?.disconnect();
    this.teardown();
  }

  setup(state) {
    this.root = this.querySelector(`:scope > ${this.constructor.rootSelector}`);
    if (!this.root) return;
    window.basecoat?.init(this.constructor.component);
    // Events start on the inner root. Catch them on the root itself, after the
    // behavior's own listeners there have run, stop them from bubbling (so
    // frameworks listening on this element see one event), and re-emit them
    // from the element so e.target is <auvyx-*>: React and others only map
    // onChange for events targeting the custom element. Events caused by
    // setting a property from code are dropped.
    this._relay = (e) => {
      if (e.target !== this.root || (!this.constructor.relayNative && !(e instanceof CustomEvent))) return;
      e.stopPropagation();
      if (!this._silent) this.emit(e.type, { value: this.value });
    };
    for (const type of this.constructor.relayed) this.root.addEventListener(type, this._relay);
    this.attach?.();
    if (state !== undefined) this.restore(state);
    else this.applyInitial();
  }

  teardown() {
    this.detach?.();
    if (!this.root) return;
    for (const type of this.constructor.relayed) this.root.removeEventListener(type, this._relay);
    this.root._destroy?.();
    // Let the behavior initialize again if this root is re-attached.
    delete this.root.dataset[`${this.constructor.component.replace(/-(\w)/g, (_, c) => c.toUpperCase())}Initialized`];
    this.root = null;
  }

  // Frameworks may set properties before the element is connected; apply them now.
  applyInitial() {
    const initial = this._pending !== undefined ? this._pending : this.getAttribute('value');
    this._pending = undefined;
    if (initial !== null) this.value = initial;
  }

  // State carried over when the inner markup is replaced.
  snapshot() {
    return this.value;
  }

  restore(value) {
    if (value !== null) this.value = value;
  }

  attributeChangedCallback(name, previous, next) {
    if (name === 'value' && this.root && next !== null && next !== this.value) this.value = next;
  }

  // For subclasses' setters: remember a value set before connect.
  defer(value) {
    if (this.root) return false;
    this._pending = value;
    return true;
  }

  silently(fn) {
    this._silent = true;
    try { fn(); } finally { this._silent = false; }
  }

  emit(type, detail) {
    this.dispatchEvent(new CustomEvent(type, { detail, bubbles: true }));
  }

  // Value components whose behavior has no change event of their own:
  // call after any possible change; emits when it was the user's.
  reportValue() {
    const value = this.value;
    if (JSON.stringify(value) === JSON.stringify(this._last)) return;
    this._last = value;
    if (!this._silent) this.emit('change', { value });
  }
}

export class AuvyxOpenWrapper extends AuvyxWrapper {
  static observedAttributes = ['open'];
  static relayed = [];
  // Subclasses implement: isOpen(), setOpen(open).

  applyInitial() {
    const initial = this._pending !== undefined ? this._pending : this.hasAttribute('open') || null;
    this._pending = undefined;
    this._lastOpen = this.isOpen();
    if (initial !== null && Boolean(initial) !== this._lastOpen) this.open = initial;
  }

  attributeChangedCallback(name, previous, next) {
    if (name === 'open' && this.root) this.open = next !== null;
  }

  snapshot() {
    return this.isOpen();
  }

  restore(open) {
    this._lastOpen = this.isOpen();
    this.open = open;
  }

  get open() {
    return this.root ? this.isOpen() : Boolean(this._pending);
  }

  set open(open) {
    if (this.defer(Boolean(open))) return;
    if (Boolean(open) !== this.isOpen()) this.setOpen(Boolean(open));
  }

  // Call after any possible open/close; emits `toggle` when the state changed.
  reportOpen() {
    const open = this.isOpen();
    if (open === this._lastOpen) return;
    this._lastOpen = open;
    this.emit('toggle', { open });
  }
}

// Watch attributes under `root` and call `fn` on change; returns a disconnect function.
export function watch(root, attributeFilter, fn, subtree = true) {
  const observer = new MutationObserver(fn);
  observer.observe(root, { attributes: true, attributeFilter, subtree });
  return () => observer.disconnect();
}

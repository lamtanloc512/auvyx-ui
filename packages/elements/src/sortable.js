// <auvyx-sortable>: drag and drop between the lists inside it (fork addition).
// Every <ol>/<ul> inside (not nested in an item) is a drop zone and its <li>
// children are the items; a kanban board is one element around its columns.
// Pointer: drag an item, or its [data-drag-handle] when it has one; touch
// starts after a short press so the page still scrolls. Keyboard: Space picks
// up the focused item, arrows move it (Left/Right between lists), Space or
// Enter drops, Escape cancels. Emits a cancelable `sort` event on drop.
// Not part of auvyx.min.js: load js/sortable.min.js where you need it.
const ITEM_FOCUSABLE = 'a[href], button, input, select, textarea, [tabindex]';
const PRESS_MS = 220;
const EDGE = 48;

class AuvyxSortable extends HTMLElement {
  connectedCallback() {
    if (this._init) return;
    this._init = true;
    this.live = document.createElement('span');
    this.live.className = 'sr-only';
    this.live.setAttribute('role', 'status');
    this.append(this.live);
    this.addEventListener('pointerdown', (e) => this.onPointerDown(e));
    this.addEventListener('keydown', (e) => this.onKeydown(e));
    this.addEventListener('click', (e) => { if (this.justDropped) { e.preventDefault(); e.stopPropagation(); } }, true);
    this.refresh();
  }

  // Re-scan after the app adds lists or items.
  refresh() {
    this.zones().forEach((zone) => [...zone.children].forEach((item) => {
      if (item.tagName === 'LI' && !item.querySelector(ITEM_FOCUSABLE) && !item.hasAttribute('tabindex')) item.tabIndex = 0;
    }));
    this.updateCounts();
  }

  // Lists nested inside an item (a checklist on a card) are not drop zones.
  zones() {
    return [...this.querySelectorAll('ol, ul')].filter((list) => {
      const owner = list.parentElement.closest('li');
      return !owner || !this.contains(owner);
    });
  }

  items(zone) {
    return [...zone.children].filter((el) => el.tagName === 'LI' && !el.hidden && !el.hasAttribute('data-drag-ghost'));
  }

  isDisabled(item) {
    return item.getAttribute('aria-disabled') === 'true' || item.hasAttribute('data-drag-disabled');
  }

  zoneOf(item) {
    return item?.parentElement && this.zones().includes(item.parentElement) ? item.parentElement : null;
  }

  itemFrom(target) {
    const item = target.closest?.('li');
    return item && this.zoneOf(item) ? item : null;
  }

  label(el, fallback) {
    const ref = el.getAttribute('aria-labelledby') || el.closest('[aria-labelledby]')?.getAttribute('aria-labelledby');
    const text = el.dataset.dragLabel || el.getAttribute('aria-label') || (ref && document.getElementById(ref)?.textContent)
      || el.querySelector('strong, h3, h4, a')?.textContent || fallback;
    return (text || '').trim().replace(/\s+/g, ' ').slice(0, 60);
  }

  where(item) {
    const zone = this.zoneOf(item);
    const zones = this.zones();
    const name = this.label(zone, `list ${zones.indexOf(zone) + 1}`);
    return `${name}, position ${this.items(zone).indexOf(item) + 1} of ${this.items(zone).length}`;
  }

  say(text) {
    this.live.textContent = '';
    requestAnimationFrame(() => { this.live.textContent = text; });
  }

  updateCounts() {
    this.zones().forEach((zone) => {
      const count = zone.parentElement.querySelector(':scope > * [data-drag-count], :scope > [data-drag-count]');
      if (count) count.textContent = String(this.items(zone).length);
    });
  }

  begin(item) {
    this.origin = { item, zone: item.parentElement, next: item.nextElementSibling, index: this.items(item.parentElement).indexOf(item) };
    item.setAttribute('data-dragging', '');
    this.setAttribute('data-sorting', '');
  }

  // Emit `sort`; a listener's preventDefault() puts the item back.
  finish(cancel) {
    const { item, zone, next, index } = this.origin || {};
    this.origin = null;
    if (!item) return;
    item.removeAttribute('data-dragging');
    item.removeAttribute('data-grabbed');
    this.removeAttribute('data-sorting');
    const to = item.parentElement;
    const moved = to !== zone || item.nextElementSibling !== next;
    const detail = { item, from: zone, to, index: this.items(to).indexOf(item), previousIndex: index };
    if (moved && !cancel) {
      if (this.dispatchEvent(new CustomEvent('sort', { detail, cancelable: true, bubbles: true }))) {
        this.updateCounts();
        return true;
      }
    }
    zone.insertBefore(item, next && next.parentElement === zone ? next : null);
    this.updateCounts();
    return false;
  }

  // ---- Pointer
  onPointerDown(e) {
    if (e.button !== 0 || this.origin) return;
    const item = this.itemFrom(e.target);
    if (!item || this.isDisabled(item)) return;
    const handle = item.querySelector('[data-drag-handle]');
    if (handle ? !handle.contains(e.target) : e.target.closest('button, input, select, textarea, [contenteditable]')) return;
    const start = { x: e.clientX, y: e.clientY };
    const touch = e.pointerType === 'touch';
    let pressed = !touch;
    let dragging = false;
    const timer = touch && setTimeout(() => { pressed = true; }, PRESS_MS);
    const blockScroll = (ev) => { if (dragging) ev.preventDefault(); };
    if (touch) document.addEventListener('touchmove', blockScroll, { passive: false });

    const move = (ev) => {
      if (!dragging) {
        const far = Math.hypot(ev.clientX - start.x, ev.clientY - start.y) > 4;
        if (!far) return;
        if (!pressed) return cleanup(); // a touch that moved early is a scroll
        dragging = true;
        this.begin(item);
        this.ghost = this.makeGhost(item, start);
      }
      this.pointer = { x: ev.clientX, y: ev.clientY };
      this.ghost.style.translate = `${ev.clientX - this.ghost._dx}px ${ev.clientY - this.ghost._dy}px`;
      this.place(item, ev.clientX, ev.clientY);
    };
    const up = () => {
      const wasDragging = dragging;
      cleanup();
      if (!wasDragging) return;
      this.finish(false);
      // Swallow the click that follows a drag so a linked card does not open.
      this.justDropped = true;
      setTimeout(() => { this.justDropped = false; }, 0);
    };
    const key = (ev) => { if (ev.key === 'Escape' && dragging) { cleanup(); this.finish(true); } };
    const cleanup = () => {
      clearTimeout(timer);
      cancelAnimationFrame(this.scrollFrame);
      document.removeEventListener('pointermove', move);
      document.removeEventListener('pointerup', up);
      document.removeEventListener('pointercancel', up);
      document.removeEventListener('keydown', key);
      document.removeEventListener('touchmove', blockScroll);
      this.ghost?.remove();
      this.ghost = null;
      dragging = false;
    };
    document.addEventListener('pointermove', move);
    document.addEventListener('pointerup', up);
    document.addEventListener('pointercancel', up);
    document.addEventListener('keydown', key);
    this.autoScroll();
  }

  makeGhost(item, start) {
    const rect = item.getBoundingClientRect();
    const ghost = item.cloneNode(true);
    ghost.removeAttribute('id');
    ghost.removeAttribute('data-dragging');
    ghost.setAttribute('data-drag-ghost', '');
    ghost.setAttribute('aria-hidden', 'true');
    ghost.style.width = `${rect.width}px`;
    ghost._dx = start.x - rect.left;
    ghost._dy = start.y - rect.top;
    ghost.style.translate = `${rect.left}px ${rect.top}px`;
    item.parentElement.append(ghost);
    return ghost;
  }

  // Move the item to where the pointer is: before the item under it, or at the end of an empty list.
  place(item, x, y) {
    const zone = this.zones().find((z) => {
      const r = z.getBoundingClientRect();
      return x >= r.left && x <= r.right && y >= r.top && y <= r.bottom;
    }) || this.zones().find((z) => {
      const r = z.parentElement.getBoundingClientRect();
      return x >= r.left && x <= r.right && y >= r.top && y <= r.bottom;
    });
    if (!zone) return;
    const horizontal = /row/.test(getComputedStyle(zone).flexDirection) && getComputedStyle(zone).display.includes('flex');
    const others = this.items(zone).filter((el) => el !== item);
    const before = others.find((el) => {
      const r = el.getBoundingClientRect();
      return horizontal ? x < r.left + r.width / 2 : y < r.top + r.height / 2;
    });
    if (before) { if (item.nextElementSibling !== before) zone.insertBefore(item, before); }
    else if (this.items(zone).at(-1) !== item) zone.append(item);
  }

  // Scroll the list or board under the pointer when it nears an edge.
  autoScroll() {
    const tick = () => {
      if (this.ghost && this.pointer) {
        const { x, y } = this.pointer;
        for (let el = document.elementFromPoint(x, y); el && el !== document.body; el = el.parentElement) {
          const r = el.getBoundingClientRect();
          const s = getComputedStyle(el);
          if (/(auto|scroll)/.test(s.overflowY) && el.scrollHeight > el.clientHeight) {
            if (y < r.top + EDGE) el.scrollTop -= 10; else if (y > r.bottom - EDGE) el.scrollTop += 10;
          }
          if (/(auto|scroll)/.test(s.overflowX) && el.scrollWidth > el.clientWidth) {
            if (x < r.left + EDGE) el.scrollLeft -= 12; else if (x > r.right - EDGE) el.scrollLeft += 12;
          }
        }
      }
      this.scrollFrame = requestAnimationFrame(tick);
    };
    this.scrollFrame = requestAnimationFrame(tick);
  }

  // ---- Keyboard
  onKeydown(e) {
    const item = this.itemFrom(e.target);
    if (!item || (e.target !== item && !e.target.matches('a, [data-drag-handle]'))) return;
    const grabbed = this.origin?.item === item;
    if (!grabbed) {
      if (e.key !== ' ' || this.isDisabled(item) || this.origin) return;
      e.preventDefault();
      this.begin(item);
      item.setAttribute('data-grabbed', '');
      return this.say(`Picked up ${this.label(item, 'item')}. ${this.where(item)}. Arrow keys move, Space drops, Escape cancels.`);
    }
    const zones = this.zones();
    const zone = item.parentElement;
    const list = this.items(zone);
    const i = list.indexOf(item);
    const rtl = getComputedStyle(this).direction === 'rtl';
    const step = { ArrowLeft: rtl ? 1 : -1, ArrowRight: rtl ? -1 : 1 }[e.key];
    if (e.key === ' ' || e.key === 'Enter' || e.key === 'Escape') {
      e.preventDefault();
      const kept = this.finish(e.key === 'Escape');
      // Moving a node drops its focus: put it back on the card.
      (e.target.isConnected ? e.target : item).focus();
      this.say(e.key === 'Escape' || !kept ? `Cancelled. ${this.where(item)}.` : `Dropped. ${this.where(item)}.`);
    } else if (e.key === 'ArrowUp' && i > 0) zone.insertBefore(item, list[i - 1]);
    else if (e.key === 'ArrowDown' && i < list.length - 1) zone.insertBefore(item, list[i + 1].nextElementSibling);
    else if (step) {
      const target = zones[zones.indexOf(zone) + step];
      if (!target) return;
      const items = this.items(target);
      target.insertBefore(item, items[Math.min(i, items.length)] ?? null);
    } else return;
    e.preventDefault();
    if (e.key.startsWith('Arrow')) {
      (e.target === item ? item : item.querySelector('a, [data-drag-handle]') || item).focus({ preventScroll: false });
      this.say(this.where(item));
    }
  }
}

if (!customElements.get('auvyx-sortable')) customElements.define('auvyx-sortable', AuvyxSortable);

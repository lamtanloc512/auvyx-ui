// Keyboard model for native menus (fork addition).
//
// The native popover variant already opens, closes, light-dismisses and
// returns focus. This adds what menus need on top, for every
// `[data-popover][popover]` that contains `[role=menu]` (dropdown, menubar,
// context menu) and for `.navigation-menu`:
// - focus the first item on open; ArrowDown/ArrowUp/Home/End move between items
// - ArrowDown/ArrowUp on a trigger opens its menu (first/last item)
// - activating an item closes the menu; menuitemcheckbox/radio toggle aria-checked
// - menubar: ArrowLeft/ArrowRight move between top-level menus, hover switches
//   menus while one is open
// - navigation menu: opens on hover for mouse users (click still works)
// One set of delegated listeners, so it covers content added later.
(() => {
  if (window.__auvyxMenu) return;
  window.__auvyxMenu = true;

  const ITEM = '[role="menuitem"], [role="menuitemcheckbox"], [role="menuitemradio"]';
  const MENU_POPOVER = '[data-popover][popover]';

  const isUsable = (el) => !el.disabled && el.getAttribute('aria-disabled') !== 'true' && !el.closest('[hidden]');
  const itemsOf = (popover) => [...popover.querySelectorAll(ITEM)].filter(isUsable);
  const triggerOf = (popover) => (popover.id ? document.querySelector(`[popovertarget="${CSS.escape(popover.id)}"]`) : null);
  const popoverOf = (trigger) => {
    const id = trigger?.getAttribute('popovertarget');
    return id ? document.getElementById(id) : null;
  };
  const isMenuPopover = (el) => el instanceof HTMLElement && el.matches(MENU_POPOVER) && el.querySelector('[role="menu"]');
  const menubarOf = (el) => el?.closest('.menubar');
  const menubarTriggers = (bar) => [...bar.querySelectorAll(':scope > .dropdown-menu > [popovertarget]')];
  const focusItem = (item) => item?.focus({ preventScroll: true });

  const open = (trigger, focus = 'first') => {
    const popover = popoverOf(trigger);
    if (!popover) return;
    popover.dataset.focusOnOpen = focus;
    if (!popover.matches(':popover-open')) popover.showPopover({ source: trigger });
    else focusItem(focus === 'last' ? itemsOf(popover).at(-1) : itemsOf(popover)[0]);
  };

  // toggle does not bubble; a capturing listener on document still sees it.
  document.addEventListener('toggle', (event) => {
    const popover = event.target;
    if (!(popover instanceof HTMLElement) || !popover.matches(MENU_POPOVER)) return;
    const trigger = triggerOf(popover);
    if (trigger && trigger.hasAttribute('aria-haspopup')) trigger.setAttribute('aria-expanded', String(event.newState === 'open'));
    if (event.newState !== 'open' || !isMenuPopover(popover)) return;
    const where = popover.dataset.focusOnOpen || 'first';
    delete popover.dataset.focusOnOpen;
    if (where === 'none') return;
    requestAnimationFrame(() => {
      const items = itemsOf(popover);
      focusItem(where === 'last' ? items.at(-1) : items[0]);
    });
  }, true);

  document.addEventListener('keydown', (event) => {
    const target = event.target;
    if (!(target instanceof Element)) return;
    const popover = target.closest(MENU_POPOVER);

    // Inside an open menu
    if (popover && isMenuPopover(popover) && target.matches(ITEM)) {
      const items = itemsOf(popover);
      const index = items.indexOf(target);
      const move = { ArrowDown: index + 1, ArrowUp: index - 1, Home: 0, End: items.length - 1 }[event.key];
      if (move !== undefined) {
        event.preventDefault();
        focusItem(items[(move + items.length) % items.length]);
        return;
      }
      if (event.key === 'Tab') {
        popover.hidePopover();
        return;
      }
      // Return focus to this menu's own trigger (after a menubar switch the
      // browser would restore focus to the first menu's trigger instead).
      if (event.key === 'Escape') {
        event.preventDefault();
        popover.hidePopover();
        triggerOf(popover)?.focus({ preventScroll: true });
        return;
      }
      const bar = menubarOf(triggerOf(popover));
      if (bar && (event.key === 'ArrowRight' || event.key === 'ArrowLeft')) {
        event.preventDefault();
        const triggers = menubarTriggers(bar);
        const at = triggers.indexOf(triggerOf(popover));
        const rtl = getComputedStyle(bar).direction === 'rtl';
        const step = (event.key === 'ArrowRight') !== rtl ? 1 : -1;
        const next = triggers[(at + step + triggers.length) % triggers.length];
        popover.hidePopover();
        open(next);
        return;
      }
      return;
    }

    // On a trigger
    if (target.matches('[popovertarget]')) {
      const menu = popoverOf(target);
      const bar = menubarOf(target);
      if (menu && isMenuPopover(menu) && (event.key === 'ArrowDown' || event.key === 'ArrowUp')) {
        event.preventDefault();
        open(target, event.key === 'ArrowUp' ? 'last' : 'first');
        return;
      }
      if (bar && (event.key === 'ArrowRight' || event.key === 'ArrowLeft' || event.key === 'Home' || event.key === 'End')) {
        event.preventDefault();
        const triggers = menubarTriggers(bar);
        const at = triggers.indexOf(target);
        const rtl = getComputedStyle(bar).direction === 'rtl';
        const step = (event.key === 'ArrowRight') !== rtl ? 1 : -1;
        const next = event.key === 'Home' ? triggers[0] : event.key === 'End' ? triggers.at(-1) : triggers[(at + step + triggers.length) % triggers.length];
        next.focus();
      }
    }
  });

  // Activating an item closes its menu; checkable items toggle.
  document.addEventListener('click', (event) => {
    const item = event.target instanceof Element && event.target.closest(ITEM);
    if (!item || !isUsable(item)) return;
    const popover = item.closest(MENU_POPOVER);
    if (!popover) return;
    const role = item.getAttribute('role');
    if (role === 'menuitemcheckbox') {
      item.setAttribute('aria-checked', String(item.getAttribute('aria-checked') !== 'true'));
    } else if (role === 'menuitemradio') {
      const group = item.closest('[role="group"]') || popover;
      group.querySelectorAll('[role="menuitemradio"]').forEach((radio) => radio.setAttribute('aria-checked', String(radio === item)));
    }
    if (item.hasAttribute('popovertarget') || item.hasAttribute('data-keep-open')) return;
    if (role !== 'menuitem' && !item.hasAttribute('data-close')) return;
    popover.hidePopover();
    triggerOf(popover)?.focus({ preventScroll: true });
  });

  // Menubar: hovering another trigger while a menu is open switches menus.
  document.addEventListener('pointerover', (event) => {
    const trigger = event.target instanceof Element && event.target.closest('.menubar > .dropdown-menu > [popovertarget]');
    if (!trigger) return;
    const bar = menubarOf(trigger);
    const openMenu = menubarTriggers(bar).map(popoverOf).find((p) => p?.matches(':popover-open'));
    if (!openMenu || openMenu === popoverOf(trigger)) return;
    openMenu.hidePopover();
    open(trigger, 'none');
  });

  // Navigation menu: hover to open for mouse users, with intent delays.
  const navTimers = new WeakMap();
  const clearNav = (li) => clearTimeout(navTimers.get(li));
  document.addEventListener('pointerover', (event) => {
    if (event.pointerType !== 'mouse') return;
    const li = event.target instanceof Element && event.target.closest('.navigation-menu > ul > li');
    if (!li) return;
    clearNav(li);
    const trigger = li.querySelector(':scope > [popovertarget]');
    const panel = popoverOf(trigger);
    if (!panel || panel.matches(':popover-open')) return;
    navTimers.set(li, setTimeout(() => {
      panel.dataset.openedByHover = String(Date.now());
      panel.showPopover({ source: trigger });
    }, 120));
  });
  document.addEventListener('pointerout', (event) => {
    if (event.pointerType !== 'mouse') return;
    const li = event.target instanceof Element && event.target.closest('.navigation-menu > ul > li');
    if (!li || li.contains(event.relatedTarget)) return;
    clearNav(li);
    const panel = popoverOf(li.querySelector(':scope > [popovertarget]'));
    if (!panel || !panel.dataset.openedByHover) return;
    navTimers.set(li, setTimeout(() => {
      if (panel.matches(':popover-open') && !li.matches(':hover')) panel.hidePopover();
      delete panel.dataset.openedByHover;
    }, 200));
  });
  // A click right after a hover-open would toggle the panel shut; keep it open.
  document.addEventListener('click', (event) => {
    const trigger = event.target instanceof Element && event.target.closest('.navigation-menu > ul > li > [popovertarget]');
    const panel = popoverOf(trigger);
    if (!panel?.dataset.openedByHover) return;
    if (Date.now() - Number(panel.dataset.openedByHover) < 600 && panel.matches(':popover-open')) {
      event.preventDefault(); // still hover-driven: leaving closes it
      return;
    }
    delete panel.dataset.openedByHover; // a deliberate click takes over
  }, true);
})();

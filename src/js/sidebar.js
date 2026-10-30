(() => {
  const initSidebar = (sidebarComponent) => {
    if (sidebarComponent.dataset.sidebarInitialized && typeof sidebarComponent.toggle === 'function') return;

    // In-flow sidebars (inside a dialog, popover or layout cell) have no open state.
    if (sidebarComponent.dataset.position === 'static') {
      sidebarComponent.dataset.sidebarInitialized = 'true';
      return;
    }

    const initialOpen = sidebarComponent.dataset.initialOpen !== 'false';
    const initialMobileOpen = sidebarComponent.dataset.initialMobileOpen === 'true';
    const breakpoint = parseInt(sidebarComponent.dataset.breakpoint) || 768;

    let open = breakpoint > 0
      ? (window.innerWidth >= breakpoint ? initialOpen : initialMobileOpen)
      : initialOpen;

    // Collapsing to an icon rail keeps the sidebar usable on desktop.
    const isIconRail = () => sidebarComponent.dataset.collapsible === 'icon' && (breakpoint <= 0 || window.innerWidth >= breakpoint);

    const updateState = () => {
      const rail = isIconRail();
      // An icon rail stays visible to assistive tech; only a fully hidden sidebar is aria-hidden.
      sidebarComponent.setAttribute('aria-hidden', String(!open && !rail));
      sidebarComponent.dataset.state = open ? 'open' : 'collapsed';
      if (open || rail) {
        sidebarComponent.removeAttribute('inert');
      } else {
        sidebarComponent.setAttribute('inert', '');
      }
      if (sidebarComponent.id) {
        document.querySelectorAll(`[data-sidebar-toggle="${CSS.escape(sidebarComponent.id)}"]`).forEach((btn) => btn.setAttribute('aria-expanded', String(open)));
      }
      sidebarComponent.dispatchEvent(new CustomEvent('basecoat:sidebar', { detail: { open } }));
    };

    const setState = (state) => {
      open = Boolean(state);
      updateState();
    };

    sidebarComponent.open = () => setState(true);
    sidebarComponent.close = () => setState(false);
    sidebarComponent.toggle = () => setState(!open);

    const handleClick = (event) => {
      const target = event.target;
      const nav = sidebarComponent.querySelector(':scope > nav');
      const isMobile = window.innerWidth < breakpoint;

      if (isMobile && target.closest('a, button') && !target.closest('[data-keep-mobile-sidebar-open]')) {
        if (document.activeElement) document.activeElement.blur();
        sidebarComponent.close();
        return;
      }

      // Collapsed icon rail: opening a submenu expands the sidebar first.
      if (!open && isIconRail() && target.closest('summary')) {
        event.preventDefault();
        sidebarComponent.open();
        target.closest('details').open = true;
        return;
      }

      if (target === sidebarComponent || (nav && !nav.contains(target))) {
        if (document.activeElement) document.activeElement.blur();
        sidebarComponent.close();
      }
    };

    sidebarComponent.addEventListener('click', handleClick);

    sidebarComponent._destroy = () => {
      sidebarComponent.removeEventListener('click', handleClick);
      delete sidebarComponent.open;
      delete sidebarComponent.close;
      delete sidebarComponent.toggle;
    };

    updateState();
    sidebarComponent.dataset.sidebarInitialized = 'true';
    sidebarComponent.dispatchEvent(new CustomEvent('basecoat:initialized'));
  };

  // Declarative toggles: <button data-sidebar-toggle="sidebar-id"> (empty value = first sidebar).
  const sidebarFor = (id) => (id ? document.getElementById(id) : document.querySelector('.sidebar:not([data-position="static"])'));
  document.addEventListener('click', (event) => {
    const button = event.target.closest('[data-sidebar-toggle]');
    if (!button) return;
    sidebarFor(button.getAttribute('data-sidebar-toggle'))?.toggle?.();
  });
  // Ctrl/Cmd+B toggles the first sidebar (opt out with data-shortcut="none").
  document.addEventListener('keydown', (event) => {
    if (event.key.toLowerCase() !== 'b' || !(event.metaKey || event.ctrlKey) || event.altKey || event.shiftKey) return;
    if (event.target.closest('input, textarea, select, [contenteditable]')) return;
    const sidebar = sidebarFor('');
    if (!sidebar || sidebar.dataset.shortcut === 'none' || typeof sidebar.toggle !== 'function') return;
    event.preventDefault();
    sidebar.toggle();
  });

  if (window.basecoat) {
    window.basecoat.register('sidebar', '.sidebar', initSidebar);
  }
})();

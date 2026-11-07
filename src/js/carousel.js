// Carousel and lightbox (fork addition).
//
// Optional: a .carousel scrolls, snaps and swipes with CSS alone. This adds
// what CSS cannot: controls the page provides, mouse dragging, autoplay, loop,
// keyboard, thumbnails kept in sync, and a lightbox for linked images.
//
//   <section class="carousel" aria-roledescription="carousel" aria-label="Photos"
//            data-loop data-autoplay="5000">
//     <ol><li aria-roledescription="slide" aria-label="1 of 3">…</li>…</ol>
//     <button type="button" data-carousel="prev" aria-label="Previous slide">…</button>
//     <button type="button" data-carousel="next" aria-label="Next slide">…</button>
//     <button type="button" data-carousel="play" aria-label="Pause slideshow">…</button>
//     <div data-carousel-dots></div>
//     <span data-carousel-counter></span>
//   </section>
//
// data-loop wraps around; data-autoplay[="ms"] advances (pauses on hover,
// focus, hidden tabs and prefers-reduced-motion); data-no-drag turns off mouse
// dragging. A carousel with data-carousel-for="<id>" is the thumbnail strip of
// that carousel. Links with data-lightbox[="group"] open their href in a
// full-screen viewer with every link of the same group.
//
// API on the root: goTo(page), goToSlide(index), next(), prev(), play(), pause().
// Event: carousel:change { page, slide, pages }.
(() => {
  const ICONS = {
    prev: '<path d="m15 18-6-6 6-6"/>',
    next: '<path d="m9 18 6-6-6-6"/>',
    close: '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
  };
  const svg = (paths) => `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths}</svg>`;
  const reducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const initCarousel = (root) => {
    if (root.dataset.carouselInitialized) return;
    const track = root.querySelector(':scope > ol, :scope > ul');
    if (!track) return;

    const vertical = root.dataset.orientation === 'vertical';
    const rtl = () => getComputedStyle(root).direction === 'rtl';
    const loop = () => root.hasAttribute('data-loop') || root.hasAttribute('data-autoplay');
    const slides = () => Array.from(track.children).filter((el) => !el.hidden);
    const offset = (el) => (vertical ? el.offsetTop - track.firstElementChild.offsetTop : el.offsetLeft - track.firstElementChild.offsetLeft);
    const scrollPos = () => (vertical ? track.scrollTop : track.scrollLeft);
    const maxScroll = () => (vertical ? track.scrollHeight - track.clientHeight : track.scrollWidth - track.clientWidth);
    // Snap positions, one per page: slides past the last full page share it.
    const stops = () => {
      const max = maxScroll();
      const out = [];
      for (const s of slides()) {
        const p = Math.sign(offset(s)) * Math.min(Math.abs(offset(s)), max);
        if (!out.length || Math.abs(p - out[out.length - 1]) > 1) out.push(p);
      }
      return out.length ? out : [0];
    };
    const nearest = (list, value) => list.reduce((best, p, i) => (Math.abs(p - value) < Math.abs(list[best] - value) ? i : best), 0);
    const scrollTo = (value, smooth) => {
      track.scrollTo({ [vertical ? 'top' : 'left']: value, behavior: smooth && !reducedMotion() ? 'smooth' : 'instant' });
    };

    const controls = (name) => root.querySelectorAll(`[data-carousel="${name}"]`);
    const dots = root.querySelector('[data-carousel-dots]');
    const counter = root.querySelector('[data-carousel-counter]');
    let page = -1;

    const goTo = (n, smooth = true) => {
      const list = stops();
      const count = list.length;
      let i = n;
      if (i < 0) i = loop() ? count - 1 : 0;
      if (i >= count) i = loop() ? 0 : count - 1;
      scrollTo(list[i], smooth);
    };
    const goToSlide = (index, smooth = true) => {
      const s = slides()[index];
      if (s) goTo(nearest(stops(), Math.sign(offset(s)) * Math.min(Math.abs(offset(s)), maxScroll())), smooth);
    };

    const update = () => {
      const list = stops();
      const current = nearest(list, scrollPos());
      const all = slides();
      const slideIndex = Math.max(0, all.findIndex((s) => Math.abs(Math.sign(offset(s)) * Math.min(Math.abs(offset(s)), maxScroll()) - list[current]) <= 1));
      all.forEach((s, i) => s.toggleAttribute('data-active', i === slideIndex));
      controls('prev').forEach((b) => { b.disabled = !loop() && current === 0; });
      controls('next').forEach((b) => { b.disabled = !loop() && current === list.length - 1; });
      if (dots && dots.children.length !== list.length) {
        dots.replaceChildren(...list.map((_, i) => {
          const b = document.createElement('button');
          b.type = 'button';
          b.setAttribute('aria-label', `Go to slide ${i + 1}`);
          b.addEventListener('click', () => goTo(i));
          return b;
        }));
      }
      dots?.querySelectorAll('button').forEach((b, i) => {
        if (i === current) b.setAttribute('aria-current', 'true');
        else b.removeAttribute('aria-current');
      });
      if (counter) counter.textContent = `${current + 1} / ${list.length}`;
      if (current !== page) {
        page = current;
        root.dispatchEvent(new CustomEvent('carousel:change', { detail: { page: current, slide: slideIndex, pages: list.length } }));
      }
    };
    let frame = 0;
    const schedule = () => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(update);
    };

    // Autoplay: paused while hovered or focused, when the tab is hidden, and
    // by default when the user prefers reduced motion.
    let timer = 0;
    let playing = root.hasAttribute('data-autoplay') && !reducedMotion();
    const hold = new Set();
    const interval = () => Number(root.dataset.autoplay) || 5000;
    const tick = () => {
      clearTimeout(timer);
      if (playing && !hold.size && !document.hidden) timer = setTimeout(() => { goTo(page + 1); tick(); }, interval());
    };
    const setPlaying = (on) => {
      playing = on;
      controls('play').forEach((b) => {
        b.setAttribute('aria-pressed', String(on));
        b.setAttribute('aria-label', on ? 'Pause slideshow' : 'Play slideshow');
      });
      tick();
    };
    const holdOn = (why) => { hold.add(why); tick(); };
    const holdOff = (why) => { hold.delete(why); tick(); };

    // Mouse dragging. Touch and pens already scroll natively.
    let drag = null;
    let dragged = false;
    const onPointerDown = (e) => {
      if (e.pointerType !== 'mouse' || e.button !== 0 || root.hasAttribute('data-no-drag')) return;
      if (e.target.closest('button, input, select, textarea, [contenteditable]')) return;
      drag = { x: e.clientX, y: e.clientY, start: scrollPos(), from: page, moved: false };
      dragged = false;
    };
    const onPointerMove = (e) => {
      if (!drag) return;
      const delta = vertical ? e.clientY - drag.y : e.clientX - drag.x;
      if (!drag.moved && Math.abs(delta) < 5) return;
      if (!drag.moved) {
        drag.moved = true;
        track.setPointerCapture(e.pointerId);
        root.setAttribute('data-dragging', '');
        track.style.scrollSnapType = 'none';
        track.style.scrollBehavior = 'auto';
        holdOn('drag');
      }
      const value = drag.start - delta;
      if (vertical) track.scrollTop = value;
      else track.scrollLeft = value;
    };
    const onPointerUp = (e) => {
      if (!drag) return;
      const { moved, from, start } = drag;
      drag = null;
      if (!moved) return;
      dragged = true;
      root.removeAttribute('data-dragging');
      track.style.scrollSnapType = '';
      track.style.scrollBehavior = '';
      if (track.hasPointerCapture(e.pointerId)) track.releasePointerCapture(e.pointerId);
      // A short flick is enough to change page.
      const list = stops();
      const moveBy = scrollPos() - start;
      const size = vertical ? track.clientHeight : track.clientWidth;
      let target = nearest(list, scrollPos());
      if (target === from && Math.abs(moveBy) > size * 0.12) target = from + Math.sign(moveBy) * (rtl() && !vertical ? -1 : 1);
      goTo(Math.min(Math.max(target, 0), list.length - 1));
      holdOff('drag');
    };
    // A drag ends with a click on what was under the pointer: swallow it.
    const onClickCapture = (e) => {
      if (!dragged) return;
      dragged = false;
      e.preventDefault();
      e.stopPropagation();
    };

    const onKeydown = (e) => {
      if (e.target !== track) return;
      const back = vertical ? 'ArrowUp' : rtl() ? 'ArrowRight' : 'ArrowLeft';
      const forward = vertical ? 'ArrowDown' : rtl() ? 'ArrowLeft' : 'ArrowRight';
      if (e.key === back) goTo(page - 1);
      else if (e.key === forward) goTo(page + 1);
      else if (e.key === 'Home') goTo(0);
      else if (e.key === 'End') goTo(stops().length - 1);
      else return;
      e.preventDefault();
    };
    const onClick = (e) => {
      const b = e.target.closest('[data-carousel]');
      if (!b || !root.contains(b) || b.closest('.carousel') !== root) return;
      if (b.dataset.carousel === 'prev') goTo(page - 1);
      else if (b.dataset.carousel === 'next') goTo(page + 1);
      else if (b.dataset.carousel === 'play') setPlaying(!playing);
      else return;
      tick();
    };
    const onEnter = () => holdOn('hover');
    const onLeave = () => holdOff('hover');
    const onFocusIn = () => holdOn('focus');
    const onFocusOut = (e) => { if (!root.contains(e.relatedTarget)) holdOff('focus'); };
    const onVisibility = () => tick();
    const onDragStart = (e) => e.preventDefault();

    if (!track.hasAttribute('tabindex')) track.tabIndex = 0;
    track.addEventListener('scroll', schedule, { passive: true });
    track.addEventListener('keydown', onKeydown);
    track.addEventListener('pointerdown', onPointerDown);
    track.addEventListener('pointermove', onPointerMove);
    track.addEventListener('pointerup', onPointerUp);
    track.addEventListener('pointercancel', onPointerUp);
    track.addEventListener('click', onClickCapture, true);
    track.addEventListener('dragstart', onDragStart);
    root.addEventListener('click', onClick);
    root.addEventListener('pointerenter', onEnter);
    root.addEventListener('pointerleave', onLeave);
    root.addEventListener('focusin', onFocusIn);
    root.addEventListener('focusout', onFocusOut);
    document.addEventListener('visibilitychange', onVisibility);
    const resize = new ResizeObserver(schedule);
    resize.observe(track);

    // Thumbnail strip for another carousel.
    let main = null;
    const onMainChange = (e) => {
      const thumbs = slides();
      thumbs.forEach((t, i) => {
        const on = i === e.detail.slide;
        t.toggleAttribute('data-active', on);
        const b = t.querySelector('button, a');
        if (b) { if (on) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current'); }
      });
      const t = thumbs[e.detail.slide];
      if (!t) return;
      const size = vertical ? track.clientHeight : track.clientWidth;
      const own = vertical ? t.offsetHeight : t.offsetWidth;
      scrollTo(offset(t) - (size - own) / 2, true);
    };
    const onThumbClick = (e) => {
      const t = e.target.closest('li');
      if (!t || t.parentElement !== track || !main?.goToSlide) return;
      main.goToSlide(slides().indexOf(t));
    };
    if (root.dataset.carouselFor) {
      main = document.getElementById(root.dataset.carouselFor);
      if (main) {
        main.addEventListener('carousel:change', onMainChange);
        track.addEventListener('click', onThumbClick);
      }
    }

    Object.assign(root, {
      goTo,
      goToSlide,
      next: () => goTo(page + 1),
      prev: () => goTo(page - 1),
      play: () => setPlaying(true),
      pause: () => setPlaying(false),
    });
    root._destroy = () => {
      clearTimeout(timer);
      cancelAnimationFrame(frame);
      resize.disconnect();
      track.removeEventListener('scroll', schedule);
      track.removeEventListener('keydown', onKeydown);
      track.removeEventListener('pointerdown', onPointerDown);
      track.removeEventListener('pointermove', onPointerMove);
      track.removeEventListener('pointerup', onPointerUp);
      track.removeEventListener('pointercancel', onPointerUp);
      track.removeEventListener('click', onClickCapture, true);
      track.removeEventListener('dragstart', onDragStart);
      track.removeEventListener('click', onThumbClick);
      root.removeEventListener('click', onClick);
      root.removeEventListener('pointerenter', onEnter);
      root.removeEventListener('pointerleave', onLeave);
      root.removeEventListener('focusin', onFocusIn);
      root.removeEventListener('focusout', onFocusOut);
      document.removeEventListener('visibilitychange', onVisibility);
      main?.removeEventListener('carousel:change', onMainChange);
      for (const k of ['goTo', 'goToSlide', 'next', 'prev', 'play', 'pause']) delete root[k];
      delete root.dataset.carouselInitialized;
    };

    root.dataset.carouselInitialized = 'true';
    update();
    setPlaying(playing);
    // The main carousel may have initialized first: sync to its current slide.
    if (main?.dataset.carouselInitialized) {
      const active = Array.from(main.querySelectorAll(':scope > ol > li, :scope > ul > li')).findIndex((s) => s.hasAttribute('data-active'));
      onMainChange({ detail: { slide: Math.max(active, 0) } });
    }
    root.dispatchEvent(new CustomEvent('basecoat:initialized'));
  };

  // ---- Lightbox: links with [data-lightbox] open their href full screen.
  let viewer = null;
  const button = (name, label, paths) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.setAttribute('aria-label', label);
    if (name) b.dataset.carousel = name;
    b.innerHTML = svg(paths);
    return b;
  };
  const getViewer = () => {
    if (viewer) return viewer;
    const dialog = document.createElement('dialog');
    dialog.className = 'lightbox';
    dialog.setAttribute('aria-label', 'Image viewer');
    dialog.setAttribute('closedby', 'any');
    const root = document.createElement('section');
    root.className = 'carousel';
    root.setAttribute('aria-roledescription', 'carousel');
    root.setAttribute('aria-label', 'Images');
    root.setAttribute('data-loop', '');
    const list = document.createElement('ol');
    const counter = document.createElement('span');
    counter.setAttribute('data-carousel-counter', '');
    counter.setAttribute('aria-live', 'polite');
    root.append(list, button('prev', 'Previous image', ICONS.prev), button('next', 'Next image', ICONS.next), counter);
    const close = button('', 'Close', ICONS.close);
    close.setAttribute('data-lightbox-close', '');
    close.addEventListener('click', () => dialog.close());
    dialog.append(root, close);
    // Click an image to zoom; move the pointer to pan while zoomed.
    dialog.addEventListener('click', (e) => {
      const img = e.target.closest('img');
      if (!img) return;
      const fig = img.closest('figure');
      const on = !fig.hasAttribute('data-zoomed');
      fig.toggleAttribute('data-zoomed', on);
      root.toggleAttribute('data-no-drag', on);
      pan(img, e);
    });
    const pan = (img, e) => {
      const r = img.getBoundingClientRect();
      img.style.transformOrigin = `${((e.clientX - r.left) / r.width) * 100}% ${((e.clientY - r.top) / r.height) * 100}%`;
    };
    dialog.addEventListener('pointermove', (e) => {
      const img = e.target.closest('figure[data-zoomed] img');
      if (img) pan(img, e);
    });
    dialog.addEventListener('keydown', (e) => {
      if (e.target.closest('ol')) return;
      if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        const forward = (e.key === 'ArrowRight') !== (getComputedStyle(root).direction === 'rtl');
        if (forward) root.next?.(); else root.prev?.();
        e.preventDefault();
      }
    });
    root.addEventListener('carousel:change', () => {
      list.querySelectorAll('figure[data-zoomed]').forEach((f) => f.removeAttribute('data-zoomed'));
      root.removeAttribute('data-no-drag');
    });
    document.body.append(dialog);
    viewer = { dialog, root, list };
    return viewer;
  };
  const openLightbox = (link) => {
    const group = link.getAttribute('data-lightbox');
    const links = group ? Array.from(document.querySelectorAll('a[data-lightbox]')).filter((a) => a.getAttribute('data-lightbox') === group) : [link];
    const { dialog, root, list } = getViewer();
    list.replaceChildren(...links.map((a, i) => {
      const li = document.createElement('li');
      li.setAttribute('aria-roledescription', 'slide');
      li.setAttribute('aria-label', `${i + 1} of ${links.length}`);
      const fig = document.createElement('figure');
      const img = document.createElement('img');
      img.src = a.href;
      img.alt = a.querySelector('img')?.alt || a.getAttribute('aria-label') || '';
      img.draggable = false;
      fig.append(img);
      const text = a.dataset.caption || a.getAttribute('title');
      if (text) {
        const cap = document.createElement('figcaption');
        cap.textContent = text;
        fig.append(cap);
      }
      li.append(fig);
      return li;
    }));
    root.toggleAttribute('data-single', links.length < 2);
    dialog.showModal();
    initCarousel(root);
    requestAnimationFrame(() => root.goToSlide(links.indexOf(link), false));
  };
  const onDocumentClick = (e) => {
    const link = e.target.closest('a[data-lightbox][href]');
    if (!link || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    openLightbox(link);
  };
  if (!window.__auvyxLightbox) {
    window.__auvyxLightbox = true;
    document.addEventListener('click', onDocumentClick);
  }

  if (window.auvyx) {
    window.auvyx.register('carousel', {
      selector: '.carousel:not([data-carousel-initialized])',
      init: initCarousel,
    });
  }
})();

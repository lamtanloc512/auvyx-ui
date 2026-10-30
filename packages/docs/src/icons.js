// Swap inline Lucide icons for the Create preset's icon library.
// Loaded by the docs, the showcase and block pages; the library comes from the
// saved preset (localStorage "auvyx-preset".icons) or auvyxIcons.apply(lib).
(function () {
  var url = new URL('icons.json', document.currentScript.src).href;
  var ICON = /^(path|circle|rect|line|polyline|polygon|ellipse)$/;
  var ROOT_ATTRS = ['viewBox', 'fill', 'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin'];
  var original = new WeakMap();
  var data = null, loading = null, lib = 'lucide', queued = false;

  function signature(svg) {
    var out = [];
    for (var i = 0; i < svg.children.length; i++) {
      var el = svg.children[i];
      if (!ICON.test(el.localName)) return '';
      var attrs = [];
      for (var j = 0; j < el.attributes.length; j++) attrs.push(el.attributes[j].name + '=' + el.attributes[j].value);
      out.push(el.localName + '(' + attrs.sort().join(',') + ')');
    }
    return out.sort().join('');
  }

  function swap(svg) {
    var saved = original.get(svg);
    if (!saved) {
      var name = data.signatures[signature(svg)];
      if (!name) return;
      saved = { name: name, html: svg.innerHTML, attrs: {} };
      ROOT_ATTRS.forEach(function (a) { saved.attrs[a] = svg.getAttribute(a); });
      original.set(svg, saved);
    }
    if (svg.getAttribute('data-icon-lib') === lib) return;
    if (lib === 'lucide') {
      svg.innerHTML = saved.html;
      ROOT_ATTRS.forEach(function (a) { if (saved.attrs[a] == null) svg.removeAttribute(a); else svg.setAttribute(a, saved.attrs[a]); });
    } else {
      var icon = data.sets[lib] && data.sets[lib].icons[saved.name];
      if (!icon) return;
      // Iconify bodies carry their own fill/stroke, so drop Lucide's root defaults.
      ROOT_ATTRS.forEach(function (a) { svg.removeAttribute(a); });
      svg.setAttribute('viewBox', '0 0 ' + icon[1] + ' ' + icon[2]);
      svg.innerHTML = icon[0];
    }
    svg.setAttribute('data-icon-lib', lib);
  }

  function run() {
    queued = false;
    if (lib !== 'lucide' && !data) return load().then(run);
    if (!data) return; // still Lucide and nothing swapped yet
    document.querySelectorAll('svg').forEach(swap);
  }
  function schedule() { if (!queued) { queued = true; requestAnimationFrame(run); } }
  function load() {
    return loading || (loading = fetch(url).then(function (r) { return r.json(); }).then(function (j) { data = j; }));
  }
  function apply(next) {
    next = next || 'lucide';
    if (next === lib && (next === 'lucide' ? !data : data)) return;
    lib = next;
    schedule();
  }
  function fromStorage() {
    try { return (JSON.parse(localStorage.getItem('auvyx-preset') || 'null') || {}).icons; } catch (e) { return null; }
  }

  new MutationObserver(function (records) {
    if (lib === 'lucide' && !data) return;
    for (var i = 0; i < records.length; i++) if (records[i].addedNodes.length) return schedule();
  }).observe(document.documentElement, { childList: true, subtree: true });
  window.addEventListener('storage', function (e) { if (e.key === 'auvyx-preset') apply(fromStorage()); });
  window.auvyxIcons = { apply: apply };
  apply(fromStorage());
})();

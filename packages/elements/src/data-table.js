// <auvyx-data-table>: sorting, filtering, facets, selection, column visibility,
// pagination, expandable rows, inline editing and grid keyboard navigation over
// a server-rendered table (fork addition). Rows stay real DOM rows; this only
// reorders and hides them. data-mode="server" leaves rows alone and emits
// statechange instead. See data-table.css for markup.
const FOCUSABLE = 'a[href], button, input, select, textarea, [tabindex]';

class AuvyxDataTable extends HTMLElement {
  connectedCallback() {
    if (this._init) return;
    this._init = true;
    this.table = this.querySelector('table');
    this.tbody = this.table?.tBodies[0];
    if (!this.tbody || !this.table.tHead) return;
    this.server = this.dataset.mode === 'server';
    this.pageSize = parseInt(this.dataset.pageSize, 10) || 0;
    this.page = 0;
    this.query = '';
    this.facets = new Map();
    this.hiddenCols = new Set();
    this.collator = new Intl.Collator(this.closest('[lang]')?.lang || undefined, { numeric: true, sensitivity: 'base' });
    this.headers = [...this.table.tHead.rows[0].cells];
    const sorted = this.headers.findIndex((th) => /^(a|de)scending$/.test(th.getAttribute('aria-sort')));
    this.sort = { col: sorted, dir: sorted < 0 ? 'ascending' : this.headers[sorted].getAttribute('aria-sort') };
    this.filterInput = this.querySelector('input[data-filter]');
    this.selectAll = this.querySelector('input[data-select-all]');
    this.scan();

    this.addEventListener('click', (e) => this.onClick(e));
    this.addEventListener('change', (e) => this.onChange(e));
    this.addEventListener('input', (e) => {
      if (e.target !== this.filterInput) return;
      this.query = this.filterInput.value.trim().toLocaleLowerCase();
      this.page = 0;
      this.commit();
    });
    this.tbody.addEventListener('dblclick', (e) => {
      const cell = e.target.closest('td[data-editable]');
      if (cell) this.edit(cell);
    });

    this.querySelectorAll('input[data-column]').forEach((t) => { if (!t.checked) this.hiddenCols.add(this.colIndex(t.dataset.column)); });
    this.querySelectorAll('input[data-facet]:checked').forEach((t) => this.facetSet(this.colIndex(t.dataset.facet)).add(t.value));
    if (this.pageSize) this.syncControls(); // the page size select follows data-page-size
    this.grid = this.hasAttribute('data-grid');
    if (this.grid) this.setupGrid();
    else this.tbody.querySelectorAll('td[data-editable]').forEach((c) => { c.tabIndex = 0; });
    this.addEventListener('keydown', (e) => this.onKeydown(e));
    this.render();
  }

  // Re-read rows after the host replaced <tbody> content (server mode).
  refresh() {
    this.scan();
    if (this.grid) this.setupGrid();
    this.render();
  }

  scan() {
    const all = [...this.tbody.rows];
    this.empty = all.find((r) => r.hasAttribute('data-empty')) || null;
    this.rows = all.filter((r) => !r.hasAttribute('data-empty') && !r.hasAttribute('data-detail'));
    this.details = new Map();
    this.rows.forEach((row) => {
      const next = row.nextElementSibling;
      if (next?.hasAttribute('data-detail')) this.details.set(row, next);
      const box = row.querySelector('input[data-select]');
      if (box?.checked) row.setAttribute('aria-selected', 'true');
    });
  }

  // Columns are addressed by index or by <th data-key>.
  colIndex(ref) {
    if (typeof ref === 'number') return ref;
    if (/^\d+$/.test(ref)) return Number(ref);
    return this.headers.findIndex((th) => th.dataset.key === ref);
  }

  colKey(i) {
    return this.headers[i]?.dataset.key ?? String(i);
  }

  rowKey(row) {
    return row.dataset.key || row.id || String(this.rows.indexOf(row));
  }

  facetSet(col) {
    if (!this.facets.has(col)) this.facets.set(col, new Set());
    return this.facets.get(col);
  }

  cellValue(row, col) {
    const cell = row.cells[col];
    return cell ? (cell.dataset.value ?? cell.textContent.trim()) : '';
  }

  matches(row) {
    for (const [col, values] of this.facets) {
      if (values.size && !values.has(this.cellValue(row, col))) return false;
    }
    if (!this.query) return true;
    const only = this.filterInput?.dataset.filter;
    const cols = only ? only.split(',').map((c) => this.colIndex(c.trim())) : null;
    return [...row.cells].some((cell, i) => (!cols || cols.includes(i)) && cell.textContent.toLocaleLowerCase().includes(this.query));
  }

  onClick(e) {
    const sortButton = e.target.closest('th[aria-sort] > button');
    if (sortButton && this.contains(sortButton)) return this.toggleSort(sortButton.parentElement.cellIndex);
    const pager = e.target.closest('[data-page]');
    if (pager) {
      const last = this.pageCount() - 1;
      const to = { prev: this.page - 1, next: this.page + 1, first: 0, last }[pager.dataset.page];
      if (to === undefined) return;
      this.page = to;
      return this.commit();
    }
    const expander = e.target.closest('[data-expand]');
    if (expander) return this.toggleExpand(expander.closest('tr'));
    if (e.target.closest('[data-reset]')) return this.reset();
    const box = e.target.closest('input[data-select]');
    if (box) {
      const row = box.closest('tr');
      // Shift-click selects the range from the last clicked row.
      if (e.shiftKey && this.anchor && this.anchor !== row) {
        const shown = this.visible();
        const [a, b] = [shown.indexOf(this.anchor), shown.indexOf(row)].sort((x, y) => x - y);
        if (a >= 0) shown.slice(a, b + 1).forEach((r) => this.setSelected(r, box.checked));
      }
      this.anchor = row;
    }
  }

  onChange(e) {
    const t = e.target;
    if (t === this.selectAll) {
      this.visible().forEach((row) => this.setSelected(row, t.checked));
      this.updateSelection();
    } else if (t.matches('input[data-select]')) {
      this.setSelected(t.closest('tr'), t.checked);
      this.updateSelection();
    } else if (t.matches('input[data-column]')) {
      this.setColumn(this.colIndex(t.dataset.column), t.checked);
      this.emit();
    } else if (t.matches('input[data-facet]')) {
      const set = this.facetSet(this.colIndex(t.dataset.facet));
      if (t.checked) set.add(t.value); else set.delete(t.value);
      this.page = 0;
      this.commit();
    } else if (t.matches('select[data-page-size]')) {
      this.pageSize = parseInt(t.value, 10) || 0;
      this.page = 0;
      this.commit();
    }
  }

  toggleSort(col) {
    this.sort = this.sort.col === col
      ? { col, dir: this.sort.dir === 'ascending' ? 'descending' : 'ascending' }
      : { col, dir: 'ascending' };
    this.commit();
  }

  toggleExpand(row) {
    const button = row?.querySelector('[data-expand]');
    const detail = this.details.get(row);
    if (!button || !detail) return;
    const open = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(open));
    detail.hidden = !open || row.hidden;
  }

  reset() {
    this.query = '';
    this.facets.clear();
    this.sort = { col: -1, dir: 'ascending' };
    this.page = 0;
    this.syncControls();
    this.commit();
  }

  ordered() {
    const list = this.rows.filter((r) => this.matches(r));
    const { col, dir } = this.sort;
    if (col < 0) return list;
    const numeric = this.headers[col]?.dataset.type === 'number';
    const sign = dir === 'descending' ? -1 : 1;
    return list.sort((a, b) => {
      const x = this.cellValue(a, col);
      const y = this.cellValue(b, col);
      return sign * (numeric ? (parseFloat(x) || 0) - (parseFloat(y) || 0) : this.collator.compare(x, y));
    });
  }

  visible() {
    return this.rows.filter((r) => !r.hidden);
  }

  setSelected(row, on) {
    const box = row.querySelector('input[data-select]');
    if (box) box.checked = on;
    if (on) row.setAttribute('aria-selected', 'true');
    else row.removeAttribute('aria-selected');
  }

  setColumn(col, show) {
    if (col < 0) return;
    if (show) this.hiddenCols.delete(col); else this.hiddenCols.add(col);
    [this.table.tHead, ...this.table.tBodies, this.table.tFoot].filter(Boolean).forEach((section) => {
      [...section.rows].forEach((row) => {
        if (row.cells[col] && !row.hasAttribute('data-empty') && !row.hasAttribute('data-detail')) row.cells[col].hidden = !show;
      });
    });
  }

  updateSelection() {
    const shown = this.visible();
    const selected = this.rows.filter((r) => r.getAttribute('aria-selected') === 'true');
    const shownSelected = shown.filter((r) => r.getAttribute('aria-selected') === 'true').length;
    if (this.selectAll) {
      this.selectAll.checked = shown.length > 0 && shownSelected === shown.length;
      this.selectAll.indeterminate = shownSelected > 0 && shownSelected < shown.length;
    }
    const count = this.querySelector('[data-selected-count]');
    if (count) {
      const tpl = count.dataset.template || '{selected} of {total} row(s) selected.';
      count.textContent = tpl.replace('{selected}', selected.length).replace('{total}', this.total());
    }
    this.dispatchEvent(new CustomEvent('selectionchange', { detail: { rows: selected } }));
  }

  total() {
    return this.server ? parseInt(this.dataset.total, 10) || this.rows.length : this.rows.length;
  }

  pageCount(count = this.server ? this.total() : this.ordered().length) {
    return this.pageSize ? Math.max(1, Math.ceil(count / this.pageSize)) : 1;
  }

  // Serializable view state: what an app (or an agent) reads and writes.
  get state() {
    const filters = {};
    this.facets.forEach((values, col) => { if (values.size) filters[this.colKey(col)] = [...values]; });
    return {
      query: this.query,
      sort: this.sort.col < 0 ? null : { column: this.colKey(this.sort.col), direction: this.sort.dir },
      filters,
      page: this.page,
      pageSize: this.pageSize,
      hiddenColumns: [...this.hiddenCols].map((c) => this.colKey(c)),
      selected: this.rows.filter((r) => r.getAttribute('aria-selected') === 'true').map((r) => this.rowKey(r)),
    };
  }

  set state(next) {
    if (!this._init || !next) return;
    if ('query' in next) this.query = String(next.query || '').toLocaleLowerCase();
    if ('sort' in next) {
      const col = next.sort ? this.colIndex(next.sort.column) : -1;
      this.sort = { col, dir: next.sort?.direction === 'descending' ? 'descending' : 'ascending' };
    }
    if ('filters' in next) {
      this.facets.clear();
      Object.entries(next.filters || {}).forEach(([key, values]) => {
        const col = this.colIndex(key);
        if (col >= 0) this.facets.set(col, new Set([].concat(values).map(String)));
      });
    }
    if ('pageSize' in next) this.pageSize = parseInt(next.pageSize, 10) || 0;
    if ('page' in next) this.page = parseInt(next.page, 10) || 0;
    if ('hiddenColumns' in next) {
      const hide = new Set((next.hiddenColumns || []).map((k) => this.colIndex(k)));
      this.headers.forEach((_, i) => this.setColumn(i, !hide.has(i)));
    }
    if ('selected' in next) {
      const keys = new Set((next.selected || []).map(String));
      this.rows.forEach((r) => this.setSelected(r, keys.has(this.rowKey(r))));
    }
    this.syncControls();
    this.commit();
  }

  syncControls() {
    if (this.filterInput && this.filterInput.value.trim().toLocaleLowerCase() !== this.query) this.filterInput.value = this.query;
    this.querySelectorAll('input[data-facet]').forEach((t) => { t.checked = !!this.facets.get(this.colIndex(t.dataset.facet))?.has(t.value); });
    this.querySelectorAll('input[data-column]').forEach((t) => { t.checked = !this.hiddenCols.has(this.colIndex(t.dataset.column)); });
    this.querySelectorAll('select[data-page-size]').forEach((s) => { s.value = String(this.pageSize); });
  }

  emit() {
    this.dispatchEvent(new CustomEvent('statechange', { detail: this.state }));
  }

  commit() {
    this.render();
    this.emit();
  }

  render() {
    this.headers.forEach((th, i) => th.hasAttribute('aria-sort') && th.setAttribute('aria-sort', i === this.sort.col ? this.sort.dir : 'none'));
    let count = this.total();
    if (!this.server) {
      const list = this.ordered();
      count = list.length;
      const pages = this.pageCount(count);
      this.page = Math.min(Math.max(0, this.page), pages - 1);
      const from = this.pageSize ? this.page * this.pageSize : 0;
      const shown = new Set(this.pageSize ? list.slice(from, from + this.pageSize) : list);
      // Reorder in place so the DOM order matches the sort (screen readers read it).
      list.forEach((row) => {
        this.tbody.insertBefore(row, this.empty);
        const detail = this.details.get(row);
        if (detail) this.tbody.insertBefore(detail, this.empty);
      });
      this.rows.forEach((row) => { row.hidden = !shown.has(row); });
    } else {
      this.page = Math.min(Math.max(0, this.page), this.pageCount(count) - 1);
    }
    this.details.forEach((detail, row) => {
      detail.hidden = row.hidden || row.querySelector('[data-expand]')?.getAttribute('aria-expanded') !== 'true';
    });
    if (this.empty) this.empty.hidden = (this.server ? this.rows.length : count) > 0;

    const pages = this.pageCount(count);
    const status = this.querySelector('[data-page-status]');
    if (status) {
      const tpl = status.dataset.template || 'Page {page} of {pages}';
      status.textContent = tpl.replace('{page}', this.page + 1).replace('{pages}', pages);
    }
    this.querySelectorAll('[data-page="prev"], [data-page="first"]').forEach((b) => { b.disabled = this.page <= 0; });
    this.querySelectorAll('[data-page="next"], [data-page="last"]').forEach((b) => { b.disabled = this.page >= pages - 1; });
    this.querySelectorAll('[data-facet-count]').forEach((el) => {
      const n = this.facets.get(this.colIndex(el.dataset.facetCount))?.size || 0;
      el.textContent = n ? String(n) : '';
      el.hidden = !n;
    });
    const reset = this.querySelector('[data-reset]');
    if (reset) reset.hidden = !this.query && this.sort.col < 0 && ![...this.facets.values()].some((s) => s.size);
    if (this.grid && this.active && !this.isNavigable(this.active)) this.setActive(this.gridRows()[0]?.[0]);
    this.updateSelection();
  }

  // Inline editing: double-click, Enter or F2 on <td data-editable>.
  edit(cell) {
    if (this.editing || !cell) return;
    const th = this.headers[cell.cellIndex];
    const previous = cell.dataset.value ?? cell.textContent.trim();
    const input = document.createElement('input');
    input.className = 'input';
    input.type = th?.dataset.type === 'number' ? 'number' : 'text';
    input.value = previous;
    input.setAttribute('aria-label', th?.textContent.trim() || 'Edit cell');
    const html = cell.innerHTML;
    this.editing = { cell };
    cell.setAttribute('data-editing', '');
    cell.replaceChildren(input);
    input.focus();
    input.select();

    const finish = (save) => {
      if (this.editing?.cell !== cell) return;
      this.editing = null;
      const value = input.value;
      cell.removeAttribute('data-editing');
      cell.innerHTML = html;
      if (save && value !== previous) {
        const ev = new CustomEvent('cellchange', {
          cancelable: true,
          detail: { row: cell.parentElement, rowKey: this.rowKey(cell.parentElement), column: this.colKey(cell.cellIndex), value, previous },
        });
        if (this.dispatchEvent(ev)) {
          if ('value' in cell.dataset) cell.dataset.value = value;
          cell.textContent = value;
        }
      }
      if (!this.server) this.render();
      if (this.grid) this.setActive(cell, true);
      else cell.focus();
    };
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === 'Escape' || e.key === 'Tab') {
        e.stopPropagation();
        if (e.key !== 'Tab') e.preventDefault();
        finish(e.key !== 'Escape');
      }
    });
    input.addEventListener('blur', () => finish(true));
  }

  // Grid keyboard model (data-grid): one tab stop, arrows move between cells.
  setupGrid() {
    this.table.setAttribute('role', 'grid');
    this.table.querySelectorAll('th, td').forEach((cell) => { cell.tabIndex = -1; });
    this.table.querySelectorAll(FOCUSABLE).forEach((el) => { if (!el.matches('th, td')) el.tabIndex = -1; });
    this.table.addEventListener('focusin', (e) => {
      const cell = e.target.closest('th, td');
      if (cell && !this.editing && this.isNavigable(cell)) this.setActive(cell);
    });
    this.setActive(this.gridRows()[0]?.[0]);
  }

  gridRows() {
    const rows = [...this.table.tHead.rows, ...this.rows.filter((r) => !r.hidden)];
    return rows.map((r) => [...r.cells].filter((c) => !c.hidden)).filter((cells) => cells.length);
  }

  isNavigable(cell) {
    return cell.isConnected && !cell.hidden && !cell.closest('tr').hidden && !cell.closest('tr').hasAttribute('data-detail');
  }

  // A cell holding exactly one control focuses the control, like the APG grid.
  target(cell) {
    const controls = [...cell.querySelectorAll(FOCUSABLE)];
    return controls.length === 1 ? controls[0] : cell;
  }

  setActive(cell, focus = false) {
    if (!cell) return;
    if (this.active && this.active !== cell) this.target(this.active).tabIndex = -1;
    this.active = cell;
    const el = this.target(cell);
    el.tabIndex = 0;
    if (focus) el.focus({ preventScroll: true });
  }

  onKeydown(e) {
    if (this.editing) return;
    const cell = e.target.closest?.('th, td');
    if (!cell || !this.table.contains(cell)) return;
    const textField = e.target.matches('input:not([type=checkbox], [type=radio]), select, textarea');
    if ((e.key === 'Enter' || e.key === 'F2') && cell.hasAttribute('data-editable') && !textField) {
      e.preventDefault();
      return this.edit(cell);
    }
    if (!this.grid || textField) return;
    if (e.key === ' ' && e.target === cell) {
      const box = cell.closest('tr').querySelector('input[data-select]');
      if (box) { e.preventDefault(); box.click(); }
      return;
    }
    const rows = this.gridRows();
    let r = rows.findIndex((cells) => cells.includes(cell));
    if (r < 0) return;
    let c = rows[r].indexOf(cell);
    const rtl = getComputedStyle(this).direction === 'rtl';
    const step = 5;
    switch (e.key) {
      case 'ArrowRight': c += rtl ? -1 : 1; break;
      case 'ArrowLeft': c += rtl ? 1 : -1; break;
      case 'ArrowDown': r += 1; break;
      case 'ArrowUp': r -= 1; break;
      case 'PageDown': r += step; break;
      case 'PageUp': r -= step; break;
      case 'Home': if (e.ctrlKey || e.metaKey) r = 0; c = 0; break;
      case 'End': if (e.ctrlKey || e.metaKey) r = rows.length - 1; c = Infinity; break;
      default: return;
    }
    e.preventDefault();
    r = Math.min(Math.max(0, r), rows.length - 1);
    c = Math.min(Math.max(0, c), rows[r].length - 1);
    this.setActive(rows[r][c], true);
  }
}

if (!customElements.get('auvyx-data-table')) customElements.define('auvyx-data-table', AuvyxDataTable);

// <auvyx-data-table>: sorting, filtering, selection, column visibility and
// pagination over a server-rendered table (fork addition). Rows stay real
// DOM rows; this only reorders and hides them. See data-table.css for markup.
class AuvyxDataTable extends HTMLElement {
  connectedCallback() {
    if (this._init) return;
    this._init = true;
    this.table = this.querySelector('table');
    this.tbody = this.table?.tBodies[0];
    if (!this.tbody) return;
    this.rows = [...this.tbody.rows].filter((r) => !r.hasAttribute('data-empty'));
    this.empty = this.tbody.querySelector('tr[data-empty]');
    this.pageSize = parseInt(this.dataset.pageSize, 10) || 0;
    this.page = 0;
    this.query = '';
    this.sort = { col: -1, dir: 'ascending' };
    this.collator = new Intl.Collator(this.closest('[lang]')?.lang || undefined, { numeric: true, sensitivity: 'base' });

    this.headers = [...this.table.tHead.rows[0].cells];
    this.headers.forEach((th, col) => {
      const button = th.hasAttribute('aria-sort') ? th.querySelector(':scope > button') : null;
      button?.addEventListener('click', () => this.toggleSort(col));
    });

    this.filterInput = this.querySelector('input[data-filter]');
    this.filterInput?.addEventListener('input', () => {
      this.query = this.filterInput.value.trim().toLocaleLowerCase();
      this.page = 0;
      this.render();
    });

    this.selectAll = this.querySelector('input[data-select-all]');
    this.selectAll?.addEventListener('change', () => {
      this.visible().forEach((row) => this.setSelected(row, this.selectAll.checked));
      this.updateSelection();
    });
    this.tbody.addEventListener('change', (e) => {
      if (!e.target.matches('input[data-select]')) return;
      this.setSelected(e.target.closest('tr'), e.target.checked);
      this.updateSelection();
    });

    this.querySelectorAll('input[data-column]').forEach((toggle) => {
      toggle.addEventListener('change', () => this.setColumn(parseInt(toggle.dataset.column, 10), toggle.checked));
      if (!toggle.checked) this.setColumn(parseInt(toggle.dataset.column, 10), false);
    });

    this.querySelector('[data-page="prev"]')?.addEventListener('click', () => { this.page--; this.render(); });
    this.querySelector('[data-page="next"]')?.addEventListener('click', () => { this.page++; this.render(); });

    this.rows.forEach((row) => {
      const box = row.querySelector('input[data-select]');
      if (box?.checked) row.setAttribute('aria-selected', 'true');
    });
    this.render();
  }

  cellValue(row, col) {
    const cell = row.cells[col];
    return cell ? (cell.dataset.value ?? cell.textContent.trim()) : '';
  }

  matches(row) {
    if (!this.query) return true;
    const only = this.filterInput?.dataset.filter;
    const cols = only ? only.split(',').map(Number) : null;
    return [...row.cells].some((cell, i) => (!cols || cols.includes(i)) && cell.textContent.toLocaleLowerCase().includes(this.query));
  }

  toggleSort(col) {
    this.sort = this.sort.col === col
      ? { col, dir: this.sort.dir === 'ascending' ? 'descending' : 'ascending' }
      : { col, dir: 'ascending' };
    this.headers.forEach((th, i) => th.hasAttribute('aria-sort') && th.setAttribute('aria-sort', i === col ? this.sort.dir : 'none'));
    this.render();
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
    [this.table.tHead, ...this.table.tBodies, this.table.tFoot].filter(Boolean).forEach((section) => {
      [...section.rows].forEach((row) => { if (row.cells[col] && !row.hasAttribute('data-empty')) row.cells[col].hidden = !show; });
    });
  }

  updateSelection() {
    const shown = this.visible();
    const selected = this.rows.filter((r) => r.getAttribute('aria-selected') === 'true').length;
    const shownSelected = shown.filter((r) => r.getAttribute('aria-selected') === 'true').length;
    if (this.selectAll) {
      this.selectAll.checked = shown.length > 0 && shownSelected === shown.length;
      this.selectAll.indeterminate = shownSelected > 0 && shownSelected < shown.length;
    }
    const count = this.querySelector('[data-selected-count]');
    if (count) {
      const tpl = count.dataset.template || '{selected} of {total} row(s) selected.';
      count.textContent = tpl.replace('{selected}', selected).replace('{total}', this.rows.length);
    }
    this.dispatchEvent(new CustomEvent('selectionchange', { detail: { rows: this.rows.filter((r) => r.getAttribute('aria-selected') === 'true') } }));
  }

  render() {
    const list = this.ordered();
    const pages = this.pageSize ? Math.max(1, Math.ceil(list.length / this.pageSize)) : 1;
    this.page = Math.min(Math.max(0, this.page), pages - 1);
    const from = this.pageSize ? this.page * this.pageSize : 0;
    const to = this.pageSize ? from + this.pageSize : list.length;
    const shown = new Set(list.slice(from, to));
    // Reorder in place so the DOM order matches the sort (screen readers read it).
    list.forEach((row) => this.tbody.insertBefore(row, this.empty));
    this.rows.forEach((row) => { row.hidden = !shown.has(row); });
    if (this.empty) this.empty.hidden = list.length > 0;

    const status = this.querySelector('[data-page-status]');
    if (status) {
      const tpl = status.dataset.template || 'Page {page} of {pages}';
      status.textContent = tpl.replace('{page}', this.page + 1).replace('{pages}', pages);
    }
    const prev = this.querySelector('[data-page="prev"]');
    const next = this.querySelector('[data-page="next"]');
    if (prev) prev.disabled = this.page <= 0;
    if (next) next.disabled = this.page >= pages - 1;
    this.updateSelection();
  }
}

if (!customElements.get('auvyx-data-table')) customElements.define('auvyx-data-table', AuvyxDataTable);

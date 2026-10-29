// <auvyx-calendar>: month grid with keyboard navigation (fork addition).
// Attributes: value ("YYYY-MM-DD", or "start/end" in range mode), min, max,
// mode ("single" | "range"), name (keeps a hidden input in sync for forms),
// data-week-start (0 = Sunday … 6; default 1 = Monday).
// Emits `change` (bubbles) with detail.value. Locale comes from the nearest [lang].
const pad = (n) => String(n).padStart(2, '0');
const toISO = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
const fromISO = (s) => {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s || '');
  return m ? new Date(+m[1], +m[2] - 1, +m[3]) : null;
};
const sameDay = (a, b) => a && b && a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
const addDays = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
const addMonths = (d, n) => {
  const last = new Date(d.getFullYear(), d.getMonth() + n + 1, 0).getDate();
  return new Date(d.getFullYear(), d.getMonth() + n, Math.min(d.getDate(), last));
};
const chevron = (d) => `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${d}"/></svg>`;

class AuvyxCalendar extends HTMLElement {
  static observedAttributes = ['value', 'min', 'max', 'mode'];

  connectedCallback() {
    this.mode = this.getAttribute('mode') === 'range' ? 'range' : 'single';
    this.readValue();
    this.focused = this.focused || this.start || new Date();
    this.view = new Date(this.focused.getFullYear(), this.focused.getMonth(), 1);
    if (!this._init) {
      this._init = true;
      this.addEventListener('click', (e) => this.onClick(e));
      this.addEventListener('keydown', (e) => this.onKey(e));
    }
    this.render();
  }

  attributeChangedCallback(name, oldValue, value) {
    if (!this._init || oldValue === value || this._writing) return;
    if (name === 'mode') this.mode = value === 'range' ? 'range' : 'single';
    this.readValue();
    if (name === 'value' && this.start) {
      this.focused = this.start;
      this.view = new Date(this.start.getFullYear(), this.start.getMonth(), 1);
    }
    this.render();
  }

  get value() {
    if (this.mode === 'range') return this.start ? `${toISO(this.start)}/${this.end ? toISO(this.end) : ''}` : '';
    return this.start ? toISO(this.start) : '';
  }

  set value(v) {
    this.setAttribute('value', v ?? '');
  }

  readValue() {
    const [a, b] = (this.getAttribute('value') || '').split('/');
    this.start = fromISO(a);
    this.end = this.mode === 'range' ? fromISO(b) : null;
    this.min = fromISO(this.getAttribute('min'));
    this.max = fromISO(this.getAttribute('max'));
  }

  locale() {
    return this.closest('[lang]')?.getAttribute('lang') || navigator.language;
  }

  disabled(d) {
    return (this.min && d < this.min) || (this.max && d > this.max);
  }

  render() {
    const locale = this.locale();
    const weekStart = Number.isFinite(parseInt(this.dataset.weekStart, 10)) ? parseInt(this.dataset.weekStart, 10) : 1;
    const today = new Date();
    const first = this.view;
    const lead = (first.getDay() - weekStart + 7) % 7;
    const gridStart = addDays(first, -lead);
    const daysInMonth = new Date(first.getFullYear(), first.getMonth() + 1, 0).getDate();
    const weeks = Math.ceil((lead + daysInMonth) / 7);
    const title = new Intl.DateTimeFormat(locale, { month: 'long', year: 'numeric' }).format(first);
    const weekday = new Intl.DateTimeFormat(locale, { weekday: 'short' });
    const weekdayLong = new Intl.DateTimeFormat(locale, { weekday: 'long' });
    const dayLabel = new Intl.DateTimeFormat(locale, { dateStyle: 'full' });
    const id = this.id || (this._uid ||= `cal-${Math.random().toString(36).slice(2, 8)}`);

    let head = '';
    for (let i = 0; i < 7; i++) {
      const d = addDays(gridStart, i);
      head += `<th scope="col" abbr="${weekdayLong.format(d)}">${weekday.format(d)}</th>`;
    }

    let body = '';
    for (let w = 0; w < weeks; w++) {
      body += '<tr>';
      for (let i = 0; i < 7; i++) {
        const d = addDays(gridStart, w * 7 + i);
        const outside = d.getMonth() !== first.getMonth();
        const attrs = [];
        if (outside) attrs.push('data-outside');
        if (this.mode === 'single' && sameDay(d, this.start)) attrs.push('aria-selected="true"');
        if (this.mode === 'range' && this.start) {
          const end = this.end || this.start;
          if (sameDay(d, this.start)) attrs.push('data-range-start');
          if (sameDay(d, end)) attrs.push('data-range-end');
          if (d > this.start && d < end) attrs.push('data-range-middle');
          if (d >= this.start && d <= end) attrs.push('aria-selected="true"');
        }
        const tab = sameDay(d, this.focused) ? '0' : '-1';
        body += `<td ${attrs.join(' ')}><button type="button" data-date="${toISO(d)}" tabindex="${tab}" aria-label="${dayLabel.format(d)}"${sameDay(d, today) ? ' aria-current="date"' : ''}${this.disabled(d) ? ' disabled' : ''}>${d.getDate()}</button></td>`;
      }
      body += '</tr>';
    }

    const hadFocus = this.contains(document.activeElement) && document.activeElement.matches('td > button');
    const prevLabel = this.dataset.labelPrev || 'Previous month';
    const nextLabel = this.dataset.labelNext || 'Next month';
    const hidden = this.getAttribute('name') ? `<input type="hidden" name="${this.getAttribute('name')}" value="${this.value}">` : '';
    this.innerHTML = `<header>
      <button type="button" data-nav="-1" aria-label="${prevLabel}">${chevron('m15 18-6-6 6-6')}</button>
      <h2 id="${id}-title" aria-live="polite">${title}</h2>
      <button type="button" data-nav="1" aria-label="${nextLabel}">${chevron('m9 18 6-6-6-6')}</button>
    </header>
    <table role="grid" aria-labelledby="${id}-title"><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>${hidden}`;
    if (hadFocus) this.focusDate();
  }

  focusDate() {
    this.querySelector(`button[data-date="${toISO(this.focused)}"]`)?.focus({ preventScroll: true });
  }

  moveFocus(d) {
    if (this.disabled(d)) return;
    this.focused = d;
    if (d.getMonth() !== this.view.getMonth() || d.getFullYear() !== this.view.getFullYear()) {
      this.view = new Date(d.getFullYear(), d.getMonth(), 1);
      this.render();
    } else {
      this.querySelectorAll('td > button').forEach((b) => { b.tabIndex = b.dataset.date === toISO(d) ? 0 : -1; });
    }
    this.focusDate();
  }

  select(d) {
    if (this.mode === 'range') {
      if (!this.start || this.end || d < this.start) { this.start = d; this.end = null; }
      else this.end = d;
    } else {
      this.start = d;
    }
    this.focused = d;
    this._writing = true;
    this.setAttribute('value', this.value);
    this._writing = false;
    this.render();
    this.focusDate();
    this.dispatchEvent(new CustomEvent('change', { bubbles: true, detail: { value: this.value, complete: this.mode !== 'range' || !!this.end } }));
  }

  onClick(event) {
    const nav = event.target.closest('button[data-nav]');
    if (nav) {
      this.view = addMonths(this.view, +nav.dataset.nav);
      this.focused = new Date(this.view.getFullYear(), this.view.getMonth(), Math.min(this.focused.getDate(), new Date(this.view.getFullYear(), this.view.getMonth() + 1, 0).getDate()));
      this.render();
      return;
    }
    const day = event.target.closest('button[data-date]');
    if (day && !day.disabled) this.select(fromISO(day.dataset.date));
  }

  onKey(event) {
    if (!event.target.matches('td > button')) return;
    const rtl = getComputedStyle(this).direction === 'rtl';
    const d = this.focused;
    const weekStart = Number.isFinite(parseInt(this.dataset.weekStart, 10)) ? parseInt(this.dataset.weekStart, 10) : 1;
    const offset = (d.getDay() - weekStart + 7) % 7;
    const moves = {
      ArrowLeft: addDays(d, rtl ? 1 : -1),
      ArrowRight: addDays(d, rtl ? -1 : 1),
      ArrowUp: addDays(d, -7),
      ArrowDown: addDays(d, 7),
      Home: addDays(d, -offset),
      End: addDays(d, 6 - offset),
      PageUp: addMonths(d, event.shiftKey ? -12 : -1),
      PageDown: addMonths(d, event.shiftKey ? 12 : 1),
    };
    if (!(event.key in moves)) return;
    event.preventDefault();
    this.moveFocus(moves[event.key]);
  }
}

if (!customElements.get('auvyx-calendar')) customElements.define('auvyx-calendar', AuvyxCalendar);

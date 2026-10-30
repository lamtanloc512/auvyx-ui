// <auvyx-calendar>: date grid with keyboard navigation (fork addition).
//
// Attributes
//   value          "YYYY-MM-DD" (single) | "start/end" (range) | "d1,d2,…" (multiple)
//   mode           single (default) | range | multiple
//   months         how many months to show side by side (default 1)
//   month          first displayed month, "YYYY-MM" (default: month of value or today)
//   min, max       bounds; days outside are disabled, navigation stops at them
//   disabled-dates "YYYY-MM-DD" or "start/end" items, comma separated
//   disabled-days  weekdays to disable, "0,6" = weekends (0 = Sunday)
//   booked         like disabled-dates, but styled as taken (data-booked)
//   min-days, max-days   range length limits in days (inclusive), range mode
//   caption        label (default) | dropdown (month + year selects)
//   week-numbers   show ISO week numbers
//   name           keep a hidden input in sync so it submits with a form
//   lang           locale (default: nearest [lang], then the browser)
//   data-week-start  first weekday, 0 = Sunday … 6 (default 1 = Monday)
//
// JS API: el.value, el.dates (Date[]), el.goTo(date), el.focusDate(),
//   el.renderDay = (date) => html | null   (extra content inside each day)
// Events: `change` (bubbles) with detail { value, dates, complete }.
const pad = (n) => String(n).padStart(2, '0');
const toISO = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
const fromISO = (s) => {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec((s || '').trim());
  return m ? new Date(+m[1], +m[2] - 1, +m[3]) : null;
};
const dayKey = (d) => d.getFullYear() * 10000 + d.getMonth() * 100 + d.getDate();
const sameDay = (a, b) => !!a && !!b && dayKey(a) === dayKey(b);
const addDays = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
const addMonths = (d, n) => {
  const last = new Date(d.getFullYear(), d.getMonth() + n + 1, 0).getDate();
  return new Date(d.getFullYear(), d.getMonth() + n, Math.min(d.getDate(), last));
};
const monthStart = (d) => new Date(d.getFullYear(), d.getMonth(), 1);
const daysBetween = (a, b) => Math.round((new Date(b.getFullYear(), b.getMonth(), b.getDate()) - new Date(a.getFullYear(), a.getMonth(), a.getDate())) / 86400000);
const isoWeek = (d) => {
  const t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
  t.setUTCDate(t.getUTCDate() + 4 - (t.getUTCDay() || 7));
  return Math.ceil(((t - Date.UTC(t.getUTCFullYear(), 0, 1)) / 86400000 + 1) / 7);
};
const parseList = (s) => (s || '').split(',').map((x) => x.trim()).filter(Boolean).map((x) => {
  const [a, b] = x.split('/');
  const from = fromISO(a);
  return from ? [from, fromISO(b) || from] : null;
}).filter(Boolean);
const inList = (list, d) => list.some(([a, b]) => d >= a && d <= b);
const chevron = (path) => `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${path}"/></svg>`;
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

class AuvyxCalendar extends HTMLElement {
  static observedAttributes = ['value', 'min', 'max', 'mode', 'months', 'month', 'disabled-dates', 'disabled-days', 'booked', 'min-days', 'max-days', 'caption', 'week-numbers', 'lang'];

  connectedCallback() {
    this.readAll();
    const first = this.selected[0] || this.start || new Date();
    this.focused ||= this.clamp(first);
    const m = /^(\d{4})-(\d{2})$/.exec(this.getAttribute('month') || '');
    this.view ||= m ? new Date(+m[1], +m[2] - 1, 1) : monthStart(this.focused);
    if (!this._init) {
      this._init = true;
      this.addEventListener('click', (e) => this.onClick(e));
      this.addEventListener('keydown', (e) => this.onKey(e));
      this.addEventListener('change', (e) => this.onSelectChange(e));
    }
    this.render();
  }

  attributeChangedCallback(name, oldValue, value) {
    if (!this._init || oldValue === value || this._writing) return;
    this.readAll();
    if (name === 'value') {
      const first = this.selected[0] || this.start;
      if (first) {
        this.focused = first;
        this.view = monthStart(first);
      }
    }
    if (name === 'month') {
      const m = /^(\d{4})-(\d{2})$/.exec(value || '');
      if (m) this.view = new Date(+m[1], +m[2] - 1, 1);
    }
    this.render();
  }

  // ---- state
  readAll() {
    const mode = this.getAttribute('mode');
    this.mode = mode === 'range' || mode === 'multiple' ? mode : 'single';
    this.monthsShown = Math.max(1, Math.min(12, parseInt(this.getAttribute('months'), 10) || 1));
    this.min = fromISO(this.getAttribute('min'));
    this.max = fromISO(this.getAttribute('max'));
    this.disabledDates = parseList(this.getAttribute('disabled-dates'));
    this.bookedDates = parseList(this.getAttribute('booked'));
    this.disabledDays = (this.getAttribute('disabled-days') || '').split(',').map((x) => parseInt(x, 10)).filter((x) => x >= 0 && x <= 6);
    this.minDays = parseInt(this.getAttribute('min-days'), 10) || 0;
    this.maxDays = parseInt(this.getAttribute('max-days'), 10) || 0;
    const raw = this.getAttribute('value') || '';
    this.start = this.end = null;
    this.selected = [];
    if (this.mode === 'range') {
      const [a, b] = raw.split('/');
      this.start = fromISO(a);
      this.end = fromISO(b);
    } else if (this.mode === 'multiple') {
      this.selected = raw.split(',').map(fromISO).filter(Boolean);
    } else {
      this.start = fromISO(raw);
      if (this.start) this.selected = [this.start];
    }
  }

  get value() {
    if (this.mode === 'range') return this.start ? `${toISO(this.start)}/${this.end ? toISO(this.end) : ''}` : '';
    if (this.mode === 'multiple') return this.selected.map(toISO).join(',');
    return this.start ? toISO(this.start) : '';
  }

  set value(v) {
    this.setAttribute('value', v ?? '');
  }

  get dates() {
    if (this.mode === 'range') return [this.start, this.end].filter(Boolean);
    return [...this.selected];
  }

  set renderDay(fn) {
    this._renderDay = fn;
    if (this._init) this.render();
  }

  get renderDay() {
    return this._renderDay;
  }

  locale() {
    return this.getAttribute('lang') || this.closest('[lang]')?.getAttribute('lang') || navigator.language;
  }

  weekStart() {
    const n = parseInt(this.dataset.weekStart, 10);
    return Number.isFinite(n) ? ((n % 7) + 7) % 7 : 1;
  }

  clamp(d) {
    if (this.min && d < this.min) return this.min;
    if (this.max && d > this.max) return this.max;
    return d;
  }

  isDisabled(d) {
    if ((this.min && d < this.min) || (this.max && d > this.max)) return true;
    if (this.disabledDays.includes(d.getDay())) return true;
    if (inList(this.disabledDates, d) || inList(this.bookedDates, d)) return true;
    // Range length limits apply while choosing the end date.
    if (this.mode === 'range' && this.start && !this.end && d > this.start) {
      const len = daysBetween(this.start, d) + 1;
      if (this.minDays && len < this.minDays) return true;
      if (this.maxDays && len > this.maxDays) return true;
      // A range cannot jump over an unavailable day.
      for (let x = addDays(this.start, 1); x < d; x = addDays(x, 1)) {
        if (this.disabledDays.includes(x.getDay()) || inList(this.disabledDates, x) || inList(this.bookedDates, x)) return true;
      }
    }
    return false;
  }

  // ---- rendering
  render() {
    const locale = this.locale();
    const fmtMonth = new Intl.DateTimeFormat(locale, { month: 'long', year: 'numeric' });
    const fmtMonthOnly = new Intl.DateTimeFormat(locale, { month: 'short' });
    const fmtWeekday = new Intl.DateTimeFormat(locale, { weekday: 'short' });
    const fmtWeekdayLong = new Intl.DateTimeFormat(locale, { weekday: 'long' });
    const fmtDay = new Intl.DateTimeFormat(locale, { dateStyle: 'full' });
    const today = new Date();
    const ws = this.weekStart();
    const id = this.id || (this._uid ||= `cal-${Math.random().toString(36).slice(2, 8)}`);
    const weekNums = this.hasAttribute('week-numbers');
    const dropdown = this.getAttribute('caption') === 'dropdown';
    const prevDisabled = this.min && addMonths(this.view, -1) < monthStart(this.min);
    const nextDisabled = this.max && addMonths(this.view, this.monthsShown) > this.max;
    const hadFocus = this.contains(document.activeElement) && document.activeElement.matches('td > button');

    let html = '';
    for (let m = 0; m < this.monthsShown; m++) {
      const first = addMonths(this.view, m);
      const lead = (first.getDay() - ws + 7) % 7;
      const gridStart = addDays(first, -lead);
      const dim = new Date(first.getFullYear(), first.getMonth() + 1, 0).getDate();
      const weeks = Math.ceil((lead + dim) / 7);
      const titleId = `${id}-title-${m}`;

      let caption = `<h2 id="${titleId}" aria-live="polite">${esc(fmtMonth.format(first))}</h2>`;
      if (dropdown && m === 0) {
        const y0 = (this.min || addMonths(today, -12 * 10)).getFullYear();
        const y1 = (this.max || addMonths(today, 12 * 10)).getFullYear();
        let months = '';
        for (let i = 0; i < 12; i++) {
          const d = new Date(first.getFullYear(), i, 1);
          const off = (this.min && new Date(first.getFullYear(), i + 1, 0) < this.min) || (this.max && d > this.max);
          months += `<option value="${i}"${i === first.getMonth() ? ' selected' : ''}${off ? ' disabled' : ''}>${esc(fmtMonthOnly.format(d))}</option>`;
        }
        let years = '';
        for (let y = y0; y <= y1; y++) years += `<option value="${y}"${y === first.getFullYear() ? ' selected' : ''}>${y}</option>`;
        caption = `<div class="calendar-caption" id="${titleId}" aria-label="${esc(fmtMonth.format(first))}" role="group">`
          + `<select class="select" data-calendar-month aria-label="${esc(this.dataset.labelMonth || 'Month')}">${months}</select>`
          + `<select class="select" data-calendar-year aria-label="${esc(this.dataset.labelYear || 'Year')}">${years}</select></div>`;
      }
      const prev = m === 0 ? `<button type="button" data-nav="-1" aria-label="${esc(this.dataset.labelPrev || 'Previous month')}"${prevDisabled ? ' disabled' : ''}>${chevron('m15 18-6-6 6-6')}</button>` : '<span></span>';
      const next = m === this.monthsShown - 1 ? `<button type="button" data-nav="1" aria-label="${esc(this.dataset.labelNext || 'Next month')}"${nextDisabled ? ' disabled' : ''}>${chevron('m9 18 6-6-6-6')}</button>` : '<span></span>';

      let head = weekNums ? `<th scope="col" data-week-number><span class="sr-only">${esc(this.dataset.labelWeek || 'Week')}</span></th>` : '';
      for (let i = 0; i < 7; i++) {
        const d = addDays(gridStart, i);
        head += `<th scope="col" abbr="${esc(fmtWeekdayLong.format(d))}">${esc(fmtWeekday.format(d))}</th>`;
      }

      let body = '';
      for (let w = 0; w < weeks; w++) {
        body += '<tr>';
        if (weekNums) body += `<th scope="row" data-week-number>${isoWeek(addDays(gridStart, w * 7 + ((8 - ws) % 7)))}</th>`;
        for (let i = 0; i < 7; i++) {
          const d = addDays(gridStart, w * 7 + i);
          const outside = d.getMonth() !== first.getMonth();
          // With several months, an outside day belongs to the neighbouring grid: render it inert.
          const hideOutside = outside && this.monthsShown > 1;
          const attrs = [];
          if (outside) attrs.push('data-outside');
          if (inList(this.bookedDates, d)) attrs.push('data-booked');
          if (!hideOutside) {
            if (this.mode !== 'range' && this.selected.some((s) => sameDay(s, d))) attrs.push('aria-selected="true"');
            if (this.mode === 'range' && this.start) {
              const end = this.end || this.start;
              if (sameDay(d, this.start)) attrs.push('data-range-start');
              if (sameDay(d, end)) attrs.push('data-range-end');
              if (d > this.start && d < end) attrs.push('data-range-middle');
              if (d >= this.start && d <= end) attrs.push('aria-selected="true"');
            }
          }
          if (hideOutside) {
            body += `<td ${attrs.join(' ')} aria-hidden="true"></td>`;
            continue;
          }
          const tab = sameDay(d, this.focused) && !outside ? '0' : '-1';
          const extra = this._renderDay ? this._renderDay(d) : null;
          body += `<td ${attrs.join(' ')}><button type="button" data-date="${toISO(d)}" tabindex="${tab}" aria-label="${esc(fmtDay.format(d))}"`
            + `${sameDay(d, today) ? ' aria-current="date"' : ''}${this.isDisabled(d) ? ' disabled' : ''}>`
            + `<span>${d.getDate()}</span>${extra ? `<small>${extra}</small>` : ''}</button></td>`;
        }
        body += '</tr>';
      }
      html += `<section class="calendar-month"><header>${prev}${caption}${next}</header>`
        + `<table role="grid" aria-labelledby="${titleId}"${weekNums ? ' data-week-numbers' : ''}><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></section>`;
    }

    // Exactly one focusable day: if the focused day isn't on screen, use the first enabled one.
    const hidden = this.getAttribute('name') ? `<input type="hidden" name="${esc(this.getAttribute('name'))}" value="${esc(this.value)}">` : '';
    this.innerHTML = `<div class="calendar-months">${html}</div>${hidden}`;
    if (!this.querySelector('td > button[tabindex="0"]')) {
      const b = this.querySelector('td:not([data-outside]) > button:not(:disabled)') || this.querySelector('td > button');
      if (b) b.tabIndex = 0;
    }
    if (hadFocus) this.focusDate();
  }

  focusDate() {
    const b = this.querySelector(`td:not([data-outside]) > button[data-date="${toISO(this.focused)}"]`)
      || this.querySelector('td > button[tabindex="0"]');
    b?.focus({ preventScroll: true });
  }

  goTo(date) {
    const d = typeof date === 'string' ? fromISO(date) : date;
    if (!d) return;
    this.view = monthStart(d);
    this.focused = d;
    this.render();
  }

  visible(d) {
    const last = addMonths(this.view, this.monthsShown - 1);
    return d >= this.view && d < addMonths(last, 1);
  }

  moveFocus(d) {
    if ((this.min && d < this.min) || (this.max && d > this.max)) return;
    this.focused = d;
    if (!this.visible(d)) {
      this.view = d < this.view ? monthStart(d) : monthStart(addMonths(d, -(this.monthsShown - 1)));
      this.render();
    } else {
      this.querySelectorAll('td > button').forEach((b) => { b.tabIndex = b.dataset.date === toISO(d) && !b.closest('[data-outside]') ? 0 : -1; });
    }
    this.focusDate();
  }

  select(d) {
    if (this.mode === 'range') {
      if (!this.start || this.end || d < this.start) { this.start = d; this.end = null; }
      else this.end = d;
    } else if (this.mode === 'multiple') {
      const i = this.selected.findIndex((s) => sameDay(s, d));
      if (i >= 0) this.selected.splice(i, 1);
      else this.selected.push(d);
      this.selected.sort((a, b) => a - b);
    } else {
      this.start = d;
      this.selected = [d];
    }
    this.focused = d;
    this._writing = true;
    this.setAttribute('value', this.value);
    this._writing = false;
    this.render();
    this.focusDate();
    this.dispatchEvent(new CustomEvent('change', { bubbles: true, detail: { value: this.value, dates: this.dates, complete: this.mode !== 'range' || !!this.end } }));
  }

  // ---- events
  onClick(event) {
    const nav = event.target.closest('button[data-nav]');
    if (nav && !nav.disabled) {
      this.view = addMonths(this.view, +nav.dataset.nav);
      const dim = new Date(this.view.getFullYear(), this.view.getMonth() + 1, 0).getDate();
      this.focused = this.clamp(new Date(this.view.getFullYear(), this.view.getMonth(), Math.min(this.focused.getDate(), dim)));
      this.render();
      return;
    }
    const day = event.target.closest('button[data-date]');
    if (day && !day.disabled) this.select(fromISO(day.dataset.date));
  }

  onSelectChange(event) {
    const t = event.target;
    if (!(t instanceof HTMLSelectElement) || !t.closest('.calendar-caption')) return;
    event.stopPropagation();
    const month = +this.querySelector('[data-calendar-month]').value;
    const year = +this.querySelector('[data-calendar-year]').value;
    this.view = new Date(year, month, 1);
    this.focused = this.clamp(new Date(year, month, Math.min(this.focused.getDate(), new Date(year, month + 1, 0).getDate())));
    this.render();
    this.querySelector(t.hasAttribute('data-calendar-month') ? '[data-calendar-month]' : '[data-calendar-year]')?.focus();
  }

  onKey(event) {
    if (!event.target.matches('td > button')) return;
    const rtl = getComputedStyle(this).direction === 'rtl';
    const d = this.focused;
    const offset = (d.getDay() - this.weekStart() + 7) % 7;
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

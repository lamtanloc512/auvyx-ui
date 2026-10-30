// <auvyx-date-picker>: progressive enhancement of <input type="date"> (fork addition).
//
// Without JS the browser's native picker is used. With JS the input(s) stay in
// the form (hidden, still submitted) and are driven by a button + native
// popover holding an <auvyx-calendar>.
//
//   <auvyx-date-picker class="date-picker"><input type="date" name="day"></auvyx-date-picker>
//   <auvyx-date-picker class="date-picker" mode="range" months="2">
//     <input type="date" name="from"><input type="date" name="to">
//   </auvyx-date-picker>
//
// Passed through to the calendar: months, min, max (from the input), caption,
// week-numbers, disabled-days, disabled-dates, booked, min-days, max-days,
// data-week-start. Locale: nearest [lang]. Placeholder: data-placeholder.
const calendarIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>';
const PASS = ['months', 'caption', 'week-numbers', 'disabled-days', 'disabled-dates', 'booked', 'min-days', 'max-days'];
const asDate = (v) => (v ? new Date(`${v}T00:00:00`) : null);

class AuvyxDatePicker extends HTMLElement {
  connectedCallback() {
    if (this._init) return;
    this.inputs = [...this.querySelectorAll(':scope > input[type="date"]')];
    if (!this.inputs.length) return;
    this._init = true;
    this.range = this.getAttribute('mode') === 'range' && this.inputs.length >= 2;
    const first = this.inputs[0];
    const uid = first.id || `dp-${Math.random().toString(36).slice(2, 8)}`;
    const locale = this.closest('[lang]')?.getAttribute('lang') || navigator.language;
    this.format = new Intl.DateTimeFormat(locale, { dateStyle: 'medium' });

    this.button = document.createElement('button');
    this.button.type = 'button';
    this.button.className = 'btn';
    this.button.dataset.variant = this.dataset.variant || 'outline';
    this.button.setAttribute('popovertarget', `${uid}-popover`);
    this.button.setAttribute('aria-haspopup', 'dialog');
    const label = first.labels?.[0];
    if (label) {
      label.id ||= `${uid}-label`;
      this.button.setAttribute('aria-labelledby', `${label.id} ${uid}-value`);
      label.htmlFor = '';
      label.addEventListener('click', () => this.button.focus());
    }
    this.button.innerHTML = `${calendarIcon}<span id="${uid}-value"></span>`;

    this.panel = document.createElement('div');
    this.panel.id = `${uid}-popover`;
    this.panel.setAttribute('data-popover', '');
    this.panel.setAttribute('popover', '');
    this.panel.setAttribute('role', 'dialog');
    this.panel.setAttribute('aria-label', this.dataset.dialogLabel || (this.range ? 'Choose dates' : 'Choose date'));
    this.panel.dataset.side = this.dataset.side || 'bottom';
    this.panel.dataset.align = this.dataset.align || 'start';

    this.calendar = document.createElement('auvyx-calendar');
    this.calendar.className = 'calendar';
    if (this.range) this.calendar.setAttribute('mode', 'range');
    for (const attr of ['min', 'max']) if (first[attr]) this.calendar.setAttribute(attr, first[attr]);
    for (const attr of PASS) if (this.hasAttribute(attr)) this.calendar.setAttribute(attr, this.getAttribute(attr));
    if (this.dataset.weekStart) this.calendar.dataset.weekStart = this.dataset.weekStart;
    const v = this.range ? (this.inputs[0].value ? `${this.inputs[0].value}/${this.inputs[1].value}` : '') : first.value;
    if (v) this.calendar.setAttribute('value', v);
    this.panel.append(this.calendar);

    for (const input of this.inputs) {
      input.hidden = true;
      input.tabIndex = -1;
      // A hidden required input cannot show its own validation bubble: flag the button instead.
      input.addEventListener('invalid', (e) => {
        e.preventDefault();
        this.button.setAttribute('aria-invalid', 'true');
        this.button.focus();
      });
    }
    this.prepend(this.button);
    this.append(this.panel);
    this.update();

    this.calendar.addEventListener('change', (e) => {
      e.stopPropagation();
      const [a, b] = e.detail.value.split('/');
      this.setInput(this.inputs[0], a || '');
      if (this.range) this.setInput(this.inputs[1], b || '');
      this.button.removeAttribute('aria-invalid');
      this.update();
      if (e.detail.complete) {
        this.panel.hidePopover();
        this.button.focus();
      }
      this.dispatchEvent(new CustomEvent('change', { bubbles: true, detail: { value: e.detail.value, complete: e.detail.complete } }));
    });
    this.panel.addEventListener('toggle', (e) => {
      if (e.newState === 'open') requestAnimationFrame(() => this.calendar.focusDate?.());
    });
  }

  setInput(input, value) {
    if (input.value === value) return;
    input.value = value;
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
  }

  get value() {
    return this.range ? `${this.inputs[0].value}/${this.inputs[1].value}` : this.inputs[0].value;
  }

  update() {
    const text = this.button.querySelector('span');
    const a = asDate(this.inputs[0].value);
    const b = this.range ? asDate(this.inputs[1].value) : null;
    let label;
    if (this.range && a && b) label = this.format.formatRange(a, b);
    else if (a) label = this.format.format(a) + (this.range ? ' –' : '');
    else label = this.dataset.placeholder || this.inputs[0].placeholder || (this.range ? 'Pick a date range' : 'Pick a date');
    text.textContent = label;
    if (a) this.button.dataset.value = this.value;
    else delete this.button.dataset.value;
  }
}

if (!customElements.get('auvyx-date-picker')) customElements.define('auvyx-date-picker', AuvyxDatePicker);

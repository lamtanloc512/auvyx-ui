// <auvyx-date-picker>: progressive enhancement of <input type="date"> (fork addition).
// Without JS the browser's native picker is used. With JS the input is kept
// (hidden, still submitted with the form) and driven by a button + native
// popover holding an <auvyx-calendar>. Locale comes from the nearest [lang];
// placeholder from data-placeholder (default "Pick a date").
const calendarIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>';

class AuvyxDatePicker extends HTMLElement {
  connectedCallback() {
    if (this._init) return;
    this.input = this.querySelector('input[type="date"]');
    if (!this.input) return;
    this._init = true;
    const uid = this.input.id || `dp-${Math.random().toString(36).slice(2, 8)}`;
    const locale = this.closest('[lang]')?.getAttribute('lang') || navigator.language;
    this.format = new Intl.DateTimeFormat(locale, { dateStyle: 'medium' });

    this.button = document.createElement('button');
    this.button.type = 'button';
    this.button.className = 'btn';
    this.button.dataset.variant = 'outline';
    this.button.setAttribute('popovertarget', `${uid}-popover`);
    this.button.setAttribute('aria-haspopup', 'dialog');
    const label = this.input.labels?.[0];
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
    this.panel.setAttribute('aria-label', this.dataset.dialogLabel || 'Choose date');
    this.panel.dataset.side = this.dataset.side || 'bottom';
    this.panel.dataset.align = this.dataset.align || 'start';
    this.calendar = document.createElement('auvyx-calendar');
    this.calendar.className = 'calendar';
    for (const attr of ['min', 'max']) if (this.input[attr]) this.calendar.setAttribute(attr, this.input[attr]);
    if (this.input.value) this.calendar.setAttribute('value', this.input.value);
    if (this.dataset.weekStart) this.calendar.dataset.weekStart = this.dataset.weekStart;
    this.panel.append(this.calendar);

    this.input.hidden = true;
    this.input.tabIndex = -1;
    this.prepend(this.button);
    this.append(this.panel);
    this.update();

    this.calendar.addEventListener('change', (e) => {
      e.stopPropagation();
      this.input.value = e.detail.value;
      this.input.dispatchEvent(new Event('input', { bubbles: true }));
      this.input.dispatchEvent(new Event('change', { bubbles: true }));
      this.update();
      this.panel.hidePopover();
      this.button.focus();
    });
    // A hidden required input cannot show its own validation bubble: point at the button.
    this.input.addEventListener('invalid', (e) => {
      e.preventDefault();
      this.button.setAttribute('aria-invalid', 'true');
      this.button.focus();
    });
    this.input.addEventListener('change', () => this.button.removeAttribute('aria-invalid'));
    // Focus the selected (or today's) day when the popover opens.
    this.panel.addEventListener('toggle', (e) => {
      if (e.newState === 'open') requestAnimationFrame(() => this.calendar.focusDate?.());
    });
  }

  update() {
    const d = this.input.value ? new Date(`${this.input.value}T00:00:00`) : null;
    const text = this.button.querySelector('span');
    text.textContent = d ? this.format.format(d) : (this.dataset.placeholder || this.input.placeholder || 'Pick a date');
    if (d) this.button.dataset.value = this.input.value;
    else delete this.button.dataset.value;
  }
}

if (!customElements.get('auvyx-date-picker')) customElements.define('auvyx-date-picker', AuvyxDatePicker);

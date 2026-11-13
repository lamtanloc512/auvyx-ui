// <auvyx-prompt-input>: behavior for a .prompt-input form (fork addition).
// Enter sends and Shift+Enter adds a line (IME composition is respected);
// Send is disabled while the prompt is empty; files come from [data-attach],
// a drop or a paste and are listed as .attachment items in [data-files];
// .suggestions buttons fill the prompt, or send it with data-send.
// Emits a cancelable `prompt` event { text, files } and `stop`. Set the
// `streaming` attribute (or property) while a reply streams to show Stop, or
// `busy` for work that cannot be stopped: the field, Send and attach are
// disabled and the form gets aria-busy.
// Not part of auvyx.min.js: load js/prompt-input.min.js where you need it.
const FILE_ICON = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/></svg>';
const X_ICON = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>';

const size = (n) => (n < 1024 ? `${n} B` : n < 1048576 ? `${(n / 1024).toFixed(0)} KB` : `${(n / 1048576).toFixed(1)} MB`);

class AuvyxPromptInput extends HTMLElement {
  static observedAttributes = ['streaming', 'busy'];

  connectedCallback() {
    if (this._init) return;
    this.form = this.querySelector('form.prompt-input');
    this.field = this.form?.querySelector('textarea');
    if (!this.form || !this.field) return;
    this._init = true;
    this.files = [];
    this.list = this.form.querySelector('[data-files]');
    this.picker = this.form.querySelector('input[type="file"]');
    this.send = this.form.querySelector('[type="submit"]');
    this.attach = this.form.querySelector('[data-attach]');

    this.form.addEventListener('submit', (e) => { e.preventDefault(); this.submit(); });
    this.field.addEventListener('input', () => this.update());
    this.field.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey && !e.isComposing && e.keyCode !== 229) {
        e.preventDefault();
        this.submit();
      }
    });
    this.addEventListener('click', (e) => this.onClick(e));
    this.picker?.addEventListener('change', () => { this.addFiles(this.picker.files); this.picker.value = ''; });
    this.field.addEventListener('paste', (e) => {
      const files = [...(e.clipboardData?.files || [])];
      if (files.length) { e.preventDefault(); this.addFiles(files); }
    });
    if (this.picker) {
      this.form.addEventListener('dragover', (e) => {
        if (this.busy || ![...(e.dataTransfer?.types || [])].includes('Files')) return;
        e.preventDefault();
        this.form.setAttribute('data-dragover', '');
      });
      this.form.addEventListener('dragleave', (e) => { if (!this.form.contains(e.relatedTarget)) this.form.removeAttribute('data-dragover'); });
      this.form.addEventListener('drop', (e) => {
        this.form.removeAttribute('data-dragover');
        if (this.busy || !e.dataTransfer?.files.length) return;
        e.preventDefault();
        this.addFiles(e.dataTransfer.files);
      });
    }
    this.sync();
    this.update();
  }

  attributeChangedCallback() {
    if (this._init) this.sync();
  }

  get streaming() { return this.hasAttribute('streaming'); }
  set streaming(on) { this.toggleAttribute('streaming', !!on); }

  get busy() { return this.hasAttribute('busy'); }
  set busy(on) { this.toggleAttribute('busy', !!on); }

  get value() { return this.field?.value ?? ''; }
  set value(text) { if (this.field) { this.field.value = text; this.update(); } }

  sync() {
    const busy = this.busy;
    if (this.streaming) this.form.dataset.state = 'streaming';
    else if (busy) this.form.dataset.state = 'busy';
    else delete this.form.dataset.state;
    if (busy) this.form.setAttribute('aria-busy', 'true');
    else this.form.removeAttribute('aria-busy');
    if (busy !== !!this._busy) {
      this._busy = busy;
      // Disabling drops focus: give it back when the work is done, unless
      // the user has moved on to something else meanwhile.
      if (busy) this._refocus = document.activeElement === this.field;
      this.field.disabled = busy;
      if (this.attach) this.attach.disabled = busy;
      if (!busy && this._refocus && (!document.activeElement || document.activeElement === document.body)) this.field.focus();
    }
    this.update();
  }

  update() {
    if (this.send) this.send.disabled = this.streaming || this.busy || (!this.field.value.trim() && !this.files.length);
  }

  onClick(e) {
    if (this.busy && !e.target.closest('[data-stop]')) return;
    if (e.target.closest('[data-attach]')) return this.picker?.click();
    if (e.target.closest('[data-stop]')) return this.dispatchEvent(new CustomEvent('stop', { bubbles: true }));
    const remove = e.target.closest('[data-remove-file]');
    if (remove) {
      this.files.splice(Number(remove.dataset.removeFile), 1);
      this.renderFiles();
      return this.field.focus();
    }
    const chip = e.target.closest('.suggestions > :is(button, a)');
    if (chip) {
      e.preventDefault();
      this.value = chip.dataset.prompt ?? chip.textContent.trim();
      if (chip.hasAttribute('data-send')) this.submit();
      else this.field.focus();
    }
  }

  addFiles(list) {
    this.files.push(...list);
    this.renderFiles();
  }

  renderFiles() {
    if (this.list) {
      this.list.replaceChildren(...this.files.map((file, i) => {
        const item = document.createElement('div');
        item.className = 'attachment';
        item.dataset.state = 'done';
        item.innerHTML = `<figure>${FILE_ICON}</figure><div><strong></strong><small>${size(file.size)}</small></div>`
          + `<div data-actions><button type="button" class="btn" data-variant="ghost" data-size="icon-sm" data-remove-file="${i}">${X_ICON}</button></div>`;
        item.querySelector('strong').textContent = file.name;
        item.querySelector('button').setAttribute('aria-label', `Remove ${file.name}`);
        return item;
      }));
      this.list.hidden = !this.files.length;
    }
    this.update();
  }

  submit() {
    const text = this.field.value.trim();
    if (this.streaming || this.busy || (!text && !this.files.length)) return;
    const ok = this.dispatchEvent(new CustomEvent('prompt', { cancelable: true, bubbles: true, detail: { text, files: [...this.files] } }));
    if (!ok) return;
    this.field.value = '';
    this.files = [];
    this.renderFiles();
    this.field.focus();
  }
}

if (!customElements.get('auvyx-prompt-input')) customElements.define('auvyx-prompt-input', AuvyxPromptInput);

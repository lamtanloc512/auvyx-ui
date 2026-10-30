// Copy to clipboard (fork addition).
//
// Any element with [data-copy] copies text on click:
//   data-copy=""           → the <pre> of the closest .code-block
//   data-copy="#selector"  → the textContent of that element
//   data-copy-text="…"     → this literal text
// While copied, the button gets [data-copied] for 2s and its aria-label
// becomes the value of data-copied-label (default "Copied").
// One delegated listener, so it also works for content added later.
(() => {
  if (window.__basecoatCopy) return;
  window.__basecoatCopy = true;

  const sourceText = (button) => {
    if (button.hasAttribute('data-copy-text')) return button.getAttribute('data-copy-text');
    const target = button.getAttribute('data-copy');
    const el = target ? document.querySelector(target) : button.closest('.code-block')?.querySelector(':scope > pre');
    return el ? el.textContent : null;
  };

  const selectFallback = (button) => {
    const target = button.getAttribute('data-copy');
    const el = target ? document.querySelector(target) : button.closest('.code-block')?.querySelector(':scope > pre');
    if (!el) return;
    const range = document.createRange();
    range.selectNodeContents(el);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
  };

  document.addEventListener('click', async (event) => {
    const button = event.target.closest('[data-copy], [data-copy-text]');
    if (!button || button.disabled) return;
    const text = sourceText(button);
    if (text == null) return;

    try {
      await navigator.clipboard.writeText(text.replace(/\n$/, ''));
    } catch {
      selectFallback(button);
      return;
    }

    const label = button.getAttribute('aria-label');
    if (!button.hasAttribute('data-copied')) button.dataset.copyLabel = label ?? '';
    button.setAttribute('data-copied', '');
    button.setAttribute('aria-label', button.getAttribute('data-copied-label') || 'Copied');
    clearTimeout(button._copyTimer);
    button._copyTimer = setTimeout(() => {
      button.removeAttribute('data-copied');
      if (button.dataset.copyLabel) button.setAttribute('aria-label', button.dataset.copyLabel);
    }, 2000);
  });
})();

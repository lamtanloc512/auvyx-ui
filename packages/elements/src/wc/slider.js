// <auvyx-slider>: Web Components edition of Slider (see base.js).
// Wraps the HTML edition's <input type="range">. value: the input's value
// (a string, like the input). Re-emits the input's `input` and `change`.
import { AuvyxWrapper } from './base.js';

class AuvyxSlider extends AuvyxWrapper {
  static component = 'range';
  static rootSelector = 'input[type="range"]';
  static relayed = ['input', 'change'];
  static relayNative = true;

  get value() {
    return this.root ? this.root.value : null;
  }

  set value(value) {
    if (this.defer(value)) return;
    this.root.value = value;
    // Repaint the filled track like the range behavior does on `input`,
    // without firing an event (setting value from code is silent).
    const { min, max } = this.root;
    const lo = parseFloat(min || '0'), hi = parseFloat(max || '100');
    this.root.style.setProperty('--slider-value', `${hi === lo ? 0 : ((parseFloat(this.root.value) - lo) / (hi - lo)) * 100}%`);
  }
}

if (!customElements.get('auvyx-slider')) customElements.define('auvyx-slider', AuvyxSlider);

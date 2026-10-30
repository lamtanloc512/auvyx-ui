// Public API of every <auvyx-*> element, the single source for
// dist/custom-elements.json, the TypeScript types (dist/types/) and the docs'
// Web Component tables. Keep it in sync with the element sources.
//
// Types are TypeScript type expressions. Events list their CustomEvent detail.

const value = (type, description) => ({ name: 'value', type, description, attribute: 'value' });
const open = (description) => ({ name: 'open', type: 'boolean', description, attribute: 'open' });
const change = (description, detail = '{ value: string | null }') => ({ name: 'change', detail, description });
const toggle = (description) => ({ name: 'toggle', detail: '{ open: boolean }', description });
const itemSelect = { name: 'select', detail: '{ value: string }', description: "The user activated an item; detail.value is its data-value or text" };

export const ELEMENTS = [
  // Web Components edition: wrappers around the HTML edition (packages/elements/src/wc).
  { tag: 'auvyx-tabs', className: 'AuvyxTabsElement', module: 'wc/tabs.min.js', key: 'tabs', description: 'Tabs; wraps the HTML edition markup (.tabs).',
    properties: [value('string | null', "The selected tab's data-value or id")], events: [change('The user selected a tab')] },
  { tag: 'auvyx-select', className: 'AuvyxSelectElement', module: 'wc/select.min.js', key: 'select', description: 'Select; wraps the HTML edition markup (.select).',
    properties: [value('string | string[] | null', "The selected option's data-value (an array when multiple)")], events: [change('The user picked an option', '{ value: string | string[] | null }')] },
  { tag: 'auvyx-combobox', className: 'AuvyxComboboxElement', module: 'wc/combobox.min.js', key: 'combobox', description: 'Combobox; wraps the HTML edition markup (.combobox).',
    properties: [value('string | string[] | null', "The selected option's data-value (an array when multiple)")], events: [change('The user picked an option', '{ value: string | string[] | null }')] },
  { tag: 'auvyx-command', className: 'AuvyxCommandElement', module: 'wc/command.min.js', key: 'command', description: 'Command menu; wraps the HTML edition markup (.command).',
    properties: [], events: [itemSelect] },
  { tag: 'auvyx-dropdown-menu', className: 'AuvyxDropdownMenuElement', module: 'wc/dropdown-menu.min.js', key: 'dropdown-menu', description: 'Dropdown menu; wraps the JS markup or the native popover variant (.dropdown-menu).',
    properties: [open('Whether the menu is shown')], events: [toggle('The menu opened or closed'), itemSelect] },
  { tag: 'auvyx-popover', className: 'AuvyxPopoverElement', module: 'wc/popover.min.js', key: 'popover', description: 'Popover; wraps the JS markup or the native popover variant (.popover).',
    properties: [open('Whether the panel is shown')], events: [toggle('The panel opened or closed')] },
  { tag: 'auvyx-accordion', className: 'AuvyxAccordionElement', module: 'wc/accordion.min.js', key: 'accordion', description: 'Accordion; wraps the HTML edition markup (.accordion).',
    properties: [value('string | string[] | null', "The open item's data-value, id or position (an array with data-multiple)")], events: [change('The user opened or closed an item', '{ value: string | string[] | null }')] },
  { tag: 'auvyx-sidebar', className: 'AuvyxSidebarElement', module: 'wc/sidebar.min.js', key: 'sidebar', description: 'Sidebar; wraps the HTML edition markup (.sidebar).',
    properties: [open('Whether the sidebar is expanded')], events: [toggle('The sidebar expanded or collapsed')] },
  { tag: 'auvyx-toaster', className: 'AuvyxToasterElement', module: 'wc/toast.min.js', key: 'toast', description: 'Toaster; wraps the HTML edition toaster (.toaster).',
    properties: [], events: [],
    methods: [{ name: 'toast', signature: '(options: AuvyxToastOptions) => void', description: 'Show a toast; same options as the HTML edition' }] },
  { tag: 'auvyx-slider', className: 'AuvyxSliderElement', module: 'wc/slider.min.js', key: 'slider', description: 'Slider; wraps the HTML edition <input type="range">.',
    properties: [value('string', "The input's value")], events: [{ name: 'input', detail: '{ value: string }', description: 'The value is changing' }, change('The user finished changing it', '{ value: string }')] },
  { tag: 'auvyx-drawer', className: 'AuvyxDrawerElement', module: 'wc/drawer.min.js', key: 'drawer', description: 'Drawer; wraps the HTML edition <dialog class="drawer">.',
    properties: [open('Whether the drawer is shown')], events: [toggle('The drawer opened or closed')] },

  // Elements that are components in their own right (packages/elements/src).
  { tag: 'auvyx-calendar', className: 'AuvyxCalendarElement', module: 'js/calendar.min.js', key: 'calendar', description: 'Date grid with keyboard navigation.',
    attributes: [
      { name: 'mode', type: "'single' | 'range' | 'multiple'", description: 'Selection mode (default single)' },
      { name: 'months', type: 'string', description: 'How many months to show side by side' },
      { name: 'month', type: 'string', description: 'First displayed month, "YYYY-MM"' },
      { name: 'min', type: 'string', description: 'Earliest selectable day, "YYYY-MM-DD"' },
      { name: 'max', type: 'string', description: 'Latest selectable day, "YYYY-MM-DD"' },
      { name: 'disabled-dates', type: 'string', description: 'Comma-separated days or "start/end" ranges' },
      { name: 'disabled-days', type: 'string', description: 'Weekdays to disable, "0,6" = weekends' },
      { name: 'booked', type: 'string', description: 'Like disabled-dates, styled as taken' },
      { name: 'min-days', type: 'string', description: 'Shortest range in days (range mode)' },
      { name: 'max-days', type: 'string', description: 'Longest range in days (range mode)' },
      { name: 'caption', type: "'label' | 'dropdown'", description: 'Month caption: label or month/year selects' },
      { name: 'week-numbers', type: 'boolean', description: 'Show ISO week numbers' },
      { name: 'name', type: 'string', description: 'Keep a hidden input in sync for forms' },
    ],
    properties: [
      value('string', '"YYYY-MM-DD" (single), "start/end" (range) or "d1,d2,…" (multiple)'),
      { name: 'dates', type: 'Date[]', description: 'Selected dates', readonly: true },
      { name: 'renderDay', type: '((date: Date) => string | null) | undefined', description: 'Extra HTML inside each day' },
    ],
    events: [change('The user picked a date', '{ value: string; dates: Date[]; complete: boolean }')],
    methods: [
      { name: 'goTo', signature: '(date: Date | string) => void', description: 'Show the month containing date' },
      { name: 'focusDate', signature: '() => void', description: 'Focus the selected or current day' },
    ] },
  { tag: 'auvyx-date-picker', className: 'AuvyxDatePickerElement', module: 'js/date-picker.min.js', key: 'date-picker', description: 'Progressive enhancement of <input type="date"> with a calendar popover.',
    attributes: [
      { name: 'mode', type: "'single' | 'range'", description: 'Two inputs for a range' },
      { name: 'months', type: 'string', description: 'Months shown in the calendar' },
      { name: 'caption', type: "'label' | 'dropdown'", description: 'Passed to the calendar' },
      { name: 'week-numbers', type: 'boolean', description: 'Passed to the calendar' },
      { name: 'disabled-days', type: 'string', description: 'Passed to the calendar' },
      { name: 'disabled-dates', type: 'string', description: 'Passed to the calendar' },
      { name: 'booked', type: 'string', description: 'Passed to the calendar' },
      { name: 'min-days', type: 'string', description: 'Passed to the calendar (range mode)' },
      { name: 'max-days', type: 'string', description: 'Passed to the calendar (range mode)' },
    ],
    properties: [{ name: 'value', type: 'string', description: '"YYYY-MM-DD", or "start/end" in range mode', readonly: true }],
    events: [change('A date was picked', '{ value: string }')] },
  { tag: 'auvyx-data-table', className: 'AuvyxDataTableElement', module: 'js/data-table.min.js', key: 'data-table', description: 'Sorting, filtering, selection, column visibility and pagination over a server-rendered table.',
    properties: [], events: [{ name: 'selectionchange', detail: '{ rows: HTMLTableRowElement[] }', description: 'Row selection changed' }] },
  { tag: 'auvyx-resizable', className: 'AuvyxResizableElement', module: 'js/resizable.min.js', key: 'resizable', description: 'Drag or arrow-key the separators between panels.',
    properties: [], events: [{ name: 'resize', detail: '{ sizes: number[] }', description: 'Panel sizes changed (percent)' }] },
  { tag: 'auvyx-context-menu', className: 'AuvyxContextMenuElement', module: 'js/context-menu.min.js', key: 'context-menu', description: 'Opens a native menu popover at the pointer.',
    properties: [], events: [],
    methods: [{ name: 'openAt', signature: '(x: number, y: number) => void', description: 'Open the menu at viewport coordinates' }] },
];

// Toast options accepted by toaster.toast() in both editions.
export const EXTRA_TYPES = `export interface AuvyxToastOptions {
  category?: 'success' | 'error' | 'info' | 'warning';
  title?: string;
  description?: string;
  /** Treat title, description and labels as HTML instead of text. */
  html?: boolean;
  action?: { label: string; href?: string; onclick?: string };
  cancel?: { label: string; onclick?: string };
  /** Milliseconds before it closes (default 3000, 5000 for errors); -1 keeps it open. */
  duration?: number;
  /** SVG markup replacing the category icon (inserted as is). */
  icon?: string;
}`;

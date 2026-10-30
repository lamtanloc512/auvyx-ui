import type {} from './auvyx-types/elements';
const tabs = document.querySelector('auvyx-tabs')!;
const v: string | null = tabs.value;
tabs.addEventListener('change', (e) => { const x: string | null = e.detail.value; void x; });
document.querySelector('auvyx-dropdown-menu')!.addEventListener('select', (e) => { const s: string = e.detail.value; void s; });
const drawer = document.querySelector('auvyx-drawer')!; drawer.open = true;
document.querySelector('auvyx-toaster')!.toast({ title: 'Saved', category: 'success', duration: -1 });
// @ts-expect-error unknown category
document.querySelector('auvyx-toaster')!.toast({ category: 'nope' });
const cal = document.querySelector('auvyx-calendar')!; cal.goTo('2026-04-01'); const d: Date[] = cal.dates;
cal.addEventListener('change', (e) => { const c: boolean = e.detail.complete; void c; });
// @ts-expect-error dates is readonly
cal.dates = [];
// @ts-expect-error open is boolean
drawer.open = 'yes';
document.querySelector('auvyx-resizable')!.addEventListener('resize', (e) => { const n: number[] = e.detail.sizes; void n; });
void v; void d;

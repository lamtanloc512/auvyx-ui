import type {} from './auvyx-types/react';
import { useState, useRef } from 'react';
import type { AuvyxToasterElement } from './auvyx-types/elements';
export function App() {
  const [tab, setTab] = useState('account');
  const [open, setOpen] = useState(false);
  const toaster = useRef<AuvyxToasterElement>(null);
  return (<>
    <auvyx-tabs value={tab} onChange={(e) => setTab(e.currentTarget.value ?? '')} class="x"><div className="tabs" /></auvyx-tabs>
    <auvyx-dropdown-menu open={open} ontoggle={(e) => setOpen(e.detail.open)} onselect={(e) => console.log(e.detail.value)} />
    <auvyx-slider value="3" onInput={(e) => console.log(e.currentTarget.value)} />
    <auvyx-select value={['a', 'b']} onChange={(e) => console.log(e.nativeEvent.detail.value)} />
    <auvyx-calendar mode="range" months="2" onChange={(e) => console.log(e.currentTarget.dates)} />
    <auvyx-toaster ref={toaster} />
    <button onClick={() => toaster.current?.toast({ title: 'Hi' })} />
    {/* @ts-expect-error onToggle never fires on custom elements */}
    <auvyx-drawer onToggle={() => {}} />
    {/* @ts-expect-error open is boolean */}
    <auvyx-popover open="yes" />
    {/* @ts-expect-error value is a string */}
    <auvyx-tabs value={3} />
    {/* @ts-expect-error unknown calendar mode */}
    <auvyx-calendar mode="weekly" />
  </>);
}

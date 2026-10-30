"""Calendar blocks (ports of shadcn calendar-01..32)."""
from common import page, register, ic

CSS = """
  body { background: var(--background); }
  .cal-box { border: 1px solid var(--border); border-radius: var(--radius); box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05); }
  .cal-note { margin: 0; font-size: 0.875rem; color: var(--muted-foreground); text-align: center; text-wrap: balance; }
  .cal-card { inline-size: fit-content; max-inline-size: 100%; }
  .cal-card > section { display: flex; justify-content: center; }
  .cal-card > section > .calendar { padding: 0; }
  .cal-center { display: flex; flex-direction: column; align-items: center; gap: 1rem; }
  .cover > .cal-center, .cover > .card, .cover > form, .cover > .calendar { inline-size: auto; }
  .cal-row { display: flex; flex-wrap: wrap; gap: 1rem; align-items: end; }
  .cal-row > .field { inline-size: auto; }
  .cal-times { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; inline-size: 100%; }
  .cal-times .field input { inline-size: 100%; }
  input[type='time']::-webkit-calendar-picker-indicator { display: none; }
"""

blocks = []


def add(n, desc, body, css="", scripts=""):
    bid = f"calendar-{n:02d}"
    page(bid, f"Calendar {n:02d}", f'<main class="cover">{body}</main>', CSS + css, scripts=f"<script>{scripts}</script>\n" if scripts else "")
    blocks.append({"id": bid, "title": f"Calendar {n:02d}", "description": desc, "category": "calendar"})


TODAY_JS = "const pad=n=>String(n).padStart(2,'0');const iso=d=>`${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;const addDays=(d,n)=>new Date(d.getFullYear(),d.getMonth(),d.getDate()+n);const today=new Date();"
cal = lambda attrs="", box=True: f'<auvyx-calendar class="calendar{" cal-box" if box else ""}" {attrs}></auvyx-calendar>'

add(1, "A simple calendar.", cal('value="2026-06-12"'))
add(2, "Multiple months with single selection.", cal('months="2" value="2026-06-12"'))
add(3, "Multiple months with multiple selection.", cal('months="2" mode="multiple" value="2026-06-12,2026-06-18,2026-07-03,2026-07-08"'))
add(4, "Single month with range selection.", cal('mode="range" value="2026-06-12/2026-06-20"'))
add(5, "Multiple months with range selection.", cal('mode="range" months="2" value="2026-06-12/2026-07-08"'))
add(6, "Range selection with minimum days.", f'<div class="cal-center">{cal(chr(32).join(["mode=\"range\"", "min-days=\"5\"", "value=\"2026-06-12/2026-06-26\""]))}<p class="cal-note">A minimum of 5 days is required</p></div>')
add(7, "Range selection with minimum and maximum days.", f'<div class="cal-center">{cal("mode=\"range\" months=\"2\" min-days=\"2\" max-days=\"20\" value=\"2026-06-18/2026-07-07\"")}<p class="cal-note">Your stay must be between 2 and 20 nights</p></div>')
add(8, "Calendar with disabled days before today.", cal('id="cal" data-min-today'), scripts=TODAY_JS + "const c=document.getElementById('cal');c.setAttribute('min',iso(today));c.setAttribute('value',iso(addDays(today,3)));")
add(9, "Range calendar with disabled weekends.", cal('mode="range" months="2" disabled-days="0,6" value="2026-06-17/2026-06-19"'))
add(10, "Calendar with a Today button.",
    '<div class="card cal-card"><header><h2>Appointment</h2><p>Find a date</p><div class="card-action"><button type="button" class="btn" data-variant="outline" data-size="sm" id="today">Today</button></div></header>'
    f'<section>{cal("id=\"cal\" month=\"2026-06\" value=\"2026-06-12\"", box=False)}</section></div>',
    scripts=TODAY_JS + "const c=document.getElementById('cal');document.getElementById('today').onclick=()=>{c.value=iso(today);c.goTo(today);};")
add(11, "Range calendar limited to June and July.", f'<div class="cal-center">{cal("mode=\"range\" months=\"2\" min=\"2026-06-01\" max=\"2026-07-31\" month=\"2026-06\" value=\"2026-06-12/2026-06-26\"")}<p class="cal-note">We are open in June and July only.</p></div>')
add(12, "Localized calendar with a language selector.",
    '<div class="card cal-card"><header><h2>Book an appointment</h2><p>Select the dates for your appointment</p><div class="card-action">'
    '<select class="select" id="lang" aria-label="Language"><option value="en-US">English</option><option value="es">Español</option><option value="vi">Tiếng Việt</option><option value="ja">日本語</option></select></div></header>'
    f'<section>{cal("id=\"cal\" mode=\"range\" months=\"2\" lang=\"en-US\" value=\"2026-06-12/2026-06-26\"", box=False)}</section></div>',
    scripts="document.getElementById('lang').onchange=e=>document.getElementById('cal').setAttribute('lang',e.target.value);")
add(13, "Calendar with a month and year dropdown.",
    f'<div class="cal-center">{cal("id=\"cal\" caption=\"dropdown\" value=\"2026-06-12\" min=\"2000-01-01\" max=\"2035-12-31\"")}'
    '<div role="group" class="field"><label for="layout">Dropdown</label><select class="select" id="layout"><option value="dropdown">Month and Year</option><option value="label">Label</option></select></div></div>',
    scripts="document.getElementById('layout').onchange=e=>document.getElementById('cal').setAttribute('caption',e.target.value);")
add(14, "Calendar with booked dates.", f'<div class="cal-center">{cal("value=\"2026-06-12\" booked=\"2026-06-03/2026-06-06,2026-06-15,2026-06-22/2026-06-24\"")}<p class="cal-note">Struck-through days are already booked.</p></div>')
add(15, "Calendar with week numbers.", cal('week-numbers value="2026-06-12"'))
add(16, "Calendar with start and end time.",
    f'<div class="card cal-card" data-size="sm"><section>{cal("value=\"2026-06-12\"", box=False)}</section>'
    '<footer class="cal-foot"><div class="cal-times">'
    '<div role="group" class="field"><label for="t1">Start Time</label><input id="t1" type="time" step="1" value="10:30:00"></div>'
    '<div role="group" class="field"><label for="t2">End Time</label><input id="t2" type="time" step="1" value="12:30:00"></div></div></footer></div>',
    "\n  .cal-foot { border-block-start: 1px solid var(--border); padding-block-start: 1rem; }")
add(17, "Calendar with inline time inputs.",
    f'<div class="card cal-card" data-size="sm"><section>{cal("value=\"2026-06-12\"", box=False)}</section>'
    '<footer class="cal-foot"><div class="stack" data-gap="3" style="inline-size:100%">'
    '<div class="cluster" data-gap="2"><label for="t1" class="cal-tl">Start</label><input class="input cal-ti" id="t1" type="time" step="1" value="10:30:00"></div>'
    '<div class="cluster" data-gap="2"><label for="t2" class="cal-tl">End</label><input class="input cal-ti" id="t2" type="time" step="1" value="12:30:00"></div></div></footer></div>',
    "\n  .cal-foot { border-block-start: 1px solid var(--border); padding-block-start: 1rem; }\n  .cal-tl { inline-size: 3rem; font-size: 0.875rem; font-weight: 500; }\n  .cal-ti { flex: 1; inline-size: auto; }")
add(18, "Calendar with a larger, responsive cell size.", cal('value="2026-06-12" class="calendar cal-box cal-big"').replace('class="calendar cal-box" value', 'value').replace('class="calendar cal-box"  ', ''),
    "\n  .cal-big { --cell-size: clamp(2.25rem, 11vw, 3.5rem); }\n  .cal-big .calendar-month > table td > button { font-size: 1rem; }")
add(19, "Calendar with quick presets.",
    f'<div class="card cal-card" data-size="sm"><section>{cal("id=\"cal\" value=\"2026-06-12\" month=\"2026-06\"", box=False)}</section>'
    '<footer class="cal-foot"><div class="cluster" data-gap="2" id="presets">'
    + "".join(f'<button type="button" class="btn" data-variant="outline" data-size="sm" data-days="{d}">{t}</button>' for t, d in [("Today", 0), ("Tomorrow", 1), ("In 3 days", 3), ("In a week", 7), ("In 2 weeks", 14)])
    + '</div></footer></div>',
    "\n  .cal-foot { border-block-start: 1px solid var(--border); padding-block-start: 1rem; }\n  #presets { max-inline-size: 16rem; }",
    TODAY_JS + "const c=document.getElementById('cal');document.getElementById('presets').onclick=e=>{const b=e.target.closest('[data-days]');if(!b)return;const d=addDays(today,+b.dataset.days);c.value=iso(d);c.goTo(d);};")

SLOTS = [f"{h:02d}:{m:02d}" for h in range(9, 18) for m in (0, 15, 30, 45)] + ["18:00"]
BOOKED = {"10:00", "10:30", "11:15", "13:30", "14:45", "16:00", "16:15"}
add(20, "Calendar with a time slot picker and booking summary.",
    '<div class="card cal-booking"><section class="cal-booking-body">'
    f'<div>{cal("id=\"cal\" value=\"2026-06-12\" month=\"2026-06\" disabled-days=\"0\"", box=False)}</div>'
    '<div class="cal-slots" role="radiogroup" aria-label="Time">'
    + "".join(f'<label class="toggle" data-variant="outline"><input type="radio" name="slot" value="{s}"{" disabled" if s in BOOKED else ""}{" checked" if s == "11:30" else ""}>{s}</label>' for s in SLOTS)
    + '</div></section><footer class="cal-booking-foot"><p id="summary" class="cal-sum"></p><button type="button" class="btn" id="go">Continue</button></footer></div>',
    """
  .cal-booking { padding: 0; gap: 0; max-inline-size: 100%; }
  .cal-booking-body { display: flex; flex-wrap: wrap; padding: 0 !important; }
  .cal-booking-body > div:first-child { padding: 1.25rem; }
  .cal-booking-body .calendar { padding: 0; }
  .cal-slots { display: flex; flex-direction: column; gap: 0.5rem; padding: 1.25rem; overflow-y: auto; max-block-size: 18rem; inline-size: 9rem; border-inline-start: 1px solid var(--border); }
  .cal-slots .toggle { inline-size: 100%; }
  @media (width < 32rem) { .cal-slots { inline-size: 100%; flex-direction: row; flex-wrap: wrap; max-block-size: 10rem; border-inline-start: 0; border-block-start: 1px solid var(--border); } .cal-slots .toggle { inline-size: auto; } }
  .cal-booking-foot { display: flex; flex-wrap: wrap; align-items: center; gap: 1rem; padding: 1.25rem !important; border-block-start: 1px solid var(--border); }
  .cal-sum { margin: 0; flex: 1; font-size: 0.875rem; }
""",
    "const c=document.getElementById('cal'),s=document.getElementById('summary'),fmt=new Intl.DateTimeFormat(undefined,{weekday:'long',day:'numeric',month:'long'});"
    "function upd(){const t=document.querySelector('[name=slot]:checked');const d=c.dates[0];s.innerHTML=d&&t?`Your meeting is booked for <strong>${fmt.format(d)}</strong> at <strong>${t.value}</strong>.`:'Select a date and time for your meeting.';document.getElementById('go').disabled=!(d&&t);}"
    "c.addEventListener('change',upd);document.querySelector('.cal-slots').addEventListener('change',upd);customElements.whenDefined('auvyx-calendar').then(upd);")

add(21, "Range calendar with custom day content.",
    cal('id="cal" mode="range" months="2" value="2026-06-12/2026-06-17" month="2026-06" class="calendar cal-box cal-price"').replace('class="calendar cal-box" id', 'id'),
    "\n  .cal-price { --cell-size: 2.75rem; }\n  .cal-price .calendar-month > table td > button { min-block-size: 2.75rem; }",
    "customElements.whenDefined('auvyx-calendar').then(()=>{document.getElementById('cal').renderDay=d=>{const we=d.getDay()===0||d.getDay()===6;return we?'$120':'$100';};});")

add(22, "A date picker in a popover.",
    '<form class="stack" data-gap="3" onsubmit="event.preventDefault()"><div role="group" class="field"><label for="dob">Date of birth</label>'
    '<auvyx-date-picker class="date-picker" caption="dropdown" data-placeholder="Select date"><input id="dob" type="date" name="dob" min="1930-01-01" max="2026-12-31"></auvyx-date-picker></div></form>')
add(23, "A date range picker.",
    '<form class="stack" data-gap="3" onsubmit="event.preventDefault()"><div role="group" class="field"><label for="from">Select your stay</label>'
    '<auvyx-date-picker class="date-picker" mode="range" months="2"><input id="from" type="date" name="from" value="2026-06-12"><input type="date" name="to" value="2026-06-19"></auvyx-date-picker></div></form>',
    "\n  .date-picker > button:first-child { inline-size: 18rem; }")
add(24, "A date and time picker.",
    '<form class="cal-row" onsubmit="event.preventDefault()"><div role="group" class="field"><label for="d">Date</label>'
    '<auvyx-date-picker class="date-picker" data-placeholder="Select date"><input id="d" type="date" name="date"></auvyx-date-picker></div>'
    '<div role="group" class="field"><label for="t">Time</label><input id="t" type="time" name="time" step="1" value="10:30:00"></div></form>',
    "\n  .date-picker > button:first-child { inline-size: 10rem; }")
add(25, "A date and time range picker.",
    '<form class="stack" data-gap="4" onsubmit="event.preventDefault()"><div role="group" class="field"><label for="r">Dates</label>'
    '<auvyx-date-picker class="date-picker" mode="range" months="2"><input id="r" type="date" name="from" value="2026-06-12"><input type="date" name="to" value="2026-06-19"></auvyx-date-picker></div>'
    '<div class="cal-times"><div role="group" class="field"><label for="t1">From</label><input id="t1" type="time" name="from_time" value="14:00"></div>'
    '<div role="group" class="field"><label for="t2">To</label><input id="t2" type="time" name="to_time" value="11:00"></div></div></form>',
    "\n  .date-picker > button:first-child { inline-size: 100%; }\n  .date-picker { display: flex; }\n  .cover > form { inline-size: 18rem; }")
add(26, "Check-in and check-out pickers with times.",
    '<form class="stack" data-gap="4" onsubmit="event.preventDefault()">'
    + "".join(f'<div class="cal-row"><div role="group" class="field"><label for="{k}">{t}</label><auvyx-date-picker class="date-picker"><input id="{k}" type="date" name="{k}" value="{v}"></auvyx-date-picker></div>'
              f'<div role="group" class="field"><label for="{k}t" class="sr-only">{t} time</label><input id="{k}t" type="time" name="{k}_time" value="{tv}"></div></div>'
              for k, t, v, tv in [("checkin", "Check-in", "2026-06-12", "14:00"), ("checkout", "Check-out", "2026-06-19", "11:00")])
    + '</form>',
    "\n  .date-picker > button:first-child { inline-size: 10rem; }")

add(27, "Web analytics chart filtered by a date range.",
    '<div class="card cal-chart"><header><h2>Web Analytics</h2><p>Showing total visitors for the selected range</p><div class="card-action">'
    '<auvyx-date-picker class="date-picker" mode="range" data-align="end" id="range"><input type="date" name="from" value="2026-06-05"><input type="date" name="to" value="2026-06-20"></auvyx-date-picker></div></header>'
    '<section><div class="cal-bars" id="bars" role="img" aria-label="Visitors per day"></div><p class="cal-note" id="total"></p></section></div>',
    """
  .cover > .cal-chart { inline-size: min(40rem, 100%); }
  .cal-bars { display: flex; align-items: flex-end; gap: 2px; block-size: 12rem; }
  .cal-bars > span { flex: 1; min-inline-size: 2px; border-radius: 3px 3px 0 0; background: var(--chart-2, var(--primary)); }
  .card-action .date-picker > button:first-child { font-size: 0.8125rem; }
  @media (width < 36rem) { .cal-chart > header { grid-template-columns: 1fr; } .cal-chart .card-action { grid-column: 1; grid-row: auto; justify-self: start; } }
""",
    "const rand=s=>{let x=Math.sin(s)*10000;return x-Math.floor(x)};const day=d=>Math.floor(d/86400000);"
    "function draw(){const r=document.getElementById('range');const [a,b]=r.value.split('/');if(!a||!b)return;const s=new Date(a+'T00:00:00'),e=new Date(b+'T00:00:00');"
    "const vals=[];for(let d=new Date(s);d<=e;d.setDate(d.getDate()+1)){vals.push(Math.round(120+rand(day(d.getTime()))*380));}"
    "const max=Math.max(...vals);document.getElementById('bars').innerHTML=vals.map(v=>`<span style=\"block-size:${v/max*100}%\" title=\"${v}\"></span>`).join('');"
    "document.getElementById('total').textContent=`${vals.reduce((x,y)=>x+y,0).toLocaleString()} visitors over ${vals.length} days`;}"
    "document.getElementById('range').addEventListener('change',draw);customElements.whenDefined('auvyx-date-picker').then(()=>requestAnimationFrame(draw));")

add(28, "A text input with an attached date picker.",
    '<form onsubmit="event.preventDefault()" class="stack" data-gap="2"><div role="group" class="field"><label for="date">Subscription Date</label>'
    '<div class="popover cal-attach"><div class="input-group"><input id="date" type="text" value="June 01, 2026" placeholder="June 01, 2026" autocomplete="off">'
    f'<button type="button" class="btn" data-variant="ghost" data-size="icon-xs" data-align="inline-end" popovertarget="date-pop" aria-label="Select date">{ic("calendar")}</button></div>'
    '<div id="date-pop" data-popover popover data-side="bottom" data-align="end" class="cal-pop"><auvyx-calendar class="calendar" id="cal" value="2026-06-01"></auvyx-calendar></div></div></div></form>',
    "\n  .cal-attach { display: block; inline-size: 18rem; }\n  .cal-attach > .input-group { anchor-name: --bc-popover; }\n  .cal-pop { padding: 0 !important; inline-size: auto !important; }",
    "const i=document.getElementById('date'),c=document.getElementById('cal'),p=document.getElementById('date-pop');const pad=n=>String(n).padStart(2,'0');"
    "const fmt=d=>d.toLocaleDateString('en-US',{day:'2-digit',month:'long',year:'numeric'});"
    "c.addEventListener('change',e=>{i.value=fmt(e.detail.dates[0]);p.hidePopover();i.focus();});"
    "i.addEventListener('input',()=>{const d=new Date(i.value);if(!isNaN(d)){c.value=`${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`;}});"
    "i.addEventListener('keydown',e=>{if(e.key==='ArrowDown'){e.preventDefault();p.showPopover();}});")

add(29, "A date picker with natural language input.",
    '<form onsubmit="event.preventDefault()" class="stack" data-gap="2"><div role="group" class="field"><label for="nl">Schedule Date</label>'
    '<div class="popover cal-attach"><div class="input-group"><input id="nl" type="text" value="In 2 days" placeholder="Tomorrow or next week" autocomplete="off">'
    f'<button type="button" class="btn" data-variant="ghost" data-size="icon-xs" data-align="inline-end" popovertarget="nl-pop" aria-label="Select date">{ic("calendar")}</button></div>'
    '<div id="nl-pop" data-popover popover data-side="bottom" data-align="end" class="cal-pop"><auvyx-calendar class="calendar" id="cal"></auvyx-calendar></div></div>'
    '<p id="nl-out" aria-live="polite"></p></div></form>',
    "\n  .cal-attach { display: block; inline-size: 18rem; }\n  .cal-attach > .input-group { anchor-name: --bc-popover; }\n  .cal-pop { padding: 0 !important; inline-size: auto !important; }\n  #nl-out { max-inline-size: 18rem; }",
    TODAY_JS +
    "const DAYS=['sunday','monday','tuesday','wednesday','thursday','friday','saturday'],UNITS={day:1,days:1,week:7,weeks:7};"
    "function parse(s){s=s.trim().toLowerCase();if(!s)return null;if(s==='today'||s==='now')return today;if(s==='tomorrow')return addDays(today,1);if(s==='yesterday')return addDays(today,-1);"
    "let m=s.match(/^in (\\d+|a|an|one|two|three) (day|days|week|weeks|month|months)$/);if(m){const n={a:1,an:1,one:1,two:2,three:3}[m[1]]||+m[1];if(m[2].startsWith('month'))return new Date(today.getFullYear(),today.getMonth()+n,today.getDate());return addDays(today,n*UNITS[m[2]]);}"
    "m=s.match(/^(next )?(sunday|monday|tuesday|wednesday|thursday|friday|saturday)$/);if(m){const t=DAYS.indexOf(m[2]);let diff=(t-today.getDay()+7)%7||7;if(m[1])diff+=diff<7?7:0;return addDays(today,diff);}"
    "if(s==='next week')return addDays(today,7);if(s==='next month')return new Date(today.getFullYear(),today.getMonth()+1,today.getDate());const d=new Date(s);return isNaN(d)?null:d;}"
    "const i=document.getElementById('nl'),c=document.getElementById('cal'),o=document.getElementById('nl-out'),p=document.getElementById('nl-pop');const long=d=>d.toLocaleDateString(undefined,{dateStyle:'full'});"
    "function sync(){const d=parse(i.value);o.innerHTML=d?`Your post will be published on <strong>${long(d)}</strong>.`:'Try “tomorrow”, “in 3 days” or “next friday”.';if(d){c.value=iso(d);c.goTo(d);}}"
    "c.addEventListener('change',e=>{const d=e.detail.dates[0];i.value=d.toLocaleDateString(undefined,{dateStyle:'medium'});o.innerHTML=`Your post will be published on <strong>${long(d)}</strong>.`;p.hidePopover();});"
    "i.addEventListener('input',sync);customElements.whenDefined('auvyx-calendar').then(sync);")

add(30, "A range picker with compact range formatting.",
    '<form class="stack" data-gap="3" onsubmit="event.preventDefault()"><div role="group" class="field"><label for="trip">Trip dates</label>'
    '<auvyx-date-picker class="date-picker" mode="range" id="trip"><input id="trip-from" type="date" name="from" value="2026-06-04"><input type="date" name="to" value="2026-06-10"></auvyx-date-picker>'
    '<p id="trip-out" aria-live="polite"></p></div></form>',
    "\n  .date-picker > button:first-child { inline-size: 16rem; }",
    "const t=document.getElementById('trip'),o=document.getElementById('trip-out');const f=new Intl.DateTimeFormat(undefined,{month:'short',day:'numeric',year:'numeric'});"
    "function upd(){const [a,b]=t.value.split('/');if(a&&b){const n=Math.round((new Date(b)-new Date(a))/86400000);o.textContent=`${f.formatRange(new Date(a+'T00:00'),new Date(b+'T00:00'))} · ${n} night${n===1?'':'s'}`;}}"
    "t.addEventListener('change',upd);customElements.whenDefined('auvyx-date-picker').then(()=>requestAnimationFrame(upd));")

EVENTS = {
    "2026-06-12": [("Team sync", "09:00 – 09:30"), ("Design review", "11:00 – 12:00"), ("Flight to Tokyo", "18:45")],
    "2026-06-13": [("Check-in, Shinjuku", "15:00")],
    "2026-06-15": [("Client workshop", "10:00 – 16:00")],
}
import json
add(31, "Calendar with events for the selected day.",
    f'<div class="card cal-card" data-size="sm"><section>{cal("id=\"cal\" value=\"2026-06-12\" month=\"2026-06\"", box=False)}</section>'
    f'<footer class="cal-foot"><div class="stack" data-gap="2" style="inline-size:100%"><div class="cluster" data-justify="between"><strong id="ev-day" class="cal-evday"></strong>'
    f'<button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Add event">{ic("plus")}</button></div><ul id="ev" class="cal-events"></ul></div></footer></div>',
    """
  .cal-foot { border-block-start: 1px solid var(--border); padding-block-start: 1rem; }
  .cal-evday { font-size: 0.875rem; font-weight: 500; }
  .cal-events { display: flex; flex-direction: column; gap: 0.5rem; margin: 0; padding: 0; list-style: none; inline-size: 100%; }
  .cal-events li { position: relative; border-radius: calc(var(--radius) - 2px); background: var(--muted); padding: 0.5rem 0.75rem 0.5rem 1.25rem; font-size: 0.875rem; }
  .cal-events li::before { content: ''; position: absolute; inset-block: 0.5rem; inset-inline-start: 0.5rem; inline-size: 0.25rem; border-radius: 9999px; background: color-mix(in oklch, var(--primary) 70%, transparent); }
  .cal-events small { display: block; color: var(--muted-foreground); font-size: 0.75rem; }
  .cal-events .cal-none { background: none; padding-inline-start: 0; color: var(--muted-foreground); }
  .cal-events .cal-none::before { display: none; }
""",
    f"const EV={json.dumps(EVENTS)};const c=document.getElementById('cal');"
    "function upd(){const v=c.value;const d=c.dates[0];document.getElementById('ev-day').textContent=d?d.toLocaleDateString(undefined,{day:'numeric',month:'long',year:'numeric'}):'';"
    "const list=EV[v]||[];document.getElementById('ev').innerHTML=list.length?list.map(([t,h])=>`<li>${t}<small>${h}</small></li>`).join(''):'<li class=\"cal-none\">No events.</li>';}"
    "c.addEventListener('change',upd);customElements.whenDefined('auvyx-calendar').then(upd);")

add(32, "A date picker in a drawer, for mobile.",
    '<form class="stack" data-gap="3" onsubmit="event.preventDefault()"><div role="group" class="field"><label for="dob-btn">Date of birth</label>'
    f'<button type="button" class="btn cal-trigger" data-variant="outline" id="dob-btn" commandfor="dob-drawer" command="show-modal">{ic("calendar")}<span id="dob-text">Select date</span></button>'
    '<input type="hidden" name="dob" id="dob"><p>This drawer is meant for small screens; on desktop use a popover.</p></div></form>'
    '<dialog id="dob-drawer" class="drawer" aria-labelledby="dob-title"><article><header class="cal-dhead"><h2 id="dob-title">Select date</h2><p>Set your date of birth</p></header>'
    '<section class="cal-dbody"><auvyx-calendar class="calendar" id="cal" caption="dropdown" min="1930-01-01" max="2026-12-31" month="2000-01"></auvyx-calendar></section></article></dialog>',
    "\n  .cal-trigger { inline-size: 14rem; justify-content: flex-start; font-weight: 400; }\n  .cal-dbody { display: flex; justify-content: center; padding-block-end: 1.5rem; }\n  .cal-dbody .calendar { --cell-size: clamp(2.25rem, 11vw, 2.75rem); }\n  .cal-dhead { text-align: center; }",
    "const c=document.getElementById('cal'),dlg=document.getElementById('dob-drawer');"
    "c.addEventListener('change',e=>{const d=e.detail.dates[0];document.getElementById('dob').value=e.detail.value;document.getElementById('dob-text').textContent=d.toLocaleDateString(undefined,{dateStyle:'long'});dlg.close();});")

register(blocks)
print(f"wrote {len(blocks)} calendar blocks")

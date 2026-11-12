"""chat-01: an AI chat page. History sidebar, a conversation (trace, answer,
sources, message actions) and a Prompt Input with suggestions.

Showcases Message, Bubble, Message Scroller, Trace, Message
Actions, Suggestions and <auvyx-prompt-input>. The page script only fakes a
streamed reply so the composer can be tried; a real app streams its own.
"""
from common import page, register, icon, ic
import sidebar as sb

I = {
    "up": '<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>',
    "stop": '<rect width="12" height="12" x="6" y="6" rx="1"/>',
    "copy": '<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>',
    "retry": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
    "thumb-up": '<path d="M7 10v12"/><path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2a3.13 3.13 0 0 1 3 3.88Z"/>',
    "thumb-down": '<path d="M17 14V2"/><path d="M9 18.12 10 14H4.17a2 2 0 0 1-1.92-2.56l2.33-8A2 2 0 0 1 6.5 2H20a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.76a2 2 0 0 0-1.79 1.11L12 22a3.13 3.13 0 0 1-3-3.88Z"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "chevron": '<path d="m9 18 6-6-6-6"/>',
    "down": '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
    "pen": '<path d="M12 20h9"/><path d="M16.376 3.622a1 1 0 0 1 3.002 3.002L7.368 18.635a2 2 0 0 1-.855.506l-2.872.838a.5.5 0 0 1-.62-.62l.838-2.872a2 2 0 0 1 .506-.854z"/>',
    "share": '<path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" x2="12" y1="2" y2="15"/>',
}


def ci(name):
    return icon(I[name])


HISTORY = [
    ("Today", ["Kestrel renewal plan", "Q4 invoice summary"]),
    ("Yesterday", ["Postgres index for postings", "Draft onboarding email"]),
    ("Previous 7 days", ["Compare two vendor quotes", "Rollback runbook outline", "Translate help article"]),
]


def history():
    out = []
    for label, items in HISTORY:
        links = "".join(
            f'<li><a href="#"{" aria-current=\"page\"" if t == "Kestrel renewal plan" else ""}><span>{t}</span></a></li>' for t in items)
        out.append(f'<div role="group" aria-labelledby="ch-h-{label[:3]}" data-sidebar-hide-collapsed><h3 id="ch-h-{label[:3]}">{label}</h3><ul>{links}</ul></div>')
    return "".join(out)


NAV = (
    f'<header><ul><li><a href="#" data-size="lg">{sb.logo_mark("bot")}<span><strong>Acme Assistant</strong><small>Workspace</small></span></a></li></ul>'
    f'<a href="#" class="btn ch-new" data-variant="outline">{ci("pen")}<span>New chat</span></a></header>'
    f'<section>{history()}</section>'
    f'<footer>{sb.nav_user()}</footer>'
)

TRACE = (
    '<ol class="trace">'
    f'<li data-status="done">{ci("check")}<span>Read 3 contracts</span><small>1.4s</small></li>'
    f'<li data-status="done">{ci("check")}<span>Checked 4 invoices</span><small>0.6s</small></li>'
    f'<li><details><summary data-status="done">{ci("chevron")}<span>Reasoning</span><small>2.1s</small></summary>'
    '<div>The current term ends Dec 1. Usage grew 18% this quarter, so the annual plan with a two-year term at the same price is the strongest offer.</div></details></li>'
    '</ol>'
)

def actions(target, visible=False):
    vis = " data-visible" if visible else ""
    return (f'<div class="message-actions"{vis} role="toolbar" aria-label="Message actions">'
            f'<button type="button" class="btn" data-variant="ghost" data-size="icon-sm" data-copy="#{target}" aria-label="Copy">{ci("copy")}</button>'
            f'<button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Retry">{ci("retry")}</button>'
            f'<label class="toggle" data-size="sm" aria-label="Good response"><input type="checkbox">{ci("thumb-up")}</label>'
            f'<label class="toggle" data-size="sm" aria-label="Bad response"><input type="checkbox">{ci("thumb-down")}</label></div>')


SOURCES = '<ul class="ch-sources" aria-label="Sources">' + "".join(
    f'<li><a href="#"><span>{n}</span>{t}</a></li>' for n, t in ((1, "Kestrel MSA 2025.pdf"), (2, "Invoice INV-2041"), (3, "Usage report · Q4"))) + '</ul>'

conversation = (
    '<article class="message" data-align="end"><section><div class="bubble"><p>Kestrel renews Dec 1. What should we offer them, and can you pull their current plan?</p></div></section></article>'
    '<article class="message ch-reply"><section>'
    f'{TRACE}'
    '<div class="ch-answer" id="ch-a1"><p>Offer the annual plan with a two-year term at today’s price. Their usage grew 18% this quarter and all four invoices were paid on time, so a longer term at a fixed price is the strongest renewal case.</p>'
    '<ul><li>Current plan: Growth, 40 seats, renews Dec 1</li><li>Ask: two-year term, same price per seat</li><li>Risk: procurement wants the security review first</li></ul>'
    '</div>'
    f'{SOURCES}{actions("ch-a1", visible=True)}'
    '</section></article>'
)

SUGGESTIONS = ['Draft the renewal email', 'List the risks', 'Compare with last year']

composer = (
    '<auvyx-prompt-input class="ch-composer">'
    '<div class="suggestions" role="group" aria-label="Suggestions">'
    + "".join(f'<button type="button">{s}</button>' for s in SUGGESTIONS) + '</div>'
    '<form class="prompt-input">'
    '<div class="attachment-group" data-files hidden></div>'
    '<textarea name="prompt" aria-label="Message" placeholder="Ask a follow-up…"></textarea>'
    '<footer>'
    f'<button type="button" class="btn" data-variant="ghost" data-size="icon-sm" data-attach aria-label="Attach files">{ic("plus")}</button>'
    '<input type="file" multiple hidden>'
    '<select class="select" data-size="sm" aria-label="Model"><option>Fast</option><option selected>Thinking</option></select>'
    f'<button type="submit" class="btn" data-size="icon-sm" aria-label="Send">{ci("up")}</button>'
    f'<button type="button" class="btn" data-size="icon-sm" data-stop aria-label="Stop">{ci("stop")}</button>'
    '</footer></form>'
    '<p class="ch-fine">Answers can be wrong. Check sources before you send anything.</p>'
    '</auvyx-prompt-input>'
)

body = (
    sb.sidebar(NAV, attrs=' data-collapsible="icon"')
    + '<main class="ch-main">'
    + f'<header class="app-header ch-header">{sb.toggle_button()}<hr role="separator" aria-orientation="vertical"><h1>Kestrel renewal plan</h1>'
      f'<button type="button" class="btn ch-push" data-variant="ghost" data-size="sm">{ci("share")}Share</button></header>'
    + '<div class="message-scroller ch-scroller"><div role="log" aria-label="Conversation" tabindex="0" aria-live="polite">'
      f'<div class="ch-thread" data-thread>{conversation}<span id="ch-end"></span></div></div>'
      f'<a href="#ch-end" class="btn" data-size="icon" data-variant="outline" aria-label="Jump to latest">{ci("down")}</a></div>'
    + f'<div class="ch-bottom">{composer}</div>'
    + '</main>'
)

CSS = sb.SB_CSS + """
  .ch-main { container-type: inline-size; min-inline-size: 0; display: flex; flex-direction: column; block-size: 100dvh; }
  .ch-header { block-size: 3.25rem; gap: 0.5rem; flex-shrink: 0; }
  .ch-header h1 { margin: 0; font-size: 0.9375rem; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .ch-push { margin-inline-start: auto; }
  .ch-header .btn svg, .ch-new svg { inline-size: 1rem; block-size: 1rem; }
  .ch-new { inline-size: 100%; justify-content: flex-start; gap: 0.5rem; margin-block-start: 0.5rem; }
  .sidebar[data-collapsible="icon"] .ch-new span { white-space: nowrap; }
  .sidebar > nav > section h3 { margin: 0; padding: 0.5rem 0.5rem 0.25rem; font-size: 0.75rem; font-weight: 500; color: var(--muted-foreground); }
  .ch-scroller { flex: 1; min-block-size: 0; }
  .ch-thread { display: flex; flex-direction: column; gap: 1.75rem; inline-size: min(46rem, 100%); margin-inline: auto; padding: 1.5rem 1rem 2rem; }
  .ch-reply > section { gap: 0.75rem; }
  .ch-reply .trace { font-size: 0.8125rem; }
  .ch-answer { display: flex; flex-direction: column; gap: 0.75rem; font-size: 0.9375rem; line-height: 1.65; }
  .ch-answer p, .ch-answer ul { margin: 0; }
  .ch-answer ul { padding-inline-start: 1.25rem; list-style: disc; }
  .ch-sources { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 0.375rem; }
  .ch-sources a { display: inline-flex; align-items: center; gap: 0.375rem; padding: 0.125rem 0.5rem 0.125rem 0.25rem; border-radius: 999px; font-size: 0.75rem; color: var(--muted-foreground); text-decoration: none; background: var(--muted); }
  .ch-sources a:hover { color: var(--foreground); }
  .ch-sources span { display: inline-grid; place-items: center; inline-size: 1.125rem; block-size: 1.125rem; border-radius: 999px; font-size: 0.625rem; font-weight: 600; background: var(--background); color: var(--foreground); }
  .ch-bottom { flex-shrink: 0; padding: 0 1rem 1rem; }
  .ch-composer { inline-size: min(46rem, 100%); margin-inline: auto; display: flex; flex-direction: column; gap: 0.5rem; }
  .ch-composer .select { inline-size: auto; }
  .ch-fine { margin: 0; text-align: center; font-size: 0.75rem; color: var(--muted-foreground); }"""

JS = """<script>
(() => {
  // Demo only: echo the prompt and fake a streamed reply. A real app sends
  // the prompt to its model and streams the answer into the bubble.
  const input = document.querySelector('.ch-composer');
  const thread = document.querySelector('[data-thread]');
  const end = document.getElementById('ch-end');
  if (!input || !thread) return;
  const reply = 'Here is a first pass. I kept it short and put the two-year offer first, then the security review, then a call to book a time this week.';
  let timer = null;
  const el = (html) => { const t = document.createElement('template'); t.innerHTML = html.trim(); return t.content.firstChild; };
  const finish = (bubble) => {
    clearInterval(timer); timer = null;
    bubble.removeAttribute('data-streaming');
    input.streaming = false;
  };
  input.addEventListener('prompt', (e) => {
    const user = el('<article class="message" data-align="end"><section><div class="bubble"><p></p></div></section></article>');
    user.querySelector('p').textContent = e.detail.text || e.detail.files.map((f) => f.name).join(', ');
    thread.insertBefore(user, end);
    const answer = el('<article class="message ch-reply"><section><div class="bubble" data-variant="muted"><span class="typing" role="status" aria-label="Assistant is typing"><i></i><i></i><i></i></span></div></section></article>');
    thread.insertBefore(answer, end);
    input.streaming = true;
    setTimeout(() => {
      const bubble = answer.querySelector('.bubble');
      bubble.innerHTML = '<p></p>';
      bubble.setAttribute('data-streaming', '');
      const p = bubble.firstChild;
      const words = reply.split(' ');
      let i = 0;
      timer = setInterval(() => {
        p.textContent += (i ? ' ' : '') + words[i++];
        if (i >= words.length) finish(bubble);
      }, 60);
      input.addEventListener('stop', () => finish(bubble), { once: true });
    }, 700);
  });
})();
</script>
"""

HEAD = '<script src="../ui/dist/js/prompt-input.min.js" defer></script>\n'

page("chat-01", "Chat 01", body, CSS, scripts=JS, head_extra=HEAD)

if __name__ == "__main__":
    register([{"id": "chat-01", "title": "Chat 01", "description": "An AI chat page: a history sidebar, a conversation with a tool-call trace, an answer with sources and message actions, and a Prompt Input with suggestions that streams a demo reply.", "category": "chat"}])
    print("wrote chat-01")

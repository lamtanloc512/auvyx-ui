"""Collect component docs data for the docs site.

- Upstream Basecoat components: examples from site/src/docs/components/*.mdx
  (the <Preview> blocks), descriptions from shadcn/ui when a local checkout is
  available (SHADCN_DOCS env var), else the first prose line of the mdx.
- Fork components: demos lifted from packages/ui/preview.html (already
  covered by the Playwright suites) plus a few hand-written examples.
Writes packages/docs/src/data/components.json.
"""
import json, os, re, pathlib, textwrap
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parents[3]
MDX = ROOT / "site/src/docs/components"
PREVIEW = ROOT / "packages/ui/preview.html"
OUT = ROOT / "packages/docs/src/data/components.json"
SHADCN = pathlib.Path(os.environ.get("SHADCN_DOCS", "/nonexistent"))

SKIP_EXAMPLES = {"RTL"}
SKIP_COMPONENTS = {"chart", "theme-switcher"}  # chart has its own page


def dedent(html):
    html = html.strip("\n")
    return textwrap.dedent(html).strip()


def shadcn_desc(slug):
    f = SHADCN / f"{slug}.mdx"
    if f.exists():
        m = re.search(r"^description:\s*(.+)$", f.read_text(), re.M)
        if m:
            return m.group(1).strip()
    return None


def upstream():
    out = {}
    for f in sorted(MDX.glob("*.mdx")):
        slug = f.stem
        if slug in SKIP_COMPONENTS:
            continue
        src = f.read_text()
        title = re.search(r"^# (.+)$", src, re.M).group(1).strip()
        examples = []
        # Walk headings and previews in order.
        heading = "Default"
        for m in re.finditer(r"^(#{2,3}) ([^\n]+)$|<Preview[^>]*>(.*?)</Preview>", src, re.M | re.S):
            if m.group(1):
                heading = m.group(2).strip()
                continue
            if heading in SKIP_EXAMPLES:
                continue
            html = dedent(m.group(3))
            if "{" in html and re.search(r"\{[a-zA-Z_]", html):
                continue  # JSX expressions, not plain HTML
            examples.append({"title": heading if examples else "Default", "html": html})
        desc = shadcn_desc(slug)
        if not desc:
            para = re.search(r"^(?!#|<|`|\s|import|\|)(.+)$", src.split("\n## Usage")[0].split("\n", 1)[-1], re.M)
            desc = para.group(1).strip() if para else ""
        out[slug] = {"title": title, "description": desc, "examples": examples[:8], "source": "basecoat"}
    return out


from bs4.formatter import HTMLFormatter


class _Keep(HTMLFormatter):
    """Keep source attribute order (bs4 sorts by default) and boolean attributes bare."""
    def attributes(self, tag):
        return list(tag.attrs.items())


KEEP = _Keep(empty_attributes_are_booleans=True, void_element_close_prefix="")

SVG_ATTRS = {"viewbox": "viewBox", "preserveaspectratio": "preserveAspectRatio", "gradientunits": "gradientUnits", "gradienttransform": "gradientTransform"}


def prettify(data):
    """Format every example with Prettier (tools/format-html.mjs), icons kept on one line."""
    import subprocess, tempfile
    items = [ex["html"] for v in data.values() for ex in v["examples"]]
    with tempfile.TemporaryDirectory() as tmp:
        src, dst = pathlib.Path(tmp, "in.json"), pathlib.Path(tmp, "out.json")
        src.write_text(json.dumps(items))
        subprocess.run(["node", str(ROOT / "packages/docs/tools/format-html.mjs"), "--json", str(src), str(dst)], check=True)
        out = iter(json.loads(dst.read_text()))
    for v in data.values():
        for ex in v["examples"]:
            ex["html"] = next(out)


def preview_demos():
    """Map h3 title -> inner HTML of each .pv-spec article in preview.html."""
    soup = BeautifulSoup(PREVIEW.read_text(), "html.parser")
    demos = {}
    for art in soup.select("article.pv-spec"):
        h = art.select_one(".pv-spec-top h3")
        if not h:
            continue
        title = h.get_text(strip=True)
        for el in art.select(":scope > .pv-spec-top, :scope > .pv-note"):
            el.decompose()
        html = "".join(c.decode(formatter=KEEP) if hasattr(c, "decode") else str(c) for c in art.children if str(c).strip())
        # html.parser lowercases attribute names; restore the SVG ones that are case-sensitive in source.
        for low, real in SVG_ATTRS.items():
            html = html.replace(f' {low}="', f' {real}="')
        demos[title] = to_en(dedent(html))
    return demos


ICON = lambda d: f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'
CHECK = ICON('<path d="M20 6 9 17l-5-5"/>')
LOADER = ICON('<path d="M21 12a9 9 0 1 1-6.219-8.56"/>')
CHEV = ICON('<path d="m9 18 6-6-6-6"/>')
FILE = ICON('<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/>')
COPY = ICON('<rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>')
DOWN = ICON('<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>')
X = ICON('<path d="M18 6 6 18"/><path d="m6 6 12 12"/>')

# preview.html demos are in Vietnamese (flowsus content); the docs site is English.
VI_EN = {
    "120 quốc gia, phù hợp chuyến đi dài.": "120 countries, good for long trips.",
    "2 gói eSIM đang chờ thanh toán.": "2 eSIM plans waiting for checkout.",
    "Bật chuyển vùng dữ liệu khi đến nơi.": "Turn on data roaming when you land.",
    "Chọn dung lượng cho chuyến đi.": "Choose the data for your trip.",
    "Có, nếu gói chưa được cài đặt.": "Yes, if the plan has not been installed.",
    "Gói doanh nghiệp (sắp có)": "Business plans (coming soon)",
    "Hướng dẫn cho iPhone và Android.": "Guides for iPhone and Android.",
    "Khi máy kết nối mạng ở nước đến lần đầu tiên.": "When your phone first connects to a network at your destination.",
    "Kiểm tra máy của bạn có hỗ trợ eSIM.": "Check whether your phone supports eSIM.",
    "Một gói cho 39 nước khối Schengen.": "One plan for 39 Schengen countries.",
    "Nhấn chuột phải (hoặc Shift+F10) vào vùng này": "Right-click (or Shift+F10) here",
    "Nhật, Hàn, Thái, Singapore và 20 nước khác.": "Japan, Korea, Thailand, Singapore and 20 more.",
    "Quản lý nhiều eSIM cho cả đội.": "Manage eSIMs for your whole team.",
    "Thay đổi sẽ lưu khi bạn bấm Lưu.": "Make changes and click Save when you're done.",
    "Đã chọn {selected} / {total} gói": "{selected} of {total} plans selected",
    "Trang {page} / {pages}": "Page {page} of {pages}",
    "Lọc theo nước, vùng…": "Filter by country or region…",
    "Hướng dẫn cài eSIM": "Installing your eSIM",
    "Quét mã QR trong email.": "Scan the QR code in the email.",
    "Mất khoảng 2 phút.": "Takes about 2 minutes.",
    "Thanh toán $23.40": "Checkout $23.40",
    "Nhật Bản · 10 GB": "Japan · 10 GB", "Hàn Quốc · 5 GB": "Korea · 5 GB",
    "eSIM kích hoạt khi nào?": "When does the eSIM activate?",
    "Có hoàn tiền không?": "Can I get a refund?",
    "Đổi kích thước chi tiết": "Resize details", "Đổi kích thước danh sách": "Resize list",
    "Danh sách đơn hàng": "Orders", "Chi tiết đơn": "Order details", "Nhật ký kích hoạt": "Activation log",
    "Thiết bị tương thích": "Compatible devices", "Điều hướng chính": "Main navigation",
    "Kích thước eSIM": "Data plan", "Dung lượng (GB)": "Data (GB)", "Gói dữ liệu": "Data plan",
    "Sao chép mã QR": "Copy QR code", "Gửi qua email": "Send by email", "Xoá eSIM": "Delete eSIM",
    "Chat với hỗ trợ": "Chat with support", "Cách cài eSIM": "How to install", "Tự chuyển vùng": "Auto roaming",
    "Mua gói mới": "Buy a plan", "Quản lý eSIM": "eSIM manager", "Thời hạn gói": "Plan length",
    "Mở giỏ hàng": "Open cart", "Tiếp tục mua": "Keep shopping", "Sheet từ bên trái.": "A sheet from the left.",
    "Không có gói phù hợp.": "No matching plans.", "Chọn tất cả": "Select all", "Lọc gói": "Filter plans",
    "Châu Đại Dương": "Oceania", "Bắc Mỹ": "North America", "Châu Âu": "Europe", "Châu Á": "Asia",
    "Chọn Nhật Bản": "Select Japan", "Chọn Hàn Quốc": "Select Korea", "Chọn Thái Lan": "Select Thailand",
    "Chọn Pháp": "Select France", "Chọn Mỹ": "Select USA", "Chọn Úc": "Select Australia",
    "Chọn Singapore": "Select Singapore", "Chọn Đức": "Select Germany",
    "Nhật Bản": "Japan", "Hàn Quốc": "Korea", "Thái Lan": "Thailand",
    "Gói eSIM": "eSIM plans", "Bảng giá": "Pricing", "Toàn cầu": "Global", "Doanh nghiệp": "Business",
    "Từ $2.90": "From $2.90", "Từ $3.90": "From $3.90", "Từ $4.50": "From $4.50", "Điểm đến": "Destinations",
    "Sửa hồ sơ": "Edit profile", "Tài khoản": "Account", "Thiết bị": "Device", "Trợ giúp": "Help",
    "Đăng xuất": "Log out", "Thanh toán": "Billing", "Hồ sơ": "Profile", "Gia hạn": "Renew", "Lịch sử": "History",
    "Giỏ hàng": "Cart", "Đơn hàng": "Orders", "Hỗ trợ": "Support", "Cài đặt": "Settings", "Thao tác": "Actions",
    "Ngày bay": "Departure", "Chọn ngày": "Pick a date", "Gửi form": "Submit", "Mã xác minh": "Verification code",
    "Thời hạn": "Length", "Dung lượng": "Data", "Nước": "Country", "Vùng": "Region", "Giá": "Price", "Cột": "Columns",
    "15 ngày": "15 days", "30 ngày": "30 days", "7 ngày": "7 days", "5 ngày": "5 days",
    "Pháp": "France", "Mỹ": "USA", "Úc": "Australia", "Đức": "Germany", "Nhật": "Japan", "Hàn": "Korea", "Thái": "Thailand",
    "Gửi: ": "Sent: ", "Mở <code>": "Open <code>", "Chưa mở.": "Not open yet.", "Từ trái": "From left", "Huỷ": "Cancel", "Lưu": "Save", "Tên": "Name", "Đóng": "Close",
    "Trước": "Previous", ">Sau<": ">Next<", "Gói": "Plans", ">Mở<": ">Open<", "→ Di động.": "→ Mobile data.",
}


def to_en(html):
    for vi in sorted(VI_EN, key=len, reverse=True):
        html = html.replace(vi, VI_EN[vi])
    return html


HAND = {
    "message": [("Default", f"""<div class="stack" data-gap="4" style="inline-size: min(28rem, 100%)">
  <article class="message">
    <span class="avatar"><span>AI</span></span>
    <section>
      <header>Assistant</header>
      <div class="bubble" data-variant="muted"><p>Your eSIM is active. You have 8.2 GB left.</p></div>
    </section>
  </article>
  <article class="message" data-align="end">
    <span class="avatar"><span>E</span></span>
    <section>
      <div class="bubble"><p>Great, thanks! Can I top up later?</p></div>
      <footer>Read 9:41</footer>
    </section>
  </article>
</div>""")],
    "bubble": [("Variants", """<div class="stack" data-gap="2" style="inline-size: min(26rem, 100%)">
  <div class="bubble"><p>Default bubble</p></div>
  <div class="bubble" data-variant="secondary"><p>Secondary</p></div>
  <div class="bubble" data-variant="muted"><p>Muted</p></div>
  <div class="bubble" data-variant="tinted"><p>Tinted from --primary</p></div>
  <div class="bubble" data-variant="outline"><p>Outline</p></div>
  <div class="bubble" data-variant="destructive"><p>Message failed to send.</p></div>
  <div class="bubble" data-align="end"><p>Aligned to the end</p><aside>👍 2</aside></div>
</div>""")],
    "marker": [("Default", f"""<div class="stack" data-gap="4" style="inline-size: min(26rem, 100%)">
  <p class="marker">{ICON('<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>')}<span>Assistant is typing…</span></p>
  <p class="marker" data-variant="separator"><span>Today</span></p>
  <p class="marker" data-variant="border"><span>Earlier messages</span></p>
</div>""")],
    "message-scroller": [("Default", f"""<div class="message-scroller" style="block-size: 18rem; inline-size: min(26rem, 100%); border: 1px solid var(--border); border-radius: var(--radius)">
  <div role="log" aria-label="Conversation" tabindex="0">
    <div>
""" + "\n".join(f'      <article class="message"{" data-align=\"end\"" if i % 2 else ""}><section><div class="bubble"{"" if i % 2 else " data-variant=\"muted\""}><p>Message {i + 1}</p></div></section></article>' for i in range(10)) + f"""
      <article class="message" id="ms-latest"><section><div class="bubble" data-variant="muted"><p>Newest message</p></div></section></article>
    </div>
  </div>
  <a href="#ms-latest" class="btn" data-size="icon" aria-label="Jump to latest">{DOWN}</a>
</div>""")],
    "trace": [("Default", f"""<ol class="trace" style="inline-size: min(26rem, 100%)">
  <li data-status="done">{CHECK}<span>Searched 3 sources</span><small>1.2s</small></li>
  <li>
    <details>
      <summary data-status="done">{CHEV}<span>Compared plans</span><small>0.8s</small></summary>
      <div>Japan 10 GB is the best price per GB for a 10 day trip.</div>
    </details>
  </li>
  <li data-status="running">{LOADER}<span>Checking coverage</span></li>
  <li data-status="pending">{LOADER}<span>Drafting answer</span></li>
  <li data-status="error">{X}<span>Payment check failed</span></li>
</ol>""")],
    "attachment": [("States", f"""<div class="attachment-group">
  <div class="attachment" data-state="done"><figure>{FILE}</figure><div><strong>passport.pdf</strong><small>1.2 MB</small></div><div data-actions><button type="button" class="btn" data-variant="ghost" data-size="icon-sm" aria-label="Remove">{X}</button></div></div>
  <div class="attachment" data-state="uploading"><figure>{FILE}</figure><div><strong>ticket.pdf</strong><small>Uploading… 64%</small></div></div>
  <div class="attachment" data-state="error"><figure>{FILE}</figure><div><strong>visa.heic</strong><small>Unsupported format</small></div></div>
  <div class="attachment" data-state="idle"><figure>{FILE}</figure><div><strong>Drop a file</strong><small>PDF or JPG, up to 10 MB</small></div></div>
</div>""")],
    "code-block": [("Default", f"""<figure class="code-block" style="inline-size: min(32rem, 100%)">
  <figcaption><span>index.html</span><button type="button" class="btn" data-variant="ghost" data-size="icon-sm" data-copy aria-label="Copy">{COPY}{CHECK}</button></figcaption>
  <pre tabindex="0" data-numbered><code><span>&lt;link rel="stylesheet" href="auvyx.min.css"&gt;</span>
<span data-line="removed">&lt;script src="all.min.js"&gt;&lt;/script&gt;</span>
<span data-line="added">&lt;script src="auvyx.min.js" defer&gt;&lt;/script&gt;</span>
<span data-line="highlighted">&lt;html data-theme="ocean"&gt;</span></code></pre>
</figure>""")],
    "questionnaire": [("Default", """<form class="questionnaire" style="inline-size: min(26rem, 100%)" onsubmit="event.preventDefault()">
  <output>Question 1 of 3</output>
  <fieldset>
    <legend>How much data do you use?</legend>
    <p>We size the plan from this.</p>
    <label><input class="input" type="radio" name="q-usage" value="light" required><span>Light<small>Maps and messaging</small></span><kbd>1</kbd></label>
    <label><input class="input" type="radio" name="q-usage" value="medium" checked><span>Medium<small>Social and photos</small></span><kbd>2</kbd></label>
    <label><input class="input" type="radio" name="q-usage" value="heavy"><span>Heavy<small>Video and hotspot</small></span><kbd>3</kbd></label>
  </fieldset>
  <footer><button class="btn">Continue</button><button type="button" class="btn" data-variant="ghost">Skip</button></footer>
</form>""")],
    "hover-card": [("Default", """<p style="font-size:.875rem">Hover or focus the link:
  <span class="hover-card">
    <a href="#">@auvyx</a>
    <span data-popover data-side="bottom">
      <strong>Auvyx UI</strong>
      <span style="color:var(--muted-foreground)">The shadcn look as one CSS file. Zero-JS by default.</span>
    </span>
  </span>
</p>""")],
    "sidebar": [("In-flow (static)", """<div style="block-size: 22rem; border: 1px solid var(--border); border-radius: var(--radius); overflow: hidden; display: flex">
  <aside class="sidebar" data-position="static">
    <nav aria-label="Demo sidebar">
      <section>
        <div role="group" aria-labelledby="sbd-1">
          <h3 id="sbd-1">Platform</h3>
          <ul>
            <li><a href="#" aria-current="page">""" + ICON('<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>') + """<span>Home</span></a></li>
            <li><a href="#">""" + ICON('<polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>') + """<span>Inbox</span><span data-badge>12</span></a></li>
            <li><details open><summary>""" + FILE + """<span>Documents</span></summary><ul><li><a href="#"><span>Drafts</span></a></li><li><a href="#"><span>Shared</span></a></li></ul></details></li>
          </ul>
        </div>
      </section>
    </nav>
  </aside>
  <div style="flex: 1; padding: 1rem; font-size: .875rem; color: var(--muted-foreground)">Page content. See Blocks → Sidebar for full app layouts (icon rail, floating, inset).</div>
</div>""")],
    "range-calendar": [("Default", '<auvyx-calendar class="calendar" mode="range" months="2" value="2026-06-12/2026-06-20" style="border:1px solid var(--border);border-radius:var(--radius)"></auvyx-calendar>'),
                       ("Minimum stay", '<auvyx-calendar class="calendar" mode="range" min-days="3" max-days="14" disabled-days="0" value="2026-06-08/2026-06-12" style="border:1px solid var(--border);border-radius:var(--radius)"></auvyx-calendar>')],
}

NATIVE = {  # zero-JS variants shown first on upstream pages
    "popover": "Popover", "dropdown-menu": "Dropdown menu", "dialog": "Dialog", "accordion": "Accordion",
}

EXTRA_META = {
    "aspect-ratio": ("Aspect Ratio", "Displays content within a desired ratio.", "Aspect Ratio"),
    "toggle": ("Toggle", "A two-state button that can be either on or off.", "Toggle"),
    "toggle-group": ("Toggle Group", "A set of two-state buttons that can be toggled on or off.", "Toggle Group"),
    "sheet": ("Sheet", "Extends the Dialog component to display content that complements the main content of the screen.", "Sheet"),
    "hover-card": ("Hover Card", "For sighted users to preview content available behind a link.", None),
    "input-otp": ("Input OTP", "Accessible one-time password component, a single native input drawn as slots.", "Input OTP"),
    "carousel": ("Carousel", "A carousel built on CSS scroll snap, with native scroll buttons and markers.", "Carousel"),
    "typography": ("Typography", "Styles for headings, paragraphs, lists and other long-form content.", "Typography"),
    "menubar": ("Menubar", "A visually persistent menu common in desktop applications.", "Menubar"),
    "navigation-menu": ("Navigation Menu", "A collection of links for navigating websites.", "Navigation Menu"),
    "context-menu": ("Context Menu", "Displays a menu at the pointer, triggered by right click or Shift+F10.", "Context Menu"),
    "resizable": ("Resizable", "Accessible resizable panel groups and layouts with keyboard support.", "Resizable"),
    "data-table": ("Data Table", "Sorting, filtering, selection and pagination over a server-rendered table.", "Data Table"),
    "calendar": ("Calendar", "A date field component that allows users to enter and edit date.", "Calendar"),
    "date-picker": ("Date Picker", "A date picker that enhances the native date input.", "Date Picker"),
    "message": ("Message", "Displays a message in a conversation, with optional avatar, header, footer, and alignment.", None),
    "bubble": ("Bubble", "The surface of a chat message, in several variants.", None),
    "marker": ("Marker", "An inline status line or labelled separator inside a conversation.", None),
    "message-scroller": ("Message Scroller", "A conversation scroller that stays pinned to the newest message, without JavaScript.", None),
    "trace": ("Trace", "The building block for reasoning, tool calls, sources and more.", None),
    "attachment": ("Attachment", "A file attached to a message, with upload states.", None),
    "code-block": ("Code Block", "Displays code with an optional caption, line numbers, diff lines and a copy button.", None),
    "questionnaire": ("Questionnaire", "A question with choices, for agents asking the user to pick.", None),
    "range-calendar": ("Range Calendar", "A calendar for selecting a range of dates.", None),
}


def main():
    data = upstream()
    demos = preview_demos()
    for slug, (title, desc, demo_title) in EXTRA_META.items():
        examples = []
        if demo_title and demo_title in demos:
            examples.append({"title": "Default", "html": demos[demo_title]})
        for t, html in HAND.get(slug, []):
            examples.append({"title": t if examples or t != "Default" else "Default", "html": html})
        data[slug] = {"title": title, "description": shadcn_desc(slug) or desc, "examples": examples, "source": "auvyx"}
    for slug, items in HAND.items():
        if slug not in EXTRA_META and slug in data:
            data[slug]["examples"] = [{"title": t, "html": h} for t, h in items] + data[slug]["examples"]
    for slug, demo_title in NATIVE.items():
        if slug in data and demo_title in demos:
            data[slug]["examples"].insert(0, {"title": "Zero JS (native)", "html": demos[demo_title]})
            data[slug]["native"] = True
    prettify(data)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(dict(sorted(data.items())), ensure_ascii=False, indent=1))
    n = sum(len(v["examples"]) for v in data.values())
    print(f"{len(data)} components, {n} examples -> {OUT.relative_to(ROOT)}")
    missing = [k for k, v in data.items() if not v["examples"]]
    if missing:
        print("no examples:", missing)


main()

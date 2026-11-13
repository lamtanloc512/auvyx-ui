"""auvyx.ai.json: component contracts for agents that write Auvyx markup.

Built by packages/docs/build.py next to llms.txt, from the same sources as the
docs, so it cannot drift from them:
  - components.json + notes: title, description, examples
  - dist/ui/src/<component>.css (the CLI split): the classes a component owns
  - dist/custom-elements.json: custom element attributes, properties, events
  - dist/js/manifest.json: which script a component needs

Per component it gives the root class and element, the other classes it owns,
the data-* and aria-* attributes its examples use (with observed values), the
direct children of the root, its script and element, and one canonical
snippet. Top level: the design rules, the theme tokens and intent groups, so a
caller can classify a request and send only the relevant contracts.
"""
import json
import re
from html.parser import HTMLParser

# Intent groups for routing: classify the request, then include only these
# components' contracts in the prompt. Every component must be in one group
# (packages/tests/ai-contract.test.mjs checks it).
GROUPS = {
    "action": ["button", "button-group", "toggle", "toggle-group", "kbd"],
    "form": ["field", "label", "input", "input-group", "input-otp", "textarea", "checkbox", "radio-group", "switch", "slider",
             "select", "native-select", "combobox", "calendar", "range-calendar", "date-picker", "questionnaire"],
    "overlay": ["dialog", "alert-dialog", "sheet", "drawer", "popover", "hover-card", "tooltip", "dropdown-menu", "context-menu", "command", "toast"],
    "navigation": ["tabs", "breadcrumb", "pagination", "menubar", "navigation-menu", "flyout-menu", "sidebar"],
    "data": ["table", "data-table", "kanban", "properties", "item", "tile", "carousel", "aspect-ratio", "avatar", "badge"],
    "feedback": ["alert", "empty", "progress", "skeleton", "spinner", "separator"],
    "content": ["card", "accordion", "typography", "code-block", "scroll-area", "resizable"],
    "chat": ["message", "bubble", "marker", "message-scroller", "prompt-input", "suggestions", "message-actions", "attachment", "trace"],
}

RULES = [
    "Load auvyx.min.css (or one style pack from styles/) and, for behavior, auvyx.min.js. Components marked js.bundled=false need their own script.",
    "Write semantic HTML: one root class per component (contract.root), native elements for controls, and the child elements the contract lists.",
    "Native button, input, select, textarea, details and dialog are already styled by the root class: do not restyle them or add inline colors.",
    "Variants and sizes are data attributes (data-variant, data-size, data-align, data-side). Use only the values in contract.attributes.",
    "ARIA describes behavior and state (aria-expanded, aria-selected, aria-current, aria-label on icon-only buttons), never styling.",
    "Colors come from theme tokens: var(--primary), var(--muted-foreground), var(--border) and the rest of tokens.colors. Never hard-code a color the theme already has.",
    "Radius, shadow, font and spacing follow --radius, --shadow-*, --font-sans and --spacing; corner shapes follow --corner-shape.",
    "Layout with the primitives: .stack (vertical, data-gap), .cluster (wrapping row, data-gap), .wrapper (centered page width, data-size), .auto-grid (responsive grid, data-min).",
    "Icons are inline SVG (Lucide, 24x24 viewBox, stroke currentColor) with aria-hidden=\"true\"; icon-only buttons need aria-label.",
    "Popovers and menus use the native popover attribute: a trigger with popovertarget and a [data-popover] element with popover. Dialogs are <dialog class=\"dialog\"> opened with commandfor/command.",
    "Use logical properties and utilities (ms/me/ps/pe, start/end) so RTL works.",
    "Stateful elements (auvyx-data-table, auvyx-tabs, auvyx-select, ...) expose properties and events (contract.element). Read and set their state there instead of re-rendering markup.",
    "Render HTML an agent wrote in a sandboxed iframe unless it was checked against these contracts.",
]

COLOR_TOKENS = ["background", "foreground", "card", "card-foreground", "popover", "popover-foreground", "primary", "primary-foreground",
                "secondary", "secondary-foreground", "muted", "muted-foreground", "accent", "accent-foreground", "destructive",
                "border", "input", "ring", "chart-1", "chart-2", "chart-3", "chart-4", "chart-5",
                "sidebar", "sidebar-foreground", "sidebar-primary", "sidebar-primary-foreground", "sidebar-accent",
                "sidebar-accent-foreground", "sidebar-border", "sidebar-ring"]
OTHER_TOKENS = ["radius", "font-sans", "font-serif", "font-mono", "font-heading", "spacing", "tracking-normal", "corner-shape",
                "shadow-2xs", "shadow-xs", "shadow-sm", "shadow-md", "shadow-lg", "shadow-xl"]

MAX_VALUES = 16

# Components whose API is not one root class: an attribute, a native element, a
# composition of other components, or a mode of another element.
OVERRIDES = {
    "alert-dialog": {"css": "dialog", "root": {"class": "alert-dialog", "tags": ["dialog"], "selector": "dialog.alert-dialog"}},
    "pagination": {"composedOf": ["button"],
                   "pattern": "A nav.pagination with a list of .btn links (data-variant=\"ghost\"); the current page has aria-current=\"page\" and data-variant=\"outline\"."},
    "range-calendar": {"element": "calendar", "root": {"class": "calendar", "tags": ["auvyx-calendar"], "selector": "auvyx-calendar[mode=range]"},
                       "pattern": "<auvyx-calendar mode=\"range\"> with value=\"start/end\" (ISO dates)."},
    "separator": {"root": {"class": None, "tags": ["hr"], "selector": "hr"}, "pattern": "A native <hr>; add role=\"separator\" and aria-orientation=\"vertical\" for a vertical one."},
    "spinner": {"pattern": "An inline loader SVG (or an empty span, drawn as a ring) with class=\"spinner\", role=\"status\" and aria-label=\"Loading\"."},
    "toast": {"root": {"class": "toaster", "tags": ["div"], "selector": ".toaster"},
              "snippet": '<div id="toaster" class="toaster"></div>\n<button type="button" class="btn" data-variant="outline" onclick="document.getElementById(\'toaster\').toast({ category: \'success\', title: \'Saved\', description: \'Your changes are live.\' })">Save</button>',
              "pattern": "One <div id=\"toaster\" class=\"toaster\"> per page; show a toast with document.getElementById('toaster').toast({ category, title, description })."},
    "switch": {"root": {"class": "input", "tags": ["input"], "selector": "input.input[type=checkbox][role=switch]"}},
    "tooltip": {"root": {"class": None, "tags": [], "selector": "[data-tooltip]"}, "attributes": {"data-tooltip": [], "data-side": ["top", "right", "bottom", "left"], "data-align": ["start", "center", "end"]},
                "pattern": "Add data-tooltip=\"Text\" to any element; data-side and data-align place it."},
}


class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.children, self.parent = tag, attrs, [], parent

    @property
    def classes(self):
        return (self.attrs.get("class") or "").split()

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Tree(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {}, None)
        self.cur = self.root
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        n = Node(tag, {k: (v if v is not None else "") for k, v in attrs}, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, {k: (v if v is not None else "") for k, v in attrs}, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent


def owned_classes(css):
    """Class names a component's CSS defines (selectors only, not @apply)."""
    out = set()
    for m in re.finditer(r"([^{};]+)\{", re.sub(r"/\*.*?\*/", "", css, flags=re.S)):
        sel = m.group(1).strip()
        if sel.startswith("@") or ":" == sel[:1]:
            continue
        out.update(re.findall(r"\.([a-z][\w-]*)", sel))
    return out


def describe_child(n, owned):
    cls = [c for c in n.classes if c in owned]
    data = sorted(k for k in n.attrs if k.startswith(("data-", "role", "aria-")) and k not in ("aria-hidden",))
    s = n.tag + "".join(f".{c}" for c in cls)
    return s + (f"[{' '.join(data)}]" if data else "")


def contract(key, comp, css, element, js, site, other_roots=frozenset()):
    owned = owned_classes(css) if css else set()
    trees = [Tree(ex["html"]) for ex in comp["examples"]]
    roots = []
    for t in trees:
        for n in t.root.walk():
            if n is t.root or n.tag == "svg":
                continue
            if element and n.tag == element["tagName"]:
                roots.append(n)
            elif any(c in owned for c in n.classes) and not any(c in owned for p in ancestors(n) for c in p.classes):
                roots.append(n)
    # The root class: the class named like the component, else the owned class the
    # component's elements carry most, skipping another component's root (a
    # checkbox example sits in a .field).
    counts = {}
    for t in trees:
        for n in t.root.walk():
            for c in n.classes:
                if c in owned:
                    counts[c] = counts.get(c, 0) + 1
    if key in counts:
        root_class = key
    else:
        cands = {c: v for c, v in counts.items() if c not in other_roots} or counts
        root_class = max(cands, key=lambda c: (cands[c], -len(c))) if cands else None
    if root_class:
        roots = [n for t in trees for n in t.root.walk() if root_class in n.classes or (element and n.tag == element["tagName"])]
    root_tags = sorted({n.tag for n in roots if root_class in n.classes}) if root_class else []

    attrs, aria, used = {}, set(), set()
    for n in roots:
        for d in n.walk():
            if d.tag in ("svg", "path", "circle", "rect", "line", "polyline", "polygon", "g"):
                continue
            used.update(c for c in d.classes if c in owned)
            for k, v in d.attrs.items():
                if k.startswith("data-"):
                    vals = attrs.setdefault(k, set())
                    if v and len(v) <= 40 and " " not in v.strip():
                        vals.add(v)
                elif k.startswith("aria-") and k != "aria-hidden":
                    aria.add(k)
    first = next((n for n in roots if root_class and root_class in n.classes), roots[0] if roots else None)
    children = []
    if first is not None:
        for c in first.children:
            d = describe_child(c, owned)
            if d not in children:
                children.append(d)

    out = {
        "name": key,
        "title": comp["title"],
        "description": comp["description"],
        "group": next((g for g, ks in GROUPS.items() if key in ks), None),
        "root": {"class": root_class, "tags": root_tags, "selector": selector(root_class, roots)} if root_class else None,
        "classes": sorted(used - {root_class}),
        "attributes": {k: sorted(v)[:MAX_VALUES] for k, v in sorted(attrs.items())},
        "aria": sorted(aria),
        "children": children,
        "install": f"npx @auvyx/cli add {key}",
        "docs": f"{site}/md/components/{key}.md",
        "examples": [ex["title"] for ex in comp["examples"]],
        "snippet": comp["examples"][0]["html"].strip() if comp["examples"] else "",
    }
    if js:
        out["js"] = {k: js[k] for k in ("file", "kind", "bundled", "note") if k in js}
    if element:
        out["element"] = {
            "tag": element["tagName"],
            "module": element.get("module"),
            "attributes": [{"name": a["name"], "type": a.get("type", {}).get("text"), "description": a.get("description")} for a in element.get("attributes", [])],
            "properties": [{"name": m["name"], "type": m.get("type", {}).get("text"), "readonly": m.get("readonly", False), "description": m.get("description")}
                           for m in element.get("members", []) if m.get("kind") == "field"],
            "methods": [{"name": m["name"], "description": m.get("description")} for m in element.get("members", []) if m.get("kind") == "method"],
            "events": [{"name": e["name"], "type": e.get("type", {}).get("text"), "description": e.get("description")} for e in element.get("events", [])],
        }
    return out


def selector(root_class, roots):
    """A CSS selector for the root: .class, plus [type] for typed inputs."""
    types = sorted({n.attrs["type"] for n in roots if root_class in n.classes and n.tag == "input" and "type" in n.attrs})
    sel = f".{root_class}"
    if len(types) == 1 and types[0] not in ("text",):
        sel = f"input{sel}[type={types[0]}]"
    return sel


def ancestors(n):
    p = n.parent
    while p is not None and p.tag != "#root":
        yield p
        p = p.parent


def elements_by_key(manifest):
    out = {}
    for mod in manifest.get("modules", []):
        for d in mod.get("declarations", []):
            tag = d.get("tagName")
            if tag and tag.startswith("auvyx-"):
                out[tag[len("auvyx-"):]] = {**d, "module": mod.get("path")}
    return out


def build(comps, ui_dist, version, cdn, site):
    manifest = json.loads((ui_dist / "custom-elements.json").read_text())
    elements = elements_by_key(manifest)
    js = json.loads((ui_dist / "js/manifest.json").read_text())
    def css_for(key):
        f = ui_dist / "ui/src" / f"{OVERRIDES.get(key, {}).get('css', key)}.css"
        return f.read_text() if f.exists() else ""

    def element_for(key):
        return elements.get(OVERRIDES.get(key, {}).get("element", key))

    # Pass 1 finds each component's own root; pass 2 skips other components' roots.
    first = {k: contract(k, c, css_for(k), element_for(k), js.get(k), site) for k, c in comps.items()}
    other = {k: frozenset(r["root"]["class"] for j, r in first.items() if j != k and r["root"] and r["root"]["class"] == j) for k in comps}
    items = []
    for key, comp in comps.items():
        item = contract(key, comp, css_for(key), element_for(key), js.get(key), site, other[key])
        o = OVERRIDES.get(key, {})
        for f in ("root", "composedOf", "pattern", "attributes", "snippet"):
            if f in o:
                item[f] = o[f]
        items.append(item)
    return {
        "name": "Auvyx UI",
        "version": version,
        "about": "Component contracts for agents that write Auvyx markup: plain HTML with one root class per component, optional JS and custom elements. Route a request to a group, then send only that group's contracts.",
        "load": {
            "css": f"{cdn}/auvyx.min.css",
            "js": f"{cdn}/auvyx.min.js",
            "styles": f"{cdn}/styles/auvyx-<style>.min.css",
            "styleNames": ["vega", "nova", "maia", "lyra", "mira", "luma", "sera", "rhea"],
        },
        "rules": RULES,
        "tokens": {"colors": COLOR_TOKENS, "other": OTHER_TOKENS},
        "groups": GROUPS,
        "components": items,
    }

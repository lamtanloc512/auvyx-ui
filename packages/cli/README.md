# @auvyx/cli

Copy Auvyx UI blocks into your project, shadcn-style: you own the code after `add`.

```bash
npx @auvyx/cli init --icons tabler
```

`init` points `@auvyx` at `https://auvyx-ui.vercel.app/r/{framework}/{icons}/{name}.json`; pass `--registry` to use another one. `--icons` picks the icon library the blocks are delivered with: `lucide` (default), `tabler`, `hugeicons`, `ph` (Phosphor) or `ri` (Remix). It is saved in `auvyx.json`, and `add --icons <library>` overrides it for one install.

```bash
npx @auvyx/cli add login-01 sidebar-07
```

`add` writes the block fragment to `auvyx/blocks/<name>.html`. Pass `--page` to also write a standalone page to `auvyx/pages/<name>.html`. Existing files are skipped unless you pass `--overwrite`; `--dry-run` prints what would be written.

## Components

Components install the same way as blocks, as plain CSS (split from `auvyx.min.css`, no Tailwind needed) plus their JavaScript when they have behavior:

```bash
npx @auvyx/cli add combobox tabs
```

The first one also writes `ui/base.css` (tokens, themes, preflight, layout primitives, motion), and each brings the components its examples use. `add` keeps `ui/index.css` importing every installed CSS file in the order they cascade in the bundle (each file's first line records it). Load that one file instead of `auvyx.min.css`, plus the `ui/*.js` files `add` lists. In React, import `ui/index.css` and those JS files once from your entry file. The files are the same for every framework.

## Frameworks

Blocks come as plain HTML (`html`, the default) or as React 19 components (`react`). `init` picks `react` when your `package.json` depends on React, and writes to `src/components/auvyx` (or `components/auvyx` without `src/`); pass `--framework` to choose yourself. It is saved in `auvyx.json`, and `add --framework <name>` overrides it for one install.

```bash
npx @auvyx/cli add login-01 --framework react
```

A React block is one `.tsx` file, `blocks/<name>.tsx`, with a default export. It renders the same markup as the HTML block, so it needs the same `auvyx.min.css` and `auvyx.min.js`, loaded once by your app (root layout or `index.html`). Blocks with `<auvyx-*>` elements also install `@auvyx/react-types` (`types/auvyx-*.d.ts`), their JSX types. The few blocks with demo scripts run them once after mount; those files are marked `// @ts-nocheck`.

```bash
npx @auvyx/cli list
```

## Registries

`auvyx.json` maps a namespace to a URL template. `{name}` is the item, `{framework}` the framework and `{icons}` the icon library. A registry whose URL has no `{framework}` serves HTML only. Items without a namespace use `@auvyx`.

```json
{
  "framework": "html",
  "dir": "auvyx",
  "icons": "tabler",
  "registries": {
    "@auvyx": "https://auvyx-ui.vercel.app/r/{framework}/{icons}/{name}.json",
    "@acme": {
      "url": "https://registry.acme.dev/r/{framework}/{icons}/{name}.json",
      "headers": { "Authorization": "Bearer ${ACME_TOKEN}" }
    }
  }
}
```

`@acme` stands for any other registry, such as a paid one. Any registry that serves the same item format works, public or private. Header values expand `${VAR}` from the environment, so tokens never live in the file. Auvyx's own registry is public and free; commercial blocks (for example Beamui's) are served by their own registries.

```bash
ACME_TOKEN=... npx @auvyx/cli add @acme/dashboard-02
```

A registry template can also be a local path, which is useful for testing a registry build.

## Registry item format

Built by `packages/blocks/tools/build_registry.mjs`. A subset of the shadcn registry item shape:

| Field | Meaning |
| --- | --- |
| `name`, `title`, `description`, `categories` | Item metadata |
| `type` | `registry:block`; `registry:ui` for components and `registry:style` for `base`; `registry:lib` for support files such as `react-types` |
| `meta.framework` | `html` or `react` |
| `meta.icons` | Icon library the item's inline SVGs use |
| `meta.*` | Anything the registry's `registry.json` entry puts in `meta` (other registries use it for their own fields) |
| `meta.scripts` | Extra scripts the block needs besides `auvyx.min.css`/`auvyx.min.js` |
| `registryDependencies` | Other items to install; unqualified names resolve in the same registry. A `registry:ui` item's list is complete for it, so the CLI does not follow its dependencies' own lists |
| `files[]` | `{ path, type, target, content }`; `target` is relative to `dir` and may not leave it |

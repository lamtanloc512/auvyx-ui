# @auvyx/cli

Copy Auvyx UI blocks into your project, shadcn-style: you own the code after `add`.

```bash
npx @auvyx/cli init --icons tabler
```

`init` points `@auvyx` at `https://auvyx-ui.vercel.app/r/{icons}/{name}.json`; pass `--registry` to use another one. `--icons` picks the icon library the blocks are delivered with: `lucide` (default), `tabler`, `hugeicons`, `ph` (Phosphor) or `ri` (Remix). It is saved in `auvyx.json`, and `add --icons <library>` overrides it for one install.

```bash
npx @auvyx/cli add login-01 sidebar-07
```

`add` writes the block fragment to `auvyx/blocks/<name>.html`. Pass `--page` to also write a standalone page to `auvyx/pages/<name>.html`. Existing files are skipped unless you pass `--overwrite`; `--dry-run` prints what would be written.

```bash
npx @auvyx/cli list
```

## Registries

`auvyx.json` maps a namespace to a URL template. `{name}` is the item and `{icons}` the icon library. Items without a namespace use `@auvyx`.

```json
{
  "dir": "auvyx",
  "icons": "tabler",
  "registries": {
    "@auvyx": "https://auvyx-ui.vercel.app/r/{icons}/{name}.json",
    "@auvyx-pro": {
      "url": "https://<pro-domain>/r/{icons}/{name}.json",
      "headers": { "Authorization": "Bearer ${AUVYX_LICENSE_KEY}" }
    }
  }
}
```

Header values expand `${VAR}` from the environment, so license keys never live in the file.

```bash
AUVYX_LICENSE_KEY=... npx @auvyx/cli add @auvyx-pro/dashboard-02
```

A registry template can also be a local path, which is useful for testing a registry build.

## Registry item format

Built by `packages/blocks/tools/build_registry.mjs`. A subset of the shadcn registry item shape:

| Field | Meaning |
| --- | --- |
| `name`, `title`, `description`, `categories` | Item metadata |
| `type` | `registry:block` |
| `meta.tier` | `free` or `pro` |
| `meta.icons` | Icon library the item's inline SVGs use |
| `meta.scripts` | Extra scripts the block needs besides `auvyx.min.css`/`auvyx.min.js` |
| `registryDependencies` | Other items to install; unqualified names resolve in the same registry |
| `files[]` | `{ path, type, target, content }`; `target` is relative to `dir` and may not leave it |

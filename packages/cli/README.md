# @auvyx/cli

Copy Auvyx UI blocks into your project, shadcn-style: you own the code after `add`.

```bash
npx @auvyx/cli init --registry https://<docs-domain>/r/{name}.json
```

```bash
npx @auvyx/cli add login-01 sidebar-07
```

`add` writes the block fragment to `auvyx/blocks/<name>.html`. Pass `--page` to also write a standalone page to `auvyx/pages/<name>.html`. Existing files are skipped unless you pass `--overwrite`; `--dry-run` prints what would be written.

```bash
npx @auvyx/cli list
```

## Registries

`auvyx.json` maps a namespace to a URL template. Items without a namespace use `@auvyx`.

```json
{
  "dir": "auvyx",
  "registries": {
    "@auvyx": "https://<docs-domain>/r/{name}.json",
    "@auvyx-pro": {
      "url": "https://<pro-domain>/r/{name}.json",
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
| `meta.scripts` | Extra scripts the block needs besides `auvyx.min.css`/`auvyx.min.js` |
| `registryDependencies` | Other items to install; unqualified names resolve in the same registry |
| `files[]` | `{ path, type, target, content }`; `target` is relative to `dir` and may not leave it |

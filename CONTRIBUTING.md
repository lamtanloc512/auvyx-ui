# Contributing to Auvyx UI

- Submit pull requests (PRs) against the `main` branch, which Vercel deploys to https://auvyx-ui.vercel.app (other branches get preview URLs).
- Keep changes focused: one feature or fix per PR.
- Test locally before submitting: `npm run check` (package), and `npm run auvyx:build` plus `npm run auvyx:test` for `packages/*` and the docs. CI runs them on every PR.
- Follow existing code style.

## Docs deploys

The docs site is `packages/docs` (built to `packages/docs/out` by `npm run auvyx:build`). Vercel deploys `main` to https://auvyx-ui.vercel.app and every other branch to a preview URL (see `vercel.json`). The upstream ReallySimpleDocs/Astro site (`site/`) was merged into it and removed.

## Releasing

`@auvyx/ui` and `@auvyx/cli` are published to npm from GitHub releases, one package per release:

1. Bump the version on `main`: `npm version 0.1.1 -w @auvyx/ui --no-git-tag-version`, commit and push.
2. Publish a GitHub release tagged `<package>@<version>` (`ui@0.1.1` or `cli@0.1.1`), or run the "Release Auvyx" workflow from the Actions tab and pick the package.

3. Approve the staged version on npmjs.com (Staged Packages) or with `npm stage approve <stage-id>`, with 2FA.

`.github/workflows/release-auvyx.yml` checks that the tag matches the package version, builds, and runs `npm stage publish --provenance` with npm trusted publishing (no token). Each package's trusted publisher is set on npmjs.com (Settings → Trusted Publisher → GitHub Actions: `lamtanloc512/auvyx-ui`, `release-auvyx.yml`, "Allow npm publish" off), so nothing reaches npm without a maintainer's approval.

The very first version of a package has to be published by hand, because npm only accepts a trusted publisher for a package that exists: `npm login`, then `npm run auvyx:publish` (builds and publishes both, asking for 2FA).

npm stages these versions: until a maintainer approves them (npmjs.com → Staged Packages, or `npm stage approve <stage-id>`, with 2FA) the package only holds a `0.0.0-stage` placeholder, and `npm install`, `npx` and the CDN do not serve the new version.

The upstream `basecoat-css` package is not published from this fork.

Thanks for helping!

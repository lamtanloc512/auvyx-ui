# Contributing to Basecoat

- Support development by sponsoring the author: https://github.com/sponsors/hunvreus
- Submit pull requests (PRs) against the `main` branch.
- Branches:
  - `main` is the default branch. All work lands here, and https://main-basecoat.hunvreus.workers.dev previews it.
  - `release` is what https://basecoatui.com deploys. Only the release workflow moves it (see below).
  - New features are worked in `feature/name-of-the-feature` branches.
  - Issues are addressed in `issue/123-main-issue` branches.
  - When ready, open a PR against `main`.
- Keep changes focused: one feature or fix per PR.
- Test locally before submitting: `npm run check` (package), and `npm run auvyx:build` plus `npm run auvyx:test` for `packages/*` and the docs. CI runs them on every PR.
- Follow existing code style.

## Docs deploys

The docs site is `packages/docs` (built to `packages/docs/out` by `npm run auvyx:build`). Vercel deploys `main` to https://auvyx-ui.vercel.app and every other branch to a preview URL (see `vercel.json`). The upstream ReallySimpleDocs/Astro site (`site/`) was merged into it and removed.

## Releasing

`@auvyx/ui` and `@auvyx/cli` are published to npm from GitHub releases, one package per release:

1. Bump the version on `main`: `npm version 0.1.1 -w @auvyx/ui --no-git-tag-version`, commit and push.
2. Publish a GitHub release tagged `<package>@<version>`: `ui@0.1.1` or `cli@0.1.1`.

`.github/workflows/release-auvyx.yml` checks that the tag matches the package version, builds, and runs `npm publish --provenance` with npm trusted publishing (no token). Each package's trusted publisher is set on npmjs.com (Settings → Trusted Publisher → GitHub Actions: `lamtanloc512/basecoat`, `release-auvyx.yml`).

The very first version of a package has to be published by hand, because npm only accepts a trusted publisher for a package that exists: `npm login`, then `npm run auvyx:publish` (builds and publishes both, asking for 2FA).

The upstream `basecoat-css` package is not published from this fork.

Thanks for helping!

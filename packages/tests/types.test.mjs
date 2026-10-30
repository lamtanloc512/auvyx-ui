// Generated element types (dist/types): DOM, React 19 JSX and Vue 3 templates
// type-check, and misuse (onToggle in React, wrong prop types) is an error.
import { test } from 'node:test';
import fs from 'node:fs/promises';
import path from 'node:path';
import { root, dist, freshDir, run, bin, requireBuild } from './lib/env.mjs';

test('element types check under tsc and vue-tsc', async () => {
  requireBuild();
  const dir = await freshDir('types');
  await fs.cp(path.join(root, 'packages/tests/fixtures/types'), dir, { recursive: true });
  await fs.cp(path.join(dist, 'types'), path.join(dir, 'auvyx-types'), { recursive: true });
  await fs.writeFile(path.join(dir, 'tsconfig.json'), JSON.stringify({
    compilerOptions: { strict: true, target: 'ES2022', module: 'ESNext', moduleResolution: 'Bundler', jsx: 'react-jsx', lib: ['ES2022', 'DOM'], noEmit: true, types: [] },
    include: ['*.ts', '*.tsx', '*.vue'],
  }));
  // The fixtures use @ts-expect-error / @vue-expect-error for misuse, so an
  // error that stops being reported fails too.
  run(bin('tsc'), ['-p', dir]);
  run(bin('vue-tsc'), ['-p', dir]);
});

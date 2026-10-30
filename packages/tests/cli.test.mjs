// The CLI against the built registry (packages/docs/out/r): frameworks, icon
// libraries, components and their dependencies, React types.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { root, registry, cli, freshDir, run, bin, json, requireBuild } from './lib/env.mjs';

const template = path.join(registry, '{framework}/{icons}/{name}.json');
const auvyx = (cwd, ...args) => run('node', [cli, ...args], { cwd });
const fails = (cwd, args, message) => assert.throws(() => auvyx(cwd, ...args), (e) => e.stderr.includes(message));

test('HTML project: blocks and pages', async () => {
  requireBuild();
  const dir = await freshDir('cli-html');
  auvyx(dir, 'init', '--registry', template, '--icons', 'tabler');
  assert.deepEqual((await json(path.join(dir, 'auvyx.json'))).framework, 'html');
  auvyx(dir, 'add', 'login-01', '--page');
  const block = await fs.readFile(path.join(dir, 'auvyx/blocks/login-01.html'), 'utf8');
  assert.match(block, /<form class="fieldset"/);
  await fs.access(path.join(dir, 'auvyx/pages/login-01.html'));
  assert.match(auvyx(dir, 'add', 'login-01'), /skip/);
  fails(dir, ['add', 'login-01', '--framework', 'vue'], 'unknown framework "vue"');
});

test('React project: detection, typed blocks, react-types dependency', async () => {
  const dir = await freshDir('cli-react');
  await fs.mkdir(path.join(dir, 'src'));
  await fs.writeFile(path.join(dir, 'package.json'), JSON.stringify({ dependencies: { react: '^19.2.0' } }));
  assert.match(auvyx(dir, 'init', '--registry', template), /React found in package.json/);
  const config = await json(path.join(dir, 'auvyx.json'));
  assert.equal(config.framework, 'react');
  assert.equal(config.dir, 'src/components/auvyx');
  auvyx(dir, 'add', 'calendar-22', 'login-01', 'dashboard-01');
  for (const f of ['blocks/calendar-22.tsx', 'blocks/login-01.tsx', 'types/auvyx-react.d.ts', 'types/auvyx-elements.d.ts']) {
    await fs.access(path.join(dir, 'src/components/auvyx', f));
  }
  await fs.writeFile(path.join(dir, 'src/App.tsx'), [
    'import Calendar22 from "./components/auvyx/blocks/calendar-22";',
    'import Login01 from "./components/auvyx/blocks/login-01";',
    'import Dashboard01 from "./components/auvyx/blocks/dashboard-01";',
    'export const App = () => <><Calendar22 /><Login01 /><Dashboard01 /></>;',
  ].join('\n'));
  await fs.writeFile(path.join(dir, 'tsconfig.json'), JSON.stringify({
    compilerOptions: { strict: true, target: 'ES2022', module: 'ESNext', moduleResolution: 'Bundler', jsx: 'react-jsx', lib: ['ES2022', 'DOM', 'DOM.Iterable'], noEmit: true, types: [] },
    include: ['src'],
  }));
  run(bin('tsc'), ['-p', dir]);
});

test('A registry without {framework} serves HTML only', async () => {
  const dir = await freshDir('cli-legacy');
  await fs.writeFile(path.join(dir, 'auvyx.json'), JSON.stringify({ dir: 'x', registries: { '@auvyx': path.join(registry, '{icons}/{name}.json') } }));
  auvyx(dir, 'add', 'login-01');
  fails(dir, ['add', 'login-01', '--framework', 'react'], 'serves HTML only');
});

test('Components: base, direct dependencies only, ui/index.css in cascade order', async () => {
  const dir = await freshDir('cli-ui');
  auvyx(dir, 'init', '--registry', template);
  const out = auvyx(dir, 'add', 'combobox');
  const { components } = await json(path.join(root, 'packages/ui/dist/ui/manifest.json'));
  const installed = (await fs.readdir(path.join(dir, 'auvyx/ui'))).sort();
  const expected = ['base.css', 'index.css', ...['combobox', ...components.combobox.dependencies].flatMap((c) => [...components[c].css, ...components[c].js].map((f) => path.basename(f)))].sort();
  assert.deepEqual(installed, expected, 'a dependency\'s own dependencies are not followed');
  assert.match(out, /<script src="auvyx\/ui\/combobox.js" defer><\/script>/);
  const order = async (f) => Number((await fs.readFile(path.join(dir, 'auvyx/ui', f), 'utf8')).match(/order (\d+)/)[1]);
  const imports = [...(await fs.readFile(path.join(dir, 'auvyx/ui/index.css'), 'utf8')).matchAll(/@import "\.\/(.+?)";/g)].map((m) => m[1]);
  assert.equal(imports[0], 'base.css');
  const orders = await Promise.all(imports.map(order));
  assert.deepEqual(orders, [...orders].sort((a, b) => a - b), 'index.css follows the bundle order');
  assert.deepEqual([...imports].sort(), installed.filter((f) => f.endsWith('.css') && f !== 'index.css'), 'index.css imports every installed CSS file');
});

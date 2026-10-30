#!/usr/bin/env node
// Auvyx CLI: copy blocks from a registry into your project (shadcn-style open code).
//
//   auvyx init [--framework html|react] [--registry <url-template>] [--icons <library>] [--dir <dir>]
//   auvyx add <item...> [--framework html|react] [--icons <library>] [--page] [--overwrite] [--dry-run]
//   auvyx list [@namespace]
//
// Items: `login-01` (default namespace), `@acme/dashboard-02`, a URL, or a
// local .json path. Registries map a namespace to a URL template with `{name}`
// and optionally `{framework}` (html or react) and `{icons}` (the icon library:
// lucide, tabler, hugeicons, ph, ri); headers may reference env vars as
// ${VAR}, so tokens stay out of the file.
import fs from 'node:fs/promises';
import path from 'node:path';

const CONFIG = 'auvyx.json';
const DEFAULT_NS = '@auvyx';
const DEFAULT_REGISTRY = 'https://auvyx-ui.vercel.app/r/{framework}/{icons}/{name}.json';
const ICON_LIBRARIES = ['lucide', 'tabler', 'hugeicons', 'ph', 'ri'];
const FRAMEWORKS = ['html', 'react'];
const SETUP_URL = 'https://auvyx-ui.vercel.app/#installation';

const argv = process.argv.slice(2);
const flags = new Set(argv.filter((a) => a.startsWith('--')));
const opt = (name) => {
  const i = argv.indexOf(`--${name}`);
  return i >= 0 ? argv[i + 1] : undefined;
};
const positional = argv.filter((a, i) => !a.startsWith('--') && !['--registry', '--dir', '--icons', '--framework'].includes(argv[i - 1]));
const [command, ...rest] = positional;

const fail = (msg) => {
  console.error(`auvyx: ${msg}`);
  process.exit(1);
};

async function loadConfig() {
  try {
    return JSON.parse(await fs.readFile(CONFIG, 'utf8'));
  } catch (e) {
    if (e.code === 'ENOENT') fail(`no ${CONFIG} found. Run \`auvyx init\` first.`);
    fail(`cannot read ${CONFIG}: ${e.message}`);
  }
}

function expandEnv(value, where) {
  return value.replace(/\$\{(\w+)\}/g, (_, name) => {
    const v = process.env[name];
    if (v === undefined) fail(`${where} needs the ${name} environment variable.`);
    return v;
  });
}

function iconLibrary(config) {
  const lib = opt('icons') ?? config.icons ?? 'lucide';
  if (!ICON_LIBRARIES.includes(lib)) fail(`unknown icon library "${lib}". Use one of: ${ICON_LIBRARIES.join(', ')}.`);
  return lib;
}

function framework(config) {
  const fw = opt('framework') ?? config.framework ?? 'html';
  if (!FRAMEWORKS.includes(fw)) fail(`unknown framework "${fw}". Use one of: ${FRAMEWORKS.join(', ')}.`);
  return fw;
}

// React when the project's package.json depends on it, HTML otherwise.
async function detectFramework() {
  try {
    const pkg = JSON.parse(await fs.readFile('package.json', 'utf8'));
    const deps = { ...pkg.dependencies, ...pkg.devDependencies };
    if (deps.react) return 'react';
  } catch (e) {
    if (e.code !== 'ENOENT') fail(`cannot read package.json: ${e.message}`);
  }
  return 'html';
}

function resolve(config, spec) {
  if (/^https?:\/\//.test(spec) || spec.endsWith('.json')) return { source: spec, headers: {} };
  const m = spec.match(/^(@[\w-]+)\/(.+)$/);
  const [ns, name] = m ? [m[1], m[2]] : [DEFAULT_NS, spec];
  const entry = config.registries?.[ns];
  if (!entry) fail(`unknown registry ${ns}. Add it to "registries" in ${CONFIG}.`);
  const { url, headers = {} } = typeof entry === 'string' ? { url: entry } : entry;
  const fw = framework(config);
  if (fw !== 'html' && !url.includes('{framework}')) fail(`${ns} serves HTML only (its URL has no {framework}); use --framework html.`);
  return {
    source: url.replaceAll('{framework}', fw).replaceAll('{icons}', iconLibrary(config)).replaceAll('{name}', encodeURIComponent(name)),
    headers: Object.fromEntries(Object.entries(headers).map(([k, v]) => [k, expandEnv(v, ns)])),
    ns,
  };
}

async function fetchJson({ source, headers, ns }) {
  if (!/^https?:\/\//.test(source)) return JSON.parse(await fs.readFile(source, 'utf8'));
  const res = await fetch(source, { headers });
  if (res.status === 401 || res.status === 403) fail(`${ns ?? source}: access denied (HTTP ${res.status}). Check this registry's credentials.`);
  if (res.status === 404) fail(`not found: ${source}`);
  if (!res.ok) fail(`${source}: HTTP ${res.status}`);
  return res.json();
}

async function init() {
  const registry = opt('registry') ?? process.env.AUVYX_REGISTRY ?? DEFAULT_REGISTRY;
  try {
    await fs.access(CONFIG);
    if (!flags.has('--overwrite')) fail(`${CONFIG} already exists (use --overwrite).`);
  } catch (e) {
    if (e.code !== 'ENOENT') throw e;
  }
  const detected = opt('framework') ? null : await detectFramework();
  const fw = framework({ framework: detected ?? undefined });
  const src = await fs.access('src').then(() => true, () => false);
  const config = {
    framework: fw,
    dir: opt('dir') ?? (fw === 'react' ? `${src ? 'src/' : ''}components/auvyx` : 'auvyx'),
    icons: iconLibrary({}),
    registries: { [DEFAULT_NS]: registry },
  };
  await fs.writeFile(CONFIG, JSON.stringify(config, null, 2) + '\n');
  console.log(`wrote ${CONFIG}${detected === 'react' ? ' (React found in package.json)' : ''}`);
  console.log(`\nLoad auvyx.min.css and auvyx.min.js once in your ${fw === 'react' ? 'root layout or index.html' : 'pages'}: ${SETUP_URL}`);
}

async function add() {
  if (!rest.length) fail('usage: auvyx add <item...>');
  const config = await loadConfig();
  const root = path.resolve(config.dir ?? 'auvyx');
  const seen = new Set();
  const scripts = new Set();
  const uiScripts = new Set();
  let uiCss = false;
  const qualify = (spec, ns = DEFAULT_NS) => (/^https?:\/\//.test(spec) || spec.endsWith('.json') || spec.startsWith('@') ? spec : `${ns}/${spec}`);
  // [spec, shallow]: a component's dependencies are already complete for it,
  // so theirs are not followed (they list what their own examples use).
  const queue = rest.map((spec) => [qualify(spec), false]);
  while (queue.length) {
    const [spec, shallow] = queue.shift();
    if (seen.has(spec)) continue;
    seen.add(spec);
    const ref = resolve(config, spec);
    const item = await fetchJson(ref);
    if (!shallow) {
      for (const dep of item.registryDependencies ?? []) {
        // Unqualified deps belong to the registry the item came from.
        queue.push([ref.ns ? qualify(dep, ref.ns) : dep, item.type === 'registry:ui']);
      }
    }
    for (const s of item.meta?.scripts ?? []) scripts.add(s);
    for (const file of item.files ?? []) {
      if (/^registry:(ui|style)$/.test(file.type)) {
        if (file.target.endsWith('.css')) uiCss = true;
        else uiScripts.add(file.target);
      }
      if (file.type === 'registry:page' && !flags.has('--page')) continue;
      const target = path.resolve(root, file.target ?? file.path);
      // Never let a registry write outside the configured directory.
      if (target !== root && !target.startsWith(root + path.sep)) fail(`${item.name}: refusing to write ${file.target}`);
      const rel = path.relative(process.cwd(), target);
      const exists = await fs.access(target).then(() => true, () => false);
      if (exists && !flags.has('--overwrite')) {
        console.log(`skip    ${rel} (exists, use --overwrite)`);
        continue;
      }
      if (flags.has('--dry-run')) {
        console.log(`would write ${rel}`);
        continue;
      }
      await fs.mkdir(path.dirname(target), { recursive: true });
      await fs.writeFile(target, file.content);
      console.log(`write   ${rel}`);
    }
  }
  if (uiCss && !flags.has('--dry-run')) await writeUiIndex(root);
  if (uiCss || uiScripts.size) {
    const rel = (f) => path.relative(process.cwd(), path.join(root, f)).split(path.sep).join('/');
    const react = framework(config) === 'react';
    console.log(`\nComponents: load ${rel('ui/index.css')} once${react ? ' (import it in your root layout or entry file)' : ''}, instead of auvyx.min.css.`);
    if (uiScripts.size) console.log(react ? 'And import these once from your entry file (they register their behavior):' : 'And add:');
    for (const f of uiScripts) console.log(react ? `  ${rel(f)}` : `  <script src="${rel(f)}" defer></script>`);
  }
  if (scripts.size) {
    console.log(`\nThese blocks also need${framework(config) === 'react' ? ', loaded once in your root layout or index.html' : ''}:`);
    for (const s of scripts) console.log(`  <script src="${s}" defer></script>`);
  }
}

// ui/index.css imports every installed component in the bundle's order (each
// file's first line says `order N`), so they cascade as in auvyx.min.css.
async function writeUiIndex(root) {
  const dir = path.join(root, 'ui');
  const entries = [];
  for (const name of await fs.readdir(dir)) {
    if (!name.endsWith('.css') || name === 'index.css') continue;
    const first = (await fs.readFile(path.join(dir, name), 'utf8')).split('\n', 1)[0];
    const order = Number(first.match(/\border (\d+)/)?.[1] ?? Infinity);
    entries.push({ name, order });
  }
  entries.sort((a, b) => a.order - b.order || a.name.localeCompare(b.name));
  const text = `/* Auvyx UI components, in the order they cascade. Written by \`auvyx add\`; files you add yourself go last. */\n${entries.map((e) => `@import "./${e.name}";`).join('\n')}\n`;
  await fs.writeFile(path.join(dir, 'index.css'), text);
  console.log(`write   ${path.relative(process.cwd(), path.join(dir, 'index.css'))}`);
}

async function list() {
  const config = await loadConfig();
  const ns = rest[0] ?? DEFAULT_NS;
  const { items = [] } = await fetchJson(resolve(config, `${ns}/index`));
  for (const it of items) console.log(`${it.name.padEnd(16)} ${it.description}`);
}

const commands = { init, add, list };
if (!commands[command]) {
  console.log('usage: auvyx <init|add|list> ...');
  process.exit(command ? 1 : 0);
}
await commands[command]();

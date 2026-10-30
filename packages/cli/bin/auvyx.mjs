#!/usr/bin/env node
// Auvyx CLI: copy blocks from a registry into your project (shadcn-style open code).
//
//   auvyx init [--registry <url-template>] [--dir <dir>]
//   auvyx add <item...> [--page] [--overwrite] [--dry-run]
//   auvyx list [@namespace]
//
// Items: `login-01` (default namespace), `@auvyx-pro/dashboard-02`, a URL, or a
// local .json path. Registries map a namespace to a URL template with `{name}`;
// headers may reference env vars as ${VAR}, so license keys stay out of the file.
import fs from 'node:fs/promises';
import path from 'node:path';

const CONFIG = 'auvyx.json';
const DEFAULT_NS = '@auvyx';

const argv = process.argv.slice(2);
const flags = new Set(argv.filter((a) => a.startsWith('--')));
const opt = (name) => {
  const i = argv.indexOf(`--${name}`);
  return i >= 0 ? argv[i + 1] : undefined;
};
const positional = argv.filter((a, i) => !a.startsWith('--') && !['--registry', '--dir'].includes(argv[i - 1]));
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

function resolve(config, spec) {
  if (/^https?:\/\//.test(spec) || spec.endsWith('.json')) return { source: spec, headers: {} };
  const m = spec.match(/^(@[\w-]+)\/(.+)$/);
  const [ns, name] = m ? [m[1], m[2]] : [DEFAULT_NS, spec];
  const entry = config.registries?.[ns];
  if (!entry) fail(`unknown registry ${ns}. Add it to "registries" in ${CONFIG}.`);
  const { url, headers = {} } = typeof entry === 'string' ? { url: entry } : entry;
  return {
    source: url.replace('{name}', encodeURIComponent(name)),
    headers: Object.fromEntries(Object.entries(headers).map(([k, v]) => [k, expandEnv(v, ns)])),
    ns,
  };
}

async function fetchJson({ source, headers, ns }) {
  if (!/^https?:\/\//.test(source)) return JSON.parse(await fs.readFile(source, 'utf8'));
  const res = await fetch(source, { headers });
  if (res.status === 401 || res.status === 403) fail(`${ns ?? source}: access denied. Check your license key.`);
  if (res.status === 404) fail(`not found: ${source}`);
  if (!res.ok) fail(`${source}: HTTP ${res.status}`);
  return res.json();
}

async function init() {
  const registry = opt('registry') ?? process.env.AUVYX_REGISTRY;
  if (!registry) fail('pass --registry <url-template>, e.g. https://example.com/r/{name}.json');
  try {
    await fs.access(CONFIG);
    if (!flags.has('--overwrite')) fail(`${CONFIG} already exists (use --overwrite).`);
  } catch (e) {
    if (e.code !== 'ENOENT') throw e;
  }
  const config = {
    dir: opt('dir') ?? 'auvyx',
    registries: { [DEFAULT_NS]: registry },
  };
  await fs.writeFile(CONFIG, JSON.stringify(config, null, 2) + '\n');
  console.log(`wrote ${CONFIG}`);
}

async function add() {
  if (!rest.length) fail('usage: auvyx add <item...>');
  const config = await loadConfig();
  const root = path.resolve(config.dir ?? 'auvyx');
  const seen = new Set();
  const scripts = new Set();
  const queue = [...rest];
  while (queue.length) {
    const spec = queue.shift();
    if (seen.has(spec)) continue;
    seen.add(spec);
    const ref = resolve(config, spec);
    const item = await fetchJson(ref);
    for (const dep of item.registryDependencies ?? []) {
      // Unqualified deps belong to the registry the item came from.
      queue.push(ref.ns && !dep.startsWith('@') && !/^https?:/.test(dep) ? `${ref.ns}/${dep}` : dep);
    }
    for (const s of item.meta?.scripts ?? []) scripts.add(s);
    for (const file of item.files ?? []) {
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
  if (scripts.size) {
    console.log('\nThese blocks also need:');
    for (const s of scripts) console.log(`  <script src="${s}" defer></script>`);
  }
}

async function list() {
  const config = await loadConfig();
  const ns = rest[0] ?? DEFAULT_NS;
  const { items = [] } = await fetchJson(resolve(config, `${ns}/index`));
  for (const it of items) console.log(`${it.name.padEnd(16)} ${it.meta?.tier === 'free' ? '' : `[${it.meta?.tier}] `}${it.description}`);
}

const commands = { init, add, list };
if (!commands[command]) {
  console.log('usage: auvyx <init|add|list> ...');
  process.exit(command ? 1 : 0);
}
await commands[command]();

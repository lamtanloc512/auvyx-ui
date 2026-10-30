// Shared helpers for the Auvyx checks: paths, a static server for the repo,
// a browser, and pixel comparison of screenshots.
import fs from 'node:fs/promises';
import { existsSync } from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

export const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
export const tmp = path.join(root, 'packages/tests/.tmp');
export const dist = path.join(root, 'packages/ui/dist');
export const registry = path.join(root, 'packages/docs/out/r');
export const cli = path.join(root, 'packages/cli/bin/auvyx.mjs');
export const bin = (name) => path.join(root, 'node_modules/.bin', name);

// The checks read the build output; build first (npm run auvyx:build).
export function requireBuild() {
  for (const f of [path.join(dist, 'auvyx.min.css'), path.join(dist, 'ui/manifest.json'), path.join(registry, 'react/lucide/index.json')]) {
    if (!existsSync(f)) throw new Error(`missing ${path.relative(root, f)}: run npm run auvyx:build first`);
  }
}

export async function freshDir(name) {
  const dir = path.join(tmp, name);
  await fs.rm(dir, { recursive: true, force: true });
  await fs.mkdir(dir, { recursive: true });
  return dir;
}

export const run = (cmd, args, opts = {}) => execFileSync(cmd, args, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], ...opts });

export const json = async (file) => JSON.parse(await fs.readFile(file, 'utf8'));

const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp' };

// Serves the repository root, so block pages find ../ui/dist as on disk.
export async function serve() {
  const server = http.createServer(async (req, res) => {
    const file = path.join(root, decodeURIComponent(new URL(req.url, 'http://x').pathname));
    if (!file.startsWith(root)) { res.writeHead(403).end(); return; }
    try {
      const body = await fs.readFile(file);
      res.writeHead(200, { 'content-type': TYPES[path.extname(file)] ?? 'application/octet-stream' }).end(body);
    } catch {
      res.writeHead(404).end();
    }
  });
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const base = `http://127.0.0.1:${server.address().port}`;
  return { url: (p) => base + '/' + path.relative(root, p).split(path.sep).join('/'), close: () => new Promise((r) => server.close(r)) };
}

export async function browser() {
  return chromium.launch();
}

// Opens a page, waits for fonts and scripts, and collects errors.
export async function open(b, url, { width = 1280, height = 900 } = {}) {
  const page = await b.newPage({ viewport: { width, height } });
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => { if (m.type() === 'error' && !/favicon|Failed to load resource/.test(m.text())) errors.push(m.text()); });
  await page.goto(url, { waitUntil: 'networkidle' });
  // Pages rendered by script request their fonts only once the text exists:
  // wait for fonts and the network again after the first render.
  for (let i = 0; i < 2; i++) {
    await page.waitForTimeout(300);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForLoadState('networkidle');
  }
  return { page, errors };
}

export const shot = async (page, fullPage = true) => (await page.screenshot({ fullPage, animations: 'disabled' })).toString('base64');

// Number of pixels whose RGB differs by more than 30 in total, or a size mismatch.
export async function diff(b, a, c) {
  const page = await b.newPage();
  try {
    return await page.evaluate(async ([a, c]) => {
      const load = (s) => new Promise((r) => { const i = new Image(); i.onload = () => r(i); i.src = 'data:image/png;base64,' + s; });
      const [x, y] = await Promise.all([load(a), load(c)]);
      if (x.width !== y.width || x.height !== y.height) return { pixels: Infinity, size: `${x.width}x${x.height} vs ${y.width}x${y.height}` };
      const canvas = new OffscreenCanvas(x.width, x.height);
      const g = canvas.getContext('2d');
      g.drawImage(x, 0, 0);
      const d1 = g.getImageData(0, 0, x.width, x.height).data;
      g.drawImage(y, 0, 0);
      const d2 = g.getImageData(0, 0, x.width, x.height).data;
      let pixels = 0;
      for (let i = 0; i < d1.length; i += 4) if (Math.abs(d1[i] - d2[i]) + Math.abs(d1[i + 1] - d2[i + 1]) + Math.abs(d1[i + 2] - d2[i + 2]) > 30) pixels++;
      return { pixels };
    }, [a, c]);
  } finally {
    await page.close();
  }
}

// Screenshots two pages (`take` returns both, base64) up to `tries` times and
// returns the smallest difference: rendering noise (text antialiasing, late
// images) changes from one load to the next, a real difference does not.
export async function stableDiff(b, take, { tries = 3, tolerance = 0 } = {}) {
  let best;
  for (let i = 0; i < tries; i++) {
    const shots = await take();
    const d = await diff(b, ...shots);
    if (!best || d.pixels < best.pixels) best = { ...d, shots };
    if (best.pixels <= tolerance) break;
  }
  return best;
}

// Keeps both screenshots of a failed comparison for the CI artifact.
export async function keep(name, a, c) {
  const dir = path.join(tmp, 'failures');
  await fs.mkdir(dir, { recursive: true });
  await fs.writeFile(path.join(dir, `${name}-a.png`), Buffer.from(a, 'base64'));
  await fs.writeFile(path.join(dir, `${name}-b.png`), Buffer.from(c, 'base64'));
}

// AUVYX_BLOCKS=login-01,login-04 limits the block checks while working on them.
export const blockNames = async () => {
  const all = Object.keys(await json(path.join(root, 'packages/blocks/registry.json'))).sort();
  const only = process.env.AUVYX_BLOCKS?.split(',').filter(Boolean);
  return only ? all.filter((n) => only.includes(n)) : all;
};
export const componentDocs = () => json(path.join(root, 'packages/docs/src/data/components.json'));

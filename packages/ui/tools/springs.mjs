// Print CSS linear() easings for the motion spring presets (src/css/motion).
//
//   node packages/ui/tools/springs.mjs
//
// Simulates a damped spring from 0 to 1 (Beamui's Motion presets), takes the
// time it needs to settle within 0.1% as the duration, and samples the curve.
const SPRINGS = {
  snappy: { stiffness: 500, damping: 35, mass: 0.8 },
  gentle: { stiffness: 240, damping: 28, mass: 1 },
  playful: { stiffness: 320, damping: 20, mass: 0.9 },
};

for (const [name, { stiffness, damping, mass }] of Object.entries(SPRINGS)) {
  const dt = 1 / 2000, xs = [];
  let x = 0, v = 0, t = 0, settled = 0;
  while (t < 3) {
    const a = (-stiffness * (x - 1) - damping * v) / mass;
    v += a * dt; x += v * dt; t += dt; xs.push(x);
    settled = Math.abs(x - 1) < 0.001 && Math.abs(v) < 0.01 ? settled || t : 0;
    if (settled && t - settled > 0.05) break;
  }
  const duration = Math.round((settled || t) * 1000);
  const n = 30, step = settled / dt / n;
  const points = Array.from({ length: n + 1 }, (_, i) => +xs[Math.min(xs.length - 1, Math.round(i * step))].toFixed(3));
  points[0] = 0; points[n] = 1;
  console.log(`  --spring-${name}: linear(${points.join(', ')});\n  --spring-${name}-duration: ${duration}ms;`);
}

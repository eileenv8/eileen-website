/* Hero animation: a mycelial network.
   A few spores send out hyphae (thin threads) that wander, branch, and fuse
   where two colonies meet. Every branch point and fusion becomes a node, and
   the threads between nodes become the edges of a network graph. Once the
   network has grown, small pulses travel along it, the way nutrients and
   signals move through real mycelium. Then it fades and grows again.

   Instance mode so nothing leaks into the global scope. */
(function () {
  const host = document.getElementById('hero-canvas');
  if (!host || typeof p5 === 'undefined') return;

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  new p5(function (s) {
    const STEP = 1.1;          // px a hyphal tip grows per frame
    const BRANCH = 0.017;      // chance per step that a tip forks
    const MAX_TIPS = 230;      // cap on growing tips at once
    const FUSE = 4;            // px: closer than this to another colony = fuse
    const CELL = 8;            // spatial-hash cell size
    const SHOW = 1500;         // frames to keep pulsing after growth stops
    const FADE = 120;          // frames to fade before regrowing

    let layer;                 // the grown network, drawn once and kept
    let tips, grid, nodes, edges, pulses;
    let phase, timer, t;

    // ---------- helpers ----------
    function key(x, y) { return (Math.floor(x / CELL)) + ',' + (Math.floor(y / CELL)); }
    function remember(x, y, colony, node) {
      const k = key(x, y);
      (grid[k] || (grid[k] = [])).push({ x: x, y: y, colony: colony, node: node });
    }
    function nearbyOther(x, y, colony) {
      const cx = Math.floor(x / CELL), cy = Math.floor(y / CELL);
      for (let i = -1; i <= 1; i++) for (let j = -1; j <= 1; j++) {
        const list = grid[(cx + i) + ',' + (cy + j)];
        if (!list) continue;
        for (const p of list) {
          if (p.colony !== colony && Math.abs(p.x - x) < FUSE && Math.abs(p.y - y) < FUSE) return p;
        }
      }
      return null;
    }
    // fade threads under the headline so the type stays readable
    // on phones the headline spans the full width, so everything stays light
    function narrow() { return s.width < 600; }
    function weightAt(x) {
      if (narrow()) return 0.45;
      return 0.25 + 0.75 * s.constrain((x / s.width - 0.15) / 0.45, 0, 1);
    }

    function addNode(x, y, kind) {
      nodes.push({ x: x, y: y, kind: kind });
      const r = kind === 'spore' ? 3.2 : kind === 'fusion' ? 2.4 : 1.3;
      const a = 255 * weightAt(x);
      layer.noStroke();
      if (kind === 'spore') {
        layer.fill(255); layer.stroke(0, a); layer.strokeWeight(1.2);
        layer.circle(x, y, r * 2);
      } else {
        layer.fill(0, a);
        layer.circle(x, y, r * 2);
      }
      return nodes.length - 1;
    }

    function newTip(x, y, angle, colony, gen, from) {
      return { x: x, y: y, a: angle, h: angle, colony: colony, gen: gen, from: from,
               path: [[x, y]], life: s.random(150, 420) / (1 + gen * 0.4) };
    }

    // ---------- lifecycle ----------
    function seed() {
      layer.clear();
      tips = []; grid = {}; nodes = []; edges = []; pulses = [];
      phase = 'grow'; timer = 0;
      const n = Math.max(4, Math.round(s.width / 230));
      for (let c = 0; c < n; c++) {
        // spores lean right, away from the headline
        const x = narrow() ? s.width * s.random(0.05, 0.95) : s.width * s.random(0.38, 0.97);
        const y = narrow() ? s.height * (c % 2 ? s.random(0.82, 0.97) : s.random(0.03, 0.18))
                           : s.height * s.random(0.12, 0.88);
        const id = addNode(x, y, 'spore');
        const arms = Math.floor(s.random(3, 6));
        for (let k = 0; k < arms; k++) tips.push(newTip(x, y, s.random(s.TWO_PI), c, 0, id));
      }
    }

    function grow() {
      const next = [];
      for (const tip of tips) {
        // wander: a slow noise field plus a little jitter, so threads curve but don't scribble
        tip.a += (s.noise(tip.x * 0.006, tip.y * 0.006, t * 0.002) - 0.5) * 0.12 + s.random(-0.05, 0.05);
        tip.a += (tip.h - tip.a) * 0.03;             // threads keep heading outward, so no spirals
        const nx = tip.x + Math.cos(tip.a) * STEP;
        const ny = tip.y + Math.sin(tip.a) * STEP;
        const w = Math.max(0.35, 1.25 - tip.gen * 0.22);
        layer.stroke(0, 200 * weightAt(nx) * (tip.gen ? 0.8 : 1));
        layer.strokeWeight(w);
        layer.line(tip.x, tip.y, nx, ny);
        tip.x = nx; tip.y = ny; tip.life--;
        tip.path.push([nx, ny]);

        const hit = nearbyOther(nx, ny, tip.colony);
        const out = nx < -10 || ny < -10 || nx > s.width + 10 || ny > s.height + 10;
        if (hit) {
          // anastomosis: two colonies meet and join, making a new node in the network
          const id = addNode(hit.x, hit.y, 'fusion');
          edges.push({ a: tip.from, b: id, path: tip.path });
          continue;
        }
        if (out || tip.life <= 0) {
          if (tip.path.length > 12) {
            const id = addNode(nx, ny, 'tip');
            edges.push({ a: tip.from, b: id, path: tip.path });
          }
          continue;
        }
        if (tip.path.length % 3 === 0) remember(nx, ny, tip.colony);
        if (tips.length + next.length < MAX_TIPS && tip.gen < 6 && s.random() < BRANCH && tip.path.length > 10) {
          // fork: close this edge at a new branch node and send out two children
          const id = addNode(nx, ny, 'branch');
          edges.push({ a: tip.from, b: id, path: tip.path });
          const spread = s.random(0.5, 1.1);
          next.push(newTip(nx, ny, tip.a - spread / 2, tip.colony, tip.gen + 1, id));
          next.push(newTip(nx, ny, tip.a + spread / 2, tip.colony, tip.gen + 1, id));
          continue;
        }
        next.push(tip);
      }
      tips = next;
    }

    function spawnPulse() {
      if (!edges.length) return;
      const e = edges[Math.floor(s.random(edges.length))];
      if (e.path.length < 8) return;
      pulses.push({ e: e, i: 0, speed: s.random(1.2, 2.6), dir: s.random() < 0.5 ? 1 : -1 });
    }

    function drawPulses() {
      s.noStroke();
      const keep = [];
      for (const p of pulses) {
        const path = p.e.path;
        p.i += p.speed;
        if (p.i >= path.length - 1) continue;
        const idx = p.dir > 0 ? Math.floor(p.i) : path.length - 1 - Math.floor(p.i);
        const pt = path[idx];
        const a = 255 * weightAt(pt[0]);
        s.fill(0, a * 0.18); s.circle(pt[0], pt[1], 9);
        s.fill(0, a); s.circle(pt[0], pt[1], 3);
        keep.push(p);
      }
      pulses = keep;
    }

    // ---------- p5 ----------
    function build() {
      layer = s.createGraphics(s.width, s.height);
      layer.pixelDensity(s.pixelDensity());
      seed();
    }

    s.setup = function () {
      const c = s.createCanvas(host.offsetWidth, host.offsetHeight);
      c.parent(host);
      s.pixelDensity(Math.min(2, window.devicePixelRatio || 1));
      t = 0;
      build();
      if (reduced) {
        // grow the whole network at once and hold still
        while (tips.length && t < 3000) { t++; grow(); }
        s.background(255); s.image(layer, 0, 0);
        s.noLoop();
      } else {
        s.frameRate(60);
      }
    };

    s.draw = function () {
      t++;
      s.background(255);
      if (phase === 'grow') {
        grow();
        if (!tips.length) { phase = 'show'; timer = 0; }
        if (s.random() < 0.08) spawnPulse();
      } else if (phase === 'show') {
        timer++;
        if (s.random() < 0.22) spawnPulse();
        if (timer > SHOW) { phase = 'fade'; timer = 0; }
      } else {
        timer++;
        if (timer > FADE) { seed(); }
      }
      const alpha = phase === 'fade' ? 255 * (1 - timer / FADE) : 255;
      s.tint(255, alpha);
      s.image(layer, 0, 0);
      s.noTint();
      if (phase !== 'fade') drawPulses();
    };

    s.windowResized = function () {
      if (host.offsetWidth === s.width && host.offsetHeight === s.height) return;
      s.resizeCanvas(host.offsetWidth, host.offsetHeight);
      build();
      if (reduced) {
        while (tips.length && t < 3000) { t++; grow(); }
        s.background(255); s.image(layer, 0, 0);
      }
    };
  });
})();

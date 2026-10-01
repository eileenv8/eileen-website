/* Hero animation — a flow field of soft brush strokes.
   Instance mode so nothing leaks into the global scope. */
(function () {
  const host = document.getElementById('hero-canvas');
  if (!host || typeof p5 === 'undefined') return;

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  new p5(function (s) {
    // Weighted: warm tones lead, ink appears roughly one stroke in six.
    const PALETTE = [
      [196, 85, 44],    // rust
      [196, 85, 44],    // rust
      [46, 93, 79],     // deep green
      [46, 93, 79],     // deep green
      [201, 154, 61],   // ochre
      [23, 21, 15]      // ink
    ];
    const COUNT = 120;
    const CYCLE = 900;          // frames before the field gently resets
    let strokes = [];
    let zoff = 0;
    let age = 0;

    function seed() {
      strokes = [];
      for (let i = 0; i < COUNT; i++) strokes.push(newStroke());
    }

    function newStroke() {
      const c = PALETTE[Math.floor(s.random(PALETTE.length))];
      return {
        x: s.random(-40, s.width + 40),
        y: s.random(-40, s.height + 40),
        life: s.random(90, 320),
        w: s.random(0.8, 3.6),
        c: c,
        a: s.random(12, 28)
      };
    }

    function step(k) {
      const angle = s.noise(k.x * 0.0009, k.y * 0.0009, zoff) * s.TWO_PI * 2;
      const nx = k.x + Math.cos(angle) * 1.6;
      const ny = k.y + Math.sin(angle) * 1.6;
      s.stroke(k.c[0], k.c[1], k.c[2], k.a);
      s.strokeWeight(k.w);
      s.line(k.x, k.y, nx, ny);
      k.x = nx;
      k.y = ny;
      k.life--;
      if (k.life <= 0 || k.x < -60 || k.x > s.width + 60 || k.y < -60 || k.y > s.height + 60) {
        Object.assign(k, newStroke());
      }
    }

    s.setup = function () {
      const c = s.createCanvas(host.offsetWidth, host.offsetHeight);
      c.parent(host);
      s.background(255, 255, 255);
      s.noFill();
      seed();
      if (reduced) {
        // One static composition, no motion.
        for (let i = 0; i < 900; i++) {
          zoff += 0.0008;
          strokes.forEach(step);
        }
        s.noLoop();
      } else {
        s.frameRate(30);
      }
    };

    s.draw = function () {
      zoff += 0.0012;
      age++;
      // Very slow bleed back toward paper so the field never turns to mud.
      s.noStroke();
      s.fill(255, 255, 255, 6);
      s.rect(0, 0, s.width, s.height);
      s.noFill();
      strokes.forEach(step);
      if (age > CYCLE) { age = 0; seed(); }
    };

    s.windowResized = function () {
      s.resizeCanvas(host.offsetWidth, host.offsetHeight);
      s.background(255, 255, 255);
      seed();
      if (reduced) {
        for (let i = 0; i < 900; i++) { zoff += 0.0008; strokes.forEach(step); }
      }
    };
  });
})();

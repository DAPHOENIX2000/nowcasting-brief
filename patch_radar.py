# -*- coding: utf-8 -*-
"""
Replace the hero decoration with one real effect.

What was there: a static SVG radar scope, plus four blurred ellipse clusters
drifting as "clouds". Two weak effects competing, and the clouds in particular
read as blobs rather than as weather.

What replaces it: a single animated radar scope on a 2D canvas, showing an
evolving precipitation field — advecting echoes, banded and coloured by the
same NEXRAD reflectivity ramp the charts use. It is the one thing on the page
that is literally what the model predicts, so it earns its place rather than
decorating.

Canvas 2D deliberately, not WebGL: section 06 already holds a WebGL context for
the interactive kernel, and browsers cap live contexts. The field is sampled
from one tileable value-noise texture generated once, so each frame is two
lookups per pixel over a small buffer rather than per-frame noise.

It pauses off-screen, renders a single static frame under prefers-reduced-motion,
and takes no pointer events.
"""
import io
import re
import sys

P = "index.html"
s = io.open(P, encoding="utf-8").read()
n = 0


def sub(old, new):
    global s, n
    if s.count(old) != 1:
        sys.exit("NOT UNIQUE (%d): %s" % (s.count(old), old[:76]))
    s = s.replace(old, new)
    n += 1


# ── 1. drop the cloud field CSS ─────────────────────────────────────────────
m = re.search(r"/\* ═+ drifting cloud field ═+\n.*?\.cl4\{animation:drift 40s ease-in-out infinite alternate-reverse\}\n",
              s, re.S)
if not m:
    sys.exit("cloud CSS block not found")
s = s[:m.start()] + s[m.end():]
n += 1

# ── 2. the radar becomes a canvas ───────────────────────────────────────────
sub(""".radar{position:absolute; inset-inline-end:-38px; top:-34px; width:330px; height:330px; opacity:.34}
html[dir=rtl] .radar{transform:scaleX(-1)}""",
    """/* One effect, and it is the subject itself: an evolving precipitation field
   on a radar scope, banded by the same reflectivity ramp as the charts. */
.radar{
  position:absolute; inset-inline-end:-56px; top:-52px;
  width:min(392px,54vw); height:min(392px,54vw);
  pointer-events:none; opacity:.92;
  mask-image:radial-gradient(circle at 50% 50%, #000 62%, transparent 76%);
  -webkit-mask-image:radial-gradient(circle at 50% 50%, #000 62%, transparent 76%);
}
/* keeps the headline readable over the brightest frame of the sweep */
.scope::after{
  content:""; position:absolute; inset:0; pointer-events:none;
  background:linear-gradient(100deg, rgba(20,45,62,.55) 0%, rgba(20,45,62,.25) 46%, transparent 72%);
}""")

# ── 3. drop the cloud markup and swap the SVG scope for a canvas ────────────
m = re.search(r'<div class="sky" aria-hidden="true">.*?</div>\n', s, re.S)
if not m:
    sys.exit("sky div not found")
s = s[:m.start()] + s[m.end():]
n += 1

m = re.search(r'    <svg class="radar" viewBox="0 0 200 200" aria-hidden="true">.*?</svg>\n', s, re.S)
if not m:
    sys.exit("radar svg not found")
s = s[:m.start()] + '    <canvas class="radar" id="scope" aria-hidden="true"></canvas>\n' + s[m.end():]
n += 1

m = re.search(r'    <svg class="herocloud" viewBox="0 0 1200 150".*?</svg>\n', s, re.S)
if not m:
    sys.exit("herocloud not found")
s = s[:m.start()] + s[m.end():]
n += 1

# the hero no longer needs room for a cloud bank at its foot
sub("box-shadow:var(--shadow-l); padding:38px 38px 96px; margin-bottom:18px;",
    "box-shadow:var(--shadow-l); padding:38px 38px 40px; margin-bottom:18px;")

# ── 4. the renderer ─────────────────────────────────────────────────────────
RADAR = r"""
/* ════════════════════════════════════════════════════════════════
   The radar scope.

   A tileable value-noise field is generated once; each frame samples it at two
   slowly diverging offsets and multiplies them, which gives echoes that drift
   AND change shape rather than sliding rigidly across the screen. Values are
   banded into the reflectivity ramp, so what is on screen reads the way a real
   radar product does — light rain at the edges of a cell, heavy at its core.
   ════════════════════════════════════════════════════════════════ */
(function(){
  var cv = document.getElementById("scope");
  if (!cv || !cv.getContext) return;
  var ctx = cv.getContext("2d", { alpha: true });
  if (!ctx) return;

  var reduced = window.matchMedia &&
                window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ── one tileable fBm field, built once ──
  var N = 128;                       // lattice size, power of two so it wraps
  var field = new Float32Array(N * N);
  (function build(){
    function lattice(size){
      var g = new Float32Array(size * size);
      for (var i = 0; i < g.length; i++) g[i] = Math.random();
      return g;
    }
    function sample(g, size, x, y){
      var xi = Math.floor(x), yi = Math.floor(y);
      var xf = x - xi, yf = y - yi;
      var sx = xf * xf * (3 - 2 * xf), sy = yf * yf * (3 - 2 * yf);
      function at(a, b){ return g[((b % size) + size) % size * size + ((a % size) + size) % size]; }
      var a = at(xi, yi), b = at(xi + 1, yi), c = at(xi, yi + 1), d = at(xi + 1, yi + 1);
      return (a * (1 - sx) + b * sx) * (1 - sy) + (c * (1 - sx) + d * sx) * sy;
    }
    var octaves = [4, 8, 16, 32], amp = [0.5, 0.26, 0.15, 0.09], gs = [];
    for (var o = 0; o < octaves.length; o++) gs.push(lattice(octaves[o]));
    for (var y = 0; y < N; y++) for (var x = 0; x < N; x++){
      var v = 0;
      for (var k = 0; k < octaves.length; k++)
        v += amp[k] * sample(gs[k], octaves[k], x / N * octaves[k], y / N * octaves[k]);
      field[y * N + x] = v;
    }
  })();

  function fld(x, y){
    var xi = ((Math.round(x) % N) + N) % N, yi = ((Math.round(y) % N) + N) % N;
    return field[yi * N + xi];
  }

  // reflectivity ramp — light rain through to the core of a cell
  var BANDS = [
    [0.560, 62, 138, 180, 0.42],
    [0.598, 46, 150, 120, 0.60],
    [0.634, 96, 168, 78, 0.72],
    [0.668, 214, 178, 46, 0.80],
    [0.702, 220, 122, 44, 0.88],
    [0.736, 186, 60, 42, 0.94],
  ];

  var R = 0, buf = null, img = null, dpr = 1;
  function resize(){
    var css = cv.clientWidth || 320;
    dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    cv.width = Math.round(css * dpr);
    cv.height = Math.round(css * dpr);
    R = cv.width / 2;
    var side = Math.max(64, Math.round(cv.width / 3));   // echoes render coarse
    buf = document.createElement("canvas");
    buf.width = buf.height = side;
    img = buf.getContext("2d").createImageData(side, side);
  }

  function echoes(t){
    var side = buf.width, d = img.data, half = side / 2;
    var ax = t * 7.5, ay = t * 2.4;          // advection
    var bx = -t * 3.1, by = t * 5.0;         // second field, diverging
    for (var y = 0; y < side; y++){
      for (var x = 0; x < side; x++){
        var i = (y * side + x) * 4;
        var dx = (x - half) / half, dy = (y - half) / half;
        var rr = dx * dx + dy * dy;
        if (rr > 1){ d[i + 3] = 0; continue; }
        var u = x / side * N, v = y / side * N;
        var a = fld(u + ax, v + ay);
        var b = fld(u * 1.7 + bx, v * 1.7 + by);
        var val = a * 0.62 + b * 0.38;
        val *= 1 - rr * 0.45;                 // fade toward the scope edge
        var band = null;
        for (var k = BANDS.length - 1; k >= 0; k--)
          if (val >= BANDS[k][0]){ band = BANDS[k]; break; }
        if (!band){ d[i + 3] = 0; continue; }
        d[i] = band[1]; d[i + 1] = band[2]; d[i + 2] = band[3];
        d[i + 3] = Math.round(band[4] * 255);
      }
    }
    buf.getContext("2d").putImageData(img, 0, 0);
  }

  function chrome(t){
    var cx = R, cy = R;
    ctx.save();
    ctx.translate(cx, cy);
    // scope ground
    var g = ctx.createRadialGradient(0, 0, 0, 0, 0, R);
    g.addColorStop(0, "rgba(9,32,46,.34)");
    g.addColorStop(1, "rgba(9,32,46,.06)");
    ctx.fillStyle = g;
    ctx.beginPath(); ctx.arc(0, 0, R * 0.97, 0, Math.PI * 2); ctx.fill();
    ctx.restore();

    // echoes, clipped to the scope
    ctx.save();
    ctx.beginPath(); ctx.arc(cx, cy, R * 0.97, 0, Math.PI * 2); ctx.clip();
    ctx.imageSmoothingEnabled = true;
    ctx.drawImage(buf, 0, 0, cv.width, cv.height);
    ctx.restore();

    // range rings, crosshair, ticks
    ctx.save();
    ctx.translate(cx, cy);
    ctx.strokeStyle = "rgba(255,255,255,.30)";
    ctx.lineWidth = Math.max(1, dpr * 0.75);
    for (var k = 1; k <= 4; k++){
      ctx.globalAlpha = k === 4 ? 0.62 : 0.32;
      ctx.beginPath(); ctx.arc(0, 0, R * 0.97 * k / 4, 0, Math.PI * 2); ctx.stroke();
    }
    ctx.globalAlpha = 0.26;
    ctx.beginPath();
    ctx.moveTo(-R * 0.97, 0); ctx.lineTo(R * 0.97, 0);
    ctx.moveTo(0, -R * 0.97); ctx.lineTo(0, R * 0.97);
    ctx.stroke();
    ctx.globalAlpha = 0.5;
    for (var a = 0; a < 360; a += 15){
      var rad = a * Math.PI / 180, o = R * 0.97, inn = o - (a % 45 === 0 ? R * 0.055 : R * 0.028);
      ctx.beginPath();
      ctx.moveTo(Math.cos(rad) * inn, Math.sin(rad) * inn);
      ctx.lineTo(Math.cos(rad) * o, Math.sin(rad) * o);
      ctx.stroke();
    }

    // sweep: a soft trailing wedge, then the arm
    if (!reduced){
      var ang = (t * 0.45) % (Math.PI * 2);
      var wedge = ctx.createConicGradient
        ? ctx.createConicGradient(ang - 1.1, 0, 0) : null;
      if (wedge){
        wedge.addColorStop(0, "rgba(255,255,255,0)");
        wedge.addColorStop(0.30, "rgba(190,225,245,.16)");
        wedge.addColorStop(0.305, "rgba(255,255,255,0)");
        ctx.globalAlpha = 1;
        ctx.fillStyle = wedge;
        ctx.beginPath(); ctx.arc(0, 0, R * 0.97, 0, Math.PI * 2); ctx.fill();
      }
      ctx.globalAlpha = 0.5;
      ctx.strokeStyle = "rgba(214,238,250,.85)";
      ctx.lineWidth = Math.max(1, dpr);
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(Math.cos(ang) * R * 0.97, Math.sin(ang) * R * 0.97);
      ctx.stroke();
    }
    ctx.restore();
  }

  var visible = true, last = 0, t0 = performance.now();
  if ("IntersectionObserver" in window){
    new IntersectionObserver(function(e){ visible = e[0].isIntersecting; },
      { threshold: 0 }).observe(cv);
  }

  function frame(now){
    if (!reduced) requestAnimationFrame(frame);
    if (!visible) return;
    if (now - last < 55) return;            // ~18fps is plenty for weather
    last = now;
    var t = (now - t0) / 1000;
    ctx.clearRect(0, 0, cv.width, cv.height);
    echoes(t);
    chrome(t);
  }

  var ro = window.ResizeObserver ? new ResizeObserver(function(){
    resize(); if (reduced){ ctx.clearRect(0,0,cv.width,cv.height); echoes(8); chrome(8); }
  }) : null;
  resize();
  if (ro) ro.observe(cv); else window.addEventListener("resize", resize);

  if (reduced){ echoes(8); chrome(8); }
  else requestAnimationFrame(frame);
})();
"""

sub("""/* ── scroll reveal. If IntersectionObserver is missing, every section is
   simply marked visible rather than left hidden. ── */""",
    RADAR + """
/* ── scroll reveal. If IntersectionObserver is missing, every section is
   simply marked visible rather than left hidden. ── */""")

io.open(P, "w", encoding="utf-8").write(s)
print("applied %d edits — clouds removed, radar is now an animated scope" % n)

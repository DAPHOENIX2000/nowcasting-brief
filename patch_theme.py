# -*- coding: utf-8 -*-
"""
Fix what the sky restyle left behind, and add a visible theme control.

Three defects, all invisible in the source and obvious on screen:

  1. --coral, --coral-s and --paper2 are referenced twelve times inside the
     SVG figures but no longer defined anywhere. An undefined custom property
     makes the whole declaration invalid, so those fills and strokes fell back
     to the initial value — black, or nothing. That is the "does not blend"
     the figures were showing.

  2. Thirteen SVG font-family attributes still name Fraunces, which the sky
     restyle stopped loading. They were silently falling back to Georgia while
     every heading around them rendered in Archivo.

  3. The page honoured the host's light/dark preference but offered no way to
     choose, so on a device set to one theme the other was unreachable.

The toggle cycles auto -> light -> dark and is applied before first paint, so
there is no flash of the wrong theme on load.
"""
import io
import re
import sys

P = "index.html"
s = io.open(P, encoding="utf-8").read()
n = 0


def sub(old, new, count=1):
    global s, n
    if s.count(old) != count:
        sys.exit("expected %d of %r, found %d" % (count, old[:66], s.count(old)))
    s = s.replace(old, new)
    n += count


# ── 1. stale tokens ─────────────────────────────────────────────────────────
for old, new in [("var(--coral-s)", "var(--sun-soft)"),
                 ("var(--coral)", "var(--mark)"),
                 ("var(--paper2)", "var(--card2)")]:
    c = s.count(old)
    if not c:
        sys.exit("no uses of %s" % old)
    s = s.replace(old, new)
    n += c
    print("  %-18s -> %-18s  %d uses" % (old, new, c))

# ── 2. a font that is no longer loaded ──────────────────────────────────────
c = s.count("Fraunces,Georgia,serif")
s = s.replace("Fraunces,Georgia,serif", "Archivo,Georgia,sans-serif")
n += c
print("  Fraunces           -> Archivo             %d uses" % c)

# ── 3. the control itself ───────────────────────────────────────────────────
sub("""    <div class="langbtns">
      <button id="bEN" class="on" type="button" onclick="setLang('en')">EN</button>
      <button id="bAR" type="button" onclick="setLang('ar')">ع</button>
    </div>""",
    """    <div class="langbtns">
      <button id="bEN" class="on" type="button" onclick="setLang('en')">EN</button>
      <button id="bAR" type="button" onclick="setLang('ar')">ع</button>
    </div>
    <button id="theme" class="themebtn" type="button" aria-label="Switch colour theme"></button>""")

sub(""".langbtns button:focus-visible{outline:2px solid var(--mark); outline-offset:2px}""",
    """.langbtns button:focus-visible{outline:2px solid var(--mark); outline-offset:2px}
.themebtn{
  flex:none; width:34px; height:34px; border-radius:999px; cursor:pointer;
  background:var(--card2); border:1px solid var(--rule); color:var(--muted);
  font-size:15px; line-height:1; display:grid; place-items:center;
  transition:color .18s, background .18s, border-color .18s;
}
.themebtn:hover{color:var(--ink); border-color:var(--rule2)}
.themebtn:focus-visible{outline:2px solid var(--mark); outline-offset:2px}""")

# ── 4. apply before first paint, so the page never flashes the wrong theme ──
sub("""<script>document.documentElement.className="js"</script>""",
    """<script>
document.documentElement.className = "js";
(function () {
  try {
    var t = localStorage.getItem("brief-theme");
    if (t === "light" || t === "dark") document.documentElement.setAttribute("data-theme", t);
  } catch (e) {}
})();
</script>""")

# ── 5. the switcher ─────────────────────────────────────────────────────────
sub("""function buildNav(lang){""",
    """/* auto follows the device; light and dark override it. Stamping data-theme is
   what the token blocks key off, so this needs no other wiring. */
var THEME_ORDER = ["auto", "light", "dark"];
var THEME_GLYPH = { auto: "◐", light: "☀", dark: "☾" };
var THEME_LABEL = { auto: "Theme: follows device", light: "Theme: light", dark: "Theme: dark" };
var theme = "auto";
try { theme = localStorage.getItem("brief-theme") || "auto"; } catch (err) {}

function applyTheme(t){
  var root = document.documentElement;
  if (t === "auto") root.removeAttribute("data-theme");
  else root.setAttribute("data-theme", t);
  var b = document.getElementById("theme");
  if (b){ b.textContent = THEME_GLYPH[t]; b.title = THEME_LABEL[t]; }
  try { localStorage.setItem("brief-theme", t); } catch (err) {}
  // the 3D kernel took its colours from the tokens at start-up
  if (window.k3dRetheme) window.k3dRetheme();
}
applyTheme(theme);
document.getElementById("theme").addEventListener("click", function(){
  theme = THEME_ORDER[(THEME_ORDER.indexOf(theme) + 1) % THEME_ORDER.length];
  applyTheme(theme);
});

function buildNav(lang){""")

# ── 6. let the kernel recolour when the theme changes ───────────────────────
sub("""  function shuffleChannels(){""",
    """  var mode = "ok";   // which palette the cubes are currently showing

  window.k3dRetheme = function(){
    GREEN.set(tok("--dbz18", "#2F8552"));
    RED.set(tok("--dbzhi", "#A32F22"));
    var base = mode === "broken" ? RED : GREEN;
    cubes.forEach(function(c){ c.colTarget.copy(shade(base, c.inten)); });
  };

  function shuffleChannels(){""")

sub("""    say("chan", "good");
  }""", """    mode = "ok";
    say("chan", "good");
  }""")
sub("""    say("spat", "bad");
  }""", """    mode = "broken";
    say("spat", "bad");
  }""")
sub("""    say("reset", "");
  }""", """    mode = "ok";
    say("reset", "");
  }""")

io.open(P, "w", encoding="utf-8").write(s)
print("applied %d edits" % n)

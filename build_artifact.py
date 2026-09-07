# -*- coding: utf-8 -*-
"""
Derive the artifact version from index.html so the two copies never drift.

The Artifact host supplies its own <!doctype>/<html>/<head>/<body> skeleton, so
this strips ours and keeps <title> + <style> + the body's inner content. It also
adds an early language script: the standalone file carries class="lang-en" on
<body>, but the artifact's <body> is the host's, so without this both languages
would flash on screen before the main script runs.
"""
import io
import re
import sys

src = io.open("index.html", encoding="utf-8").read()

head = re.search(r"(<title>.*?</style>)", src, re.S)
body = re.search(r"<body[^>]*>(.*)</body>", src, re.S)
if not head or not body:
    sys.exit("could not locate head or body")

# A name, not a caption - this is what shows in the artifact gallery.
head_html = head.group(1).replace(
    "<title>Nowcasting PEFT — Project Brief</title>",
    "<title>Nowcasting PEFT Brief</title>")

EARLY = '''
<script>
/* Set the language class before paint. The host owns the body element, so the
   class the standalone file hard-codes onto it is not present here, and both
   languages would show for a frame. setLang() below re-applies this harmlessly. */
(function(){
  var l = "en";
  try { l = localStorage.getItem("brief-lang") || "en"; } catch (e) {}
  document.body.className = "lang-" + l;
  document.documentElement.dir = (l === "ar") ? "rtl" : "ltr";
})();
</script>
'''

out = head_html + "\n" + EARLY + "\n" + body.group(1).strip() + "\n"

for bad in ("<!doctype", "<html", "</html>", "<head>", "<body"):
    if bad in out.lower():
        sys.exit("wrapper tag leaked into artifact output: " + bad)

io.open("artifact.html", "w", encoding="utf-8").write(out)
print("wrote artifact.html  (%d chars, %d sections)"
      % (len(out), out.count('<section id=')))

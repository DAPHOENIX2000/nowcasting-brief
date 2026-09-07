# -*- coding: utf-8 -*-
"""
Move the new section 09 in front of section 10, and resync every section
comment with the eyebrow number inside it.

The insert anchored on an HTML comment that the renumber pass had not
touched, so the block landed one section too late: 08, 10, 09, 11.
The comments are cosmetic but they were what made the mistake possible,
so they get regenerated from the eyebrow rather than maintained by hand.
"""
import io
import re
import sys

P = "index.html"
s = io.open(P, encoding="utf-8").read()

BLOCK = re.compile(
    r'\n<!-- ═+ \d+ ═+ -->\n<section id="s9" class="rv">.*?\n</section>\n',
    re.S)
m = BLOCK.search(s)
if not m:
    sys.exit("could not isolate the s9 block")
block = m.group(0)
s = s[:m.start()] + s[m.end():]

tgt = re.search(r'\n<!-- ═+ \d+ ═+ -->\n<section id="s10" class="rv">', s)
if not tgt:
    sys.exit("could not find section s10")
s = s[:tgt.start()] + block.rstrip("\n") + s[tgt.start():]

# resync each comment to the eyebrow number of the section it introduces
def resync(mm):
    return '<!-- %s %s %s -->\n<section id="%s"%s>\n  <div class="eyebrow"><b>%s</b>' % (
        "═" * 26, mm.group(3), "═" * 26, mm.group(1), mm.group(2), mm.group(3))

s, n = re.subn(
    r'<!-- ═+ \d+ ═+ -->\n<section id="(s\d+)"([^>]*)>\n  <div class="eyebrow"><b>(\d+)</b>',
    resync, s)

io.open(P, "w", encoding="utf-8").write(s)
print("moved section 09 into place; resynced %d section comments" % n)

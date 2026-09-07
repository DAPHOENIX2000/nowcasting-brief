# -*- coding: utf-8 -*-
"""
Mark up the elements that motion attaches to.

  section id=s2..s15  ->  class="rv"   (scroll reveal; hero and s1 are never
                                        revealed, so the first frame is complete)
  rect rx="4"         ->  class="gb"   (the vertical data bars in the two charts;
                                        every structural box uses a different rx,
                                        so this selector is exact)
"""
import io
import re
import sys

P = "index.html"
s = io.open(P, encoding="utf-8").read()

# --- reveal targets: every section except the hero and section 01
n_rv = 0
for i in range(2, 16):
    old = '<section id="s%d">' % i
    new = '<section id="s%d" class="rv">' % i
    if s.count(old) == 1:
        s = s.replace(old, new)
        n_rv += 1
    else:
        sys.exit("section s%d not found exactly once" % i)

# the dashed threads travel with the section that follows them
s = s.replace('<svg class="thread"', '<svg class="thread rv"')
n_thread = s.count('thread rv')

# --- data bars. rx="4" is used only by chart bars.
bars = re.findall(r'<rect [^>]*rx="4"', s)
s = re.sub(r'(<rect )([^>]*rx="4")', r'\1class="gb" \2', s)

io.open(P, "w", encoding="utf-8").write(s)
print("sections revealed : %d" % n_rv)
print("threads revealed  : %d" % n_thread)
print("bars marked       : %d" % len(bars))
if len(bars) != 11:
    print("  WARNING expected 11 bars (4 in the decay chart, 7 in the CSI chart)")

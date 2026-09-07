# -*- coding: utf-8 -*-
"""
The body text of the brief is bilingual, but every section kicker and <h2> was
written in English only, so Arabic mode still showed English headings.

This splits each one into an .en / .ar pair. Run once; it is idempotent in the
sense that a second run reports every patch as a MISS rather than doubling up.
"""
import io
import sys

P = "index.html"
s = io.open(P, encoding="utf-8").read()
hits, misses = 0, []

# (kicker_en, kicker_ar, h2_inner_en, h2_inner_ar)
ROWS = [
    ("01 — The core", "01 — الجوهر",
     'The five sentences <span class="badge b-must">must know</span>',
     'الجمل الخمس <span class="badge b-must">احفظها</span>'),
    ("02 — The problem", "02 — المشكلة",
     "Why a model stops working when it crosses a border",
     "لماذا يتوقف النموذج عن العمل حين يعبر الحدود"),
    ("03 — The data", "03 — البيانات",
     'Four radar datasets <span class="badge b-ctx">context</span>',
     'أربع مجموعات بيانات رادار <span class="badge b-ctx">سياق</span>'),
    ("04 — The starting point", "04 — نقطة الانطلاق",
     "AlphaPre — the model you freeze",
     "AlphaPre — النموذج الذي تُجمّده"),
    ("05 — The idea", "05 — الفكرة",
     'What "parameter-efficient fine-tuning" actually means',
     "ما معنى «الضبط الدقيق كفء المعاملات» فعليًا"),
    ("06 — The technical core", "06 — الجوهر التقني",
     'The one picture that carries your whole argument <span class="badge b-must">must know</span>',
     'الصورة الواحدة التي تحمل حجّتك كلها <span class="badge b-must">احفظها</span>'),
    ("07 — Your contribution", "07 — إسهامك",
     'Your two methods <span class="badge b-must">must know</span>',
     'طريقتاك <span class="badge b-must">احفظهما</span>'),
    ("08 — Defending novelty", "08 — الدفاع عن الابتكار",
     'Where the innovation is <span class="badge b-must">must know</span>',
     'أين يكمن الابتكار <span class="badge b-must">احفظه</span>'),
    ("09 — Your evidence", "09 — دليلك",
     'What you have already measured <span class="badge b-meas">measured</span>',
     'ما قِستَه بالفعل <span class="badge b-meas">مقيس</span>'),
    ("10 — Honesty", "10 — الأمانة العلمية",
     'What your results do <u>not</u> prove <span class="badge b-care">be careful</span>',
     'ما <u>لا</u> تُثبته نتائجك <span class="badge b-care">انتبه</span>'),
    ("11 — The plan", "11 — الخطة",
     "What still has to be run",
     "ما تبقّى من تجارب"),
    ("12 — The defence", "12 — المناقشة",
     'How to present, and how to sound like you know it <span class="badge b-must">must know</span>',
     'كيف تعرض، وكيف تبدو متمكنًا <span class="badge b-must">احفظه</span>'),
    ("13 — Reference", "13 — مرجع",
     "The papers you are standing on",
     "الأوراق البحثية التي تقف عليها"),
    ("14 — Reference", "14 — مصطلحات",
     "The words, briefly",
     "المصطلحات باختصار"),
    ("15 — Where things stand", "15 — أين نحن الآن",
     "Status and what is next",
     "الحالة والخطوات التالية"),
]


def sub(old, new):
    global s, hits
    if s.count(old) == 1:
        s = s.replace(old, new)
        hits += 1
    else:
        misses.append((s.count(old), old.replace("\n", " ")[:64]))


for k_en, k_ar, h_en, h_ar in ROWS:
    old = '<div class="kicker">%s</div>' % k_en
    new = ('<div class="kicker en">%s</div>\n  <div class="kicker ar">%s</div>'
           % (k_en, k_ar))
    sub(old, new)

    old = "<h2>%s</h2>" % h_en
    new = '<h2 class="en">%s</h2>\n  <h2 class="ar">%s</h2>' % (h_en, h_ar)
    sub(old, new)

# the hero tag is the one remaining English-only chrome element
sub('<span class="hero-tag">Master\'s thesis · HITSZ · defence brief</span>',
    '<span class="hero-tag en">Master\'s thesis · HITSZ · defence brief</span>'
    '<span class="hero-tag ar">أطروحة ماجستير · HITSZ · ملخّص المناقشة</span>')

io.open(P, "w", encoding="utf-8").write(s)
print("applied %d patches" % hits)
for c, m in misses:
    print("  MISS (found %d) %s" % (c, m))
sys.exit(1 if misses else 0)

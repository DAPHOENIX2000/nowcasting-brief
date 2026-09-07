# -*- coding: utf-8 -*-
"""
Add "What is new, exactly" as section 09, directly after the novelty defence
it belongs with, and renumber 09-15 up to 10-16.

Renumbering has to be done back-to-front or s9->s10 would collide with the
existing s10. Two in-text cross-references point at the old numbering and are
updated with it.
"""
import io
import sys

P = "index.html"
s = io.open(P, encoding="utf-8").read()

# ── 1. renumber existing sections 15..9 -> 16..10, highest first
for old in range(15, 8, -1):
    new = old + 1
    for a, b in [('<section id="s%d" class="rv">' % old, '<section id="s%d" class="rv">' % new),
                 ('<b>%02d</b>' % old, '<b>%02d</b>' % new),
                 ('["s%d",' % old, '["s%d",' % new)]:
        if s.count(a) != 1:
            sys.exit("renumber anchor not unique (%d): %s" % (s.count(a), a))
        s = s.replace(a, b)
    # the nav labels carry the number too
    for a, b in [('"%02d · ' % old, '"%02d · ' % new)]:
        s = s.replace(a, b)

# ── 2. in-text cross-references that moved
s = s.replace("<i>(Section 09.)</i>", "<i>(Section 10.)</i>")
s = s.replace("<i>(القسم 09.)</i>", "<i>(القسم 10.)</i>")

# ── 3. the new section, inserted after section 08
NEW = '''
<!-- ══════════════════════════ 09 ══════════════════════════ -->
<section id="s9" class="rv">
  <div class="eyebrow"><b>09</b> <span class="en">The gap</span><span class="ar">الفجوة</span></div>
  <h2 class="en">What is new, exactly <span class="pen"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 17c4-7 12-11 18-12"/><path d="M15 3.6l6 1.4-1.6 5.6"/></svg> memorise</span></h2>
  <h2 class="ar">ما الجديد بالضبط <span class="pen"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 17c4-7 12-11 18-12"/><path d="M15 3.6l6 1.4-1.6 5.6"/></svg> احفظه</span></h2>

  <p class="lead en"><b>Everyone before you trained and tested on one country&#39;s radar at a time.</b> SEVIR, MeteoNet, Shanghai and CIKM are used as four separate leaderboards. Nobody asked the obvious practical question: can you take the model that already works in America and make it work in France without collecting a French training set?</p>
  <p class="lead ar"><b>كل من سبقك درّب واختبر على رادار دولة واحدة في كل مرة.</b> فمجموعات SEVIR وMeteoNet وشنغهاي وCIKM تُستخدم كأربعة تصنيفات منفصلة. ولم يسأل أحد السؤال العملي البديهي: هل يمكن أخذ النموذج الذي يعمل في أمريكا وجعله يعمل في فرنسا دون جمع بيانات تدريب فرنسية؟</p>

  <h3 class="en">What existed, and what you add</h3>
  <h3 class="ar">ما كان موجودًا، وما تضيفه أنت</h3>

  <div class="tw en"><table>
    <tr><th>Already done, by others</th><th>What you add</th></tr>
    <tr><td><b>AlphaPre</b> trains a nowcasting model on SEVIR</td><td>You <b>freeze it</b> and move it to a different country</td></tr>
    <tr><td><b>DiffCast</b> establishes the four datasets, 5→20 at 128×128</td><td>You use that protocol for <b>transfer between them</b>, which it was never used for</td></tr>
    <tr class="hi"><td><b>S²FT</b> does PEFT by permuting rows and columns — <b>linear layers only</b></td><td>You extend it to <b>convolutional kernels</b>, which forces the question of which axes may be permuted</td></tr>
    <tr><td><b>LoRA / FourierFT</b> — general-purpose PEFT recipes</td><td>You design around <b>measured properties of this model</b>, not a general recipe</td></tr>
  </table></div>
  <div class="tw ar"><table>
    <tr><th>ما أنجزه آخرون بالفعل</th><th>ما تضيفه أنت</th></tr>
    <tr><td><b>AlphaPre</b> يدرّب نموذج تنبؤ آني على SEVIR</td><td>أنت <b>تُجمّده</b> وتنقله إلى دولة أخرى</td></tr>
    <tr><td><b>DiffCast</b> ترسي المجموعات الأربع وبروتوكول 5→20 بدقة 128×128</td><td>أنت تستخدم البروتوكول من أجل <b>النقل بينها</b>، وهو ما لم يُستخدم له قط</td></tr>
    <tr class="hi"><td><b>S²FT</b> تنجز PEFT بإعادة ترتيب الصفوف والأعمدة — <b>للطبقات الخطية فقط</b></td><td>أنت تُوسّعها إلى <b>نوى الالتفاف</b>، وهو ما يفرض سؤال أي المحاور يجوز ترتيبها</td></tr>
    <tr><td><b>LoRA / FourierFT</b> — وصفات PEFT عامة الغرض</td><td>أنت تُصمّم حول <b>خصائص مقيسة لهذا النموذج</b>، لا وصفة عامة</td></tr>
  </table></div>

  <h3 class="en">The three things that are actually yours</h3>
  <h3 class="ar">الأشياء الثلاثة التي هي حقًا لك</h3>
  <div class="grid g3">
    <div class="step"><div class="no">Yours 01</div>
      <h4 class="en">The problem framing</h4><h4 class="ar">صياغة المشكلة</h4>
      <p class="en">Cross-dataset, few-shot nowcasting. In the literature you surveyed, all four datasets are trained and evaluated separately — no transfer, no few-shot regime. <b>That gap is the project.</b></p>
      <p class="ar">تنبؤ آني عابر للمجموعات وبأمثلة قليلة. في الأدبيات التي مسحتَها، تُدرَّب المجموعات الأربع وتُقيَّم منفصلة — بلا نقل ولا نظام أمثلة قليلة. <b>هذه الفجوة هي المشروع.</b></p></div>
    <div class="step hot"><div class="no">Yours 02</div>
      <h4 class="en">The convolutional extension of S²FT</h4><h4 class="ar">التوسعة الالتفافية لـ S²FT</h4>
      <p class="en">Your hardest technical contribution. Shuffling is only legal on an axis whose order is meaningless — and a kernel has two of each. The paper&#39;s second author confirmed he has never tried it on convolutions, and there is <b>no public implementation</b>. You derive it from the paper, not from code.</p>
      <p class="ar">أصعب إسهاماتك التقنية. إعادة الترتيب مشروعة فقط على محور لا معنى لترتيبه — وللنواة محوران من كل نوع. وقد أكّد المؤلف الثاني للورقة أنه لم يجرّبها على الالتفافات قط، ولا يوجد <b>أي تنفيذ عام</b>. أنت تشتقّها من الورقة لا من كود.</p></div>
    <div class="step"><div class="no">Yours 03</div>
      <h4 class="en">The controlled comparison</h4><h4 class="ar">المقارنة المضبوطة</h4>
      <p class="en">Two methods identical in every respect except <b>the space the update is written in</b> — original parameters against sparse spectrum — measured as target data shrink. That comparison <i>is</i> the thesis.</p>
      <p class="ar">طريقتان متطابقتان في كل شيء إلا <b>الفضاء الذي يُكتب فيه التحديث</b> — المعاملات الأصلية مقابل الطيف المتناثر — مقيستان مع تناقص بيانات الهدف. تلك المقارنة <i>هي</i> الأطروحة.</p></div>
  </div>

  <div class="note warn">
    <h4 class="en">What is NOT new — say this before they do <span class="pen grey">careful</span></h4>
    <h4 class="ar">ما ليس جديدًا — قله قبل أن يقولوه <span class="pen grey">انتبه</span></h4>
    <ul class="en">
      <li><b>PEFT itself is not yours</b>, and neither is <b>LoRA on convolutions</b> — conv-LoRA variants already exist. Your Research Content One is a baseline and a controlled counterpart, <b>not a novelty claim</b>.</li>
      <li><b>The amplitude/phase decomposition is AlphaPre&#39;s</b>, not yours. What is yours is using it to decide where the parameter budget goes.</li>
      <li>The datasets, the protocol and the base model are all inherited.</li>
    </ul>
    <ul class="ar">
      <li><b>PEFT نفسها ليست لك</b>، ولا <b>LoRA على الالتفافات</b> — فنسخ conv-LoRA موجودة بالفعل. محتوى بحثك الأول خط أساس ونظير مضبوط، <b>لا ادّعاء ابتكار</b>.</li>
      <li><b>تفكيك السعة والطور من AlphaPre</b> لا منك. ما هو لك هو استخدامه لتحديد أين تُنفَق ميزانية المعاملات.</li>
      <li>المجموعات والبروتوكول والنموذج الأساس، كلها موروثة.</li>
    </ul>
    <p class="en">Claiming any of those would get you caught. Volunteering them makes the real claims land harder.</p>
    <p class="ar">ادّعاء أيٍّ منها سيوقعك. أما التطوّع بذكرها فيجعل ادّعاءاتك الحقيقية أوقع.</p>
  </div>

  <div class="say">
    <span class="who en">The sentence for the defence</span>
    <span class="who ar">الجملة المخصّصة للمناقشة</span>
    <span class="q en">“Precipitation nowcasting models are trained and evaluated one country at a time. I take a frozen model from one country and adapt it to another using under 0.1% of its weights — and to do that I had to extend a spectral PEFT method, written for linear layers, to convolutional kernels, which nobody has done. Every design decision comes from a property of this model that I measured.”</span>
    <span class="q ar">«نماذج التنبؤ الآني بالأمطار تُدرَّب وتُقيَّم على دولة واحدة في كل مرة. أنا آخذ نموذجًا مُجمَّدًا من دولة وأُكيّفه على أخرى باستخدام أقل من 0.1% من أوزانه — ولفعل ذلك كان عليّ توسيع طريقة PEFT طيفية، كُتبت للطبقات الخطية، إلى نوى الالتفاف، وهو ما لم يفعله أحد. وكل قرار تصميمي نابع من خاصية في هذا النموذج قِستُها بنفسي.»</span>
  </div>
</section>
'''

anchor = "\n<!-- ══════════════════════════ 10 ══════════════════════════ -->"
if s.count(anchor) != 1:
    sys.exit("insert anchor not unique (%d)" % s.count(anchor))
s = s.replace(anchor, NEW + anchor)

# ── 4. nav entry
navanchor = '  ["s10","10 · What you measured","10 · ما قِستَه"],'
if s.count(navanchor) != 1:
    sys.exit("nav anchor not unique (%d)" % s.count(navanchor))
s = s.replace(navanchor,
              '  ["s9","09 · What is new, exactly","09 · ما الجديد بالضبط"],\n' + navanchor)

io.open(P, "w", encoding="utf-8").write(s)
print("added section 09; renumbered old 09-15 to 10-16")

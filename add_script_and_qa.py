# -*- coding: utf-8 -*-
"""
Add two sections to the brief:

  14  The script       — the spoken notes from the defence deck, so the words
                         to say live in the same place as the understanding
                         behind them.
  15  Questions        — what the committee is likely to ask, with an answer
                         for each, grouped by what the question is really
                         testing.

Old sections 14-16 shift to 16-18. No cross-reference in the document points at
those numbers (only 01, 02, 06, 08 and 10 are referenced), so nothing else has
to change.
"""
import io
import re
import sys

P = "index.html"
s = io.open(P, encoding="utf-8").read()

# ── renumber 16,15,14 -> 18,17,16, highest first so ids never collide ───────
for old in (16, 15, 14):
    new = old + 2
    for a, b in [('<section id="s%d" class="rv">' % old, '<section id="s%d" class="rv">' % new),
                 ('<b>%02d</b>' % old, '<b>%02d</b>' % new),
                 ('["s%d",' % old, '["s%d",' % new)]:
        if s.count(a) != 1:
            sys.exit("renumber anchor not unique (%d): %s" % (s.count(a), a))
        s = s.replace(a, b)
    s = s.replace('"%02d · ' % old, '"%02d · ' % new)


def block(num, title_en, title_ar, kicker_en, kicker_ar, body):
    return '''
<!-- ══════════════════════════ %s ══════════════════════════ -->
<section id="s%d" class="rv">
  <div class="eyebrow"><b>%s</b> <span class="en">%s</span><span class="ar">%s</span></div>
  <h2 class="en">%s</h2>
  <h2 class="ar">%s</h2>
%s
</section>
''' % (num, int(num), num, kicker_en, kicker_ar, title_en, title_ar, body)


# ══════════════════════════════════════════════════ 14  THE SCRIPT
SLIDES = [
    ("01", "Title",
     "Good morning. My name is Yassine Achouak. My proposal is on cross-dataset generalization for precipitation nowcasting, using parameter-efficient fine-tuning. My supervisor is Professor Zhang Baoquan. Thank you for your time today.",
     "صباح الخير. اسمي ياسين أشواك. مقترحي عن التعميم عبر مجموعات البيانات في التنبؤ الآني بالأمطار، باستخدام الضبط الدقيق كفء المعاملات. مشرفي هو الأستاذ الدكتور تشانغ باوتشيوان. شكرًا لوقتكم اليوم."),
    ("02", "Contents",
     "There are eight parts to this presentation. I will spend most of the time on part four, which is the key technical problem, and part five, which is the innovation.",
     "يتكوّن هذا العرض من ثمانية أجزاء. وسأقضي معظم الوقت في الجزء الرابع، وهو المشكلة التقنية الجوهرية، والجزء الخامس، وهو الابتكار."),
    ("03", "Background",
     "A rain warning is only useful if it arrives in time. Nowcasting means predicting rainfall one to two hours ahead, directly from radar images. The standard task is five frames in, twenty frames out.<br><br>The difficulty is that these models do not cross borders. On the radar network it was trained on, this model keeps sixty-one point eight percent of its opening skill after one hundred minutes. On a network it has never seen, it keeps only thirty-three point eight percent. The decay is one point seven times faster.<br><br>So the penalty is not a fixed offset. It compounds with lead time, which means the useful forecast horizon itself becomes shorter.<br><br>And collecting a full training archive for every new country is not practical. So the model has to be adapted from very little target data. That is the problem this project addresses.",
     "التحذير من المطر لا يفيد إلا إذا وصل في وقته. والتنبؤ الآني يعني توقّع هطول المطر قبل ساعة إلى ساعتين، مباشرةً من صور الرادار. والمهمة القياسية هي خمس لقطات دخلًا وعشرون خرجًا.<br><br>والصعوبة أن هذه النماذج لا تعبر الحدود. فعلى شبكة الرادار التي دُرِّب عليها، يحتفظ هذا النموذج بواحد وستين فاصلة ثمانية بالمئة من مهارته الأولى بعد مئة دقيقة. وعلى شبكة لم يرها قط، يحتفظ بثلاثة وثلاثين فاصلة ثمانية بالمئة فقط. أي أن التدهور أسرع بمقدار واحد فاصلة سبعة مرة.<br><br>إذن العقوبة ليست فارقًا ثابتًا، بل تتراكم مع الزمن، ما يعني أن أفق التنبؤ المفيد نفسه يقصر.<br><br>وجمع أرشيف تدريب كامل لكل دولة جديدة أمر غير عملي. لذا يجب تكييف النموذج انطلاقًا من بيانات هدف قليلة جدًا. وهذه هي المشكلة التي يعالجها هذا المشروع."),
    ("04", "Related work",
     "There are four pieces of prior work that matter here.<br><br>AlphaPre gives me the model and a checkpoint trained on SEVIR, but it never transfers between archives. DiffCast establishes the four datasets and the five-to-twenty protocol that I adopt, but it trains each dataset separately. S-squared-F-T gives me the adaptation mechanism, but it is defined for linear layers only. And LoRA and FourierFT are general recipes, not designed for this class of model.<br><br>So the gap is this. No study trains on one national radar network and adapts to another under a restricted target-data budget. That gap is my project.",
     "هناك أربعة أعمال سابقة مهمة هنا.<br><br>يمنحني AlphaPre النموذج ونقطة تفتيش مدرَّبة على SEVIR، لكنه لا ينتقل بين المجموعات أبدًا. ويُرسي DiffCast المجموعات الأربع وبروتوكول الخمسة إلى العشرين الذي أتبنّاه، لكنه يدرّب كل مجموعة على حدة. ويمنحني S²FT آلية التكييف، لكنها معرَّفة للطبقات الخطية فقط. أما LoRA وFourierFT فوصفتان عامتان غير مصمّمتين لهذا النوع من النماذج.<br><br>إذن الفجوة هي: لا توجد دراسة تدرّب على شبكة رادار وطنية وتتكيّف مع أخرى في ظل ميزانية بيانات هدف محدودة. وهذه الفجوة هي مشروعي."),
    ("05", "Research content",
     "This diagram shows the whole structure of the research.<br><br>At the top is the problem: a model trained on one country's radar degrades on another, and target data are scarce.<br><br>Below that is the base model, AlphaPre, with eighty-nine million parameters. I do not train it. I download it and I freeze it.<br><br>Underneath are four properties of that model that I measured, and these drive every design decision below them.<br><br>In the middle are the two research contents. The first adapts in the original parameter space. The second adapts in the sparse spectrum domain. Between them you can see the phrase identical except the representation, and that is the important part. The same frozen model, the same axes touched, the same merge at the end. Only the description of the change differs, and that is what makes the comparison fair.<br><br>Below that is the supporting work, which is the benchmark and the comparison protocol. I mark it as apparatus rather than as a contribution, so that it is not mistaken for one.<br><br>And at the bottom are the expected outcomes.",
     "يوضّح هذا المخطط بنية البحث كاملة.<br><br>في الأعلى المشكلة: نموذج مدرَّب على رادار دولة يتدهور على أخرى، وبيانات الهدف شحيحة.<br><br>وتحته النموذج الأساس، AlphaPre، بتسعة وثمانين مليون معامل. أنا لا أدرّبه، بل أُنزّله وأُجمّده.<br><br>وتحته أربع خصائص لهذا النموذج قِستُها بنفسي، وهي تقود كل قرار تصميمي أدناه.<br><br>وفي الوسط محتويا البحث. الأول يتكيّف في فضاء المعاملات الأصلي، والثاني في مجال الطيف المتناثر. وبينهما ترون عبارة «متطابقان إلا في التمثيل»، وهذا هو الجزء المهم. النموذج المُجمَّد نفسه، والمحاور نفسها، والدمج النهائي نفسه. الوصف وحده هو ما يختلف، وهذا ما يجعل المقارنة عادلة.<br><br>وتحته العمل المساند، وهو المرجعية وبروتوكول المقارنة. وأصنّفه كأداة لا كإسهام، حتى لا يُفهم خطأً على أنه إسهام.<br><br>وفي الأسفل النتائج المتوقعة."),
    ("06", "Research content one",
     "This is the first method, in four steps.<br><br>First, the frozen kernel. It has four axes: output channels, input channels, and two spatial axes, which are the height and the width of the window.<br><br>Second, I slice it by spatial position. A three-by-three kernel becomes nine matrices, each one of size output channels by input channels.<br><br>Third, the change to each slice is constrained to low rank. This is the only part that is trainable. Everything else stays frozen.<br><br>And fourth, at inference the change merges back into the frozen kernel, so there is no added latency when the model makes a prediction.<br><br>The box underneath shows two design choices that I resolve by experiment rather than by assumption. Whether the factors are shared across the nine positions or learned independently at each one, and whether the rank is allocated uniformly or by pathway.<br><br>I should be clear that this method is closely related to existing low-rank adaptation. It is here as a controlled counterpart and as a strong baseline. My novelty claim is the second method, and the comparison between the two.",
     "هذه هي الطريقة الأولى، في أربع خطوات.<br><br>أولًا، النواة المُجمَّدة. ولها أربعة محاور: قنوات الخرج، وقنوات الدخل، ومحوران مكانيان هما ارتفاع النافذة وعرضها.<br><br>ثانيًا، أُقطّعها حسب الموضع المكاني. فتصبح النواة ثلاثة في ثلاثة تسع مصفوفات، حجم كل منها قنوات الخرج في قنوات الدخل.<br><br>ثالثًا، يُقيَّد التغيير في كل شريحة برتبة منخفضة. وهذا هو الجزء الوحيد القابل للتدريب، وكل ما عداه يبقى مُجمَّدًا.<br><br>ورابعًا، عند الاستدلال يُدمج التغيير في النواة المُجمَّدة، فلا يوجد أي تأخير إضافي عند التنبؤ.<br><br>والصندوق أدناه يُظهر قرارين تصميميين أحسمهما بالتجربة لا بالافتراض: هل تُشترك العوامل عبر المواضع التسعة أم تُتعلَّم مستقلة عند كل موضع، وهل تُوزَّع الرتبة بالتساوي أم حسب المسار.<br><br>وأودّ التوضيح أن هذه الطريقة وثيقة الصلة بالتكييف منخفض الرتبة الموجود. وهي هنا كنظير مضبوط وخط أساس قوي. أما ادّعائي بالابتكار فهو الطريقة الثانية والمقارنة بينهما."),
    ("07", "Research content two",
     "This is the second method, in five steps.<br><br>First, the frozen kernel again, sliced by position.<br><br>Second, a short fine-tune gives a coarse estimate of the change. It is used only to decide an ordering, and then it is discarded. It is not the answer.<br><br>Third, that ordering is a permutation of the channels, found by a nearest-neighbour search. And it is shared across all nine spatial positions.<br><br>Fourth, once the channels are reordered, the slice is smooth. Smooth things are sparse in the spectral domain, so I keep only a small number of coefficients, and those are what I train.<br><br>And fifth, I invert the transform, un-permute, and add the result back into the kernel.<br><br>The panel in the middle explains why this is allowed. Channel order carries no meaning, so it may be reordered. But the same reordering has to apply at every spatial position. Otherwise a given channel would no longer denote the same feature map, and the kernel would stop being a kernel.<br><br>At the bottom are four candidate designs that I will compare. Design D is the naive approach of flattening the kernel into a matrix. I keep it as a control, and I expect it to fail. If it fails while the channel-only design works, that is evidence that spatial correlation is the obstacle, rather than just my assertion that it is.",
     "هذه هي الطريقة الثانية، في خمس خطوات.<br><br>أولًا، النواة المُجمَّدة مجددًا، مُقطَّعة حسب الموضع.<br><br>ثانيًا، ضبط دقيق قصير يعطي تقديرًا خشنًا للتغيير. ويُستخدم فقط لتحديد ترتيب، ثم يُهمَل. فهو ليس الجواب.<br><br>ثالثًا، ذلك الترتيب هو إعادة ترتيب للقنوات، تُوجَد ببحث الجار الأقرب. وهي مشتركة عبر المواضع المكانية التسعة جميعها.<br><br>رابعًا، بعد إعادة ترتيب القنوات تصبح الشريحة ناعمة. والأشياء الناعمة متناثرة في المجال الطيفي، فأحتفظ بعدد صغير من المعاملات فقط، وهي ما أُدرّبه.<br><br>وخامسًا، أعكس التحويل، وأُلغي إعادة الترتيب، وأضيف الناتج إلى النواة.<br><br>واللوحة في الوسط تشرح لماذا هذا مسموح. ترتيب القنوات لا يحمل معنى، فيجوز إعادة ترتيبه. لكن إعادة الترتيب نفسها يجب أن تُطبَّق عند كل موضع مكاني، وإلا لم تعد القناة المعيّنة تدل على خريطة السمات نفسها، وتوقّفت النواة عن كونها نواة.<br><br>وفي الأسفل أربعة تصاميم مرشَّحة سأقارنها. التصميم D هو المقاربة الساذجة بتسطيح النواة إلى مصفوفة. أُبقيه كضابط، وأتوقّع فشله. فإن فشل بينما ينجح التصميم القنوي فقط، فذلك دليل على أن الارتباط المكاني هو العائق، لا مجرّد ادّعاء مني."),
    ("08", "Key problem",
     "This is the central technical problem, so I would like to take it slowly.<br><br>The method I am extending works by permutation. And permutation is only legitimate on an axis whose order carries no meaning.<br><br>A convolution kernel has four axes. The first two are channel indices. Channel number seven has no special meaning. It is a label, like a name on a locker. If I renumber all of them consistently, nothing breaks. So those two axes may be permuted.<br><br>The last two axes are positions inside the window. Position zero-zero genuinely sits next to position zero-one. They look at neighbouring pixels. If I shuffle those, the filter stops detecting what it was detecting. So those two may not be permuted.<br><br>There is a second reason to work on the channels. Inside a kernel, channel entries outnumber spatial entries by roughly forty-nine thousand nine hundred to one. So restricting adaptation to the channel axes is not a preference. It is arithmetic. There is nothing to compress in nine numbers.<br><br>That is why the method cannot simply be reshaped onto a convolution, and why the extension has to be derived rather than ported.",
     "هذه هي المشكلة التقنية الجوهرية، ولذلك أودّ أن أتناولها ببطء.<br><br>الطريقة التي أُوسّعها تعمل بإعادة الترتيب. وإعادة الترتيب مشروعة فقط على محور لا يحمل ترتيبُه أي معنى.<br><br>نواة الالتفاف لها أربعة محاور. الأولان مؤشّرا قنوات. والقناة رقم سبعة لا تحمل معنى خاصًا؛ إنها تسمية، كاسم على خزانة. فإن أعدتُ ترقيمها جميعًا باتساق لا ينكسر شيء. إذن هذان المحوران يجوز إعادة ترتيبهما.<br><br>والمحوران الأخيران موضعان داخل النافذة. فالموضع صفر-صفر يجاور فعلًا الموضع صفر-واحد، وهما ينظران إلى بكسلات متجاورة. فإن خلطتُهما توقّف المُرشِّح عن كشف ما كان يكشفه. إذن هذان لا يجوز إعادة ترتيبهما.<br><br>وهناك سبب ثانٍ للعمل على القنوات. فداخل النواة، تفوق مُدخلات القنوات المُدخلات المكانية بنحو تسعة وأربعين ألفًا وتسعمئة إلى واحد. لذا فحصر التكييف في محاور القنوات ليس تفضيلًا، بل حساب. فليس في تسعة أرقام ما يُضغط.<br><br>ولهذا لا يمكن ببساطة إعادة تشكيل الطريقة على الالتفاف، ولهذا يجب اشتقاق التوسعة لا نقلها."),
    ("09", "Innovation",
     "I make three claims, and I want to be equally clear about what I am not claiming.<br><br>The first claim is about the problem itself. The four archives are used as four separate benchmarks. No study trains on one national radar network and adapts to another under a restricted budget. That question is open.<br><br>The second is the technical contribution. A kernel has two permutable axes and two that are not, so the method is not transferable by reshaping. There is no public implementation of it in any form, and an author of the paper has confirmed that it has never been attempted on convolutions. I derive it from the publication.<br><br>The third is the form of the comparison. Both methods share the frozen model, the restriction to the channel axes, the merge at inference, and the parameter budget. Only the representation differs, so the comparison isolates the representation.<br><br>Now, what I am not claiming. I am not claiming parameter-efficient fine-tuning itself, and I am not claiming low-rank adaptation of convolutions, because several such methods already exist. The amplitude and phase decomposition is AlphaPre's, not mine. What is mine is using it to decide where the budget should go. And the datasets, the protocol and the source checkpoint are all inherited.<br><br>I am not proposing a general-purpose method. Every design decision I make comes from a property of this model that I measured.",
     "أقدّم ثلاثة ادّعاءات، وأودّ أن أكون واضحًا بالقدر نفسه بشأن ما لا أدّعيه.<br><br>الادّعاء الأول عن المشكلة نفسها. فالمجموعات الأربع تُستخدم كأربع مرجعيات منفصلة. ولا توجد دراسة تدرّب على شبكة رادار وطنية وتتكيّف مع أخرى في ظل ميزانية محدودة. وهذا السؤال مفتوح.<br><br>والثاني هو الإسهام التقني. فللنواة محوران يجوز إعادة ترتيبهما ومحوران لا يجوز، لذا فالطريقة غير قابلة للنقل بإعادة التشكيل. ولا يوجد لها أي تنفيذ عام بأي صورة، وقد أكّد أحد مؤلفي الورقة أنها لم تُجرَّب قط على الالتفافات. وأنا أشتقّها من المنشور.<br><br>والثالث هو شكل المقارنة. فكلتا الطريقتين تشتركان في النموذج المُجمَّد، والحصر في محاور القنوات، والدمج عند الاستدلال، وميزانية المعاملات. والتمثيل وحده هو ما يختلف، فتعزل المقارنةُ التمثيلَ.<br><br>أما ما لا أدّعيه: لا أدّعي الضبط الدقيق كفء المعاملات نفسه، ولا أدّعي التكييف منخفض الرتبة للالتفافات، لأن عدة طرق كهذه موجودة بالفعل. وتفكيك السعة والطور من AlphaPre لا مني؛ وما هو لي هو استخدامه لتحديد أين تذهب الميزانية. والمجموعات والبروتوكول ونقطة التفتيش المصدر، كلها موروثة.<br><br>أنا لا أقترح طريقة عامة الغرض. وكل قرار تصميمي أتخذه نابع من خاصية في هذا النموذج قِستُها بنفسي."),
    ("10", "Completed work I",
     "Before designing anything, I took the trained model apart and counted it. This needed no dataset and no GPU, and it took one afternoon.<br><br>The model has eighty-nine million parameters. Ninety-nine point nine three percent of them are in convolutional layers. Two hundredths of one percent are in linear layers. And inside a kernel, channel entries outnumber spatial entries by about forty-nine thousand nine hundred to one.<br><br>That third number is the premise of my project. The method I am extending is defined for linear layers, and linear layers are two hundredths of one percent of this model. Applied as it was published, it could adapt almost nothing of it. That is now measured rather than asserted.<br><br>I also found that the amplitude pathway carries five hundred and thirty-four times the parameters of the phase pathway. That is an architectural fact, not evidence about where domain shift lives, but it would have confounded a naive comparison between the two. So that ablation now runs under a matched parameter budget. The measurement changed my experiment design before I ran any training.",
     "قبل تصميم أي شيء، فكّكتُ النموذج المدرَّب وأحصيتُه. ولم يتطلّب ذلك أي بيانات ولا معالجًا رسوميًا، واستغرق فترة بعد ظهر واحدة.<br><br>النموذج يحوي تسعة وثمانين مليون معامل. تسعة وتسعون فاصلة تسعة ثلاثة بالمئة منها في طبقات التفافية، ومئتان من واحد بالمئة في طبقات خطية. وداخل النواة، تفوق مُدخلات القنوات المُدخلات المكانية بنحو تسعة وأربعين ألفًا وتسعمئة إلى واحد.<br><br>والرقم الثالث هو منطلق مشروعي. فالطريقة التي أُوسّعها معرَّفة للطبقات الخطية، والطبقات الخطية تمثّل مئتين من واحد بالمئة من هذا النموذج. ولو طُبِّقت كما نُشرت لما استطاعت تكييف شيء يُذكر منه. وهذا الآن مقيس لا مُدَّعى.<br><br>ووجدتُ أيضًا أن مسار السعة يحمل أربعمئة وأربعة وثلاثين... بل خمسمئة وأربعة وثلاثين ضعف معاملات مسار الطور. وهذه حقيقة معمارية لا دليل على موضع انزياح المجال، لكنها كانت ستُربك مقارنة ساذجة بينهما. لذا تجري تلك الدراسة الآن تحت ميزانية معاملات مطابَقة. فالقياس غيّر تصميم تجربتي قبل أن أُجري أي تدريب."),
    ("11", "Completed work II",
     "I then ran the adaptation comparison. Every arm adapts the same frozen checkpoint to MeteoNet, trains on the stated fraction of the target training split, and is scored once on the same untouched test split.<br><br>With no training at all, the model scores zero point three one seven eight. That is the floor. Every adaptation arm beats it by between zero point zero six two and zero point zero seven.<br><br>Now the interesting part. The low-rank method trains seventy-one thousand six hundred and eighty parameters, which is zero point zero eight percent of the model. Full fine-tuning trains all eighty-nine million. At every data budget the two are within zero point zero zero two three of each other. And at one percent of the target archive, the small method is actually ahead.<br><br>That is one parameter in one thousand two hundred and forty-two, for the same accuracy.<br><br>My reading is that in the few-shot regime, extreme parameter efficiency acts as a regulariser, and not only as a storage convenience. With sixty-three training sequences, the eighty-nine million parameter model overfits before the small one does.",
     "ثم أجريتُ مقارنة التكييف. كل ذراع تُكيّف نقطة التفتيش المُجمَّدة نفسها على MeteoNet، وتتدرّب على النسبة المذكورة من شطر تدريب الهدف، وتُقيَّم مرة واحدة على شطر الاختبار نفسه غير الممسوس.<br><br>وبلا أي تدريب، يسجّل النموذج صفر فاصلة ثلاثة واحد سبعة ثمانية. وهذه هي الأرضية. وكل ذراع تكييف تتفوّق عليها بما بين صفر فاصلة صفر ستة اثنين وصفر فاصلة صفر سبعة.<br><br>والآن الجزء المثير. الطريقة منخفضة الرتبة تدرّب واحدًا وسبعين ألفًا وستمئة وثمانين معاملًا، أي صفر فاصلة صفر ثمانية بالمئة من النموذج. والضبط الكامل يدرّب التسعة والثمانين مليونًا كلها. وعند كل ميزانية بيانات تبقى الاثنتان ضمن صفر فاصلة صفر صفر اثنين ثلاثة من بعضهما. وعند واحد بالمئة من أرشيف الهدف تكون الطريقة الصغيرة متقدّمة فعلًا.<br><br>أي معامل واحد من كل ألف ومئتين واثنين وأربعين، بالدقة نفسها.<br><br>وقراءتي أنه في نظام الأمثلة القليلة، تعمل الكفاءة القصوى في المعاملات كمنظِّم، لا كوسيلة توفير تخزين فحسب. فمع ثلاثة وستين تسلسلًا تدريبيًا، يُفرِط النموذج ذو التسعة والثمانين مليون معامل في التخصيص قبل الصغير."),
    ("12", "Limits",
     "I want to state clearly what these results do not establish.<br><br>Every number is a single run with one random seed. There are no error bars.<br><br>The margins are small. Plus or minus zero point zero zero two is within what a single seed can produce. So the reversal at one percent is suggestive, and it is consistent across three budgets, but it is not proven, and I am not presenting it as a result.<br><br>There is also one ordering that I cannot yet explain. The low-rank method scores higher at one percent than at ten percent. Each arm was stopped at its own validation peak, so the larger budget was never fully consumed before overfitting began. Whether that is real or noise is unresolved.<br><br>And the second research content is not implemented yet. So the comparison that this project exists to make is still open.<br><br>Repeating every configuration across several random seeds is the immediate next step.",
     "أودّ أن أوضّح ما لا تُثبته هذه النتائج.<br><br>كل رقم ناتج عن تشغيل واحد ببذرة عشوائية واحدة. ولا توجد أشرطة خطأ.<br><br>والفوارق صغيرة. فزائد أو ناقص صفر فاصلة صفر صفر اثنين يقع ضمن ما قد تنتجه بذرة واحدة. لذا فالانقلاب عند واحد بالمئة مُرجِّح، وهو متّسق عبر ثلاث ميزانيات، لكنه غير مُثبَت، ولا أقدّمه كنتيجة.<br><br>وهناك أيضًا ترتيب واحد لا أستطيع تفسيره بعد. فالطريقة منخفضة الرتبة تسجّل عند واحد بالمئة أعلى منها عند عشرة بالمئة. وقد أُوقفت كل ذراع عند ذروة تحقّقها، فلم تُستهلك الميزانية الأكبر بالكامل قبل بدء الإفراط في التخصيص. وهل هذا حقيقي أم ضجيج؟ الأمر غير محسوم.<br><br>ومحتوى البحث الثاني لم يُنفَّذ بعد. فالمقارنة التي وُجد هذا المشروع لأجلها ما تزال مفتوحة.<br><br>وتكرار كل إعداد عبر عدة بذور عشوائية هو الخطوة التالية المباشرة."),
    ("13", "Schedule",
     "The schedule runs from now until December 2027.<br><br>For the rest of this year I will acquire the remaining archives, finish the data loaders and the HSS metric, fix the benchmark protocol, and implement the spectral method. I start from FourierFT, which is open source, and which the method builds on.<br><br>In the first half of 2027 I run the full comparison, and then the ablations.<br><br>In the second half I consolidate the results, prepare a paper, and begin writing the thesis.<br><br>The pipeline already exists and has produced results, so the largest single item of remaining work is implementing the spectral method from its publication, and I have allocated one to two months for that.",
     "يمتد الجدول من الآن حتى ديسمبر 2027.<br><br>في ما تبقّى من هذا العام سأحصل على الأرشيفات المتبقية، وأُنهي محمّلات البيانات ومقياس HSS، وأُثبّت بروتوكول المرجعية، وأُنفّذ الطريقة الطيفية. وأبدأ من FourierFT، وهي مفتوحة المصدر، وتبني عليها الطريقة.<br><br>وفي النصف الأول من 2027 أُجري المقارنة الكاملة ثم دراسات الحذف.<br><br>وفي النصف الثاني أُوحّد النتائج وأُعدّ ورقة وأبدأ كتابة الأطروحة.<br><br>والمسار البرمجي موجود بالفعل وأنتج نتائج، لذا فأكبر بند متبقٍّ هو تنفيذ الطريقة الطيفية من منشورها، وقد خصّصتُ لذلك شهرًا إلى شهرين."),
    ("14", "Expected outcomes",
     "I expect five outcomes from this project.<br><br>A reusable cross-dataset benchmark, with data loaders for four archives and a documented normalisation and thresholding protocol.<br><br>Two parameter-efficient adaptation methods for convolutional spatiotemporal models, differing only in the representation of the update.<br><br>A systematic comparison across target-data budgets, including the two baselines that are most often left out, which are training from scratch and adaptive batch normalisation.<br><br>An analysis of where domain shift resides inside a trained nowcasting model, and which layers actually require adaptation.<br><br>And the outcome this project is ultimately for: which of the two spaces is the better place to spend a small adaptation budget, and whether that answer reverses as target data become scarce. The two methods are constructed to be comparable precisely so that this question can be settled rather than argued.",
     "أتوقّع خمس نتائج من هذا المشروع.<br><br>مرجعية عابرة للمجموعات قابلة لإعادة الاستخدام، مع محمّلات بيانات لأربعة أرشيفات وبروتوكول موثَّق للتطبيع والعتبات.<br><br>وطريقتان للتكييف كفء المعاملات للنماذج المكانية-الزمانية الالتفافية، تختلفان فقط في تمثيل التحديث.<br><br>ومقارنة منهجية عبر ميزانيات بيانات الهدف، تشمل خطَّي الأساس الأكثر إغفالًا، وهما التدريب من الصفر وتطبيع الدفعات التكيّفي.<br><br>وتحليل لموضع انزياح المجال داخل نموذج تنبؤ آني مدرَّب، وأي الطبقات تحتاج التكييف فعلًا.<br><br>والنتيجة التي وُجد المشروع لأجلها: أي الفضاءين هو المكان الأفضل لإنفاق ميزانية تكييف صغيرة، وهل ينقلب ذلك الجواب مع شحّ بيانات الهدف. والطريقتان مُصمَّمتان لتكونا قابلتين للمقارنة تحديدًا كي يُحسم هذا السؤال لا أن يُجادَل فيه."),
    ("15", "Closing",
     "That concludes my presentation. Thank you for listening, and I welcome your comments and questions.",
     "بهذا أختم عرضي. شكرًا لإصغائكم، وأرحّب بتعليقاتكم وأسئلتكم."),
]

rows = []
for num, title, en, ar in SLIDES:
    rows.append('''  <div class="note">
    <h4><span class="mono" style="color:var(--mark)">SLIDE %s</span>&nbsp;&nbsp;%s</h4>
    <p class="en" style="font-size:15.5px">%s</p>
    <p class="ar" style="font-size:15.5px">%s</p>
  </div>''' % (num, title, en, ar))

SCRIPT_BODY = '''  <p class="lead en">This is exactly what is in the speaker notes of the deck, so you can learn it here and read it there. Numbers are written the way they should be said out loud.</p>
  <p class="lead ar">هذا هو نصّ ملاحظات المتحدّث في العرض حرفيًا، فيمكنك حفظه هنا وقراءته هناك. والأرقام مكتوبة بالطريقة التي يجب أن تُنطق بها.</p>
  <p class="en">Read the whole thing aloud twice. The second time, look up at the end of every paragraph.</p>
  <p class="ar">اقرأ النص كاملًا بصوت مسموع مرتين. وفي المرة الثانية، ارفع بصرك في نهاية كل فقرة.</p>
''' + "\n".join(rows)

s14 = block("14", "The script — what to say", "النص — ما ينبغي أن تقوله",
            "The defence", "المناقشة", SCRIPT_BODY)


# ══════════════════════════════════════════════════ 15  QUESTIONS
QA = [
  ("Novelty and prior work", "الابتكار والأعمال السابقة", [
    ("Has anyone done this before?",
     "هل سبق أن أنجز أحد هذا؟",
     "Not this. Efficient fine-tuning exists, and nowcasting exists. What does not exist is transfer between these radar archives under a restricted target-data budget — in the literature I surveyed, all four datasets are trained and evaluated separately. And the spectral method has never been extended to convolutions by anyone, which I can say with confidence because there is no public implementation and an author of the paper confirmed it.",
     "ليس هذا تحديدًا. فالضبط الدقيق الكفء موجود، والتنبؤ الآني موجود. أما غير الموجود فهو النقل بين أرشيفات الرادار هذه في ظل ميزانية بيانات هدف محدودة — ففي الأدبيات التي مسحتُها تُدرَّب المجموعات الأربع وتُقيَّم منفصلة. كما أن الطريقة الطيفية لم يُوسّعها أحد إلى الالتفافات، وأقول ذلك بثقة لأنه لا يوجد تنفيذ عام، وقد أكّد ذلك أحد مؤلفي الورقة."),
    ("How is this different from existing convolutional PEFT work?",
     "بمَ يختلف هذا عن أعمال PEFT الالتفافية الموجودة؟",
     "I am not proposing a general-purpose method, so I am not competing with those. Conv-LoRA, LoRA-C and CoLoRA are general recipes tested mostly on photographs. Every design decision I make comes from a property of a precipitation nowcasting model that I measured — that it is 99.93% convolutional, that channels outnumber spatial entries 49,900 to one, that amplitude and phase differ 534-fold in size. A general method has no basis for choosing any of them.",
     "أنا لا أقترح طريقة عامة الغرض، فلستُ منافسًا لها. فـ Conv-LoRA وLoRA-C وCoLoRA وصفات عامة اختُبرت غالبًا على الصور الفوتوغرافية. أما كل قرار تصميمي أتخذه فنابع من خاصية في نموذج تنبؤ آني قِستُها — أنه التفافي بنسبة 99.93%، وأن القنوات تفوق المُدخلات المكانية بـ49,900 إلى واحد، وأن السعة والطور يختلفان في الحجم 534 ضعفًا. والطريقة العامة لا تملك أي أساس لاختيار أيٍّ منها."),
    ("Isn't your first method just LoRA?",
     "أليست طريقتك الأولى مجرّد LoRA؟",
     "Largely, yes, and I say so in the proposal. It is included as a controlled counterpart and as a strong baseline, not as a novelty claim. The comparison is only meaningful if one side is the established method done properly.",
     "إلى حد كبير نعم، وأقول ذلك في المقترح. فهي مُدرَجة كنظير مضبوط وخط أساس قوي، لا كادّعاء ابتكار. فالمقارنة لا تكون ذات معنى إلا إذا كان أحد طرفيها الطريقةَ الراسخة مُنفَّذة كما ينبغي."),
    ("What is your contribution, as opposed to your supervisor's?",
     "ما إسهامك أنت مقابل إسهام مشرفك؟",
     "The model and the spectral method both come from this laboratory, and I say that openly. What is mine is the extension of that method to convolutional kernels, the decision of which axes may be permuted and why, the controlled comparison between the two representations, and the measurements that drove those decisions.",
     "النموذج والطريقة الطيفية كلاهما من هذا المختبر، وأقول ذلك صراحةً. أما ما هو لي فهو توسعة تلك الطريقة إلى نوى الالتفاف، وقرار أي المحاور يجوز إعادة ترتيبها ولماذا، والمقارنة المضبوطة بين التمثيلين، والقياسات التي قادت تلك القرارات."),
  ]),
  ("Your evidence", "دليلك", [
    ("Have you actually run any experiments, or is this all planned?",
     "هل أجريتَ تجارب فعلية أم أن هذا كله مخطَّط؟",
     "Three are complete. A parameter census of the source checkpoint. A cross-dataset zero-shot baseline with a control run on the source domain itself. And a seven-arm adaptation comparison across three data budgets. All three are in Chapter 5 of the proposal with their numbers.",
     "ثلاث تجارب مكتملة. إحصاء معاملات نقطة التفتيش المصدر. وخط أساس صفري عابر للمجموعات مع تشغيل ضابط على المجال المصدر نفسه. ومقارنة تكييف بسبع أذرع عبر ثلاث ميزانيات بيانات. والثلاث جميعها في الفصل الخامس من المقترح بأرقامها."),
    ("Where did these results come from?",
     "من أين جاءت هذه النتائج؟",
     "From running code on real data. The census reads the released AlphaPre checkpoint directly and classifies every parameter tensor. The baseline and the comparison run on the SEVIR and MeteoNet archives, which I have on disk. Nothing on those slides is quoted from a paper or estimated.",
     "من تشغيل كود على بيانات حقيقية. فالإحصاء يقرأ نقطة تفتيش AlphaPre المنشورة مباشرةً ويصنّف كل موتّر معاملات. وخط الأساس والمقارنة يعملان على أرشيفي SEVIR وMeteoNet الموجودين لديّ على القرص. ولا شيء في تلك الشرائح منقول من بحث أو مُقدَّر تخمينًا."),
    ("Only one seed? How do you know this is not noise?",
     "بذرة واحدة فقط؟ كيف تعرف أن هذا ليس ضجيجًا؟",
     "I do not, and I say so on the slide. Plus or minus 0.002 CSI is within single-seed variation. The reversal is suggestive because it is monotonic across three budgets and the training curves agree with it, but I present it as a trend, not a result. Seed repeats are the first item in the next phase.",
     "لا أعرف، وأقول ذلك في الشريحة. فزائد أو ناقص 0.002 من CSI يقع ضمن تباين البذرة الواحدة. والانقلاب مُرجِّح لأنه مطّرد عبر ثلاث ميزانيات ولأن منحنيات التدريب تتّفق معه، لكني أقدّمه كاتجاه لا كنتيجة. وتكرار البذور هو البند الأول في المرحلة التالية."),
    ("Why does the low-rank method score higher at 1% than at 10%?",
     "لماذا تسجّل الطريقة منخفضة الرتبة عند 1% أعلى منها عند 10%؟",
     "That is the one result I cannot yet explain, and I flag it rather than hide it. Every arm was early-stopped at its own validation peak, and all peaked at a similar number of optimisation steps, so the 10% arm never consumed its extra data before overfitting. Whether repeated exposure to a small set genuinely beats one pass over a larger one, or this is seed noise, is not resolved by these runs.",
     "هذه هي النتيجة الوحيدة التي لا أستطيع تفسيرها بعد، وأنا أُبرزها لا أُخفيها. فقد أُوقفت كل ذراع مبكرًا عند ذروة تحقّقها، وبلغت جميعها الذروة عند عدد متقارب من خطوات التحسين، فلم تستهلك ذراع الـ10% بياناتها الإضافية قبل الإفراط في التخصيص. وهل التعرّض المتكرر لمجموعة صغيرة يتفوّق فعلًا على مرور واحد على مجموعة أكبر، أم أن هذا ضجيج بذرة؟ لم تحسم هذه التشغيلات ذلك."),
    ("You report 0.3508 on SEVIR and 0.3178 on MeteoNet — isn't that a tiny gap?",
     "تذكر 0.3508 على SEVIR و0.3178 على MeteoNet — أليست فجوة ضئيلة؟",
     "Those two numbers must not be compared. They average over different physical quantities — vertically integrated liquid against reflectivity in dBZ — at different thresholds, and their closeness is a coincidence of threshold choice. The valid comparison is decay relative to each curve's own first frame, matched on minutes: 61.8% retained against 33.8%.",
     "لا يجوز مقارنة هذين الرقمين. فهما متوسّطان على كميتين فيزيائيتين مختلفتين — السائل المتكامل رأسيًا مقابل الانعكاسية بـ dBZ — وعند عتبات مختلفة، وتقاربهما محض صدفة في اختيار العتبة. والمقارنة الصحيحة هي التدهور بالنسبة إلى اللقطة الأولى لكل منحنى ومطابَقة بالدقائق: 61.8% محفوظة مقابل 33.8%."),
  ]),
  ("Feasibility", "الجدوى", [
    ("Is this achievable in the time you have?",
     "هل هذا قابل للإنجاز في الوقت المتاح؟",
     "The schedule runs to December 2027, which is about fifteen months. The strongest evidence that it is feasible is that the pipeline already exists and has produced results — data loading, adaptation, training and evaluation all ran end to end for the preliminary experiments. What remains is extending the method and widening the comparison, not building an apparatus from nothing. The largest single item is implementing the spectral method, and one to two months are allocated for it.",
     "يمتد الجدول حتى ديسمبر 2027، أي نحو خمسة عشر شهرًا. وأقوى دليل على الجدوى أن المسار البرمجي موجود بالفعل وأنتج نتائج — فالتحميل والتكييف والتدريب والتقييم جرت كلها من طرف إلى طرف في التجارب الأولية. وما تبقّى هو توسيع الطريقة وتوسيع المقارنة، لا بناء جهاز من الصفر. وأكبر بند مفرد هو تنفيذ الطريقة الطيفية، وقد خُصّص له شهر إلى شهران."),
    ("There is no public implementation of the method. How do you know you can build it?",
     "لا يوجد تنفيذ عام للطريقة. كيف تعرف أنك تستطيع بناءها؟",
     "I start from FourierFT, which is open source and which the method builds on, and reproduce that first to establish correctness. Then the spectral transformation, then the convolutional extension, each on a verified basis. Working from the publication also forces the detailed understanding that the extension requires anyway.",
     "أبدأ من FourierFT، وهي مفتوحة المصدر وتبني عليها الطريقة، وأُعيد إنتاجها أولًا لإثبات الصحة. ثم التحويل الطيفي، ثم التوسعة الالتفافية، كلٌّ على أساس مُتحقَّق منه. والعمل من المنشور يفرض أيضًا الفهم التفصيلي الذي تتطلّبه التوسعة على أي حال."),
    ("You only have two of the four datasets. Isn't that a risk?",
     "لديك مجموعتان فقط من أربع. أليست تلك مخاطرة؟",
     "SEVIR and MeteoNet are on disk and both preliminary experiments ran on them, so the source and the primary target are secured. Shanghai Radar and CIKM are additional target domains that strengthen generality; they are scheduled and the authors of DiffCast publish preprocessed versions of three of the four archives. The core comparison does not depend on them.",
     "SEVIR وMeteoNet على القرص وقد جرت عليهما التجربتان الأوليتان، فالمصدر والهدف الأساسي مؤمَّنان. أما رادار شنغهاي وCIKM فمجالا هدف إضافيان يعزّزان التعميم؛ وهما مجدولان، ومؤلفو DiffCast ينشرون نسخًا مُعالَجة مسبقًا لثلاثة من الأرشيفات الأربعة. والمقارنة الجوهرية لا تعتمد عليهما."),
    ("What if you never get the compute you asked for?",
     "ماذا لو لم تحصل على الحوسبة التي طلبتها؟",
     "The preliminary work was done on the laboratory server and the work continues there while the dedicated container is approved, so the absence of it delays widening the comparison but does not halt the project. The task configuration is 128 by 128, which is modest — twenty-four gigabytes of graphics memory is sufficient.",
     "أُنجز العمل الأولي على خادم المختبر، والعمل مستمر هناك ريثما تُعتمد الحاوية المخصّصة، فغيابها يؤخّر توسيع المقارنة لكنه لا يوقف المشروع. وإعداد المهمة هو 128 في 128، وهو متواضع — وأربعة وعشرون غيغابايت من ذاكرة الرسوميات كافية."),
  ]),
  ("Method choices", "الخيارات المنهجية", [
    ("Why freeze the model instead of fine-tuning it normally?",
     "لماذا تُجمّد النموذج بدل ضبطه بالطريقة المعتادة؟",
     "Three reasons. Storage: one frozen model plus a small file per country instead of a whole model per country. Compute: far less memory and time. And most interestingly, regularisation — with very little target data, eighty-nine million free parameters overfit, and a much smaller set cannot as easily. My results already point at that.",
     "ثلاثة أسباب. التخزين: نموذج مُجمَّد واحد مع ملف صغير لكل دولة بدل نموذج كامل لكل دولة. والحوسبة: ذاكرة ووقت أقل بكثير. والأهم، التنظيم — فمع بيانات هدف قليلة جدًا يُفرِط تسعة وثمانون مليون معامل حر في التخصيص، بينما لا تستطيع مجموعة أصغر بكثير ذلك بسهولة. ونتائجي تشير إلى ذلك بالفعل."),
    ("Why only the channel axes? Why not adapt the spatial ones too?",
     "لماذا محاور القنوات فقط؟ ولمَ لا تُكيّف المكانية أيضًا؟",
     "Two reasons, and the second is decisive. First, permutation is only admissible where order carries no meaning, and spatial positions are real adjacencies. Second, inside a kernel the channel entries outnumber the spatial ones by roughly 49,900 to one — there is nothing to compress in nine numbers. It is arithmetic rather than preference.",
     "سببان، والثاني حاسم. أولًا، إعادة الترتيب مشروعة فقط حيث لا يحمل الترتيب معنى، والمواضع المكانية تجاورات حقيقية. وثانيًا، داخل النواة تفوق مُدخلات القنوات المكانية بنحو 49,900 إلى واحد — فليس في تسعة أرقام ما يُضغط. إنه حساب لا تفضيل."),
    ("What if adaptive batch normalisation beats your method? It costs nothing.",
     "ماذا لو تفوّق تطبيع الدفعات التكيّفي على طريقتك؟ فهو لا يكلّف شيئًا.",
     "Then I must report that, and it is precisely why it is one of my seven comparison arms. If the difference between countries really is mostly an intensity shift, recomputing normalisation statistics might close much of the gap for free. Including that possibility is what makes the study credible rather than a demonstration.",
     "عندئذٍ يجب أن أُبلّغ بذلك، ولهذا تحديدًا هو أحد أذرع المقارنة السبع لديّ. فإن كان الفرق بين الدول يعود في معظمه إلى انزياح في الشدة، فقد تُغلق إعادةُ حساب إحصاءات التطبيع جزءًا كبيرًا من الفجوة مجانًا. وإدراج هذا الاحتمال هو ما يجعل الدراسة ذات مصداقية لا مجرّد استعراض."),
    ("What if the naive reshape actually works?",
     "ماذا لو نجحت إعادة التشكيل الساذجة فعلًا؟",
     "Then I have learned something real and I report it. That design is kept deliberately as a control arm. A negative result for it alongside a positive result for the channel-only design is evidence that spatial correlation is the obstacle; a positive result would mean the obstacle is smaller than the theory suggests, which is also worth knowing.",
     "عندئذٍ أكون قد تعلّمتُ شيئًا حقيقيًا وأُبلّغ به. فذلك التصميم مُبقًى عمدًا كذراع ضابطة. ونتيجة سلبية له إلى جانب نتيجة إيجابية للتصميم القنوي فقط دليلٌ على أن الارتباط المكاني هو العائق؛ ونتيجة إيجابية تعني أن العائق أصغر مما تفترضه النظرية، وهذا أيضًا جدير بالمعرفة."),
    ("Why CSI? Why not mean squared error?",
     "لماذا CSI؟ ولمَ لا متوسط مربع الخطأ؟",
     "Mean squared error rewards blurry forecasts, because averaging away the uncertainty minimises it. CSI thresholds the prediction and the truth at a rainfall intensity and asks whether rain was predicted where and when it actually fell, which is what a warning depends on. I also report HSS, which corrects for lucky guesses.",
     "متوسط مربع الخطأ يكافئ التنبؤات الضبابية، لأن تمييع عدم اليقين بالمتوسط يُقلّله. أما CSI فيضع عتبة على التنبؤ والحقيقة عند شدة مطر معيّنة، ويسأل هل تُوقّع المطر حيث ومتى هطل فعلًا، وهذا ما يعتمد عليه التحذير. وأُبلّغ أيضًا بـ HSS الذي يصحّح أثر التخمين الموفَّق."),
  ]),
  ("Scope and outcome", "النطاق والنتيجة", [
    ("Why two research contents instead of one?",
     "لماذا محتويان بحثيان بدل واحد؟",
     "Because the question is which representation is better, and that cannot be answered with one method. The two are built to be identical in every respect except the space the update lives in, so the comparison isolates exactly the variable I care about. The comparison is the thesis.",
     "لأن السؤال هو أي التمثيلين أفضل، ولا يمكن الإجابة عنه بطريقة واحدة. فالطريقتان مبنيّتان لتكونا متطابقتين في كل شيء إلا الفضاء الذي يعيش فيه التحديث، فتعزل المقارنة بالضبط المتغيّر الذي يهمّني. والمقارنة هي الأطروحة."),
    ("What if the two methods perform identically?",
     "ماذا لو تطابق أداء الطريقتين؟",
     "That is a reportable result. It would mean the choice of representation does not matter for this problem, which is useful to know and is stated as such in my expected outcomes. The hypotheses are written as falsifiable predictions, not as expected conclusions.",
     "تلك نتيجة قابلة للإبلاغ. فهي تعني أن اختيار التمثيل لا يهم في هذه المسألة، وهذا مفيد أن يُعرف، وهو مذكور كذلك في نتائجي المتوقعة. فالفرضيات مكتوبة كتنبؤات قابلة للدحض لا كاستنتاجات متوقّعة."),
    ("What is the practical value of this?",
     "ما القيمة العملية لهذا؟",
     "A meteorological service in a country with little archived radar data could take a model trained elsewhere and adapt it with a small file rather than a full retraining. And the layer-wise analysis says which parts of such a model actually need adapting, which is reusable knowledge beyond this pair of methods.",
     "يمكن لهيئة أرصاد في دولة قليلة بيانات الرادار المؤرشفة أن تأخذ نموذجًا دُرِّب في مكان آخر وتُكيّفه بملف صغير بدل إعادة تدريب كاملة. كما يُبيّن التحليل الطبقي أي أجزاء هذا النموذج تحتاج التكييف فعلًا، وهي معرفة قابلة لإعادة الاستخدام خارج هاتين الطريقتين."),
  ]),
]

qa_html = ['''  <p class="lead en">Grouped by what the question is really testing. Read the answer, then say it in your own words — a memorised answer sounds memorised.</p>
  <p class="lead ar">مُجمَّعة حسب ما يختبره السؤال فعلًا. اقرأ الجواب ثم قله بكلماتك — فالجواب المحفوظ يبدو محفوظًا.</p>''']
for cat_en, cat_ar, items in QA:
    qa_html.append('  <h3 class="en">%s</h3>\n  <h3 class="ar">%s</h3>' % (cat_en, cat_ar))
    for q_en, q_ar, a_en, a_ar in items:
        qa_html.append('''  <div class="note">
    <h4 class="en">“%s”</h4>
    <h4 class="ar">«%s»</h4>
    <p class="en">%s</p>
    <p class="ar">%s</p>
  </div>''' % (q_en, q_ar, a_en, a_ar))

qa_html.append('''  <div class="say">
    <span class="who en">If you genuinely do not know</span>
    <span class="who ar">إذا كنت لا تعرف فعلًا</span>
    <span class="q en">“I have not measured that yet. I would find out by … and it would change the design in this way if the answer came out differently.”</span>
    <span class="q ar">«لم أقِس ذلك بعد. سأكتشفه عن طريق… وسيغيّر التصميم بهذه الطريقة إن جاء الجواب مختلفًا.»</span>
  </div>
  <p class="en">This will happen at least once, and it is survivable. <b>Inventing an answer is not.</b></p>
  <p class="ar">سيحدث هذا مرة على الأقل، ويمكن تجاوزه. <b>أما اختلاق إجابة فلا.</b></p>''')

s15 = block("15", "Questions they will ask", "الأسئلة التي سيطرحونها",
            "The defence", "المناقشة", "\n".join(qa_html))

# ── Insert before the section that is now 16, anchoring on the element itself.
#    The HTML comments above each section still carry the pre-renumber value, so
#    anchoring on one of those puts the insert a section too late.
m = re.search(r'\n<!-- [^\n]*-->\n<section id="s16" class="rv">', s)
if not m:
    sys.exit("insert anchor not found")
s = s[:m.start()] + s14 + s15 + s[m.start():]

# resync every section comment to the eyebrow number it introduces
s = re.sub(
    r'<!-- [^\n]*-->\n<section id="(s\d+)"([^>]*)>\n  <div class="eyebrow"><b>(\d+)</b>',
    lambda mm: '<!-- %s %s %s -->\n<section id="%s"%s>\n  <div class="eyebrow"><b>%s</b>'
               % ("=" * 26, mm.group(3), "=" * 26, mm.group(1), mm.group(2), mm.group(3)),
    s)

# ── nav entries
navanchor = '  ["s16",'
if s.count(navanchor) != 1:
    sys.exit("nav anchor not unique (%d)" % s.count(navanchor))
s = s.replace(navanchor,
              '  ["s14","14 · The script","14 · النص"],\n'
              '  ["s15","15 · Questions they will ask","15 · الأسئلة المتوقعة"],\n' + navanchor)

io.open(P, "w", encoding="utf-8").write(s)
print("added sections 14 (script, %d slides) and 15 (Q&A, %d questions)"
      % (len(SLIDES), sum(len(i[2]) for i in QA)))

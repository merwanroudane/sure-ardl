import streamlit as st

from lib.ui import definition, hero, intuition, rtl_css, signature, warn
from lib.viz import bounds_decision_chart

rtl_css()

hero("الاختبارات البعدية", "Post-estimation — ما تفعله بعد ظهور النتائج")

st.markdown(
    """
التقدير ليس النهاية. بعده تأتي ثلاث مجموعات من الفحوص، ولكل واحدة سؤال
مختلف تمامًا.
"""
)

st.mermaid_chart(
    """
flowchart TB
    E["النتائج الأولية"] --> G1["المجموعة الأولى<br>هل النموذج سليم؟"]
    E --> G2["المجموعة الثانية<br>هل توجد علاقة طويلة الأجل؟"]
    E --> G3["المجموعة الثالثة<br>ماذا تخبرنا المقارنة بين الوحدات؟"]

    G1 --> A1["estat serial"]
    G1 --> A2["estat sigma"]
    G2 --> B1["estat bounds"]
    G2 --> B2["فحص إشارة لامدا"]
    G2 --> B3["estat longrun"]
    G3 --> C1["estat ecequal"]
    G3 --> C2["estat lrequal"]
    G3 --> C3["estat poolability"]

    style G1 fill:#FBF4E8,stroke:#E08D3C,stroke-width:2px
    style G2 fill:#E6F0E9,stroke:#2E8B6F,stroke-width:3px
    style G3 fill:#EFE9F5,stroke:#7D5BA6,stroke-width:2px
"""
)

st.markdown("## المجموعة الأولى: هل النموذج سليم؟")

st.markdown("### 1. الارتباط التسلسلي — الفحص الأهم على الإطلاق")

st.code("estat serial, lags(2)", language="stata")

st.code(
    """--------------------------------------------------------------------------------
Breusch-Godfrey LM test for serial correlation in the SUR residuals
H0: no autocorrelation up to order 2
--------------------------------------------------------------------------------
                              LM       df          p
   Indonesia                11.9239        2     0.0026   <- reject at 5%
   Malaysia                  5.3427        2     0.0692
   Philippines               4.4670        2     0.1072
   Singapore                12.5082        2     0.0019   <- reject at 5%
   Thailand                  6.0135        2     0.0495   <- reject at 5%
   Vietnam                   3.6389        2     0.1621""",
    language="text",
)

warn(
    "<b>هذا ليس فحصًا روتينيًا.</b> صحة استعمال مصفوفة التغاير اللحظي "
    "$\\Sigma$ — بدل مصفوفة التغاير طويل الأجل — <b>تتوقف عليه كليًا</b>. "
    "وهو مبرّر الورقة كلها (الملاحظة 4).<br><br>"
    "في المثال أعلاه، ثلاث دول ترفض فرضية العدم. معنى ذلك أن توصيف "
    "ARDL(1,1,1,1) <b>قصير جدًا</b> لتلك الدول.<br><br>"
    "<b>العلاج الصحيح الوحيد: زد رتب الإبطاء.</b> لا تستعمل أخطاء معيارية "
    "«قوية» كبديل — المشكلة في توصيف النموذج لا في تقدير التباين.",
    term="لماذا هذا حاسم",
)

st.code(
    """
* جرّب رتبًا أعلى
surardl lrec lgdp lfdi lto, case(3) lags(2)
estat serial, lags(2)

* أو دع المعيار المعلوماتي يختار لكل دولة
surardl lrec lgdp lfdi lto, case(3) maxlags(4) bic
estat serial, lags(2)
""",
    language="stata",
)

st.markdown("### 2. جودة مصفوفة التغاير")

st.code("estat sigma", language="stata")

st.markdown(
    """
يعرض $\\hat\\Sigma$ ومصفوفة الارتباط، ثم:

| المؤشّر | ماذا يعني | ما يُقلق |
|---|---|---|
| Breusch-Pagan LM | هل $\\Sigma$ قطرية؟ | عدم الرفض ← لا فائدة من SUR |
| Pesaran CD | فحص تأكيدي | ضعيف القدرة عند $N$ صغيرة |
| T / N | كفاية البيانات | :red-badge[أقل من 5 ← حذر شديد] |
| Reciprocal condition number | شرطية المصفوفة | قريب جدًا من الصفر ← شبه منفردة |
| Positive definite | قابلية الانعكاس | `NO` ← النموذج غير صالح |
"""
)

st.markdown("## المجموعة الثانية: هل توجد علاقة طويلة الأجل؟")

st.markdown("### 1. اختبار الحدود — بثلاثة إحصاءات لا واحد")

st.code("estat bounds", language="stata")

st.code(
    """                        F        t      p(boot)   decision (10%/5%/1%)
--------------------------------------------------------------------------------
Indonesia               0.580   -1.098    0.880   N  N  N
Malaysia                2.380   -2.402    0.333   N  N  N
Philippines             8.632   -5.036    0.030   R  R  R
Singapore               7.275   -3.205    0.557   R  R  R
Thailand               11.372   -4.758    0.013   R  R  R
Vietnam                 6.132   -4.577    0.187   R  R  R""",
    language="text",
)

st.markdown(
    """
**رموز القرار:** :green-badge[N] لا نرفض · :orange-badge[-] غير حاسم ·
:red-badge[R] نرفض · `.` الحدود غير متاحة

**لكن انتبه إلى العمود `p(boot)`.** لاحظ سنغافورة: رموز القرار تقول «نرفض»،
لكن القيمة الاحتمالية بإعادة المعاينة 0.557 — أي **لا رفض إطلاقًا**.
أيّهما نصدّق؟
"""
)

st.error(
    "**نصدّق إعادة المعاينة.** الحدود المجدولة محسوبة لإحصاء F ناتج عن "
    "**معادلة واحدة بـ OLS**، لا لإحصاء نظام تُقدَّر فيه $\\Sigma$ من البيانات "
    "نفسها. وعند $T$ صغيرة يكون التوزيع تحت فرضية العدم أكثر تشتّتًا، "
    "فتصبح الحدود المجدولة **متساهلة**.",
    icon=":material/priority_high:",
)

st.markdown("### لماذا سنغافورة تحديدًا؟")

intuition(
    "عند الفحص تبيّن أن معاملات الأجل القصير لسنغافورة كبيرة جدًا: "
    "1.51 على <code>D.lgdp</code> و −1.11 على <code>D.lto</code>.<br><br>"
    "معنى ذلك أن $\\Delta y$ عندها <b>تهيمن عليه</b> الفروق المعاصرة "
    "للمتغيرات المفسّرة. فالمتغيّر التابع المولَّد في إعادة المعاينة يصبح "
    "قريبًا من تركيبة خطّية من المتغيرات المفسّرة زائد سير عشوائي، "
    "فتصبح حدود المستويات في معادلة الحدود <b>شبه مزدوجة خطيًا</b>، "
    "ويكتسب توزيع الإحصاء ذيلًا أيمن ثقيلًا جدًا.<br><br>"
    "<b>جداول PSS تفترض أن المتغيرات المفسّرة مستقلة عن المتغيّر التابع.</b> "
    "سنغافورة تخرق هذا الافتراض بشدة، فلا تنطبق عليها الجداول. "
    "إعادة المعاينة تقوم بعملها: تخبرك أن إحصاءك غير استثنائي "
    "بالنظر إلى بنية بياناتك.",
    term="تشخيص، لا عطل",
)

st.markdown("### 2. فحص إشارة λ — شرط ضروري مستقل")

st.markdown(
    """
رفض فرضية العدم **لا يكفي**. يجب أيضًا أن يكون $\\hat\\lambda_i < 0$ ومعنويًا،
وإلا فآلية تصحيح الخطأ غير مستقرة ولا يوجد توازن تعود إليه.

الأمر يطبع تحذيرًا تلقائيًا إن كان $\\hat\\lambda_i \\geq 0$ في أي معادلة.
"""
)

st.markdown("### 3. معاملات الأجل الطويل")

st.code(
    """
estat longrun, fieller
estat longrun, bootstrap(999)
""",
    language="stata",
)

definition(
    "لماذا ثلاث فترات ثقة مختلفة؟",
    "<b>دلتا:</b> سريعة وهي صيغة الورقة (المعادلة 89)، لكن المحاكاة الخامسة "
    "تُظهر أن تغطيتها منهارة.<br>"
    "<b>Fieller:</b> تعكس الاختبار $\\beta + \\theta\\lambda = 0$ فلا تقسم على "
    "$\\hat\\lambda$ أبدًا. إن خرجت <b>غير محدودة</b> فهذا إخبار صادق بأن "
    "$\\lambda$ ضعيف التعريف.<br>"
    "<b>Bootstrap:</b> فترات مئينية ومصحّحة التحيّز، تحافظ على الترابط بين المعادلات.",
)

st.markdown("## المجموعة الثالثة: المقارنة بين الوحدات")

st.markdown(
    """
هذه المجموعة هي **القيمة المضافة الحقيقية** للنظام. لا يمكن إجراؤها إطلاقًا
بالتقدير معادلةً بمعادلة.
"""
)

st.markdown("### 1. تساوي سرعات التعديل")

st.code("estat ecequal, mtest(holm)", language="stata")

st.code(
    """   Unit i                 Unit j                 chi2(1)        p    p(holm)
--------------------------------------------------------------------------------
   Indonesia              Malaysia                  1.098   0.2947   1.0000
   Indonesia              Philippines              11.337   0.0008   0.0106 **
   Indonesia              Thailand                 11.606   0.0007   0.0099 ***
   Indonesia              Vietnam                   8.768   0.0031   0.0399 **
   Malaysia               Philippines               7.402   0.0065   0.0731 *
   Philippines            Thailand                  0.222   0.6372   1.0000
   Philippines            Vietnam                   0.082   0.7752   1.0000
   Thailand               Vietnam                   0.516   0.4725   1.0000
--------------------------------------------------------------------------------
Joint H0: lambda_1 = ... = lambda_6   chi2( 5) =    21.540   p = 0.0006""",
    language="text",
)

st.success(
    "**هذه هي بنية العنقودين التي تذكرها الورقة.** إندونيسيا وماليزيا "
    "(بطيئتا التعديل) تختلفان معنويًا عن الفلبين وتايلند وفيتنام "
    "(سريعة التعديل)، بينما **لا فرق معنوي داخل كل مجموعة** "
    "(القيم الاحتمالية ≈ 1).\n\n"
    "استنتاج اقتصادي قابل للنشر، ومستحيل الحصول عليه من ست عمليات تقدير منفصلة.",
    icon=":material/insights:",
)

warn(
    "<b>تصحيح الاختبارات المتعددة ليس ترفًا.</b> مع ست وحدات لديك 15 مقارنة "
    "ثنائية. المحاكاة الرابعة في الورقة تُبلّغ أن أقصى معدّل رفض ثنائي يبلغ "
    "<b>53%</b> عند $N=5$ و $T=50$ دون تصحيح.<br><br>"
    "الخيار <code>mtest()</code> يقبل <code>holm</code> (الافتراضي) و "
    "<code>bonferroni</code> و <code>sidak</code> و <code>none</code>. "
    "<b>لا تستعمل <code>none</code> إلا إذا كانت لديك فرضية واحدة محدّدة سلفًا.</b>",
    term="انتبه",
)

st.markdown("### 2. تساوي معاملات الأجل الطويل")

st.code(
    """
estat lrequal              // كل المتغيرات
estat lrequal lgdp         // متغيّر بعينه
""",
    language="stata",
)

st.markdown(
    "يستعمل طريقة دلتا متعددة المتغيرات (المعادلتان 92-93)، ويأخذ في الحسبان "
    "التغايرات المتقاطعة بين معاملات الوحدتين."
)

st.markdown("### 3. قابلية التجميع")

st.code(
    """
estat poolability               // معاملات الأجل الطويل بيتا
estat poolability, lambda       // سرعات التعديل
estat poolability, all          // الاثنان معًا
""",
    language="stata",
)

st.markdown(
    """
السؤال: **هل يصحّ أصلًا أن نفرض معاملًا واحدًا على كل الوحدات؟**
إن رُفضت الفرضية، فنموذج البانل المتجانس التقليدي **غير ملائم** لبياناتك،
وهذا في حد ذاته نتيجة تستحق الإبلاغ.
"""
)

warn(
    "المحاكاة الرابعة تُبلّغ أن هذا الاختبار <b>يفرط في الرفض</b> عند $N$ كبيرة "
    "و $T$ صغيرة: 21.2% عند $N=5$ و $T=50$ بمستوى اسمي 5%. "
    "فسّر النتيجة بحذر إن كان $T < 200$ عند $N=5$، أو $T < 100$ عند $N \\leq 3$.",
    term="حدود الاختبار",
)

st.markdown("### 4. قياس المكسب")

st.code("estat efficiency", language="stata")

st.markdown(
    """
يعرض $1 - SE_{SUR}/SE_{OLS}$ لكل معامل مستوى — أي كم بالمئة انخفض الخطأ
المعياري بفضل التقدير المشترك. في تطبيق الآسيان كان المتوسط **20.7%**.
"""
)

st.markdown("## الرسوم")

st.code(
    """
estat graph                              // المجموعة الكاملة
estat graph, lambda                      // سرعات التعديل مرتّبة — تُظهر العناقيد
estat graph, bounds                      // الإحصاءات مقابل نطاقات PSS
estat graph, longrun variable(lgdp)      // مخطّط غابة للمعاملات
estat graph, sigma                       // خريطة حرارية للارتباطات
estat graph, bootdist equation(5)        // توزيع إعادة المعاينة
estat graph, saving("figs/paper")        // تصدير PNG
""",
    language="stata",
)

st.markdown("## قائمة الفحص النهائية")

st.markdown(
    """
قبل أن تكتب النتائج في ورقتك:

1. :material/check_box_outline_blank: `estat serial` لا يرفض ← الإبطاءات كافية
2. :material/check_box_outline_blank: `estat sigma` يرفض القطرية ← SUR مبرَّرة
3. :material/check_box_outline_blank: $T/N \\geq 5$ ← $\\hat\\Sigma$ موثوقة
4. :material/check_box_outline_blank: $\\hat\\lambda_i < 0$ في كل معادلة تدّعي وجود علاقة
5. :material/check_box_outline_blank: `bootstrap(999)` مُشغَّل والقيم الاحتمالية مُبلَّغة
6. :material/check_box_outline_blank: فترات Fieller أو Bootstrap للأجل الطويل
7. :material/check_box_outline_blank: تصحيح الاختبارات المتعددة مُطبَّق ومُعلَن
8. :material/check_box_outline_blank: الحالة الحتمية مُبرَّرة ومُعلَنة
"""
)

signature()

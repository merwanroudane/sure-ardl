import streamlit as st

from lib.ui import hero, rtl_css, signature, warn

rtl_css()

hero("المراجع والمصطلحات", "من أين جاء كل شيء، وما يقابل كل مصطلح")

st.markdown("## المراجع الأساسية")

st.markdown(
    """
**الورقة التي يشرحها هذا الدليل**

> Arif, M. A., and F. Furuoka (2026). *Seemingly Unrelated Cointegrating
> Regressions with Autoregressive Distributed Lag Dynamics: Estimation,
> Bounds Testing, and Cross-Equation Inference.* Research Square.
> [doi:10.21203/rs.3.rs-9237078/v1](https://doi.org/10.21203/rs.3.rs-9237078/v1)

**المنهجيتان الأصليتان**

> Zellner, A. (1962). An efficient method of estimating seemingly unrelated
> regressions and tests for aggregation bias. *Journal of the American
> Statistical Association* 57: 348–368.
> [doi:10.1080/01621459.1962.10480664](https://doi.org/10.1080/01621459.1962.10480664)

> Pesaran, M. H., Y. Shin, and R. J. Smith (2001). Bounds testing approaches
> to the analysis of level relationships. *Journal of Applied Econometrics*
> 16: 289–326. [doi:10.1002/jae.616](https://doi.org/10.1002/jae.616)

> Pesaran, M. H., and Y. Shin (1999). An autoregressive distributed lag
> modelling approach to cointegration analysis. In *Econometrics and Economic
> Theory in the 20th Century*, ed. S. Strom, 371–413. Cambridge University Press.

**القيم الحرجة**

> Narayan, P. K. (2005). The saving and investment nexus for China: Evidence
> from cointegration tests. *Applied Economics* 37: 1979–1990.
> [doi:10.1080/00036840500278103](https://doi.org/10.1080/00036840500278103)

> Kripfganz, S., and D. C. Schneider (2020). Response surface regressions for
> critical value bounds and approximate p-values in equilibrium correction
> models. *Oxford Bulletin of Economics and Statistics* 82: 1456–1481.
> [doi:10.1111/obes.12377](https://doi.org/10.1111/obes.12377)

**إعادة المعاينة**

> McNown, R., C. Y. Sam, and S. K. Goh (2018). Bootstrapping the
> autoregressive distributed lag test for cointegration. *Applied Economics*
> 50: 1509–1521.
> [doi:10.1080/00036846.2017.1366643](https://doi.org/10.1080/00036846.2017.1366643)

> Palm, F. C., S. Smeekes, and J.-P. Urbain (2010). A sieve bootstrap test
> for cointegration in a conditional error correction model. *Econometric
> Theory* 26: 647–681.
> [doi:10.1017/S0266466609990053](https://doi.org/10.1017/S0266466609990053)

**الأدبيات المنافسة**

> Wagner, M., P. Grabarczyk, and S. H. Hong (2020). Fully modified OLS
> estimation and inference for seemingly unrelated cointegrating polynomial
> regressions. *Journal of Econometrics* 218: 456–480.
> [doi:10.1016/j.jeconom.2019.05.012](https://doi.org/10.1016/j.jeconom.2019.05.012)

> Lin, Y., and H. Reuvers (2025). FM-GLS estimation and inference for
> seemingly unrelated cointegrating polynomial regressions. *Oxford Bulletin
> of Economics and Statistics*.
> [doi:10.1111/obes.70030](https://doi.org/10.1111/obes.70030)

**الاختبارات**

> Breusch, T. S., and A. R. Pagan (1980). The Lagrange multiplier test and
> its applications to model specification in econometrics. *Review of
> Economic Studies* 47: 239–253.
> [doi:10.2307/2297111](https://doi.org/10.2307/2297111)

> Pesaran, M. H. (2004). General diagnostic tests for cross section
> dependence in panels. Cambridge Working Papers in Economics 0435.

> Fieller, E. C. (1954). Some problems in interval estimation. *Journal of
> the Royal Statistical Society, Series B* 16: 175–185.
> [doi:10.1111/j.2517-6161.1954.tb00159.x](https://doi.org/10.1111/j.2517-6161.1954.tb00159.x)

**الأمر المرجعي في Stata للمعادلة الواحدة**

> Kripfganz, S., and D. C. Schneider (2023). ardl: Estimating autoregressive
> distributed lag and equilibrium correction models. *Stata Journal* 23:
> 983–1019.
> [doi:10.1177/1536867X231212434](https://doi.org/10.1177/1536867X231212434)
"""
)

st.caption(
    "كل المعرّفات الرقمية أعلاه جرى التحقق منها فردًا فردًا، بمطابقة العنوان "
    "والمؤلفين وأرقام الصفحات، لا بمجرد استجابة الرابط."
)

st.markdown("## مواضع تختلف فيها هذه المنصة عن نص المسودة")

warn(
    "الورقة الأصلية <b>مسودة لم تُحكَّم بعد</b>. وُجدت فيها مواضع تحتاج تنبيهًا، "
    "وقد عولجت في الأمر <code>surardl</code> وفي هذا الدليل كما يلي.",
    term="أمانة علمية",
)

st.markdown(
    """
**1. صيغة اختبار Pesaran CD — المعادلة (100)**

كما طُبعت، تُسقط العامل 2 تحت الجذر. الصيغة المستعملة هنا هي صيغة بيساران
الأصلية $\\;CD = \\sqrt{2T/(N(N-1))}\\sum_{i<j}\\hat r_{ij}$، وهي التي
تُعيد إنتاج القيمة $CD = 1.32$ المذكورة في القسم الخامس من الورقة انطلاقًا
من مصفوفة الارتباط في جدولها التاسع. الصيغة المطبوعة لا تُعيد إنتاجها.

**2. النظام المقيَّد في صيغة RSS — المعادلة (69)**

نص الورقة يقيّد **معادلة واحدة** ويترك الباقي حرًّا. لكن سكريبتات المؤلفين
المنشورة تقيّد **كل المعادلات** في آن واحد. الأمر يوفّر الصيغتين:
`fstat(rss)` لنص الورقة، و `fstat(rssall)` للسكريبتات.

**3. الحالة الحتمية في التطبيق المنشور**

السكريبتات المنشورة تُدخل اتجاهًا زمنيًا في النموذج غير المقيَّد وتحذفه من
المقيَّد، أي **الحالة الرابعة** بخمس قيود. لكن الجدول العاشر في الورقة
يُعاد إنتاجه بدقة **بالحالة الثالثة** بأربع قيود وبلا اتجاه، وباللوغاريتمات
لا بالمستويات.

**4. معالم المحاكاة في القسم 4.1**

النص يذكر $\\lambda = -0.3$ و $\\beta = -0.09$ و $\\theta = 0.3$ معًا، وهي
**غير متّسقة**، لأن $\\theta = -\\beta/\\lambda = -0.3$ بهذه القيم. المجموعة
المتّسقة التي تعطي $\\theta = 0.3$ هي $\\beta = +0.09$، وهي المستعملة في ملف
الاختبار الذاتي.

**5. أرقام معادلات غائبة**

القسمان 3.3 و4 يحيلان إلى المعادلات (159) و(164) و(170) و(178) و(189)–(195)،
وهي **غير موجودة** في المستند المكوّن من 58 صفحة. ولذلك أُعيد بناء مصفوفات
القيود لاختبارات قابلية التجميع وتساوي المعاملات **من نصّ الفرضيات** كما
ورد في القسم 4.5، لا من معادلة معروضة.

**6. كمية غير معرَّفة**

القسم الخامس يشير إلى «المعيار النسبي لفروبنيوس» لقياس جودة $\\hat\\Sigma$
دون تعريفه. الأمر يستعمل تعريفه الخاص
$\\;\\|\\Sigma - \\mathrm{diag}(\\Sigma)\\|_F / \\|\\Sigma\\|_F$
ويصرّح بذلك.

**7. المستودعات على GitHub**

المستودعان المنسوبان إلى المؤلف الثاني **ليسا حزمة تكرار** لهذه النسخة من
الورقة: بياناتهما تحوي تسعة متغيرات لكل دولة لا أربعة، وسكريبتاتهما تستعملان
الحالة الرابعة والمستويات، بينما الجداول المنشورة تُعاد بالحالة الثالثة
واللوغاريتمات. واستُعملا هنا مرجعًا تطبيقيًا ثانويًا لا مصدرًا للحجية.
"""
)

st.markdown("## معجم المصطلحات")

st.markdown(
    """
| بالعربية | English | الشرح المختصر |
|---|---|---|
| السكون | Stationarity | ثبات الخصائص الإحصائية مع الزمن |
| جذر الوحدة | Unit root | سمة السلسلة غير الساكنة |
| رتبة التكامل | Order of integration | عدد الفروق اللازمة للسكون |
| التكامل المشترك | Cointegration | وجود توليفة ساكنة من متغيرات غير ساكنة |
| الانحدار الزائف | Spurious regression | علاقة وهمية بين سلسلتين غير ساكنتين |
| نموذج تصحيح الخطأ | Error correction model | نموذج يجمع الأجلين القصير والطويل |
| سرعة التعديل | Speed of adjustment | $\\lambda$ — نسبة الانحراف المُصحَّح كل فترة |
| معامل الأجل الطويل | Long-run coefficient | $\\theta = -\\beta/\\lambda$ |
| الإبطاء الموزّع | Distributed lag | إدخال قيم سابقة للمتغيرات المفسّرة |
| اختبار الحدود | Bounds test | اختبار العلاقة طويلة الأجل بحدّين حرجين |
| الحالة الحتمية | Deterministic case | معاملة الثابت والاتجاه، من 1 إلى 5 |
| الحالة المنحلّة | Degenerate case | رفض زائف لفرضية العدم |
| انحدارات تبدو غير مترابطة | Seemingly unrelated regressions | نظام معادلات مرتبط عبر الأخطاء |
| التغاير اللحظي | Contemporaneous covariance | $\\Sigma$ — ترابط الأخطاء في اللحظة نفسها |
| التغاير طويل الأجل | Long-run covariance | $\\Omega$ — يشمل الترابط عبر الزمن |
| المربعات الصغرى المعمّمة الممكنة | Feasible GLS | تقدير بوزن مصفوفة تغاير مُقدَّرة |
| المعالم المزعجة | Nuisance parameters | معالم تُقدَّر دون أن تكون هدفًا |
| الخارجية الضعيفة | Weak exogeneity | شرط صحة النموذج المشروط |
| الترابط المقطعي | Cross-sectional dependence | ترابط الوحدات في اللحظة نفسها |
| الارتباط التسلسلي | Serial correlation | ترابط الخطأ مع قيمه السابقة |
| قابلية التجميع | Poolability | هل يصحّ فرض معاملات مشتركة؟ |
| طريقة دلتا | Delta method | تقريب تباين دالة غير خطية |
| مجموعة فييلر | Fieller set | فترة ثقة لنسبة، بلا قسمة |
| إعادة المعاينة | Bootstrap | توليد التوزيع من البيانات نفسها |
| فائق الاتساق | Super-consistency | تقارب بمعدل $T$ لا $\\sqrt{T}$ |
| التوزيع الطبيعي المختلط | Mixed normal | توزيع نهائي مشروط بمسار المتغيرات |
| تصحيح الاختبارات المتعددة | Multiple-testing correction | ضبط معدّل الخطأ عبر المقارنات |
"""
)

st.markdown("## عن هذه المنصة")

st.markdown(
    """
هذا الدليل مرافق للأمر **`surardl`** في Stata، وهو تنفيذ كامل لمنهجية
SUR-ARDL يشمل التقدير واختبار الحدود بأربعة مصادر للقيم الحرجة، ومعاملات
الأجل الطويل بثلاث طرق لفترات الثقة، والاختبارات العابرة للمعادلات،
وجداول ورسومًا بمستوى النشر.

```stata
ssc install surardl
help surardl
```

كُتب الدليل بحيث يُقرأ على ثلاثة مستويات: المبتدئ يبدأ من **الأساسيات**،
والمتخصص من **التفاصيل الرياضية**، والممارس من **التطبيق العملي**.
"""
)

signature()

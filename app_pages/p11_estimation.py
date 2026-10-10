import streamlit as st

from lib.ui import hero, intuition, rtl_css, signature, step, warn

rtl_css()

hero("التقدير", "من الأمر إلى المخرجات — خطوة بخطوة")

st.markdown("## شكل البيانات المطلوب")

st.markdown(
    """
`surardl` يتوقّع **بانل طويل** (long panel): كل صف يمثّل وحدة في فترة زمنية.
وكل وحدة تصبح **معادلة** في النظام.
"""
)

c1, c2 = st.columns(2)
with c1:
    st.markdown("#### :green-badge[الشكل الصحيح]")
    st.code(
        """country  year   rec     gdp      fdi    to
      1   1990   21.56  4184.8   1.03   52.9
      1   1991   23.87  4456.9   1.27   54.8
      ...
      2   1990   11.19  1470.9   5.30  146.9
      2   1991   12.36  1545.0   8.14  159.3
      ...""",
        language="text",
    )
with c2:
    st.markdown("#### :red-badge[الشكل الخاطئ — عريض]")
    st.code(
        """year   rec1    rec2    gdp1     gdp2   ...
1990   21.56   11.19   4184.8   1470.9
1991   23.87   12.36   4456.9   1545.0
...""",
        language="text",
    )
    st.caption("إن كانت بياناتك عريضة، حوّلها بـ `reshape long`.")

st.code(
    """
* التحويل من عريض إلى طويل عند الحاجة
reshape long rec gdp fdi to, i(year) j(country)
xtset country year
""",
    language="stata",
)

warn(
    "<code>xtset</code> <b>شرط لا بد منه</b>. الأمر يقرأ منه متغيّر الوحدة "
    "ومتغيّر الزمن والفاصل الزمني، ويتوقف برسالة واضحة إن لم تفعل.",
    term="لا تنسَ",
)

st.markdown("## بنية الأمر")

st.code("surardl depvar indepvars [if] [in] [, options]", language="stata")

st.markdown(
    """
:material/priority_high: **المتغيرات تُدخل في المستويات، لا في الفروق.** الأمر
يبني صيغة تصحيح الخطأ بنفسه: يحسب $\\Delta y$ و $y_{t-1}$ و $x_{t-1}$ و
$\\Delta x$ داخليًا. إن أدخلت `D.y` فستحصل على نموذج مختلف تمامًا.
"""
)

st.markdown("## أبسط صورة")

st.code(
    """
use surardl_asean6, clear
generate double lrec = ln(rec)
generate double lgdp = ln(gdp)
generate double lfdi = ln(fdi + 4)
generate double lto  = ln(to)
xtset country year

surardl lrec lgdp lfdi lto
""",
    language="stata",
)

st.markdown(
    """
هذا يكافئ `surardl lrec lgdp lfdi lto, case(3) lags(1) method(twostep)` —
أي ARDL(1,1,1,1) مع ثابت غير مقيَّد وبلا اتجاه، مقدَّرة بـ FGLS على خطوتين.
"""
)

st.markdown("## الخيارات المهمة")

t1, t2, t3, t4 = st.tabs(["بنية النموذج", "الحالة الحتمية", "طريقة التقدير", "الاستدلال"])

with t1:
    st.markdown(
        """
| الخيار | المعنى | مثال |
|---|---|---|
| `lags(p q1 ... qK)` | رتب ثابتة للجميع | `lags(2 1 1 1)` |
| `lags(#)` | الرتبة نفسها لكل المتغيرات | `lags(1)` |
| `maxlags(...)` + `bic` أو `aic` | اختيار آلي لكل وحدة | `maxlags(4) bic` |
| `qmin(#)` | أدنى رتبة للإبطاء الموزّع | `qmin(0)` |
| `lagmatrix(name)` | رتب يدوية لكل وحدة | مصفوفة $N\\times(K{+}1)$ |
"""
    )
    st.info(
        "**لماذا `qmin(1)` هو الافتراضي؟** لأن الحدّ المعاصر $\\Delta x_t$ هو ما "
        "يجعل خطأ النموذج المشروط متعامدًا مع ابتكارات المتغيرات المفسّرة "
        "(المعادلة A.13). إن سمحت بـ `qmin(0)` فقد يختار المعيار حذفه، "
        "وتسقط حجة الخارجية الضعيفة لذلك المتغيّر.",
        icon=":material/info:",
    )

with t2:
    st.markdown(
        """
| الخيار | الحالة | عدد القيود |
|---|---|---|
| `case(1)` أو `noconstant` | لا ثابت ولا اتجاه | $K+1$ |
| `case(2)` أو `restricted` | ثابت مقيَّد | $K+2$ |
| `case(3)` :green-badge[افتراضي] | ثابت غير مقيَّد | $K+1$ |
| `case(4)` أو `trend restricted` | اتجاه مقيَّد | $K+2$ |
| `case(5)` أو `trend` | اتجاه غير مقيَّد | $K+1$ |

`trendvar(varname)` يستعمل متغيّرًا موجودًا كاتجاه بدل التسلسل الافتراضي.
"""
    )

with t3:
    st.markdown(
        """
| الخيار | المعنى |
|---|---|
| `method(twostep)` :green-badge[افتراضي] | FGLS على خطوتين — كافٍ بحسب المحاكاة السادسة |
| `method(iterated)` | تكرار حتى الاستقرار ← مقدّر الإمكان الأعظم |
| `method(ols)` | معادلةً بمعادلة — للمقارنة فقط |
| `sigmadf(t)` :green-badge[افتراضي] | قسمة $\\hat\\Sigma$ على $T$ |
| `sigmadf(dfmax, dfk, dfk2)` | تصحيحات درجات حرية بديلة |
| `small` | إحصاءات $t$ و $F$ بدل $z$ و $\\chi^2$ |

:material/lightbulb: عندما تتساوى أعداد المتغيرات في كل المعادلات، تختلف خيارات
`sigmadf()` بعامل قياس فقط، فتغيّر **الأخطاء المعيارية** دون أن تغيّر
**التقديرات النقطية**.
"""
    )

with t4:
    st.markdown(
        """
| الخيار | المعنى |
|---|---|
| `fstat(wald)` :green-badge[افتراضي] | صيغة Wald — هي التي تُعيد إنتاج نتائج الورقة |
| `fstat(rss)` | صيغة مجموع المربعات، بتقييد معادلة واحدة |
| `fstat(rssall)` | بتقييد كل المعادلات — كما في سكريبتات المؤلفين |
| `bootstrap(#)` | قيم حرجة مُعايَرة على بياناتك :green-badge[موصى به] |
| `seed(#)` | بذرة التوليد العشوائي — للتكرار |
| `simulate(#)` | حدود $I(0)$ و $I(1)$ محاكاة للنظام |
| `level(#)` | مستوى الثقة |
"""
    )

st.markdown("## أمثلة متدرّجة")

step(1, "<b>التقدير الأساسي مع كل التشخيصات</b>")
st.code("surardl lrec lgdp lfdi lto, case(3) lags(1)", language="stata")

step(2, "<b>مع قيم حرجة مُعايَرة بإعادة المعاينة</b> — هذا ما ينبغي أن تبلّغه")
st.code(
    "surardl lrec lgdp lfdi lto, case(3) lags(1) bootstrap(999) seed(20261010)",
    language="stata",
)

step(3, "<b>مع اتجاه زمني واختيار آلي للإبطاءات</b>")
st.code("surardl lrec lgdp lfdi lto, case(5) maxlags(3) bic", language="stata")

step(4, "<b>مقارنة مع OLS لقياس المكسب</b>")
st.code(
    """
quietly surardl lrec lgdp lfdi lto, case(3) method(ols)
estimates store ols_model

quietly surardl lrec lgdp lfdi lto, case(3)
estimates store sur_model

estimates table ols_model sur_model, star stats(N T)
""",
    language="stata",
)

st.markdown("## قراءة الترويسة")

st.code(
    """--------------------------------------------------------------------------------
Seemingly unrelated ARDL (SUR-ARDL) error-correction model
--------------------------------------------------------------------------------
Two-step feasible GLS (Zellner SUR)        Equations     =        6
Dependent variable: D.lrec                 Time periods  =       34
Case 3: unrestricted constant, no trend    Observations  =      204
Panel: country   Time: year                Parameters    =       48
Lag structure: ARDL(1,1,1,1)               Restrictions  =        4""",
    language="text",
)

st.markdown(
    """
| السطر | المعنى | ما يجب أن تتحقق منه |
|---|---|---|
| `Equations = 6` | عدد الوحدات = عدد المعادلات | يطابق عدد وحداتك |
| `Time periods = 34` | $T$ الفعلي بعد خسارة الإبطاءات | 35 سنة − 1 إبطاء = 34 |
| `Observations = 204` | $N \\times T$ | 6 × 34 = 204 |
| `Parameters = 48` | $M$ = مجموع معالم النظام | 6 × 8 = 48 |
| `Restrictions = 4` | $q$ لاختبار الحدود | $K+1 = 3+1$ في الحالة 3 |

:material/warning: إن رأيت `Observations` أقل مما تتوقّع، فغالبًا هناك قيم
مفقودة أو فجوات زمنية. الأمر يستعمل **أطول مدى متّصل تكون فيه كل الوحدات
مرصودة**، ويطبع عدد الفترات المحذوفة.
"""
)

intuition(
    "لماذا يصرّ الأمر على نافذة متوازنة ومتّصلة؟<br><br>"
    "لأن $\\hat\\Sigma$ تُبنى من <b>حاصل ضرب البواقي في اللحظة نفسها</b>. "
    "إن كانت الدولة الأولى مرصودة سنة 1995 والثانية غير مرصودة، "
    "فلا يمكن حساب $\\hat\\sigma_{12}$ لتلك السنة. "
    "ولهذا يجب أن تكون المشاهدات <b>متزامنة</b>.",
    term="لماذا بانل متوازن؟",
)

st.markdown("## ماذا يُخزَّن بعد التقدير؟")

st.code(
    """
ereturn list

* أهم العناصر
matrix list e(b)          // متجه المعاملات، بأسماء [المعادلة]المتغيّر
matrix list e(V)          // مصفوفة التغاير الكاملة، بكتلها المتقاطعة
matrix list e(Sigma)      // مصفوفة التغاير اللحظي N×N
matrix list e(bounds)     // F و Wald و t و q و F على بيتا
matrix list e(longrun)    // معاملات الأجل الطويل بأخطائها
display e(bp)             // إحصاء Breusch-Pagan
display e(cd)             // إحصاء Pesaran CD
""",
    language="stata",
)

st.success(
    "لأن `e(b)` و `e(V)` مخزّنتان بالصيغة القياسية، فإن **كل أدوات Stata** "
    "تعمل بعدها: `test`, `lincom`, `nlcom`, `testnl`, `estimates store`. "
    "وكلها تستعمل مصفوفة التغاير الكاملة بكتلها المتقاطعة — وهذا بالضبط ما "
    "يجعل الاختبارات العابرة للمعادلات صحيحة.",
    icon=":material/check_circle:",
)

st.code(
    """
* اختبار فرق بين دولتين — يستعمل التغاير المتقاطع تلقائيًا
test [Thailand]L.lrec = [Vietnam]L.lrec

* معامل الأجل الطويل بطريقة دلتا، يدويًا
nlcom -_b[Thailand:L.lgdp] / _b[Thailand:L.lrec]
""",
    language="stata",
)

signature()

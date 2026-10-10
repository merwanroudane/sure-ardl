import streamlit as st

from lib.ui import hero, intuition, rtl_css, signature, step, warn

rtl_css()

hero("الاختبارات القبلية", "Pre-estimation — ما يجب فعله قبل كتابة أمر التقدير")

st.markdown(
    """
قبل أن تقدّر أي شيء، عليك الإجابة عن ثلاثة أسئلة. وكل سؤال له اختبار، وكل
نتيجة لها قرار عملي.
"""
)

st.mermaid_chart(
    """
flowchart TB
    S["البيانات الخام"] --> Q1["السؤال 1<br>ما رتب التكامل؟"]
    S --> Q2["السؤال 2<br>هل الأخطاء مترابطة بين الوحدات؟"]
    S --> Q3["السؤال 3<br>أي حالة حتمية؟"]

    Q1 --> T1["ADF · PP · KPSS"]
    Q2 --> T2["Breusch-Pagan · Pesaran CD"]
    Q3 --> T3["رسم البيانات + المنطق الاقتصادي"]

    T1 --> D1{"يوجد I(2)؟"}
    D1 -->|"نعم"| STOP["توقّف<br>النموذج غير صالح"]
    D1 -->|"لا"| OK1["تابع"]

    T2 --> D2{"رُفضت القطرية؟"}
    D2 -->|"لا"| OLS["استعمل OLS<br>لا فائدة من SUR"]
    D2 -->|"نعم"| OK2["تابع"]

    OK1 --> EST["جاهز للتقدير"]
    OK2 --> EST
    T3 --> EST

    style STOP fill:#FBEFF1,stroke:#D1495B,stroke-width:3px
    style OLS fill:#FBF4E8,stroke:#E08D3C,stroke-width:2px
    style EST fill:#E6F0E9,stroke:#2E8B6F,stroke-width:3px
"""
)

st.markdown("## السؤال الأول: ما رتب التكامل؟")

st.markdown(
    """
**لماذا نسأل؟** ليس لاختيار النموذج — فـ ARDL يعمل مع $I(0)$ و $I(1)$ معًا —
بل لسبب واحد فقط: **التأكد من عدم وجود $I(2)$**.
"""
)

step(1, "طبّق <b>ADF</b> على <b>مستوى</b> كل متغيّر في كل وحدة.")
step(2, "طبّق <b>ADF</b> على <b>الفرق الأول</b> لكل متغيّر لم يُرفض جذر الوحدة في مستواه.")
step(3, "طبّق <b>KPSS</b> كتأكيد، لأن فرضية عدمه معكوسة.")

st.markdown("### الأوامر في Stata")

st.code(
    """
* اختبار ADF لكل متغيّر في كل دولة
levelsof country, local(cids)
foreach v of varlist lrec lgdp lfdi lto {
    display _n "=== `v' ==="
    foreach i of local cids {
        quietly dfuller `v' if country == `i', lags(1) trend regress
        local a = r(Zt)
        quietly dfuller D.`v' if country == `i', lags(1) regress
        local b = r(Zt)
        display "  country `i':  level = " %7.3f `a' "   D. = " %7.3f `b'
    }
}

* اختبار KPSS (يحتاج تثبيتًا أولًا)
* ssc install kpss
* kpss lrec if country == 1, maxlag(3)
""",
    language="stata",
)

st.markdown("### كيف تقرأ النتيجة؟")

st.markdown(
    """
| ADF على المستوى | ADF على الفرق | الحكم | القرار |
|---|---|---|---|
| رُفض H₀ | — | $I(0)$ | :green-badge[مقبول] |
| لم يُرفض | رُفض H₀ | $I(1)$ | :green-badge[مقبول] |
| لم يُرفض | لم يُرفض | $I(2)$ أو أعلى | :red-badge[توقّف] |

القيمة الحرجة عند 5% تقارب $-2.98$ مع ثابت، و $-3.58$ مع ثابت واتجاه.
"""
)

intuition(
    "لا تقلق كثيرًا إن أعطت الاختبارات نتائج متضاربة بين المستوى والاتجاه، أو "
    "بين ADF و KPSS. <b>هذا بالضبط الموقف الذي صُمّمت له منهجية ARDL.</b><br><br>"
    "القلق الوحيد المشروع هو احتمال وجود $I(2)$ — وهذا يظهر بوضوح: "
    "متغيّر لا يصبح ساكنًا حتى بعد أخذ الفرق الأول.",
)

st.markdown("## السؤال الثاني: هل الأخطاء مترابطة بين الوحدات؟")

st.markdown(
    """
**لماذا نسأل؟** هذا السؤال يحدّد **هل تحتاج SUR أصلًا**. بموجب قضية زيلنر،
إذا كانت $\\Sigma$ قطرية فإن SUR = OLS تمامًا، ولا فائدة من التعقيد.
"""
)

st.markdown("### الاختباران")

c1, c2 = st.columns(2)
with c1:
    with st.container(border=True):
        st.markdown(
            "#### Breusch-Pagan LM\n"
            "$H_0$: كل $\\sigma_{ij} = 0$ عند $i \\neq j$\n\n"
            ":green-badge[الاختبار الأساسي]\n\n"
            "يربّع معاملات الارتباط، فيكشف الترابط **موجبًا كان أو سالبًا**. "
            "توزيعه $\\chi^2$ بدرجات حرية $N(N-1)/2$.\n\n"
            "**رفض H₀ ← استعمل SUR**"
        )
with c2:
    with st.container(border=True):
        st.markdown(
            "#### Pesaran CD\n"
            "$H_0$: استقلال مقطعي\n\n"
            ":orange-badge[اختبار تأكيدي فقط]\n\n"
            "يستعمل المعاملات **بإشاراتها**، فقد تتلاشى الإشارات المتعاكسة. "
            "صُمّم أصلًا لبانل كبير $N$، وقدرته **ضعيفة** عند $N$ صغيرة.\n\n"
            "**لا تبنِ قرارك عليه وحده**"
        )

st.markdown("### الأمر")

st.code(
    """
* الطريقة المباشرة: الأمر يحسبهما تلقائيًا ويعرضهما في كتلة التشخيص
surardl lrec lgdp lfdi lto, case(3) lags(1)

* أو بعد التقدير، مع مصفوفة الارتباط كاملة
estat sigma
""",
    language="stata",
)

st.markdown("### مثال من تطبيق الآسيان")

st.code(
    """   Breusch-Pagan LM (eq. 96-99)  chi2( 15) =   28.8419   p = 0.0169
   Pesaran CD (eq. 100)                      =    1.2988   p = 0.1940
   Mean absolute off-diagonal correlation    =    0.1898""",
    language="text",
)

st.success(
    "**كيف نقرأ هذا؟** اختبار LM يرفض عند 5% (p = 0.017) ← يوجد ترابط ← "
    "SUR مبرَّرة. أما CD فلا يرفض (p = 0.194)، وهذا **متوقّع ولا يناقض الأول**: "
    "مصفوفة الارتباط فيها قيم موجبة (0.548) وسالبة (−0.364) تتلاشى عند الجمع "
    "بالإشارات. ولهذا السبب بالذات يُعتمد اختبار LM لا CD.",
    icon=":material/lightbulb:",
)

warn(
    "إذا <b>لم يرفض</b> اختبار Breusch-Pagan، فالنتيجة ليست «فشلًا» بل معلومة "
    "مفيدة: وحداتك مستقلة، فاستعمل ARDL لكل وحدة على حدة بأمر "
    "<code>ardl</code>، واستفد من قيمه الحرجة الجاهزة. "
    "استعمال SUR عندها تعقيد بلا عائد.",
    term="ماذا لو لم يُرفض؟",
)

st.markdown("## السؤال الثالث: أي حالة حتمية؟")

st.markdown(
    """
هذا القرار **لا يُؤخذ بالاختبار الإحصائي**، بل بالنظر إلى البيانات والمنطق
الاقتصادي. وهو قرار مهم لأنه يحدّد عدد القيود $q$ والقيم الحرجة.
"""
)

st.code(
    """
* ارسم متغيراتك أولًا — هذه أهم خطوة
xtline lrec, overlay legend(rows(2))
xtline lgdp, overlay legend(rows(2))
""",
    language="stata",
)

st.markdown(
    """
| ما تراه في الرسم | الحالة | الأمر |
|---|---|---|
| لا اتجاه واضح، تذبذب حول مستوى | **3** | `case(3)` :green-badge[الافتراضي] |
| اتجاه واضح، وتعتقد أنه جزء من التوازن | **4** | `case(4)` |
| اتجاه واضح ومستقل عن العلاقة | **5** | `case(5)` |
| لا ثابت ولا اتجاه (نادر) | **1** | `noconstant` |
| ثابت مقيَّد ضمن العلاقة | **2** | `restricted` |
"""
)

warn(
    "<b>لا تجرّب الحالات الخمس وتختر التي تعطي أجمل نتيجة.</b> "
    "هذا تنقيب في البيانات، ويُبطل مستوى المعنوية المُعلن تمامًا. "
    "اختر الحالة <b>قبل</b> أن ترى النتائج، بناءً على الرسم والنظرية الاقتصادية، "
    "والتزم بها.<br><br>"
    "وإن أردت فحص الحساسية، فأعلن ذلك صراحة في ورقتك وأبلغ النتائج كلها.",
    term="خطأ منهجي شائع",
)

st.markdown("## قرار رابع: رتب الإبطاء")

st.markdown(
    """
ليس اختبارًا قبليًا بالمعنى الدقيق، لكنه قرار يُتخذ قبل التقدير النهائي.
أمامك خياران:
"""
)

c1, c2 = st.columns(2)
with c1:
    with st.container(border=True):
        st.markdown(
            "#### :material/push_pin: رتبة ثابتة\n"
            "```stata\nsurardl y x1 x2, lags(1)\n```\n"
            "ARDL(1,1,1) للجميع — وهو ما تعتمده الورقة في قسمها الخامس.\n\n"
            ":green-badge[بسيط] :green-badge[قابل للمقارنة]\n\n"
            "لكنه قد يترك ارتباطًا تسلسليًا."
        )
with c2:
    with st.container(border=True):
        st.markdown(
            "#### :material/auto_awesome: اختيار آلي\n"
            "```stata\nsurardl y x1 x2, maxlags(4) bic\n```\n"
            "لكل وحدة رتبها الخاصة، تُختار بمعيار معلوماتي.\n\n"
            ":green-badge[يعالج الارتباط التسلسلي]\n\n"
            "لكنه يتجاوز ما تغطّيه محاكاة الورقة."
        )

st.info(
    "**SBC أم AIC؟** معيار شوارتز (`bic`) أكثر تحفّظًا ويختار نماذج أبسط، "
    "ونارايان (2005) يوصي به للعينات الصغيرة. أما `aic` فيميل إلى رتب أعلى، "
    "وقد يكون مفيدًا إذا كان الارتباط التسلسلي عنيدًا. "
    "الافتراضي في `surardl` هو `bic`.",
    icon=":material/balance:",
)

st.markdown("## سيناريو كامل: من البيانات إلى الاستعداد للتقدير")

st.code(
    """
* ------------------------------------------------------------------
* 0. تحضير البيانات
* ------------------------------------------------------------------
use surardl_asean6, clear

generate double lrec = ln(rec)
generate double lgdp = ln(gdp)
generate double lfdi = ln(fdi + 4)      // FDI فيها قيم سالبة
generate double lto  = ln(to)

xtset country year                       // لا بد منه

* ------------------------------------------------------------------
* 1. فحص شكل البيانات: هل يوجد اتجاه؟
* ------------------------------------------------------------------
xtline lrec, overlay

* ------------------------------------------------------------------
* 2. رتب التكامل
* ------------------------------------------------------------------
foreach v of varlist lrec lgdp lfdi lto {
    forvalues i = 1/6 {
        quietly dfuller `v' if country == `i', lags(1) regress
        local lev = r(Zt)
        quietly dfuller D.`v' if country == `i', lags(1) regress
        display "`v' c`i':  level=" %7.2f `lev' "  diff=" %7.2f r(Zt)
    }
}

* ------------------------------------------------------------------
* 3. الترابط المقطعي — يظهر تلقائيًا في كتلة التشخيص
* ------------------------------------------------------------------
surardl lrec lgdp lfdi lto, case(3) lags(1)
estat sigma
""",
    language="stata",
)

signature()

import streamlit as st

from lib.ui import hero, rtl_css, signature

rtl_css()

hero("دليل أمر surardl", "المرجع الكامل لخيارات الأمر ومخرجاته")

st.markdown("## التثبيت")

st.code(
    """
ssc install surardl
net get surardl          // لجلب ملفات البيانات والأمثلة
help surardl
""",
    language="stata",
)

st.markdown("## البنية")

st.code("surardl depvar indepvars [if] [in] [, options]", language="stata")

st.markdown(
    """
البيانات **بانل طويل** معلَن بـ `xtset panelvar timevar`. كل وحدة = معادلة.
المتغيرات تُدخل في **المستويات**، والأمر يبني صيغة تصحيح الخطأ بنفسه.
"""
)

st.markdown("## جدول الخيارات الكامل")

tabs = st.tabs(["النموذج", "الحتمية", "التقدير", "اختبار الحدود", "العرض"])

with tabs[0]:
    st.markdown(
        """
| الخيار | المعنى | الافتراضي |
|---|---|---|
| `lags(numlist)` | رتب الإبطاء $p\\;q_1 \\dots q_K$ | `lags(1)` |
| `maxlags(numlist)` | أقصى رتب للاختيار الآلي | — |
| `aic` | الاختيار بمعيار أكايكي | — |
| `bic` | الاختيار بمعيار شوارتز | افتراضي مع `maxlags` |
| `lagmatrix(name)` | مصفوفة $N\\times(K{+}1)$ لرتب كل وحدة | — |
| `maxcombs(#)` | حدّ أقصى لعدد التوليفات | `20000` |
| `qmin(#)` | أدنى رتبة للإبطاء الموزّع | `1` |
"""
    )

with tabs[1]:
    st.markdown(
        """
| الخيار | المعنى | عدد القيود |
|---|---|---|
| `case(#)` | الحالة من 1 إلى 5 | `case(3)` |
| `noconstant` | يكافئ `case(1)` | $K+1$ |
| `trend` | يكافئ `case(5)` | $K+1$ |
| `restricted` | مع `trend` ← `case(4)`، بدونه ← `case(2)` | $K+2$ |
| `trendvar(varname)` | استعمال متغيّر موجود كاتجاه | — |
"""
    )

with tabs[2]:
    st.markdown(
        """
| الخيار | المعنى | الافتراضي |
|---|---|---|
| `method(twostep)` | FGLS على خطوتين | ✓ |
| `method(iterated)` | تكرار حتى الاستقرار ← ML | — |
| `method(ols)` | معادلةً بمعادلة | — |
| `iterate(#)` | حدّ التكرارات | `200` |
| `tolerance(#)` | عتبة التقارب | `1e-9` |
| `sigmadf(t)` | قسمة $\\hat\\Sigma$ على $T$ | ✓ |
| `sigmadf(dfmax)` | $T - \\max(m_i, m_j)$ | — |
| `sigmadf(dfk)` | مكافئ `sureg, dfk` | — |
| `sigmadf(dfk2)` | مكافئ `sureg, dfk2` | — |
| `small` | $t$ و $F$ بدل $z$ و $\\chi^2$ | — |
| `level(#)` | مستوى الثقة | `95` |
"""
    )

with tabs[3]:
    st.markdown(
        """
| الخيار | المعنى | الافتراضي |
|---|---|---|
| `fstat(wald)` | صيغة Wald، $F = W/q$ | ✓ |
| `fstat(rss)` | صيغة RSS بتقييد معادلة واحدة | — |
| `fstat(rssall)` | بتقييد كل المعادلات | — |
| `bootstrap(#)` | عدد تكرارات إعادة المعاينة | `0` |
| `seed(#)` | بذرة التوليد | `20261010` |
| `boottarget(equation)` | فرض العدم على المعادلة المختبَرة فقط | ✓ |
| `boottarget(joint)` | فرض العدم على كل المعادلات | — |
| `bootdgp(rw)` | المتغيرات المفسّرة كسير عشوائي | ✓ |
| `bootdgp(vecm)` | نموذج VECM هامشي مُقدَّر | — |
| `bootlags(#)` | رتبة النموذج الهامشي | `1` |
| `nodrift` | توليد $y^*$ بلا انجراف | — |
| `simulate(#)` | حدود $I(0)$ و $I(1)$ محاكاة | `0` |
| `simrho(#)` | ارتباط المتغيرات المفسّرة بين الوحدات | `0` |
"""
    )

with tabs[4]:
    st.markdown(
        """
| الخيار | المعنى |
|---|---|
| `bglags(#)` | رتبة اختبار بروش-غودفري |
| `eqnames(string)` | أسماء المعادلات |
| `noctable` | إخفاء جدول المعاملات |
| `noheader` | إخفاء الترويسة |
| `nolrtable` | إخفاء جدول الأجل الطويل |
| `nobounds` | إخفاء اختبار الحدود |
| `nodiagnostics` | إخفاء كتلة التشخيص |
| `graph` | رسم المجموعة القياسية |
"""
    )

st.markdown("## أوامر ما بعد التقدير")

st.markdown(
    """
| الأمر | الوظيفة |
|---|---|
| `estat bounds` | اختبار الحدود، ويقبل `bootstrap()` و `simulate()` لإعادة التقدير |
| `estat longrun` | معاملات الأجل الطويل، مع `fieller` و `bootstrap(#)` |
| `estat shortrun` | معاملات الأجل القصير والحدود الحتمية |
| `estat ecequal` | تساوي سرعات التعديل، مع `mtest()` |
| `estat lrequal [varlist]` | تساوي معاملات الأجل الطويل |
| `estat poolability` | قابلية التجميع، مع `lambda`/`shortrun`/`all` |
| `estat sigma` | مصفوفة التغاير والارتباط والتشخيصات |
| `estat serial` | بروش-غودفري، مع `lags(#)` |
| `estat efficiency` | المكسب في الكفاءة |
| `estat summary` | ملخّص كل معادلة |
| `estat graph` | الرسوم |
| `predict` | `residuals` · `olsresiduals` · `xb` · `ec` |
"""
)

st.markdown("## سيناريو كامل جاهز للنسخ")

st.code(
    """
* ==================================================================
* تحليل SUR-ARDL كامل
* ==================================================================
clear all
use surardl_asean6, clear

* --- التحويلات ---
generate double lrec = ln(rec)
generate double lgdp = ln(gdp)
generate double lfdi = ln(fdi + 4)
generate double lto  = ln(to)
xtset country year

* --- 1. فحص الشكل ---
xtline lrec, overlay

* --- 2. رتب التكامل ---
foreach v of varlist lrec lgdp lfdi lto {
    forvalues i = 1/6 {
        quietly dfuller `v' if country == `i', lags(1) regress
        local lv = r(Zt)
        quietly dfuller D.`v' if country == `i', lags(1) regress
        display "`v' c`i': level=" %7.2f `lv' "  diff=" %7.2f r(Zt)
    }
}

* --- 3. التقدير الأساسي ---
surardl lrec lgdp lfdi lto, case(3) lags(1)
estimates store base

* --- 4. هل التقدير النظامي مبرَّر؟ ---
estat sigma

* --- 5. هل الإبطاءات كافية؟ ---
estat serial, lags(2)
*    إن رُفضت الفرضية، أعد التقدير برتب أعلى:
*    surardl lrec lgdp lfdi lto, case(3) maxlags(3) bic

* --- 6. اختبار الحدود بقيم مُعايَرة ---
surardl lrec lgdp lfdi lto, case(3) lags(1) bootstrap(999) seed(20261010)

* --- 7. الأجل الطويل بفترات موثوقة ---
estimates restore base
estat longrun, fieller
estat longrun, bootstrap(999)

* --- 8. المقارنات بين الوحدات ---
estat ecequal, mtest(holm)
estat lrequal lgdp
estat poolability
estat efficiency

* --- 9. اختبارات بصيغتك أنت ---
test [Thailand]L.lrec = [Vietnam]L.lrec
nlcom -_b[Thailand:L.lgdp] / _b[Thailand:L.lrec]

* --- 10. الرسوم ---
estat graph
estat graph, saving("figs/paper")
""",
    language="stata",
)

st.markdown("## الملفات المرافقة")

st.markdown(
    """
| الملف | المحتوى |
|---|---|
| `surardl_asean6.dta` | بانل الآسيان الست، 1990–2024 |
| `surardl_asean6.do` | التطبيق المنشور كاملًا، خطوة بخطوة |
| `surardl_example.do` | اختبار ذاتي على بيانات معروفة الحقيقة |

:material/lightbulb: ملف `surardl_example.do` مفيد جدًا للتعلّم: يولّد بيانات
بمعالم **تعرفها سلفًا**، ثم يتحقق من أن الأمر يستردّها. تشغيله يطمئنك إلى
أن التثبيت سليم، ويريك كيف تتصرّف الاختبارات عندما تكون الحقيقة معلومة.
"""
)

st.code("do surardl_example.do", language="stata")

st.markdown("## التحقق من صحة الأمر")

st.markdown(
    """
الأمر مُختبَر مقابل مراجع خارجية لا مقابل نفسه:

| المرجع | النتيجة |
|---|---|
| `sureg` | تطابق حتى $10^{-10}$ على التصميم نفسه |
| `sureg, isure` | تطابق حتى ست منازل مع `method(iterated)` |
| `regress` + `test` | تطابق حتى ست منازل مع `method(ols)` |
| `nlcom` | أخطاء دلتا متطابقة |
| جدول PSS CI | محرك `simulate()` يُعيد إنتاج الحدود المنشورة عند $T=500$ |
| جداول الورقة | يُعيد إنتاج مصفوفة الارتباط وعمودَي OLS و SUR |
| DGP معروف الحقيقة | يستردّ المعالم؛ حجم الاختبار 0.040 عند 5%، والقوة 0.890 |
"""
)

signature()

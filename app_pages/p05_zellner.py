import streamlit as st

from lib.ui import definition, hero, intuition, rtl_css, signature, step, warn
from lib.viz import efficiency_gain_chart, sur_correlation_chart, sur_vs_ols_chart

rtl_css()

hero("Zellner 1962 — نظام SUR",
     "الانحدارات التي تبدو غير مترابطة — Seemingly Unrelated Regressions")

st.markdown(
    """
## القصة

سنة 1962 نشر **أرنولد زيلنر** ورقة في مجلة الجمعية الإحصائية الأمريكية
عنوانها: «طريقة كفؤة لتقدير الانحدارات التي تبدو غير مترابطة واختبارات
تحيّز التجميع».

العنوان نفسه يحمل المفتاح: **«تبدو» غير مترابطة**. أي أنها في الظاهر منفصلة،
لكنها في الحقيقة مرتبطة — والارتباط مخفيّ في مكان لا ينتبه إليه أحد:
**في الأخطاء**.
"""
)

st.markdown("## المشكلة")

st.markdown(
    """
لديك $N$ معادلة، كل واحدة لها متغيّرها التابع ومتغيراتها المفسّرة الخاصة:
"""
)

st.latex(r"""
\begin{aligned}
y_{1t} &= \mathbf{x}_{1t}'\boldsymbol{\theta}_1 + u_{1t} \\
y_{2t} &= \mathbf{x}_{2t}'\boldsymbol{\theta}_2 + u_{2t} \\
&\;\;\vdots \\
y_{Nt} &= \mathbf{x}_{Nt}'\boldsymbol{\theta}_N + u_{Nt}
\end{aligned}
""")

st.markdown(
    """
لا يوجد متغيّر مشترك بين المعادلات. لا توجد قيود على المعاملات. تبدو منفصلة
تمامًا، والبديهي أن تُقدّر كل واحدة بـ OLS وحدها.

**لكن زيلنر لاحظ شيئًا:** ماذا لو كانت الأخطاء في اللحظة نفسها مترابطة؟
"""
)

st.latex(r"E[u_{it}\, u_{jt}] = \sigma_{ij} \neq 0 \quad \text{عندما } i \neq j")

intuition(
    "تخيّل أنك تدرس <b>إنفاق خمس شركات على البحث والتطوير</b>، لكل شركة معادلتها "
    "ومتغيراتها.<br><br>"
    "الآن تحدث <b>أزمة مالية عالمية</b>. ماذا يحصل؟ كل الشركات الخمس تخفض "
    "إنفاقها أكثر مما تتوقعه معادلاتها. أي أن <b>أخطاء المعادلات الخمس تكون "
    "سالبة في الوقت نفسه</b>.<br><br>"
    "هذه معلومة! إذا رأيتَ خطأ المعادلة الأولى سالبًا بشدة، فأنت تعرف شيئًا عن "
    "خطأ المعادلة الثانية. <b>تقدير كل معادلة وحدها يرمي هذه المعلومة في سلّة "
    "المهملات.</b>",
)

st.markdown("## شاهد الارتباط")

rho = st.slider(
    "حرّك المؤشر لترى قوة الارتباط بين خطأي معادلتين (ρ)",
    -0.9, 0.9, 0.6, 0.1, key="rho_sur",
)
st.plotly_chart(sur_correlation_chart(rho), width="stretch")

if abs(rho) < 0.15:
    st.info("لا يوجد نمط. معرفة خطأ المعادلة الأولى لا تخبرك شيئًا عن الثانية "
            "← **لا فائدة من SUR هنا**.", icon=":material/info:")
elif rho > 0:
    st.success("نمط صاعد واضح: الأخطاء تتحرك في الاتجاه نفسه. "
               "**هنا تكسب SUR كفاءة.**", icon=":material/trending_up:")
else:
    st.success("نمط هابط: عندما يرتفع خطأ الأولى ينخفض خطأ الثانية. "
               "**هذا ارتباط أيضًا، وSUR تستفيد منه بالقدر نفسه.**",
               icon=":material/trending_down:")

st.markdown("## الحل الذي اقترحه زيلنر")

st.markdown("الفكرة: اجمع المعادلات في **نظام واحد**، ثم قدّرها معًا بأسلوب GLS.")

step(1, "<b>اكتب النظام في صورة مصفوفية.</b> كوّم المعادلات فوق بعضها بحيث تصبح "
        "مصفوفة المتغيرات المفسّرة <b>قطرية كتليًا</b> (block diagonal): لكل معادلة "
        "كتلتها الخاصة، والأصفار في بقية المواضع.")

st.latex(r"""
\mathbf{y}_t = \mathbf{Z}_t\boldsymbol{\theta} + \boldsymbol{\varepsilon}_t,
\qquad
\mathbf{Z}_t = \begin{pmatrix}
\mathbf{x}_{1t}' & \mathbf{0}' & \cdots & \mathbf{0}' \\
\mathbf{0}' & \mathbf{x}_{2t}' & \cdots & \mathbf{0}' \\
\vdots & \vdots & \ddots & \vdots \\
\mathbf{0}' & \mathbf{0}' & \cdots & \mathbf{x}_{Nt}'
\end{pmatrix}
""")

step(2, "<b>عرّف مصفوفة التغاير اللحظي.</b> هي مصفوفة $N \\times N$ تجمع كل "
        "الترابطات بين أخطاء المعادلات في اللحظة نفسها.")

st.latex(r"""
\boldsymbol{\Sigma} = E[\boldsymbol{\varepsilon}_t\boldsymbol{\varepsilon}_t'] =
\begin{pmatrix}
\sigma_{11} & \sigma_{12} & \cdots & \sigma_{1N} \\
\sigma_{21} & \sigma_{22} & \cdots & \sigma_{2N} \\
\vdots & \vdots & \ddots & \vdots \\
\sigma_{N1} & \sigma_{N2} & \cdots & \sigma_{NN}
\end{pmatrix}
""")

st.markdown(
    "القطر الرئيسي = تباين كل معادلة. وخارج القطر = **الترابط بين المعادلات**، "
    "وهو بالضبط ما نريد استغلاله."
)

step(3, "<b>قدّر $\\Sigma$ من بواقي OLS.</b> لا نعرف $\\Sigma$ الحقيقية، لذا "
        "نقدّرها على خطوتين: أولًا OLS لكل معادلة للحصول على البواقي، ثم:")

st.latex(r"\hat{\sigma}_{ij} = \frac{1}{T}\sum_{t=1}^{T}\hat{u}_{it}\,\hat{u}_{jt}")

step(4, "<b>طبّق GLS الممكن</b> (Feasible GLS) باستخدام $\\hat{\\Sigma}$ وزنًا:")

st.latex(r"""
\hat{\boldsymbol{\theta}}_{SUR} =
\left(\mathbf{Z}'\hat{\boldsymbol{\Omega}}^{-1}\mathbf{Z}\right)^{-1}
\mathbf{Z}'\hat{\boldsymbol{\Omega}}^{-1}\mathbf{Y},
\qquad
\hat{\boldsymbol{\Omega}} = \mathbf{I}_T \otimes \hat{\boldsymbol{\Sigma}}
""")

st.markdown(
    """
:material/info: الرمز $\\otimes$ هو **الجداء الكرونيكري** (Kronecker product).
معناه هنا بسيط: مصفوفة التغاير نفسها $\\Sigma$ تتكرّر في كل فترة زمنية، ولا
يوجد ترابط بين فترتين مختلفتين.
"""
)

st.markdown("## كم نربح؟ جرّبها بنفسك")

st.markdown(
    "هذه محاكاة حيّة: نولّد بيانات بمعامل حقيقي معروف، ثم نقدّره بالطريقتين "
    "مئتي مرة، ونرسم توزّع الخطأ."
)

c1, c2, c3 = st.columns(3)
with c1:
    sim_rho = st.slider("ρ — الارتباط بين الأخطاء", 0.0, 0.9, 0.7, 0.1, key="simrho")
with c2:
    sim_n = st.slider("N — عدد المعادلات", 2, 6, 4, 1, key="simn")
with c3:
    sim_t = st.slider("T — طول السلسلة", 30, 150, 60, 10, key="simt")

with st.spinner("جارٍ تشغيل المحاكاة…"):
    fig, re_ratio = sur_vs_ols_chart(sim_rho, sim_n, sim_t)
st.plotly_chart(fig, width="stretch")

mc1, mc2 = st.columns(2)
mc1.metric("الكفاءة النسبية RE", f"{re_ratio:.3f}",
           delta=f"{(re_ratio-1)*100:+.1f}% دقة" if re_ratio == re_ratio else None)
mc2.markdown(
    "**كيف تقرأ الرقم؟**  \n"
    "RE > 1 ← SUR أدقّ من OLS.  \n"
    "RE ≈ 1 ← لا فرق يُذكر.  \n"
    "القيمة = نسبة جذر متوسط مربعات الخطأ بين الطريقتين."
)

st.markdown("## النتيجة الأشهر: متى تتساوى SUR مع OLS؟")

definition(
    "قضية زيلنر — Zellner's Proposition",
    "مقدّر SUR <b>مطابق عدديًا</b> لمقدّر OLS معادلةً بمعادلة إذا تحقّق "
    "أحد شرطين:<br>"
    "<b>(أ)</b> مصفوفة التغاير قطرية: $\\sigma_{ij}=0$ لكل $i \\neq j$ "
    "— أي لا يوجد ترابط أصلًا.<br>"
    "<b>(ب)</b> المتغيرات المفسّرة متطابقة في كل المعادلات: "
    "$\\mathbf{X}_i = \\mathbf{X}_j$ لكل $i,j$.",
)

st.markdown(
    """
وهذه نتيجة عملية بالغة الأهمية، لأنها تقول لك **متى لا تحتاج SUR أصلًا**:

- إذا لم يرفض اختبار Breusch-Pagan فرضية أن $\\Sigma$ قطرية ← استخدم OLS وارتَح.
- أما الشرط (ب) فلا يتحقق عمليًا في بانل الدول، لأن لكل دولة بياناتها الخاصة.

وكلما **قوي الارتباط** و**اختلفت** المتغيرات المفسّرة بين المعادلات،
**زاد المكسب**.
"""
)

st.plotly_chart(efficiency_gain_chart(), width="stretch")

st.caption(
    "الأرقام مأخوذة من الجدولين 1 و2 في ورقة أريف وفوروكا (2026). "
    "لاحظ: عند ρ = 0 الكفاءة النسبية ≈ 1 تمامًا كما تتنبأ قضية زيلنر، "
    "وعند ρ = 0.8 مع خمس معادلات تصل إلى 1.79 — أي تحسّن 79% في الدقة."
)

warn(
    "<b>شرط لا غنى عنه:</b> لتكون $\\hat{\\Sigma}$ قابلة للانعكاس يجب أن يكون "
    "$T > N$. ورتبة $\\hat{\\Sigma}$ لا تتجاوز $\\min(T, N)$.<br><br>"
    "وحتى عند تحقق الشرط، فإن عدد المعالم الحرّة في $\\Sigma$ هو "
    "$N(N+1)/2$ وينمو <b>تربيعيًا</b> في $N$. فإذا كانت $N$ كبيرة نسبيًا إلى "
    "$T$، فالتقدير رديء حتى لو كان ممكنًا. القاعدة العملية: "
    "<b>$T/N \\geq 5$ على الأقل</b>.",
    term="حدود الطريقة",
)

st.markdown("## خلاصة الصفحة")

st.success(
    """
**ما قدّمه زيلنر سنة 1962:**

1. ملاحظة أن معادلات تبدو منفصلة قد تكون مرتبطة عبر أخطائها.
2. طريقة لاستغلال هذا الترابط: تقدير النظام كله بـ GLS الممكن.
3. برهان أن المكسب يختفي تمامًا إذا كانت المصفوفة قطرية.

**ما لم يعالجه:** زيلنر افترض أن المتغيرات **ساكنة**. لم يكن يفكّر في
السلاسل غير الساكنة ولا في التكامل المشترك — هذه أدبيات جاءت بعده بعقدين.
وهنا يأتي دور بيساران وشين وسميث.
""",
    icon=":material/check_circle:",
)

signature()

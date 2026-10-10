import streamlit as st

from lib.ui import definition, hero, rtl_css, signature, warn

rtl_css()

hero("الاشتقاق خطوة بخطوة", "كل معادلة، بأرقامها كما في الورقة الأصلية")

st.info(
    "هذه الصفحة للمتخصص. إن كنت مبتدئًا فيمكنك تخطّيها والعودة إليها لاحقًا — "
    "الفهم العملي للنموذج لا يتوقف عليها.",
    icon=":material/info:",
)

st.markdown("## 1. من ARDL إلى صيغة تصحيح الخطأ")

st.markdown("نبدأ من نموذج ARDL العام — **المعادلة (1)**:")
st.latex(r"""
Y_{i,t} = \mu_i + \delta_i t + \sum_{j=1}^{p_i}\phi_{j,i} Y_{i,t-j}
+ \sum_{k=1}^{K}\sum_{j=0}^{q_{k,i}}\varphi_{k,j,i} X_{k,i,t-j} + u_{i,t}
""")

st.markdown(
    "لتحويلها إلى صيغة تصحيح الخطأ نستخدم تفكيكين جبريين. "
    "**المعادلة (5)** للمتغيّر التابع:"
)
st.latex(r"""
\sum_{j=1}^{p_i}\phi_{j,i} Y_{i,t-j}
= \left(\sum_{j=1}^{p_i}\phi_{j,i}\right) Y_{i,t-1}
- \sum_{j=1}^{p_i-1}\left(\sum_{l=j+1}^{p_i}\phi_{l,i}\right)\Delta Y_{i,t-j}
""")

st.markdown("و**المعادلة (6)** لكل متغيّر مفسّر. بالتعويض نحصل على **المعادلة (7)**:")
st.latex(r"""
\Delta Y_{i,t} = \mu_i + \delta_i t + \lambda_i Y_{i,t-1}
+ \sum_{k=1}^{K}\beta_{k,i} X_{k,i,t-1}
+ \sum_{j=1}^{p_i-1}\psi_{j,i}\Delta Y_{i,t-j}
+ \sum_{k=1}^{K}\sum_{j=0}^{q_{k,i}-1}\gamma_{k,j,i}\Delta X_{k,i,t-j} + u_{i,t}
""")

st.markdown("حيث المعاملات الجديدة معرّفة بالمعادلات (8)-(11):")

c1, c2 = st.columns(2)
with c1:
    st.latex(r"\lambda_i = -\Big(1 - \sum_{j=1}^{p_i}\phi_{j,i}\Big) = -\Phi_i(1)")
    st.caption("المعادلة (8) — سرعة التعديل")
    st.latex(r"\psi_{j,i} = -\sum_{l=j+1}^{p_i}\phi_{l,i}")
    st.caption("المعادلة (10) — معاملات الفروق المُبطَّأة")
with c2:
    st.latex(r"\beta_{k,i} = \sum_{j=0}^{q_{k,i}}\varphi_{k,j,i} = \Psi_{k,i}(1)")
    st.caption("المعادلة (9) — معاملات المستويات المُبطَّأة")
    st.latex(r"\gamma_{k,0,i} = \varphi_{k,0,i}, \quad \gamma_{k,j,i} = -\sum_{l=j+1}^{q_{k,i}}\varphi_{k,l,i}")
    st.caption("المعادلة (11) — معاملات الأجل القصير")

definition(
    "نقطة جوهرية",
    "هذا التحويل <b>تطابق جبري تام</b>، ولا يفرض أي قيد. "
    "الصيغتان تعطيان البواقي نفسها و R² نفسه. "
    "الفائدة الوحيدة أن صيغة تصحيح الخطأ <b>تفصل</b> معالم الأجل الطويل "
    "($\\lambda_i$, $\\beta_{k,i}$) عن معالم الأجل القصير "
    "($\\psi_{j,i}$, $\\gamma_{k,j,i}$)، فتسهّل اختبار وجود العلاقة.",
)

st.markdown("## 2. بناء النظام")

st.markdown("متجه المتغيرات المفسّرة للوحدة $i$ — **المعادلة (14)**:")
st.latex(r"""
\mathbf{x}_{i,t} = \big(1,\; t,\; Y_{i,t-1},\; X_{1,i,t-1},\dots,X_{K,i,t-1},\;
\Delta X_{1,i,t},\dots,\Delta X_{K,i,t}\big)' \in \mathbb{R}^{m_i}
""")

st.markdown("بتكويم الوحدات في اللحظة $t$ — **المعادلتان (26) و(30)**:")
st.latex(r"""
\mathbf{y}_t = \mathbf{Z}_t\boldsymbol{\theta} + \boldsymbol{\varepsilon}_t,
\qquad
\mathbf{Z}_t = \mathrm{diag}\big(\mathbf{x}_{1,t}',\dots,\mathbf{x}_{N,t}'\big)
\in \mathbb{R}^{N\times M}
""")

st.markdown("وبالتكويم عبر الزمن نحصل على النظام الكامل — **المعادلة (32)**، مع بنية التغاير **(39)**:")
st.latex(r"""
\boldsymbol{\Omega} = E[\boldsymbol{\varepsilon}\boldsymbol{\varepsilon}']
= \mathbf{I}_T \otimes \boldsymbol{\Sigma},
\qquad
\boldsymbol{\Omega}^{-1} = \mathbf{I}_T \otimes \boldsymbol{\Sigma}^{-1}
""")

st.markdown("## 3. المقدّر")

st.markdown(
    "بدل بناء مصفوفة $NT \\times NT$، نستغل بنية الكتل. "
    "**المعادلتان (52) و(53)** تعطيان الكتل مباشرة:"
)

st.latex(r"""
\big[\mathbf{Z}_t'\boldsymbol{\Sigma}^{-1}\mathbf{Z}_t\big]_{i,j} = \sigma^{ij}\,\mathbf{x}_{i,t}\mathbf{x}_{j,t}'
\qquad\qquad
\big[\mathbf{Z}_t'\boldsymbol{\Sigma}^{-1}\mathbf{y}_t\big]_{i} = \sum_{j=1}^{N}\sigma^{ij}\,\mathbf{x}_{i,t}\,\Delta Y_{j,t}
""")

st.markdown(
    """
والمعادلة (53) هي **مصدر مكسب الكفاءة كله**: لاحظ أن المتغيّر التابع للمعادلة
$j$ يدخل في تقدير معاملات المعادلة $i$، بوزن $\\sigma^{ij}$. أي أن المعادلات
**تتبادل المعلومات**. وعندما تكون $\\Sigma$ قطرية تنعدم هذه الحدود ويختفي المكسب.
"""
)

st.latex(r"""
\hat{\boldsymbol{\theta}}_{SUR} = \mathbf{A}^{-1}\mathbf{b},
\qquad
\mathbf{A} = \sum_t \mathbf{Z}_t'\hat{\boldsymbol{\Sigma}}^{-1}\mathbf{Z}_t,
\qquad
\widehat{\mathrm{Var}}(\hat{\boldsymbol{\theta}}_{SUR}) = \mathbf{A}^{-1}
""")

st.markdown("## 4. اختبار الحدود في النظام")

st.markdown("فرضية العدم للوحدة $i$ — **المعادلة (61)**:")
st.latex(r"H_0^{(i)}:\; \lambda_i = \beta_{1,i} = \cdots = \beta_{K,i} = 0")

st.markdown("مصفوفة القيود على مستوى النظام — **المعادلة (64)**:")
st.latex(r"""
\tilde{\mathbf{R}}_i = \big(\mathbf{0}\;\;\big|\;\;\mathbf{R}_i\;\;\big|\;\;\mathbf{0}\big)
\in \mathbb{R}^{q\times M}
""")

st.markdown("**صيغة Wald** — المعادلة (77)، وهي الصيغة الافتراضية في `surardl`:")
st.latex(r"""
W_i^{SUR} = \big(\tilde{\mathbf{R}}_i\hat{\boldsymbol{\theta}}_{SUR}\big)'
\Big[\tilde{\mathbf{R}}_i\,\mathbf{A}^{-1}\,\tilde{\mathbf{R}}_i'\Big]^{-1}
\big(\tilde{\mathbf{R}}_i\hat{\boldsymbol{\theta}}_{SUR}\big),
\qquad
F_i^{SUR} = \frac{W_i^{SUR}}{q}
""")

st.markdown("**صيغة مجموع مربعات البواقي** — المعادلة (76):")
st.latex(r"""
F_i^{SUR} = \frac{\big(\mathrm{RSS}_R^{(i)} - \mathrm{RSS}_U^{(i)}\big)/q}
{\mathrm{RSS}_U^{(i)}/(T-m_i)}
""")

warn(
    "الورقة تقول إن الصيغتين <b>متكافئتان تقاربيًا</b>. وهذا صحيح، لكنهما "
    "<b>ليستا متساويتين في العينات المنتهية</b>: صيغة Wald تستعمل "
    "$\\hat{\\Sigma}$ بمقام $T$، بينما صيغة RSS تقسم على "
    "$\\mathrm{RSS}/(T-m_i)$. الفرق بينهما تقريبًا عامل "
    "$T/(T-m_i)$.<br><br>"
    "في تطبيق الآسيان ($T=34$, $m=8$) هذا العامل ≈ 1.31. "
    "ولهذا تعطي الصيغتان أرقامًا مختلفة: 8.63 مقابل 5.04 للفلبين.<br><br>"
    "<b>الصيغة التي تُعيد إنتاج الجدول العاشر في الورقة هي صيغة Wald</b>، "
    "وهي الافتراضية في الأمر. والخيار <code>fstat(rss)</code> يعطيك الأخرى.",
    term="فرق مهم بين الصيغتين",
)

st.markdown("**الاختبار المشترك لكل المعادلات** — المعادلتان (78)-(79):")
st.latex(r"""
W^{Joint} = \big(\tilde{\mathbf{R}}_{Joint}\hat{\boldsymbol{\theta}}\big)'
\Big[\tilde{\mathbf{R}}_{Joint}\mathbf{A}^{-1}\tilde{\mathbf{R}}_{Joint}'\Big]^{-1}
\big(\tilde{\mathbf{R}}_{Joint}\hat{\boldsymbol{\theta}}\big)
\;\sim\; \chi^2\big(N(K+1)\big)
""")

st.markdown("## 5. معاملات الأجل الطويل وأخطاؤها المعيارية")

st.markdown("من شرط التوازن — **المعادلات (80)-(82)**:")
st.latex(r"\theta_{k,i}^{LR} = -\frac{\beta_{k,i}}{\lambda_i}")

st.markdown("وبما أنها **نسبة**، نحتاج طريقة دلتا. التدرّج — **المعادلة (86)**:")
st.latex(r"""
\nabla g = \frac{\partial g}{\partial(\lambda_i,\beta_{k,i})}
= \begin{pmatrix} \beta_{k,i}/\lambda_i^2 \\[4pt] -1/\lambda_i \end{pmatrix}
""")

st.markdown("والتباين — **المعادلة (89)**:")
st.latex(r"""
\mathrm{Var}\big(\hat{\theta}_{k,i}^{LR}\big)
= \frac{\hat\beta_{k,i}^{2}}{\hat\lambda_i^{4}}\,v_{\lambda\lambda,i}
\;-\; \frac{2\hat\beta_{k,i}}{\hat\lambda_i^{3}}\,v_{\lambda\beta,ki}
\;+\; \frac{1}{\hat\lambda_i^{2}}\,v_{\beta\beta,ki}
""")

st.error(
    "**المحاكاة الخامسة في الورقة تكشف مشكلة خطيرة:** تغطية فترة الثقة بطريقة "
    "دلتا **منهارة**. عند $\\lambda = -0.3$ و $T = 100$، التغطية الفعلية 1.4% "
    "بدل 95%. والأسوأ: **التغطية تسوء كلما زاد $T$**.\n\n"
    "السبب أن $\\hat\\theta^{LR}$ **فائق الاتساق** (يتقارب بمعدل $T$) بينما الخطأ "
    "المعياري بطريقة دلتا مُعايَر لمقدّر يتقارب بمعدل $\\sqrt{T}$. "
    "فالنسبة $|\\hat\\theta - \\theta|/se$ **تتباعد** بمعدل $\\sqrt{T}$.",
    icon=":material/warning:",
)

st.markdown("### الحل: مجموعة Fieller")

st.markdown(
    """
بدل قسمة $\\hat\\beta$ على $\\hat\\lambda$، نعكس الاختبار
$H_0:\\; \\beta + \\theta\\lambda = 0$ — وهو **خطّي** في المعاملات ولا يقسم على شيء:
"""
)

st.latex(r"""
A\theta^2 + B\theta + C \leq 0,
\qquad
\begin{cases}
A = \hat\lambda^2 - z^2 v_{\lambda\lambda} \\
B = 2(\hat\beta\hat\lambda - z^2 v_{\lambda\beta}) \\
C = \hat\beta^2 - z^2 v_{\beta\beta}
\end{cases}
""")

st.markdown(
    """
| الحالة | المجموعة الناتجة | المعنى |
|---|---|---|
| $A>0$ و المميّز $>0$ | فترة محدودة | التعريف جيد — نتيجة عادية |
| $A>0$ و المميّز $\\leq 0$ | المجموعة الخالية | البيانات ترفض كل القيم |
| $A<0$ و المميّز $>0$ | **مجموعة غير محدودة** | $\\lambda$ ضعيف التعريف |
| $A \\leq 0$ و المميّز $\\leq 0$ | كل المستقيم الحقيقي | لا معلومة إطلاقًا |

:material/lightbulb: **المجموعة غير المحدودة ليست عيبًا، بل صدق.** عندما يكون
$\\lambda$ قريبًا من الصفر، البيانات فعلًا لا تحدّد النسبة. وفترة دلتا المحدودة
في تلك الحالة **تكذب عليك**. الأمر `estat longrun, fieller` يعطيك الجواب الصادق.
"""
)

st.markdown("## 6. اختبارات عبر المعادلات — المعادلتان (92)-(93)")

st.markdown("للفرق بين معاملين طويلي الأجل من وحدتين مختلفتين، نحتاج اليعقوبي:")
st.latex(r"""
\mathbf{J} = \begin{pmatrix}
\beta_{k,i}/\lambda_i^2 & -1/\lambda_i & 0 & 0 \\
0 & 0 & \beta_{k,j}/\lambda_j^2 & -1/\lambda_j
\end{pmatrix}
""")
st.latex(r"""
\mathrm{Var}\begin{pmatrix}\hat\theta_{k,i}^{LR}\\ \hat\theta_{k,j}^{LR}\end{pmatrix}
= \mathbf{J}\,\mathrm{Var}\big(\hat\lambda_i,\hat\beta_{k,i},\hat\lambda_j,\hat\beta_{k,j}\big)\,\mathbf{J}'
""")

st.success(
    "**الكتل خارج القطر هي بيت القصيد.** التغايرات "
    "$\\mathrm{Cov}(\\hat\\lambda_i, \\hat\\lambda_j)$ و "
    "$\\mathrm{Cov}(\\hat\\beta_{k,i}, \\hat\\beta_{k,j})$ تساوي **صفرًا بالتعريف** "
    "في التقدير معادلةً بمعادلة. ووجودها في النظام هو ما يجعل هذه الاختبارات "
    "صحيحة أصلًا.",
    icon=":material/key:",
)

st.markdown("## 7. اختبارات الترابط المقطعي")

c1, c2 = st.columns(2)
with c1:
    st.markdown("**Breusch-Pagan LM** — المعادلات (96)-(99):")
    st.latex(r"LM_{BP} = T\sum_{i=2}^{N}\sum_{j=1}^{i-1}\hat{r}_{ij}^{2} \;\sim\; \chi^2\!\Big(\frac{N(N-1)}{2}\Big)")
    st.caption("حساس لأي ترابط، موجبًا كان أو سالبًا، لأنه يربّع المعاملات.")
with c2:
    st.markdown("**Pesaran CD** — المعادلة (100):")
    st.latex(r"CD = \sqrt{\frac{2T}{N(N-1)}}\sum_{i=2}^{N}\sum_{j=1}^{i-1}\hat{r}_{ij} \;\sim\; N(0,1)")
    st.caption("يستعمل المعاملات بإشاراتها، فقد تتلاشى الإشارات المتعاكسة.")

warn(
    "<b>تصحيح:</b> المعادلة (100) كما طُبعت في المسودة <b>تُسقط العامل 2</b> "
    "تحت الجذر. الصيغة المستعملة هنا وفي الأمر <code>surardl</code> هي صيغة "
    "بيساران الأصلية، وهي التي تُعيد إنتاج القيمة $CD = 1.32$ المذكورة في "
    "القسم الخامس من الورقة انطلاقًا من مصفوفة الارتباط في جدولها التاسع. "
    "الصيغة المطبوعة لا تُعيد إنتاجها.",
    term="فرق عن نص المسودة",
)

signature()

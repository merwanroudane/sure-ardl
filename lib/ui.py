"""أدوات العرض المشتركة: تخطيط من اليمين إلى اليسار، وبطاقات، ومعادلات."""

from __future__ import annotations

import streamlit as st

# ----------------------------------------------------------------------
# ألوان المنصة، مطابقة لملف config.toml
# ----------------------------------------------------------------------
TEAL = "#1D7A8C"
ORANGE = "#E08D3C"
GREEN = "#2E8B6F"
RED = "#D1495B"
VIOLET = "#7D5BA6"
BLUE = "#2A6F97"
GOLD = "#D9A520"
GRAY = "#5C6B73"
INK = "#1B2A33"
PAPER = "#FEFCF7"

PALETTE = [TEAL, ORANGE, GREEN, RED, VIOLET, BLUE, GOLD, GRAY]


_RTL_CSS = """
<style>
/* ===== اتجاه الصفحة من اليمين إلى اليسار، والشريط الجانبي على اليمين ===== */
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stSidebar"],
[data-testid="stBottomBlockContainer"] {
    direction: rtl;
}
[data-testid="stAppViewContainer"] .stMarkdown,
[data-testid="stSidebar"] .stMarkdown {
    text-align: right;
}

/* القوائم تأخذ مسافتها من اليمين */
[data-testid="stMarkdownContainer"] ul,
[data-testid="stMarkdownContainer"] ol {
    padding-right: 1.4rem;
    padding-left: 0;
}

/* الجداول من اليمين */
[data-testid="stMarkdownContainer"] table th,
[data-testid="stMarkdownContainer"] table td {
    text-align: right;
}

/* ===== ما يجب أن يبقى من اليسار إلى اليمين ===== */
code, pre, kbd, samp,
[data-testid="stCode"], [data-testid="stCodeBlock"],
.katex, .katex-display,
[data-testid="stJson"], [data-testid="stDataFrame"] {
    direction: ltr;
    text-align: left;
    unicode-bidi: isolate;
}
.katex-display { text-align: center !important; }

/* ===== لمسات بصرية ===== */
h1, h2, h3 { letter-spacing: 0 !important; }

h2 {
    border-bottom: 3px solid #D8E3E6;
    padding-bottom: .35rem;
    margin-top: 1.6rem;
}

/* صندوق التعريف */
.sa-def {
    background: linear-gradient(95deg, #F1F7F8 0%, #FBF7F0 100%);
    border-right: 6px solid #1D7A8C;
    border-radius: 10px;
    padding: 1rem 1.15rem;
    margin: .85rem 0;
}
.sa-def .sa-term {
    font-weight: 800;
    color: #0B5767;
    font-size: 1.05em;
    display: block;
    margin-bottom: .3rem;
}

/* صندوق الحدس / التبسيط */
.sa-intuition {
    background: #FBF4E8;
    border-right: 6px solid #E08D3C;
    border-radius: 10px;
    padding: 1rem 1.15rem;
    margin: .85rem 0;
}
.sa-intuition .sa-term {
    font-weight: 800;
    color: #8A5415;
    display: block;
    margin-bottom: .3rem;
}

/* صندوق التحذير */
.sa-warn {
    background: #FBEFF1;
    border-right: 6px solid #D1495B;
    border-radius: 10px;
    padding: 1rem 1.15rem;
    margin: .85rem 0;
}
.sa-warn .sa-term {
    font-weight: 800;
    color: #96243A;
    display: block;
    margin-bottom: .3rem;
}

/* بطاقة الخطوة */
.sa-step {
    background: #F3F8F4;
    border: 1px solid #D3E3D7;
    border-radius: 12px;
    padding: .9rem 1.1rem;
    margin: .6rem 0;
}
.sa-step .sa-num {
    display: inline-block;
    background: #2E8B6F;
    color: #fff;
    width: 1.9rem; height: 1.9rem;
    line-height: 1.9rem;
    text-align: center;
    border-radius: 50%;
    font-weight: 800;
    margin-left: .55rem;
}

/* ترويسة الصفحة */
.sa-hero {
    background: linear-gradient(100deg, #1D7A8C 0%, #2E8B6F 55%, #E08D3C 130%);
    color: #fff;
    border-radius: 16px;
    padding: 1.5rem 1.7rem;
    margin-bottom: 1.1rem;
}
.sa-hero h1 { color: #fff !important; margin: 0 0 .35rem 0 !important; }
.sa-hero p  { color: #EAF6F8; margin: 0; font-size: 1.03em; }

/* شريط المصطلح الإنجليزي */
.sa-en {
    font-family: 'JetBrains Mono', monospace;
    direction: ltr;
    unicode-bidi: isolate;
    background: #E8F2F4;
    color: #0B5767;
    padding: .08em .45em;
    border-radius: 5px;
    font-size: .88em;
}
</style>
"""


def setup_page(title: str, icon: str = ":material/school:") -> None:
    """يضبط إعدادات الصفحة ويحقن تنسيق الاتجاه من اليمين إلى اليسار."""
    st.set_page_config(
        page_title=title,
        page_icon="📘",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.html(_RTL_CSS)


def rtl_css() -> None:
    """يحقن التنسيق فقط، للصفحات الفرعية."""
    st.html(_RTL_CSS)


def _box(html: str) -> None:
    """يعرض صندوقًا منسّقًا.

    نستعمل st.markdown لا st.html لأن st.html يمرّر الوسم كما هو دون معالجة
    الـ Markdown، فلا تُصيَّر صيغ LaTeX المكتوبة بين علامتي $ داخل الصندوق.
    """
    st.markdown(html, unsafe_allow_html=True)


def hero(title: str, subtitle: str) -> None:
    _box(f'<div class="sa-hero"><h1>{title}</h1><p>{subtitle}</p></div>')


def definition(term: str, body: str) -> None:
    _box(f'<div class="sa-def"><span class="sa-term">{term}</span>\n\n{body}</div>')


def intuition(body: str, term: str = "الفكرة ببساطة") -> None:
    _box(f'<div class="sa-intuition"><span class="sa-term">{term}</span>\n\n{body}</div>')


def warn(body: str, term: str = "انتبه") -> None:
    _box(f'<div class="sa-warn"><span class="sa-term">{term}</span>\n\n{body}</div>')


def step(number: int, body: str) -> None:
    _box(f'<div class="sa-step"><span class="sa-num">{number}</span>{body}</div>')


def en(text: str) -> str:
    """يُظهر مصطلحًا إنجليزيًا داخل نص عربي دون أن ينقلب اتجاهه."""
    return f'<span class="sa-en">{text}</span>'


def signature() -> None:
    """توقيع المؤلف في أسفل كل صفحة."""
    st.divider()
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown(
            "**إعداد: الدكتور مروان رودان**  \n"
            ":small[Dr Merwan Roudane]  \n"
            ":small[merwanroudane920@gmail.com · github.com/merwanroudane]"
        )
    with c2:
        st.markdown(
            ":small[هذه المنصة دليل تعليمي مرافق للأمر ]"
            ":small[**surardl**]"
            ":small[ في Stata.]"
        )

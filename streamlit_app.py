"""منصة SUR-ARDL التعليمية — دليل شامل للباحثين.

إعداد: الدكتور مروان رودان
"""

import streamlit as st

from lib.ui import setup_page

setup_page("دليل SUR-ARDL")

pages = {
    "البداية": [
        st.Page("app_pages/p00_home.py", title="الصفحة الرئيسية",
                icon=":material/home:", default=True),
        st.Page("app_pages/p01_why.py", title="لماذا هذا النموذج؟",
                icon=":material/help:"),
    ],
    "الأساسيات — ابدأ من هنا": [
        st.Page("app_pages/p02_timeseries.py", title="السلاسل الزمنية والسكون",
                icon=":material/show_chart:"),
        st.Page("app_pages/p03_cointegration.py", title="العلاقة طويلة الأجل",
                icon=":material/link:"),
        st.Page("app_pages/p04_ecm.py", title="نموذج تصحيح الخطأ",
                icon=":material/replay:"),
    ],
    "المنهجيتان": [
        st.Page("app_pages/p05_zellner.py", title="Zellner 1962 — نظام SUR",
                icon=":material/account_tree:"),
        st.Page("app_pages/p06_ardl.py", title="PSS 2001 — ARDL واختبار الحدود",
                icon=":material/timeline:"),
        st.Page("app_pages/p07_surardl.py", title="الدمج 2026 — SUR-ARDL",
                icon=":material/merge:"),
    ],
    "التفاصيل الرياضية": [
        st.Page("app_pages/p08_math.py", title="الاشتقاق خطوة بخطوة",
                icon=":material/functions:"),
        st.Page("app_pages/p09_assumptions.py", title="الشروط والافتراضات",
                icon=":material/rule:"),
    ],
    "التطبيق العملي": [
        st.Page("app_pages/p10_pretests.py", title="الاختبارات القبلية",
                icon=":material/fact_check:"),
        st.Page("app_pages/p11_estimation.py", title="التقدير",
                icon=":material/calculate:"),
        st.Page("app_pages/p12_posttests.py", title="الاختبارات البعدية",
                icon=":material/verified:"),
        st.Page("app_pages/p13_results.py", title="قراءة النتائج",
                icon=":material/table_chart:"),
    ],
    "المرجع": [
        st.Page("app_pages/p14_stata.py", title="دليل أمر surardl",
                icon=":material/terminal:"),
        st.Page("app_pages/p15_pitfalls.py", title="أخطاء شائعة",
                icon=":material/warning:"),
        st.Page("app_pages/p16_refs.py", title="المراجع والمصطلحات",
                icon=":material/menu_book:"),
    ],
}

page = st.navigation(pages)
page.run()

"""رسوم ومخططات وأنيميشن تعليمية."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from lib.ui import BLUE, GOLD, GRAY, GREEN, ORANGE, PALETTE, RED, TEAL, VIOLET

LAYOUT = dict(
    paper_bgcolor="#FEFCF7",
    plot_bgcolor="#FFFFFF",
    font=dict(family="Tajawal, sans-serif", size=14, color="#1B2A33"),
    margin=dict(l=40, r=40, t=60, b=40),
    hoverlabel=dict(font_family="Tajawal, sans-serif"),
)


def _fig(title: str = "", height: int = 380) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor="center", font=dict(size=17)),
        height=height,
        **LAYOUT,
    )
    fig.update_xaxes(gridcolor="#EDF2F3", zerolinecolor="#D8E3E6")
    fig.update_yaxes(gridcolor="#EDF2F3", zerolinecolor="#D8E3E6")
    return fig


# ======================================================================
# 1. السكون مقابل عدم السكون
# ======================================================================
@st.cache_data
def _stationarity_data(seed: int = 7, n: int = 200):
    rng = np.random.default_rng(seed)
    e = rng.standard_normal(n)
    stationary = np.zeros(n)
    for t in range(1, n):
        stationary[t] = 0.5 * stationary[t - 1] + e[t]
    rw = np.cumsum(e)
    rw_drift = np.cumsum(e + 0.12)
    return stationary, rw, rw_drift


def stationarity_chart() -> go.Figure:
    stationary, rw, rw_drift = _stationarity_data()
    t = np.arange(len(stationary))
    fig = _fig("ثلاث سلاسل: واحدة ساكنة واثنتان غير ساكنتين", 400)
    fig.add_trace(go.Scatter(x=t, y=stationary, name="I(0) ساكنة",
                             line=dict(color=GREEN, width=2)))
    fig.add_trace(go.Scatter(x=t, y=rw, name="I(1) سير عشوائي",
                             line=dict(color=TEAL, width=2)))
    fig.add_trace(go.Scatter(x=t, y=rw_drift, name="I(1) مع انجراف",
                             line=dict(color=ORANGE, width=2)))
    fig.add_hline(y=0, line=dict(color=GRAY, dash="dot", width=1))
    fig.update_layout(legend=dict(orientation="h", y=1.14, x=0.5, xanchor="center"))
    fig.update_xaxes(title="الزمن t")
    return fig


# ======================================================================
# 2. التكامل المشترك: سلسلتان تتجولان معًا
# ======================================================================
@st.cache_data
def _coint_data(seed: int = 11, n: int = 200, theta: float = 0.8, coint: bool = True):
    rng = np.random.default_rng(seed)
    x = np.cumsum(rng.standard_normal(n))
    if coint:
        err = np.zeros(n)
        e = rng.standard_normal(n)
        for t in range(1, n):
            err[t] = 0.6 * err[t - 1] + e[t]
        y = 2.0 + theta * x + err
    else:
        y = np.cumsum(rng.standard_normal(n)) + 10
    return x, y


def cointegration_chart(coint: bool = True) -> go.Figure:
    x, y = _coint_data(coint=coint)
    t = np.arange(len(x))
    title = ("متغيران متكاملان تكامُلًا مشتركًا: يتجولان معًا"
             if coint else "متغيران غير متكاملين: كل واحد في طريقه")
    fig = _fig(title, 360)
    fig.add_trace(go.Scatter(x=t, y=y, name="y", line=dict(color=TEAL, width=2.2)))
    fig.add_trace(go.Scatter(x=t, y=x, name="x", line=dict(color=ORANGE, width=2.2)))
    fig.update_layout(legend=dict(orientation="h", y=1.14, x=0.5, xanchor="center"))
    fig.update_xaxes(title="الزمن t")
    return fig


def cointegration_residual_chart(coint: bool = True) -> go.Figure:
    x, y = _coint_data(coint=coint)
    beta = np.polyfit(x, y, 1)[0]
    resid = y - beta * x
    t = np.arange(len(x))
    title = ("الفارق بينهما يعود دائمًا إلى متوسطه ← يوجد توازن طويل الأجل"
             if coint else "الفارق بينهما يتيه بلا عودة ← لا يوجد توازن")
    fig = _fig(title, 300)
    fig.add_trace(go.Scatter(x=t, y=resid, name="y − θx",
                             line=dict(color=GREEN if coint else RED, width=2),
                             fill="tozeroy",
                             fillcolor="rgba(46,139,111,.14)" if coint
                             else "rgba(209,73,91,.14)"))
    fig.add_hline(y=float(resid.mean()), line=dict(color=GRAY, dash="dash"))
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title="الزمن t")
    return fig


# ======================================================================
# 3. أنيميشن: تصحيح الخطأ — كيف تعود y إلى التوازن
# ======================================================================
@st.cache_data
def _ecm_paths(lams=(-0.15, -0.35, -0.70), n: int = 40, shock: float = 1.0):
    """انحراف أوّلي قدره shock، ثم عودة بمعدل lambda في كل فترة."""
    out = {}
    for lam in lams:
        gap = np.zeros(n)
        gap[0] = shock
        for t in range(1, n):
            gap[t] = gap[t - 1] + lam * gap[t - 1]
        out[lam] = gap
    return out


def ecm_animation() -> go.Figure:
    paths = _ecm_paths()
    lams = list(paths.keys())
    n = len(next(iter(paths.values())))
    colors = {lams[0]: RED, lams[1]: ORANGE, lams[2]: GREEN}
    names = {
        lams[0]: "λ = −0.15 (تعديل بطيء)",
        lams[1]: "λ = −0.35 (تعديل متوسط)",
        lams[2]: "λ = −0.70 (تعديل سريع)",
    }

    fig = _fig("كيف يُغلق الانحراف عن التوازن طويل الأجل", 430)
    for lam in lams:
        fig.add_trace(go.Scatter(
            x=[0], y=[paths[lam][0]], mode="lines+markers",
            name=names[lam], line=dict(color=colors[lam], width=3),
            marker=dict(size=7),
        ))
    fig.add_hline(y=0, line=dict(color=GRAY, dash="dash"),
                  annotation_text="التوازن طويل الأجل",
                  annotation_position="bottom left")

    frames = []
    for k in range(1, n + 1):
        frames.append(go.Frame(
            name=str(k),
            data=[go.Scatter(x=np.arange(k), y=paths[lam][:k],
                             mode="lines+markers",
                             line=dict(color=colors[lam], width=3),
                             marker=dict(size=6))
                  for lam in lams],
        ))
    fig.frames = frames

    fig.update_layout(
        xaxis=dict(range=[-1, n], title="عدد الفترات بعد الصدمة"),
        yaxis=dict(range=[-0.1, 1.12], title="حجم الانحراف عن التوازن"),
        legend=dict(orientation="h", y=1.14, x=0.5, xanchor="center"),
        updatemenus=[dict(
            type="buttons", direction="left",
            x=0.5, xanchor="center", y=-0.18, yanchor="top",
            showactive=False, pad=dict(t=8),
            buttons=[
                dict(label="▶  شغّل", method="animate",
                     args=[None, dict(frame=dict(duration=90, redraw=True),
                                      fromcurrent=True,
                                      transition=dict(duration=0))]),
                dict(label="⏸  أوقف", method="animate",
                     args=[[None], dict(frame=dict(duration=0, redraw=False),
                                        mode="immediate")]),
            ],
        )],
    )
    return fig


# ======================================================================
# 4. فكرة SUR: الارتباط بين أخطاء المعادلات
# ======================================================================
@st.cache_data
def _sur_scatter(rho: float, seed: int = 3, n: int = 220):
    rng = np.random.default_rng(seed)
    z = rng.standard_normal(n)
    u1 = z * np.sqrt(abs(rho)) + rng.standard_normal(n) * np.sqrt(1 - abs(rho))
    u2 = z * np.sqrt(abs(rho)) + rng.standard_normal(n) * np.sqrt(1 - abs(rho))
    if rho < 0:
        u2 = -u2
    return u1, u2


def sur_correlation_chart(rho: float) -> go.Figure:
    u1, u2 = _sur_scatter(rho)
    fig = _fig(f"أخطاء معادلتين في اللحظة نفسها (ρ = {rho:.1f})", 360)
    fig.add_trace(go.Scatter(
        x=u1, y=u2, mode="markers",
        marker=dict(size=7, color=TEAL, opacity=0.55,
                    line=dict(width=0.5, color="#FFFFFF")),
        name="",
    ))
    if abs(rho) > 0.05:
        b = np.polyfit(u1, u2, 1)
        xs = np.linspace(u1.min(), u1.max(), 50)
        fig.add_trace(go.Scatter(x=xs, y=np.polyval(b, xs), mode="lines",
                                 line=dict(color=ORANGE, width=3), name=""))
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title="خطأ المعادلة الأولى  u₁ₜ")
    fig.update_yaxes(title="خطأ المعادلة الثانية  u₂ₜ")
    return fig


def efficiency_gain_chart() -> go.Figure:
    """مكاسب الكفاءة كما وردت في الجدولين 1 و2 من الورقة."""
    rho = [0.0, 0.3, 0.6, 0.8]
    n2 = [0.989, 1.047, 1.187, 1.423]
    n3 = [0.989, 1.060, 1.272, 1.629]
    n5 = [0.991, 1.072, 1.351, 1.790]
    fig = _fig("كم تربح الكفاءة كلما قوي الارتباط بين المعادلات؟", 380)
    for name, vals, c in [("N = 2 معادلتان", n2, GOLD),
                          ("N = 3 معادلات", n3, TEAL),
                          ("N = 5 معادلات", n5, GREEN)]:
        fig.add_trace(go.Scatter(x=rho, y=vals, mode="lines+markers", name=name,
                                 line=dict(color=c, width=3),
                                 marker=dict(size=10)))
    fig.add_hline(y=1.0, line=dict(color=RED, dash="dash"),
                  annotation_text="لا ربح ولا خسارة")
    fig.update_xaxes(title="ρ — قوة الارتباط بين أخطاء المعادلات")
    fig.update_yaxes(title="الكفاءة النسبية RE = RMSE(OLS) / RMSE(SUR)")
    fig.update_layout(legend=dict(orientation="h", y=1.14, x=0.5, xanchor="center"))
    return fig


# ======================================================================
# 5. منطق اختبار الحدود
# ======================================================================
def bounds_decision_chart(fstat: float, lower: float, upper: float) -> go.Figure:
    top = max(upper * 1.65, fstat * 1.25, 10)
    fig = _fig("أين يقع إحصاؤك بين الحدّين؟", 300)

    fig.add_shape(type="rect", x0=0, x1=lower, y0=0, y1=1,
                  fillcolor="rgba(46,139,111,.16)", line_width=0)
    fig.add_shape(type="rect", x0=lower, x1=upper, y0=0, y1=1,
                  fillcolor="rgba(217,165,32,.20)", line_width=0)
    fig.add_shape(type="rect", x0=upper, x1=top, y0=0, y1=1,
                  fillcolor="rgba(209,73,91,.16)", line_width=0)

    fig.add_annotation(x=lower / 2, y=0.78, text="لا نرفض H₀<br>لا توجد علاقة",
                       showarrow=False, font=dict(size=13, color="#1F6B55"))
    fig.add_annotation(x=(lower + upper) / 2, y=0.78, text="غير حاسم",
                       showarrow=False, font=dict(size=13, color="#8A6A12"))
    fig.add_annotation(x=(upper + top) / 2, y=0.78, text="نرفض H₀<br>توجد علاقة",
                       showarrow=False, font=dict(size=13, color="#96243A"))

    for val, lab, col in [(lower, f"I(0) = {lower:.2f}", GREEN),
                          (upper, f"I(1) = {upper:.2f}", RED)]:
        fig.add_vline(x=val, line=dict(color=col, width=2, dash="dash"),
                      annotation_text=lab, annotation_position="top")

    fig.add_trace(go.Scatter(
        x=[fstat], y=[0.34], mode="markers+text",
        marker=dict(size=22, color=TEAL, symbol="diamond",
                    line=dict(width=2.5, color="#FFFFFF")),
        text=[f"F = {fstat:.2f}"], textposition="bottom center",
        textfont=dict(size=15, color=TEAL), name="",
    ))
    fig.update_layout(showlegend=False)
    fig.update_yaxes(visible=False, range=[0, 1])
    fig.update_xaxes(title="قيمة إحصاء F", range=[0, top])
    return fig


# ======================================================================
# 6. تفكيك ARDL: من المستويات إلى صيغة تصحيح الخطأ
# ======================================================================
def ardl_decomposition_chart() -> go.Figure:
    """يوضّح أن الأجل القصير والأجل الطويل مكوّنان مختلفان داخل المعادلة نفسها."""
    fig = _fig("ماذا يقيس كل جزء من معادلة تصحيح الخطأ؟", 330)
    parts = ["الأجل الطويل<br>λ·y₍ₜ₋₁₎ + β·x₍ₜ₋₁₎",
             "الأجل القصير<br>γ·Δx₍ₜ₎",
             "المكوّن الحتمي<br>μ + δ·t",
             "الخطأ<br>u₍ₜ₎"]
    vals = [1, 1, 1, 1]
    cols = [TEAL, ORANGE, VIOLET, GRAY]
    fig.add_trace(go.Bar(x=parts, y=vals, marker_color=cols,
                         text=["يسحب نحو التوازن",
                               "الأثر الفوري",
                               "الاتجاه العام",
                               "ما لم يُفسَّر"],
                         textposition="inside",
                         insidetextfont=dict(color="#FFFFFF", size=13)))
    fig.update_layout(showlegend=False, bargap=0.35)
    fig.update_yaxes(visible=False)
    return fig


# ======================================================================
# 7. مقارنة أحجام مصفوفات المعالم المزعجة
# ======================================================================
def nuisance_dimension_chart() -> go.Figure:
    n = np.arange(2, 13)
    sur_ardl = n * n
    fm_sur = (2 * n) ** 2
    fig = _fig("عدد المعالم التي يجب تقديرها: لماذا SUR-ARDL أخف؟", 380)
    fig.add_trace(go.Scatter(x=n, y=fm_sur, mode="lines+markers",
                             name="FM-SUR: مصفوفة 2N×2N",
                             line=dict(color=RED, width=3),
                             marker=dict(size=9),
                             fill="tozeroy",
                             fillcolor="rgba(209,73,91,.10)"))
    fig.add_trace(go.Scatter(x=n, y=sur_ardl, mode="lines+markers",
                             name="SUR-ARDL: مصفوفة N×N",
                             line=dict(color=GREEN, width=3),
                             marker=dict(size=9),
                             fill="tozeroy",
                             fillcolor="rgba(46,139,111,.14)"))
    fig.update_xaxes(title="عدد الوحدات المقطعية N", dtick=1)
    fig.update_yaxes(title="عدد عناصر المصفوفة")
    fig.update_layout(legend=dict(orientation="h", y=1.14, x=0.5, xanchor="center"))
    return fig


# ======================================================================
# 8. محاكاة تفاعلية: SUR مقابل OLS
# ======================================================================
@st.cache_data(show_spinner=False)
def sur_vs_ols_sim(rho: float, n_eq: int, T: int, reps: int = 200, seed: int = 5):
    """محاكاة مبسّطة توضّح لماذا تتفوق SUR عند وجود ارتباط.

    نموذج مبسّط: y_i = a_i + b_i x_i + u_i، مع ارتباط ρ بين الأخطاء.
    نقارن تشتّت تقدير b_1 بين OLS و GLS الممكن.
    """
    rng = np.random.default_rng(seed)
    err_ols, err_sur = [], []
    for _ in range(reps):
        cf = rng.standard_normal(T)
        U = np.empty((T, n_eq))
        for i in range(n_eq):
            U[:, i] = np.sqrt(rho) * cf + np.sqrt(1 - rho) * rng.standard_normal(T)
        X = [rng.standard_normal(T) for _ in range(n_eq)]
        Y = [2.0 + 0.5 * X[i] + U[:, i] for i in range(n_eq)]

        b_ols = np.empty(n_eq)
        resid = np.empty((T, n_eq))
        Xd = []
        for i in range(n_eq):
            Z = np.column_stack([np.ones(T), X[i]])
            Xd.append(Z)
            bb = np.linalg.lstsq(Z, Y[i], rcond=None)[0]
            b_ols[i] = bb[1]
            resid[:, i] = Y[i] - Z @ bb
        err_ols.append(b_ols[0] - 0.5)

        S = resid.T @ resid / T
        try:
            Si = np.linalg.inv(S)
        except np.linalg.LinAlgError:
            continue
        m = 2
        A = np.zeros((n_eq * m, n_eq * m))
        bvec = np.zeros(n_eq * m)
        for i in range(n_eq):
            for j in range(n_eq):
                A[i * m:(i + 1) * m, j * m:(j + 1) * m] = Si[i, j] * (Xd[i].T @ Xd[j])
            bvec[i * m:(i + 1) * m] = sum(
                Si[i, j] * (Xd[i].T @ Y[j]) for j in range(n_eq)
            )
        th = np.linalg.solve(A, bvec)
        err_sur.append(th[1] - 0.5)

    return np.array(err_ols), np.array(err_sur)


def sur_vs_ols_chart(rho: float, n_eq: int, T: int) -> tuple[go.Figure, float]:
    e_ols, e_sur = sur_vs_ols_sim(rho, n_eq, T)
    rmse_ols = float(np.sqrt(np.mean(e_ols ** 2)))
    rmse_sur = float(np.sqrt(np.mean(e_sur ** 2)))
    fig = _fig("توزّع خطأ التقدير: كلما ضاق المنحنى كان التقدير أدقّ", 380)
    fig.add_trace(go.Histogram(x=e_ols, name="OLS معادلة بمعادلة",
                               marker_color=ORANGE, opacity=0.6, nbinsx=40))
    fig.add_trace(go.Histogram(x=e_sur, name="SUR نظام مشترك",
                               marker_color=TEAL, opacity=0.6, nbinsx=40))
    fig.add_vline(x=0, line=dict(color=GRAY, dash="dash"),
                  annotation_text="القيمة الحقيقية")
    fig.update_layout(barmode="overlay",
                      legend=dict(orientation="h", y=1.14, x=0.5, xanchor="center"))
    fig.update_xaxes(title="خطأ التقدير (المقدَّر − الحقيقي)")
    fig.update_yaxes(title="التكرار")
    return fig, (rmse_ols / rmse_sur if rmse_sur > 0 else float("nan"))

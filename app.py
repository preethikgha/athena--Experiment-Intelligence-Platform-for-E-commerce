import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import json

st.set_page_config(
    page_title="SmartShop A/B Testing",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .win-badge {
        background: #1a472a;
        color: #4ade80;
        border: 1px solid #4ade80;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .neutral-badge {
        background: #2d2d2d;
        color: #9ca3af;
        border: 1px solid #4b5563;
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.75rem;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #e2e8f0;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #2e3250;
    }
    .insight-box {
        background: #1a1f35;
        border-left: 4px solid #6366f1;
        border-radius: 0 8px 8px 0;
        padding: 14px 18px;
        margin: 8px 0;
        color: #cbd5e1;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ── sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.title("SmartShop A/B")
    st.caption("Experiment Intelligence Platform")
    st.divider()

    st.markdown("**Experiment Config**")
    st.markdown("**Name:** Checkout Recommender Test")
    st.markdown("**Period:** Oct 4 - Nov 18, 2015")
    st.markdown("**Goal:** Increase Purchase CVR")
    st.markdown("**Split:** 50 / 50")
    st.divider()

    st.markdown("**Models**")
    st.markdown("**Model A** — Purchase Popularity")
    st.markdown("**Model B** — Engagement Weighted")
    st.divider()

    st.markdown("**Statistical Config**")
    st.markdown("a = 0.05 (Bonferroni corrected to 0.0167)")
    st.markdown("Test: Two-sample t-test")
    st.markdown("Correction: Bonferroni (3 metrics)")

# ── load data ─────────────────────────────────────────────
with open("ab_results.json") as f:
    results = json.load(f)

control_df   = pd.read_csv("control_events.csv")
treatment_df = pd.read_csv("treatment_events.csv")

# ── header ────────────────────────────────────────────────
st.markdown("## SmartShop A/B Testing Dashboard")
st.markdown("**Retailrocket Dataset · 1.4M users · 2.75M events · 3 metrics**")
st.divider()

# ── overview cards ────────────────────────────────────────
st.markdown('<div class="section-header">Experiment Overview</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("Total Users", "1,407,580")
with c2:
    st.metric("Model A Users", "703,998")
with c3:
    st.metric("Model B Users", "703,582")
with c4:
    st.metric("Total Events", "2,756,101")
with c5:
    st.metric("SRM Status", "Clean", help="Chi-squared p=0.8051 — no sample ratio mismatch")

st.divider()

# ── main results ──────────────────────────────────────────
st.markdown('<div class="section-header">A/B Test Results</div>', unsafe_allow_html=True)

label_map = {
    "ctr":           "Click-through Rate",
    "cart_rate":     "Add-to-Cart Rate",
    "purchase_rate": "Purchase Conversion Rate"
}

for metric, r in results.items():
    label = label_map[metric]
    sig   = r["significant"]
    lift  = r["lift_pct"]

    with st.container():
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            st.markdown(f"### {label}")
            badge = '<span class="win-badge">SIGNIFICANT</span>' if sig else '<span class="neutral-badge">Not Significant</span>'
            st.markdown(badge, unsafe_allow_html=True)
            st.metric("Model A (Control)",   f"{r['control_mean']:.4f}")
            st.metric("Model B (Treatment)", f"{r['treatment_mean']:.4f}",
                      delta=f"{lift:+.2f}%",
                      delta_color="normal" if lift > 0 else "inverse")

        with col2:
            st.markdown("&nbsp;", unsafe_allow_html=True)
            st.markdown("&nbsp;", unsafe_allow_html=True)
            st.markdown(f"**p-value:** `{r['p_value']:.4f}`")
            st.markdown(f"**Bonferroni a:** `0.0167`")
            st.markdown(f"**Lift:** `{lift:+.2f}%`")
            verdict = "Inconclusive — need more data" if not sig else "Ship Model B"
            st.markdown(f"**Verdict:** {verdict}")

        with col3:
            fig = go.Figure()
            values = [r["control_mean"], r["treatment_mean"]]
            fig.add_trace(go.Bar(
                x=["Model A (Control)", "Model B (Treatment)"],
                y=values,
                marker_color=["#378ADD", "#1D9E75"],
                text=[f"{v:.4f}" for v in values],
                textposition="outside",
                width=0.4
            ))
            fig.add_hline(y=r["control_mean"], line_dash="dash",
                          line_color="#ff6b6b", opacity=0.6,
                          annotation_text="Baseline")
            fig.update_layout(
                height=220,
                margin=dict(t=30, b=10, l=10, r=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0"),
                yaxis=dict(gridcolor="#2e3250",
                           range=[0, max(values) * 1.35]),
                xaxis=dict(gridcolor="#2e3250")
            )
            st.plotly_chart(fig, use_container_width=True)

    st.divider()

# ── conversion funnel ─────────────────────────────────────
st.markdown('<div class="section-header">Conversion Funnel</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

def get_funnel(df):
    return [
        df["visitorid"].nunique(),
        df[df["event"] == "view"]["visitorid"].nunique(),
        df[df["event"] == "addtocart"]["visitorid"].nunique(),
        df[df["event"] == "transaction"]["visitorid"].nunique()
    ]

with col1:
    vals = get_funnel(control_df)
    fig = go.Figure(go.Funnel(
        y=["All Users", "Viewed", "Added to Cart", "Purchased"],
        x=vals,
        marker_color=["#378ADD", "#5b9bd5", "#3a7fc1", "#1a5fa8"],
        textinfo="value+percent initial"
    ))
    fig.update_layout(title="Model A (Control)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="#e2e8f0"),
                      height=350, margin=dict(t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    vals = get_funnel(treatment_df)
    fig = go.Figure(go.Funnel(
        y=["All Users", "Viewed", "Added to Cart", "Purchased"],
        x=vals,
        marker_color=["#1D9E75", "#25b585", "#1a8f69", "#0f6e52"],
        textinfo="value+percent initial"
    ))
    fig.update_layout(title="Model B (Treatment)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="#e2e8f0"),
                      height=350, margin=dict(t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── insights ──────────────────────────────────────────────
st.markdown('<div class="section-header">Experiment Insights</div>', unsafe_allow_html=True)

insights = [
    "Model B shows a consistent +1% lift in both cart and purchase rates — directionally positive but not yet statistically significant.",
    "SRM check passed (p=0.8051) — the 50/50 split is clean, so results are trustworthy and not due to assignment bugs.",
    "Bonferroni correction was applied across 3 metrics (a=0.0167 per metric) to prevent false positives from multiple comparisons.",
    "Recommended action: extend experiment duration or run power analysis to calculate the exact sample size needed for 80% power at +1% MDE.",
    "CTR is nearly identical across both groups (99.76% vs 99.75%) — the models differ mainly at the cart and purchase stage."
]

for insight in insights:
    st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)

st.divider()

# ── event volume ──────────────────────────────────────────
st.markdown('<div class="section-header">Event Volume by Variant</div>', unsafe_allow_html=True)

ctrl_counts = control_df["event"].value_counts().reset_index()
trt_counts  = treatment_df["event"].value_counts().reset_index()
ctrl_counts.columns = ["event", "count"]
trt_counts.columns  = ["event", "count"]
ctrl_counts["variant"] = "Model A (Control)"
trt_counts["variant"]  = "Model B (Treatment)"
combined = pd.concat([ctrl_counts, trt_counts])

fig = px.bar(combined, x="event", y="count", color="variant",
             barmode="group",
             color_discrete_map={
                 "Model A (Control)":   "#378ADD",
                 "Model B (Treatment)": "#1D9E75"
             })
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0"),
    height=350,
    legend=dict(bgcolor="rgba(0,0,0,0)"),
    yaxis=dict(gridcolor="#2e3250"),
    xaxis=dict(gridcolor="#2e3250"),
    margin=dict(t=20, b=20)
)
st.plotly_chart(fig, use_container_width=True)


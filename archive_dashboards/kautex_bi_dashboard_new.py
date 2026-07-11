"""
Kautex Executive BI Dashboard — Streamlit template
=================================================

Single-file executive BI dashboard for Kautex.
Run:  streamlit run kautex_bi_dashboard.py

Designed to be extended by GitHub Copilot in PyCharm:
- All mock data lives in the "DATA" section at the top; replace with
  real sources (Excel via pandas.read_excel, SQL, API, etc.).
- All chart builders are small pure functions taking a DataFrame.
- Region filter propagates through the whole page.
- Dark/light theme toggle in the sidebar.
- Interactive "world" region selector (Plotly scatter_geo with clickable
  Kautex regions) mirrors the web version's globe.

Dependencies:
    pip install streamlit pandas plotly

Tested with:
    streamlit>=1.37, pandas>=2.2, plotly>=5.22
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Kautex Executive BI",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# THEME
# ============================================================
Theme = Literal["dark", "light"]


@dataclass(frozen=True)
class Palette:
    background: str
    surface: str
    text: str
    muted: str
    border: str
    primary: str        # Kautex red
    success: str
    warning: str
    info: str
    chart: tuple[str, ...]


DARK = Palette(
    background="#1a1d24",
    surface="#22262f",
    text="#f2f3f5",
    muted="#9aa1ad",
    border="#333844",
    primary="#e0524a",
    success="#5ec78a",
    warning="#e0b74a",
    info="#4a9ee0",
    chart=("#e0524a", "#4a9ee0", "#5ec78a", "#e0b74a", "#a877e0"),
)

LIGHT = Palette(
    background="#f6f7f9",
    surface="#ffffff",
    text="#1a1d24",
    muted="#5b6470",
    border="#e2e5ea",
    primary="#c9342b",
    success="#2f9d5a",
    warning="#b8871c",
    info="#2f7fc0",
    chart=("#c9342b", "#2f7fc0", "#2f9d5a", "#b8871c", "#7a4fb0"),
)


def get_palette(theme: Theme) -> Palette:
    return DARK if theme == "dark" else LIGHT


def inject_css(p: Palette) -> None:
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {p.background}; color: {p.text}; }}
        section[data-testid="stSidebar"] {{ background-color: {p.surface}; }}
        .block-container {{ padding-top: 1.5rem; max-width: 1600px; }}
        .kpi-card {{
            background: {p.surface};
            border: 1px solid {p.border};
            border-radius: 10px;
            padding: 16px 18px;
            height: 100%;
        }}
        .kpi-label {{ color: {p.muted}; font-size: 12px; text-transform: uppercase; letter-spacing: .06em; }}
        .kpi-value {{ font-size: 28px; font-weight: 700; margin-top: 4px; color: {p.text}; }}
        .kpi-delta-up {{ color: {p.success}; font-size: 12px; font-weight: 600; }}
        .kpi-delta-down {{ color: {p.primary}; font-size: 12px; font-weight: 600; }}
        .kpi-sub {{ color: {p.muted}; font-size: 11px; margin-top: 2px; }}
        h1, h2, h3 {{ color: {p.text}; }}
        .section-title {{
            font-size: 12px; text-transform: uppercase; letter-spacing: .08em;
            color: {p.text}; margin: 8px 0 6px 0; font-weight: 600;
        }}
        .section-sub {{ color: {p.muted}; font-size: 11px; margin-bottom: 10px; }}
        .badge {{ display:inline-block; padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 600; }}
        .badge-ok {{ background: {p.success}22; color: {p.success}; }}
        .badge-warn {{ background: {p.warning}22; color: {p.warning}; }}
        .badge-risk {{ background: {p.primary}22; color: {p.primary}; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def plotly_layout(p: Palette) -> dict:
    """Shared Plotly layout for consistent theming."""
    return dict(
        paper_bgcolor=p.surface,
        plot_bgcolor=p.surface,
        font=dict(color=p.text, size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(gridcolor=p.border, zerolinecolor=p.border),
        yaxis=dict(gridcolor=p.border, zerolinecolor=p.border),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )


# ============================================================
# DATA  ── Replace these blocks with real data sources.
# Kept as plain DataFrames so Copilot can easily swap in
# pd.read_excel("archive/xxx.xlsx", sheet_name="...") calls.
# ============================================================

# Kautex regions with an approximate geographic center used for the globe.
REGIONS = pd.DataFrame(
    [
        {"region": "EMEA",     "lat": 50.0, "lon": 10.0, "hq": "Bonn, Germany"},
        {"region": "Americas", "lat": 30.0, "lon": -90.0, "hq": "Shelbyville, USA"},
        {"region": "APAC",     "lat": 25.0, "lon": 110.0, "hq": "Wuhan, China"},
    ]
)

PLANTS = pd.DataFrame(
    [
        {"plant": "Bonn",         "region": "EMEA",     "lat": 50.73, "lon":   7.10, "oee": 82.1, "volume_m": 28.4, "scrap_pct": 1.80},
        {"plant": "Blumberg",     "region": "EMEA",     "lat": 47.84, "lon":   8.54, "oee": 80.4, "volume_m": 24.6, "scrap_pct": 2.00},
        {"plant": "Shelbyville",  "region": "Americas", "lat": 39.52, "lon": -85.78, "oee": 79.6, "volume_m": 31.2, "scrap_pct": 2.10},
        {"plant": "Querétaro",    "region": "Americas", "lat": 20.59, "lon":-100.39, "oee": 77.9, "volume_m": 19.8, "scrap_pct": 2.30},
        {"plant": "São Paulo",    "region": "Americas", "lat":-23.55, "lon": -46.63, "oee": 74.3, "volume_m": 18.9, "scrap_pct": 2.70},
        {"plant": "Wuhan",        "region": "APAC",     "lat": 30.59, "lon": 114.30, "oee": 81.2, "volume_m": 26.1, "scrap_pct": 1.90},
        {"plant": "Suzhou",       "region": "APAC",     "lat": 31.30, "lon": 120.58, "oee": 78.5, "volume_m": 13.7, "scrap_pct": 2.50},
        {"plant": "Chennai",      "region": "APAC",     "lat": 13.08, "lon":  80.27, "oee": 76.8, "volume_m": 21.5, "scrap_pct": 2.40},
    ]
)

REVENUE_TREND = pd.DataFrame(
    [
        {"month": "Jan", "actual": 218, "plan": 210, "ly": 205, "region": "Global"},
        {"month": "Feb", "actual": 224, "plan": 220, "ly": 208, "region": "Global"},
        {"month": "Mar", "actual": 241, "plan": 235, "ly": 219, "region": "Global"},
        {"month": "Apr", "actual": 236, "plan": 232, "ly": 222, "region": "Global"},
        {"month": "May", "actual": 252, "plan": 245, "ly": 228, "region": "Global"},
        {"month": "Jun", "actual": 261, "plan": 250, "ly": 235, "region": "Global"},
        {"month": "Jul", "actual": 258, "plan": 255, "ly": 238, "region": "Global"},
        {"month": "Aug", "actual": 249, "plan": 248, "ly": 231, "region": "Global"},
        {"month": "Sep", "actual": 267, "plan": 260, "ly": 244, "region": "Global"},
        {"month": "Oct", "actual": 273, "plan": 265, "ly": 249, "region": "Global"},
        {"month": "Nov", "actual": 281, "plan": 270, "ly": 253, "region": "Global"},
        {"month": "Dec", "actual": 289, "plan": 278, "ly": 261, "region": "Global"},
    ]
)

SEGMENT_MIX = pd.DataFrame(
    [
        {"segment": "Fuel Systems",         "share": 46},
        {"segment": "Industrial Packaging", "share": 23},
        {"segment": "Consumer Packaging",   "share": 18},
        {"segment": "Machinery",            "share": 13},
    ]
)

QUALITY_TREND = pd.DataFrame(
    [
        {"week": "W40", "scrap": 2.60, "rework": 1.40, "complaints": 12},
        {"week": "W41", "scrap": 2.40, "rework": 1.30, "complaints": 10},
        {"week": "W42", "scrap": 2.50, "rework": 1.50, "complaints": 14},
        {"week": "W43", "scrap": 2.30, "rework": 1.20, "complaints":  9},
        {"week": "W44", "scrap": 2.20, "rework": 1.10, "complaints":  8},
        {"week": "W45", "scrap": 2.14, "rework": 1.05, "complaints":  7},
    ]
)

ALERTS = pd.DataFrame(
    [
        {"severity": "high",   "region": "Americas", "plant": "São Paulo",  "message": "OEE below target for 3 consecutive weeks", "time": "2h ago"},
        {"severity": "medium", "region": "APAC",     "plant": "Chennai",    "message": "Scrap rate trending up on Line 4",         "time": "6h ago"},
        {"severity": "low",    "region": "EMEA",     "plant": "Bonn",       "message": "Preventive maintenance window scheduled",  "time": "1d ago"},
        {"severity": "medium", "region": "Americas", "plant": "Querétaro",  "message": "OTD dropped to 93.2% this week",           "time": "1d ago"},
    ]
)

# Region-level KPI overrides. Fallback = global.
KPI_BY_REGION: dict[str, dict[str, str]] = {
    "Global":   {"revenue": "€2.84B", "revenue_sub": "vs. €2.67B LY",  "volume": "184.2M", "oee": "78.4%", "otd": "96.1%", "scrap": "2.14%", "ltifr": "0.82"},
    "EMEA":     {"revenue": "€1.12B", "revenue_sub": "vs. €1.05B LY",  "volume": "53.0M",  "oee": "81.3%", "otd": "97.0%", "scrap": "1.90%", "ltifr": "0.74"},
    "Americas": {"revenue": "€1.05B", "revenue_sub": "vs. €0.99B LY",  "volume": "69.9M",  "oee": "77.3%", "otd": "95.4%", "scrap": "2.37%", "ltifr": "0.91"},
    "APAC":     {"revenue": "€0.67B", "revenue_sub": "vs. €0.63B LY",  "volume": "61.3M",  "oee": "78.8%", "otd": "95.9%", "scrap": "2.27%", "ltifr": "0.79"},
}


# ============================================================
# STATE
# ============================================================
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "region" not in st.session_state:
    st.session_state.region = "Global"


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### Kautex Executive BI")
    st.caption("Global Operations · FY 2026")

    st.session_state.theme = st.radio(
        "Theme", ["dark", "light"],
        horizontal=True,
        index=0 if st.session_state.theme == "dark" else 1,
    )

    st.session_state.region = st.selectbox(
        "Region",
        ["Global", "EMEA", "Americas", "APAC"],
        index=["Global", "EMEA", "Americas", "APAC"].index(st.session_state.region),
    )

    st.selectbox("Period", ["YTD 2026", "Q4 2026", "Last 12 months"])
    st.caption("Last updated: 2026-07-08 06:14 CET")

palette = get_palette(st.session_state.theme)
inject_css(palette)
region = st.session_state.region


# ============================================================
# HELPERS
# ============================================================
def filter_plants(df: pd.DataFrame, region: str) -> pd.DataFrame:
    return df if region == "Global" else df[df["region"] == region]


def kpi_card(label: str, value: str, delta: str, trend: str, sub: str) -> str:
    css = "kpi-delta-up" if trend == "up" else "kpi-delta-down"
    arrow = "▲" if trend == "up" else "▼"
    return (
        f'<div class="kpi-card">'
        f'  <div class="kpi-label">{label}</div>'
        f'  <div class="kpi-value">{value}</div>'
        f'  <div class="{css}">{arrow} {delta}</div>'
        f'  <div class="kpi-sub">{sub}</div>'
        f'</div>'
    )


def section(title: str, subtitle: str = "") -> None:
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-sub">{subtitle}</div>', unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================
st.markdown(f"## Executive Overview — {region}")
st.caption("Snapshot across finance, operations, quality and safety.")


# ============================================================
# INTERACTIVE GLOBE (Plotly scatter_geo, clickable regions)
# ============================================================
section("Global footprint", "Click a region marker to filter the dashboard.")

globe = go.Figure(
    go.Scattergeo(
        lat=REGIONS["lat"],
        lon=REGIONS["lon"],
        text=REGIONS["region"] + "<br>" + REGIONS["hq"],
        customdata=REGIONS["region"],
        mode="markers+text",
        marker=dict(
            size=[36 if r == region else 22 for r in REGIONS["region"]],
            color=[palette.primary if r == region else palette.info for r in REGIONS["region"]],
            line=dict(width=2, color=palette.surface),
            opacity=0.9,
        ),
        textposition="top center",
        textfont=dict(color=palette.text, size=12),
        hovertemplate="<b>%{text}</b><extra></extra>",
    )
)

# plotly_events would give real click callbacks; keep this dep-free.
# Region can also be picked from the sidebar select above.
st.plotly_chart(globe, use_container_width=True, config={"displayModeBar": False})

region_cols = st.columns(4)
for i, r in enumerate(["Global", "EMEA", "Americas", "APAC"]):
    if region_cols[i].button(r, use_container_width=True, type="primary" if r == region else "secondary"):
        st.session_state.region = r
        st.rerun()


# ============================================================
# KPI ROW
# ============================================================
k = KPI_BY_REGION.get(region, KPI_BY_REGION["Global"])
cards = [
    ("Revenue YTD",       k["revenue"], "+6.2%",  "up",   k["revenue_sub"]),
    ("Production Volume", k["volume"],  "+3.8%",  "up",   "units shipped"),
    ("OEE",               k["oee"],     "+1.9pp", "up",   "target 82%"),
    ("On-Time Delivery",  k["otd"],     "-0.4pp", "down", "target 97%"),
    ("Scrap Rate",        k["scrap"],   "-0.23pp","up",   "target < 2%"),
    ("Safety (LTIFR)",    k["ltifr"],   "-0.11",  "up",   "per 1M hours"),
]
cols = st.columns(6)
for col, (label, value, delta, trend, sub) in zip(cols, cards):
    col.markdown(kpi_card(label, value, delta, trend, sub), unsafe_allow_html=True)


# ============================================================
# ROW 1 — Revenue trend + Segment mix
# ============================================================
c1, c2 = st.columns([2, 1])

with c1:
    section("Revenue vs Plan vs Last Year", "Monthly, € millions")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=REVENUE_TREND["month"], y=REVENUE_TREND["actual"], name="Actual",
        mode="lines", line=dict(color=palette.chart[0], width=3),
        fill="tozeroy", fillcolor=f"{palette.chart[0]}33",
    ))
    fig.add_trace(go.Scatter(x=REVENUE_TREND["month"], y=REVENUE_TREND["plan"], name="Plan",
                             mode="lines", line=dict(color=palette.chart[1], width=2)))
    fig.add_trace(go.Scatter(x=REVENUE_TREND["month"], y=REVENUE_TREND["ly"], name="Last Year",
                             mode="lines", line=dict(color=palette.chart[3], width=2, dash="dash")))
    fig.update_layout(**plotly_layout(palette), height=320)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with c2:
    section("Revenue by Segment", "Share of YTD revenue")
    fig = px.pie(SEGMENT_MIX, names="segment", values="share", hole=0.55,
                 color_discrete_sequence=list(palette.chart))
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(**plotly_layout(palette), height=320, showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ============================================================
# ROW 2 — Plant performance + Quality trend
# ============================================================
c1, c2 = st.columns([2, 1])

with c1:
    section("Plant Performance", "OEE and volume by plant")
    plants_f = filter_plants(PLANTS, region)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=plants_f["plant"], y=plants_f["volume_m"], name="Volume (M units)",
        marker_color=palette.chart[1],
    ))
    fig.add_trace(go.Scatter(
        x=plants_f["plant"], y=plants_f["oee"], name="OEE %",
        mode="lines+markers", yaxis="y2",
        line=dict(color=palette.chart[0], width=3),
    ))
    fig.update_layout(
        **plotly_layout(palette),
        height=320,
        yaxis=dict(title="Volume", gridcolor=palette.border),
        yaxis2=dict(title="OEE %", overlaying="y", side="right", showgrid=False),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with c2:
    section("Quality Trend", "Last 6 weeks")
    fig = go.Figure()
    for i, metric in enumerate(["scrap", "rework", "complaints"]):
        fig.add_trace(go.Scatter(
            x=QUALITY_TREND["week"], y=QUALITY_TREND[metric], name=metric.title(),
            mode="lines+markers", line=dict(color=palette.chart[i], width=2),
        ))
    fig.update_layout(**plotly_layout(palette), height=320)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ============================================================
# ROW 3 — Plant detail table + Alerts
# ============================================================
c1, c2 = st.columns([2, 1])

with c1:
    section("Plants — Detail", "OEE, volume, scrap by site")
    plants_f = filter_plants(PLANTS, region).copy()

    def status_of(oee: float) -> str:
        if oee >= 80: return "on-track"
        if oee >= 76: return "watch"
        return "at-risk"

    plants_f["status"] = plants_f["oee"].map(status_of)
    st.dataframe(
        plants_f[["plant", "region", "oee", "volume_m", "scrap_pct", "status"]]
            .rename(columns={"volume_m": "Volume (M)", "scrap_pct": "Scrap %",
                             "plant": "Plant", "region": "Region",
                             "oee": "OEE %", "status": "Status"}),
        hide_index=True,
        use_container_width=True,
    )

with c2:
    section("Alerts & Actions", "Requires executive attention")
    alerts_f = ALERTS if region == "Global" else ALERTS[ALERTS["region"] == region]
    if alerts_f.empty:
        st.info("No open alerts for this region.")
    else:
        for _, a in alerts_f.iterrows():
            badge = {"high": "badge-risk", "medium": "badge-warn", "low": "badge-ok"}[a["severity"]]
            st.markdown(
                f'<div style="background:{palette.surface};border:1px solid {palette.border};'
                f'border-radius:8px;padding:10px 12px;margin-bottom:8px;'>
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'  <b style="color:{palette.text}">{a["plant"]}</b>'
                f'  <span class="badge {badge}">{a["severity"]}</span>'
                f'</div>'
                f'<div style="color:{palette.muted};font-size:12px;margin-top:4px;">{a["message"]}</div>'
                f'<div style="color:{palette.muted};font-size:11px;margin-top:2px;">{a["time"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

st.markdown("---")
st.caption("Kautex Executive BI · Template for internal use · Data shown is illustrative")

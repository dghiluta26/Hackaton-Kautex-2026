"""Shared frontend theme and sample planning data for the Streamlit app."""

from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

from utils.calculations import (
    calculate_employee_topic_cost,
    calculate_total_topic_cost,
    calculate_total_utilization,
    is_overallocated,
)


#We deleted TOPIC_COLUMNS to remove hardcoding


def is_dark_mode() -> bool:
    """Whether the Kautex dark theme toggle is currently on."""
    return bool(st.session_state.get("dark_mode", False))


def render_theme_toggle() -> bool:
    """Render the sidebar Light/Dark switch. Call this exactly once per run
    (from app.py) since it's a stateful widget — inject_app_theme() itself
    only emits CSS and is safe to call from every page.
    """
    with st.sidebar:
        dark = st.toggle("Dark mode", key="dark_mode")
    return dark


def inject_app_theme() -> None:
    dark = is_dark_mode()

    if dark:
        kautex_blue = "#38BDF8"
        ink = "#E5E9F0"
        muted = "#94A3B8"
        line = "#2A3A55"
        soft = "#16223A"
        app_bg = "#0B1220"
        card_bg = "#111C31"
        metric_shadow = "rgba(0, 0, 0, 0.35)"
        pill_border = "#2D5875"
        pill_bg = "rgba(56, 189, 248, 0.12)"
        pill_text = "#7DD3FC"
    else:
        kautex_blue = "#00A6DF"
        ink = "#172033"
        muted = "#667085"
        line = "#D9E2EC"
        soft = "#F4F6F9"
        app_bg = "#f4f6f9"
        card_bg = "#ffffff"
        metric_shadow = "rgba(23, 32, 51, 0.06)"
        pill_border = "#B7E5F6"
        pill_bg = "#EAF8FD"
        pill_text = "#0879A4"

    native_widget_overrides = f"""
            .stApp, [data-testid="stHeader"] {{
                color: {ink};
            }}

            [data-testid="stHeader"] {{
                background: {app_bg};
            }}

            [data-testid="stSidebar"] {{
                background: {card_bg};
                border-right: 1px solid {line};
            }}

            [data-testid="stSidebar"] * {{
                color: {ink};
            }}

            [data-testid="stMetricLabel"], [data-testid="stMetricValue"], [data-testid="stMetricDelta"] {{
                color: {ink} !important;
            }}

            .stApp p, .stApp span, .stApp label, .stApp li,
            [data-testid="stMarkdownContainer"] {{
                color: {ink};
            }}

            [data-testid="stCaptionContainer"] {{
                color: {muted} !important;
            }}

            [data-testid="stTextInput"] input,
            [data-testid="stNumberInput"] input,
            [data-testid="stTextArea"] textarea,
            [data-baseweb="select"] > div,
            [data-baseweb="base-input"] {{
                background: {soft} !important;
                border-color: {line} !important;
                color: {ink} !important;
            }}

            [data-testid="stForm"], [data-testid="stExpander"], [data-testid="stFileUploaderDropzone"] {{
                background: {card_bg};
                border-color: {line} !important;
            }}

            [data-testid="stDataFrame"], [data-testid="stTable"] {{
                border: 1px solid {line};
                border-radius: 8px;
            }}

            [data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-tertiary"],
            [data-testid="stFormSubmitButton"] button {{
                background: {soft};
                border-color: {line} !important;
                color: {ink} !important;
            }}

            [data-testid="stTabs"] [data-baseweb="tab"] {{
                color: {muted};
            }}

            [data-testid="stTabs"] [aria-selected="true"] {{
                color: {kautex_blue} !important;
            }}
    """ if dark else ""

    st.html(
        f"""
        <style>
            :root {{
                --kautex-blue: {kautex_blue};
                --ink: {ink};
                --muted: {muted};
                --line: {line};
                --soft: {soft};
            }}

            .stApp {{
                background: {app_bg};
            }}

            .block-container {{
                max-width: 1500px;
                padding-top: 1.25rem;
                padding-bottom: 2.5rem;
            }}

            [data-testid="stMetric"] {{
                background: {card_bg};
                border: 1px solid var(--line);
                border-radius: 8px;
                padding: 14px 16px;
                box-shadow: 0 10px 24px {metric_shadow};
            }}

            {native_widget_overrides}

            .kautex-hero {{
                background: {card_bg};
                border: 1px solid var(--line);
                border-radius: 8px;
                padding: 18px 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 18px;
                margin-bottom: 18px;
                box-sizing: border-box;
                width: 100%;
            }}

            .brand-lockup {{
                display: flex;
                align-items: center;
                gap: 16px;
                min-width: 0;
                width: 100%;
            }}

            .k-logo {{
                width: 52px;
                height: 52px;
                flex: 0 0 52px;
                background: var(--kautex-blue);
                border-radius: 6px;
                color: #ffffff;
                font-weight: 900;
                font-size: 34px;
                line-height: 52px;
                text-align: center;
                border: 3px solid #ffffff;
                outline: 2px solid var(--kautex-blue);
            }}

            .eyebrow {{
                color: var(--kautex-blue);
                font-size: 0.78rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-bottom: 2px;
            }}

            .hero-title {{
                color: var(--ink);
                font-size: clamp(1.4rem, 3vw, 2.35rem);
                font-weight: 850;
                line-height: 1.05;
                overflow-wrap: anywhere;
            }}

            .hero-subtitle,
            .section-note {{
                color: var(--muted);
                font-size: 0.95rem;
            }}

            .status-pill {{
                border: 1px solid {pill_border};
                background: {pill_bg};
                color: {pill_text};
                padding: 8px 12px;
                border-radius: 999px;
                font-size: 0.82rem;
                font-weight: 700;
                white-space: nowrap;
            }}

            @media (max-width: 740px) {{
                [data-testid="stHorizontalBlock"] {{
                    flex-wrap: wrap;
                }}

                [data-testid="stHorizontalBlock"] > div {{
                    min-width: min(100%, 260px) !important;
                    flex: 1 1 260px !important;
                }}

                .kautex-hero {{
                    align-items: flex-start;
                    flex-direction: column;
                    padding: 14px;
                }}

                .brand-lockup {{
                    align-items: flex-start;
                    flex-direction: column;
                    gap: 10px;
                }}

                .status-pill {{
                    white-space: normal;
                }}
            }}
        </style>
        """
    )


def render_kautex_header(title: str, subtitle: str, pill: str = "Kautex planning system") -> None:
    st.html(
        f"""
        <div class="kautex-hero">
            <div class="brand-lockup">
                <div class="k-logo">K</div>
                <div>
                    <div class="eyebrow">Kautex engineering planning</div>
                    <div class="hero-title">{title}</div>
                    <div class="hero-subtitle">{subtitle}</div>
                </div>
            </div>
            <div class="status-pill">{pill}</div>
        </div>
        """
    )


def load_sample_planning_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    employees = pd.DataFrame(
        [
            ["Employee A", "CAE Romania", "CAE", "Romania", 1768, 71.77, "Active"],
            ["Employee B", "CAE India", "CAE", "India", 1816, 49.55, "Active"],
            ["Employee C", "Test Bonn", "Testing", "Germany", 1669, 149.23, "Active"],
            ["Employee D", "Test Pinghu", "Testing", "China", 1600, 64.20, "Replacement"],
            ["Employee E", "Test Mexico", "Testing", "Mexico", 1600, 58.60, "New position"],
            ["Employee F", "Management", "Management", "Germany", 1500, 132.00, "Active"],
            ["Employee G", "CAE Romania", "Internal Development", "Romania", 1768, 83.40, "Active"],
            ["Employee H", "Sampling Pinghu", "Sampling", "China", 1600, 52.80, "Temporary"],
        ],
        columns=["employee", "team", "department", "location", "hours_per_year", "hourly_rate", "status"],
    )
    topics = pd.DataFrame(
        [
            ["AI antimicrobial surfaces", "AI initiatives", "CAE", "Active"],
            ["Fuel tank standardization", "Testing activities", "Testing", "Active"],
            ["Pneumatic D-projects", "Internal D-projects", "Internal Development", "Active"],
            ["Customer request", "Customer requests", "Customer Engineering", "At risk"],
            ["Virtual validation", "Virtual validation", "CAE", "Active"],
        ],
        columns=["topic", "category", "area", "status"],
    )
    allocations = pd.DataFrame(
        [
            ["Employee A", 20, 30, 10, 20, 20, "Balanced across CAE and customer topics"],
            ["Employee B", 40, 20, 30, 20, 0, "Above 100% because of transition support"],
            ["Employee C", 0, 60, 10, 15, 10, "Main validation owner"],
            ["Employee D", 0, 45, 25, 20, 0, "Lab execution"],
            ["Employee E", 10, 35, 15, 20, 10, "Ramp-up and handover"],
            ["Employee F", 10, 15, 10, 20, 25, "Portfolio and decision support"],
            ["Employee G", 50, 0, 30, 10, 15, "Automation-heavy work package"],
            ["Employee H", 0, 30, 0, 10, 40, "Prototype sampling"],
        ],
        columns=["employee", *TOPIC_COLUMNS, "allocation_comment"],
    )
    costs = pd.DataFrame(
        [
            ["AI antimicrobial surfaces", "Internal", 30000],
            ["Fuel tank standardization", "Internal", 26000],
            ["Fuel tank standardization", "External", 14000],
            ["Pneumatic D-projects", "Internal", 20000],
            ["Customer request", "External", 22000],
            ["Virtual validation", "Internal", 15000],
            ["Virtual validation", "Recovery", 8000],
        ],
        columns=["topic", "cost_type", "amount"],
    )
    return employees, topics, allocations, costs


def build_planning_model(
    employees: pd.DataFrame, topics: pd.DataFrame, allocations: pd.DataFrame, costs: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    model = employees.merge(allocations, on="employee", how="left")
    for topic in TOPIC_COLUMNS:
        model[topic] = pd.to_numeric(model[topic], errors="coerce").fillna(0)

    model["total_utilization"] = model[TOPIC_COLUMNS].apply(lambda row: calculate_total_utilization(row.tolist()), axis=1)
    model["allocated_internal_cost"] = model.apply(
        lambda row: sum(
            calculate_employee_topic_cost(row["hours_per_year"], row["hourly_rate"], row[topic])
            for topic in TOPIC_COLUMNS
        ),
        axis=1,
    )
    model["risk"] = model["total_utilization"].apply(lambda value: "Overallocated" if is_overallocated(value) else "OK")

    topic_rows = []
    for topic in TOPIC_COLUMNS:
        extra = costs[costs["topic"] == topic]
        internal_extra = extra.loc[extra["cost_type"] == "Internal", "amount"].sum()
        external = extra.loc[extra["cost_type"] == "External", "amount"].sum()
        recovery = extra.loc[extra["cost_type"] == "Recovery", "amount"].sum()
        employee_internal = (
            model["hours_per_year"] * model["hourly_rate"] * model[topic] / 100
        ).sum()
        topic_meta = topics[topics["topic"] == topic]
        topic_rows.append(
            {
                "topic": topic,
                "category": topic_meta["category"].iloc[0] if not topic_meta.empty else "Unmapped",
                "employees_involved": int((model[topic] > 0).sum()),
                "employee_internal_cost": employee_internal,
                "additional_internal_cost": internal_extra,
                "external_cost": external,
                "recovery": recovery,
                "total_topic_cost": calculate_total_topic_cost(employee_internal, internal_extra, external, recovery),
            }
        )

    topic_summary = pd.DataFrame(topic_rows)
    team_summary = (
        model.groupby(["team", "department", "location"], as_index=False)
        .agg(
            team_members=("employee", "count"),
            average_utilization=("total_utilization", "mean"),
            total_internal_cost=("allocated_internal_cost", "sum"),
            overallocated=("risk", lambda values: int((values == "Overallocated").sum())),
        )
        .sort_values("total_internal_cost", ascending=False)
    )
    return model, topic_summary, team_summary


def money_column(label: str):
    return st.column_config.NumberColumn(label, format="$ %.0f")


def percent_column(label: str, editable: bool = False):
    return st.column_config.NumberColumn(
        label,
        min_value=0 if editable else None,
        max_value=200 if editable else None,
        step=5 if editable else None,
        format="%.0f%%",
    )


def table_height(row_count: int, min_height: int = 260, max_height: int = 560) -> int:
    return max(min_height, min(max_height, 88 + row_count * 36))


def topic_cost_chart(topic_summary: pd.DataFrame) -> alt.Chart:
    return alt.Chart(topic_summary).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X("topic:N", title=None, sort="-y", axis=alt.Axis(labelAngle=-28)),
        y=alt.Y("total_topic_cost:Q", title="Cost"),
        color=alt.Color("category:N", title="Category"),
        tooltip=["topic", "category", alt.Tooltip("total_topic_cost:Q", format="$,.0f")],
    )


def utilization_chart(model: pd.DataFrame) -> alt.Chart:
    bars = alt.Chart(model).mark_bar(cornerRadiusTopRight=3, cornerRadiusBottomRight=3).encode(
        y=alt.Y("employee:N", title=None, sort="-x"),
        x=alt.X("total_utilization:Q", title="Utilization %"),
        color=alt.condition(alt.datum.total_utilization > 100, alt.value("#D92D20"), alt.value("#00A6DF")),
        tooltip=["employee", "team", alt.Tooltip("total_utilization:Q", format=".0f")],
    )
    rule = alt.Chart(pd.DataFrame({"limit": [100]})).mark_rule(strokeDash=[6, 4], color="#667085").encode(x="limit:Q")
    return bars + rule

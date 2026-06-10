"""
CodeTrack AI – Coding Interview Performance Analyzer
=====================================================
A professional dashboard for tracking coding interview preparation,
analyzing performance, and generating personalized recommendations.

Author: CodeTrack AI
Version: 1.0.0
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, date, timedelta
import os
import io

# ─────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CodeTrack AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CONSTANTS & THEME
# ─────────────────────────────────────────────
TOPICS = [
    "Arrays", "Linked Lists", "Stacks", "Queues", "Trees", "Graphs",
    "Dynamic Programming", "Binary Search", "Sliding Window", "Two Pointers",
    "Backtracking", "Heaps", "Greedy", "Design", "Sorting", "Hashing",
    "Tries", "Bit Manipulation", "Math", "Recursion",
]

DIFFICULTIES = ["Easy", "Medium", "Hard"]
STATUSES = ["Solved", "Not Solved"]

DATA_PATH = "data/problems.csv"
SAMPLE_PATH = "sample_data.csv"

PALETTE = {
    "bg":        "#0F1117",
    "card":      "#1A1D27",
    "accent":    "#6C63FF",
    "green":     "#00D4AA",
    "orange":    "#FF8C42",
    "red":       "#FF4D6D",
    "easy":      "#00D4AA",
    "medium":    "#FFB347",
    "hard":      "#FF4D6D",
    "text":      "#E8E8F0",
    "muted":     "#8B8FA8",
    "border":    "#2A2D3E",
}

DIFFICULTY_COLORS = {
    "Easy":   PALETTE["easy"],
    "Medium": PALETTE["medium"],
    "Hard":   PALETTE["hard"],
}

TOPIC_COLORS = px.colors.qualitative.Vivid


# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
def inject_css():
    st.markdown(f"""
    <style>
    /* ── Imports ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    /* ── Global Reset ── */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: {PALETTE['bg']};
        color: {PALETTE['text']};
    }}

    /* ── Hide default Streamlit chrome ── */
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{
        padding: 1.5rem 2rem 3rem 2rem;
        max-width: 1400px;
    }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background: {PALETTE['card']};
        border-right: 1px solid {PALETTE['border']};
    }}
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] label {{
        color: {PALETTE['text']} !important;
        font-size: 0.85rem;
        font-weight: 500;
    }}

    /* ── Metric cards ── */
    .metric-card {{
        background: {PALETTE['card']};
        border: 1px solid {PALETTE['border']};
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(108,99,255,0.15);
    }}
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, {PALETTE['accent']}, {PALETTE['green']});
        border-radius: 14px 14px 0 0;
    }}
    .metric-value {{
        font-size: 2rem;
        font-weight: 800;
        line-height: 1;
        font-family: 'JetBrains Mono', monospace;
        color: {PALETTE['text']};
    }}
    .metric-label {{
        font-size: 0.78rem;
        font-weight: 500;
        color: {PALETTE['muted']};
        margin-top: 0.4rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}
    .metric-delta {{
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }}
    .delta-up   {{ color: {PALETTE['green']}; }}
    .delta-down {{ color: {PALETTE['red']}; }}

    /* ── Section headers ── */
    .section-header {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin: 2rem 0 1rem 0;
    }}
    .section-title {{
        font-size: 1.15rem;
        font-weight: 700;
        color: {PALETTE['text']};
    }}
    .section-pill {{
        background: {PALETTE['accent']}22;
        color: {PALETTE['accent']};
        font-size: 0.7rem;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }}

    /* ── Progress bars ── */
    .progress-wrap {{
        background: {PALETTE['border']};
        border-radius: 99px;
        height: 8px;
        overflow: hidden;
        margin: 0.4rem 0 0.8rem 0;
    }}
    .progress-fill {{
        height: 100%;
        border-radius: 99px;
        transition: width 0.6s cubic-bezier(0.4,0,0.2,1);
    }}

    /* ── Readiness gauge card ── */
    .readiness-card {{
        background: {PALETTE['card']};
        border: 1px solid {PALETTE['border']};
        border-radius: 18px;
        padding: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }}
    .readiness-score {{
        font-size: 4rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        background: linear-gradient(135deg, {PALETTE['accent']}, {PALETTE['green']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
    }}
    .readiness-label {{
        font-size: 1rem;
        font-weight: 600;
        margin-top: 0.5rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }}

    /* ── Badge chips ── */
    .badge {{
        display: inline-block;
        padding: 0.2rem 0.65rem;
        border-radius: 99px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.04em;
    }}
    .badge-easy   {{ background: {PALETTE['easy']}22;   color: {PALETTE['easy']}; }}
    .badge-medium {{ background: {PALETTE['medium']}22; color: {PALETTE['medium']}; }}
    .badge-hard   {{ background: {PALETTE['hard']}22;   color: {PALETTE['hard']}; }}
    .badge-solved {{ background: {PALETTE['green']}22;  color: {PALETTE['green']}; }}
    .badge-unsolved {{ background: {PALETTE['red']}22;  color: {PALETTE['red']}; }}

    /* ── Recommendation cards ── */
    .rec-card {{
        background: {PALETTE['card']};
        border: 1px solid {PALETTE['border']};
        border-left: 3px solid {PALETTE['accent']};
        border-radius: 10px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.6rem;
        font-size: 0.88rem;
        color: {PALETTE['text']};
        line-height: 1.5;
    }}
    .rec-icon {{
        font-size: 1rem;
        margin-right: 0.5rem;
    }}

    /* ── Strength / Weakness chips ── */
    .strength-chip {{
        display: inline-block;
        background: {PALETTE['green']}18;
        border: 1px solid {PALETTE['green']}44;
        color: {PALETTE['green']};
        border-radius: 8px;
        padding: 0.35rem 0.75rem;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }}
    .weakness-chip {{
        display: inline-block;
        background: {PALETTE['red']}18;
        border: 1px solid {PALETTE['red']}44;
        color: {PALETTE['red']};
        border-radius: 8px;
        padding: 0.35rem 0.75rem;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }}

    /* ── Tables ── */
    .dataframe {{
        background: {PALETTE['card']} !important;
        border-radius: 10px !important;
    }}

    /* ── Input widgets ── */
    .stTextInput input, .stNumberInput input, .stSelectbox select,
    .stDateInput input, .stTextArea textarea {{
        background: {PALETTE['card']} !important;
        border: 1px solid {PALETTE['border']} !important;
        color: {PALETTE['text']} !important;
        border-radius: 8px !important;
    }}
    .stButton > button {{
        background: linear-gradient(135deg, {PALETTE['accent']}, #8B5CF6);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.55rem 1.5rem;
        transition: opacity 0.2s;
        width: 100%;
    }}
    .stButton > button:hover {{ opacity: 0.88; }}

    /* ── Page header banner ── */
    .page-banner {{
        background: linear-gradient(135deg, {PALETTE['card']} 0%, #1E1B3A 100%);
        border: 1px solid {PALETTE['border']};
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }}
    .banner-title {{
        font-size: 1.7rem;
        font-weight: 800;
        background: linear-gradient(90deg, {PALETTE['accent']}, {PALETTE['green']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
    }}
    .banner-subtitle {{
        font-size: 0.85rem;
        color: {PALETTE['muted']};
        margin-top: 0.25rem;
    }}

    /* ── Plotly chart containers ── */
    .js-plotly-plot {{ border-radius: 12px; }}

    /* ── Dividers ── */
    hr {{
        border: none;
        border-top: 1px solid {PALETTE['border']};
        margin: 1.5rem 0;
    }}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA LAYER
# ─────────────────────────────────────────────

def load_data() -> pd.DataFrame:
    """Load problems data from session state, CSV file, or create empty frame."""
    if "df" in st.session_state:
        return st.session_state["df"]

    os.makedirs("data", exist_ok=True)
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    elif os.path.exists(SAMPLE_PATH):
        df = pd.read_csv(SAMPLE_PATH)
    else:
        df = pd.DataFrame(columns=[
            "problem_name", "topic", "difficulty",
            "status", "time_taken", "date_solved",
        ])

    df = _clean_df(df)
    st.session_state["df"] = df
    return df


def save_data(df: pd.DataFrame):
    """Persist dataframe to CSV and update session state."""
    os.makedirs("data", exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    st.session_state["df"] = df


def _clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise column types for safe downstream use."""
    if df.empty:
        return df
    df["date_solved"] = pd.to_datetime(df["date_solved"], errors="coerce")
    df["time_taken"]  = pd.to_numeric(df["time_taken"],  errors="coerce").fillna(0)
    df["difficulty"]  = df["difficulty"].str.strip().str.title()
    df["status"]      = df["status"].str.strip().str.title()
    df["topic"]       = df["topic"].str.strip().str.title()
    return df


def add_problem(name, topic, difficulty, status, time_taken, date_solved):
    """Append a new problem record and save."""
    df = load_data()
    new_row = pd.DataFrame([{
        "problem_name": name.strip(),
        "topic":        topic,
        "difficulty":   difficulty,
        "status":       status,
        "time_taken":   int(time_taken),
        "date_solved":  str(date_solved),
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df = _clean_df(df)
    save_data(df)
    return df


# ─────────────────────────────────────────────
# ANALYTICS ENGINE
# ─────────────────────────────────────────────

def compute_stats(df: pd.DataFrame) -> dict:
    """Return aggregate statistics dictionary."""
    total   = len(df)
    solved  = len(df[df["status"] == "Solved"])
    unsolved = total - solved
    accuracy = round(solved / total * 100, 1) if total else 0.0

    by_difficulty = df.groupby("difficulty")["status"].apply(
        lambda s: (s == "Solved").sum()
    ).to_dict()

    by_topic = df.groupby("topic").agg(
        total   =("status", "count"),
        solved  =("status", lambda s: (s == "Solved").sum()),
    ).reset_index()
    by_topic["accuracy"] = (by_topic["solved"] / by_topic["total"] * 100).round(1)

    avg_time = round(df[df["status"] == "Solved"]["time_taken"].mean(), 1) if solved else 0.0

    return {
        "total": total, "solved": solved, "unsolved": unsolved,
        "accuracy": accuracy, "avg_time": avg_time,
        "by_difficulty": by_difficulty, "by_topic": by_topic,
    }


def compute_readiness(stats: dict, df: pd.DataFrame) -> tuple[int, str, list[str]]:
    """
    Compute interview readiness score 0-100.
    Returns (score, category, list_of_recommendation_strings).
    """
    if stats["total"] == 0:
        return 0, "Beginner", ["Start solving problems to get your readiness score!"]

    # — Volume score (max 30 pts) —
    vol_score = min(stats["solved"] / 150 * 30, 30)

    # — Accuracy score (max 25 pts) —
    acc_score = stats["accuracy"] / 100 * 25

    # — Difficulty score (max 25 pts) —
    solved_df = df[df["status"] == "Solved"]
    diff_dist  = solved_df["difficulty"].value_counts(normalize=True).to_dict()
    hard_pct   = diff_dist.get("Hard",   0)
    medium_pct = diff_dist.get("Medium", 0)
    diff_score = (hard_pct * 15) + (medium_pct * 10)

    # — Topic coverage score (max 20 pts) —
    core_topics = {"Arrays", "Dynamic Programming", "Graphs", "Trees",
                   "Linked Lists", "Binary Search", "Sliding Window", "Backtracking"}
    practiced_core = set(df["topic"].unique()) & core_topics
    cov_score = len(practiced_core) / len(core_topics) * 20

    raw   = vol_score + acc_score + diff_score + cov_score
    score = int(min(max(raw, 0), 100))

    if score < 30:
        category = "Beginner"
    elif score < 65:
        category = "Intermediate"
    else:
        category = "Interview Ready"

    recommendations = _build_recommendations(stats, df, practiced_core, core_topics)
    return score, category, recommendations


def _build_recommendations(stats, df, practiced_core, core_topics) -> list[str]:
    """Generate personalised, actionable recommendations."""
    recs = []
    by_topic = stats["by_topic"]

    # Weak accuracy topics
    weak = by_topic[
        (by_topic["accuracy"] < 60) & (by_topic["total"] >= 2)
    ].sort_values("accuracy").head(3)
    for _, row in weak.iterrows():
        recs.append(
            f"📉 Improve accuracy in **{row['topic']}** ({row['accuracy']:.0f}% solved). "
            f"Review core patterns before tackling new problems."
        )

    # Uncovered core topics
    missing = core_topics - practiced_core
    for t in list(missing)[:3]:
        recs.append(f"🔍 You haven't practiced **{t}** yet — it's a high-frequency interview topic.")

    # Hard problem exposure
    hard_count = len(df[(df["difficulty"] == "Hard") & (df["status"] == "Solved")])
    if hard_count < 5:
        recs.append(
            f"💪 Only {hard_count} Hard problems solved. Aim for 10+ Hard problems "
            f"to boost confidence in senior-level interviews."
        )

    # Accuracy general
    if stats["accuracy"] < 70:
        recs.append(
            "🎯 Overall accuracy is below 70%. Focus on **understanding** problem patterns "
            "before moving on — quality beats quantity."
        )

    # Low volume
    if stats["solved"] < 50:
        recs.append(
            f"📚 You've solved {stats['solved']} problems. Push toward 75–100 to build "
            "solid pattern recognition."
        )

    # Least practiced topic
    if not by_topic.empty:
        least = by_topic.sort_values("total").iloc[0]
        if least["total"] < 3:
            recs.append(
                f"⚡ **{least['topic']}** has only {int(least['total'])} problem(s). "
                f"Practice at least 5 problems per topic."
            )

    if not recs:
        recs.append("🚀 You're on track! Keep solving Hard problems and broaden topic coverage.")

    return recs[:6]  # cap at 6


# ─────────────────────────────────────────────
# CHART BUILDERS  (all return Plotly figures)
# ─────────────────────────────────────────────

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color=PALETTE["text"], size=12),
    margin=dict(t=40, b=20, l=20, r=20),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color=PALETTE["text"], size=11),
    ),
)


def chart_topic_bar(df: pd.DataFrame) -> go.Figure:
    counts = df["topic"].value_counts().reset_index()
    counts.columns = ["topic", "count"]
    fig = px.bar(
        counts, x="count", y="topic", orientation="h",
        color="count",
        color_continuous_scale=[[0, PALETTE["accent"]+"55"], [1, PALETTE["accent"]]],
        labels={"count": "Problems", "topic": ""},
        title="Problems by Topic",
    )
    fig.update_coloraxes(showscale=False)
    fig.update_traces(marker_line_width=0)
    fig.update_layout(**CHART_LAYOUT, height=420,
                      yaxis=dict(gridcolor=PALETTE["border"]),
                      xaxis=dict(gridcolor=PALETTE["border"]))
    return fig


def chart_difficulty_pie(df: pd.DataFrame) -> go.Figure:
    counts = df["difficulty"].value_counts().reset_index()
    counts.columns = ["difficulty", "count"]
    color_map = {k: DIFFICULTY_COLORS.get(k, "#888") for k in counts["difficulty"]}
    fig = px.pie(
        counts, names="difficulty", values="count",
        color="difficulty", color_discrete_map=color_map,
        title="Difficulty Distribution",
        hole=0.55,
    )
    fig.update_traces(
        textposition="outside",
        textinfo="label+percent",
        marker=dict(line=dict(color=PALETTE["bg"], width=3)),
    )
    fig.update_layout(**CHART_LAYOUT, height=360,
                      showlegend=True,
                      legend=dict(orientation="h", yanchor="bottom", y=-0.2, x=0.3))
    return fig


def chart_progress_line(df: pd.DataFrame) -> go.Figure:
    daily = (
        df[df["status"] == "Solved"]
        .groupby(df["date_solved"].dt.date)
        .size()
        .reset_index(name="count")
        .rename(columns={"date_solved": "date"})
        .sort_values("date")
    )
    daily["cumulative"] = daily["count"].cumsum()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=daily["date"], y=daily["count"],
        name="Daily Solved",
        marker_color=PALETTE["accent"] + "66",
        marker_line_width=0,
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=daily["date"], y=daily["cumulative"],
        name="Cumulative",
        mode="lines+markers",
        line=dict(color=PALETTE["green"], width=2.5),
        marker=dict(size=5, color=PALETTE["green"]),
    ), secondary_y=True)
    fig.update_layout(**CHART_LAYOUT, title="Progress Over Time", height=360,
                      xaxis=dict(gridcolor=PALETTE["border"]),
                      yaxis=dict(gridcolor=PALETTE["border"], title="Daily"),
                      yaxis2=dict(title="Cumulative", gridcolor="transparent"))
    return fig


def chart_accuracy_by_topic(stats: dict) -> go.Figure:
    bt = stats["by_topic"].sort_values("accuracy", ascending=True).tail(15)
    colors = [
        PALETTE["green"] if a >= 70 else
        PALETTE["medium"] if a >= 40 else
        PALETTE["red"]
        for a in bt["accuracy"]
    ]
    fig = go.Figure(go.Bar(
        x=bt["accuracy"], y=bt["topic"],
        orientation="h",
        marker_color=colors,
        marker_line_width=0,
        text=[f"{a:.0f}%" for a in bt["accuracy"]],
        textposition="outside",
        textfont=dict(color=PALETTE["text"], size=11),
    ))
    fig.update_layout(**CHART_LAYOUT, title="Accuracy by Topic (%)", height=420,
                      xaxis=dict(range=[0, 120], gridcolor=PALETTE["border"]),
                      yaxis=dict(gridcolor="transparent"))
    return fig


def chart_weekly_heatmap(df: pd.DataFrame) -> go.Figure:
    """Render a weekly activity bar chart for the last 10 weeks."""
    solved_df = df[df["status"] == "Solved"].copy()
    if solved_df.empty:
        return go.Figure()
    solved_df["week"] = solved_df["date_solved"].dt.to_period("W").dt.start_time
    weekly = solved_df.groupby("week").size().reset_index(name="count")
    weekly = weekly.sort_values("week").tail(10)
    fig = go.Figure(go.Bar(
        x=weekly["week"].astype(str),
        y=weekly["count"],
        marker_color=PALETTE["accent"],
        marker_line_width=0,
        text=weekly["count"],
        textposition="outside",
        textfont=dict(color=PALETTE["text"], size=11),
    ))
    fig.update_layout(**CHART_LAYOUT, title="Weekly Activity (last 10 weeks)", height=300,
                      xaxis=dict(gridcolor=PALETTE["border"]),
                      yaxis=dict(gridcolor=PALETTE["border"], title="Problems Solved"))
    return fig


# ─────────────────────────────────────────────
# REUSABLE UI COMPONENTS
# ─────────────────────────────────────────────

def metric_card(label: str, value, delta: str = "", delta_up: bool = True):
    delta_html = ""
    if delta:
        cls = "delta-up" if delta_up else "delta-down"
        arrow = "▲" if delta_up else "▼"
        delta_html = f'<div class="metric-delta {cls}">{arrow} {delta}</div>'
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str, pill: str = ""):
    pill_html = f'<span class="section-pill">{pill}</span>' if pill else ""
    st.markdown(f"""
    <div class="section-header">
        <span class="section-title">{title}</span>
        {pill_html}
    </div>
    """, unsafe_allow_html=True)


def progress_bar(pct: float, color: str = PALETTE["accent"]):
    st.markdown(f"""
    <div class="progress-wrap">
        <div class="progress-fill" style="width:{pct}%; background:{color};"></div>
    </div>
    """, unsafe_allow_html=True)


def readiness_card(score: int, category: str):
    cat_colors = {
        "Beginner":        PALETTE["red"],
        "Intermediate":    PALETTE["medium"],
        "Interview Ready": PALETTE["green"],
    }
    cat_color = cat_colors.get(category, PALETTE["accent"])
    st.markdown(f"""
    <div class="readiness-card">
        <div style="font-size:0.75rem;font-weight:600;color:{PALETTE['muted']};
                    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem;">
            Interview Readiness Score
        </div>
        <div class="readiness-score">{score}</div>
        <div class="readiness-label" style="color:{cat_color};">{category}</div>
    </div>
    """, unsafe_allow_html=True)


def recommendation_card(text: str):
    st.markdown(f'<div class="rec-card">{text}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding:1rem 0 0.5rem 0;">
            <div style="font-size:1.4rem;font-weight:800;
                        background:linear-gradient(90deg,#6C63FF,#00D4AA);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        background-clip:text;">
                ⚡ CodeTrack AI
            </div>
            <div style="font-size:0.75rem;color:#8B8FA8;margin-top:0.2rem;">
                Interview Performance Analyzer
            </div>
        </div>
        <hr style="border-color:#2A2D3E;margin:0.75rem 0;">
        """, unsafe_allow_html=True)

        page = st.radio(
            "Navigate",
            ["🏠  Dashboard", "➕  Add Problem", "📊  Analytics",
             "🎯  Readiness", "📋  Problem Log"],
            label_visibility="collapsed",
        )

        st.markdown("<hr style='border-color:#2A2D3E;margin:1rem 0;'>", unsafe_allow_html=True)

        # Quick stats in sidebar
        df = load_data()
        if not df.empty:
            solved = len(df[df["status"] == "Solved"])
            total  = len(df)
            acc    = round(solved / total * 100) if total else 0

            st.markdown(f"""
            <div style="font-size:0.72rem;color:#8B8FA8;text-transform:uppercase;
                        letter-spacing:0.08em;margin-bottom:0.6rem;">Quick Stats</div>
            <div style="display:grid;gap:0.5rem;">
                <div style="display:flex;justify-content:space-between;font-size:0.82rem;">
                    <span style="color:#8B8FA8;">Total</span>
                    <span style="font-weight:700;font-family:'JetBrains Mono',monospace;">{total}</span>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:0.82rem;">
                    <span style="color:#8B8FA8;">Solved</span>
                    <span style="font-weight:700;font-family:'JetBrains Mono',monospace;
                                 color:#00D4AA;">{solved}</span>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:0.82rem;">
                    <span style="color:#8B8FA8;">Accuracy</span>
                    <span style="font-weight:700;font-family:'JetBrains Mono',monospace;
                                 color:#6C63FF;">{acc}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#2A2D3E;margin:1rem 0;'>", unsafe_allow_html=True)

        # Upload CSV
        st.markdown(
            '<div style="font-size:0.72rem;color:#8B8FA8;text-transform:uppercase;'
            'letter-spacing:0.08em;margin-bottom:0.6rem;">Import Data</div>',
            unsafe_allow_html=True
        )
        uploaded = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
        if uploaded:
            try:
                new_df = pd.read_csv(uploaded)
                new_df = _clean_df(new_df)
                save_data(new_df)
                st.success("✓ Data imported")
                st.rerun()
            except Exception as e:
                st.error(f"Import failed: {e}")

        # Download button
        df_dl = load_data()
        if not df_dl.empty:
            csv_bytes = df_dl.to_csv(index=False).encode()
            st.download_button(
                "⬇ Export CSV",
                data=csv_bytes,
                file_name="codetrack_problems.csv",
                mime="text/csv",
                use_container_width=True,
            )

    return page.strip().split("  ", 1)[-1]   # strip emoji + spaces


# ─────────────────────────────────────────────
# PAGES
# ─────────────────────────────────────────────

def page_dashboard():
    df = load_data()

    st.markdown("""
    <div class="page-banner">
        <div>
            <div class="banner-title">Dashboard</div>
            <div class="banner-subtitle">Your coding interview preparation at a glance</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.info("No problems yet. Head to **Add Problem** or upload a CSV to get started.")
        return

    stats = compute_stats(df)
    score, category, _ = compute_readiness(stats, df)

    # ── Top KPI row ──
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: metric_card("Total Problems",    stats["total"])
    with c2: metric_card("Solved",            stats["solved"],   delta_up=True)
    with c3: metric_card("Accuracy",          f"{stats['accuracy']}%",
                         delta="goal 80%" if stats["accuracy"] < 80 else "✓ target met",
                         delta_up=(stats["accuracy"] >= 80))
    with c4: metric_card("Avg. Solve Time",   f"{stats['avg_time']}m")
    with c5: metric_card("Readiness Score",   score)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Difficulty breakdown ──
    section_header("Difficulty Breakdown", pill="overview")
    dc1, dc2, dc3 = st.columns(3)
    diff_totals = df.groupby("difficulty").size().to_dict()
    diff_solved = df[df["status"]=="Solved"].groupby("difficulty").size().to_dict()
    for col, diff in zip([dc1, dc2, dc3], ["Easy", "Medium", "Hard"]):
        with col:
            tot = diff_totals.get(diff, 0)
            sol = diff_solved.get(diff, 0)
            pct = round(sol/tot*100) if tot else 0
            color = DIFFICULTY_COLORS[diff]
            st.markdown(f"""
            <div class="metric-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span class="badge badge-{diff.lower()}">{diff}</span>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.85rem;
                                 color:{PALETTE['muted']};">{sol}/{tot}</span>
                </div>
                <div style="font-size:1.6rem;font-weight:800;margin:0.6rem 0;
                            color:{color};font-family:'JetBrains Mono',monospace;">
                    {pct}%
                </div>
            """, unsafe_allow_html=True)
            progress_bar(pct, color)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row 1 ──
    section_header("Performance Visualizations", pill="charts")
    ch1, ch2 = st.columns([1.5, 1])
    with ch1:
        st.plotly_chart(chart_topic_bar(df), use_container_width=True)
    with ch2:
        st.plotly_chart(chart_difficulty_pie(df), use_container_width=True)

    # ── Charts row 2 ──
    ch3, ch4 = st.columns(2)
    with ch3:
        if df["date_solved"].notna().any():
            st.plotly_chart(chart_progress_line(df), use_container_width=True)
    with ch4:
        st.plotly_chart(chart_weekly_heatmap(df), use_container_width=True)


def page_add_problem():
    st.markdown("""
    <div class="page-banner">
        <div>
            <div class="banner-title">Add Problem</div>
            <div class="banner-subtitle">Log a new coding problem to your tracker</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("add_problem_form", clear_on_submit=True):
        c1, c2 = st.columns([2, 1])
        with c1:
            name = st.text_input("Problem Name *", placeholder="e.g. Two Sum")
        with c2:
            topic = st.selectbox("Topic *", TOPICS)

        c3, c4, c5 = st.columns(3)
        with c3:
            difficulty = st.selectbox("Difficulty *", DIFFICULTIES)
        with c4:
            status = st.selectbox("Status *", STATUSES)
        with c5:
            time_taken = st.number_input("Time Taken (min)", min_value=1, max_value=600, value=30)

        date_solved = st.date_input("Date Solved", value=date.today())

        submitted = st.form_submit_button("Save Problem ✓")

    if submitted:
        if not name.strip():
            st.error("Problem name is required.")
        else:
            add_problem(name, topic, difficulty, status, time_taken, date_solved)
            st.success(f"✓ **{name}** added successfully!")
            st.balloons()

    # ── Recent problems preview ──
    df = load_data()
    if not df.empty:
        section_header("Recently Added", pill="last 10")
        recent = df.sort_values("date_solved", ascending=False).head(10).copy()
        recent["date_solved"] = recent["date_solved"].dt.strftime("%Y-%m-%d")
        recent["difficulty"] = recent["difficulty"].apply(
            lambda d: f'<span class="badge badge-{d.lower()}">{d}</span>'
        )
        recent["status"] = recent["status"].apply(
            lambda s: f'<span class="badge badge-{"solved" if s=="Solved" else "unsolved"}">{s}</span>'
        )
        display_cols = ["problem_name", "topic", "difficulty", "status", "time_taken", "date_solved"]
        html_table = recent[display_cols].rename(columns={
            "problem_name": "Problem", "topic": "Topic",
            "difficulty": "Diff", "status": "Status",
            "time_taken": "Time (min)", "date_solved": "Date",
        }).to_html(escape=False, index=False,
                   classes="dataframe",
                   border=0)
        st.markdown(html_table, unsafe_allow_html=True)


def page_analytics():
    df = load_data()

    st.markdown("""
    <div class="page-banner">
        <div>
            <div class="banner-title">Analytics</div>
            <div class="banner-subtitle">Deep-dive into your performance patterns</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.info("No data yet. Add some problems first.")
        return

    stats = compute_stats(df)

    # ── Strengths & Weaknesses ──
    section_header("Strengths & Weaknesses", pill="AI insight")
    bt = stats["by_topic"]
    strengths = bt[bt["accuracy"] >= 70].sort_values("accuracy", ascending=False)
    weaknesses = bt[(bt["accuracy"] < 60) & (bt["total"] >= 2)].sort_values("accuracy")

    sw1, sw2 = st.columns(2)
    with sw1:
        st.markdown(
            '<div style="font-size:0.8rem;font-weight:600;color:#00D4AA;'
            'text-transform:uppercase;letter-spacing:0.07em;margin-bottom:0.6rem;">✅ Strengths</div>',
            unsafe_allow_html=True
        )
        if strengths.empty:
            st.caption("Keep solving to unlock strengths.")
        else:
            chips = "".join(
                f'<span class="strength-chip">{r.topic} {r.accuracy:.0f}%</span>'
                for _, r in strengths.iterrows()
            )
            st.markdown(chips, unsafe_allow_html=True)

    with sw2:
        st.markdown(
            '<div style="font-size:0.8rem;font-weight:600;color:#FF4D6D;'
            'text-transform:uppercase;letter-spacing:0.07em;margin-bottom:0.6rem;">⚠️ Needs Work</div>',
            unsafe_allow_html=True
        )
        if weaknesses.empty:
            st.caption("No weak spots detected — great work!")
        else:
            chips = "".join(
                f'<span class="weakness-chip">{r.topic} {r.accuracy:.0f}%</span>'
                for _, r in weaknesses.iterrows()
            )
            st.markdown(chips, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Highlight stats ──
    section_header("Practice Insights", pill="breakdown")
    most_practiced = bt.sort_values("total", ascending=False).iloc[0]["topic"] if not bt.empty else "—"
    least_practiced = bt.sort_values("total").iloc[0]["topic"] if not bt.empty else "—"
    best_accuracy   = bt.sort_values("accuracy", ascending=False).iloc[0]["topic"] if not bt.empty else "—"
    worst_accuracy  = bt[bt["total"] >= 2].sort_values("accuracy").iloc[0]["topic"] \
                      if not bt[bt["total"] >= 2].empty else "—"

    i1, i2, i3, i4 = st.columns(4)
    with i1: metric_card("Most Practiced", most_practiced)
    with i2: metric_card("Least Practiced", least_practiced)
    with i3: metric_card("Best Accuracy", best_accuracy)
    with i4: metric_card("Needs Focus", worst_accuracy)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ──
    section_header("Accuracy Analysis", pill="by topic")
    st.plotly_chart(chart_accuracy_by_topic(stats), use_container_width=True)

    ch1, ch2 = st.columns(2)
    with ch1:
        if df["date_solved"].notna().any():
            st.plotly_chart(chart_progress_line(df), use_container_width=True)
    with ch2:
        st.plotly_chart(chart_weekly_heatmap(df), use_container_width=True)

    # ── Topic-level table ──
    section_header("Topic Summary Table", pill="full breakdown")
    tbl = bt.sort_values("total", ascending=False).copy()
    tbl.columns = ["Topic", "Total", "Solved", "Accuracy (%)"]
    tbl["Accuracy (%)"] = tbl["Accuracy (%)"].round(1)
    tbl["Unsolved"] = tbl["Total"] - tbl["Solved"]
    st.dataframe(
        tbl[["Topic", "Total", "Solved", "Unsolved", "Accuracy (%)"]],
        use_container_width=True,
        hide_index=True,
    )


def page_readiness():
    df = load_data()

    st.markdown("""
    <div class="page-banner">
        <div>
            <div class="banner-title">Interview Readiness</div>
            <div class="banner-subtitle">Your personalised readiness score and action plan</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.info("No data yet. Add some problems first.")
        return

    stats = compute_stats(df)
    score, category, recommendations = compute_readiness(stats, df)

    # ── Score card + gauge ──
    r1, r2 = st.columns([1, 2])
    with r1:
        readiness_card(score, category)
        st.markdown("<br>", unsafe_allow_html=True)
        progress_bar(score, PALETTE["accent"])
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;'
            f'font-size:0.72rem;color:{PALETTE["muted"]};">'
            f'<span>0 · Beginner</span><span>65 · Intermediate</span>'
            f'<span>90 · Ready</span></div>',
            unsafe_allow_html=True
        )

    with r2:
        # Build gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Interview Readiness", "font": {"size": 16, "color": PALETTE["text"]}},
            number={"font": {"size": 48, "color": PALETTE["text"],
                             "family": "JetBrains Mono"}},
            gauge={
                "axis": {"range": [0, 100], "tickfont": {"color": PALETTE["muted"]},
                         "tickcolor": PALETTE["muted"]},
                "bar": {"color": PALETTE["accent"], "thickness": 0.25},
                "bgcolor": PALETTE["border"],
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 30],  "color": PALETTE["red"]   + "33"},
                    {"range": [30, 65], "color": PALETTE["medium"]+ "33"},
                    {"range": [65, 100],"color": PALETTE["green"] + "33"},
                ],
                "threshold": {
                    "line": {"color": PALETTE["green"], "width": 3},
                    "thickness": 0.75,
                    "value": 65,
                },
            },
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color=PALETTE["text"]),
            height=300,
            margin=dict(t=30, b=0, l=30, r=30),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Score breakdown ──
    section_header("Score Breakdown", pill="how it's calculated")
    solved_df = df[df["status"] == "Solved"]
    diff_dist  = solved_df["difficulty"].value_counts(normalize=True).to_dict() if not solved_df.empty else {}
    core_topics = {"Arrays", "Dynamic Programming", "Graphs", "Trees",
                   "Linked Lists", "Binary Search", "Sliding Window", "Backtracking"}
    covered_core = len(set(df["topic"].unique()) & core_topics)

    sub_scores = {
        "Volume (max 30)":          round(min(stats["solved"] / 150 * 30, 30), 1),
        "Accuracy (max 25)":        round(stats["accuracy"] / 100 * 25, 1),
        "Difficulty Mix (max 25)":  round(diff_dist.get("Hard", 0)*15 + diff_dist.get("Medium", 0)*10, 1),
        "Topic Coverage (max 20)":  round(covered_core / len(core_topics) * 20, 1),
    }

    for label, sub in sub_scores.items():
        mx = int(label.split("max ")[-1].rstrip(")"))
        pct = sub / mx * 100 if mx else 0
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.markdown(
                f'<div style="font-size:0.82rem;color:{PALETTE["text"]};'
                f'margin-bottom:0.2rem;">{label}</div>',
                unsafe_allow_html=True
            )
            progress_bar(pct, PALETTE["accent"])
        with col_b:
            st.markdown(
                f'<div style="font-size:1rem;font-weight:700;font-family:"JetBrains Mono",monospace;'
                f'color:{PALETTE["text"]};text-align:right;padding-top:0.1rem;">'
                f'{sub}/{mx}</div>',
                unsafe_allow_html=True
            )

    # ── Recommendations ──
    section_header("Personalised Recommendations", pill="action plan")
    for rec in recommendations:
        recommendation_card(rec)


def page_problem_log():
    df = load_data()

    st.markdown("""
    <div class="page-banner">
        <div>
            <div class="banner-title">Problem Log</div>
            <div class="banner-subtitle">Browse, filter and manage all your problems</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.info("No problems yet. Add some from the **Add Problem** page.")
        return

    # ── Filters ──
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        topic_filter = st.multiselect("Topic", sorted(df["topic"].unique()), placeholder="All Topics")
    with f2:
        diff_filter = st.multiselect("Difficulty", DIFFICULTIES, placeholder="All Difficulties")
    with f3:
        status_filter = st.multiselect("Status", STATUSES, placeholder="All Statuses")
    with f4:
        search = st.text_input("Search", placeholder="Problem name…")

    filtered = df.copy()
    if topic_filter:  filtered = filtered[filtered["topic"].isin(topic_filter)]
    if diff_filter:   filtered = filtered[filtered["difficulty"].isin(diff_filter)]
    if status_filter: filtered = filtered[filtered["status"].isin(status_filter)]
    if search:        filtered = filtered[filtered["problem_name"].str.contains(search, case=False, na=False)]

    st.markdown(
        f'<div style="font-size:0.8rem;color:{PALETTE["muted"]};margin:0.5rem 0 1rem 0;">'
        f'Showing <b style="color:{PALETTE["text"]};">{len(filtered)}</b> of '
        f'<b style="color:{PALETTE["text"]};">{len(df)}</b> problems</div>',
        unsafe_allow_html=True
    )

    if filtered.empty:
        st.warning("No problems match your filters.")
        return

    display = filtered.sort_values("date_solved", ascending=False).copy()
    display["date_solved"] = display["date_solved"].dt.strftime("%Y-%m-%d")
    st.dataframe(
        display.rename(columns={
            "problem_name": "Problem", "topic": "Topic",
            "difficulty": "Difficulty", "status": "Status",
            "time_taken": "Time (min)", "date_solved": "Date",
        })[["Problem", "Topic", "Difficulty", "Status", "Time (min)", "Date"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Difficulty": st.column_config.SelectboxColumn(
                options=DIFFICULTIES, width="small"
            ),
            "Status": st.column_config.SelectboxColumn(
                options=STATUSES, width="small"
            ),
            "Time (min)": st.column_config.NumberColumn(format="%d min"),
        },
    )


# ─────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────

def main():
    inject_css()
    page = render_sidebar()

    routes = {
        "Dashboard":    page_dashboard,
        "Add Problem":  page_add_problem,
        "Analytics":    page_analytics,
        "Readiness":    page_readiness,
        "Problem Log":  page_problem_log,
    }

    handler = routes.get(page, page_dashboard)
    handler()


if __name__ == "__main__":
    main()

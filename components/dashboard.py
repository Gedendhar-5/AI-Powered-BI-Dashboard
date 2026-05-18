"""
components/dashboard.py
=======================
Phase 2 + Phase 3 — Full dashboard: KPIs → Charts → Anomaly Radar → Chatbot.

FIXES:
  - Anomaly Radar: uses None sentinel (not []) so empty-list false-cache bug is gone
  - Anomaly Radar: always shows a message even when no outliers found
  - Anomaly Radar: displays a mini Plotly box-plot for each flagged column
  - Chatbot: full multi-turn conversation with session memory
"""

from __future__ import annotations
from typing import List, Dict, Any

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from modules.analyzer import (
    get_chart_configs,
    get_kpi_cards,
    get_anomaly_narratives,
    ask_gemini_about_data,
)
from modules.cleaner import CleanResult


# ── Plotly dark theme ──────────────────────────────────────────────────────────
PLOTLY_COLORS = [
    "#6366f1", "#06b6d4", "#10b981", "#f59e0b",
    "#ef4444", "#8b5cf6", "#ec4899", "#14b8a6",
]
_BASE_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#9090a8", size=12),
    title_font=dict(family="Inter, sans-serif", color="#f0f0f8", size=15),
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.08)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.08)"),
    colorway=PLOTLY_COLORS,
)


# ─────────────────────────────────────────────────────────────────────────────
# Main entry — called from app.py
# ─────────────────────────────────────────────────────────────────────────────

def render_dashboard(result: CleanResult, gemini_summary: dict) -> None:
    """Renders KPIs → Charts → Anomaly Radar in the Dashboard tab."""
    df = result.df
    _render_kpis(df)
    st.markdown("<br>", unsafe_allow_html=True)
    _render_charts(df, gemini_summary)
    st.markdown("<br>", unsafe_allow_html=True)
    _render_anomalies(df, result)


def render_chatbot(result: CleanResult, gemini_summary: dict) -> None:
    """Renders the Phase 3 AI chatbot — called from the Ask AI tab in app.py."""
    _render_chat_ui(result.df, gemini_summary)


# ─────────────────────────────────────────────────────────────────────────────
# KPI Cards
# ─────────────────────────────────────────────────────────────────────────────

def _render_kpis(df: pd.DataFrame) -> None:
    st.markdown(
        '<div class="section-title">⚡ Key Metrics <span class="tag">Live</span></div>',
        unsafe_allow_html=True,
    )
    kpis = get_kpi_cards(df)
    if not kpis:
        st.info("No numeric columns found for KPI cards.")
        return

    # Skeleton shown only on first load (session state trick not needed —
    # get_kpi_cards is synchronous so we skip showing skeleton here)

    for row_start in range(0, min(len(kpis), 8), 4):
        row = kpis[row_start : row_start + 4]
        cols = st.columns(len(row))
        for col, kpi in zip(cols, row):
            with col:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                      <span class="kpi-icon">{kpi['icon']}</span>
                      <div class="kpi-label">{kpi['label']}</div>
                      <div class="kpi-value">{kpi['value']}</div>
                      <div class="kpi-delta {kpi['delta_type']}">{kpi['delta_label']}</div>
                      <div style="font-size:0.7rem;color:var(--text-muted);margin-top:.3rem;">
                        {kpi['detail']}
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        if row_start + 4 < min(len(kpis), 8):
            st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# AI Charts
# ─────────────────────────────────────────────────────────────────────────────

def _render_charts(df: pd.DataFrame, gemini_summary: dict) -> None:
    st.markdown(
        '<div class="section-title">📊 AI-Generated Visualisations '
        '<span class="tag">Gemini</span></div>',
        unsafe_allow_html=True,
    )

    # Use None sentinel — empty list [] means "tried and got nothing"
    if st.session_state.get("chart_configs") is None or        st.session_state.get("chart_configs") == []:
        # Show skeleton placeholders while Gemini works
        sk1, sk2 = st.columns(2)
        with sk1:
            st.markdown('<div class="skeleton skeleton-chart"></div>', unsafe_allow_html=True)
        with sk2:
            st.markdown('<div class="skeleton skeleton-chart"></div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-top:.6rem;'></div>", unsafe_allow_html=True)
        sk3, sk4 = st.columns(2)
        with sk3:
            st.markdown('<div class="skeleton skeleton-chart"></div>', unsafe_allow_html=True)
        with sk4:
            st.markdown('<div class="skeleton skeleton-chart"></div>', unsafe_allow_html=True)

        with st.spinner("🤖 Gemini is selecting the best charts for your data…"):
            try:
                configs = get_chart_configs(gemini_summary)
            except Exception as e:
                st.error(f"❌ Gemini chart generation failed: {e}")
                return
        st.session_state["chart_configs"] = configs if configs else "__empty__"
        st.rerun()  # rerun so skeletons are replaced by real charts
    
    raw = st.session_state.get("chart_configs")
    configs = [] if raw == "__empty__" else (raw if isinstance(raw, list) else [])

    if not configs:
        st.warning("Gemini couldn't determine charts for this dataset. Try a richer CSV with more numeric columns.")
        return

    for i in range(0, len(configs), 2):
        col_l, col_r = st.columns(2)
        with col_l:
            _render_single_chart(df, configs[i])
        with col_r:
            if i + 1 < len(configs):
                _render_single_chart(df, configs[i + 1])


def _render_single_chart(df: pd.DataFrame, cfg: dict) -> None:
    chart_type = cfg.get("chart_type", "bar")
    x_col      = cfg.get("x")
    y_col      = cfg.get("y")
    title      = cfg.get("title", "Chart")
    insight    = cfg.get("insight", "")

    if x_col not in df.columns:
        st.warning(f"Column '{x_col}' not found in dataset.")
        return
    if y_col and y_col not in df.columns:
        y_col = None

    try:
        fig = _build_figure(df, chart_type, x_col, y_col)
    except Exception as e:
        st.warning(f"Could not render '{title}': {e}")
        return

    if fig is None:
        return

    fig.update_layout(**_BASE_LAYOUT)
    fig.update_layout(title_text=title)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    if insight:
        st.markdown(
            f'<div class="insight-box">💡 <strong>Insight:</strong> {insight}</div>',
            unsafe_allow_html=True,
        )


def _build_figure(
    df: pd.DataFrame,
    chart_type: str,
    x_col: str,
    y_col: str | None,
) -> go.Figure | None:
    c = PLOTLY_COLORS

    if chart_type == "bar":
        if y_col:
            agg = df.groupby(x_col)[y_col].sum().reset_index().sort_values(y_col, ascending=False)
            fig = px.bar(agg, x=x_col, y=y_col, color=x_col, color_discrete_sequence=c)
        else:
            vc = df[x_col].value_counts().reset_index()
            vc.columns = [x_col, "count"]
            fig = px.bar(vc, x=x_col, y="count", color=x_col, color_discrete_sequence=c)
        fig.update_traces(marker_line_width=0)

    elif chart_type == "line":
        if not y_col:
            return None
        plot_df = df[[x_col, y_col]].dropna().sort_values(x_col)
        fig = px.line(plot_df, x=x_col, y=y_col, color_discrete_sequence=c, markers=True)
        fig.update_traces(line_width=2.5, marker_size=5)

    elif chart_type == "pie":
        if y_col:
            agg = df.groupby(x_col)[y_col].sum().reset_index()
            fig = px.pie(agg, names=x_col, values=y_col, color_discrete_sequence=c, hole=0.4)
        else:
            vc = df[x_col].value_counts().reset_index()
            vc.columns = [x_col, "count"]
            fig = px.pie(vc, names=x_col, values="count", color_discrete_sequence=c, hole=0.4)
        fig.update_traces(textposition="inside", textinfo="percent+label")

    elif chart_type == "scatter":
        if not y_col:
            return None
        fig = px.scatter(df, x=x_col, y=y_col, color_discrete_sequence=c, opacity=0.7)
        fig.update_traces(marker_size=6)

    elif chart_type == "histogram":
        fig = px.histogram(df, x=x_col, color_discrete_sequence=c, nbins=30)
        fig.update_traces(marker_line_width=0)

    elif chart_type == "box":
        if y_col:
            fig = px.box(df, x=x_col, y=y_col, color=x_col, color_discrete_sequence=c)
        else:
            fig = px.box(df, y=x_col, color_discrete_sequence=c)

    else:
        return None

    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Anomaly Radar  — FIXED
# ─────────────────────────────────────────────────────────────────────────────

def _render_anomalies(df: pd.DataFrame, result: CleanResult) -> None:
    st.markdown(
        '<div class="section-title">🚨 Anomaly Radar '
        '<span class="tag">AI Narrated</span></div>',
        unsafe_allow_html=True,
    )

    # Collect columns that actually have outliers
    outlier_cols = {
        name: meta
        for name, meta in result.columns.items()
        if getattr(meta, "outlier_count", 0) > 0
    }

    # ── No outliers found ─────────────────────────────────────────────────────
    if not outlier_cols:
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:.75rem;
                        background:var(--green-soft);border:1px solid rgba(16,185,129,.25);
                        border-left:3px solid var(--green);border-radius:10px;
                        padding:1rem 1.25rem;">
              <span style="font-size:1.5rem;">✅</span>
              <div>
                <strong style="color:var(--green);">No anomalies detected</strong><br>
                <span style="font-size:.85rem;color:var(--text-secondary);">
                  Every numeric column passed the IQR outlier check.
                  Your data looks clean!
                </span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # ── Fetch AI narratives (None = not fetched yet, [] = no outliers) ────────
    # Use a dedicated key; default in session_state is set to None in app.py
    cache_key = "anomaly_narratives"

    if st.session_state.get(cache_key) is None:
        with st.spinner("🤖 Gemini is analysing anomalies…"):
            try:
                narratives = get_anomaly_narratives(df, result.columns)
            except Exception as exc:
                # Graceful fallback — show stats without AI narrative
                narratives = [
                    {
                        "col":       name,
                        "count":     meta.outlier_count,
                        "pct":       round(meta.outlier_count / max(len(df), 1) * 100, 1),
                        "mean":      round(float(df[name].mean()), 2) if name in df else 0,
                        "median":    round(float(df[name].median()), 2) if name in df else 0,
                        "narrative": f"{meta.outlier_count} value(s) fall outside the expected IQR range.",
                        "sample":    list(meta.outlier_values[:5]),
                    }
                    for name, meta in list(outlier_cols.items())[:4]
                ]
        st.session_state[cache_key] = narratives
    else:
        narratives = st.session_state[cache_key]

    # If narratives is still None or empty after fetch, build fallback
    if not narratives:
        narratives = [
            {
                "col":       name,
                "count":     meta.outlier_count,
                "pct":       round(meta.outlier_count / max(len(df), 1) * 100, 1),
                "mean":      0,
                "median":    0,
                "narrative": f"{meta.outlier_count} value(s) fall outside the expected IQR range.",
                "sample":    list(meta.outlier_values[:5]),
            }
            for name, meta in list(outlier_cols.items())[:4]
        ]

    # ── Render each anomaly callout + mini box-plot ───────────────────────────
    for item in narratives:
        col_name   = item["col"]
        count      = item["count"]
        pct        = item.get("pct", 0)
        narrative  = item.get("narrative", "")
        sample     = item.get("sample", [])
        sample_str = ", ".join(str(v) for v in sample[:3])

        left, right = st.columns([2, 1])

        with left:
            st.markdown(
                f"""
                <div class="anomaly-card">
                  <span class="anomaly-icon">⚠️</span>
                  <div class="anomaly-text">
                    <div style="margin-bottom:.35rem;">
                      <span class="anomaly-col">{col_name}</span>
                      &nbsp;
                      <span style="font-size:.78rem;color:var(--text-muted);">
                        {count} outlier(s) &nbsp;·&nbsp; {pct}% of rows
                      </span>
                    </div>
                    <div style="font-size:.82rem;color:var(--text-secondary);
                                line-height:1.55;margin-bottom:.4rem;">
                      {narrative}
                    </div>
                    <div style="font-size:.75rem;color:var(--text-muted);">
                      Sample outlier values: <strong style="color:var(--text-primary);">
                      {sample_str}</strong>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with right:
            # Mini box-plot to visualise the outlier distribution
            if col_name in df.columns and pd.api.types.is_numeric_dtype(df[col_name]):
                fig = px.box(
                    df, y=col_name,
                    color_discrete_sequence=["#ef4444"],
                    points="outliers",
                )
                # _BASE_LAYOUT already has margin — build a copy without it
                # to avoid duplicate-keyword TypeError
                _mini = {k: v for k, v in _BASE_LAYOUT.items() if k != "margin"}
                fig.update_layout(**_mini)
                fig.update_layout(
                    margin=dict(l=10, r=10, t=30, b=10),
                    height=180,
                    showlegend=False,
                    title_text=col_name,
                    title_font_size=12,
                )
                fig.update_traces(marker_color="#ef4444", marker_size=5)
                st.plotly_chart(
                    fig, use_container_width=True,
                    config={"displayModeBar": False},
                )

        st.markdown("<div style='margin-bottom:.75rem;'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Phase 3 — AI Chatbot UI
# ─────────────────────────────────────────────────────────────────────────────

def _render_chat_ui(df: pd.DataFrame, gemini_summary: dict) -> None:
    """Full multi-turn chatbot with conversation memory."""

    st.markdown(
        '<div class="section-title">💬 Ask AI About Your Data '
        '<span class="tag">Phase 3</span></div>',
        unsafe_allow_html=True,
    )

    # Initialise message history in session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # ── Suggested starter questions ───────────────────────────────────────────
    if not st.session_state["messages"]:
        st.markdown(
            "<p style='font-size:.85rem;color:var(--text-secondary);"
            "margin-bottom:.6rem;'>Try asking:</p>",
            unsafe_allow_html=True,
        )
        suggestions = [
            "What are the top 5 rows by value?",
            "Which column has the most missing data?",
            "Summarise the key trends in this dataset.",
            "What is the average value per category?",
        ]
        cols = st.columns(2)
        for i, suggestion in enumerate(suggestions):
            with cols[i % 2]:
                if st.button(suggestion, key=f"sugg_{i}", use_container_width=True):
                    st.session_state["messages"].append(
                        {"role": "user", "content": suggestion}
                    )
                    with st.spinner("🤖 Thinking…"):
                        try:
                            reply = ask_gemini_about_data(
                                suggestion,
                                gemini_summary,
                                st.session_state["messages"][:-1],
                            )
                        except Exception as e:
                            reply = f"Sorry, I couldn't answer that: {e}"
                    st.session_state["messages"].append(
                        {"role": "assistant", "content": reply}
                    )
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

    # ── Render conversation history ───────────────────────────────────────────
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ── Chat input ────────────────────────────────────────────────────────────
    user_input = st.chat_input(
        "Ask anything about your data…  e.g. 'Which month had the highest sales?'"
    )

    if user_input:
        # Append user message and show it immediately
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Call Gemini with full history context
        with st.chat_message("assistant"):
            with st.spinner("🤖 Analysing your data…"):
                try:
                    reply = ask_gemini_about_data(
                        user_input,
                        gemini_summary,
                        st.session_state["messages"][:-1],  # history without current Q
                    )
                except Exception as e:
                    reply = f"❌ Gemini error: {e}"
            st.markdown(reply)

        st.session_state["messages"].append({"role": "assistant", "content": reply})

    # ── Clear conversation button ─────────────────────────────────────────────
    if st.session_state.get("messages"):
        if st.button("🗑️ Clear conversation", key="clear_chat"):
            st.session_state["messages"] = []
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# Phase 4 — Forecast Tab Renderer
# ─────────────────────────────────────────────────────────────────────────────

def render_forecast(result: CleanResult) -> None:
    """
    Renders the 30-day forecast tab.
    Shows a column selector, runs OLS regression + Gemini narrative,
    plots historical + forecast on one Plotly chart with confidence band.
    """
    from modules.forecaster import run_forecasts

    df = result.df

    st.markdown(
        '<div class="section-title">📈 30-Day Forecast '
        '<span class="tag">Phase 4</span></div>',
        unsafe_allow_html=True,
    )

    # ── Check for datetime column ─────────────────────────────────────────────
    dt_cols  = df.select_dtypes(include=["datetime64"]).columns.tolist()
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if not dt_cols:
        st.warning(
            "⚠️ No datetime column found in your dataset.  \n"
            "Forecast requires at least one date/time column. "
            "Make sure your CSV has a column like 'date', 'month', or 'timestamp'."
        )
        return

    if not num_cols:
        st.warning("⚠️ No numeric columns found to forecast.")
        return

    # ── Controls ──────────────────────────────────────────────────────────────
    col_left, col_right = st.columns([1, 1])
    with col_left:
        date_col = st.selectbox(
            "📅 Date / Time column",
            options=dt_cols,
            help="Column used as the X-axis (time axis)",
        )
    with col_right:
        target_cols = st.multiselect(
            "🔢 Numeric columns to forecast",
            options=num_cols,
            default=num_cols[:2],
            help="Select one or more numeric columns to forecast",
        )

    horizon = st.slider(
        "Forecast horizon (days)", min_value=7, max_value=90, value=30, step=1
    )

    if not target_cols:
        st.info("Select at least one numeric column above.")
        return

    # ── Run forecast ──────────────────────────────────────────────────────────
    cache_key = f"forecast_{date_col}_{'_'.join(target_cols)}_{horizon}"
    if st.session_state.get(cache_key) is None:
        with st.spinner("🤖 Running forecast + generating AI narrative…"):
            try:
                fc_results = run_forecasts(df, date_col, target_cols, horizon)
                st.session_state[cache_key] = fc_results
            except Exception as e:
                st.error(f"❌ Forecast error: {e}")
                return
    else:
        fc_results = st.session_state[cache_key]

    if not fc_results:
        st.warning("Could not generate a forecast. Ensure your numeric columns have at least 10 non-null values.")
        return

    # ── Render each forecast ──────────────────────────────────────────────────
    for fc in fc_results:
        st.markdown(f"#### 📊 {fc.col_name.replace('_', ' ').title()}")

        # Merge historical + forecast for plotting
        hist = fc.historical.copy()
        hist["type"] = "Historical"
        hist["lower"] = np.nan
        hist["upper"] = np.nan

        fcast = fc.forecast.copy()
        fcast["type"] = "Forecast"

        combined = pd.concat(
            [hist.rename(columns={fc.col_name: "_val"}),
             fcast.rename(columns={fc.col_name: "_val"})],
            ignore_index=True,
        )

        # Build Plotly figure
        fig = go.Figure()

        # Historical line
        h = hist.rename(columns={fc.col_name: "_val"})
        fig.add_trace(go.Scatter(
            x=h[fc.date_col], y=h["_val"],
            mode="lines+markers",
            name="Historical",
            line=dict(color="#6366f1", width=2.5),
            marker=dict(size=4),
        ))

        # Confidence band (shaded area)
        f = fcast.rename(columns={fc.col_name: "_val"})
        fig.add_trace(go.Scatter(
            x=pd.concat([f[fc.date_col], f[fc.date_col][::-1]]),
            y=pd.concat([f["upper"], f["lower"][::-1]]),
            fill="toself",
            fillcolor="rgba(239,68,68,0.1)",
            line=dict(color="rgba(0,0,0,0)"),
            showlegend=False,
            name="95% CI",
        ))

        # Forecast line
        fig.add_trace(go.Scatter(
            x=f[fc.date_col], y=f["_val"],
            mode="lines",
            name="Forecast",
            line=dict(color="#ef4444", width=2.5, dash="dash"),
        ))

        # Layout — no duplicate margin issue here
        fig.update_layout(
            **_BASE_LAYOUT,
            title_text=f"{fc.col_name.replace('_', ' ').title()} — {horizon}-Day Forecast",
            xaxis_title=fc.date_col,
            yaxis_title=fc.col_name,
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Stats row
        s1, s2, s3 = st.columns(3)
        with s1:
            dir_emoji = "📈" if fc.trend_direction == "upward" else "📉" if fc.trend_direction == "downward" else "➡️"
            st.metric("Trend", f"{dir_emoji} {fc.trend_direction.title()}")
        with s2:
            st.metric("Daily slope", f"{fc.slope:+.4f} / day")
        with s3:
            st.metric("R² fit", f"{fc.r_squared:.2f}")

        # AI narrative
        st.markdown(
            f'<div class="insight-box">🤖 <strong>AI Forecast Narrative:</strong> {fc.narrative}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Phase 4 — Export Tab Renderer
# ─────────────────────────────────────────────────────────────────────────────

def render_export(result: CleanResult, file_name: str) -> None:
    """
    Renders the Export tab with:
      - Download cleaned CSV (always available)
      - Download full PDF dashboard report (requires kaleido)
    """
    from modules.exporter import get_csv_bytes, export_charts_to_pdf
    from modules.analyzer import get_kpi_cards

    st.markdown(
        '<div class="section-title">📥 Export Your Data '
        '<span class="tag">Phase 4</span></div>',
        unsafe_allow_html=True,
    )

    df = result.df

    # ── CSV download ──────────────────────────────────────────────────────────
    st.markdown("#### ⬇️ Cleaned Dataset")
    st.markdown(
        '<div style="font-size:.85rem;color:var(--text-secondary);margin-bottom:.6rem;">'
        'Your data after auto-cleaning: nulls filled, duplicates removed, '
        'headers standardised.</div>',
        unsafe_allow_html=True,
    )
    csv_bytes = get_csv_bytes(df)
    st.download_button(
        label=f"⬇️ Download cleaned_{file_name}.csv",
        data=csv_bytes,
        file_name=f"cleaned_{file_name}",
        mime="text/csv",
        use_container_width=True,
        type="primary",
        key="dl_csv",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ── PDF download ──────────────────────────────────────────────────────────
    st.markdown("#### 📄 Full Dashboard PDF Report")
    st.markdown(
        '<div style="font-size:.85rem;color:var(--text-secondary);margin-bottom:.8rem;">'
        'Exports KPI cards + all AI-generated charts into a formatted PDF report.</div>',
        unsafe_allow_html=True,
    )

    if st.button("🖨️ Generate PDF Report", use_container_width=True, key="gen_pdf"):
        with st.spinner("Building PDF — rendering charts…"):
            try:
                # Collect chart figures from session state chart configs
                chart_figs = []
                configs = st.session_state.get("chart_configs") or []
                if isinstance(configs, list):
                    from components.dashboard import _build_figure
                    for cfg in configs:
                        x_col = cfg.get("x")
                        y_col = cfg.get("y")
                        ctype = cfg.get("chart_type", "bar")
                        title = cfg.get("title", "Chart")
                        if x_col and x_col in df.columns:
                            try:
                                fig = _build_figure(df, ctype, x_col, y_col)
                                if fig:
                                    fig.update_layout(**_BASE_LAYOUT)
                                    fig.update_layout(title_text=title)
                                    chart_figs.append(fig)
                            except Exception:
                                pass

                kpis     = get_kpi_cards(df)
                pdf_bytes = export_charts_to_pdf(df, kpis, chart_figs, file_name)
                st.session_state["pdf_bytes"] = pdf_bytes
                st.success("✅ PDF ready — click below to download.")
            except ImportError as e:
                st.error(
                    f"❌ PDF export requires reportlab. "
                    f"Run: pip install reportlab kaleido==0.2.1\n\nError: {e}"
                )
            except Exception as e:
                st.error(f"❌ PDF generation failed: {e}")

    pdf_bytes = st.session_state.get("pdf_bytes")
    if pdf_bytes:
        st.download_button(
            label="⬇️ Download PDF Report",
            data=pdf_bytes,
            file_name=f"dashboard_{file_name.replace('.csv','')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="dl_pdf",
        )
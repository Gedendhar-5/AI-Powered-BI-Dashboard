"""
app.py — AI-Powered BI Dashboard  (Option A — Production Polish)
All 4 phases + polished upload landing + loading skeletons + toast notifications.
"""

from __future__ import annotations
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page config — first Streamlit call ───────────────────────────────────────
st.set_page_config(
    page_title="AI-Powered BI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS injection ─────────────────────────────────────────────────────────────
_css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
try:
    with open(_css_path) as _f:
        st.markdown(f"<style>{_f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# ── Local imports ─────────────────────────────────────────────────────────────
from components.sidebar     import render_sidebar
from components.health_card import render_health_card
from components.dashboard   import (
    render_dashboard,
    render_chatbot,
    render_forecast,
    render_export,
)
from modules.cleaner import load_and_clean, build_gemini_summary

# ── Session state ─────────────────────────────────────────────────────────────
_DEFAULTS: dict = {
    "clean_result":       None,
    "gemini_summary":     None,
    "messages":           [],
    "chart_configs":      None,   # None = not yet fetched
    "anomaly_narratives": None,   # None = not yet fetched
    "pdf_bytes":          None,
    "file_name":          None,
    "toast":              None,   # {"msg": str, "kind": "success"|"error"|"info"}
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ── Toast renderer ────────────────────────────────────────────────────────────
def _show_toast() -> None:
    t = st.session_state.get("toast")
    if not t:
        return
    kind  = t.get("kind", "info")
    icons = {"success": "✅", "error": "❌", "info": "ℹ️"}
    st.markdown(
        f'<div class="toast toast-{kind}">'
        f'{icons.get(kind,"ℹ️")} {t["msg"]}</div>',
        unsafe_allow_html=True,
    )
    st.session_state["toast"] = None   # consume after one render


def _toast(msg: str, kind: str = "info") -> None:
    st.session_state["toast"] = {"msg": msg, "kind": kind}


# ── KPI skeleton renderer ─────────────────────────────────────────────────────
def _skeleton_kpis(n: int = 4) -> None:
    cols = st.columns(n)
    for col in cols:
        with col:
            st.markdown(
                '<div class="skeleton skeleton-kpi"></div>',
                unsafe_allow_html=True,
            )


# ── Chart skeleton renderer ───────────────────────────────────────────────────
def _skeleton_charts(n: int = 4) -> None:
    for _ in range(n // 2):
        c1, c2 = st.columns(2)
        for col in (c1, c2):
            with col:
                st.markdown(
                    '<div class="skeleton skeleton-chart"></div>'
                    '<div style="margin-top:.5rem;">'
                    '  <div class="skeleton skeleton-text med"></div>'
                    '  <div class="skeleton skeleton-text short"></div>'
                    '</div>',
                    unsafe_allow_html=True,
                )
        st.markdown("<br>", unsafe_allow_html=True)


# ── Upload landing page ───────────────────────────────────────────────────────
def _render_upload_landing(inline_file) -> None:
    """Beautiful hero upload page shown when no data is loaded."""
    st.markdown(
        """
        <div class="upload-hero">
          <span class="upload-hero-icon">📊</span>
          <div class="upload-hero-title">Drop your data. Get instant insights.</div>
          <div class="upload-hero-sub">
            Upload any CSV or Excel file and Gemini AI will automatically
            clean it, pick the best charts, and answer your questions in plain English.
          </div>
          <div class="upload-feature-grid">
            <div class="upload-feature">
              <span class="upload-feature-icon">🧹</span>
              Auto-clean nulls, duplicates &amp; headers
            </div>
            <div class="upload-feature">
              <span class="upload-feature-icon">📊</span>
              AI-generated charts &amp; insights
            </div>
            <div class="upload-feature">
              <span class="upload-feature-icon">💬</span>
              Ask anything in plain English
            </div>
            <div class="upload-feature">
              <span class="upload-feature-icon">📈</span>
              30-day trend forecasting
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Centered uploader
    _, c2, _ = st.columns([1, 2, 1])
    with c2:
        file = st.file_uploader(
            "Drag & drop or click to browse",
            type=["csv", "xlsx", "xls"],
            key="inline_uploader",
            help="CSV, Excel (.xlsx / .xls) — max 200 MB",
        )
        st.caption(
            "🔒 Your data stays in your session — never stored or shared."
        )

    st.divider()
    return file


# ── Sidebar ───────────────────────────────────────────────────────────────────
sidebar_file = render_sidebar()

# ── App header ────────────────────────────────────────────────────────────────
_show_toast()
st.markdown(
    """
    <div class="app-header">
      <span class="app-header-icon">📊</span>
      <div>
        <div class="app-header-title">AI-Powered BI Dashboard</div>
        <div class="app-header-subtitle">
          Upload any dataset → Auto clean → AI visualisations → Ask anything in plain English
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Determine uploaded file ───────────────────────────────────────────────────
inline_file = None
no_data     = st.session_state.get("clean_result") is None

if no_data:
    inline_file = _render_upload_landing(None)

uploaded_file = sidebar_file or inline_file

# ── Process uploaded file ─────────────────────────────────────────────────────
if uploaded_file is not None:
    if st.session_state.file_name != uploaded_file.name:
        with st.spinner("⚙️ Reading and cleaning your data…"):
            try:
                result = load_and_clean(uploaded_file)
                st.session_state.clean_result       = result
                st.session_state.gemini_summary     = build_gemini_summary(result)
                st.session_state.file_name          = uploaded_file.name
                st.session_state.chart_configs      = None
                st.session_state.anomaly_narratives = None
                st.session_state.pdf_bytes          = None
                st.session_state.messages           = []
                for k in [k for k in st.session_state if k.startswith("forecast_")]:
                    del st.session_state[k]
                _toast(
                    f"✨ '{uploaded_file.name}' loaded — "
                    f"{result.cleaned_shape[0]:,} rows, {result.cleaned_shape[1]} columns.",
                    "success",
                )
                st.rerun()
            except ValueError as e:
                st.error(f"❌ {e}")
                st.stop()
            except Exception as e:
                st.error(f"❌ Unexpected error while processing your file: {e}")
                st.stop()

# ── Tabs ──────────────────────────────────────────────────────────────────────
if not no_data:
    tab_dash, tab_health, tab_chat, tab_forecast, tab_export = st.tabs(
        ["📊 Dashboard", "🏥 Health", "💬 Ask AI", "📈 Forecast", "📥 Export"]
    )

    result = st.session_state.get("clean_result")

    # ── Dashboard ─────────────────────────────────────────────────────────────
    with tab_dash:
        gemini_summary = st.session_state.get("gemini_summary", {})
        # render_dashboard handles its own spinner internally — call once only
        render_dashboard(result, gemini_summary)

    # ── Health ────────────────────────────────────────────────────────────────
    with tab_health:
        st.markdown(
            '<div class="section-title">🏥 Data Health Report '
            '<span class="tag">Phase 1</span></div>',
            unsafe_allow_html=True,
        )
        render_health_card(result)

    # ── Ask AI ────────────────────────────────────────────────────────────────
    with tab_chat:
        render_chatbot(result, st.session_state.get("gemini_summary", {}))

    # ── Forecast ──────────────────────────────────────────────────────────────
    with tab_forecast:
        render_forecast(result)

    # ── Export ────────────────────────────────────────────────────────────────
    with tab_export:
        render_export(result, st.session_state.get("file_name", "data.csv"))

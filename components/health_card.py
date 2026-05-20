"""
components/health_card.py
=========================
Renders the "Data Health Card" — a professional summary card displayed
at the top of the dashboard showing data quality metrics at a glance.

Shown after file upload, before the charts. Includes:
  - Overall health score (0–100) with colour-coded grade
  - Key stats: rows, columns, null %, duplicate count, outlier count
  - Per-column null-rate pills
  - Cleaning warnings
"""

import streamlit as st
import pandas as pd
from modules.cleaner import CleanResult


def render_health_card(result: CleanResult) -> None:
    """Render the full data health card using CleanResult."""

    score = result.health_score
    grade_class, grade_label, grade_emoji = _grade(score)

    # ── Card container ──
    st.markdown('<div class="health-card">', unsafe_allow_html=True)

    # Header row
    st.markdown(
        f"""
        <div class="health-card-header">
          <div class="health-card-title">
            🏥 Data Health Report
            <span class="badge badge-{'green' if score >= 80 else 'amber' if score >= 50 else 'red'}">
              {grade_label}
            </span>
          </div>
          <div>
            <span class="{grade_class} health-score">{score}</span>
            <span style="font-size:0.8rem; color:var(--text-muted);">/100</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 5 stat tiles ──
    df = result.df
    total_nulls = sum(m.null_count for m in result.columns.values())
    total_cells = max(df.shape[0] * df.shape[1], 1)
    total_outliers = sum(m.outlier_count for m in result.columns.values())
    null_pct = round(total_nulls / total_cells * 100, 1)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        _stat_tile(f"{result.cleaned_shape[0]:,}", "Rows")
    with c2:
        _stat_tile(str(result.cleaned_shape[1]), "Columns")
    with c3:
        _stat_tile(f"{null_pct}%", "Null Rate", warn=null_pct > 10)
    with c4:
        _stat_tile(
            str(result.duplicates_removed),
            "Duplicates",
            warn=result.duplicates_removed > 0,
        )
    with c5:
        _stat_tile(
            str(total_outliers),
            "Outliers",
            warn=total_outliers > 0,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Column health pills ──
    st.markdown(
        '<p style="font-size:0.78rem; font-weight:600; color:var(--text-secondary); '
        'text-transform:uppercase; letter-spacing:0.07em; margin-bottom:0.5rem;">'
        'Column Null Coverage</p>',
        unsafe_allow_html=True,
    )

    pills_html = ""
    for name, meta in result.columns.items():
        if meta.null_pct == 0:
            cls = "col-pill clean"
            icon = "✓"
        elif meta.null_pct < 15:
            cls = "col-pill warn"
            icon = "⚠"
        else:
            cls = "col-pill danger"
            icon = "✗"

        pills_html += (
            f'<span class="{cls}">{icon} {name} '
            f'<span style="opacity:0.65;">{meta.null_pct}%</span></span>'
        )

    st.markdown(
        f'<div style="line-height:2.2;">{pills_html}</div>',
        unsafe_allow_html=True,
    )

    # ── Warnings ──
    if result.warnings:
        st.markdown("<br>", unsafe_allow_html=True)
        for w in result.warnings:
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:0.5rem;
                            font-size:0.8rem; color:var(--amber);
                            background:var(--amber-soft);
                            border:1px solid rgba(245,158,11,0.25);
                            border-radius:6px; padding:0.5rem 0.75rem; margin-bottom:0.4rem;">
                  ⚠️ {w}
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Type breakdown ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:0.78rem; font-weight:600; color:var(--text-secondary); '
        'text-transform:uppercase; letter-spacing:0.07em; margin-bottom:0.5rem;">'
        'Column Type Breakdown</p>',
        unsafe_allow_html=True,
    )

    type_counts: dict = {}
    for meta in result.columns.values():
        type_counts[meta.semantic_type] = type_counts.get(meta.semantic_type, 0) + 1

    type_icons = {
        "numeric": ("🔢", "badge-cyan"),
        "datetime": ("📅", "badge-accent"),
        "categorical": ("🏷️", "badge-green"),
        "free_text": ("📝", "badge-amber"),
    }

    badges_html = " ".join(
        f'<span class="badge {type_icons.get(t, ("❓","badge-accent"))[1]}">'
        f'{type_icons.get(t, ("❓",""))[0]} {t} ({n})</span>'
        for t, n in sorted(type_counts.items())
    )
    st.markdown(badges_html, unsafe_allow_html=True)

    # ── Outlier detail (if any) ──
    outlier_cols = {
        name: meta
        for name, meta in result.columns.items()
        if meta.outlier_count > 0
    }
    if outlier_cols:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander(f"🔍 Outlier Details ({sum(m.outlier_count for m in outlier_cols.values())} total)"):
            for col_name, meta in outlier_cols.items():
                samples = ", ".join(str(v) for v in meta.outlier_values[:5])
                st.markdown(
                    f"""
                    <div class="anomaly-card">
                      <span class="anomaly-icon">📌</span>
                      <div class="anomaly-text">
                        <span class="anomaly-col">{col_name}</span>&nbsp;
                        has <strong>{meta.outlier_count}</strong> outlier(s).
                        Sample values: <strong>{samples}</strong>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ── Show cleaned dataframe preview ──
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("👀 Preview Cleaned Data (first 50 rows)"):
        st.dataframe(
            result.df.head(50),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ──────────────────────────────────────────────────────────────────────────────

def _grade(score: int):
    """Return (css_class, label, emoji) for a health score."""
    if score >= 85:
        return "health-score excellent", "Excellent", "🟢"
    elif score >= 65:
        return "health-score good", "Good", "🔵"
    elif score >= 45:
        return "health-score fair", "Fair", "🟡"
    else:
        return "health-score poor", "Needs Attention", "🔴"


def _stat_tile(value: str, label: str, warn: bool = False) -> None:
    """Render a single stat tile inside the health card."""
    color = "var(--amber)" if warn and value not in ("0", "0.0%", "0%") else "var(--text-primary)"
    st.markdown(
        f"""
        <div class="health-stat">
          <div class="health-stat-value" style="color:{color};">{value}</div>
          <div class="health-stat-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
)

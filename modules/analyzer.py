"""
modules/analyzer.py
===================
Phase 2 + Phase 3 — AI engine: chart selection, KPI cards, anomaly detection.

FIXES in this version:
  - get_anomaly_narratives: no longer imported from cleaner (circular import removed)
  - Anomaly cache key uses None sentinel instead of [] so empty-list bug is gone
  - get_chart_configs: robust JSON extraction with multi-line regex
"""

from __future__ import annotations

import json
import re
import os
from typing import List, Dict, Any, Optional

import numpy as np
import pandas as pd
import streamlit as st
import google.generativeai as genai
from groq import Groq

# ─────────────────────────────────────────────────────────────────────────────
# Gemini client — shared initialiser
# ─────────────────────────────────────────────────────────────────────────────

def _get_model() -> Groq:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. Add it to .env locally "
            "or to Streamlit Cloud secrets in production."
        )
    return Groq(api_key=api_key)


# ─────────────────────────────────────────────────────────────────────────────
# Chart config generation
# ─────────────────────────────────────────────────────────────────────────────

def get_chart_configs(gemini_summary: dict) -> List[Dict[str, Any]]:
    """
    Ask Gemini to decide the best charts. Returns validated list of configs.
    Each config: {chart_type, x, y, title, insight}
    """
    model = _get_model()
    summary_json = json.dumps(gemini_summary, indent=2, default=str)

    prompt = f"""You are a senior data visualisation expert and business analyst.

Given this dataset summary, decide the BEST charts to generate for a business dashboard.

Dataset summary:
{summary_json}

Return ONLY a valid JSON array — no explanation, no markdown, no code fences.
Example format:
[
  {{
    "chart_type": "bar",
    "x": "product_category",
    "y": "revenue",
    "title": "Revenue by Product Category",
    "insight": "Electronics drives 42% of total revenue, far outpacing other categories. Consider expanding inventory in this segment."
  }}
]

Rules:
- Only use column names that appear in the columns array of the summary
- Maximum 6 charts total
- insight must be exactly 2 sentences specific to the actual data values shown
- chart_type must be one of: bar, line, pie, scatter, histogram, box
- For histogram and box: set y to null
- For line charts: prefer datetime columns as x
- For scatter: pick two numeric columns with potential correlation
- If datetime columns exist: include at least one line chart
- If categorical columns exist with <=8 unique values: use bar or pie
"""

    response = model.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3,
)
raw = response.choices[0].message.content.strip()

    # Strip markdown code fences if Gemini adds them
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"\s*```$", "", raw, flags=re.MULTILINE)
    raw = raw.strip()

    configs = []
    try:
        configs = json.loads(raw)
    except json.JSONDecodeError:
        # Try to pull a JSON array out of noisy text
        match = re.search(r"\[.*?\]", raw, re.DOTALL)
        if match:
            try:
                configs = json.loads(match.group())
            except json.JSONDecodeError:
                return []
        else:
            return []

    if not isinstance(configs, list):
        return []

    # Validate each config against actual column names
    valid_cols = {c["name"] for c in gemini_summary.get("columns", [])}
    allowed_types = {"bar", "line", "pie", "scatter", "histogram", "box"}
    validated = []

    for cfg in configs:
        if not isinstance(cfg, dict):
            continue
        chart_type = str(cfg.get("chart_type", "")).lower()
        x_col = cfg.get("x")
        y_col = cfg.get("y")

        if chart_type not in allowed_types:
            continue
        if x_col not in valid_cols:
            continue
        if y_col and y_col not in valid_cols:
            cfg["y"] = None
        cfg.setdefault("title",   f"{chart_type.title()} Chart")
        cfg.setdefault("insight", "This chart shows the distribution of your data.")

        validated.append(cfg)
        if len(validated) == 6:
            break

    return validated


# ─────────────────────────────────────────────────────────────────────────────
# KPI cards
# ─────────────────────────────────────────────────────────────────────────────

def get_kpi_cards(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Generate KPI card data for numeric columns."""
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    icons = ["💰", "📦", "📈", "🎯", "🔢", "💡"]
    kpis = []

    def fmt(n: float) -> str:
        if abs(n) >= 1_000_000:
            return f"{n/1_000_000:.1f}M"
        if abs(n) >= 1_000:
            return f"{n/1_000:.1f}K"
        if n == int(n):
            return f"{int(n):,}"
        return f"{n:,.2f}"

    for i, col in enumerate(num_cols[:6]):
        s = df[col].dropna()
        if len(s) == 0:
            continue
        kpis.append({
            "label":       col.replace("_", " ").title(),
            "value":       fmt(s.sum()),
            "delta_label": f"Avg: {fmt(s.mean())}",
            "delta_type":  "neu",
            "icon":        icons[i % len(icons)],
            "detail":      f"Max: {fmt(s.max())} · Min: {fmt(s.min())}",
        })

    return kpis


# ─────────────────────────────────────────────────────────────────────────────
# Anomaly narratives  — FIXED: no circular import, no empty-list bug
# ─────────────────────────────────────────────────────────────────────────────

def get_anomaly_narratives(
    df: pd.DataFrame,
    columns_meta: dict,          # {col_name: ColumnMeta}
) -> List[Dict]:
    """
    For every column flagged with outliers, call Gemini for a 1-sentence
    business-context explanation.

    Returns list of dicts:
      {col, count, narrative, sample, mean, median, pct}
    Returns [] if no outlier columns exist.
    """
    outlier_cols = {
        name: meta
        for name, meta in columns_meta.items()
        if getattr(meta, "outlier_count", 0) > 0
    }

    if not outlier_cols:
        return []

    model = _get_model()
    results = []

    for col_name, meta in list(outlier_cols.items())[:4]:
        s = df[col_name].dropna()
        mean_val   = round(float(s.mean()),   2) if len(s) else 0
        median_val = round(float(s.median()), 2) if len(s) else 0
        sample_vals = list(meta.outlier_values[:5])
        pct = round(meta.outlier_count / max(len(df), 1) * 100, 1)

        prompt = (
            f'You are a business analyst. A dataset column "{col_name}" has '
            f"{meta.outlier_count} outlier(s) out of {len(df)} rows ({pct}%). "
            f"Column mean: {mean_val}, median: {median_val}. "
            f"Sample outlier values: {sample_vals}. "
            f"Write exactly ONE sentence (max 30 words) explaining why this "
            f"anomaly might matter in a business context. "
            f"Be specific. Do not start with 'The'."
        )

        try:
            response  = model.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.4,
)
            narrative = response.choices[0].message.content.strip().replace("\n", " ")
            # Truncate if Gemini ignores the word limit
            words = narrative.split()
            if len(words) > 40:
                narrative = " ".join(words[:40]) + "…"
        except Exception as exc:
            narrative = (
                f"{meta.outlier_count} value(s) deviate significantly "
                f"from the expected range (mean: {mean_val})."
            )

        results.append({
            "col":       col_name,
            "count":     meta.outlier_count,
            "pct":       pct,
            "mean":      mean_val,
            "median":    median_val,
            "narrative": narrative,
            "sample":    sample_vals,
        })

    return results


# ─────────────────────────────────────────────────────────────────────────────
# Chatbot — single-turn Gemini call with full conversation history
# ─────────────────────────────────────────────────────────────────────────────

def ask_gemini_about_data(
    question: str,
    gemini_summary: dict,
    history: List[Dict[str, str]],
) -> str:
    """
    Send a user question + dataset summary + conversation history to Gemini.
    Returns the assistant reply as a plain string.

    history: list of {"role": "user"|"assistant", "content": "..."}
    """
    model = _get_model()

    # Build the system context (prepended to every call)
    system_context = (
        "You are an expert data analyst assistant embedded in a BI dashboard. "
        "The user has uploaded a dataset. Answer their questions about it clearly "
        "and concisely. Use numbers and column names from the summary when relevant. "
        "If the question cannot be answered from the dataset summary, say so honestly.\n\n"
        f"Dataset summary:\n{json.dumps(gemini_summary, indent=2, default=str)}"
    )

    # Build the Gemini contents list: alternate user/model turns
    messages = [{"role": "system", "content": system_context}]
for turn in history[-10:]:
    role = "user" if turn["role"] == "user" else "assistant"
    messages.append({"role": role, "content": turn["content"]})
messages.append({"role": "user", "content": question})

response = model.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    temperature=0.4,
)
return response.choices[0].message.content.strip()

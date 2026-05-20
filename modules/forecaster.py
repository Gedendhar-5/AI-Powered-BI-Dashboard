"""
modules/forecaster.py
=====================
Phase 4 — 30-day forecast engine.

For every numeric column paired with a datetime column:
  - Fits a statsmodels OLS linear regression on the time-series
  - Generates 30 future daily data points
  - Returns the historical + forecast dataframe and regression stats
  - Calls Gemini for a plain-English narrative of the trend

Gracefully handles:
  - Datasets with no datetime column  → returns empty result with message
  - Columns with too few rows (< 10)  → skipped with warning
  - Gemini API errors                 → fallback narrative from stats only
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional

import numpy as np
import pandas as pd
import streamlit as st
import google.generativeai as genai
from groq import Groq

@dataclass
class ForecastResult:
    col_name: str                   # numeric column being forecast
    date_col: str                   # datetime column used as x-axis
    historical: pd.DataFrame        # original data  (date_col, col_name)
    forecast: pd.DataFrame          # 30-day forecast (date_col, col_name, lower, upper)
    slope: float                    # regression slope  (units / day)
    r_squared: float                # goodness-of-fit
    trend_direction: str            # "upward" | "downward" | "flat"
    narrative: str                  # Gemini-written interpretation


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


def run_forecasts(
    df: pd.DataFrame,
    date_col: str,
    numeric_cols: List[str],
    horizon_days: int = 30,
) -> List[ForecastResult]:
    """
    Run OLS linear-regression forecast for each numeric column against date_col.
    Returns a list of ForecastResult (one per column, skipping failures).
    """
    results: List[ForecastResult] = []

    # Parse datetime column if needed
    ts = pd.to_datetime(df[date_col], errors="coerce")
    valid_mask = ts.notna()
    ts = ts[valid_mask].sort_values()

    for col in numeric_cols:
        series = df.loc[valid_mask, col]
        combined = pd.DataFrame({"ds": ts.values, "y": series.values}).dropna()
        combined = combined.sort_values("ds").reset_index(drop=True)

        if len(combined) < 10:
            continue  # not enough data for a meaningful regression

        # ── OLS regression on ordinal days ────────────────────────────────────
        t0         = combined["ds"].min()
        combined["t"] = (combined["ds"] - t0).dt.days.astype(float)
        X          = np.column_stack([np.ones(len(combined)), combined["t"].values])
        y          = combined["y"].values

        # Normal equations: β = (XᵀX)⁻¹ Xᵀy
        try:
            beta     = np.linalg.lstsq(X, y, rcond=None)[0]
        except np.linalg.LinAlgError:
            continue

        intercept, slope = float(beta[0]), float(beta[1])

        # R²
        y_pred   = X @ beta
        ss_res   = float(np.sum((y - y_pred) ** 2))
        ss_tot   = float(np.sum((y - y.mean()) ** 2))
        r_sq     = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0

        # Residual std for confidence interval
        n        = len(y)
        residual_std = float(np.sqrt(ss_res / max(n - 2, 1)))

        # ── Build forecast dates ──────────────────────────────────────────────
        last_date  = combined["ds"].max()
        last_t     = float((last_date - t0).days)
        future_t   = np.arange(last_t + 1, last_t + horizon_days + 1)
        future_ds  = [last_date + pd.Timedelta(days=int(d - last_t)) for d in future_t]
        future_y   = intercept + slope * future_t
        ci         = 1.96 * residual_std   # 95 % confidence interval

        forecast_df = pd.DataFrame({
            date_col: future_ds,
            col:      future_y,
            "lower":  future_y - ci,
            "upper":  future_y + ci,
        })

        # ── Historical df ─────────────────────────────────────────────────────
        hist_df = combined[["ds", "y"]].rename(columns={"ds": date_col, "y": col})

        # ── Trend direction ───────────────────────────────────────────────────
        if abs(slope) < 0.001:
            trend = "flat"
        elif slope > 0:
            trend = "upward"
        else:
            trend = "downward"

        # ── Gemini narrative ──────────────────────────────────────────────────
        narrative = _get_narrative(col, slope, r_sq, trend, y, future_y, horizon_days)

        results.append(ForecastResult(
            col_name=col,
            date_col=date_col,
            historical=hist_df,
            forecast=forecast_df,
            slope=round(slope, 4),
            r_squared=round(r_sq, 4),
            trend_direction=trend,
            narrative=narrative,
        ))

    return results


def _get_narrative(
    col: str,
    slope: float,
    r_sq: float,
    trend: str,
    historical_y: np.ndarray,
    forecast_y: np.ndarray,
    horizon: int,
) -> str:
    """Call Gemini for a plain-English narrative of the forecast trend."""
    hist_avg  = round(float(np.mean(historical_y)), 2)
    hist_last = round(float(historical_y[-1]),      2)
    fc_end    = round(float(forecast_y[-1]),        2)
    pct_chg   = round((fc_end - hist_last) / max(abs(hist_last), 1) * 100, 1)

    prompt = (
        f'You are a business analyst interpreting a {horizon}-day forecast for column "{col}". '
        f"Historical average: {hist_avg}. Last actual value: {hist_last}. "
        f"Forecasted value in {horizon} days: {fc_end} ({pct_chg:+.1f}%). "
        f"Regression R²: {r_sq:.2f}. Trend: {trend}. "
        f"Write exactly 2 sentences in plain English summarising what this trend means "
        f"for the business. Be specific. Do not start with 'The'."
    )

    try:
        model     = _get_model()
        response  = model.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3,
)
narrative = response.choices[0].message.content.strip().replace("\n", " ")
        words     = narrative.split()
        if len(words) > 60:
            narrative = " ".join(words[:60]) + "…"
        return narrative
    except Exception:
        direction_word = {"upward": "rise", "downward": "fall", "flat": "remain stable"}[trend]
        return (
            f'Based on historical data, "{col}" is projected to {direction_word} '
            f"by approximately {abs(pct_chg):.1f}% over the next {horizon} days. "
            f"Regression R² = {r_sq:.2f} — {'reliable' if r_sq > 0.6 else 'low confidence'} fit."
        )

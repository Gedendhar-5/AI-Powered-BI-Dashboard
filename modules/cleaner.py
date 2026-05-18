"""
modules/cleaner.py
==================
Full data cleaning engine for the AI-Powered BI Dashboard.

Responsibilities:
  - Load .xlsx / .xls / .csv files from Streamlit UploadedFile objects
  - Auto-detect column semantic types: numeric, datetime, categorical, free_text
  - Clean: standardise headers, fill/drop nulls, drop full duplicates
  - Detect outliers via IQR method per numeric column
  - Return a structured CleanResult dataclass with the cleaned df + metadata
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


# ──────────────────────────────────────────────────────────────────────────────
# Data structures
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class ColumnMeta:
    """Metadata about a single column after cleaning."""
    original_name: str
    clean_name: str
    semantic_type: str          # "numeric" | "datetime" | "categorical" | "free_text"
    null_count: int
    null_pct: float
    outlier_count: int          # 0 for non-numeric columns
    outlier_values: List        # sample of outlier values (up to 5)


@dataclass
class CleanResult:
    """Everything the rest of the app needs after cleaning."""
    df: pd.DataFrame                              # cleaned dataframe
    original_shape: Tuple[int, int]               # (rows, cols) before cleaning
    cleaned_shape: Tuple[int, int]                # (rows, cols) after cleaning
    duplicates_removed: int
    columns: Dict[str, ColumnMeta]               # key = clean column name
    outlier_rows: pd.DataFrame                    # rows that contain at least one outlier
    health_score: int                             # 0–100 overall health score
    warnings: List[str]                          # human-readable warnings


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

def load_and_clean(uploaded_file) -> CleanResult:
    """
    Load an UploadedFile (csv / xlsx / xls), run the full cleaning pipeline,
    and return a CleanResult.

    Raises ValueError with a user-friendly message on unsupported formats.
    """
    df_raw = _load_file(uploaded_file)
    return _clean_pipeline(df_raw)


# ──────────────────────────────────────────────────────────────────────────────
# Step 1 — Load
# ──────────────────────────────────────────────────────────────────────────────

def _load_file(uploaded_file) -> pd.DataFrame:
    """Read the file into a DataFrame based on its extension."""
    name = uploaded_file.name.lower()

    if name.endswith(".csv"):
        # Try common encodings gracefully
        for enc in ("utf-8", "latin-1", "cp1252"):
            try:
                uploaded_file.seek(0)
                return pd.read_csv(uploaded_file, encoding=enc)
            except UnicodeDecodeError:
                continue
        raise ValueError("Could not decode the CSV file. Try saving it as UTF-8.")

    elif name.endswith((".xlsx", ".xls")):
        uploaded_file.seek(0)
        return pd.read_excel(uploaded_file, engine="openpyxl")

    else:
        ext = name.rsplit(".", 1)[-1] if "." in name else "unknown"
        raise ValueError(
            f"Unsupported file type '.{ext}'. Please upload a .csv, .xlsx, or .xls file."
        )


# ──────────────────────────────────────────────────────────────────────────────
# Step 2 — Clean pipeline
# ──────────────────────────────────────────────────────────────────────────────

def _clean_pipeline(df_raw: pd.DataFrame) -> CleanResult:
    """Run all cleaning steps and return a CleanResult."""
    warnings: List[str] = []
    original_shape = df_raw.shape

    df = df_raw.copy()

    # 1. Standardise column names
    df, col_name_map = _fix_column_names(df)

    # 2. Drop completely empty rows/columns
    df = df.dropna(how="all")
    df = df.loc[:, ~(df.isna().all())]

    # 3. Remove full duplicate rows
    n_before = len(df)
    df = df.drop_duplicates()
    duplicates_removed = n_before - len(df)
    if duplicates_removed:
        warnings.append(f"Removed {duplicates_removed} exact duplicate row(s).")

    # 4. Infer + coerce column types
    df = _coerce_types(df)

    # 5. Fill / impute nulls per column type
    df = _impute_nulls(df, warnings)

    # 6. Detect outliers (IQR) for numeric columns
    outlier_rows, col_outlier_counts, col_outlier_samples = _detect_outliers(df)

    # 7. Build ColumnMeta per column
    columns: Dict[str, ColumnMeta] = {}
    for clean_name, orig_name in col_name_map.items():
        if clean_name not in df.columns:
            continue
        sem_type = _semantic_type(df[clean_name])
        null_count = int(df[clean_name].isna().sum())
        null_pct = round(null_count / max(len(df), 1) * 100, 1)
        columns[clean_name] = ColumnMeta(
            original_name=orig_name,
            clean_name=clean_name,
            semantic_type=sem_type,
            null_count=null_count,
            null_pct=null_pct,
            outlier_count=col_outlier_counts.get(clean_name, 0),
            outlier_values=col_outlier_samples.get(clean_name, []),
        )

    # 8. Compute health score
    health_score = _compute_health_score(df, columns, duplicates_removed, original_shape)

    # 9. Warn if very few rows remain
    if len(df) < 5:
        warnings.append("Very few rows remain after cleaning — results may not be meaningful.")

    return CleanResult(
        df=df.reset_index(drop=True),
        original_shape=original_shape,
        cleaned_shape=df.shape,
        duplicates_removed=duplicates_removed,
        columns=columns,
        outlier_rows=outlier_rows,
        health_score=health_score,
        warnings=warnings,
    )


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _fix_column_names(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """
    Normalise column names to lowercase_with_underscores.
    Returns (new_df, {clean_name: original_name}).
    Handles duplicate names by appending _1, _2, etc.
    """
    seen: Dict[str, int] = {}
    mapping: Dict[str, str] = {}   # clean → original
    new_cols = []

    for orig in df.columns:
        clean = re.sub(r"[^a-z0-9]+", "_", str(orig).lower().strip()).strip("_")
        if not clean:
            clean = "col"

        # Handle duplicates
        if clean in seen:
            seen[clean] += 1
            clean = f"{clean}_{seen[clean]}"
        else:
            seen[clean] = 0

        new_cols.append(clean)
        mapping[clean] = str(orig)

    df = df.copy()
    df.columns = new_cols
    return df, mapping


def _coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Attempt smart type coercion:
      - Try numeric conversion for object columns that look numeric
      - Try datetime conversion for object columns that look like dates
      - Leave everything else as object (categorical / free_text)
    """
    df = df.copy()
    for col in df.columns:
        if df[col].dtype == object:
            # Try numeric first (faster)
            numeric_attempt = pd.to_numeric(df[col], errors="coerce")
            if numeric_attempt.notna().sum() / max(df[col].notna().sum(), 1) > 0.7:
                df[col] = numeric_attempt
                continue

            # Try datetime
            try:
                dt_attempt = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")
                if dt_attempt.notna().sum() / max(df[col].notna().sum(), 1) > 0.6:
                    df[col] = dt_attempt
                    continue
            except Exception:
                pass

    return df


def _impute_nulls(df: pd.DataFrame, warnings: List[str]) -> pd.DataFrame:
    """
    Impute missing values by column semantic type:
      - numeric   → fill with median
      - datetime  → forward fill, then backward fill
      - object    → fill with the string "Unknown"
    Only fills if null % < 40%; otherwise leaves as-is and warns.
    """
    df = df.copy()
    for col in df.columns:
        null_pct = df[col].isna().sum() / max(len(df), 1)
        if null_pct == 0:
            continue
        if null_pct > 0.40:
            warnings.append(
                f"Column '{col}' is {null_pct:.0%} null — leaving nulls as-is."
            )
            continue

        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].ffill().bfill()
        else:
            df[col] = df[col].fillna("Unknown")

    return df


def _detect_outliers(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, Dict[str, int], Dict[str, List]]:
    """
    IQR-based outlier detection on numeric columns.

    Returns:
      - outlier_rows  : subset of df where at least one outlier was found
      - col_counts    : {col_name: n_outliers}
      - col_samples   : {col_name: [up to 5 sample outlier values]}
    """
    outlier_mask = pd.Series(False, index=df.index)
    col_counts: Dict[str, int] = {}
    col_samples: Dict[str, List] = {}

    for col in df.select_dtypes(include=[np.number]).columns:
        series = df[col].dropna()
        if len(series) < 10:
            # Too few points to be meaningful
            continue
        q1, q3 = series.quantile(0.25), series.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        mask = (df[col] < lower) | (df[col] > upper)
        n = int(mask.sum())
        if n:
            outlier_mask |= mask
            col_counts[col] = n
            col_samples[col] = df.loc[mask, col].head(5).tolist()

    return df[outlier_mask].copy(), col_counts, col_samples


def _semantic_type(series: pd.Series) -> str:
    """Classify a column into one of four semantic types."""
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    # Distinguish long free-text from short categorical strings
    non_null = series.dropna().astype(str)
    if len(non_null) == 0:
        return "categorical"
    avg_len = non_null.str.len().mean()
    n_unique = non_null.nunique()
    cardinality_ratio = n_unique / max(len(non_null), 1)
    if avg_len > 50 or cardinality_ratio > 0.8:
        return "free_text"
    return "categorical"


def _compute_health_score(
    df: pd.DataFrame,
    columns: Dict[str, ColumnMeta],
    duplicates_removed: int,
    original_shape: Tuple[int, int],
) -> int:
    """
    Compute an overall data health score from 0–100.
    Penalises: high null rates, many outliers, many duplicates.
    """
    score = 100

    # Penalty: null rates
    avg_null_pct = np.mean([m.null_pct for m in columns.values()]) if columns else 0
    score -= min(30, avg_null_pct * 0.8)

    # Penalty: outliers
    total_outliers = sum(m.outlier_count for m in columns.values())
    total_rows = max(df.shape[0], 1)
    outlier_ratio = total_outliers / total_rows
    score -= min(25, outlier_ratio * 100)

    # Penalty: duplicates
    if original_shape[0] > 0:
        dup_ratio = duplicates_removed / original_shape[0]
        score -= min(20, dup_ratio * 100)

    return max(0, min(100, int(score)))


# ──────────────────────────────────────────────────────────────────────────────
# Utility: build a lightweight JSON-safe dataset summary for Gemini prompts
# ──────────────────────────────────────────────────────────────────────────────

def build_gemini_summary(result: CleanResult) -> dict:
    """
    Build a compact, token-efficient summary of the dataset to pass to Gemini.
    Never sends the full raw dataframe — only metadata + a sample.
    """
    df = result.df

    # Describe only numeric columns
    describe_dict = {}
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if num_cols:
        desc = df[num_cols].describe().round(2)
        describe_dict = desc.to_dict()

    # Column type summary
    col_info = []
    for name, meta in result.columns.items():
        col_info.append({
            "name": name,
            "type": meta.semantic_type,
            "null_pct": meta.null_pct,
            "outlier_count": meta.outlier_count,
        })

    # 5-row sample — serialise datetimes to strings
    sample_df = df.head(5).copy()
    for c in sample_df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns:
        sample_df[c] = sample_df[c].dt.strftime("%Y-%m-%d")
    sample = sample_df.to_dict(orient="records")

    return {
        "shape": {"rows": result.cleaned_shape[0], "cols": result.cleaned_shape[1]},
        "columns": col_info,
        "describe": describe_dict,
        "sample_rows": sample,
        "health_score": result.health_score,
    }
from __future__ import annotations
"""
modules/exporter.py
===================
Phase 4 — Export engine.

Provides:
  - export_charts_to_pdf()  : saves Plotly figs + KPI text to a PDF using reportlab
  - get_csv_bytes()         : returns cleaned dataframe as UTF-8 CSV bytes

Uses kaleido to convert Plotly figures to PNG, then embeds them in a reportlab PDF.
Handles missing kaleido gracefully with a text-only fallback PDF.
"""

import io
import os
import tempfile
from datetime import datetime
from typing import List, Dict, Any

import pandas as pd


def get_csv_bytes(df: pd.DataFrame) -> bytes:
    """Return the cleaned dataframe as UTF-8 encoded CSV bytes."""
    return df.to_csv(index=False).encode("utf-8")


def export_charts_to_pdf(
    df: pd.DataFrame,
    kpi_cards: List[Dict[str, Any]],
    chart_figs: List[Any],       # list of plotly Figure objects
    file_name: str = "dataset",
) -> bytes:
    """
    Build a PDF containing:
      - Cover page with title, date, and dataset summary
      - KPI summary table
      - Each Plotly chart as an embedded image
      - Footer on every page

    Returns PDF as bytes. Falls back to a text-only PDF if kaleido is missing.
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table,
        TableStyle, Image, PageBreak, HRFlowable,
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

    buffer = io.BytesIO()
    doc    = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm,  bottomMargin=2*cm,
        title=f"AI BI Dashboard — {file_name}",
    )

    # ── Styles ─────────────────────────────────────────────────────────────────
    styles   = getSampleStyleSheet()
    title_st = ParagraphStyle(
        "title_st", parent=styles["Title"],
        fontSize=22, textColor=colors.HexColor("#6366f1"),
        spaceAfter=6, alignment=TA_CENTER,
    )
    h1_st = ParagraphStyle(
        "h1_st", parent=styles["Heading1"],
        fontSize=14, textColor=colors.HexColor("#f0f0f8"),
        spaceAfter=4,
    )
    body_st = ParagraphStyle(
        "body_st", parent=styles["Normal"],
        fontSize=10, textColor=colors.HexColor("#9090a8"),
        spaceAfter=4, leading=14,
    )
    caption_st = ParagraphStyle(
        "caption_st", parent=styles["Normal"],
        fontSize=8, textColor=colors.HexColor("#55556a"),
        alignment=TA_CENTER, spaceAfter=8,
    )

    story: list = []

    # ── Cover page ─────────────────────────────────────────────────────────────
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("📊 AI-Powered BI Dashboard", title_st))
    story.append(Paragraph(f"Report: {file_name}", body_st))
    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}",
        body_st,
    ))
    story.append(HRFlowable(width="100%", thickness=1,
                             color=colors.HexColor("#6366f1")))
    story.append(Spacer(1, 0.5*cm))

    # Dataset summary stats
    story.append(Paragraph("Dataset Summary", h1_st))
    summary_data = [
        ["Metric", "Value"],
        ["Total rows",    f"{df.shape[0]:,}"],
        ["Total columns", str(df.shape[1])],
        ["Numeric cols",  str(len(df.select_dtypes(include=["number"]).columns))],
        ["Datetime cols", str(len(df.select_dtypes(include=["datetime64"]).columns))],
        ["Null cells",    str(int(df.isna().sum().sum()))],
    ]
    tbl = Table(summary_data, colWidths=[8*cm, 8*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#6366f1")),
        ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1,-1), 10),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[
            colors.HexColor("#1c1c25"), colors.HexColor("#18181f"),
        ]),
        ("TEXTCOLOR",    (0, 1), (-1,-1), colors.HexColor("#f0f0f8")),
        ("GRID",         (0, 0), (-1,-1), 0.5, colors.HexColor("#333345")),
        ("ALIGN",        (1, 0), (-1,-1), "RIGHT"),
        ("TOPPADDING",   (0, 0), (-1,-1), 6),
        ("BOTTOMPADDING",(0, 0), (-1,-1), 6),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 0.5*cm))

    # ── KPI section ────────────────────────────────────────────────────────────
    if kpi_cards:
        story.append(PageBreak())
        story.append(Paragraph("Key Performance Indicators", h1_st))
        story.append(HRFlowable(width="100%", thickness=0.5,
                                 color=colors.HexColor("#333345")))
        story.append(Spacer(1, 0.3*cm))

        kpi_table_data = [["Metric", "Total", "Average", "Details"]]
        for k in kpi_cards:
            kpi_table_data.append([
                k.get("label", ""),
                k.get("value", ""),
                k.get("delta_label", "").replace("Avg: ", ""),
                k.get("detail", ""),
            ])
        kpi_tbl = Table(kpi_table_data, colWidths=[5*cm, 3*cm, 3*cm, 6*cm])
        kpi_tbl.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#18181f")),
            ("TEXTCOLOR",    (0, 0), (-1, 0), colors.HexColor("#6366f1")),
            ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",     (0, 0), (-1,-1), 9),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[
                colors.HexColor("#1c1c25"), colors.HexColor("#18181f"),
            ]),
            ("TEXTCOLOR",    (0, 1), (-1,-1), colors.HexColor("#f0f0f8")),
            ("GRID",         (0, 0), (-1,-1), 0.5, colors.HexColor("#333345")),
            ("TOPPADDING",   (0, 0), (-1,-1), 5),
            ("BOTTOMPADDING",(0, 0), (-1,-1), 5),
        ]))
        story.append(kpi_tbl)

    # ── Chart pages ────────────────────────────────────────────────────────────
    kaleido_ok = _check_kaleido()

    for i, fig in enumerate(chart_figs):
        story.append(PageBreak())
        chart_title = fig.layout.title.text or f"Chart {i + 1}"
        story.append(Paragraph(chart_title, h1_st))
        story.append(HRFlowable(width="100%", thickness=0.5,
                                 color=colors.HexColor("#333345")))
        story.append(Spacer(1, 0.3*cm))

        if kaleido_ok:
            try:
                png_bytes = fig.to_image(format="png", width=900, height=450,
                                         scale=2, engine="kaleido")
                img_buf   = io.BytesIO(png_bytes)
                img       = Image(img_buf, width=16*cm, height=8*cm)
                story.append(img)
            except Exception:
                story.append(Paragraph(
                    "[Chart image could not be rendered — "
                    "ensure kaleido is installed correctly.]",
                    body_st,
                ))
        else:
            story.append(Paragraph(
                "[Install kaleido to embed chart images in the PDF: "
                "pip install kaleido==0.2.1]",
                body_st,
            ))

        story.append(Spacer(1, 0.4*cm))
        story.append(Paragraph(
            f"Chart {i+1} of {len(chart_figs)} · AI-Powered BI Dashboard",
            caption_st,
        ))

    # ── Build PDF ──────────────────────────────────────────────────────────────
    doc.build(story)
    return buffer.getvalue()


def _check_kaleido() -> bool:
    """Return True if kaleido is importable and functional."""
    try:
        import kaleido  # noqa: F401
        return True
    except ImportError:
        return False

<div align="center">

```
 █████╗ ██╗    ██████╗ ██╗    ██████╗  █████╗ ███████╗██╗  ██╗██████╗  ██████╗  █████╗ ██████╗ ██████╗
██╔══██╗██║    ██╔══██╗██║    ██╔══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗
███████║██║    ██████╔╝██║    ██║  ██║███████║███████╗███████║██████╔╝██║   ██║███████║██████╔╝██║  ██║
██╔══██║██║    ██╔══██╗██║    ██║  ██║██╔══██║╚════██║██╔══██║██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║
██║  ██║██║    ██████╔╝██║    ██████╔╝██║  ██║███████║██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
╚═╝  ╚═╝╚═╝    ╚═════╝ ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝
```

**Your data. Cleaned. Visualised. Understood. In seconds.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini](https://img.shields.io/badge/Gemini_1.5_Flash-Google_AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com)
[![Plotly](https://img.shields.io/badge/Plotly-5.22-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![Deploy](https://img.shields.io/badge/Deploy-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://share.streamlit.io)
[![Cost](https://img.shields.io/badge/Monthly_Cost-₹0-10b981?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-6366f1?style=for-the-badge)](LICENSE)

<br/>

> *The work of a senior data analyst — automated, AI-narrated, and delivered in a dark-mode dashboard.*
> *Upload any CSV or Excel file and walk away with cleaned data, AI-generated charts, plain-English insights, anomaly detection, 30-day forecasts, and a downloadable PDF report.*

<br/>

---

</div>

<br/>

## ◈   What Problem This Solves

Every business has spreadsheets. Almost nobody has a data analyst sitting next to them 24/7 to clean those spreadsheets, pick the right charts, explain what the numbers mean, catch the outliers that matter, and forecast what comes next.

This dashboard replaces that workflow entirely. It does the full job of a data analyst — automatically, in your browser, at zero cost — using Google Gemini AI as the intelligence layer and a production-grade Python stack underneath.

You upload a file. The AI does the rest.

<br/>

---

## ◈   Capabilities

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                     │
│   UPLOAD ANY FILE          AUTO-CLEAN              AI VISUALISE                     │
│   ─────────────────        ──────────────          ─────────────────                │
│   CSV · XLSX · XLS    →    Nulls filled       →    Gemini picks the                 │
│   Up to 200 MB             Dupes removed           best 6 chart types               │
│   Multi-encoding           Headers fixed           for your columns                 │
│   support                  Types coerced           Bar · Line · Pie                 │
│                            Outliers flagged        Scatter · Histogram              │
│                            Health scored           Box · Donut                      │
│                                                    2-sentence AI insight            │
│                                                    under every chart                │
│                                                                                     │
│   ASK ANYTHING             DETECT ANOMALIES        FORECAST TRENDS                  │
│   ─────────────────        ──────────────          ─────────────────                │
│   Plain-English Q&A   →    IQR detection      →    OLS linear regression            │
│   Multi-turn memory        Per-column stats        Up to 90-day horizon             │
│   Starter questions        Box-plot visual         95% confidence band              │
│   Follow-up support        Gemini narrates         Daily slope + R² score           │
│   No SQL needed            why it matters          Gemini trend narrative           │
│                            Business context                                         │
│                                                                                     │
│   EXPORT EVERYTHING                                                                 │
│   ─────────────────────────────────────────────────────────────────────             │
│   Download cleaned CSV  ·  Generate full PDF report  ·  Charts embedded in PDF      │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

<br/>

---

## ◈   Live Screenshots

<br/>

> **Dashboard — KPI Cards + AI Charts**

![Dashboard](<image.png>)


> **Data Health Report**

<!-- SCREENSHOT: paste health card screenshot here -->
```
[ paste screenshot of the Health tab — health score, column pills, outlier detail ]
```

<br/>

> **AI Chatbot — Ask Anything**

<!-- SCREENSHOT: paste Ask AI tab screenshot here -->
```
[ paste screenshot of a chat conversation about your data ]
```

<br/>

> **30-Day Forecast**

<!-- SCREENSHOT: paste Forecast tab screenshot here -->
```
[ paste screenshot of the forecast chart with confidence band and AI narrative ]
```

<br/>

> **Export PDF**

<!-- SCREENSHOT: paste Export tab screenshot here -->
```
[ paste screenshot of the Export tab ]
```

<br/>

---

## ◈   Full Tech Stack

| Layer | Technology | Version | Role in this project |
|---|---|---|---|
| **App framework** | [Streamlit](https://streamlit.io) | `1.35.0` | UI rendering, tab routing, session state management, sidebar, file uploader |
| **AI — language model** | [Google Gemini 1.5 Flash](https://aistudio.google.com) | `gemini-1.5-flash` | Chart type selection, insight generation, anomaly narration, chatbot Q&A, forecast narrative |
| **AI — Python SDK** | [google-generativeai](https://pypi.org/project/google-generativeai/) | `0.7.2` | Gemini API client, multi-turn conversation history, content generation |
| **Data engine** | [Pandas](https://pandas.pydata.org) | `2.2.2` | File loading, type coercion, null imputation, deduplication, aggregation |
| **Numerical computing** | [NumPy](https://numpy.org) | `1.26.4` | OLS normal equations, IQR bounds, confidence intervals, regression math |
| **Charting** | [Plotly Express](https://plotly.com/python/plotly-express/) | `5.22.0` | Bar, line, pie, scatter, histogram, box, forecast chart with CI band — all dark-themed |
| **Excel parsing** | [openpyxl](https://openpyxl.readthedocs.io) | `3.1.3` | Reading `.xlsx` and `.xls` files |
| **PDF generation** | [ReportLab](https://www.reportlab.com) | `4.2.0` | Multi-page PDF: cover, dataset summary table, KPI table, embedded chart images |
| **Chart → image** | [Kaleido](https://github.com/plotly/Kaleido) | `0.2.1` | Converts Plotly figures to PNG for PDF embedding |
| **Statistics** | [SciPy](https://scipy.org) | `1.13.0` | Statistical computation support |
| **Environment** | [python-dotenv](https://pypi.org/project/python-dotenv/) | `1.0.1` | Loads `GEMINI_API_KEY` from `.env` locally |
| **Styling** | Custom CSS (600+ lines) | — | Inter font, dark SaaS theme, CSS animations, loading skeletons, toast notifications, mobile breakpoints |
| **Hosting** | [Streamlit Community Cloud](https://share.streamlit.io) | free tier | One-click deployment from GitHub, secrets manager, free public URL |
| **Version control** | [GitHub](https://github.com) | — | Source repository and deployment trigger |

<br/>

---

## ◈   System Architecture

![System Architecture](<samples/System Architecture.png>)


## ◈   Data Flow — End to End

![Data Flow](<samples/DATA PIPELINE.png>)


## ◈   AI Decision Loop

Every AI call in this project sends only a **compact JSON summary** of your data — never the raw rows. This keeps token usage minimal, costs zero, and keeps your data private.

```
What Gemini receives:
{
  "shape": { "rows": 5000, "cols": 12 },
  "columns": [
    { "name": "revenue",    "type": "numeric",  "null_pct": 0.0, "outlier_count": 3 },
    { "name": "order_date", "type": "datetime", "null_pct": 0.2, "outlier_count": 0 }
  ],
  "describe": { "revenue": { "mean": 4200, "std": 800, "min": 120, "max": 18000 } },
  "sample_rows": [ first 5 rows only ],
  "health_score": 87
}

What Gemini returns (chart selection example):
[
  {
    "chart_type": "line",
    "x": "order_date",
    "y": "revenue",
    "title": "Revenue Trend Over Time",
    "insight": "Revenue shows a consistent upward trend with a notable spike in Q3,
                likely driven by seasonal demand. Consider aligning inventory and
                marketing spend with this pattern."
  }
]
```

**Your raw data never leaves your machine or Streamlit session.**

<br/>

---

## ◈   Privacy & Data Security

> 🔒 **Your data is never stored, logged, or shared.**
> All processing happens inside your Streamlit session in memory — when you close the tab, everything is gone.

<br/>

---

## ◈   Project Structure

```
ai-bi-dashboard/
│
├── app.py                    ← Main entry: page config, CSS, session state, tab routing
│
├── modules/                  ← Business logic — no Streamlit calls inside
│   ├── cleaner.py            ← CleanResult dataclass + full cleaning pipeline
│   ├── analyzer.py           ← All Gemini calls: charts, KPIs, anomalies, chatbot
│   ├── forecaster.py         ← OLS regression engine + ForecastResult dataclass
│   └── exporter.py           ← CSV bytes + ReportLab PDF assembler
│
├── components/               ← Pure UI renderers — all Streamlit calls live here
│   ├── sidebar.py            ← File uploader, dataset stats panel, action buttons
│   ├── health_card.py        ← Health score card, column pills, outlier expander
│   └── dashboard.py          ← KPI grid, chart grid, anomaly radar,
│                                chatbot UI, forecast renderer, export renderer
│
├── assets/
│   └── style.css             ← 600+ line dark SaaS CSS:
│                                Inter font · CSS variables · animations
│                                Loading skeletons · Toast notifications
│                                Mobile breakpoints @ 768px and 480px
│
├── requirements.txt          ← All dependencies with pinned versions
├── .env.example              ← Template: GEMINI_API_KEY=your_key_here
├── .gitignore                ← Excludes .env · venv/ · __pycache__/ · *.pdf
└── README.md                 ← This file
```

<br/>

---

## ◈   Getting Started

### Requirements

- Python **3.11** or higher
- A free Gemini API key — get one at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### Setup — Windows PowerShell

```powershell
# Clone
git clone https://github.com/YOUR_USERNAME/ai-bi-dashboard.git
cd ai-bi-dashboard

# Virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# If you get a policy error, run this once first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt

# Add your Gemini API key
Copy-Item .env.example .env
# Open .env and replace: GEMINI_API_KEY=your_actual_key_here

# Run
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

### Setup — Mac / Linux

```bash
git clone https://github.com/YOUR_USERNAME/ai-bi-dashboard.git
cd ai-bi-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env — add your key
streamlit run app.py
```

<br/>

---

## ◈   Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | Your Google Gemini API key. Free at [aistudio.google.com](https://aistudio.google.com/app/apikey) |

**Locally** — add to `.env`:
```
GEMINI_API_KEY=your_key_here
```

**On Streamlit Cloud** — add under **App Settings → Secrets**:
```toml
GEMINI_API_KEY = "your_key_here"
```

<br/>

---

## ◈   Deploy to Streamlit Cloud (Free)

```
1.  Push this repo to GitHub (make sure .env is in .gitignore — it already is)

2.  Go to → https://share.streamlit.io

3.  New app → select your repo → main file: app.py

4.  Advanced settings → Secrets → paste:
        GEMINI_API_KEY = "your_key_here"

5.  Click Deploy
    └─ Your app is live at a free public URL in ~2 minutes
```

<br/>

---

## ◈   What The AI Actually Does

This project uses Gemini 1.5 Flash as a **reasoning layer** — not just a text generator. Here is exactly what each AI call does:

| Call | When triggered | What it receives | What it returns |
|---|---|---|---|
| `get_chart_configs()` | First Dashboard load after upload | Column names, types, null %, sample rows, describe() stats | JSON array of up to 6 chart configs with type, x, y, title, 2-sentence insight |
| `get_anomaly_narratives()` | After charts load, if outliers detected | Column name, outlier count, mean, median, sample outlier values | One business-context sentence per anomaly column |
| `ask_gemini_about_data()` | Every chat message | Full conversation history (last 10 turns) + dataset summary | Plain-English answer to the user's question |
| `_get_narrative()` | After OLS forecast computed | Slope, R², trend direction, historical avg, forecasted end value | Two-sentence business interpretation of the trend |

All four calls send only **summary statistics** — never raw row data.

<br/>

---

## ◈   Troubleshooting

| Error | Fix |
|---|---|
| `(venv)` not in terminal prompt | Run `.\venv\Scripts\Activate.ps1` again |
| `ModuleNotFoundError` | Activate venv first, then re-run `pip install -r requirements.txt` |
| `GEMINI_API_KEY not found` | Check `.env` exists and has no spaces around `=` |
| `openpyxl` missing | `pip install openpyxl` inside the venv |
| `kaleido` install fails | `pip install kaleido==0.2.1 --pre` |
| Port already in use | `streamlit run app.py --server.port 8502` |
| Sidebar disappeared | Click the **›** arrow pinned at the top-left of the screen |
| PDF export blank | Ensure kaleido is installed: `pip show kaleido` |

<br/>

---

## ◈   Cost Breakdown

| Service | Cost |
|---|---|
| Streamlit Community Cloud | **Free** |
| GitHub | **Free** |
| Google Gemini API (free tier) | **Free** |
| All Python libraries | **Free / Open Source** |
| **Total monthly cost** | **₹ 0** |

<br/>

---

## ◈   Roadmap

- [ ] Multi-file merge — upload two CSVs, join on a common column, query across both
- [ ] Executive Summary Generator — one-click Gemini business report (300–400 words)
- [ ] Custom chart builder — user picks their own x/y columns
- [ ] Google Sheets import via URL
- [ ] Scheduled email reports

<br/>

---

## ◈   License

```
MIT License — Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
```

<br/>

---

<div align="center">

**Built with Python · Streamlit · Google Gemini · Plotly · ReportLab**

*If this project helped you, give it a ⭐ on GitHub*

<br/>

```
Upload. Clean. Visualise. Ask. Forecast. Export.
         The full data analyst workflow.
              Automated. Free. Yours.
```

</div>

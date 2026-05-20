
<br/>

```
█████╗ ██╗    ██████╗ ██╗    ██████╗  █████╗ ███████╗██╗  ██╗██████╗  ██████╗  █████╗ ██████╗ ██████╗
██╔══██╗██║    ██╔══██╗██║    ██╔══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗
███████║██║    ██████╔╝██║    ██║  ██║███████║███████╗███████║██████╔╝██║   ██║███████║██████╔╝██║  ██║
██╔══██║██║    ██╔══██╗██║    ██║  ██║██╔══██║╚════██║██╔══██║██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║
██║  ██║██║    ██████╔╝██║    ██████╔╝██║  ██║███████║██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
╚═╝  ╚═╝╚═╝    ╚═════╝ ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝
```

<h3>
  <samp>Upload any dataset &nbsp;→&nbsp; AI cleans it &nbsp;→&nbsp; Gemini visualises it &nbsp;→&nbsp; Ask anything in plain English</samp>
</h3>

<br/>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_1.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.22-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

![Cost](https://img.shields.io/badge/Monthly_Cost-₹_0-10b981?style=for-the-badge)
![Privacy](https://img.shields.io/badge/Your_Data-Never_Stored-6366f1?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-f59e0b?style=for-the-badge)

<br/>

> **"The work of a senior data analyst — automated, AI-narrated, and delivered in a dark-mode dashboard.
Upload any CSV or Excel file and walk away with cleaned data, AI-generated charts, plain-English insights, anomaly detection, 30-day forecasts, and a downloadable PDF report.."**

<br/>

---

</div>

<br/>

## ⚡ What Is This

**AI-Powered BI Dashboard** is a full-stack data intelligence application that replaces the first 4 hours of any data analyst's morning. Drop in a CSV or Excel file — the system automatically cleans it, detects data quality issues, picks the most meaningful charts using Gemini AI, writes plain-English business insights under each chart, flags statistical anomalies, answers any question you ask in natural language with full conversation memory, and forecasts the next 30 days of any time-series column.

No SQL. No Python knowledge required. No paid cloud services. **₹0/month.**

<br/>

---

<br/>

## 🗺️ Capabilities

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

<br/>

---

<br/>

## 🛠️ Exact Tech Stack

| # | Layer | Technology | Version | Role in This Project |
|---|-------|-----------|---------|---------------------|
| 1 | **App Framework** | [Streamlit](https://streamlit.io) | `1.35.0` | Entire UI — tabs, sidebar, session state, file upload, chat UI |
| 2 | **AI / LLM** | [Google Gemini 1.5 Flash](https://aistudio.google.com) | `gemini-1.5-flash` | Chart type selection, insight generation, anomaly narration, chatbot Q&A, forecast narrative |
| 3 | **Gemini SDK** | [google-generativeai](https://pypi.org/project/google-generativeai) | `0.7.2` | Python client that calls the Gemini REST API |
| 4 | **Data Engine** | [Pandas](https://pandas.pydata.org) | `2.2.2` | Cleaning, type coercion, null imputation, deduplication, aggregation |
| 5 | **Numerical** | [NumPy](https://numpy.org) | `1.26.4` | OLS regression (normal equations), IQR outlier bounds, confidence intervals |
| 6 | **Charting** | [Plotly Express](https://plotly.com/python/plotly-express) | `5.22.0` | All charts — bar, line, pie, scatter, histogram, box, forecast with CI band |
| 7 | **Excel I/O** | [openpyxl](https://openpyxl.readthedocs.io) | `3.1.3` | Reads `.xlsx` and `.xls` files |
| 8 | **PDF Builder** | [ReportLab](https://www.reportlab.com) | `4.2.0` | Generates multi-page PDF — cover, KPI table, embedded chart images |
| 9 | **Chart → PNG** | [Kaleido](https://github.com/plotly/Kaleido) | `0.2.1` | Rasterises Plotly figures to PNG bytes for PDF embedding |
| 10 | **Statistics** | [SciPy](https://scipy.org) | `1.13.0` | Statistical support utilities |
| 11 | **Env Config** | [python-dotenv](https://pypi.org/project/python-dotenv) | `1.0.1` | Loads `GEMINI_API_KEY` from `.env` locally |
| 12 | **Styling** | Custom CSS (`assets/style.css`) | — | 600-line dark-theme SaaS CSS — Inter font, shimmer skeletons, toast, mobile-responsive |
| 13 | **Hosting** | [Streamlit Cloud](https://share.streamlit.io) | free tier | Zero-cost deployment — CI/CD from GitHub push |
| 14 | **Source Control** | [GitHub](https://github.com) | — | Version control + deployment trigger |

<br/>

---

<br/>

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              USER'S BROWSER                                     │
│                                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────────┐   │
│   │                       STREAMLIT FRONTEND                                │   │
│   │                                                                         │   │
│   │   ┌──────────┐   ┌──────────────────────────────────────────────────┐  │   │
│   │   │          │   │                    TABS                           │  │   │
│   │   │ SIDEBAR  │   │  📊 Dashboard │ 🏥 Health │ 💬 Ask AI │ 📈 Forecast│  │   │
│   │   │          │   │  📥 Export    │           │           │           │  │   │
│   │   │ File     │   └──────────────────────────────────────────────────┘  │   │
│   │   │ Upload   │                         │                               │   │
│   │   │          │              ┌──────────▼──────────┐                    │   │
│   │   │ Dataset  │              │   components/        │                    │   │
│   │   │ Info     │              │   dashboard.py       │                    │   │
│   │   │          │              │   health_card.py     │                    │   │
│   │   │ Regen    │              │   sidebar.py         │                    │   │
│   │   │ Button   │              └──────────┬──────────┘                    │   │
│   │   └──────────┘                         │                               │   │
│   └───────────────────────────────────────┼─────────────────────────────┘   │
│                                           │                                   │
└───────────────────────────────────────────┼───────────────────────────────────┘
                                            │
                    ┌───────────────────────▼────────────────────────┐
                    │              PYTHON BACKEND                      │
                    │            (Streamlit Server)                    │
                    │                                                  │
                    │  ┌─────────────┐   ┌────────────────────────┐  │
                    │  │ cleaner.py  │   │     analyzer.py         │  │
                    │  │             │   │                         │  │
                    │  │ • Load file │   │ • get_chart_configs()   │  │
                    │  │ • Fix hdrs  │   │ • get_kpi_cards()       │  │
                    │  │ • Fill null │   │ • get_anomaly_narr()    │  │
                    │  │ • Dedup     │   │ • ask_gemini_about_data │  │
                    │  │ • IQR       │   │                         │  │
                    │  │ • Score     │───▶  ┌─────────────────┐    │  │
                    │  └─────────────┘   │  │  GEMINI API     │    │  │
                    │                    │  │  (Google Cloud) │    │  │
                    │  ┌─────────────┐   │  │                 │    │  │
                    │  │forecaster.py│   │  │ gemini-1.5-flash│    │  │
                    │  │             │   │  └────────┬────────┘    │  │
                    │  │ • OLS math  │   │           │             │  │
                    │  │ • 30-day    │   └───────────┘             │  │
                    │  │ • CI bands  │                              │  │
                    │  └─────────────┘   ┌────────────────────────┐  │
                    │                    │     exporter.py         │  │
                    │  ┌─────────────┐   │                         │  │
                    │  │ st.session  │   │ • CSV bytes             │  │
                    │  │ _state[]    │   │ • ReportLab PDF         │  │
                    │  │             │   │ • Kaleido PNG           │  │
                    │  │ In-memory   │   └────────────────────────┘  │
                    │  │ only —      │                                │
                    │  │ no database │                                │
                    │  └─────────────┘                               │
                    └────────────────────────────────────────────────┘
```

<br/>

---

<br/>

## 🔄 Data Flow

```
                              ┌─────────────────┐
                              │  User uploads   │
                              │  CSV / Excel    │
                              └────────┬────────┘
                                       │
                                       ▼
                    ┌──────────────────────────────────────┐
                    │         modules/cleaner.py            │
                    │                                       │
                    │  1 ─ Load with encoding fallback      │
                    │       utf-8 → latin-1 → cp1252        │
                    │                                       │
                    │  2 ─ Normalise headers                │
                    │       "Total Revenue " → total_revenue│
                    │                                       │
                    │  3 ─ Coerce types                     │
                    │       "123" → int  "2024-01" → date   │
                    │                                       │
                    │  4 ─ Impute nulls                     │
                    │       numeric → median                │
                    │       datetime → ffill/bfill          │
                    │       text → "Unknown"                │
                    │       (skips if null% > 40%)          │
                    │                                       │
                    │  5 ─ Drop full duplicate rows         │
                    │                                       │
                    │  6 ─ IQR outlier detection            │
                    │       flag per numeric column         │
                    │                                       │
                    │  7 ─ Compute health score 0–100       │
                    │       penalty: nulls + dupes + outlier│
                    │                                       │
                    │  8 ─ build_gemini_summary()           │
                    │       compact JSON, never raw data    │
                    │       column names + types + describe │
                    │       + 5-row sample only             │
                    └──────────────┬───────────────────────┘
                                   │
                    ┌──────────────▼───────────────────────┐
                    │     CleanResult dataclass             │
                    │     (held in st.session_state)        │
                    └──┬──────────┬────────────┬───────────┘
                       │          │            │
             ┌─────────▼──┐  ┌───▼──────┐  ┌─▼──────────┐
             │ Health Card │  │ Analyzer │  │ Forecaster │
             │             │  │          │  │            │
             │ Score, pills│  │ Gemini → │  │ OLS → 30d  │
             │ Column types│  │ charts   │  │ + Gemini   │
             │ Null % / col│  │ + KPIs   │  │ narrative  │
             │ Outlier list│  │ + anomaly│  │            │
             └─────────────┘  │ + chatbot│  └────────────┘
                               └────┬─────┘
                                    │
                             ┌──────▼──────┐
                             │   Plotly    │
                             │   Charts    │
                             │  rendered   │
                             │  in browser │
                             └─────────────┘
```

<br/>

---

<br/>

## 🔒 Data Privacy — One Line

> **Your data never leaves your session** — nothing is written to disk, no database exists, no server stores your file; it lives in `st.session_state` (Python RAM) and is destroyed the moment you close the browser tab.

<br/>

---

<br/>

## 📁 Project Structure

```
ai-bi-dashboard/
│
├── 📄 app.py                    ← Entry point — page config, CSS injection,
│                                  session state, tab routing, upload hero
│
├── 📦 modules/                  ← Pure business logic (zero Streamlit imports)
│   ├── cleaner.py               ← Full ETL pipeline → CleanResult dataclass
│   ├── analyzer.py              ← Gemini: charts · KPIs · anomalies · chatbot
│   ├── forecaster.py            ← NumPy OLS regression · ForecastResult dataclass
│   └── exporter.py              ← get_csv_bytes() · export_charts_to_pdf()
│
├── 🧩 components/               ← Streamlit UI renderers
│   ├── sidebar.py               ← File uploader · dataset info · action buttons
│   ├── health_card.py           ← Health score card · column pills · outlier list
│   └── dashboard.py             ← render_dashboard() · render_chatbot()
│                                   render_forecast() · render_export()
│
├── 🎨 assets/
│   └── style.css                ← 600-line dark SaaS CSS
│                                   Inter font · shimmer skeletons · toast
│                                   KPI cards · anomaly callouts · mobile
│
├── 📋 requirements.txt          ← All dependencies, pinned versions
├── 🔑 .env.example              ← API key template
├── 🚫 .gitignore                ← Excludes .env · venv · __pycache__
└── 📖 README.md                 ← This file
```

<br/>

---

<br/>

## 🤖 AI Analyst — What Gemini Does

This app replaces an entire junior-to-mid data analyst workflow. Here is every AI call made, in sequence:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    GEMINI 1.5 FLASH — CALL MAP                              │
├──────┬──────────────────────────┬───────────────────────────────────────────┤
│  #   │  Function                │  What Gemini is asked to do               │
├──────┼──────────────────────────┼───────────────────────────────────────────┤
│  1   │ get_chart_configs()      │ Read column names, types, 5-row sample.   │
│      │                          │ Pick the 6 best chart types. Return JSON  │
│      │                          │ array: {type, x, y, title, insight}       │
├──────┼──────────────────────────┼───────────────────────────────────────────┤
│  2   │ get_anomaly_narratives() │ For each IQR-flagged column: explain WHY  │
│      │                          │ this outlier matters in business terms.   │
│      │                          │1 sentence, column-specific, max 30 words  │
├──────┼──────────────────────────┼───────────────────────────────────────────┤
│  3   │ ask_gemini_about_data()  │ Full NL chatbot. Receives: dataset        │
│      │                          │ summary + full conversation history       │
│      │                          │ (last 10 turns). Returns plain English.   │
├──────┼──────────────────────────┼───────────────────────────────────────────┤
│  4   │ _get_narrative()         │ For each forecasted column: interpret     │
│  (forecaster.py)                │ trend direction, slope, R², % change.    │
│      │                          │ 2-sentence business interpretation.       │
└──────┴──────────────────────────┴───────────────────────────────────────────┘

Token safety: raw dataframes are NEVER sent to Gemini.
Only a compact summary (column metadata + describe() stats + 5-row sample)
is sent — keeping every call well within the free-tier context window.
```

<br/>

---

<br/>

## 📸 Screenshots

<br/>

### Upload Landing Page
> *Screenshot — drag & drop hero, feature grid, animated uploader*

```
[ PASTE SCREENSHOT HERE ]
```

---

### Dashboard — KPI Cards + AI Charts
> *Screenshot — 4 KPI metric cards + 6 Gemini-selected Plotly charts with insights*

```
[ PASTE SCREENSHOT HERE ]
```

---

### Anomaly Radar
> *Screenshot — red callout cards + mini box-plots per flagged column*

```
[ PASTE SCREENSHOT HERE ]
```

---

### Ask AI — Chatbot
> *Screenshot — chat bubbles, starter question buttons, multi-turn conversation*

```
[ PASTE SCREENSHOT HERE ]
```

---

### Forecast Tab
> *Screenshot — historical line + dashed forecast + shaded confidence band + AI narrative*

```
[ PASTE SCREENSHOT HERE ]
```

---

### Data Health Report
> *Screenshot — health score card, column null pills, outlier detail, type breakdown*

```
[ PASTE SCREENSHOT HERE ]
```

<br/>

---

<br/>

## 🚀 Local Setup — Windows PowerShell

```powershell
# Step 1 — Clone
git clone https://github.com/YOUR_USERNAME/ai-bi-dashboard.git
cd ai-bi-dashboard

# Step 2 — Virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
# If policy error: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Step 3 — Dependencies
pip install -r requirements.txt

# Step 4 — API key
Copy-Item .env.example .env
# Open .env and set: GEMINI_API_KEY=your_key_here
# Get free key → https://aistudio.google.com/app/apikey

# Step 5 — Run
streamlit run app.py
# Opens at http://localhost:8501
```

<br/>

---

<br/>

## ☁️ Deploy to Streamlit Cloud (Free)

```
1. Push repo to GitHub
2. Go to → https://share.streamlit.io
3. New app → select repo → main file: app.py
4. Advanced settings → Secrets → add:
      GEMINI_API_KEY = "your_key_here"
5. Click Deploy
   └── Live public URL in ~2 minutes
```

<br/>

---

<br/>

## 💰 Cost Breakdown

| Service | Cost |
|---------|------|
| Streamlit Cloud hosting | **Free** |
| GitHub repository | **Free** |
| Google Gemini API (free tier via Google AI Studio) | **Free** |
| All Python libraries | **Free / Open source** |
| **Total monthly cost** | **₹ 0** |

<br/>

---

<br/>

## 🔧 Troubleshooting

| Error | Fix |
|-------|-----|
| `(venv)` not showing in terminal | Run `.\venv\Scripts\Activate.ps1` |
| `ModuleNotFoundError` | Activate venv first, then `pip install -r requirements.txt` |
| `GEMINI_API_KEY not found` | Check `.env` exists with correct key, no spaces around `=` |
| `SyntaxError: from __future__` | Ensure `from __future__ import annotations` is line 1 of the file |
| `TypeError: duplicate keyword margin` | Replace `components/dashboard.py` with latest version |
| Sidebar invisible | Click the `›` arrow pinned at top-left of screen |
| Charts not generating | Click **🔄 Regenerate AI Charts** in sidebar |
| PDF export fails | Run `pip install kaleido==0.2.1 reportlab==4.2.0` |
| Port already in use | `streamlit run app.py --server.port 8502` |

<br/>

---

<br/>

## 🗓️ Build Phases

```
Week 1 — Phase 1   File upload · Auto-cleaning · Data health card
Week 2 — Phase 2   KPI cards · Gemini chart selection · Anomaly radar
Week 3 — Phase 3   NL chatbot · Conversation memory · Starter questions
Week 4 — Phase 4   30-day forecast · PDF export · Production CSS polish
```

<br/>

---

<br/>

<div align="center">

```
Built with  ♥  using Streamlit · Pandas · Plotly · Google Gemini 1.5 Flash
```

**[⭐ Star this repo](https://github.com/YOUR_USERNAME/ai-bi-dashboard)** if it saved you time.

<br/>

![Made with Python](https://img.shields.io/badge/Made_with-Python_3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![AI Powered](https://img.shields.io/badge/AI_Powered-Gemini_1.5-4285F4?style=flat-square&logo=google&logoColor=white)
![Zero Cost](https://img.shields.io/badge/Zero_Cost-₹_0_/_month-10b981?style=flat-square)

</div>


# Retail Lens — Project Structure

## Overview

Retail Lens follows a **modular, layered architecture** for maintainability, testability, and scalability.

---

## Folder Structure

```
retail-lens/
│
├── data/
│   ├── raw/
│   │   └── data.csv                     # UCI Online Retail Dataset (~45MB)
│   ├── processed/
│   │   ├── cleaned_retail.csv           # Output of ETL pipeline
│   │   ├── retail.db                    # SQLite database
│   │   ├── rfm_table.csv                # RFM scores per customer
│   │   ├── rfm_segments.csv             # RFM + customer segments
│   │   ├── cohort_retention.csv         # Cohort retention pivot table
│   │   ├── cohort_sizes.csv             # Customers per cohort
│   │   ├── cohort_revenue.csv           # Avg revenue per cohort
│   │   └── customer_churn_dataset.csv   # ML-ready churn features
│   └── exports/                         # User-downloaded CSV reports
│
├── notebooks/
│   └── 01_dataset_understanding.ipynb  # EDA and initial exploration
│
├── src/
│   ├── etl/
│   │   └── clean_data.py               # Full ETL pipeline (load → clean → engineer → save)
│   │
│   ├── analytics/
│   │   ├── database_setup.py           # Load CSV into SQLite
│   │   ├── queries.py                  # 25+ SQL query constants
│   │   └── test_queries.py             # Query validation tests
│   │
│   ├── customer_analytics/
│   │   ├── rfm.py                      # RFM calculation + quintile scoring
│   │   ├── segmentation.py             # Rule-based 6-segment classification
│   │   └── utils.py                    # Placeholder utilities
│   │
│   ├── cohort_analysis/
│   │   ├── cohort.py                   # Full cohort pipeline
│   │   └── utils.py                    # Data loaders and savers
│   │
│   ├── ml/
│   │   ├── utils.py                    # PROCESSED_DIR path + data loaders
│   │   ├── baseline/
│   │   │   ├── __init__.py
│   │   │   ├── churn_dataset.py        # Churn label creation from RFM
│   │   │   ├── churn_model.py          # Logistic Regression baseline
│   │   │   └── evaluation.py           # Reusable evaluation functions
│   │   └── experiments/
│   │       ├── __init__.py
│   │       ├── logistic_no_leakage.py  # Logistic Regression (R_Score excluded)
│   │       ├── random_forest.py        # Random Forest (n=100 estimators)
│   │       └── roc_analysis.py         # ROC-AUC curve analysis
│   │
│   ├── visualization/
│   │   └── (visualization utilities)
│   │
│   └── dashboard/
│       ├── __init__.py
│       ├── app.py                      # Streamlit entrypoint + routing
│       ├── styles.py                   # Global CSS styles
│       ├── utils.py                    # @st.cache_data data loaders
│       ├── components/
│       │   ├── __init__.py
│       │   ├── sidebar.py              # Navigation + year filter widget
│       │   ├── charts.py               # 5 reusable Plotly chart functions
│       │   └── metrics.py              # KPI card renderer
│       └── views/
│           ├── __init__.py
│           ├── overview.py             # Overview page (KPIs + charts)
│           ├── revenue.py              # Revenue Analytics page
│           ├── customers.py            # Customer Analytics page
│           ├── cohort.py               # Cohort Analysis page
│           └── churn.py                # Churn Prediction page
│
├── models/                             # Saved ML model artifacts (future)
│
├── docs/
│   ├── ARCHITECTURE.md                 # System architecture + data flow
│   ├── DATA_PIPELINE.md                # ETL + SQL + analytics pipeline
│   ├── ML_DOCUMENTATION.md             # ML models + experiments + leakage
│   ├── DASHBOARD.md                    # Dashboard pages + components
│   └── screenshots/
│       ├── overview.png
│       ├── revenue.png
│       ├── customers.png
│       ├── cohort.png
│       └── churn.png
│
├── README.md                           # Project overview + portfolio docs
├── PROJECT_STRUCTURE.md                # This file
├── requirements.txt                    # Python dependencies
├── LICENSE                             # MIT License
└── test.py                             # Basic project tests
```

---

## Module Responsibilities

### `data/`
Stores all data at different stages of the pipeline. The directory is organized into `raw/` (never modified), `processed/` (pipeline outputs), and `exports/` (user downloads).

---

### `src/etl/`

**`clean_data.py`** — Entry point for the data cleaning pipeline.

Responsibilities:
- Load raw CSV with correct encoding
- Remove duplicate rows
- Validate and filter unusable rows
- Parse datetime fields
- Create business semantic flags
- Engineer analytical features (Revenue, time components)
- Validate output quality
- Save cleaned CSV

---

### `src/analytics/`

**`database_setup.py`** — Loads cleaned CSV into SQLite.  
**`queries.py`** — SQL query constant library (25+ queries).  
**`test_queries.py`** — Basic SQL query tests.

---

### `src/customer_analytics/`

**`rfm.py`** — Computes RFM table from the database. Handles recency calculation, frequency aggregation, monetary aggregation, and quintile-based scoring.  
**`segmentation.py`** — Applies rule-based segmentation to RFM scores to classify customers into 6 behavioral segments.

---

### `src/cohort_analysis/`

**`cohort.py`** — Full cohort pipeline: assigns cohort months, calculates cohort indices, builds retention pivot tables, and exports cohort outputs.  
**`utils.py`** — Shared data loading and saving utilities for cohort module.

---

### `src/ml/`

**`baseline/churn_dataset.py`** — Creates the ML training dataset from RFM data by applying the churn definition and selecting features.  
**`baseline/churn_model.py`** — Trains and evaluates a logistic regression baseline.  
**`baseline/evaluation.py`** — Reusable evaluation functions (metrics, confusion matrix, feature importance).  
**`experiments/logistic_no_leakage.py`** — Corrected logistic regression without temporal leakage.  
**`experiments/random_forest.py`** — Random Forest alternative to logistic regression.  
**`experiments/roc_analysis.py`** — ROC-AUC analysis for model comparison.

---

### `src/dashboard/`

**`app.py`** — Streamlit entrypoint. Sets page config, applies global styles, renders sidebar, and routes to the appropriate view.  
**`styles.py`** — Global CSS customization via `st.markdown()`.  
**`utils.py`** — Cached data loaders for all data sources used by the dashboard.  
**`components/sidebar.py`** — Renders navigation radio buttons and year filter multiselect.  
**`components/charts.py`** — 5 reusable Plotly chart functions used across multiple pages.  
**`components/metrics.py`** — KPI card renderer using `st.metric()`.  
**`views/overview.py`** — Business KPI overview with revenue trend and segment distribution.  
**`views/revenue.py`** — Revenue analytics with trend line, country breakdown, and CSV export.  
**`views/customers.py`** — Customer segment explorer with filterable data table.  
**`views/cohort.py`** — Cohort retention heatmap visualization.  
**`views/churn.py`** — Churn distribution, high-risk customer table, and CSV export.

---

## Contributing Guidelines

### Setup
```bash
git clone <repository-url>
cd retail-lens
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Code Style
- Follow modular architecture — one responsibility per module
- Use descriptive function and variable names
- Avoid hardcoded paths — use `pathlib.Path(__file__).resolve()`
- Reuse shared utilities instead of duplicating logic
- Document functions with docstrings

### Branching Strategy
```
feature/new-analytics-module
feature/ml-improvements
feature/dashboard-enhancement
fix/data-leakage-correction
```

### Before Submitting
- Verify data pipeline runs end-to-end
- Confirm dashboard loads without errors
- Check that all new functions have docstrings
- Update relevant docs if architecture changes


# Retail Lens — Architecture Documentation

## System Overview

Retail Lens follows a **layered, modular pipeline architecture** where each layer has a single responsibility and feeds into the next. The design ensures clean separation between data ingestion, transformation, analytics, ML, and presentation.

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        DATA LAYER                           │
│                                                             │
│  data/raw/data.csv  ──────────────────────────────────────  │
│  (UCI Online Retail, ~500K rows, ~45MB, cp1252 encoding)    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                        ETL LAYER                            │
│                    src/etl/clean_data.py                    │
│                                                             │
│  1. load_data()           → Read CSV                        │
│  2. remove_duplicates()   → Drop exact duplicates           │
│  3. remove_invalid_rows() → Drop nulls, zero-qty rows       │
│  4. standardize_datatypes() → Parse InvoiceDate             │
│  5. create_flags()        → IsCancelled, IsReturn, etc.     │
│  6. engineer_features()   → Revenue, Year, Month, Weekday   │
│  7. validate_data()       → Assertions and summaries        │
│  8. save_data()           → Write cleaned_retail.csv        │
└─────────────────────────┬───────────────────────────────────┘
                          │ data/processed/cleaned_retail.csv
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATABASE LAYER                          │
│               src/analytics/database_setup.py               │
│                                                             │
│  CSV → pandas DataFrame → SQLite (retail.db)               │
│  Table: retail                                              │
└─────────────────────────┬───────────────────────────────────┘
                          │ data/processed/retail.db
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    ANALYTICS LAYER                          │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  src/analytics/queries.py (25+ SQL queries)          │   │
│  │  · EXPLORATION: Preview, row count, schema, countries│   │
│  │  · KPIs: Revenue, Orders, Customers, AOV, ARPC       │   │
│  │  · REVENUE: Monthly, by country, by weekday          │   │
│  │  · PRODUCT: Top by qty, revenue, frequency, price    │   │
│  │  · CUSTOMER: Top spenders, frequent buyers, geography│   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  src/customer_analytics/rfm.py                       │   │
│  │  · Load retail data from SQLite                      │   │
│  │  · Aggregate: Recency, Frequency, Monetary           │   │
│  │  · Score: R_Score, F_Score, M_Score (quintile bins)  │   │
│  │  → Output: rfm_table.csv                             │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  src/customer_analytics/segmentation.py              │   │
│  │  · Load rfm_table.csv                                │   │
│  │  · Apply rule-based segmentation logic               │   │
│  │  → Output: rfm_segments.csv                          │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  src/cohort_analysis/cohort.py                       │   │
│  │  · Assign CohortMonth (first purchase month)         │   │
│  │  · Calculate CohortIndex (months since cohort start) │   │
│  │  · Build retention pivot table                       │   │
│  │  · Calculate retention rate (%)                      │   │
│  │  → Output: cohort_retention.csv, cohort_sizes.csv,   │   │
│  │            cohort_revenue.csv                        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │ processed CSVs + retail.db
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    ML PIPELINE LAYER                        │
│                                                             │
│  src/ml/baseline/churn_dataset.py                          │
│  · Load rfm_segments.csv                                    │
│  · Create churn label: Recency > 90 days → Churn = 1       │
│  · Select features: Frequency, Monetary, R/F/M_Score       │
│  → Output: customer_churn_dataset.csv                       │
│                                                             │
│  src/ml/baseline/churn_model.py  (Baseline)                │
│  · Logistic Regression + StandardScaler                     │
│  · 80/20 train/test split                                   │
│  · Evaluate: accuracy, F1, confusion matrix                 │
│                                                             │
│  src/ml/experiments/logistic_no_leakage.py                 │
│  · Removes R_Score to eliminate temporal leakage            │
│                                                             │
│  src/ml/experiments/random_forest.py                       │
│  · RandomForestClassifier(n_estimators=100)                 │
│  · Feature importances via Gini impurity                    │
│                                                             │
│  src/ml/experiments/roc_analysis.py                        │
│  · ROC-AUC curve analysis                                   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                        │
│                  src/dashboard/app.py                       │
│                                                             │
│  Components:                                                │
│  ├── sidebar.py    → Navigation + Year filter               │
│  ├── charts.py     → 5 reusable Plotly chart functions      │
│  └── metrics.py    → KPI card renderer                      │
│                                                             │
│  Views (Pages):                                             │
│  ├── overview.py   → KPIs + revenue trend + segments        │
│  ├── revenue.py    → Revenue trend + country bar + export   │
│  ├── customers.py  → RFM pie + segment filter + table       │
│  ├── cohort.py     → Cohort retention heatmap               │
│  └── churn.py      → Churn pie + risk table + export        │
│                                                             │
│  Utilities:                                                 │
│  └── utils.py      → @st.cache_data loaders for all CSVs   │
└─────────────────────────────────────────────────────────────┘
```

---

## Design Principles

### 1. Modular Architecture
Each module has a single responsibility. ETL does not know about ML. Dashboard does not know about cohort computation. This makes modules independently testable and replaceable.

### 2. Path Management
All modules use `pathlib.Path(__file__).resolve().parent.parent.parent` to compute `BASE_DIR` dynamically. This avoids hardcoded paths and ensures the project runs correctly regardless of where it's executed from.

### 3. Caching for Dashboard Performance
The dashboard's `utils.py` wraps all data loaders with `@st.cache_data`. This means the SQLite database and CSVs are loaded only once per session, making the multi-page app fast and responsive.

### 4. Data Leakage Awareness
The ML experiments explicitly document and address data leakage. The `logistic_no_leakage.py` experiment intentionally drops `R_Score` because Recency directly encodes the churn label's temporal information (a customer inactive >90 days would have a low R_Score).

### 5. Modular SQL Query Library
All SQL queries are stored as named constants in `queries.py`, not embedded in application code. This allows queries to be tested independently (`test_queries.py`) and reused across modules.

---

## File Dependency Graph

```
data/raw/data.csv
    └── etl/clean_data.py
            └── data/processed/cleaned_retail.csv
                    └── analytics/database_setup.py
                            └── data/processed/retail.db
                                    └── customer_analytics/rfm.py
                                            └── data/processed/rfm_table.csv
                                                    └── customer_analytics/segmentation.py
                                                    │       └── data/processed/rfm_segments.csv
                                                    └── ml/baseline/churn_dataset.py
                                                            └── data/processed/customer_churn_dataset.csv
                                                                    └── ml/baseline/churn_model.py
                                                                    └── ml/experiments/*.py
                    └── cohort_analysis/cohort.py
                            └── data/processed/cohort_retention.csv
                            └── data/processed/cohort_sizes.csv
                            └── data/processed/cohort_revenue.csv

dashboard/app.py
    └── dashboard/components/sidebar.py
    └── dashboard/utils.py  (loads: retail.db, rfm_segments.csv, cohort_retention.csv, customer_churn_dataset.csv)
    └── dashboard/views/*.py
    └── dashboard/components/charts.py
    └── dashboard/components/metrics.py
```

---

## Technology Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Database | SQLite | Zero-setup, file-based, perfect for single-machine analytics projects |
| Dashboard | Streamlit | Rapid development, native Python, no frontend skills needed |
| Visualization | Plotly | Interactive charts with zoom/hover, dark theme support |
| ML | Scikit-learn | Industry-standard, clean API, multiple algorithms |
| Data format | Pandas DataFrames + CSV | Universal interoperability, easy inspection |

---

## Processed Data Files

| File | Generated By | Used By | Description |
|---|---|---|---|
| `cleaned_retail.csv` | `etl/clean_data.py` | `database_setup.py` | Cleaned transaction data |
| `retail.db` | `database_setup.py` | `rfm.py`, dashboard | SQLite database with retail table |
| `rfm_table.csv` | `customer_analytics/rfm.py` | `segmentation.py`, `churn_dataset.py` | RFM scores per customer |
| `rfm_segments.csv` | `segmentation.py` | dashboard `utils.py` | RFM scores + customer segment labels |
| `cohort_retention.csv` | `cohort_analysis/cohort.py` | dashboard `utils.py` | Retention % pivot table |
| `cohort_sizes.csv` | `cohort_analysis/cohort.py` | (analysis) | Customer count per cohort |
| `cohort_revenue.csv` | `cohort_analysis/cohort.py` | (analysis) | Average revenue per cohort |
| `customer_churn_dataset.csv` | `ml/baseline/churn_dataset.py` | dashboard `utils.py`, ML models | ML-ready feature matrix with churn labels |

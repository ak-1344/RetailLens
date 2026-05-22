
# Retail Lens — Dashboard Documentation

## Overview

The Retail Lens dashboard is a multi-page **Streamlit** web application providing interactive business intelligence across five analytical domains. It runs on Streamlit 1.57 with a dark-themed Plotly visualization layer.

---

## Running the Dashboard

```bash
# From project root with venv activated:
python -m streamlit run src/dashboard/app.py
```

Access at: `http://localhost:8501`

---

## Architecture

```
src/dashboard/
├── app.py                  # Entrypoint: page config, routing
├── styles.py               # Global CSS injection
├── utils.py                # @st.cache_data data loaders
├── components/
│   ├── sidebar.py          # Navigation + year filter
│   ├── charts.py           # 5 reusable Plotly chart functions
│   └── metrics.py          # KPI card renderer
└── views/
    ├── overview.py         # Overview page
    ├── revenue.py          # Revenue Analytics page
    ├── customers.py        # Customer Analytics page
    ├── cohort.py           # Cohort Analysis page
    └── churn.py            # Churn Prediction page
```

---

## Routing (app.py)

```python
st.set_page_config(
    page_title="Retail Lens",
    page_icon="📊",
    layout="wide"
)

page, year_filter = render_sidebar()

if page == "Overview":           render_overview_page(year_filter)
elif page == "Revenue Analytics": render_revenue_page(year_filter)
elif page == "Customer Analytics": render_customers_page(year_filter)
elif page == "Cohort Analysis":  render_cohort_page(year_filter)
elif page == "Churn Prediction": render_churn_page(year_filter)
```

---

## Pages

### 1. Overview

**File:** `src/dashboard/views/overview.py`

**Purpose:** High-level business snapshot combining KPIs, revenue trends, and customer distribution.

**Components:**
- **4 KPI Cards:** Total Revenue, Total Orders, Total Customers, Average Order Value
- **Monthly Revenue Trend** (line chart)
- **Top Countries by Revenue** (bar chart)
- **Customer Segments** (pie chart)

**Data Sources:**
- `retail.db` → retail transactions (filtered by year)
- `rfm_segments.csv` → customer segment data

**Key Metrics Displayed:**
| Metric | Value (2010–2011) |
|---|---|
| Total Revenue | $9,726,007 |
| Total Orders | 24,446 |
| Total Customers | 4,372 |
| AOV | $397.86 |

---

### 2. Revenue Analytics

**File:** `src/dashboard/views/revenue.py`

**Purpose:** Deep dive into revenue trends and geographic distribution.

**Components:**
- **Monthly Revenue Trend** (line chart, interactive)
- **Top 10 Countries by Revenue** (bar chart)
- **Revenue Dataset Preview** (paginated dataframe)
- **Download Revenue Data** (CSV export button)

**Data Sources:**
- `retail.db` → filtered retail transactions

---

### 3. Customer Analytics

**File:** `src/dashboard/views/customers.py`

**Purpose:** RFM-based customer segmentation explorer.

**Components:**
- **Segment Selector** (dropdown — filter by segment)
- **Customer Segments Pie Chart** (full distribution)
- **Segment Data Table** (20 rows, filtered by segment)
- **Segment Metrics:** Total customers in segment, Average Monetary Value

**Segment Options:**
- Champions
- Loyal Customers
- Big Spenders
- At Risk
- Lost Customers
- Regular Customers

**Data Sources:**
- `rfm_segments.csv` → RFM scores + segments

---

### 4. Cohort Analysis

**File:** `src/dashboard/views/cohort.py`

**Purpose:** Visualize customer retention over time using cohort methodology.

**Components:**
- **Cohort Retention Heatmap** (Plotly imshow, percentage labels)

Each row = a customer cohort (grouped by first purchase month)  
Each column = months since first purchase (CohortIndex)  
Cell value = % of original cohort still purchasing that month

**Data Sources:**
- `cohort_retention.csv` → pivot table of retention rates

---

### 5. Churn Prediction

**File:** `src/dashboard/views/churn.py`

**Purpose:** Identify and export at-risk customers based on the churn model.

**Components:**
- **Churn Distribution Pie Chart** (Active vs Churned)
- **High Risk Customer Table** (top 20 churned customers)
- **Estimated Churn Rate Metric** (percentage badge)
- **Download Churn Data Button** (CSV export: high_risk_customers.csv)

**Data Sources:**
- `customer_churn_dataset.csv` → customers with Churn labels

---

## Sidebar

**File:** `src/dashboard/components/sidebar.py`

```python
# Navigation
page = st.sidebar.radio("Navigation", [
    "Overview",
    "Revenue Analytics",
    "Customer Analytics",
    "Cohort Analysis",
    "Churn Prediction"
])

# Year Filter
year_filter = st.sidebar.multiselect(
    "Select Year",
    [2010, 2011],
    default=[2010, 2011]
)
```

The `year_filter` is passed to each page view and applied to filter the retail DataFrame:
```python
df = df[df["Year"].isin(year_filter)]
```

---

## Chart Components

**File:** `src/dashboard/components/charts.py`

All charts use `template="plotly_dark"` for consistent dark-mode styling.

| Function | Chart Type | Use Case |
|---|---|---|
| `plot_revenue_trend(df)` | Line chart | Monthly revenue over time |
| `plot_country_revenue(df)` | Bar chart | Top 10 countries by revenue |
| `plot_customer_segments(df)` | Pie chart | Customer segment distribution |
| `plot_cohort_heatmap(df)` | Heatmap | Cohort retention matrix |
| `plot_churn_distribution(df)` | Pie chart | Active vs Churned customers |

All charts use `st.plotly_chart(fig, width="stretch")` for full-width rendering.

---

## Data Loading & Caching

**File:** `src/dashboard/utils.py`

All loaders are decorated with `@st.cache_data` to cache data across page navigations:

```python
@st.cache_data
def load_retail_data():
    # Loads from SQLite: data/processed/retail.db
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM retail", conn)
    conn.close()
    return df

@st.cache_data
def load_rfm_data():
    # Loads: data/processed/rfm_segments.csv
    return pd.read_csv(RFM_SEGMENTS_PATH)

@st.cache_data
def load_cohort_data():
    # Loads: data/processed/cohort_retention.csv
    return pd.read_csv(COHORT_PATH, index_col=0)

@st.cache_data
def load_churn_data():
    # Loads: data/processed/customer_churn_dataset.csv
    return pd.read_csv(CHURN_PATH)
```

Caching ensures the ~45MB retail database is loaded only once per session, significantly improving multi-page navigation speed.

---

## Styling

**File:** `src/dashboard/styles.py`

Global CSS styles are injected via `st.markdown()` using `unsafe_allow_html=True`. This provides consistent visual styling across all pages beyond Streamlit's default theme.

---

## KPI Cards

**File:** `src/dashboard/components/metrics.py`

```python
def render_kpi_card(label, value):
    st.metric(label=label, value=value)
```

Used on the Overview page to display Revenue, Orders, Customers, and AOV in a 4-column layout.

---

## Dashboard Screenshots

### Overview
![Overview](screenshots/overview.png)

### Revenue Analytics
![Revenue](screenshots/revenue.png)

### Customer Analytics
![Customers](screenshots/customers.png)

### Cohort Analysis
![Cohort](screenshots/cohort.png)

### Churn Prediction
![Churn](screenshots/churn.png)

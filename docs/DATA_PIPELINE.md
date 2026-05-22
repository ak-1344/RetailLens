
# Retail Lens — Data Pipeline Documentation

## Overview

The Retail Lens data pipeline transforms raw e-commerce transaction data into analysis-ready datasets through five sequential stages.

---

## Stage 1: Raw Data

**File:** `data/raw/data.csv`  
**Source:** UCI Machine Learning Repository — Online Retail Dataset  
**Size:** ~45 MB  
**Encoding:** Windows-1252 (cp1252)

### Raw Schema

| Column | Type | Description |
|---|---|---|
| `InvoiceNo` | string | Invoice number (prefix "C" = cancellation) |
| `StockCode` | string | Product/item code |
| `Description` | string | Product name |
| `Quantity` | int | Quantity per transaction (negative = return) |
| `InvoiceDate` | string | Date and time of transaction |
| `UnitPrice` | float | Price per unit (GBP) |
| `CustomerID` | float | Unique customer identifier (nullable) |
| `Country` | string | Country of customer |

---

## Stage 2: ETL Cleaning

**Script:** `src/etl/clean_data.py`  
**Output:** `data/processed/cleaned_retail.csv`

### Pipeline Steps

#### `remove_duplicates()`
- Drops exact duplicate rows across all columns
- Tracks and logs count of removed duplicates

#### `remove_invalid_rows()`
- Drops rows where `Description`, `Quantity`, or `UnitPrice` is null
- Drops rows where `Quantity == 0` (meaningless transactions)

#### `standardize_datatypes()`
- Converts `InvoiceDate` string → `pandas.Timestamp`

#### `create_flags()`
Creates three boolean business flags:

| Flag | Logic | Purpose |
|---|---|---|
| `IsCancelled` | `InvoiceNo.startswith("C")` | Marks cancellation invoices |
| `IsReturn` | `Quantity < 0 AND NOT IsCancelled` | Marks return/refund transactions |
| `HasCustomerID` | `CustomerID IS NOT NULL` | Marks transactions with known customer |

#### `engineer_features()`
Creates analytical columns from `InvoiceDate`:

| Feature | Formula | Example |
|---|---|---|
| `Revenue` | `Quantity × UnitPrice` | 2.55 |
| `Year` | `InvoiceDate.dt.year` | 2011 |
| `Month` | `InvoiceDate.dt.month` | 11 |
| `Day` | `InvoiceDate.dt.day` | 23 |
| `Hour` | `InvoiceDate.dt.hour` | 14 |
| `Weekday` | `InvoiceDate.dt.day_name()` | "Wednesday" |

### Cleaned Schema (Additional Columns)

| Column | Type | Description |
|---|---|---|
| `Revenue` | float | Quantity × UnitPrice |
| `Year` | int | Transaction year |
| `Month` | int | Transaction month (1–12) |
| `Day` | int | Transaction day (1–31) |
| `Hour` | int | Transaction hour (0–23) |
| `Weekday` | string | Day name (Monday–Sunday) |
| `IsCancelled` | bool | True if cancellation invoice |
| `IsReturn` | bool | True if return transaction |
| `HasCustomerID` | bool | True if customer is identified |

---

## Stage 3: Database Load

**Script:** `src/analytics/database_setup.py`  
**Output:** `data/processed/retail.db`

Loads `cleaned_retail.csv` into a SQLite database as table `retail` using `pandas.DataFrame.to_sql()`.

The SQLite database enables:
- Structured SQL querying via `queries.py`
- Efficient filtering and aggregation
- Easy sharing and inspection with any SQLite client

---

## Stage 4: Customer Analytics

### RFM Computation — `src/customer_analytics/rfm.py`

**Output:** `data/processed/rfm_table.csv`

#### Snapshot Date
`snapshot_date = max(InvoiceDate) + 1 day`

This ensures recency is measured relative to the end of the dataset.

#### Aggregation
For each `CustomerID`:

| Metric | Aggregation |
|---|---|
| `Recency` | Days between snapshot_date and last purchase |
| `Frequency` | Count of distinct InvoiceNo |
| `Monetary` | Sum of Revenue |

#### Scoring (Quintile Bins)
Each metric is split into 5 equal-size bins (quintiles).

| Score | Recency | Frequency/Monetary |
|---|---|---|
| 5 | Most recent (lowest days) | Highest |
| 4 | Above average | Above average |
| 3 | Average | Average |
| 2 | Below average | Below average |
| 1 | Oldest (highest days) | Lowest |

> **Note:** `F_Score` uses `rank(method="first")` before binning to handle ties.

#### RFM Score
`RFM_Score = str(R_Score) + str(F_Score) + str(M_Score)`  
Example: `"543"` → R=5, F=4, M=3

---

### Customer Segmentation — `src/customer_analytics/segmentation.py`

**Input:** `rfm_table.csv`  
**Output:** `rfm_segments.csv`

Rule-based segmentation applied row-by-row:

```
IF R≥4 AND F≥4 AND M≥4  →  Champions
ELIF F≥4                →  Loyal Customers
ELIF M≥4                →  Big Spenders
ELIF R=1 AND F≤2 AND M≤2 →  Lost Customers
ELIF R≤2                →  At Risk
ELSE                    →  Regular Customers
```

---

## Stage 5: Cohort Analysis

**Script:** `src/cohort_analysis/cohort.py`

### Step 1: Assign Cohort Month
- `InvoiceMonth` = transaction month (period)
- `CohortMonth` = customer's *first* InvoiceMonth (earliest transaction)

### Step 2: Calculate Cohort Index
```
CohortIndex = (InvoiceYear - CohortYear) * 12 + (InvoiceMonth - CohortMonth_month) + 1
```
- Index 1 = the month the customer first purchased
- Index 2 = one month after first purchase, etc.

### Step 3: Build Retention Table
Pivot table: `CohortMonth × CohortIndex → UniqueCustomerCount`

### Step 4: Calculate Retention Rate
```
retention_rate = retention_table / cohort_sizes (first column)
```
Each cell = % of the original cohort still active in that month.

### Outputs

| File | Contents |
|---|---|
| `cohort_retention.csv` | Retention rate pivot table (%) |
| `cohort_sizes.csv` | Unique customers per cohort month |
| `cohort_revenue.csv` | Average revenue per cohort month |

---

## Stage 6: ML Churn Dataset

**Script:** `src/ml/baseline/churn_dataset.py`

### Churn Definition
```
Churn = 1  if  Recency > 90 days
Churn = 0  otherwise
```
A customer is considered churned if they haven't made a purchase in over 90 days from the snapshot date.

### Feature Selection

| Feature | Source | Type |
|---|---|---|
| `CustomerID` | RFM table | Identifier |
| `Frequency` | RFM table | Continuous |
| `Monetary` | RFM table | Continuous |
| `R_Score` | RFM table | Ordinal (1–5) |
| `F_Score` | RFM table | Ordinal (1–5) |
| `M_Score` | RFM table | Ordinal (1–5) |
| `Churn` | Derived | Binary (0/1) |

**Output:** `data/processed/customer_churn_dataset.csv`

---

## SQL Query Library

**File:** `src/analytics/queries.py`

25+ SQL queries organized by category:

### Exploration Queries
| Query | Description |
|---|---|
| `PREVIEW_DATA` | SELECT * LIMIT 5 |
| `TOTAL_ROWS` | COUNT(*) |
| `TABLE_SCHEMA` | PRAGMA table_info |
| `UNIQUE_COUNTRIES` | DISTINCT Country |

### KPI Queries
| Query | Description |
|---|---|
| `TOTAL_REVENUE` | SUM(Revenue) |
| `TOTAL_ORDERS` | COUNT(DISTINCT InvoiceNo) |
| `TOTAL_CUSTOMERS` | COUNT(DISTINCT CustomerID) WHERE NOT NULL |
| `AVERAGE_ORDER_VALUE` | SUM(Revenue) / COUNT(DISTINCT InvoiceNo) |
| `AVERAGE_REVENUE_PER_CUSTOMER` | SUM(Revenue) / COUNT(DISTINCT CustomerID) |

### Revenue Analytics
| Query | Description |
|---|---|
| `REVENUE_BY_COUNTRY` | TOP 10 countries by total revenue |
| `MONTHLY_REVENUE` | Revenue by Year and Month |
| `REVENUE_BY_WEEKDAY` | Revenue by day of week |
| `TOP_REVENUE_INVOICES` | TOP 10 invoices by revenue |

### Product Analytics
| Query | Description |
|---|---|
| `TOP_PRODUCTS_BY_QUANTITY` | TOP 10 by units sold |
| `TOP_PRODUCTS_BY_REVENUE` | TOP 10 by total revenue |
| `MOST_FREQUENTLY_PURCHASED_PRODUCTS` | TOP 10 by purchase frequency |
| `AVERAGE_PRODUCT_PRICE` | TOP 10 most expensive products |

### Customer Analytics
| Query | Description |
|---|---|
| `TOP_CUSTOMERS_BY_REVENUE` | TOP 10 highest-spending customers |
| `MOST_FREQUENT_CUSTOMERS` | TOP 10 by order count |
| `AVERAGE_CUSTOMER_SPEND` | TOP 10 by average spend |
| `CUSTOMER_COUNTRY_DISTRIBUTION` | Customer count by country |
| `TOP_COUNTRIES_BY_CUSTOMERS` | TOP 10 countries by unique customers |
| `MONTHLY_ORDER_VOLUME` | Order count by Year and Month |

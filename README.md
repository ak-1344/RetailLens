
# Retail Lens

Retail Lens is an end-to-end retail analytics and customer intelligence platform built using Python, SQL, Machine Learning, and Streamlit.

The project transforms raw retail transaction data into actionable business insights through:

- SQL analytics
- Customer segmentation
- Cohort analysis
- Churn prediction
- Interactive BI dashboards

---

# Features

## Retail Analytics

- Revenue trend analysis
- Country-wise sales analytics
- Product performance insights
- KPI reporting

---

## Customer Intelligence

- RFM Analysis
- Customer segmentation
- Behavioral analytics
- Retention analysis

---

## Cohort Analysis

- Monthly cohort tracking
- Customer retention heatmaps
- Cohort revenue analysis

---

## Machine Learning

- Churn prediction pipeline
- Logistic regression modeling
- Random forest experimentation
- ROC-AUC evaluation

---

## Interactive Dashboard

Built using Streamlit.

Includes:

- KPI cards
- Interactive charts
- Filters
- Downloadable reports
- Customer analytics dashboard

---

# Tech Stack

| Category | Tools |
|---|---|
| Programming | Python |
| Database | SQLite |
| Data Analysis | Pandas, NumPy |
| Visualization | Plotly, Matplotlib, Seaborn |
| Machine Learning | Scikit-learn |
| Dashboard | Streamlit |

---

# Dashboard Screenshots

## Overview Dashboard

![Overview](docs/screenshots/overview.png)

---

## Revenue Analytics

![Revenue](docs/screenshots/revenue.png)

---

## Cohort Analysis

![Cohort](docs/screenshots/cohort.png)

---

## Churn Prediction

![Churn](docs/screenshots/churn.png)

---

# Installation

Clone repository:

```bash
git clone <repository-url>
cd retail-lens
```

Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running Dashboard

```bash
python -m streamlit run src/dashboard/app.py
```

---

# Project Structure

```text
retail-lens/
│
├── data/
├── docs/
├── notebooks/
├── src/
│   ├── analytics/
│   ├── visualization/
│   ├── customer_analytics/
│   ├── cohort_analysis/
│   ├── ml/
│   └── dashboard/
│
├── requirements.txt
└── README.md
```

---

# Learning Outcomes

This project demonstrates:

- Data cleaning pipelines
- SQL analytics
- Business intelligence workflows
- Customer segmentation
- Cohort retention analysis
- Machine learning experimentation
- Dashboard engineering
- Modular software architecture

---

# Future Improvements

- Real-time analytics
- PostgreSQL integration
- Advanced ML models
- Cloud deployment
- Authentication system
- API integration
```

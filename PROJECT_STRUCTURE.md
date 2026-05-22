# Retail Lens — Project Structure

## Overview

Retail Lens follows a modular architecture for scalability and maintainability.

---

# Folder Structure

```text
retail-lens/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── exports/
│
├── notebooks/
│
├── src/
│   ├── analytics/
│   ├── visualization/
│   ├── customer_analytics/
│   ├── cohort_analysis/
│   ├── ml/
│   └── dashboard/
│
├── docs/
│
├── README.md
├── requirements.txt
└── PROJECT_STRUCTURE.md
```

---

# Module Responsibilities

## analytics/

Handles:

- SQL queries
- KPI calculations
- business metrics
- database interactions

---

## visualization/

Handles:

- chart generation
- visual analytics
- reusable plotting utilities

---

## customer_analytics/

Handles:

- RFM analysis
- customer segmentation
- retention recommendations

---

## cohort_analysis/

Handles:

- cohort grouping
- retention analysis
- cohort revenue analysis

---

## ml/

Handles:

- churn dataset creation
- ML experimentation
- model evaluation
- predictive analytics

---

## dashboard/

Handles:

- Streamlit application
- routing
- dashboard views
- UI components
```

---

# FILE: CONTRIBUTING.md

```md
# Contributing Guidelines

## Setup

Clone the repository:

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

# Code Style

- Follow modular architecture
- Use descriptive naming
- Keep functions focused
- Avoid hardcoded paths
- Reuse utilities where possible

---

# Branching Strategy

Use feature-based branches:

```text
feature/dashboard
feature/ml-improvements
feature/cohort-analysis
```

---

# Pull Requests

Before submitting:

- Ensure code runs successfully
- Verify dashboard functionality
- Check formatting consistency
- Update documentation if needed
```

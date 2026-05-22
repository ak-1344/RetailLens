
# Retail Lens — Machine Learning Documentation

## Overview

The ML pipeline in Retail Lens implements a **binary classification** problem: predicting whether a customer will churn based on their RFM (Recency, Frequency, Monetary) behavioral profile.

---

## Problem Statement

**Objective:** Identify customers likely to churn so the business can proactively intervene with retention campaigns.

**Churn Definition:** A customer is marked as **churned** if they have not made a purchase in over **90 days** from the observation date.

```python
df["Churn"] = (df["Recency"] > 90).astype(int)
```

This threshold is a common business heuristic for e-commerce. At 90 days, a customer is considered lapsed.

---

## Dataset

**File:** `data/processed/customer_churn_dataset.csv`

| Feature | Type | Description |
|---|---|---|
| `CustomerID` | Identifier | Customer reference |
| `Frequency` | Continuous | Number of unique invoices |
| `Monetary` | Continuous | Total revenue generated |
| `R_Score` | Ordinal (1–5) | Recency quintile score |
| `F_Score` | Ordinal (1–5) | Frequency quintile score |
| `M_Score` | Ordinal (1–5) | Monetary quintile score |
| `Churn` | Binary | 1 = churned (Recency > 90), 0 = active |

---

## Models

### Model 1: Baseline — Logistic Regression

**File:** `src/ml/baseline/churn_model.py`

#### Feature Set
```python
X = df[["Frequency", "Monetary", "R_Score", "F_Score", "M_Score"]]
y = df["Churn"]
```

#### Pipeline
```
Raw Features
    → StandardScaler (fit on train, transform both)
    → LogisticRegression()
    → Predictions
    → Accuracy, Classification Report, Confusion Matrix, Feature Importance
```

#### Configuration
```python
# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = LogisticRegression()
```

#### Outputs
- Accuracy score
- Classification report (Precision, Recall, F1 per class)
- Confusion matrix heatmap (Seaborn/Matplotlib)
- Feature coefficients (importance ranking)

---

### Model 2: Logistic Regression — No Data Leakage

**File:** `src/ml/experiments/logistic_no_leakage.py`

#### Motivation
The baseline model uses `R_Score` as a feature. However, `R_Score` is derived directly from `Recency`, and the churn label is also derived from `Recency > 90`. This creates **temporal data leakage**: the model is essentially predicting churn from the same variable used to define it.

This experiment removes `R_Score` to get a more realistic estimate of model performance.

#### Feature Set
```python
X = df[["Frequency", "Monetary", "F_Score", "M_Score"]]  # R_Score excluded
```

#### Key Difference from Baseline
- Identical pipeline (StandardScaler + LogisticRegression)
- Only difference: `R_Score` is removed from features
- This test reveals how much predictive power came from the leakage

---

### Model 3: Random Forest Classifier

**File:** `src/ml/experiments/random_forest.py`

#### Configuration
```python
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
```

#### Feature Set (Same as No-Leakage)
```python
X = df[["Frequency", "Monetary", "F_Score", "M_Score"]]
```

#### Advantages over Logistic Regression
- Handles non-linear relationships
- No need for feature scaling
- Native feature importance via Gini impurity
- More robust to outliers in `Monetary`

#### Outputs
- Accuracy, Classification Report
- Confusion matrix heatmap (green colormap)
- Feature importances (Gini-based)

---

### Analysis: ROC-AUC

**File:** `src/ml/experiments/roc_analysis.py`

Provides ROC curve and AUC score analysis for comparing model discriminative ability beyond simple accuracy.

---

## Evaluation Framework

**File:** `src/ml/baseline/evaluation.py`

Provides three reusable evaluation functions used by the baseline model:

```python
def print_classification_metrics(y_test, predictions):
    # sklearn classification_report

def plot_confusion_matrix(y_test, predictions):
    # Seaborn heatmap, Blues colormap

def print_feature_importance(model, feature_names):
    # model.coef_[0] → sorted feature coefficients
```

---

## Data Leakage Analysis

### What is Data Leakage?
Data leakage occurs when information from the future or from the label itself "leaks" into the training features, inflating model performance metrics and producing models that fail in production.

### Leakage in This Project

| Feature | Issue | Resolution |
|---|---|---|
| `R_Score` | Directly encodes Recency → encodes Churn label | Excluded in experiment |
| `Recency` | Not used as feature (only as label source) | Correctly excluded |
| `F_Score`, `M_Score` | No temporal leakage | Kept |
| `Frequency`, `Monetary` | No temporal leakage | Kept |

### Experiment Design
```
Baseline: [Frequency, Monetary, R_Score, F_Score, M_Score]
No-Leakage: [Frequency, Monetary, F_Score, M_Score]

Performance gap = Leakage contribution
```

---

## Directory Structure

```
src/ml/
├── utils.py                   # PROCESSED_DIR path + data loaders
├── baseline/
│   ├── __init__.py
│   ├── churn_dataset.py       # Churn label creation + feature selection
│   ├── churn_model.py         # Logistic Regression baseline pipeline
│   └── evaluation.py          # Shared evaluation utilities
└── experiments/
    ├── __init__.py
    ├── logistic_no_leakage.py  # Leakage-corrected logistic regression
    ├── random_forest.py        # Random Forest experiment
    └── roc_analysis.py         # ROC-AUC analysis
```

---

## Running the ML Pipeline

```bash
# From project root, with venv activated:

# 1. Build churn dataset (requires rfm_segments.csv)
python -m src.ml.baseline.churn_dataset

# 2. Train and evaluate baseline model
python -m src.ml.baseline.churn_model

# 3. Run leakage-corrected experiment
python -m src.ml.experiments.logistic_no_leakage

# 4. Run Random Forest experiment
python -m src.ml.experiments.random_forest

# 5. ROC analysis
python -m src.ml.experiments.roc_analysis
```

---

## Future ML Improvements

| Improvement | Description |
|---|---|
| Cross-validation | k-Fold CV for more reliable evaluation |
| Hyperparameter tuning | GridSearchCV / RandomizedSearchCV |
| Class imbalance | SMOTE or class_weight for imbalanced churn |
| Advanced models | XGBoost, LightGBM, Neural Networks |
| Model persistence | joblib.dump() for saving trained models |
| SHAP explanability | Feature importance via SHAP values |
| Temporal split | Train on 2010, test on 2011 for real-world validation |

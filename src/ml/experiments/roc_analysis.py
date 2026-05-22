import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression

from sklearn.preprocessing import StandardScaler

from sklearn.metrics import (
    roc_curve,
    roc_auc_score
)

import matplotlib.pyplot as plt

from src.ml.utils import (
    PROCESSED_DIR
)


# =========================
# LOAD DATA
# =========================

def load_dataset():

    path = (
        PROCESSED_DIR /
        "customer_churn_dataset.csv"
    )

    df = pd.read_csv(path)

    return df


# =========================
# PREPARE FEATURES
# =========================

def prepare_features(df):

    X = df[[
        "Frequency",
        "Monetary",
        "F_Score",
        "M_Score"
    ]]

    y = df["Churn"]

    return X, y


# =========================
# MAIN
# =========================

def main():

    print("Loading dataset...")

    df = load_dataset()


    X, y = prepare_features(df)


    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )


    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)

    X_test = scaler.transform(X_test)


    model = LogisticRegression()

    model.fit(
        X_train,
        y_train
    )


    probabilities = model.predict_proba(
        X_test
    )[:, 1]


    auc_score = roc_auc_score(
        y_test,
        probabilities
    )

    print("\nROC-AUC Score:\n")

    print(round(auc_score, 4))


    fpr, tpr, thresholds = roc_curve(
        y_test,
        probabilities
    )


    plt.figure(figsize=(8, 6))

    plt.plot(
        fpr,
        tpr,
        linewidth=2
    )

    plt.plot(
        [0, 1],
        [0, 1],
        linestyle="--"
    )

    plt.title(
        "ROC Curve",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("False Positive Rate")

    plt.ylabel("True Positive Rate")

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
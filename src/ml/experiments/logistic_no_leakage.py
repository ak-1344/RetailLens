import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression

from sklearn.preprocessing import StandardScaler

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

import matplotlib.pyplot as plt
import seaborn as sns

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

    # NO R_SCORE
    # Prevent leakage

    X = df[[
        "Frequency",
        "Monetary",
        "F_Score",
        "M_Score"
    ]]

    y = df["Churn"]

    return X, y


# =========================
# SCALE FEATURES
# =========================

def scale_features(
    X_train,
    X_test
):

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(
        X_train
    )

    X_test_scaled = scaler.transform(
        X_test
    )

    return X_train_scaled, X_test_scaled


# =========================
# TRAIN MODEL
# =========================

def train_model(
    X_train,
    y_train
):

    model = LogisticRegression()

    model.fit(
        X_train,
        y_train
    )

    return model


# =========================
# EVALUATION
# =========================

def evaluate_model(
    model,
    X_test,
    y_test,
    feature_names
):

    predictions = model.predict(X_test)


    # Accuracy
    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print("\nAccuracy:\n")

    print(round(accuracy, 4))


    # Classification Report
    print("\nClassification Report:\n")

    print(
        classification_report(
            y_test,
            predictions
        )
    )


    # Confusion Matrix
    cm = confusion_matrix(
        y_test,
        predictions
    )

    plt.figure(figsize=(6, 5))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues"
    )

    plt.title(
        "Logistic Regression (No Leakage)",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.tight_layout()

    plt.show()


    # Feature Importance
    print("\nFeature Importance:\n")

    coefficients = model.coef_[0]

    for feature, coef in zip(
        feature_names,
        coefficients
    ):

        print(
            f"{feature}: {round(coef, 4)}"
        )


# =========================
# MAIN
# =========================

def main():

    print("Loading dataset...")

    df = load_dataset()


    print("Preparing features...")

    X, y = prepare_features(df)

    feature_names = X.columns


    print("Train/Test split...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )


    print("Scaling features...")

    X_train, X_test = scale_features(
        X_train,
        X_test
    )


    print("Training model...")

    model = train_model(
        X_train,
        y_train
    )


    print("Evaluating model...")

    evaluate_model(
        model,
        X_test,
        y_test,
        feature_names
    )


if __name__ == "__main__":
    main()
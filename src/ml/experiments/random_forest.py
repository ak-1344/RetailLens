import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

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

    X = df[[
        "Frequency",
        "Monetary",
        "F_Score",
        "M_Score"
    ]]

    y = df["Churn"]

    return X, y


# =========================
# TRAIN MODEL
# =========================

def train_model(
    X_train,
    y_train
):

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    return model


# =========================
# EVALUATE MODEL
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
        cmap="Greens"
    )

    plt.title(
        "Random Forest Classifier",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.tight_layout()

    plt.show()


    # Feature Importance
    print("\nFeature Importance:\n")

    importances = model.feature_importances_

    for feature, importance in zip(
        feature_names,
        importances
    ):

        print(
            f"{feature}: {round(importance, 4)}"
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


    print("Training Random Forest...")

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
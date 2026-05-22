import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    confusion_matrix,
    classification_report
)


# =========================
# CONFUSION MATRIX
# =========================

def plot_confusion_matrix(
    y_test,
    predictions
):

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
        "Confusion Matrix",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")

    plt.tight_layout()

    plt.show()


# =========================
# CLASSIFICATION REPORT
# =========================

def print_classification_metrics(
    y_test,
    predictions
):

    report = classification_report(
        y_test,
        predictions
    )

    print("\nClassification Report:\n")

    print(report)


# =========================
# FEATURE IMPORTANCE
# =========================

def print_feature_importance(
    model,
    feature_names
):

    coefficients = model.coef_[0]

    print("\nFeature Importance:\n")

    for feature, coef in zip(
        feature_names,
        coefficients
    ):

        print(
            f"{feature}: {round(coef, 4)}"
        )
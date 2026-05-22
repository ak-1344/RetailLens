import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression

from sklearn.preprocessing import StandardScaler

from sklearn.metrics import accuracy_score


from src.ml.utils import (
    PROCESSED_DIR
)

from src.ml.baseline.evaluation import (
    plot_confusion_matrix,
    print_classification_metrics,
    print_feature_importance
)


# =========================
# LOAD DATASET
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
        "R_Score",
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

    print("\nModel Accuracy:\n")

    print(round(accuracy, 4))


    # Classification Report
    print_classification_metrics(
        y_test,
        predictions
    )


    # Confusion Matrix
    plot_confusion_matrix(
        y_test,
        predictions
    )


    # Feature Importance
    print_feature_importance(
        model,
        feature_names
    )


# =========================
# MAIN PIPELINE
# =========================

def main():

    print("Loading churn dataset...")

    df = load_dataset()


    print("Preparing features...")

    X, y = prepare_features(df)

    feature_names = X.columns


    print("Splitting train/test data...")

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


    print("Training logistic regression model...")

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
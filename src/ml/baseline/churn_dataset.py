import pandas as pd

from src.ml.utils import (
    load_rfm_data,
    save_dataframe
)


# =========================
# CREATE CHURN LABEL
# =========================

def create_churn_label(df):

    # Churn Definition:
    # Customer inactive for >90 days

    df["Churn"] = (
        df["Recency"] > 90
    ).astype(int)

    return df


# =========================
# SELECT ML FEATURES
# =========================

def select_features(df):

    ml_df = df[[

        "CustomerID",

        "Frequency",
        "Monetary",

        "R_Score",
        "F_Score",
        "M_Score",

        "Churn"
    ]]


    # Convert scores to integers
    score_columns = [
        "R_Score",
        "F_Score",
        "M_Score"
    ]

    for col in score_columns:

        ml_df[col] = ml_df[col].astype(int)

    return ml_df


# =========================
# DATASET SUMMARY
# =========================

def print_dataset_summary(df):

    print("\nDataset Shape:\n")

    print(df.shape)


    print("\nDataset Preview:\n")

    print(df.head())


    print("\nChurn Distribution:\n")

    print(
        df["Churn"]
        .value_counts(normalize=True)
    )


# =========================
# MAIN PIPELINE
# =========================

def main():

    print("Loading RFM data...")

    df = load_rfm_data()


    print("Creating churn labels...")

    df = create_churn_label(df)


    print("Selecting ML features...")

    ml_df = select_features(df)


    print_dataset_summary(ml_df)


    save_dataframe(
        ml_df,
        "customer_churn_dataset.csv"
    )


if __name__ == "__main__":
    main()
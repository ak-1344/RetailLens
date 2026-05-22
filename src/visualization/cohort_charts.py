from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

COHORT_PATH = (
    BASE_DIR /
    "data" /
    "processed" /
    "cohort_retention.csv"
)


# =========================
# LOAD DATA
# =========================

def load_cohort_data():

    df = pd.read_csv(
        COHORT_PATH,
        index_col=0
    )

    return df


# =========================
# PLOT HEATMAP
# =========================

def plot_retention_heatmap(df):

    plt.figure(figsize=(14, 8))

    sns.heatmap(
        df,
        annot=True,
        fmt=".0%",
        cmap="Blues",
        linewidths=0.5
    )

    plt.title(
        "Customer Retention Cohort Analysis",
        fontsize=18,
        fontweight="bold"
    )

    plt.xlabel(
        "Cohort Index (Months Since Acquisition)",
        fontsize=12
    )

    plt.ylabel(
        "Cohort Month",
        fontsize=12
    )

    plt.tight_layout()

    plt.show()


# =========================
# MAIN
# =========================

def main():

    print("Loading cohort retention data...")

    df = load_cohort_data()


    print("Generating heatmap...")

    plot_retention_heatmap(df)


if __name__ == "__main__":
    main()
from pathlib import Path
import pandas as pd

from src.visualization.chart_utils import (
    create_bar_chart
)


# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SEGMENT_PATH = (
    BASE_DIR /
    "data" /
    "processed" /
    "rfm_segments.csv"
)


# =========================
# LOAD DATA
# =========================

def load_segment_data():

    df = pd.read_csv(SEGMENT_PATH)

    return df


# =========================
# SEGMENT DISTRIBUTION
# =========================

def plot_segment_distribution():

    df = load_segment_data()

    segment_counts = (
        df["CustomerSegment"]
        .value_counts()
        .reset_index()
    )

    segment_counts.columns = [
        "CustomerSegment",
        "CustomerCount"
    ]


    create_bar_chart(
        df=segment_counts,
        x_column="CustomerSegment",
        y_column="CustomerCount",
        title="Customer Segment Distribution",
        x_label="Segment",
        y_label="Customers",
        figure_size=(12, 6)
    )


# =========================
# SEGMENT REVENUE
# =========================

def plot_segment_revenue():

    df = load_segment_data()

    revenue_df = (
        df.groupby("CustomerSegment")["Monetary"]
        .sum()
        .reset_index()
    )

    revenue_df.columns = [
        "CustomerSegment",
        "TotalRevenue"
    ]


    create_bar_chart(
        df=revenue_df,
        x_column="CustomerSegment",
        y_column="TotalRevenue",
        title="Revenue Contribution By Segment",
        x_label="Segment",
        y_label="Revenue",
        figure_size=(12, 6)
    )


# =========================
# SEGMENT FREQUENCY
# =========================

def plot_segment_frequency():

    df = load_segment_data()

    frequency_df = (
        df.groupby("CustomerSegment")["Frequency"]
        .mean()
        .reset_index()
    )

    frequency_df.columns = [
        "CustomerSegment",
        "AverageFrequency"
    ]


    create_bar_chart(
        df=frequency_df,
        x_column="CustomerSegment",
        y_column="AverageFrequency",
        title="Average Purchase Frequency By Segment",
        x_label="Segment",
        y_label="Average Frequency",
        figure_size=(12, 6)
    )


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    plot_segment_distribution()

    plot_segment_revenue()

    plot_segment_frequency()
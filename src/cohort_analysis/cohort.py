import pandas as pd

from src.cohort_analysis.utils import (
    load_retail_data,
    save_dataframe
)


# =========================
# DATA PREPARATION
# =========================

def prepare_data(df):

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"]
    )

    return df


# =========================
# ASSIGN COHORT MONTH
# =========================

def assign_cohort_month(df):

    # Transaction month
    df["InvoiceMonth"] = (
        df["InvoiceDate"]
        .dt.to_period("M")
    )

    # First purchase month
    cohort_month = (
        df.groupby("CustomerID")["InvoiceMonth"]
        .min()
    )

    df["CohortMonth"] = df["CustomerID"].map(
        cohort_month
    )

    return df


# =========================
# CALCULATE COHORT INDEX
# =========================

def calculate_cohort_index(df):

    invoice_year = (
        df["InvoiceMonth"]
        .dt.year
    )

    invoice_month = (
        df["InvoiceMonth"]
        .dt.month
    )

    cohort_year = (
        df["CohortMonth"]
        .dt.year
    )

    cohort_month = (
        df["CohortMonth"]
        .dt.month
    )

    year_diff = invoice_year - cohort_year

    month_diff = invoice_month - cohort_month

    df["CohortIndex"] = (
        year_diff * 12
        + month_diff
        + 1
    )

    return df


# =========================
# BUILD RETENTION TABLE
# =========================

def build_retention_table(df):

    cohort_data = (
        df.groupby(
            ["CohortMonth", "CohortIndex"]
        )["CustomerID"]
        .nunique()
        .reset_index()
    )

    retention_table = cohort_data.pivot_table(
        index="CohortMonth",
        columns="CohortIndex",
        values="CustomerID"
    )

    return retention_table


# =========================
# CALCULATE RETENTION RATE
# =========================

def calculate_retention_rate(retention_table):

    cohort_sizes = retention_table.iloc[:, 0]

    retention_rate = retention_table.divide(
        cohort_sizes,
        axis=0
    )

    retention_rate = retention_rate.round(3)

    return retention_rate



# =========================
# BUILD COHORT SIZE TABLE
# =========================

def build_cohort_size_table(df):

    cohort_sizes = (
        df.groupby("CohortMonth")["CustomerID"]
        .nunique()
        .reset_index()
    )

    cohort_sizes.columns = [
        "CohortMonth",
        "TotalCustomers"
    ]

    return cohort_sizes


# =========================
# BUILD COHORT REVENUE TABLE
# =========================

def build_cohort_revenue_table(df):

    cohort_revenue = (
        df.groupby("CohortMonth")["Revenue"]
        .mean()
        .reset_index()
    )

    cohort_revenue.columns = [
        "CohortMonth",
        "AverageRevenue"
    ]

    return cohort_revenue



# =========================
# MAIN PIPELINE
# =========================

def main():

    print("Loading retail data...")
    df = load_retail_data()

    print("Preparing data...")
    df = prepare_data(df)

    print("Assigning cohort months...")
    df = assign_cohort_month(df)

    print("Calculating cohort index...")
    df = calculate_cohort_index(df)
    
    
    print("Building cohort size table...")
    cohort_sizes = build_cohort_size_table(df)

    print("\nCohort Sizes:\n")
    print(cohort_sizes.head())
    print("\nBuilding cohort revenue table...")
    cohort_revenue = build_cohort_revenue_table(df)

    print("\nCohort Revenue:\n")
    print(cohort_revenue.head())

    print("Building retention table...")
    retention_table = build_retention_table(df)

    print("Calculating retention rates...")
    retention_rate = calculate_retention_rate(
        retention_table
    )

    print("\nRetention Rate Preview:\n")
    print(retention_rate.head())


    save_dataframe(
        retention_rate,
        "cohort_retention.csv"
    )
    save_dataframe(
        cohort_sizes,
        "cohort_sizes.csv"
    )
    save_dataframe(
        cohort_revenue,
        "cohort_revenue.csv"
    )


if __name__ == "__main__":
    main()
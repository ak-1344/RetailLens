import pandas as pd

RAW_DATA_PATH = "../../data/raw/data.csv"
OUTPUT_PATH = "../../data/processed/cleaned_retail.csv"


def load_data(path):
    """
    Load raw retail dataset.
    """
    df = pd.read_csv(path, encoding="cp1252")
    print(f"\nLoaded dataset with {len(df)} rows")
    return df


def remove_duplicates(df):
    """
    Remove exact duplicate rows.
    """
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    print(f"Removed {before - after} duplicate rows")
    return df


def remove_invalid_rows(df):
    """
    Remove analytically unusable rows.
    """

    before = len(df)

    # Rows missing critical fields
    missing_critical = df[
        df[["Description", "Quantity", "UnitPrice"]]
        .isnull()
        .any(axis=1)
    ]

    print(f"Rows missing critical fields: {len(missing_critical)}")
    df = df.dropna(
        subset=["Description", "Quantity", "UnitPrice"]
    )

    # Zero quantity rows
    zero_quantity = df[df["Quantity"] == 0]
    print(f"Zero quantity rows removed: {len(zero_quantity)}")
    df = df[df["Quantity"] != 0]
    
    after = len(df)
    
    print(f"Removed total {before - after} invalid rows")
    return df


def standardize_datatypes(df):
    """
    Standardize dataset datatypes.
    """

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"]
    )

    return df


def create_flags(df):
    """
    Create business semantic flags.
    """

    # Cancellation invoices
    df["IsCancelled"] = (
        df["InvoiceNo"]
        .astype(str)
        .str.startswith("C")
    )

    # Returns/refunds
    df["IsReturn"] = (df["Quantity"] < 0) & (~df["IsCancelled"])

    # Customer tracking availability
    df["HasCustomerID"] = (
        df["CustomerID"].notna()
    )

    return df


# def classify_transactions(df):
#     """
#     Classify transaction categories.
#     """
#     df["TransactionType"] = "NORMAL"

#     # Discount transactions
#     df.loc[
#         df["Description"].str.contains(
#             "Discount",
#             case=False,
#             na=False
#         )| df["StockCode"].str.contains(
#             "D",
#             case=False,
#             na=False
#         ),
#         "TransactionType"
#     ] = "DISCOUNT"

#     # Manual entries
#     df.loc[
#         df["Description"].str.contains(
#             "Manual",
#             case=False,
#             na=False
#         ) | df["StockCode"].str.contains(
#             "M",
#             case=False,
#             na=False
#         ),
#         "TransactionType"
#     ] = "MANUAL"

#     # Cancellation transactions
#     df.loc[
#         df["IsCancelled"],
#         "TransactionType"
#     ] = "CANCELLATION"

#     # Return/refund transactions
#     df.loc[
#         df["IsReturn"],
#         "TransactionType"
#     ] = "RETURN"

#     df.loc[
#         df["UnitPrice"] < 0,
#         "TransactionType"
#     ] = "Debt Adjustment"
    
#     return df


def engineer_features(df):
    """
    Create analytical features.
    """

    # Revenue feature
    df["Revenue"] = (
        df["Quantity"] * df["UnitPrice"]
    )

    # Time-based features
    df["Year"] = (
        df["InvoiceDate"].dt.year
    )

    df["Month"] = (
        df["InvoiceDate"].dt.month
    )

    df["Day"] = (
        df["InvoiceDate"].dt.day
    )

    df["Hour"] = (
        df["InvoiceDate"].dt.hour
    )

    df["Weekday"] = (
        df["InvoiceDate"].dt.day_name()
    )

    return df


def validate_data(df):
    """
    Validate cleaned dataset.
    """
    print("\n========== VALIDATION ==========")

    print("\nDataset Shape:")
    print(df.shape)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nData Types:")
    print(df.dtypes)

    print("\nRevenue Summary:")
    print(df["Revenue"].describe())

    # print("\nTransaction Type Distribution:")
    # print(df["TransactionType"].value_counts())

    print("\nCancellation Count:")
    print(df["IsCancelled"].sum())

    print("\nReturn Count:")
    print(df["IsReturn"].sum())


def save_data(df, path):
    """
    Save cleaned dataset.
    """
    df.to_csv(path, index=False)
    print(f"\nCleaned dataset saved to:\n{path}")


def main():
    print("\n========== STARTING ETL ==========")
    df = load_data(RAW_DATA_PATH)
    df = remove_duplicates(df)
    df = remove_invalid_rows(df)
    df = standardize_datatypes(df)
    df = create_flags(df)
    # df = classify_transactions(df)
    df = engineer_features(df)
    validate_data(df)
    save_data(df, OUTPUT_PATH)
    print("\n========== ETL COMPLETED ==========")
    print("\nSample Data:")
    print(df.head())


if __name__ == "__main__":
    main()
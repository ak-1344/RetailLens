from pathlib import Path
import sqlite3
import pandas as pd


# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DB_PATH = BASE_DIR / "data" / "processed" / "retail.db"

OUTPUT_PATH = BASE_DIR / "data" / "processed" / "rfm_table.csv"


# =========================
# LOAD DATA
# =========================

def load_retail_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM retail
    WHERE CustomerID IS NOT NULL
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# =========================
# CREATE RFM TABLE
# =========================

def create_rfm_table(df):

    # Ensure datetime conversion
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])


    # Snapshot date
    snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)


    # Customer aggregation
    rfm = df.groupby("CustomerID").agg({

        "InvoiceDate": lambda x: (
            snapshot_date - x.max()
        ).days,

        "InvoiceNo": "nunique",

        "Revenue": "sum"

    })


    # Rename columns
    rfm.columns = [
        "Recency",
        "Frequency",
        "Monetary"
    ]

    # =========================
    # RFM SCORING
    # =========================

    # Recency Score
    rfm["R_Score"] = pd.qcut(
        rfm["Recency"],
        5,
        labels=[5, 4, 3, 2, 1]
    )

    # Frequency Score
    rfm["F_Score"] = pd.qcut(
        rfm["Frequency"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5]
    )

    # Monetary Score
    rfm["M_Score"] = pd.qcut(
        rfm["Monetary"],
        5,
        labels=[1, 2, 3, 4, 5]
    )

    rfm["RFM_Score"] = (
        rfm["R_Score"].astype(str) +
        rfm["F_Score"].astype(str) +
        rfm["M_Score"].astype(str)
    )

    # Reset index
    rfm = rfm.reset_index()

    return rfm


# =========================
# SAVE DATA
# =========================

def save_rfm_table(rfm):

    rfm.to_csv(OUTPUT_PATH, index=False)
    print(f"RFM table saved to:\n{OUTPUT_PATH}")


# =========================
# MAIN
# =========================

def main():
    print("Loading retail data...")
    df = load_retail_data()

    print("Creating RFM table...")
    rfm = create_rfm_table(df)

    print("\nRFM Table Preview:\n")
    print(rfm.head())

    print("\nRFM Summary:\n")
    print(rfm.describe())

    save_rfm_table(rfm)


if __name__ == "__main__":
    main()
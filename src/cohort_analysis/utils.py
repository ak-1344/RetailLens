from pathlib import Path
import sqlite3
import pandas as pd


# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DB_PATH = BASE_DIR / "data" / "processed" / "retail.db"

OUTPUT_DIR = BASE_DIR / "data" / "processed"


# =========================
# LOAD RETAIL DATA
# =========================

def load_retail_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        CustomerID,
        InvoiceNo,
        InvoiceDate,
        Revenue
    FROM retail
    WHERE CustomerID IS NOT NULL
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# =========================
# SAVE DATAFRAME
# =========================

def save_dataframe(df, filename):

    output_path = OUTPUT_DIR / filename

    df.to_csv(output_path)

    print(f"\nSaved:\n{output_path}")
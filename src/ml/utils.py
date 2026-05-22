from pathlib import Path
import pandas as pd


# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROCESSED_DIR = (
    BASE_DIR /
    "data" /
    "processed"
)


# =========================
# LOAD RFM DATA
# =========================

def load_rfm_data():

    path = (
        PROCESSED_DIR /
        "rfm_table.csv"
    )

    df = pd.read_csv(path)

    return df


# =========================
# SAVE DATAFRAME
# =========================

def save_dataframe(df, filename):

    output_path = (
        PROCESSED_DIR /
        filename
    )

    df.to_csv(output_path, index=False)

    print(f"\nSaved:\n{output_path}")
from pathlib import Path
import pandas as pd


# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

RFM_PATH = BASE_DIR / "data" / "processed" / "rfm_table.csv"

OUTPUT_PATH = BASE_DIR / "data" / "processed" / "rfm_segments.csv"


# =========================
# LOAD RFM DATA
# =========================

def load_rfm_data():

    df = pd.read_csv(RFM_PATH)

    return df


# =========================
# CUSTOMER SEGMENTATION
# =========================

def assign_customer_segment(row):

    r = int(row["R_Score"])
    f = int(row["F_Score"])
    m = int(row["M_Score"])

    # Champions
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"

    # Loyal Customers
    elif f >= 4:
        return "Loyal Customers"

    # Big Spenders
    elif m >= 4:
        return "Big Spenders"

    # Lost Customers
    elif r == 1 and f <= 2 and m <= 2:
        return "Lost Customers"

    # At Risk
    elif r <= 2:
        return "At Risk"
    

    # Others
    else:
        return "Regular Customers"


# =========================
# APPLY SEGMENTATION
# =========================

def segment_customers(df):
    df["CustomerSegment"] = df.apply(
        assign_customer_segment,
        axis=1
    )
    return df


# =========================
# SAVE DATA
# =========================

def save_segmented_data(df):
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSegmented data saved to:\n{OUTPUT_PATH}")


# =========================
# MAIN
# =========================

def main():
    print("Loading RFM data...")
    df = load_rfm_data()


    print("Assigning customer segments...")
    segmented_df = segment_customers(df)


    print("\nSegment Distribution:\n")
    print(
        segmented_df["CustomerSegment"]
        .value_counts()
    )


    print("\nPreview:\n")
    print(
        segmented_df[
            [
                "CustomerID",
                "RFM_Score",
                "CustomerSegment"
            ]
        ].head()
    )
    save_segmented_data(segmented_df)


if __name__ == "__main__":
    main()
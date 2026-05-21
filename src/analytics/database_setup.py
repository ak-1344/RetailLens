import sqlite3
import pandas as pd


# Paths
CSV_PATH = "../../data/processed/cleaned_retail.csv"
DB_PATH = "../../data/processed/retail.db"


def load_cleaned_data():
    df = pd.read_csv(CSV_PATH)
    return df


def create_database_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def load_dataframe_to_sql(df, conn):
    df.to_sql(
        name="retail",
        con=conn,
        if_exists="replace",
        index=False
    )


def main():
    print("Loading cleaned dataset...")

    df = load_cleaned_data()

    print("Creating SQLite connection...")

    conn = create_database_connection()

    print("Loading data into SQL table...")

    load_dataframe_to_sql(df, conn)

    print("Database created successfully.")

    conn.close()


if __name__ == "__main__":
    main()
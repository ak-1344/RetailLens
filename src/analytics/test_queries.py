import sqlite3
import pandas as pd
from queries import TOTAL_ROWS
DB_PATH = "../../data/processed/retail.db"

def run_query(query):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df


def main():
    result = run_query(TOTAL_ROWS)
    print(result)


if __name__ == "__main__":
    main()
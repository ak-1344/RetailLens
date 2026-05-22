from pathlib import Path

import pandas as pd

import sqlite3

import streamlit as st


# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DB_PATH = (
    BASE_DIR /
    "data" /
    "processed" /
    "retail.db"
)

PROCESSED_DIR = (
    BASE_DIR /
    "data" /
    "processed"
)


# =========================
# LOAD SQL TABLE
# =========================

@st.cache_data
def load_retail_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM retail
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


# =========================
# LOAD RFM DATA
# =========================

@st.cache_data
def load_rfm_data():

    path = (
        PROCESSED_DIR /
        "rfm_segments.csv"
    )

    df = pd.read_csv(path)

    return df


# =========================
# LOAD COHORT DATA
# =========================

@st.cache_data
def load_cohort_data():

    path = (
        PROCESSED_DIR /
        "cohort_retention.csv"
    )

    df = pd.read_csv(
        path,
        index_col=0
    )

    return df


# =========================
# LOAD CHURN DATA
# =========================

@st.cache_data
def load_churn_data():

    path = (
        PROCESSED_DIR /
        "customer_churn_dataset.csv"
    )

    df = pd.read_csv(path)

    return df
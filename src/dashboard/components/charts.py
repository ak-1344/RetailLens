import streamlit as st
import plotly.express as px


# =========================
# REVENUE TREND
# =========================

def plot_revenue_trend(df):

    revenue_by_month = (
        df.groupby(["Year", "Month"])["Revenue"]
        .sum()
        .reset_index()
    )

    revenue_by_month["Period"] = (
        revenue_by_month["Year"].astype(str)
        + "-"
        + revenue_by_month["Month"].astype(str)
    )

    fig = px.line(
        revenue_by_month,
        x="Period",
        y="Revenue",
        markers=True,
        title="Monthly Revenue Trend",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# =========================
# COUNTRY REVENUE
# =========================

def plot_country_revenue(df):

    country_revenue = (
        df.groupby("Country")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(
            by="Revenue",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        country_revenue,
        x="Country",
        y="Revenue",
        title="Top Countries by Revenue",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# =========================
# CUSTOMER SEGMENTS
# =========================

def plot_customer_segments(df):

    segment_counts = (
        df["CustomerSegment"]
        .value_counts()
        .reset_index()
    )

    segment_counts.columns = [
        "Segment",
        "Count"
    ]

    fig = px.pie(
        segment_counts,
        names="Segment",
        values="Count",
        title="Customer Segments",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# =========================
# COHORT HEATMAP
# =========================

def plot_cohort_heatmap(df):

    fig = px.imshow(
        df,
        text_auto=".0%",
        aspect="auto",
        title="Customer Retention Heatmap",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# =========================
# CHURN DISTRIBUTION
# =========================

def plot_churn_distribution(df):

    churn_counts = (
        df["Churn"]
        .value_counts()
        .reset_index()
    )

    churn_counts.columns = [
        "Status",
        "Count"
    ]

    churn_counts["Status"] = (
        churn_counts["Status"]
        .map({
            0: "Active",
            1: "Churned"
        })
    )

    fig = px.pie(
        churn_counts,
        names="Status",
        values="Count",
        title="Churn Distribution",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )
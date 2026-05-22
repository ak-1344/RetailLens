import streamlit as st

from src.dashboard.utils import (
    load_churn_data
)

from src.dashboard.components.charts import (
    plot_churn_distribution
)


# =========================
# CHURN PAGE
# =========================

def render_churn_page(year_filter):

    st.title("Churn Prediction")

    st.markdown("---")

    df = load_churn_data()

    plot_churn_distribution(df)

    st.subheader(
        "High Risk Customers"
    )

    high_risk = df[
        df["Churn"] == 1
    ]

    st.dataframe(
        high_risk.head(20)
    )

    churn_rate = round(
        (
            high_risk.shape[0]
            / df.shape[0]
        ) * 100,
        2
    )

    st.metric(
        "Estimated Churn Rate",
        f"{churn_rate}%"
    )

    csv = high_risk.to_csv(index=False)

    st.download_button(
        "Download Churn Data",
        csv,
        "high_risk_customers.csv",
        "text/csv"
    )
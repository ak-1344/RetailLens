import streamlit as st

from src.dashboard.utils import (
    load_retail_data
)

from src.dashboard.components.charts import (
    plot_revenue_trend,
    plot_country_revenue
)


# =========================
# REVENUE PAGE
# =========================

def render_revenue_page(year_filter):

    st.title("Revenue Analytics")

    st.markdown("---")

    df = load_retail_data()

    df = df[
        df["Year"].isin(year_filter)
    ]

    plot_revenue_trend(df)

    plot_country_revenue(df)

    st.subheader(
        "Revenue Dataset Preview"
    )

    st.dataframe(
        df.head(20)
    )

    csv = df.to_csv(index=False)

    st.download_button(
        "Download Revenue Data",
        csv,
        "revenue_data.csv",
        "text/csv"
    )
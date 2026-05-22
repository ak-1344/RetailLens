import streamlit as st

from src.dashboard.utils import (
    load_retail_data,
    load_rfm_data
)

from src.dashboard.components.metrics import (
    render_kpi_card
)

from src.dashboard.components.charts import (
    plot_revenue_trend,
    plot_country_revenue,
    plot_customer_segments
)


# =========================
# OVERVIEW PAGE
# =========================

def render_overview_page(year_filter):

    st.title("Retail Lens Dashboard")

    st.markdown("---")

    retail_df = load_retail_data()

    rfm_df = load_rfm_data()

    retail_df = retail_df[
        retail_df["Year"].isin(year_filter)
    ]


    # =========================
    # KPIs
    # =========================

    st.subheader("Business Overview")

    total_revenue = round(
        retail_df["Revenue"].sum(),
        2
    )

    total_orders = (
        retail_df["InvoiceNo"]
        .nunique()
    )

    total_customers = (
        retail_df["CustomerID"]
        .nunique()
    )

    average_order_value = round(
        total_revenue / total_orders,
        2
    )


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_kpi_card(
            "Revenue",
            f"${total_revenue:,.0f}"
        )

    with col2:
        render_kpi_card(
            "Orders",
            f"{total_orders:,}"
        )

    with col3:
        render_kpi_card(
            "Customers",
            f"{total_customers:,}"
        )

    with col4:
        render_kpi_card(
            "AOV",
            f"${average_order_value}"
        )

    st.markdown("---")


    # =========================
    # CHARTS
    # =========================

    st.subheader(
        "Revenue & Customer Insights"
    )

    plot_revenue_trend(retail_df)

    col1, col2 = st.columns(2)

    with col1:
        plot_country_revenue(retail_df)

    with col2:
        plot_customer_segments(rfm_df)
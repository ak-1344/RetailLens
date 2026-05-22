import streamlit as st

from src.dashboard.utils import (
    load_rfm_data
)

from src.dashboard.components.charts import (
    plot_customer_segments
)


# =========================
# CUSTOMER PAGE
# =========================

def render_customers_page(year_filter):

    st.title("Customer Analytics")

    st.markdown("---")

    df = load_rfm_data()

    segment_filter = st.selectbox(

        "Select Customer Segment",

        sorted(
            df["CustomerSegment"]
            .unique()
        )
    )

    filtered_df = df[
        df["CustomerSegment"]
        == segment_filter
    ]

    plot_customer_segments(df)

    st.subheader(
        f"{segment_filter} Customers"
    )

    st.dataframe(
        filtered_df.head(20)
    )

    st.markdown("---")

    st.write(
        f"Total Customers: {filtered_df.shape[0]}"
    )

    st.write(
        f"Average Monetary Value: ${round(filtered_df['Monetary'].mean(), 2)}"
    )
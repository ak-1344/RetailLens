import streamlit as st

from src.dashboard.utils import (
    load_cohort_data
)

from src.dashboard.components.charts import (
    plot_cohort_heatmap
)


# =========================
# COHORT PAGE
# =========================

def render_cohort_page(year_filter):

    st.title("Cohort Analysis")

    st.markdown("---")

    df = load_cohort_data()

    plot_cohort_heatmap(df)

    with st.expander(
        "View Cohort Retention Table"
    ):

        st.dataframe(df)

    csv = df.to_csv()

    st.download_button(
        "Download Cohort Data",
        csv,
        "cohort_retention.csv",
        "text/csv"
    )
import streamlit as st


# =========================
# SIDEBAR
# =========================

def render_sidebar():

    st.sidebar.markdown(
        "# Retail Lens"
    )

    st.sidebar.caption(
        "Retail Analytics Platform"
    )

    st.sidebar.markdown("---")

    page = st.sidebar.radio(

        "Navigation",

        [
            "Overview",
            "Revenue Analytics",
            "Customer Analytics",
            "Cohort Analysis",
            "Churn Prediction"
        ]
    )

    st.sidebar.markdown("---")

    st.sidebar.markdown(
        "### Dashboard Filters"
    )

    year_filter = st.sidebar.multiselect(
        "Select Year",
        [2010, 2011],
        default=[2010, 2011]
    )

    return page, year_filter
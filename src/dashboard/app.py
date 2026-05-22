import streamlit as st

from src.dashboard.styles import (
    apply_global_styles
)

from src.dashboard.components.sidebar import (
    render_sidebar
)

from src.dashboard.views.overview import (
    render_overview_page
)

from src.dashboard.views.revenue import (
    render_revenue_page
)

from src.dashboard.views.customers import (
    render_customers_page
)

from src.dashboard.views.cohort import (
    render_cohort_page
)

from src.dashboard.views.churn import (
    render_churn_page
)


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(

    page_title="Retail Lens",

    page_icon="📊",

    layout="wide"
)

apply_global_styles()


# =========================
# SIDEBAR
# =========================

page, year_filter = render_sidebar()


# =========================
# ROUTING
# =========================

if page == "Overview":

    render_overview_page(
        year_filter
    )

elif page == "Revenue Analytics":

    render_revenue_page(
        year_filter
    )

elif page == "Customer Analytics":

    render_customers_page(
        year_filter
    )

elif page == "Cohort Analysis":

    render_cohort_page(
        year_filter
    )

elif page == "Churn Prediction":

    render_churn_page(
        year_filter
    )
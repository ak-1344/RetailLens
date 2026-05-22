import streamlit as st


# =========================
# KPI CARD
# =========================

def render_kpi_card(
    title,
    value,
    delta=None
):

    st.metric(
        label=title,
        value=value,
        delta=delta
    )
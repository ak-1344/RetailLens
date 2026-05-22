import streamlit as st


# =========================
# GLOBAL STYLES
# =========================

def apply_global_styles():

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #0E1117;
            color: white;
        }

        section[data-testid="stSidebar"] {
            background-color: #161A22;
        }

        div[data-testid="metric-container"] {
            background-color: #1C1F26;
            border: 1px solid #2E3440;
            padding: 20px;
            border-radius: 14px;
        }

        h1, h2, h3 {
            color: white;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
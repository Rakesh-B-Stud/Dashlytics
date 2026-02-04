import streamlit as st
import pandas as pd
from components import navbar, kpi, card_start, card_end,header

# -----------------------------------
# Navbar (React style)
# -----------------------------------
navbar()

st.title("Upload Dataset")

header("📂 Upload Dataset")
# -----------------------------------
# Upload Card
# -----------------------------------
card_start()

file = st.file_uploader("Upload CSV file", type=["csv"])

card_end()


if file:
    try:
        df = pd.read_csv(file)

        # ==================================
        # Save to session (KEEP THIS)
        # ==================================
        st.session_state["df"] = df
        st.session_state["dataset_name"] = file.name

        st.success(f"{file.name} uploaded successfully")


        # ==================================
        # KPI Row (React cards style)
        # ==================================
        rows, cols = df.shape
        missing = int(df.isnull().sum().sum())

        c1, c2, c3 = st.columns(3)

        kpi("Rows", rows, c1)
        kpi("Columns", cols, c2)
        kpi("Missing", missing, c3)


        # ==================================
        # Preview Card
        # ==================================
        card_start()

        st.subheader("Dataset Preview")
        st.dataframe(df.head(), width="stretch")

        card_end()

    except Exception as e:
        st.error(f"Error loading file: {e}")

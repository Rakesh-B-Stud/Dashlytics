import streamlit as st
from utils.visualization import histogram_plot, heatmap_plot
from components import navbar, kpi, card_start, card_end


# -----------------------------------
# Navbar
# -----------------------------------
navbar()

st.title("Data Analysis")


# -----------------------------------
# Check dataset
# -----------------------------------
if "clean_df" not in st.session_state:
    st.warning("Clean dataset not found")
    st.stop()

df = st.session_state["clean_df"]


# -----------------------------------
# KPI ROW (React style)
# -----------------------------------
rows, cols = df.shape
missing = int(df.isna().sum().sum())

c1, c2, c3 = st.columns(3)

kpi("Rows", rows, c1)
kpi("Columns", cols, c2)
kpi("Missing", missing, c3)


# -----------------------------------
# FILTER CARD
# -----------------------------------
card_start()

col = st.selectbox("Select Column for Histogram", df.columns)

card_end()


# -----------------------------------
# CHART GRID (React layout)
# -----------------------------------
left, right = st.columns(2)


with left:
    card_start()
    st.subheader("Histogram")
    st.plotly_chart(histogram_plot(df, col), width="stretch")
    card_end()


with right:
    card_start()
    st.subheader("Correlation Heatmap")
    st.plotly_chart(heatmap_plot(df), width="stretch")
    card_end()

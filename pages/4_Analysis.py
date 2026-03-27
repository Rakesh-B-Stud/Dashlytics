import streamlit as st
from utils.visualization import histogram_plot, heatmap_plot
from components import navbar, kpi, card_start, card_end, header, page_nav

st.set_page_config(
    page_title="Dashlytics — Analysis",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><rect x='2' y='12' width='4' height='10' rx='1' fill='%234493F8'/><rect x='8' y='7' width='4' height='15' rx='1' fill='%23A371F7'/><rect x='14' y='2' width='4' height='20' rx='1' fill='%234493F8' opacity='.7'/><rect x='20' y='9' width='2' height='13' rx='1' fill='%233FB950'/></svg>",
    layout="wide",
    initial_sidebar_state="collapsed",
)

navbar()
header("Data Analysis", "Histograms, correlation heatmaps, and descriptive statistics")

if "clean_df" not in st.session_state:
    st.warning("Clean dataset not found. Run Data Cleaning first.")
    st.stop()

df = st.session_state["clean_df"]

# -------------------------------------------------------
# KPI Row
# -------------------------------------------------------
rows, cols  = df.shape
missing     = int(df.isna().sum().sum())
num_cols    = len(df.select_dtypes("number").columns)

c1, c2, c3, c4 = st.columns(4)
kpi("Rows",            f"{rows:,}", c1)
kpi("Columns",         cols,        c2)
kpi("Numeric Columns", num_cols,    c3)
kpi("Missing Values",  missing,     c4)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------
# Column selector
# -------------------------------------------------------
card_start()
st.markdown("""
<div style="font-size:13px; font-weight:600; color:#8B949E; text-transform:uppercase;
             letter-spacing:0.08em; margin-bottom:12px;">Select Column</div>
""", unsafe_allow_html=True)
col = st.selectbox("Column for Histogram", df.columns, label_visibility="collapsed")
card_end()

# -------------------------------------------------------
# Chart grid
# -------------------------------------------------------
left, right = st.columns(2)

with left:
    st.markdown("""
    <div style="font-size:13px; font-weight:600; color:#8B949E; text-transform:uppercase;
                 letter-spacing:0.08em; margin-bottom:12px;">Distribution</div>
    """, unsafe_allow_html=True)
    fig_hist = histogram_plot(df, col)
    fig_hist.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#8B949E",
        margin=dict(l=0, r=0, t=10, b=0),
        height=300
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with right:
    st.markdown("""
    <div style="font-size:13px; font-weight:600; color:#8B949E; text-transform:uppercase;
                 letter-spacing:0.08em; margin-bottom:12px;">Correlation Heatmap</div>
    """, unsafe_allow_html=True)
    fig_heat = heatmap_plot(df)
    fig_heat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#8B949E",
        margin=dict(l=0, r=0, t=10, b=0),
        height=300
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# -------------------------------------------------------
# Stats table
# -------------------------------------------------------
st.markdown("""
<div style="font-size:13px; font-weight:600; color:#8B949E; text-transform:uppercase;
             letter-spacing:0.08em; margin-bottom:14px;">Descriptive Statistics</div>
""", unsafe_allow_html=True)
st.dataframe(df.describe().T, use_container_width=True)

# Page navigator
page_nav(current_step=3, next_page="pages/5_Models.py", next_label="Models →")
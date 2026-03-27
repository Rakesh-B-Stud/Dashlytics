import streamlit as st
import plotly.express as px
from components import navbar, kpi, card_start, card_end, header, page_nav

st.set_page_config(
    page_title="Dashlytics — Dashboard",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><rect x='2' y='12' width='4' height='10' rx='1' fill='%234493F8'/><rect x='8' y='7' width='4' height='15' rx='1' fill='%23A371F7'/><rect x='14' y='2' width='4' height='20' rx='1' fill='%234493F8' opacity='.7'/><rect x='20' y='9' width='2' height='13' rx='1' fill='%233FB950'/></svg>",
    layout="wide",
    initial_sidebar_state="collapsed",
)
navbar()
header("Interactive Dashboard", "Build custom charts · Select axes and chart types freely")

if "clean_df" not in st.session_state:
    st.warning("Upload & clean a dataset first.")
    st.stop()

df = st.session_state["clean_df"]

# -------------------------------------------------------
# KPI Row
# -------------------------------------------------------
rows, cols  = df.shape
num_cols    = len(df.select_dtypes("number").columns)

c1, c2, c3 = st.columns(3)
kpi("Rows",            f"{rows:,}", c1)
kpi("Columns",         cols,        c2)
kpi("Numeric Columns", num_cols,    c3)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------
# Chart builder
# -------------------------------------------------------
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#8B949E",
    font_family="Space Grotesk",
    margin=dict(l=0, r=0, t=20, b=0),
    height=280,
    colorway=["#4493F8","#A371F7","#3FB950","#F0883E","#58A6FF"],
    xaxis=dict(gridcolor="#21262D", linecolor="#21262D"),
    yaxis=dict(gridcolor="#21262D", linecolor="#21262D"),
)

def build_chart(name, idx):
    card_start()
    st.markdown(f"""
    <div style="font-size:12px; font-weight:600; color:#484F58; text-transform:uppercase;
                 letter-spacing:0.1em; margin-bottom:12px;">{name}</div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    chart = col1.selectbox("Type", ["Scatter", "Bar", "Line", "Histogram", "Box"], key=f"type{idx}")
    x     = col2.selectbox("X Axis", df.columns, key=f"x{idx}")
    y     = col3.selectbox("Y Axis", df.columns, key=f"y{idx}")

    if chart == "Scatter":
        fig = px.scatter(df, x=x, y=y, template="plotly_dark")
    elif chart == "Bar":
        fig = px.bar(df, x=x, y=y, template="plotly_dark")
    elif chart == "Line":
        fig = px.line(df, x=x, y=y, template="plotly_dark")
    elif chart == "Histogram":
        fig = px.histogram(df, x=x, template="plotly_dark")
    else:
        fig = px.box(df, y=y, template="plotly_dark")

    fig.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig, use_container_width=True, key=f"chart{idx}")
    card_end()
    return fig


# -------------------------------------------------------
# 4 chart grid
# -------------------------------------------------------
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

with row1_col1:
    fig1 = build_chart("Chart 1", 1)
with row1_col2:
    fig2 = build_chart("Chart 2", 2)
with row2_col1:
    fig3 = build_chart("Chart 3", 3)
with row2_col2:
    fig4 = build_chart("Chart 4", 4)

st.session_state["dashboard_figs"] = [fig1, fig2, fig3, fig4]

# Page navigator
page_nav(current_step=5, next_page="pages/7_Report.py", next_label="Generate Report →")
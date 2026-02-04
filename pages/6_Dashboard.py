import streamlit as st
import plotly.express as px
from components import navbar, kpi, card_start, card_end


# -----------------------------------
# Navbar
# -----------------------------------
navbar()

st.title("Interactive Dashboard")


# -----------------------------------
# Safety
# -----------------------------------
if "clean_df" not in st.session_state:
    st.warning("Upload & clean dataset first")
    st.stop()

df = st.session_state["clean_df"]


# -----------------------------------
# KPI ROW (professional look)
# -----------------------------------
rows, cols = df.shape
num_cols = len(df.select_dtypes("number").columns)

c1, c2, c3 = st.columns(3)
kpi("Rows", rows, c1)
kpi("Columns", cols, c2)
kpi("Numeric", num_cols, c3)



# -----------------------------------
# Chart builder (wrapped in card)
# -----------------------------------
def build_chart(name, idx):

    card_start()

    st.markdown(f"### {name}")

    col1, col2, col3 = st.columns(3)

    chart = col1.selectbox(
        "Type",
        ["Scatter", "Bar", "Line", "Histogram", "Box"],
        key=f"type{idx}"
    )

    x = col2.selectbox("X Axis", df.columns, key=f"x{idx}")
    y = col3.selectbox("Y Axis", df.columns, key=f"y{idx}")

    if chart == "Scatter":
        fig = px.scatter(df, x=x, y=y)

    elif chart == "Bar":
        fig = px.bar(df, x=x, y=y)

    elif chart == "Line":
        fig = px.line(df, x=x, y=y)

    elif chart == "Histogram":
        fig = px.histogram(df, x=x)

    else:
        fig = px.box(df, y=y)

    st.plotly_chart(fig, width="stretch", key=f"chart{idx}")

    card_end()

    return fig



# -----------------------------------
# 4 chart grid (React layout)
# -----------------------------------
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



# -----------------------------------
# Save figures
# -----------------------------------
st.session_state["dashboard_figs"] = [fig1, fig2, fig3, fig4]

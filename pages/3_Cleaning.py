import streamlit as st
from utils.cleaning import clean_data
from components import navbar, kpi, card_start, card_end


# -----------------------------------
# Navbar (React style)
# -----------------------------------
navbar()

st.title("Data Cleaning")


# -----------------------------------
# Stop if dataset not uploaded
# -----------------------------------
if "df" not in st.session_state:
    st.warning("Upload dataset first")
    st.stop()

df = st.session_state["df"]


# -----------------------------------
# Run cleaning (YOUR ORIGINAL LOGIC)
# -----------------------------------
clean_df, report = clean_data(df)
st.session_state["clean_df"] = clean_df


# -----------------------------------
# KPI Row (React style cards)
# -----------------------------------
c1, c2 = st.columns(2)

kpi("Duplicates Removed", report["duplicates_removed"], c1)
kpi("Missing Fixed", report["missing_before"], c2)


# -----------------------------------
# Preview Card
# -----------------------------------
card_start()

st.subheader("Cleaned Dataset Preview")
st.dataframe(clean_df.head(), width="stretch")

card_end()

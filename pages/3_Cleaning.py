import streamlit as st
from utils.cleaning import clean_data
from components import navbar, kpi, card_start, card_end, header, page_nav

st.set_page_config(
    page_title="Dashlytics — Cleaning",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><rect x='2' y='12' width='4' height='10' rx='1' fill='%234493F8'/><rect x='8' y='7' width='4' height='15' rx='1' fill='%23A371F7'/><rect x='14' y='2' width='4' height='20' rx='1' fill='%234493F8' opacity='.7'/><rect x='20' y='9' width='2' height='13' rx='1' fill='%233FB950'/></svg>",
    layout="wide",
    initial_sidebar_state="collapsed",
)

navbar()
header("Data Cleaning", "Automated duplicate removal and missing value imputation")

if "df" not in st.session_state:
    st.warning("Upload a dataset first.")
    st.stop()

df = st.session_state["df"]

# Run cleaning
clean_df, report = clean_data(df)
st.session_state["clean_df"] = clean_df

# -------------------------------------------------------
# KPI Row
# -------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
kpi("Original Rows",      f'{df.shape[0]:,}',                    c1)
kpi("Clean Rows",         f'{clean_df.shape[0]:,}',              c2)
kpi("Duplicates Removed", report["duplicates_removed"],          c3)
kpi("Missing Fixed",      f'{int(report["missing_before"]):,}',  c4)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------
# Cleaning summary
# -------------------------------------------------------
card_start()
st.markdown("""
<div style="font-size:13px; font-weight:600; color:#8B949E; text-transform:uppercase;
             letter-spacing:0.08em; margin-bottom:16px;">Cleaning Summary</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    dup_color  = "#F85149" if report["duplicates_removed"] > 0 else "#3FB950"
    dup_status = "removed" if report["duplicates_removed"] > 0 else "none found"
    st.markdown(f"""
    <div style="background:#0D1117; border:1px solid #21262D; border-radius:10px; padding:16px 18px;">
        <div style="font-size:11px; color:#484F58; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">
            Duplicates
        </div>
        <div style="font-size:22px; font-weight:700; color:{dup_color}; font-family:'JetBrains Mono',monospace;">
            {report["duplicates_removed"]}
        </div>
        <div style="font-size:12px; color:#484F58;">{dup_status}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    miss = int(report["missing_before"])
    miss_color  = "#F0883E" if miss > 0 else "#3FB950"
    miss_status = "imputed with column mean" if miss > 0 else "dataset is complete"
    st.markdown(f"""
    <div style="background:#0D1117; border:1px solid #21262D; border-radius:10px; padding:16px 18px;">
        <div style="font-size:11px; color:#484F58; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">
            Missing Values
        </div>
        <div style="font-size:22px; font-weight:700; color:{miss_color}; font-family:'JetBrains Mono',monospace;">
            {miss}
        </div>
        <div style="font-size:12px; color:#484F58;">{miss_status}</div>
    </div>
    """, unsafe_allow_html=True)

card_end()
st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------
# Preview
# -------------------------------------------------------
st.markdown("""
<div style="font-size:13px; font-weight:600; color:#8B949E; text-transform:uppercase;
             letter-spacing:0.08em; margin-bottom:14px;">Cleaned Dataset Preview</div>
""", unsafe_allow_html=True)
st.dataframe(clean_df.head(10), use_container_width=True)

# Page navigator
page_nav(current_step=2, next_page="pages/4_Analysis.py", next_label="Analysis →")
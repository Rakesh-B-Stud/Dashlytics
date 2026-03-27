import streamlit as st
import pandas as pd
from components import navbar, kpi, header, page_nav

st.set_page_config(
    page_title="Dashlytics — Upload",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><rect x='2' y='12' width='4' height='10' rx='1' fill='%234493F8'/><rect x='8' y='7' width='4' height='15' rx='1' fill='%23A371F7'/><rect x='14' y='2' width='4' height='20' rx='1' fill='%234493F8' opacity='.7'/><rect x='20' y='9' width='2' height='13' rx='1' fill='%233FB950'/></svg>",
    layout="wide",
    initial_sidebar_state="collapsed",
)

navbar()
header("Upload Dataset", "Supported format: CSV · Max recommended size: 200 MB")

# -------------------------------------------------------
# Upload
# -------------------------------------------------------
st.markdown("""
<div style="margin-bottom:14px;">
    <span style="font-size:13px; font-weight:600; color:#8B949E; text-transform:uppercase;
                 letter-spacing:0.08em;">Select File</span>
</div>
""", unsafe_allow_html=True)

file = st.file_uploader(
    "Drop your CSV here or click to browse",
    type=["csv"],
    label_visibility="collapsed"
)

# -------------------------------------------------------
# On upload
# -------------------------------------------------------
if file:
    try:
        df = pd.read_csv(file)

        st.session_state["df"] = df
        st.session_state["dataset_name"] = file.name

        # Success banner
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; background:rgba(63,185,80,0.08);
                    border:1px solid rgba(63,185,80,0.25); border-radius:12px; padding:12px 18px;
                    margin-bottom:20px;">
            <span style="color:#3FB950; font-size:16px;">&#10003;</span>
            <div>
                <div style="font-size:14px; font-weight:600; color:#3FB950;">{file.name}</div>
                <div style="font-size:12px; color:#484F58;">File uploaded successfully</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # KPI Row
        rows, cols = df.shape
        missing = int(df.isnull().sum().sum())

        c1, c2, c3 = st.columns(3)
        kpi("Rows", f"{rows:,}", c1)
        kpi("Columns", cols, c2)
        kpi("Missing Values", f"{missing:,}", c3)

        st.markdown("<br>", unsafe_allow_html=True)

        # Preview
        st.markdown("""
        <div style="font-size:13px; font-weight:600; color:#8B949E; text-transform:uppercase;
                     letter-spacing:0.08em; margin-bottom:14px;">Dataset Preview</div>
        """, unsafe_allow_html=True)
        st.dataframe(df.head(10), use_container_width=True)

        # Page navigator
        page_nav(current_step=1, next_page="pages/3_Cleaning.py", next_label="Data Cleaning →")

    except Exception as e:
        st.error(f"Error loading file: {e}")
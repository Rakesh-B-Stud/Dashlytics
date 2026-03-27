import streamlit as st
from utils.database import fetch_all
from components import navbar, header, kpi

st.set_page_config(
    page_title="Dashlytics — Report",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><rect x='2' y='12' width='4' height='10' rx='1' fill='%234493F8'/><rect x='8' y='7' width='4' height='15' rx='1' fill='%23A371F7'/><rect x='14' y='2' width='4' height='20' rx='1' fill='%234493F8' opacity='.7'/><rect x='20' y='9' width='2' height='13' rx='1' fill='%233FB950'/></svg>",
    layout="wide",
    initial_sidebar_state="collapsed",
)
navbar()
header("Analysis History", "All past model runs, sorted by most recent")

rows = fetch_all()

if not rows:
    st.markdown("""
    <div style="text-align:center; padding:60px 20px;">
        <div style="font-size:32px; margin-bottom:12px;">&#128345;</div>
        <div style="font-size:16px; font-weight:600; color:#E6EDF3; margin-bottom:6px;">No analyses yet</div>
        <div style="font-size:13px; color:#484F58;">Run models on a dataset to see history here.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# -------------------------------------------------------
# Summary KPIs
# -------------------------------------------------------
c1, c2 = st.columns(2)
kpi("Total Runs", len(rows), c1)

best_accs = [r[2] for r in rows]
kpi("Best Accuracy", f"{round(max(best_accs)*100,1)}%", c2)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------
# History table header
# -------------------------------------------------------
st.markdown("""
<div style="display:grid; grid-template-columns:2fr 1.5fr 1fr 1.5fr;
            padding:10px 20px; background:#0D1117; border:1px solid #21262D;
            border-radius:10px 10px 0 0; margin-bottom:0;">
    <span style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#484F58;">Dataset</span>
    <span style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#484F58;">Best Model</span>
    <span style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#484F58;">Accuracy</span>
    <span style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#484F58;">Timestamp</span>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Rows
# -------------------------------------------------------
for i, (dataset, model, acc, time) in enumerate(rows):
    acc_pct    = round(acc * 100, 2)
    is_last    = (i == len(rows) - 1)
    border_rad = "0 0 10px 10px" if is_last else "0"

    st.markdown(f"""
    <div style="display:grid; grid-template-columns:2fr 1.5fr 1fr 1.5fr;
                padding:14px 20px; background:#161B22; border:1px solid #21262D;
                border-top:none; border-radius:{border_rad};">
        <div>
            <div style="font-size:14px;font-weight:600;color:#E6EDF3;">{dataset}</div>
        </div>
        <div style="font-size:13px;color:#8B949E;display:flex;align-items:center;">{model}</div>
        <div style="display:flex;align-items:center;">
            <span style="background:rgba(63,185,80,0.12);border:1px solid rgba(63,185,80,0.25);
                         color:#3FB950;font-size:12px;font-weight:700;font-family:'JetBrains Mono',monospace;
                         padding:3px 10px;border-radius:100px;">{acc_pct}%</span>
        </div>
        <div style="font-size:12px;color:#484F58;display:flex;align-items:center;
                    font-family:'JetBrains Mono',monospace;">{time}</div>
    </div>
    """, unsafe_allow_html=True)
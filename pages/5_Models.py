import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from utils.modeling import run_models
from utils.database import init_db, insert_record
from components import navbar, kpi, card_start, card_end, header, page_nav

st.set_page_config(
    page_title="Dashlytics — Models",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><rect x='2' y='12' width='4' height='10' rx='1' fill='%234493F8'/><rect x='8' y='7' width='4' height='15' rx='1' fill='%23A371F7'/><rect x='14' y='2' width='4' height='20' rx='1' fill='%234493F8' opacity='.7'/><rect x='20' y='9' width='2' height='13' rx='1' fill='%233FB950'/></svg>",
    layout="wide",
    initial_sidebar_state="collapsed",
)

navbar()
header("Machine Learning Models", "KNN · Decision Tree · Naive Bayes — evaluated simultaneously")

init_db()

if "clean_df" not in st.session_state:
    st.warning("Please upload and clean a dataset first.")
    st.stop()

df           = st.session_state["clean_df"]
dataset_name = st.session_state.get("dataset_name", "Dataset")

# -------------------------------------------------------
# KPI Row
# -------------------------------------------------------
rows, cols = df.shape
c1, c2, c3 = st.columns(3)
kpi("Rows",    f"{rows:,}", c1)
kpi("Columns", cols,        c2)
kpi("Models",  "3",         c3)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------
# Target selection
# -------------------------------------------------------
card_start()
st.markdown("""
<div style="font-size:13px; font-weight:600; color:#8B949E; text-transform:uppercase;
             letter-spacing:0.08em; margin-bottom:12px;">Configuration</div>
""", unsafe_allow_html=True)

c_sel, c_btn = st.columns([3, 1])
with c_sel:
    target = st.selectbox("Target Column", df.columns, label_visibility="visible")
with c_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("▶  Run Models", use_container_width=True)

card_end()

# -------------------------------------------------------
# Run models
# -------------------------------------------------------
if run_btn:
    try:
        with st.spinner("Training models…"):
            results, best = run_models(df, target)
            st.session_state["model_results"] = results

        result_df = pd.DataFrame(
            list(results.items()),
            columns=["Model", "Accuracy"]
        )

        st.markdown("""
        <div style="font-size:13px; font-weight:600; color:#8B949E; text-transform:uppercase;
                     letter-spacing:0.08em; margin-bottom:16px;">Model Performance</div>
        """, unsafe_allow_html=True)

        rows_html = ""
        for _, row in result_df.iterrows():
            acc_pct  = round(row["Accuracy"] * 100, 2)
            is_best  = row["Model"] == best
            bar_w    = int(acc_pct)
            name_col = f'<strong style="color:#E6EDF3;">{row["Model"]}</strong>' if is_best else row["Model"]
            badge    = '<span style="background:rgba(63,185,80,0.12);border:1px solid rgba(63,185,80,0.3);color:#3FB950;font-size:10px;font-weight:700;padding:2px 8px;border-radius:100px;margin-left:8px;">BEST</span>' if is_best else ""

            rows_html += f"""
            <tr>
                <td style="padding:14px 16px; border-bottom:1px solid #21262D; color:#8B949E;">
                    {name_col}{badge}
                </td>
                <td style="padding:14px 16px; border-bottom:1px solid #21262D;">
                    <div>
                        <div style="background:#0D1117; border-radius:100px; height:6px; margin-bottom:6px;">
                            <div style="width:{bar_w}%; height:6px; background:{'#3FB950' if is_best else '#4493F8'}; border-radius:100px;"></div>
                        </div>
                        <span style="display:block; text-align:right; font-family:'JetBrains Mono',monospace; font-size:13px; font-weight:600;
                                     color:{'#3FB950' if is_best else '#E6EDF3'};">
                            {acc_pct}%
                        </span>
                    </div>
                </td>
            </tr>
            """

        components.html(f"""
        <table style="width:100%; border-collapse:collapse;">
            <thead>
                <tr>
                    <th style="text-align:left; padding:10px 16px; background:#0D1117; color:#484F58;
                               font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.08em;
                               border-bottom:1px solid #21262D;">Model</th>
                    <th style="text-align:left; padding:10px 16px; background:#0D1117; color:#484F58;
                               font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.08em;
                               border-bottom:1px solid #21262D;">Accuracy</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        """, height=300)

        # Best model card
        best_acc = round(results[best] * 100, 2)
        st.markdown(f"""
        <div class="best-model-card">
            <div class="best-model-label">&#127942; &nbsp;Best Performing Model</div>
            <div class="best-model-name">{best}</div>
            <div class="best-model-acc">{best_acc}% accuracy</div>
        </div>
        """, unsafe_allow_html=True)

        insert_record(dataset_name, best, results[best])

        st.markdown("""
        <div style="margin-top:12px; text-align:center;">
            <span style="font-size:12px; color:#484F58;">&#10003; &nbsp;Saved to analysis history</span>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")

# Page navigator
page_nav(current_step=4, next_page="pages/6_Dashboard.py", next_label="Dashboard →")
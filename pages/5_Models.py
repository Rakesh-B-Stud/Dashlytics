import streamlit as st
import pandas as pd
from utils.modeling import run_models
from utils.database import init_db, insert_record
from components import navbar, kpi, card_start, card_end


# -----------------------------------
# Navbar
# -----------------------------------
navbar()

st.title("Machine Learning Models")


# -----------------------------------
# Init database
# -----------------------------------
init_db()


# -----------------------------------
# Safety
# -----------------------------------
if "clean_df" not in st.session_state:
    st.warning("Please upload and clean dataset first")
    st.stop()

df = st.session_state["clean_df"]
dataset_name = st.session_state.get("dataset_name", "Dataset")


# -----------------------------------
# KPI ROW (React style)
# -----------------------------------
rows, cols = df.shape

c1, c2 = st.columns(2)
kpi("Rows", rows, c1)
kpi("Columns", cols, c2)


# -----------------------------------
# Target selection card
# -----------------------------------
card_start()

target = st.selectbox("Select Target Column", df.columns)

run_btn = st.button("Run Models")

card_end()


# -----------------------------------
# Run models
# -----------------------------------
if run_btn:

    try:
        results, best = run_models(df, target)

        st.session_state["model_results"] = results

        result_df = pd.DataFrame(
            list(results.items()),
            columns=["Model", "Accuracy"]
        )


        # ------------------------------
        # Results table card
        # ------------------------------
        card_start()

        st.subheader("Model Performance")
        st.dataframe(result_df, width="stretch")

        card_end()


        # ------------------------------
        # Best model highlight card
        # ------------------------------
        best_acc = round(results[best] * 100, 2)

        card_start()

        st.markdown(f"""
        <h3 style='color:white;'>Best Model</h3>
        <p style='color:#9ca3af;'>Algorithm</p>
        <h2 style='color:white;'>{best}</h2>
        <p style='color:#9ca3af;'>Accuracy</p>
        <h2 style='color:white;'>{best_acc}%</h2>
        """, unsafe_allow_html=True)

        card_end()


        # Save history
        insert_record(dataset_name, best, results[best])

        st.success("Saved to history successfully")

    except Exception as e:
        st.error(f"Error: {e}")

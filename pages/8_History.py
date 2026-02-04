import streamlit as st
from utils.database import fetch_all

st.title("🕘 Recent Analyses")

rows = fetch_all()

if not rows:
    st.info("No analyses yet. Run models first.")
    st.stop()

for dataset, model, acc, time in rows:

    with st.container():

        c1, c2, c3, c4 = st.columns([3,2,2,2])

        c1.markdown(f"### 📂 {dataset}")
        c2.metric("Best Model", model)
        c3.metric("Accuracy", f"{round(acc*100,2)}%")
        c4.write(time)

        st.divider()

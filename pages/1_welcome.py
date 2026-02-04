import streamlit as st
from components import navbar, kpi, card_start, card_end

# Top navbar (React style)
navbar()


# -----------------------------
# HERO TITLE
# -----------------------------

st.markdown("""
<h1 style='text-align:center; color:white; margin-bottom:10px;'>
🚀 SmartEDA
</h1>

<p style='text-align:center; color:#9ca3af; margin-bottom:40px;'>
AI-Powered Automatic Data Cleaning, Analysis & Dashboard Generation
</p>
""", unsafe_allow_html=True)



# -----------------------------
# KPI ROW (React style cards)
# -----------------------------

c1, c2, c3 = st.columns(3)

kpi("⚡ Speed", "Automatic", c1)
kpi("🤖 Models", "3 Algorithms", c2)
kpi("📊 Dashboard", "Interactive", c3)



# -----------------------------
# CTA BUTTON CARD
# -----------------------------

card_start()

st.markdown("""
<h3 style='text-align:center;color:white;'>Get Started</h3>
<p style='text-align:center;color:#9ca3af;'>Upload your dataset and begin analysis instantly</p>
""", unsafe_allow_html=True)

if st.button("Upload Dataset"):
    st.switch_page("pages/2_Upload.py")

card_end()


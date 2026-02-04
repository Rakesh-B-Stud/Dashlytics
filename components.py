import streamlit as st


# ---------- LOAD CSS ----------
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ---------- NAVBAR ----------
def navbar():
    st.markdown("""
    <div class="navbar">
        <h2 style="margin:0;color:white;">Dashlytics</h2>
        <p style="margin:0;color:#9ca3af;">AI-Driven Dashboard & Reporting System</p>
    </div>
    """, unsafe_allow_html=True)


# ---------- SIDEBAR ----------
def sidebar():
    with st.sidebar:
        st.title("Workspace")

        st.page_link("pages/2_Upload.py", label="Upload")
        st.page_link("pages/4_Analysis.py", label="Analysis")
        st.page_link("pages/6_Dashboard.py", label="Dashboard")
        st.page_link("pages/5_Models.py", label="Models")
        st.page_link("pages/7_Report.py", label="Report")
        st.page_link("pages/8_History.py", label="History")


# ---------- KPI CARD ----------
def kpi(title, value, col):
    with col:
        st.markdown(f"""
        <div class="kpi">
            <p style="color:#9ca3af;margin:0">{title}</p>
            <h2 style="color:white;margin:5px 0">{value}</h2>
        </div>
        """, unsafe_allow_html=True)


# ---------- CARD WRAPPER ----------
def card_start():
    st.markdown('<div class="card">', unsafe_allow_html=True)


def card_end():
    st.markdown('</div>', unsafe_allow_html=True)
import streamlit as st

# -----------------------------------
# Gradient Page Header
# -----------------------------------
def header(title):

    st.markdown(
        """
        <div class="gradient-text">
            Dashlytics
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"<h3 style='color:#94a3b8; margin-top:-10px'>{title}</h3>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

import streamlit as st
import os

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "styles.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # Fallback inline if file not found
        st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] { background-color: #080A0F !important; color: #E6EDF3 !important; }
                    /* 🔥 REMOVE STREAMLIT UI */
header[data-testid="stHeader"] { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

/* Fix top spacing after removing header */
.block-container {
    padding-top: 1rem !important;
}
                    /* 📱 MOBILE RESPONSIVE */
@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .stColumns {
        flex-direction: column !important;
        gap: 12px !important;
    }

    .card {
        width: 100% !important;
    }

    button {
        width: 100% !important;
    }

    h1 { font-size: 22px !important; }
    h2 { font-size: 18px !important; }
    h3 { font-size: 16px !important; }
}
        </style>
        """, unsafe_allow_html=True)
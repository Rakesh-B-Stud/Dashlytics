import streamlit as st

def load_css():

    st.markdown("""
    <style>

    /* =====================================================
       BACKGROUND (Purple/Blue Premium Gradient)
    ====================================================== */
    [data-testid="stAppViewContainer"] {
        background:
        radial-gradient(circle at 20% 20%, #1e1b4b 0%, transparent 40%),
        radial-gradient(circle at 80% 80%, #0ea5e9 0%, transparent 40%),
        linear-gradient(135deg,#0b1026,#111827,#0f172a);
        color: #e2e8f0;
    }

    /* =====================================================
       SIDEBAR
    ====================================================== */
    section[data-testid="stSidebar"] {
        background: rgba(15,23,42,0.9);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* =====================================================
       GLASS CARDS
    ====================================================== */
    .card {
        background: rgba(30,41,59,0.65);
        backdrop-filter: blur(18px);
        border-radius: 18px;
        padding: 28px;
        border: 1px solid rgba(255,255,255,0.08);

        box-shadow:
            0 10px 30px rgba(0,0,0,0.5),
            0 0 30px rgba(59,130,246,0.15);

        margin-bottom: 25px;
        transition: 0.25s ease;
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow:
            0 12px 40px rgba(0,0,0,0.6),
            0 0 40px rgba(59,130,246,0.35);
    }

    /* =====================================================
       GRADIENT HEADER TEXT
    ====================================================== */
    .gradient-text {
        font-size: 48px;
        font-weight: 900;
        background: linear-gradient(90deg,#8b5cf6,#3b82f6,#06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* =====================================================
       BUTTONS (Neon Gradient)
    ====================================================== */
    .stButton > button {
        background: linear-gradient(90deg,#8b5cf6,#3b82f6);
        color: white;
        font-weight: 600;
        border-radius: 14px;
        padding: 10px 26px;
        border: none;
        box-shadow: 0 0 18px rgba(139,92,246,0.5);
    }

    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 28px rgba(139,92,246,0.8);
    }

    /* =====================================================
       METRIC CARDS
    ====================================================== */
    [data-testid="metric-container"] {
        background: rgba(30,41,59,0.65);
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.06);
        padding: 16px;
    }

    /* =====================================================
       TABLES
    ====================================================== */
    .stDataFrame {
        border-radius: 14px;
    }

    </style>
    """, unsafe_allow_html=True)

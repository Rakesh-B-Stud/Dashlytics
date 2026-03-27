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
        </style>
        """, unsafe_allow_html=True)
import streamlit as st
from components import load_css, navbar, sidebar
from style import load_css
load_css()

st.set_page_config(
    page_title="Dashlytics",
    page_icon="📊",
    layout="wide"
)

load_css()
navbar()
sidebar()

st.write("Select a page from the sidebar to begin.")

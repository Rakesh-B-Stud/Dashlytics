import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import *
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
import re

from components import navbar, kpi, card_start, card_end, header, page_nav

load_dotenv()
st.set_page_config(
    page_title="Dashlytics — Report",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><rect x='2' y='12' width='4' height='10' rx='1' fill='%234493F8'/><rect x='8' y='7' width='4' height='15' rx='1' fill='%23A371F7'/><rect x='14' y='2' width='4' height='20' rx='1' fill='%234493F8' opacity='.7'/><rect x='20' y='9' width='2' height='13' rx='1' fill='%233FB950'/></svg>",
    layout="wide",
    initial_sidebar_state="collapsed",
)
# =========================================================
# FONTS
# =========================================================
pdfmetrics.registerFont(TTFont("Times",      "assets/fonts/times.ttf"))
pdfmetrics.registerFont(TTFont("Times-Bold", "assets/fonts/timesbd.ttf"))

navbar()
header("AI Professional Report", "Generate and download a full analytical PDF report")

# =========================================================
# OpenRouter Client
# =========================================================
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    st.error("OPENROUTER_API_KEY not found in .env")
    st.stop()

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=API_KEY)

if "clean_df" not in st.session_state:
    st.warning("Run analysis first.")
    st.stop()

df           = st.session_state["clean_df"]
models       = st.session_state.get("model_results", {})
figs         = st.session_state.get("dashboard_figs", [])
dataset_name = st.session_state.get("dataset_name", "Dataset")
rows, cols   = df.shape

# -------------------------------------------------------
# KPI Row
# -------------------------------------------------------
c1, c2, c3 = st.columns(3)
kpi("Rows",   f"{rows:,}",  c1)
kpi("Columns", cols,         c2)
kpi("Charts",  len(figs),    c3)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# PROMPT
# =========================================================
def build_prompt():
    stats      = df.describe().to_string()
    model_text = "\n".join([f"{k}: {round(v*100,2)}%" for k, v in models.items()]) or "No models run."
    return f"""
You are a senior data analyst.
Write a FULL professional analytics report.

STRICT REQUIREMENTS:
- Total length MUST be 1500+ words
- EACH section must be 150-250 words
- DO NOT summarize
- DO NOT shorten content
- Use detailed explanations
- Maintain business report style
- DO NOT use markdown formatting like **, *, ##, or any symbols
- Write in plain text only
- Each section heading must appear ALONE on its own line, exactly as listed below

USE EXACT HEADINGS (DO NOT CHANGE TEXT, place each on its own line):
Executive Summary
Data Cleaning
Statistical Analysis
Visualization Insights
Model Evaluation
Business Recommendations
Conclusion

Dataset:
Rows: {rows}
Columns: {cols}

Statistics:
{stats}

Model Results:
{model_text}
"""

# =========================================================
# AI Generation
# =========================================================
def generate_ai_text():
    response = client.chat.completions.create(
        model="meta-llama/llama-3-70b-instruct",
        messages=[{"role": "user", "content": build_prompt()}],
        temperature=0.3,
        max_tokens=6000
    )
    return response.choices[0].message.content

# =========================================================
# Save charts
# =========================================================
def save_images():
    paths = []
    for i, fig in enumerate(figs):
        fig.update_layout(
            template="plotly_white",
            colorway=["#4f46e5","#06b6d4","#22c55e","#f59e0b","#ef4444"]
        )
        p = f"chart_{i}.png"
        fig.write_image(p, scale=3)
        paths.append(p)
    return paths

# =========================================================
# Strip markdown
# =========================================================
def clean_markdown(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'__(.*?)__',     r'\1', text)
    text = re.sub(r'\*(.*?)\*',     r'\1', text)
    text = re.sub(r'_(.*?)_',       r'\1', text)
    text = re.sub(r'^#{1,6}\s+',    '',    text, flags=re.MULTILINE)
    text = re.sub(r'^\s*[-•]\s+',   '',    text, flags=re.MULTILINE)
    return text

# =========================================================
# Header/footer
# =========================================================
def add_header_footer(canvas, doc):
    canvas.saveState()
    width, height = doc.pagesize
    logo_path = "assets/logo/logo.png"
    canvas.setFont("Times-Bold", 10)
    canvas.drawString(60, height - 35, "Dashlytics — Automated Analytics, Intelligent Reporting")
    if os.path.exists(logo_path):
        canvas.drawImage(logo_path, width-140, height-50, width=120, height=30,
                         preserveAspectRatio=True, mask='auto')
    canvas.setStrokeColor(colors.grey)
    canvas.setLineWidth(1.5)
    canvas.line(20, height-60, width-20, height-60)
    footer_y     = 25
    dataset_name = st.session_state.get("dataset_name", "Dataset")
    canvas.setLineWidth(1.5)
    canvas.line(20, 45, width-20, 45)
    canvas.setFont("Times", 9)
    canvas.drawString(20, footer_y, f"Dataset: {dataset_name}")
    canvas.drawRightString(width-20, footer_y, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()

# =========================================================
# PDF Generator
# =========================================================
def generate_pdf(text, paths):
    text = clean_markdown(text)
    doc  = SimpleDocTemplate("Dashlytics_Report.pdf",
                              leftMargin=60, rightMargin=60,
                              topMargin=60,  bottomMargin=60)
    elements = []

    heading_style = ParagraphStyle("heading", fontName="Times-Bold", fontSize=18,
                                   leading=22, spaceBefore=30, spaceAfter=18, alignment=0)
    body_style    = ParagraphStyle("body", fontName="Times", fontSize=12,
                                   leading=19, spaceAfter=8, alignment=TA_JUSTIFY)
    title_style   = ParagraphStyle("analysis_title", fontName="Times-Bold", fontSize=24,
                                   alignment=1, spaceAfter=30)

    logo_path = "assets/logo/logo.png"
    elements.append(Spacer(1, 200))
    if os.path.exists(logo_path):
        elements.append(Image("assets/logo/logo.png", width=380, height=85))
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("Dashlytics", heading_style))
    elements.append(Paragraph("Automated Analytics, Intelligent Reporting", body_style))
    elements.append(Spacer(1, 30))
    elements.append(Paragraph(f"Dataset: {st.session_state.get('dataset_name','Dataset')}", heading_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%d %B %Y')}", body_style))
    elements.append(PageBreak())
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("Analysis Report", title_style))
    elements.append(Spacer(1, 30))

    HEADINGS = {"Executive Summary","Data Cleaning","Statistical Analysis",
                "Visualization Insights","Model Evaluation","Business Recommendations","Conclusion"}
    charts_inserted = False

    for line in text.split("\n"):
        clean = line.strip()
        if not clean:
            continue
        if clean in HEADINGS:
            elements.append(Paragraph(clean, heading_style))
            if clean == "Visualization Insights" and not charts_inserted:
                charts_inserted = True
                for i, p in enumerate(paths):
                    elements.append(Spacer(1, 12))
                    elements.append(Image(p, width=420, height=260))
                    elements.append(Spacer(1, 6))
                    elements.append(Paragraph(f"Figure {i+1}: Dashboard Visualization", body_style))
        else:
            elements.append(Paragraph(clean, body_style))

    doc.build(elements, onFirstPage=add_header_footer, onLaterPages=add_header_footer)


# =========================================================
# UI
# =========================================================
card_start()

st.markdown("""
<div style="margin-bottom:16px;">
    <div style="font-size:15px; font-weight:600; color:#E6EDF3; margin-bottom:4px;">
        Generate Professional PDF Report
    </div>
    <div style="font-size:13px; color:#484F58;">
        An LLM will analyse your dataset statistics and write a detailed 1500+ word report
        with your dashboard charts embedded.
    </div>
</div>
""", unsafe_allow_html=True)

model_chips = ""
for name, acc in models.items():
    model_chips += f'<span style="background:#161B22;border:1px solid #21262D;color:#8B949E;font-size:11px;font-family:\'JetBrains Mono\',monospace;padding:4px 10px;border-radius:6px;margin-right:6px;">{name}: {round(acc*100,1)}%</span>'

if model_chips:
    st.markdown(f'<div style="margin-bottom:16px;">{model_chips}</div>', unsafe_allow_html=True)

generate = st.button("&#9889;  Generate Report", use_container_width=False)
card_end()

# =========================================================
# Generate Flow
# =========================================================
if generate:
    with st.spinner("Analysing data and writing report…"):
        text = generate_ai_text()
        st.session_state["report_text"] = text
        paths = save_images()
        generate_pdf(text, paths)

    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;background:rgba(63,185,80,0.08);
                border:1px solid rgba(63,185,80,0.25);border-radius:12px;padding:12px 18px;
                margin:16px 0;">
        <span style="color:#3FB950;font-size:16px;">&#10003;</span>
        <span style="font-size:14px;font-weight:600;color:#3FB950;">Report generated successfully</span>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# Preview + Download
# =========================================================
if "report_text" in st.session_state:
    card_start()
    st.markdown("""
    <div style="font-size:13px; font-weight:600; color:#8B949E; text-transform:uppercase;
                 letter-spacing:0.08em; margin-bottom:12px;">Report Preview</div>
    """, unsafe_allow_html=True)
    st.text_area("", st.session_state["report_text"], height=400, label_visibility="collapsed")
    card_end()

    st.markdown("<br>", unsafe_allow_html=True)

    with open("Dashlytics_Report.pdf", "rb") as f:
        st.download_button(
            "&#11015;  Download PDF Report",
            f,
            "Dashlytics_Report.pdf",
            mime="application/pdf",
            use_container_width=False
        )

# Page navigator — last step, no next page
page_nav(current_step=6)
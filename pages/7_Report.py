import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from components import navbar, kpi, card_start, card_end

load_dotenv()


# =========================================================
# Navbar
# =========================================================
navbar()
st.title("AI Professional Report")


# =========================================================
# OpenRouter Client
# =========================================================
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    st.error("OPENROUTER_API_KEY not found")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)


# =========================================================
# Safety
# =========================================================
if "clean_df" not in st.session_state:
    st.warning("Run analysis first")
    st.stop()

df = st.session_state["clean_df"]
models = st.session_state.get("model_results", {})
figs = st.session_state.get("dashboard_figs", [])
dataset_name = st.session_state.get("dataset_name", "Dataset")


# =========================================================
# KPI
# =========================================================
rows, cols = df.shape
c1, c2, c3 = st.columns(3)
kpi("Rows", rows, c1)
kpi("Columns", cols, c2)
kpi("Charts", len(figs), c3)


# =========================================================
# Clean AI text (remove quotes)
# =========================================================
def clean_text(text):
    return text.replace('"', '').replace("'", '')


# =========================================================
# Prompt
# =========================================================
def build_prompt():

    stats = df.describe().to_string()

    model_text = "\n".join(
        [f"{k}: {round(v*100,2)}%" for k, v in models.items()]
    ) or "No models run."

    return f"""
Write a detailed professional analytics report (minimum 1500 words).

IMPORTANT:
• Do NOT use quotes
• Do NOT use bullets
• Headings must be plain text

Sections:
Executive Summary
Data Cleaning
Statistical Analysis
Visualization Insights
Model Evaluation
Business Recommendations
Conclusion

Dataset: {rows} rows, {cols} columns

Statistics:
{stats}

Model Results:
{model_text}
"""


# =========================================================
# AI generation
# =========================================================
def generate_ai_text():

    response = client.chat.completions.create(
        model="meta-llama/llama-3-8b-instruct",
        messages=[{"role": "user", "content": build_prompt()}],
        temperature=0.6,
        max_tokens=3000
    )

    return clean_text(response.choices[0].message.content)


# =========================================================
# Save charts (colorful + high quality)
# =========================================================
def save_images():

    import os

    paths = []

    for i, fig in enumerate(figs):

        fig.update_layout(
            template="plotly",
            paper_bgcolor="white",
            plot_bgcolor="white"
        )

        p = f"chart_{i}.png"
        fig.write_image(p, scale=3)

        if os.path.exists(p):
            paths.append(p)

    return paths


# =========================================================
# PDF Generator (PROFESSIONAL GRADE)
# =========================================================
def generate_pdf(text, paths):

    doc = SimpleDocTemplate("Dashlytics_Report.pdf")
    elements = []

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    subtitle_style = styles["Heading2"]

    heading_style = ParagraphStyle(
        "heading",
        parent=styles["Heading2"],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10
    )

    body_style = ParagraphStyle(
        "body",
        parent=styles["BodyText"],
        fontSize=11,
        leading=16
    )

    # -------------------------------
    # Cover Page
    # -------------------------------
    elements.append(Spacer(1, 200))
    elements.append(Paragraph("Dashlytics", title_style))
    elements.append(Spacer(1, 10))
    elements.append(
        Paragraph("Automated Analytics, Intelligent Reporting", subtitle_style)
    )
    elements.append(PageBreak())

    # -------------------------------
    # Strict headings
    # -------------------------------
    headings = [
        "Executive Summary",
        "Data Cleaning",
        "Statistical Analysis",
        "Visualization Insights",
        "Model Evaluation",
        "Business Recommendations",
        "Conclusion"
    ]

    charts_inserted = False

    for line in text.split("\n"):

        clean = line.strip()

        if not clean:
            continue

        # STRICT MATCH ONLY
        if clean.lower() in [h.lower() for h in headings]:

            elements.append(Paragraph(clean, heading_style))

            # Insert charts only once
            if clean.lower() == "visualization insights" and not charts_inserted:

                charts_inserted = True

                for i, p in enumerate(paths):

                    elements.append(Spacer(1, 12))
                    elements.append(Image(p, width=420, height=260))
                    elements.append(Spacer(1, 4))

                    caption = f"Figure {i+1}: Dashboard Visualization"
                    elements.append(Paragraph(caption, body_style))

                    if (i + 1) % 2 == 0:
                        elements.append(PageBreak())

        else:
            elements.append(Paragraph(clean, body_style))

        elements.append(Spacer(1, 6))

    doc.build(elements)



# =========================================================
# UI
# =========================================================
card_start()
generate = st.button("Generate AI Report")
card_end()


# =========================================================
# Generate Flow
# =========================================================
if generate:

    with st.spinner("Generating professional report..."):

        text = generate_ai_text()
        st.session_state["report_text"] = text

        paths = save_images()

        generate_pdf(text, paths)

        st.success("Professional report generated successfully")


# =========================================================
# Preview + Download
# =========================================================
if "report_text" in st.session_state:

    card_start()
    st.subheader("Report Preview")
    st.text_area("", st.session_state["report_text"], height=400)
    card_end()

    with open("Dashlytics_Report.pdf", "rb") as f:
        st.download_button("Download PDF", f, "Dashlytics_Report.pdf")

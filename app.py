import streamlit as st
import streamlit.components.v1 as components
from components import navbar

st.set_page_config(
    page_title="Dashlytics — Intelligent Analytics",
    page_icon="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><rect x='2' y='12' width='4' height='10' rx='1' fill='%234493F8'/><rect x='8' y='7' width='4' height='15' rx='1' fill='%23A371F7'/><rect x='14' y='2' width='4' height='20' rx='1' fill='%234493F8' opacity='.7'/><rect x='20' y='9' width='2' height='13' rx='1' fill='%233FB950'/></svg>",
    layout="wide",
    initial_sidebar_state="collapsed",
)

navbar()

components.html("""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    background: #080A0F;
    color: #E6EDF3;
    font-family: 'Space Grotesk', sans-serif;
    padding: 0 8px 40px;
    overflow-x: hidden;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}
@keyframes floatY {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-6px); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.35; }
}
@keyframes scanline {
    0%   { transform: translateY(-100%); }
    100% { transform: translateY(600%); }
}
@keyframes orbDrift {
    0%,100% { transform: translate(0,0) scale(1); }
    33%     { transform: translate(24px,-16px) scale(1.04); }
    66%     { transform: translate(-16px,12px) scale(0.97); }
}
@keyframes blink {
    0%,100% { opacity: 1; }
    50%      { opacity: 0; }
}

/* ── Hero ── */
.hero-wrap {
    position: relative;
    text-align: center;
    padding: 56px 20px 44px;
    overflow: hidden;
}
.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    pointer-events: none;
    animation: orbDrift 14s ease-in-out infinite;
}
.orb-blue   { width:380px;height:380px;background:rgba(68,147,248,0.08);top:-60px;left:2%; animation-delay:0s; }
.orb-purple { width:300px;height:300px;background:rgba(163,113,247,0.07);top:10px;right:4%; animation-delay:-5s; }
.orb-green  { width:180px;height:180px;background:rgba(63,185,80,0.05);bottom:0;left:46%; animation-delay:-9s; }

.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(68,147,248,0.09);
    border: 1px solid rgba(68,147,248,0.28);
    color: #4493F8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 6px 18px;
    border-radius: 100px;
    margin-bottom: 28px;
    animation: fadeUp 0.6s ease both;
}
.pill-dot {
    width: 6px; height: 6px;
    background: #4493F8;
    border-radius: 50%;
    box-shadow: 0 0 7px #4493F8;
    animation: pulse 2s infinite;
}

.hero-h1 {
    font-size: clamp(38px, 5.5vw, 62px);
    font-weight: 900;
    letter-spacing: -0.045em;
    line-height: 1.02;
    color: #E6EDF3;
    margin-bottom: 20px;
    animation: fadeUp 0.65s 0.08s ease both;
}
.grad {
    background: linear-gradient(120deg, #4493F8 0%, #A371F7 50%, #3FB950 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s linear infinite;
}

.hero-sub {
    font-size: 16px;
    color: #8B949E;
    max-width: 520px;
    margin: 0 auto 44px;
    line-height: 1.7;
    animation: fadeUp 0.65s 0.16s ease both;
}

/* ── Metric strip ── */
.metric-strip {
    display: flex;
    justify-content: center;
    max-width: 580px;
    margin: 0 auto 52px;
    border: 1px solid #21262D;
    border-radius: 14px;
    overflow: hidden;
    animation: fadeUp 0.65s 0.24s ease both;
}
.metric-item {
    flex: 1;
    padding: 18px 10px;
    background: #161B22;
    text-align: center;
    border-right: 1px solid #21262D;
    transition: background 0.2s;
}
.metric-item:last-child { border-right: none; }
.metric-item:hover { background: #1C2333; }
.metric-val {
    font-size: 24px;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 4px;
}
.metric-val.blue   { color: #4493F8; }
.metric-val.purple { color: #A371F7; }
.metric-val.green  { color: #3FB950; }
.metric-val.orange { color: #F0883E; }
.metric-lbl {
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #484F58;
}

/* ── Pipeline ── */
.pipeline {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    max-width: 720px;
    margin: 0 auto 52px;
    animation: fadeUp 0.65s 0.32s ease both;
}
.pipe-step { display:flex;flex-direction:column;align-items:center;gap:8px;flex:1; }
.pipe-icon {
    width: 48px; height: 48px;
    background: #161B22;
    border: 1px solid #21262D;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    transition: all 0.22s;
    animation: floatY 4s ease-in-out infinite;
    cursor: default;
}
.pipe-step:nth-child(1) .pipe-icon { animation-delay:0s;   border-color:rgba(68,147,248,0.35); }
.pipe-step:nth-child(3) .pipe-icon { animation-delay:0.3s; border-color:rgba(163,113,247,0.35); }
.pipe-step:nth-child(5) .pipe-icon { animation-delay:0.6s; border-color:rgba(68,147,248,0.35); }
.pipe-step:nth-child(7) .pipe-icon { animation-delay:0.9s; border-color:rgba(63,185,80,0.35); }
.pipe-step:nth-child(9) .pipe-icon { animation-delay:1.2s; border-color:rgba(240,136,62,0.35); }
.pipe-icon:hover { transform:translateY(-4px) scale(1.1); border-color:#4493F8; box-shadow:0 0 18px rgba(68,147,248,0.25); }
.pipe-label { font-size:10px;font-weight:600;color:#484F58;text-transform:uppercase;letter-spacing:0.1em; }
.pipe-arrow { color:#30363D;font-size:22px;padding-bottom:22px;margin:0 2px;flex-shrink:0; }


/* ── Terminal ── */
.terminal-wrap {
    background: #0D1117;
    border: 1px solid #21262D;
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 44px;
    animation: fadeUp 0.65s 0.5s ease both;
}
.terminal-header {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 10px 16px;
    background: #161B22;
    border-bottom: 1px solid #21262D;
}
.term-dot { width:10px;height:10px;border-radius:50%; }
.term-title { font-size:11px;color:#484F58;font-family:'JetBrains Mono',monospace;margin-left:8px; }
.terminal-body {
    padding: 16px 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    line-height: 2;
    position: relative;
    overflow: hidden;
}
.terminal-body::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(68,147,248,0.3), transparent);
    animation: scanline 3.5s linear infinite;
}
.t-green  { color: #3FB950; }
.t-blue   { color: #4493F8; }
.t-purple { color: #A371F7; }
.t-orange { color: #F0883E; }
.t-muted  { color: #484F58; }
.t-white  { color: #E6EDF3; }
.cursor {
    display: inline-block;
    width: 8px; height: 13px;
    background: #4493F8;
    vertical-align: middle;
    animation: blink 1s steps(1) infinite;
    margin-left: 2px;
}

/* ── Quotes ── */
.quote-strip {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 12px;
    margin-bottom: 44px;
    animation: fadeUp 0.65s 0.6s ease both;
}
.quote-card {
    background: #0D1117;
    border: 1px solid #21262D;
    border-radius: 14px;
    padding: 20px;
    position: relative;
    transition: border-color 0.2s;
}
.quote-card:hover { border-color: #30363D; }
.quote-card::before {
    content: '"';
    position: absolute;
    top: 8px; right: 14px;
    font-size: 52px;
    color: #1C2333;
    font-family: Georgia, serif;
    line-height: 1;
}
.quote-text {
    font-size: 13px;
    color: #8B949E;
    line-height: 1.65;
    margin-bottom: 16px;
    font-style: italic;
}
.quote-author { display:flex;align-items:center;gap:10px; }
.quote-avatar {
    width:30px;height:30px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;
    font-size:14px;flex-shrink:0;
}
.quote-name { font-size:12px;font-weight:700;color:#E6EDF3; }
.quote-role { font-size:11px;color:#484F58;margin-top:1px; }

/* ── Stack chips ── */
.stack-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 44px;
    animation: fadeUp 0.65s 0.7s ease both;
}
.stack-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #161B22;
    border: 1px solid #21262D;
    border-radius: 100px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 600;
    color: #8B949E;
    transition: all 0.2s;
    cursor: default;
}
.stack-chip:hover { border-color:#30363D;color:#E6EDF3;background:#1C2333; }

/* ── CTA ── */
.cta-wrap {
    text-align: center;
    padding: 52px 20px;
    background: linear-gradient(135deg, rgba(68,147,248,0.04) 0%, rgba(163,113,247,0.04) 100%);
    border: 1px solid #21262D;
    border-radius: 20px;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.65s 0.8s ease both;
}
.cta-glow {
    position: absolute;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(68,147,248,0.07), transparent 70%);
    top: 50%; left: 50%;
    transform: translate(-50%,-50%);
    pointer-events: none;
}
.cta-eyebrow { font-size:11px;font-weight:700;letter-spacing:0.16em;text-transform:uppercase;color:#4493F8;margin-bottom:12px; }
.cta-heading { font-size:clamp(26px,3.5vw,38px);font-weight:800;letter-spacing:-0.04em;color:#E6EDF3;margin-bottom:10px;line-height:1.1; }
.cta-sub { font-size:14px;color:#8B949E;line-height:1.7;max-width:460px;margin:0 auto 8px; }
</style>
</head>
<body>

<!-- HERO -->
<div class="hero-wrap">
    <div class="orb orb-blue"></div>
    <div class="orb orb-purple"></div>
    <div class="orb orb-green"></div>
    <div><span class="hero-pill"><span class="pill-dot"></span> AI-Powered Analytics Suite </span></div>
    <div class="hero-h1">From Raw Data to<br><span class="grad">Intelligent Insights</span></div>
    <p class="hero-sub">Upload any CSV and receive automated cleaning, statistical analysis, ML benchmarks, interactive dashboards, and an AI-authored report — all in one seamless pipeline.</p>
    <div class="metric-strip">
        <div class="metric-item"><div class="metric-val blue">3</div><div class="metric-lbl">ML Models</div></div>
        <div class="metric-item"><div class="metric-val purple">5</div><div class="metric-lbl">Chart Types</div></div>
        <div class="metric-item"><div class="metric-val green">Auto</div><div class="metric-lbl">Cleaning</div></div>
        <div class="metric-item"><div class="metric-val orange">PDF</div><div class="metric-lbl">AI Report</div></div>
    </div>
    <div class="pipeline">
        <div class="pipe-step"><div class="pipe-icon">&#128194;</div><div class="pipe-label">Upload</div></div>
        <div class="pipe-arrow">&rsaquo;</div>
        <div class="pipe-step"><div class="pipe-icon">&#129529;</div><div class="pipe-label">Clean</div></div>
        <div class="pipe-arrow">&rsaquo;</div>
        <div class="pipe-step"><div class="pipe-icon">&#128202;</div><div class="pipe-label">Analyse</div></div>
        <div class="pipe-arrow">&rsaquo;</div>
        <div class="pipe-step"><div class="pipe-icon">&#129302;</div><div class="pipe-label">Model</div></div>
        <div class="pipe-arrow">&rsaquo;</div>
        <div class="pipe-step"><div class="pipe-icon">&#128196;</div><div class="pipe-label">Report</div></div>
    </div>
</div>

<!-- CTA -->
<div class="cta-wrap">
    <div class="cta-glow"></div>
    <div class="cta-eyebrow">Ready to begin?</div>
    <div class="cta-heading">Start your first analysis</div>
    <p class="cta-sub">Upload a CSV in the sidebar and the entire pipeline starts automatically.<br>No configuration. No code. Just insights.</p>
</div>

</body>
</html>
""", height=1000, scrolling=False)
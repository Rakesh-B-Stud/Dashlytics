import streamlit as st
import os
from style import load_css


# ============================================================
# AUTO-INJECT CSS ON EVERY PAGE
# ============================================================
def _inject_css():
    load_css()


# ============================================================
# NAVBAR
# ============================================================
def navbar():
    _inject_css()

    # ── Inject JS directly into the page (NOT via components.html iframe)
    # This runs in the real document so it can reach the sidebar toggle button
    st.markdown("""
    <script>
    (function() {
        function setupSidebar() {
            var btn = document.querySelector('[data-testid="collapsedControl"]');
            if (!btn) { setTimeout(setupSidebar, 200); return; }

            // --- 1. Inject hamburger SVG if not already there ---
            if (!btn.querySelector('svg.dash-hamburger')) {
                // Hide everything else inside the button
                Array.from(btn.children).forEach(function(child) {
                    child.style.display = 'none';
                });

                var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                svg.setAttribute('class', 'dash-hamburger');
                svg.setAttribute('viewBox', '0 0 18 14');
                svg.setAttribute('width', '18');
                svg.setAttribute('height', '14');
                svg.setAttribute('fill', 'none');
                svg.style.cssText = 'display:block;flex-shrink:0;pointer-events:none;';

                [[0,1],[6,7],[12,13]].forEach(function(y) {
                    var line = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                    line.setAttribute('x', '0');
                    line.setAttribute('y', String(y[0]));
                    line.setAttribute('width', '18');
                    line.setAttribute('height', '2');
                    line.setAttribute('rx', '1');
                    line.setAttribute('fill', '#8B949E');
                    svg.appendChild(line);
                });
                btn.appendChild(svg);
            }

            // --- 2. Close sidebar when clicking outside ---
            document.addEventListener('click', function(e) {
                var sidebar = document.querySelector('[data-testid="stSidebar"]');
                var toggle  = document.querySelector('[data-testid="collapsedControl"]');
                if (!sidebar || !toggle) return;

                // Streamlit marks sidebar open with aria-expanded="true"
                var isOpen = sidebar.getAttribute('aria-expanded') === 'true';
                if (!isOpen) return;

                var clickedSidebar = sidebar.contains(e.target);
                var clickedToggle  = toggle.contains(e.target);
                if (!clickedSidebar && !clickedToggle) {
                    toggle.click();
                }
            }, true);
        }

        // Run after DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', setupSidebar);
        } else {
            setupSidebar();
        }
    })();
    </script>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="navbar">
        <div class="navbar-brand">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <rect x="2" y="12" width="4" height="10" rx="1" fill="#4493F8"/>
                <rect x="8" y="7"  width="4" height="15" rx="1" fill="#A371F7"/>
                <rect x="14" y="2" width="4" height="20" rx="1" fill="#4493F8" opacity="0.7"/>
                <rect x="20" y="9" width="2" height="13" rx="1" fill="#3FB950"/>
            </svg>
            Dashlytics
            <div class="dot"></div>
        </div>
        <span class="navbar-tagline">Automated Analytics &nbsp;&middot;&nbsp; Intelligent Reporting</span>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================
def sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding: 8px 4px 20px; border-bottom: 1px solid #21262D; margin-bottom: 16px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                    <rect x="2" y="12" width="4" height="10" rx="1" fill="#4493F8"/>
                    <rect x="8" y="7"  width="4" height="15" rx="1" fill="#A371F7"/>
                    <rect x="14" y="2" width="4" height="20" rx="1" fill="#4493F8" opacity="0.7"/>
                    <rect x="20" y="9" width="2" height="13" rx="1" fill="#3FB950"/>
                </svg>
                <span style="font-size:15px; font-weight:700; color:#E6EDF3; letter-spacing:-0.03em;">Dashlytics</span>
            </div>
            <span style="font-size:11px; color:#484F58; font-family:'JetBrains Mono',monospace;">v1.0 &middot; Analytics Suite</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="font-size:10px; font-weight:600; text-transform:uppercase; letter-spacing:0.12em;
                    color:#484F58; padding: 0 4px 8px;">Navigation</div>
        """, unsafe_allow_html=True)


# ============================================================
# PAGE HEADER
# ============================================================
def header(title: str, subtitle: str = ""):
    sub_html = f'<p style="margin:0;font-size:13px;color:#484F58;">{subtitle}</p>' if subtitle else ""
    st.markdown(f"""
    <div class="page-header">
        <h2>{title}</h2>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# CARD WRAPPERS
# ============================================================
def card_start():
    st.markdown('<div class="card">', unsafe_allow_html=True)

def card_end():
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# KPI CARD
# ============================================================
def kpi(label: str, value, col=None):
    html = f"""
    <div class="kpi-card">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """
    if col:
        col.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown(html, unsafe_allow_html=True)


# ============================================================
# SECTION DIVIDER
# ============================================================
def section_divider():
    st.markdown('<hr style="border-color:#21262D; margin:24px 0;">', unsafe_allow_html=True)


# ============================================================
# STATUS BADGE
# ============================================================
def badge(text: str, color: str = "blue"):
    colors = {
        "blue":   ("rgba(68,147,248,0.12)",  "rgba(68,147,248,0.35)",  "#4493F8"),
        "green":  ("rgba(63,185,80,0.12)",   "rgba(63,185,80,0.3)",    "#3FB950"),
        "purple": ("rgba(163,113,247,0.12)", "rgba(163,113,247,0.3)",  "#A371F7"),
        "orange": ("rgba(240,136,62,0.12)",  "rgba(240,136,62,0.3)",   "#F0883E"),
    }
    bg, border, fg = colors.get(color, colors["blue"])
    st.markdown(f"""
    <span style="display:inline-flex;align-items:center;background:{bg};border:1px solid {border};
                 color:{fg};font-size:11px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;
                 padding:4px 12px;border-radius:100px;">{text}</span>
    """, unsafe_allow_html=True)


# ============================================================
# PAGE NAVIGATOR — pipeline progress bar + next button
# ============================================================
PIPELINE_STEPS = [
    ("Upload",    "pages/2_Upload.py"),
    ("Cleaning",  "pages/3_Cleaning.py"),
    ("Analysis",  "pages/4_Analysis.py"),
    ("Models",    "pages/5_Models.py"),
    ("Dashboard", "pages/6_Dashboard.py"),
    ("Report",    "pages/7_Report.py"),
]

def page_nav(current_step: int, next_page: str = None, next_label: str = None):
    """
    Render a bottom pipeline progress bar + optional Next button.
    current_step: 1-based index matching PIPELINE_STEPS (1=Upload…6=Report). 0 for welcome.
    next_page:    path string for st.switch_page, e.g. "pages/3_Cleaning.py"
    next_label:   override button label text (default "Continue →")
    """
    pills_html = ""
    for i, (label, _) in enumerate(PIPELINE_STEPS, start=1):
        if i < current_step:
            pills_html += (
                f'<span style="display:inline-flex;align-items:center;gap:4px;font-size:11px;'
                f'font-weight:600;color:#3FB950;background:rgba(63,185,80,0.1);'
                f'border:1px solid rgba(63,185,80,0.25);padding:3px 10px;border-radius:100px;">'
                f'&#10003; {label}</span>'
            )
        elif i == current_step:
            pills_html += (
                f'<span style="display:inline-flex;align-items:center;gap:4px;font-size:11px;'
                f'font-weight:600;color:#4493F8;background:rgba(68,147,248,0.12);'
                f'border:1px solid rgba(68,147,248,0.35);padding:3px 10px;border-radius:100px;">'
                f'&#11044; {label}</span>'
            )
        else:
            pills_html += (
                f'<span style="display:inline-flex;align-items:center;gap:4px;font-size:11px;'
                f'font-weight:500;color:#484F58;background:#161B22;'
                f'border:1px solid #21262D;padding:3px 10px;border-radius:100px;">'
                f'{label}</span>'
            )
        if i < len(PIPELINE_STEPS):
            pills_html += '<span style="color:#30363D;font-size:10px;margin:0 2px;">&#8250;</span>'

    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;
                padding:14px 20px;background:#161B22;border:1px solid #21262D;border-radius:12px;
                margin-top:28px;">
        <div style="display:flex;align-items:center;gap:6px;flex-wrap:wrap;">
            {pills_html}
        </div>
        <span style="font-size:11px;color:#484F58;font-family:'JetBrains Mono',monospace;flex-shrink:0;">
            Step {current_step} of {len(PIPELINE_STEPS)}
        </span>
    </div>
    """, unsafe_allow_html=True)

    if next_page:
        btn_label = next_label or "Continue &rarr;"
        _c1, _c2, col_btn = st.columns([4, 1, 1])
        with col_btn:
            if st.button(btn_label.replace("&rarr;", "→"), use_container_width=True, key=f"nav_next_{current_step}"):
                st.switch_page(next_page)
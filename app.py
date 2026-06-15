import streamlit as st

st.set_page_config(
    page_title="IPL Analytics Hub",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed" # Hide sidebar on home page for clean look
)

# ── Global CSS for Home Page ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0d1117; color: #e6edf3; }
.block-container { padding: 3rem 2.5rem !important; max-width: 1200px; }

/* Hide default Streamlit chrome */
#MainMenu, footer { visibility: hidden; }

/* ── Custom Classes ── */
.title-box { text-align: center; margin-bottom: 3rem; }
.main-title { font-family: 'Space Grotesk', sans-serif; font-size: 3.5rem; font-weight: 700; background: linear-gradient(90deg, #f5a623, #e8651a); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; }
.sub-title { font-size: 1.2rem; color: #8b949e; font-weight: 400; }
.author { font-size: 0.9rem; color: #4a9eff; font-weight: 600; margin-top: 1rem; letter-spacing: 1px; text-transform: uppercase; }

.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; margin-bottom: 3rem; }
.kpi-card { background: #161b22; border: 1px solid #21262d; border-radius: 12px; padding: 1.5rem; text-align: center; transition: transform 0.2s; }
.kpi-card:hover { border-color: #f5a623; transform: translateY(-3px); }
.kpi-val { font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: #e6edf3; }
.kpi-label { font-size: 0.8rem; color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 0.5rem; }

.section-card { background: #161b22; border: 1px solid #21262d; border-radius: 12px; padding: 2rem; margin-bottom: 2rem; }
.section-title { font-family: 'Space Grotesk', sans-serif; font-size: 1.5rem; color: #e6edf3; margin-bottom: 1.5rem; border-bottom: 1px solid #21262d; padding-bottom: 0.5rem; }

.tech-badge { display: inline-block; background: #21262d; border: 1px solid #30363d; padding: 0.4rem 1rem; border-radius: 20px; font-size: 0.85rem; font-weight: 500; color: #c9d1d9; margin: 0.3rem 0.3rem 0 0; }

.flow-box { display: flex; align-items: center; justify-content: space-between; background: #0d1117; padding: 1.5rem; border-radius: 8px; border: 1px dashed #30363d; overflow-x: auto; }
.flow-step { text-align: center; min-width: 120px; }
.flow-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }
.flow-text { font-size: 0.85rem; font-weight: 600; color: #8b949e; }
.flow-arrow { color: #f5a623; font-weight: bold; }
            
/* Universal Footer Styling */
.footer { 
    margin-top: 3rem; 
    padding-top: 1.5rem; 
    border-top: 1px solid #21262d; 
    text-align: center; 
}
.footer-links { 
    display: flex; 
    justify-content: center; 
    gap: 1.5rem; 
    margin-bottom: 0.75rem; 
}
.footer-link { 
    display: inline-flex; 
    align-items: center; 
    gap: 0.4rem; 
    color: #8b949e; 
    text-decoration: none; 
    font-size: 0.85rem; 
    font-weight: 500; 
    padding: 0.4rem 1rem; 
    border: 1px solid #21262d; 
    border-radius: 20px; 
    transition: all 0.2s; 
}
.footer-link:hover { 
    color: #f5a623; 
    border-color: #f5a623; 
    background-color: #161b22;
}
.footer-copy { 
    font-size: 0.75rem; 
    color: #484f58; 
}
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div class="title-box">
    <div class="main-title">IPL Analytics Intelligence System</div>
    <div class="sub-title">End-to-end Machine Learning & Business Intelligence Platform</div>
    <div class="author">Built by Yuvak Ratnaparkhi</div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ──
st.markdown("""
<div class="kpi-grid">
    <div class="kpi-card"><div class="kpi-val">1090+</div><div class="kpi-label">Matches Analyzed</div></div>
    <div class="kpi-card"><div class="kpi-val">200K+</div><div class="kpi-label">Deliveries Processed</div></div>
    <div class="kpi-card"><div class="kpi-val">14</div><div class="kpi-label">IPL Seasons</div></div>
    <div class="kpi-card"><div class="kpi-val" style="color:#28a745;">56.4%</div><div class="kpi-label">ML Accuracy</div></div>
</div>
""", unsafe_allow_html=True)

col_about, col_arch = st.columns([1, 1.2], gap="large")

# ── About Section ──
with col_about:
    st.markdown("""
    <div class="section-card" style="height: 100%;">
        <div class="section-title">About the Project</div>
        <p style="color: #c9d1d9; line-height: 1.6; font-size: 0.95rem; margin-bottom: 1.5rem;">
            A full-stack data engineering and machine learning pipeline that transforms raw IPL cricket datasets into actionable insights. The system predicts match outcomes using historical win rates, toss decisions, and venue dynamics.
        </p>
        <div style="font-size: 0.8rem; color: #8b949e; text-transform: uppercase; margin-bottom: 0.5rem; font-weight:600;">Tech Stack</div>
        <div>
            <span class="tech-badge">🐘 PostgreSQL</span>
            <span class="tech-badge">🐍 Python</span>
            <span class="tech-badge">🤖 XGBoost</span>
            <span class="tech-badge">📊 Power BI</span>
            <span class="tech-badge">👑 Streamlit</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Architecture Diagram ──
with col_arch:
    st.markdown("""
    <div class="section-card" style="height: 100%;">
        <div class="section-title">System Architecture</div>
        <div class="flow-box">
            <div class="flow-step"><div class="flow-icon">📄</div><div class="flow-text">Raw CSV</div></div>
            <div class="flow-arrow">→</div>
            <div class="flow-step"><div class="flow-icon">🐘</div><div class="flow-text">PostgreSQL</div></div>
            <div class="flow-arrow">→</div>
            <div class="flow-step"><div class="flow-icon">🐍</div><div class="flow-text">Python / Pandas</div></div>
            <div class="flow-arrow">→</div>
            <div class="flow-step"><div class="flow-icon">🤖</div><div class="flow-text">XGBoost ML</div></div>
            <div class="flow-arrow">→</div>
            <div class="flow-step"><div class="flow-icon">💻</div><div class="flow-text">Streamlit UI</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Navigation Buttons ──
st.markdown('<div class="section-title" style="margin-top: 1rem;">Explore Modules</div>', unsafe_allow_html=True)

n1, n2, n3, n4 = st.columns(4)
with n1: st.page_link("pages/1_Predictor.py", label="🚀 IPL Match Predictor", use_container_width=True)
with n2: st.page_link("pages/2_Head_to_Head.py", label="⚔️ Head-to-Head Analyzer", use_container_width=True)
with n3: st.page_link("pages/3_Team_Analytics.py", label="📈 Team Analytics", use_container_width=True)
with n4: st.page_link("pages/4_Venue_Intelligence.py", label="🏟️ Venue Intelligence", use_container_width=True)

# ── Footer ──
st.markdown("""
<div class="footer">
    <div class="footer-links">
        <a class="footer-link" href="https://www.linkedin.com/in/yuvak-ratnaparkhi" target="_blank">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
            LinkedIn
        </a>
        <a class="footer-link" href="https://github.com/yuvak-ratnaparkhi/IPL-Performance-Analytics-System" target="_blank">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            GitHub
        </a>
    </div>
    <div class="footer-copy">Built by Yuvak Ratnaparkhi · IPL Performance Analytics Intelligence System</div>
</div>
""", unsafe_allow_html=True)
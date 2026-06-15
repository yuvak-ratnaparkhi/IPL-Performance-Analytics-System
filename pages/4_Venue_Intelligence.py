import streamlit as st
import pandas as pd
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Venue Intelligence | IPL Hub",
    page_icon="🏟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# GLOBAL CSS — Dark Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0d1117; color: #e6edf3; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #161b22 0%, #0d1117 100%); border-right: 1px solid #21262d; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem 2.5rem !important; }

/* Headers */
.page-header { font-family: 'Space Grotesk', sans-serif; font-size: 2.2rem; font-weight: 700; color: #f5a623; margin-bottom: 0.2rem; }
.page-sub { font-size: 0.95rem; color: #8b949e; margin-bottom: 2rem; }

/* KPI Cards */
.kpi-container { display: flex; gap: 1rem; margin-bottom: 2rem; }
.kpi-card { flex: 1; background: #161b22; border: 1px solid #21262d; border-radius: 12px; padding: 1.5rem; text-align: center; }
.kpi-title { font-size: 0.75rem; font-weight: 600; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem; }
.kpi-val { font-family: 'Space Grotesk', sans-serif; font-size: 2.2rem; font-weight: 700; color: #e6edf3; }

/* Section Cards */
.section-card { background: #161b22; border: 1px solid #21262d; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; height: 100%; }
.section-title { font-size: 0.9rem; font-weight: 600; color: #e6edf3; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1.2rem; border-bottom: 1px solid #21262d; padding-bottom: 0.5rem; }

/* AI Insight */
.ai-card { background: linear-gradient(135deg, #161b22, #12181f); border: 1px solid #30363d; border-left: 3px solid #f5a623; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; }
.ai-label { font-size: 0.7rem; font-weight: 700; color: #f5a623; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.5rem; }
.ai-text { font-size: 0.95rem; color: #c9d1d9; font-style: italic; }

/* Universal Footer Styling */
.footer { margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #21262d; text-align: center; }
.footer-links { display: flex; justify-content: center; gap: 1.5rem; margin-bottom: 0.75rem; }
.footer-link { display: inline-flex; align-items: center; gap: 0.4rem; color: #8b949e; text-decoration: none; font-size: 0.85rem; font-weight: 500; padding: 0.4rem 1rem; border: 1px solid #21262d; border-radius: 20px; transition: all 0.2s; }
.footer-link:hover { color: #f5a623; border-color: #f5a623; background-color: #161b22; }
.footer-copy { font-size: 0.75rem; color: #484f58; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base, "machine_learning", "dataset", "match_winner_dataset.csv")
    df = pd.read_csv(csv_path)
    return df

try:
    df = load_data()
    # Normalize naming variations if necessary, clean venues list
    venues = sorted(list(df['venue'].dropna().unique()))
except Exception as e:
    st.error("⚠️ Dataset not found. Please ensure match_winner_dataset.csv is in the correct directory.")
    st.stop()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0 1.5rem; border-bottom: 1px solid #21262d; margin-bottom: 1.5rem;">
        <div style="font-size:1.4rem; font-weight:700; color:#f5a623; font-family:'Space Grotesk',sans-serif;">🏟️ Venue Intel</div>
        <div style="font-size:0.75rem; color:#8b949e; margin-top:0.25rem;">Stadium Analytics Module</div>
    </div>
    """, unsafe_allow_html=True)

    selected_venue = st.selectbox("Select Stadium", venues, index=0)

# ─────────────────────────────────────────────
# DATA PROCESSING
# ─────────────────────────────────────────────
venue_df = df[df['venue'] == selected_venue].copy()
total_matches = len(venue_df)

if total_matches > 0:
    # 1. Toss Decision Analysis
    # Standardizing expected column entries ('bat', 'field')
    toss_bat = len(venue_df[venue_df['toss_decision'].str.lower() == 'bat'])
    toss_field = len(venue_df[venue_df['toss_decision'].str.lower() == 'field'])
    
    toss_bat_pct = (toss_bat / total_matches * 100) if total_matches > 0 else 0
    toss_field_pct = (toss_field / total_matches * 100) if total_matches > 0 else 0

    # 2. Defending vs Chasing Analytics
    # If toss winner chooses bat and wins match OR toss winner chooses field and loses match -> Team batting first won
    bat_first_wins = len(venue_df[
        ((venue_df['toss_decision'].str.lower() == 'bat') & (venue_df['toss_winner'] == venue_df['winner'])) |
        ((venue_df['toss_decision'].str.lower() == 'field') & (venue_df['toss_winner'] != venue_df['winner']))
    ])
    chasing_wins = total_matches - bat_first_wins
    
    bat_first_pct = (bat_first_wins / total_matches * 100) if total_matches > 0 else 0
    chasing_pct = (chasing_wins / total_matches * 100) if total_matches > 0 else 0
else:
    toss_bat_pct = toss_field_pct = bat_first_pct = chasing_pct = 0

# ─────────────────────────────────────────────
# MAIN UI
# ─────────────────────────────────────────────
st.markdown('<div class="page-header">🏟️ Venue Intelligence</div>', unsafe_allow_html=True)
st.markdown(f'<div class="page-sub">Ground parameters, bias vectors, and strategic history for <strong>{selected_venue}</strong></div>', unsafe_allow_html=True)

if total_matches == 0:
    st.warning(f"No historical records found for the venue: {selected_venue}")
    st.stop()

# ── KPI Cards ──
bias_label = "Neutral"
bias_color = "#e6edf3"
if chasing_pct > 54:
    bias_label = "Chasing Bias (Dew Factor)"
    bias_color = "#4a9eff"
elif bat_first_pct > 54:
    bias_label = "Defending Bias (Dry Surface)"
    bias_color = "#28a745"

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-title">Total Matches Tracked</div>
        <div class="kpi-val">{total_matches}</div>
    </div>
    <div class="kpi-card" style="border-bottom: 3px solid #28a745;">
        <div class="kpi-title">Batting First Wins</div>
        <div class="kpi-val" style="color: #28a745;">{bat_first_wins}</div>
    </div>
    <div class="kpi-card" style="border-bottom: 3px solid #4a9eff;">
        <div class="kpi-title">Chasing Wins</div>
        <div class="kpi-val" style="color: #4a9eff;">{chasing_wins}</div>
    </div>
    <div class="kpi-card" style="border-bottom: 3px solid {bias_color};">
        <div class="kpi-title">Ground Strategic Bias</div>
        <div class="kpi-val" style="color: {bias_color}; font-size: 1.4rem; padding-top: 0.6rem;">{bias_label}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Analytical Breakdown Columns ──
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-card"><div class="section-title">📊 Match Outcome Dynamics</div>', unsafe_allow_html=True)
    outcome_chart_data = pd.DataFrame({
        "Match Outcome": ["Batting First Wins", "Chasing Wins"],
        "Percentage": [bat_first_pct, chasing_pct]
    }).set_index("Match Outcome")
    st.bar_chart(outcome_chart_data, y="Percentage", height=240, color="#4a9eff")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card"><div class="section-title">🪙 Toss Captain Decisions</div>', unsafe_allow_html=True)
    toss_chart_data = pd.DataFrame({
        "Decision Option": ["Opted to Bat", "Opted to Field"],
        "Selection Ratio %": [toss_bat_pct, toss_field_pct]
    }).set_index("Decision Option")
    st.bar_chart(toss_chart_data, y="Selection Ratio %", height=240, color="#f5a623")
    st.markdown('</div>', unsafe_allow_html=True)

# ── AI Strategic Commentary ──
dominant_toss_choice = "Fielding" if toss_field_pct > toss_bat_pct else "Batting"
ai_strategy = (
    f"Statistical mapping shows {selected_venue} experiences a strong trend favoring teams **{ 'Chasing' if chasing_pct > bat_first_pct else 'Defending' }** "
    f"({max(chasing_pct, bat_first_pct):.1f}% win rate). Captains winning the toss heavily gravitate toward **{dominant_toss_choice}** "
    f"({max(toss_field_pct, toss_bat_pct):.1f}% optimization rate), aligning cleanly with modern predictive modeling configurations."
)

st.markdown(f"""
<div class="ai-card">
    <div class="ai-label">🤖 AI Tactical Surface Analysis</div>
    <div class="ai-text">"{ai_strategy}"</div>
</div>
""", unsafe_allow_html=True)

# ── Universal Footer ──
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
import streamlit as st
import pandas as pd
import os
import requests

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="H2H Analyzer | IPL Analytics",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# GLOBAL CSS — Dark IPL Theme
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
.kpi-container { display: flex; gap: 1.5rem; margin-bottom: 2rem; }
.kpi-card { flex: 1; background: #161b22; border: 1px solid #21262d; border-radius: 12px; padding: 1.5rem; text-align: center; }
.kpi-title { font-size: 0.8rem; font-weight: 600; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem; }
.kpi-val { font-family: 'Space Grotesk', sans-serif; font-size: 2.5rem; font-weight: 700; color: #e6edf3; }
.kpi-highlight-t1 { color: #f5a623; }
.kpi-highlight-t2 { color: #4a9eff; }

/* Win % Bar */
.bar-container { background: #161b22; border: 1px solid #21262d; border-radius: 12px; padding: 2rem; margin-bottom: 2rem; }
.bar-labels { display: flex; justify-content: space-between; margin-bottom: 0.75rem; font-weight: 600; font-size: 1.1rem; }
.bar-track { display: flex; height: 16px; border-radius: 8px; overflow: hidden; background: #21262d; }
.bar-t1 { background: linear-gradient(90deg, #f5a623, #e8651a); transition: width 0.8s ease; }
.bar-t2 { background: linear-gradient(90deg, #4a9eff, #0969da); transition: width 0.8s ease; }

/* Table Styling */
.table-container { background: #161b22; border: 1px solid #21262d; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; }
.custom-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem; }
.custom-table th { color: #8b949e; font-weight: 600; padding: 1rem 0.5rem; border-bottom: 1px solid #30363d; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.5px;}
.custom-table td { padding: 1rem 0.5rem; border-bottom: 1px solid #21262d; color: #c9d1d9; }
.custom-table tr:last-child td { border-bottom: none; }
.winner-badge { background: rgba(40,167,69,0.15); color: #28a745; padding: 0.2rem 0.6rem; border-radius: 12px; font-weight: 600; font-size: 0.8rem; border: 1px solid rgba(40,167,69,0.3); }

/* AI Insight */
.ai-card { background: linear-gradient(135deg, #161b22, #12181f); border: 1px solid #30363d; border-left: 3px solid #9b59b6; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; }
.ai-label { font-size: 0.7rem; font-weight: 700; color: #9b59b6; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.5rem; }
.ai-text { font-size: 0.95rem; color: #c9d1d9; font-style: italic; }

/* Footer */
.footer { margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #21262d; text-align: center; }
.footer-links { display: flex; justify-content: center; gap: 1.5rem; margin-bottom: 0.75rem; }
.footer-link { display: inline-flex; align-items: center; gap: 0.4rem; color: #8b949e; text-decoration: none; font-size: 0.85rem; font-weight: 500; padding: 0.4rem 1rem; border: 1px solid #21262d; border-radius: 20px; transition: all 0.2s; }
.footer-link:hover { color: #f5a623; border-color: #f5a623; }
.footer-copy { font-size: 0.75rem; color: #484f58; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD DATA DYNAMICALLY
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base, "machine_learning", "dataset", "match_winner_dataset.csv")
    df = pd.read_csv(csv_path)
    return df

try:
    df = load_data()
    # Dynamically extract all unique teams and seasons
    teams = sorted(list(set(df['team1']).union(set(df['team2']))))
    seasons = ["All Time"] + sorted(list(df['season'].unique()), reverse=True)
except Exception as e:
    st.error(f"⚠️ Could not load dataset. Ensure match_winner_dataset.csv is in the correct folder. Error: {e}")
    st.stop()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0 1.5rem; border-bottom: 1px solid #21262d; margin-bottom: 1.5rem;">
        <div style="font-size:1.4rem; font-weight:700; color:#f5a623; font-family:'Space Grotesk',sans-serif;">⚔️ H2H Analyzer</div>
        <div style="font-size:0.75rem; color:#8b949e; margin-top:0.25rem;">Historical Rivalry Engine</div>
    </div>
    """, unsafe_allow_html=True)

    team1 = st.selectbox("Team A", teams, index=5)
    team2_options = [t for t in teams if t != team1]
    team2 = st.selectbox("Team B", team2_options, index=0)
    selected_season = st.selectbox("Season Filter", seasons)

# ─────────────────────────────────────────────
# DATA PROCESSING
# ─────────────────────────────────────────────
# Filter matches where these two teams played each other
h2h_df = df[((df['team1'] == team1) & (df['team2'] == team2)) | ((df['team1'] == team2) & (df['team2'] == team1))].copy()

# Apply season filter if necessary
if selected_season != "All Time":
    h2h_df = h2h_df[h2h_df['season'] == selected_season]

# Sort by most recent first (assuming dataset is generally chronological or we can sort by index/date)
h2h_df = h2h_df.sort_index(ascending=False)

# Calculate Metrics
total_matches = len(h2h_df)
t1_wins = len(h2h_df[h2h_df['winner'] == team1])
t2_wins = len(h2h_df[h2h_df['winner'] == team2])
draws = total_matches - t1_wins - t2_wins

# ─────────────────────────────────────────────
# MAIN UI
# ─────────────────────────────────────────────
st.markdown('<div class="page-header">⚔️ Head-to-Head Analyzer</div>', unsafe_allow_html=True)
st.markdown(f'<div class="page-sub">Historical matchup analytics for <strong>{team1}</strong> vs <strong>{team2}</strong> ({selected_season})</div>', unsafe_allow_html=True)

if total_matches == 0:
    st.markdown(f"""
    <div style="background: rgba(255,193,7,0.08); border: 1px solid rgba(255,193,7,0.3); border-radius: 12px; padding: 2rem; text-align: center; margin-top: 2rem;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">📭</div>
        <div style="font-size: 1.1rem; color: #ffc107; font-weight: 600; margin-bottom: 0.5rem;">No Matches Found</div>
        <div style="color: #8b949e; font-size: 0.9rem;">There is no recorded match data between these two teams for the selected season.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    # ── KPI Cards ──
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-title">Total Encounters</div>
            <div class="kpi-val">{total_matches}</div>
        </div>
        <div class="kpi-card" style="border-bottom: 3px solid #f5a623;">
            <div class="kpi-title">{team1} Wins</div>
            <div class="kpi-val kpi-highlight-t1">{t1_wins}</div>
        </div>
        <div class="kpi-card" style="border-bottom: 3px solid #4a9eff;">
            <div class="kpi-title">{team2} Wins</div>
            <div class="kpi-val kpi-highlight-t2">{t2_wins}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Win % Bar Chart ──
    t1_pct = (t1_wins / total_matches) * 100 if total_matches > 0 else 50
    t2_pct = (t2_wins / total_matches) * 100 if total_matches > 0 else 50

    st.markdown(f"""
    <div class="bar-container">
        <div class="kpi-title" style="margin-bottom: 1.5rem;">Historical Dominance</div>
        <div class="bar-labels">
            <span style="color: #f5a623;">{team1} ({t1_pct:.1f}%)</span>
            <span style="color: #4a9eff;">{team2} ({t2_pct:.1f}%)</span>
        </div>
        <div class="bar-track">
            <div class="bar-t1" style="width: {t1_pct}%;"></div>
            <div class="bar-t2" style="width: {t2_pct}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── AI Insight ──
    leader = team1 if t1_wins > t2_wins else (team2 if t2_wins > t1_wins else "Neither team")
    margin = abs(t1_wins - t2_wins)
    insight_text = f"Based on historical data, {leader} holds the edge in this rivalry with a lead of {margin} match{'es' if margin != 1 else ''}. "
    if draws > 0:
        insight_text += f"Interestingly, {draws} match{'es' if draws > 1 else ''} ended in a no-result or tie."
    if t1_wins == t2_wins:
        insight_text = f"This is one of the tightest rivalries in the IPL. Both teams are deadlocked at {t1_wins} wins apiece."

    st.markdown(f"""
    <div class="ai-card">
        <div class="ai-label">🤖 AI H2H Insight</div>
        <div class="ai-text">"{insight_text}"</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Last 5 Meetings Table ──
    st.markdown('<div class="kpi-title" style="margin-bottom: 1rem;">Recent Encounters (Last 5)</div>', unsafe_allow_html=True)
    
    last_5 = h2h_df.head(5)
    table_rows = ""
    for _, row in last_5.iterrows():
        winner = str(row.get('winner', 'N/A'))
        venue = str(row.get('venue', 'N/A'))
        season = str(row.get('season', 'N/A'))
        
        # Format winner nicely
        if winner == team1:
            win_display = f'<span style="color:#f5a623; font-weight:600;">{winner}</span>'
        elif winner == team2:
            win_display = f'<span style="color:#4a9eff; font-weight:600;">{winner}</span>'
        else:
            win_display = f'<span style="color:#8b949e;">{winner}</span>'

# Removed indentation so Streamlit doesn't render it as a code block!
        table_rows += f"<tr><td>{season}</td><td>{venue}</td><td>{win_display}</td></tr>"

    st.markdown(f"""
    <div class="table-container">
        <table class="custom-table">
            <thead>
                <tr>
                    <th>Season</th>
                    <th>Venue</th>
                    <th>Winner</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div class="footer">
    <div class="footer-links">
        <a class="footer-link" href="https://www.linkedin.com/in/yuvak-ratnaparkhi" target="_blank">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
            LinkedIn
        </a>
        <a class="footer-link" href="https://github.com/yuvak-ratnaparkhi/IPL-Performance-Analytics-System" target="_blank">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            GitHub
        </a>
    </div>
    <div class="footer-copy">Built by Yuvak Ratnaparkhi · IPL Performance Analytics Intelligence System</div>
</div>
""", unsafe_allow_html=True)
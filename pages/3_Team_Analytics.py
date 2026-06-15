import streamlit as st
import pandas as pd
import json
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Team Analytics | IPL Hub",
    page_icon="📈",
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

/* Player Tables */
.player-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.85rem; }
.player-table th { color: #8b949e; font-weight: 600; padding: 0.75rem 0.5rem; border-bottom: 1px solid #30363d; text-transform: uppercase; font-size: 0.7rem; letter-spacing: 0.5px;}
.player-table td { padding: 0.75rem 0.5rem; border-bottom: 1px solid #21262d; color: #c9d1d9; }
.player-name { font-weight: 600; color: #4a9eff; }

/* Footer */
.footer { margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #21262d; text-align: center; }
.footer-links { display: flex; justify-content: center; gap: 1.5rem; margin-bottom: 0.75rem; }
.footer-link { display: inline-flex; align-items: center; gap: 0.4rem; color: #8b949e; text-decoration: none; font-size: 0.85rem; font-weight: 500; padding: 0.4rem 1rem; border: 1px solid #21262d; border-radius: 20px; transition: all 0.2s; }
.footer-link:hover { color: #f5a623; border-color: #f5a623; }
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
    
    path_option_1 = os.path.join(base, "data", "processed", "franchise_players.json")
    path_option_2 = os.path.join(base, "machine_learning", "dataset", "franchise_players.json")
    
    player_data = {}
    json_loaded_path = None

    if os.path.exists(path_option_1):
        with open(path_option_1, 'r') as f:
            player_data = json.load(f)
        json_loaded_path = path_option_1
    elif os.path.exists(path_option_2):
        with open(path_option_2, 'r') as f:
            player_data = json.load(f)
        json_loaded_path = path_option_2
            
    return df, player_data, json_loaded_path

try:
    df, player_data, json_path_used = load_data()
    teams = sorted(list(set(df['team1']).union(set(df['team2']))))
except Exception as e:
    st.error(f"⚠️ Critical Error loading datasets: {e}")
    st.stop()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0 1.5rem; border-bottom: 1px solid #21262d; margin-bottom: 1.5rem;">
        <div style="font-size:1.4rem; font-weight:700; color:#f5a623; font-family:'Space Grotesk',sans-serif;">📈 Team Analytics</div>
        <div style="font-size:0.75rem; color:#8b949e; margin-top:0.25rem;">Franchise Performance Hub</div>
    </div>
    """, unsafe_allow_html=True)

    selected_team = st.selectbox("Select Franchise", teams, index=5)
    
    # ── DYNAMIC CASCADING FILTER LOGIC ──
    # 1. Find only the matches where the selected team played
    team_history_df = df[(df['team1'] == selected_team) | (df['team2'] == selected_team)]
    # 2. Extract only the valid seasons for this specific team
    valid_seasons = ["All Time"] + sorted(list(team_history_df['season'].unique()), reverse=True)
    
    selected_season = st.selectbox("Season Filter", valid_seasons)
    
    # ── DEBUG/STATUS TRACKER ──
    st.markdown("<br><hr style='border-color:#21262d;'>", unsafe_allow_html=True)
    if json_path_used:
        st.sidebar.success(f"📂 Pipeline Data Loaded")
        # Optional: uncomment next line if you want to see the exact path in sidebar
        # st.sidebar.caption(f"Source: {os.path.basename(os.path.dirname(json_path_used))}/{os.path.basename(json_path_used)}")
    else:
        st.sidebar.error("❌ 'franchise_players.json' Not Found")
        st.sidebar.info("👉 Please run 'python machine_learning/build_player_stats.py' in your terminal to generate it.")

# ─────────────────────────────────────────────
# DATA PROCESSING
# ─────────────────────────────────────────────
team_df = df[(df['team1'] == selected_team) | (df['team2'] == selected_team)].copy()

if selected_season != "All Time":
    team_df = team_df[team_df['season'] == selected_season]

total_matches = len(team_df)
wins = len(team_df[team_df['winner'] == selected_team])
losses = total_matches - wins
win_pct = (wins / total_matches * 100) if total_matches > 0 else 0

# Calculate Season-wise Trend
trend_data = []
for s in sorted(df['season'].unique()):
    s_df = df[((df['team1'] == selected_team) | (df['team2'] == selected_team)) & (df['season'] == s)]
    s_matches = len(s_df)
    s_wins = len(s_df[s_df['winner'] == selected_team])
    if s_matches > 0:
        trend_data.append({"Season": str(s), "Win %": (s_wins/s_matches)*100})

if trend_data:
    trend_df = pd.DataFrame(trend_data).set_index("Season")
    best_season_row = trend_df.idxmax()
    best_season = best_season_row['Win %']
    best_win_pct = trend_df['Win %'].max()
else:
    trend_df = pd.DataFrame()
    best_season = "N/A"
    best_win_pct = 0

# ─────────────────────────────────────────────
# MAIN UI
# ─────────────────────────────────────────────
st.markdown('<div class="page-header">📈 Franchise Analytics</div>', unsafe_allow_html=True)
st.markdown(f'<div class="page-sub">Comprehensive performance metrics for <strong>{selected_team}</strong> ({selected_season})</div>', unsafe_allow_html=True)

if total_matches == 0:
    st.warning(f"No matches found for {selected_team} in the {selected_season} season.")
    st.stop()

# ── KPI Cards ──
st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-title">Matches Played</div>
        <div class="kpi-val">{total_matches}</div>
    </div>
    <div class="kpi-card" style="border-bottom: 3px solid #28a745;">
        <div class="kpi-title">Total Wins</div>
        <div class="kpi-val" style="color: #28a745;">{wins}</div>
    </div>
    <div class="kpi-card" style="border-bottom: 3px solid #dc3545;">
        <div class="kpi-title">Total Losses</div>
        <div class="kpi-val" style="color: #dc3545;">{losses}</div>
    </div>
    <div class="kpi-card" style="border-bottom: 3px solid #f5a623;">
        <div class="kpi-title">Win Percentage</div>
        <div class="kpi-val" style="color: #f5a623;">{win_pct:.1f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Trend Chart & Best Season ──
col_chart, col_best = st.columns([2, 1], gap="large")

with col_chart:
    st.markdown('<div class="section-card"><div class="section-title">Season-wise Win Percentage Trend</div>', unsafe_allow_html=True)
    if not trend_df.empty:
        # Lowered height to 210 to give x-axis labels horizontal clearance
        st.line_chart(trend_df, height=210, use_container_width=True, color="#f5a623")
    st.markdown('</div>', unsafe_allow_html=True)

with col_best:
    st.markdown(f"""
    <div class="section-card" style="display:flex; flex-direction:column; justify-content:center; text-align:center;">
        <div class="section-title" style="border:none; margin-bottom:0;">Peak Performance Season</div>
        <div style="font-size: 3rem; font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: #4a9eff; margin: 1rem 0;">{best_season}</div>
        <div style="font-size: 0.9rem; color: #8b949e;">Highest Win Rate: <strong style="color:#e6edf3;">{best_win_pct:.1f}%</strong></div>
    </div>
    """, unsafe_allow_html=True)

# ── AI Insight ──
ai_commentary = f"Overall, {selected_team} maintains a {win_pct:.1f}% historical win rate. Their strategic peak occurred during the {best_season} campaign where they achieved a dominant {best_win_pct:.1f}% win ratio."
if selected_season != "All Time":
    ai_commentary = f"In the {selected_season} season, {selected_team} secured {wins} victories, resulting in a {win_pct:.1f}% win rate across {total_matches} fixtures."

st.markdown(f"""
<div class="ai-card">
    <div class="ai-label">🤖 AI Team Summary</div>
    <div class="ai-text">"{ai_commentary}"</div>
</div>
""", unsafe_allow_html=True)

# ── Top Players (Dynamic Generation from Pipeline) ──
col_bat, col_bowl = st.columns(2, gap="large")

# Extract player information safely
clean_team_name = selected_team.strip()
team_players = player_data.get(clean_team_name, {"bat": [], "bowl": []})

with col_bat:
    bat_rows_html = ""
    for player in team_players["bat"]:
        # Flattened string to prevent Markdown code block rendering
        bat_rows_html += f"<tr><td class='player-name'>{player[0]}</td><td>{player[1]}</td><td>{player[2]}</td><td>{player[3]}</td></tr>"
        
    if not bat_rows_html:
        bat_rows_html = "<tr><td colspan='4' style='text-align:center; color:#8b949e;'>No batting data compiled for this franchise</td></tr>"

    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">🏏 Top 3 Batsmen (Franchise History)</div>
        <table class="player-table">
            <thead><tr><th>Player</th><th>Runs</th><th>Avg</th><th>SR</th></tr></thead>
            <tbody>{bat_rows_html}</tbody>
        </table>
        <div style="font-size:0.7rem; color:#484f58; margin-top:1rem; text-align:right;">*Data compiled dynamically from deliveries.csv data pipeline.</div>
    </div>
    """, unsafe_allow_html=True)

with col_bowl:
    bowl_rows_html = ""
    for player in team_players["bowl"]:
        # Flattened string to prevent Markdown code block rendering
        bowl_rows_html += f"<tr><td class='player-name'>{player[0]}</td><td>{player[1]}</td><td>{player[2]}</td><td>{player[3]}</td></tr>"
        
    if not bowl_rows_html:
        bowl_rows_html = "<tr><td colspan='4' style='text-align:center; color:#8b949e;'>No bowling data compiled for this franchise</td></tr>"

    st.markdown(f"""
    <div class="section-card">
        <div class="section-title">🎯 Top 3 Bowlers (Franchise History)</div>
        <table class="player-table">
            <thead><tr><th>Player</th><th>Wickets</th><th>Econ</th><th>Avg</th></tr></thead>
            <tbody>{bowl_rows_html}</tbody>
        </table>
        <div style="font-size:0.7rem; color:#484f58; margin-top:1rem; text-align:right;">*Data compiled dynamically from deliveries.csv data pipeline.</div>
    </div>
    """, unsafe_allow_html=True)

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
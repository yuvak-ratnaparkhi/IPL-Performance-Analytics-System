import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import requests
import json

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Analytics Intelligence System",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# GLOBAL CSS — Dark IPL Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0d1117;
    color: #e6edf3;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
    border-right: 1px solid #21262d;
}
[data-testid="stSidebar"] * { color: #e6edf3 !important; }

/* Hide default Streamlit chrome */
#MainMenu, footer { visibility: hidden; }

/* Main container padding */
.block-container { padding: 2rem 2.5rem 4rem 2.5rem !important; }

/* ── Hero Header ── */
.hero-header {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #1a1f29 100%);
    border: 1px solid #21262d;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #f5a623, #e8651a, #c0392b, #f5a623);
    background-size: 200% auto;
    animation: shimmer 3s linear infinite;
}
@keyframes shimmer { to { background-position: 200% center; } }

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #f5a623;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-size: 0.95rem;
    color: #8b949e;
    margin: 0;
    font-weight: 400;
    letter-spacing: 0.2px;
}

/* ── Cards ── */
.card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 1.5rem;
    height: 100%;
}
.card-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.5rem;
}

/* ── Winner Card ── */
.winner-card {
    background: linear-gradient(135deg, #161b22, #1a1f29);
    border: 1px solid #f5a623;
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
    box-shadow: 0 0 40px rgba(245, 166, 35, 0.08);
    margin-bottom: 1.5rem;
}
.winner-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 0.75rem;
}
.winner-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #f5a623;
    margin: 0;
    line-height: 1.1;
}
.winner-trophy { font-size: 1.8rem; margin-bottom: 0.5rem; }

/* ── Confidence Badge ── */
.badge {
    display: inline-block;
    padding: 0.35rem 1rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-top: 1rem;
    letter-spacing: 0.3px;
}
.badge-cointoss  { background: rgba(255,193,7,0.15);  color: #ffc107; border: 1px solid rgba(255,193,7,0.3); }
.badge-moderate  { background: rgba(40,167,69,0.15);  color: #28a745; border: 1px solid rgba(40,167,69,0.3); }
.badge-favourite { background: rgba(220,53,69,0.15);  color: #ff6b6b; border: 1px solid rgba(220,53,69,0.3); }

/* ── Probability Bar ── */
.prob-row {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
.prob-team-name {
    font-size: 0.95rem;
    font-weight: 600;
    color: #e6edf3;
    margin-bottom: 0.5rem;
    display: flex;
    justify-content: space-between;
}
.prob-pct { color: #f5a623; font-weight: 700; }
.prob-track {
    background: #21262d;
    border-radius: 6px;
    height: 10px;
    overflow: hidden;
}
.prob-fill-t1 {
    height: 100%;
    border-radius: 6px;
    background: linear-gradient(90deg, #f5a623, #e8651a);
    transition: width 0.8s ease;
}
.prob-fill-t2 {
    height: 100%;
    border-radius: 6px;
    background: linear-gradient(90deg, #4a9eff, #0969da);
    transition: width 0.8s ease;
}

/* ── Match Insights ── */
.tape-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.tape-title {
    font-size: 0.75rem;
    font-weight: 600;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #21262d;
}
.tape-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid #21262d;
}
.tape-row:last-child { border-bottom: none; }
.tape-metric { font-size: 0.8rem; color: #8b949e; }
.tape-val    { font-size: 0.9rem; font-weight: 600; color: #e6edf3; }
.tape-val-highlight { color: #f5a623; }

/* ── AI Commentary ── */
.ai-card {
    background: linear-gradient(135deg, #161b22, #12181f);
    border: 1px solid #30363d;
    border-left: 3px solid #f5a623;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.ai-label {
    font-size: 0.7rem;
    font-weight: 700;
    color: #f5a623;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 0.75rem;
}
.ai-text {
    font-size: 0.92rem;
    color: #c9d1d9;
    line-height: 1.7;
    font-style: italic;
}

/* ── Sidebar Inputs ── */
.sidebar-section {
    background: #21262d;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
}
.sidebar-title {
    font-size: 0.7rem;
    font-weight: 700;
    color: #f5a623;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.75rem;
}

/* Streamlit widget overrides */
.stSelectbox > div > div {
    background: #21262d !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
}
.stRadio > div { gap: 0.5rem; }
.stButton > button {
    background: linear-gradient(135deg, #f5a623, #e8651a) !important;
    color: #0d1117 !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* Expander */
.streamlit-expanderHeader {
    background: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 10px !important;
    color: #8b949e !important;
}

/* ── Footer ── */
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


# ─────────────────────────────────────────────
# DATA & MODEL CONSTANTS (DYNAMIC)
# ─────────────────────────────────────────────
@st.cache_data
def load_dynamic_data():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Ensure this matches the exact name of your cleaned dataset from Phase 2/3
    csv_path = os.path.join(base, "machine_learning", "dataset", "match_winner_dataset.csv") 
    
    df = pd.read_csv(csv_path)
    
    teams = sorted(list(set(df['team1']).union(set(df['team2']))))
    venues = sorted(list(df['venue'].unique()))
    venue_avg_scores = df.groupby('venue')['venue_avg_score'].last().to_dict()
    
    win_pct = {}
    for team in teams:
        team_data = df[(df['team1'] == team) | (df['team2'] == team)].iloc[-1]
        win_pct[team] = team_data['team1_win_pct'] if team_data['team1'] == team else team_data['team2_win_pct']
        
    return teams, venues, venue_avg_scores, win_pct

TEAMS, VENUES, VENUE_AVG_SCORES, WIN_PCT = load_dynamic_data()


# ─────────────────────────────────────────────
# LOAD MODELS
# ─────────────────────────────────────────────
@st.cache_resource
def load_models():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_path = os.path.join(base, "machine_learning", "models")
    xgb     = joblib.load(os.path.join(models_path, "xgb_model.pkl"))
    rf      = joblib.load(os.path.join(models_path, "rf_model.pkl"))
    encoder = joblib.load(os.path.join(models_path, "venue_encoder.pkl"))
    trackers = joblib.load(os.path.join(models_path, "historical_trackers.pkl"))
    return xgb, rf, encoder, trackers

try:
    xgb_model, rf_model, venue_encoder, trackers = load_models()
    models_loaded = True
except Exception as e:
    models_loaded = False
    model_error = str(e)


# ─────────────────────────────────────────────
# HELPER FUNCTIONS & LOOKUPS
# ─────────────────────────────────────────────
HOME_KEYWORDS = {
    "Mumbai Indians":              ["wankhede", "brabourne", "patil"],
    "Chennai Super Kings":         ["chidambaram", "chepauk"],
    "Royal Challengers Bengaluru": ["chinnaswamy"],
    "Kolkata Knight Riders":       ["eden"],
    "Delhi Capitals":              ["jaitley", "kotla", "feroz"],
    "Rajasthan Royals":            ["mansingh", "sawai"],
    "Sunrisers Hyderabad":         ["rajiv gandhi", "hyderabad", "uppal"],
    "Punjab Kings":                ["mohali", "bindra", "punjab"],
    "Gujarat Titans":              ["modi", "ahmedabad", "motera"],
    "Lucknow Super Giants":        ["ekana", "lucknow"],
    "Deccan Chargers":             ["rajiv gandhi", "hyderabad"],
    "Pune Warriors":               ["maharashtra", "pune"],
    "Rising Pune Supergiant":      ["maharashtra", "pune"],
    "Gujarat Lions":               ["saurashtra", "rajkot"],
    "Kochi Tuskers Kerala":        ["nehru", "kochi"]
}

def check_home(team, venue):
    for kw in HOME_KEYWORDS.get(team, []):
        if kw in venue.lower():
            return 1
    return 0

def get_h2h(t1, t2):
    pair = tuple(sorted([t1, t2]))
    if 'h2h_tracker' in trackers and pair in trackers['h2h_tracker']:
        t1w = trackers['h2h_tracker'][pair].get(t1, 0)
        t2w = trackers['h2h_tracker'][pair].get(t2, 0)
        total_matches = t1w + t2w
        if total_matches > 0:
            return total_matches, t1w, t2w
    return None, None, None

def get_confidence(prob):
    if prob >= 0.60:
        return "🔥 Strong Favourite", "badge-favourite"
    elif prob >= 0.55:
        return "🟢 Moderate Edge", "badge-moderate"
    else:
        return "🟡 Coin Toss Match", "badge-cointoss"

def build_feature_vector(t1, t2, venue, toss_winner, toss_decision):
    t1_won_toss       = 1 if toss_winner == t1 else 0
    toss_decision_field = 1 if toss_decision == "Field First" else 0
    team1_is_chasing  = int(
        (t1_won_toss == 1 and toss_decision_field == 1) or
        (t1_won_toss == 0 and toss_decision_field == 0)
    )
    t1_home           = check_home(t1, venue)
    t2_home           = check_home(t2, venue)
    home_adv_diff     = t1_home - t2_home
    win_pct_diff      = WIN_PCT.get(t1, 50.0) - WIN_PCT.get(t2, 50.0)
    venue_avg         = VENUE_AVG_SCORES.get(venue, 160)
    venue_is_highway  = 1 if venue_avg >= 170 else 0

    try:
        venue_enc = venue_encoder.transform([venue])[0]
    except Exception:
        venue_enc = 0

    # --- CALCULATE THE 5 MISSING ADVANCED FEATURES ---
    pair = tuple(sorted([t1, t2]))
    h2h_diff = trackers['h2h_tracker'].get(pair, {}).get(t1, 0) - trackers['h2h_tracker'].get(pair, {}).get(t2, 0)
    
    t1_form = sum(trackers['team_recent_form'].get(t1, [0])[-5:])
    t2_form = sum(trackers['team_recent_form'].get(t2, [0])[-5:])
    recent_form_diff = t1_form - t2_form
    
    streak_diff = trackers['team_streak'].get(t1, 0) - trackers['team_streak'].get(t2, 0)
    
    t1_v_stats = trackers['venue_team_tracker'].get((venue, t1), {'w':0, 't':1})
    t2_v_stats = trackers['venue_team_tracker'].get((venue, t2), {'w':0, 't':1})
    t1_vw = t1_v_stats['w'] / t1_v_stats['t'] if t1_v_stats['t'] > 0 else 0.5
    t2_vw = t2_v_stats['w'] / t2_v_stats['t'] if t2_v_stats['t'] > 0 else 0.5
    v_win_rate_diff = t1_vw - t2_vw
    
    v_toss = trackers['venue_toss_tracker'].get(venue, {'bat_wins':0, 'chase_wins':0, 'total':1})
    v_toss_total = v_toss['total'] if v_toss['total'] > 0 else 1
    v_toss_bias = (v_toss['bat_wins']/v_toss_total) - (v_toss['chase_wins']/v_toss_total)

    # --- BUILD THE EXACT 14-FEATURE DATAFRAME ---
    df = pd.DataFrame([{
        "season":              2024,
        "venue_encoded":       venue_enc,
        "venue_avg_score":     venue_avg,
        "venue_is_highway":    venue_is_highway,
        "team1_won_toss":      t1_won_toss,
        "toss_decision_field": toss_decision_field,
        "team1_is_chasing":    team1_is_chasing,
        "home_advantage_diff": home_adv_diff,
        "win_pct_diff":        win_pct_diff,
        "head_to_head_diff":   h2h_diff,
        "recent_form_diff":    recent_form_diff,
        "streak_diff":         streak_diff,
        "venue_win_rate_diff": v_win_rate_diff,
        "venue_toss_bias":     v_toss_bias
    }])

    # Force exact column order required by XGBoost
    expected_cols = ['season', 'venue_encoded', 'venue_avg_score', 'venue_is_highway',
                     'team1_won_toss', 'toss_decision_field', 'team1_is_chasing',
                     'home_advantage_diff', 'win_pct_diff', 'head_to_head_diff', 
                     'recent_form_diff', 'streak_diff', 'venue_win_rate_diff', 'venue_toss_bias']
    df = df[expected_cols]

    return df, venue_avg, win_pct_diff, home_adv_diff, team1_is_chasing

def get_ai_commentary(t1, t2, venue, t1_prob, t2_prob, venue_avg,
                      win_pct_diff, home_adv_diff, is_chasing, h2h):
    """Call Claude API for AI match analyst commentary."""
    winner = t1 if t1_prob > t2_prob else t2
    loser  = t2 if t1_prob > t2_prob else t1
    margin = abs(t1_prob - t2_prob) * 100

    h2h_text = ""
    if h2h[0]:
        h2h_text = f"Head-to-head: {t1} leads {h2h[1]}-{h2h[2]} in {h2h[0]} meetings."

    prompt = f"""You are an expert IPL cricket analyst. Give a concise 3-sentence match preview.

Match: {t1} vs {t2} at {venue}
Model predicts {winner} wins with {max(t1_prob, t2_prob)*100:.1f}% probability (margin: {margin:.1f}%)
Venue average score: {venue_avg} runs | {'Batting highway' if venue_avg >= 170 else 'Balanced pitch' if venue_avg >= 155 else "Bowler's pitch"}
{t1} historical win %: {WIN_PCT.get(t1, 50):.1f}% | {t2}: {WIN_PCT.get(t2, 50):.1f}%
Win % differential: {win_pct_diff:+.1f}% in favour of {t1 if win_pct_diff > 0 else t2}
Home advantage: {'Neither team is at home' if home_adv_diff == 0 else (t1 + ' has home advantage' if home_adv_diff > 0 else t2 + ' has home advantage')}
Chasing: {t1 + ' is chasing' if is_chasing else t2 + ' is chasing'}
{h2h_text}

Write 3 punchy sentences. Be specific about the venue, teams, and stats. No bullet points. No generic phrases."""

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type": "application/json"},
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=15
        )
        data = response.json()
        return data["content"][0]["text"].strip()
    except Exception:
        return f"{winner} enters this fixture with a statistical edge — {max(t1_prob, t2_prob)*100:.1f}% model confidence backed by historical win rates and venue dynamics. The {venue} surface {'favours big scores and chasing sides' if venue_avg >= 170 else 'tends to reward the bowling side early'}. {loser} will need to overcome a {margin:.1f}% probability gap to pull off the upset."


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0 1.5rem; border-bottom: 1px solid #21262d; margin-bottom: 1.5rem;">
        <div style="font-size:1.4rem; font-weight:700; color:#f5a623; font-family:'Space Grotesk',sans-serif;">
            🏏 IPL Predictor
        </div>
        <div style="font-size:0.75rem; color:#8b949e; margin-top:0.25rem;">
            AI-Powered Match Analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-title">⚔️ Select Teams</div>', unsafe_allow_html=True)
    team1 = st.selectbox("Team 1", TEAMS, index=5, key="team1")
    team2 = st.selectbox("Team 2", TEAMS, index=0, key="team2")

    # ── CLEANED DYNAMIC HOME GROUND LOGIC ──
    default_venue_idx = 0
    keywords_list = HOME_KEYWORDS.get(team1, [])
    found_match = False
    for keyword in keywords_list:
        for i, venue_name in enumerate(VENUES):
            if keyword.lower() in venue_name.lower():
                default_venue_idx = i
                found_match = True
                break
        if found_match:
            break

    # ── STREAMLIT STATE LOCK FIX ──
    if "prev_team1" not in st.session_state:
        st.session_state.prev_team1 = team1

    if st.session_state.prev_team1 != team1:
        st.session_state.venue = VENUES[default_venue_idx]  # Force overwrite state memory
        st.session_state.prev_team1 = team1

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">🏟️ Venue</div>', unsafe_allow_html=True)
    venue = st.selectbox("Stadium", VENUES, index=default_venue_idx, key="venue")

    if team1 == team2:
        toss_options = [team1]
    else:
        toss_options = [team1, team2]

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">🪙 Toss</div>', unsafe_allow_html=True)
    toss_winner   = st.selectbox("Toss Winner", toss_options, key="toss_winner")
    toss_decision = st.radio("Decision", ["Bat First", "Field First"], key="toss_decision")

    st.markdown("<br>", unsafe_allow_html=True)
    predict_clicked = st.button("Predict Winner 🚀")

    st.markdown("""
    <div style="margin-top:2rem; padding-top:1rem; border-top:1px solid #21262d;
                font-size:0.72rem; color:#484f58; text-align:center; line-height:1.6;">
        XGBoost · Random Forest<br>
        Trained on 1090+ IPL Matches<br>
        <span style="color:#f5a623;">56.4% Prediction Accuracy</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN PAGE
# ─────────────────────────────────────────────

# Hero Header
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🏏 IPL Performance Analytics Intelligence System</div>
    <div class="hero-subtitle">
        Powered by XGBoost · Trained on 14 IPL seasons · 
        Historical win rates · Venue dynamics · Toss analysis
    </div>
</div>
""", unsafe_allow_html=True)

# ── Validation ──
if team1 == team2:
    st.markdown("""
    <div class="warning-box">
        ⚠️ A team cannot play against itself. Please select two different teams from the sidebar.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if not models_loaded:
    st.error(f"⚠️ Could not load models. Check that .pkl files exist in machine_learning/models/. Error: {model_error}")
    st.stop()

# ── Default State (Before Click) ──
if not predict_clicked:
    col_left, col_right = st.columns([1.2, 0.8], gap="large")
    
    with col_left:
        st.markdown("""
        <div style="background: #161b22; border: 1px solid #21262d; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;">
            <div style="font-size: 0.75rem; font-weight: 600; color: #8b949e; text-transform: uppercase; margin-bottom: 0.5rem;">Selected Matchup</div>
            <div style="font-size: 1.2rem; font-weight: 600; color: #e6edf3;">{t1} <span style="color:#f5a623;">vs</span> {t2}</div>
        </div>
        """.format(t1=team1, t2=team2), unsafe_allow_html=True)

        col_v, col_t = st.columns(2)
        with col_v:
            st.markdown("""
            <div style="background: #161b22; border: 1px solid #21262d; border-radius: 12px; padding: 1.2rem; height: 100%;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #8b949e; text-transform: uppercase; margin-bottom: 0.25rem;">🏟️ Venue</div>
                <div style="font-size: 0.95rem; font-weight: 500; color: #e6edf3;">{v}</div>
            </div>
            """.format(v=venue), unsafe_allow_html=True)
        with col_t:
            st.markdown("""
            <div style="background: #161b22; border: 1px solid #21262d; border-radius: 12px; padding: 1.2rem; height: 100%;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #8b949e; text-transform: uppercase; margin-bottom: 0.25rem;">🪙 Toss</div>
                <div style="font-size: 0.95rem; font-weight: 500; color: #e6edf3;">{tw} · {td}</div>
            </div>
            """.format(tw=toss_winner, td=toss_decision), unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-top: 2rem; padding: 1.5rem; background: rgba(245, 166, 35, 0.05); border: 1px dashed rgba(245, 166, 35, 0.3); border-radius: 12px; text-align: center;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🏏</div>
            <div style="font-size: 0.9rem; color: #c9d1d9;">All parameters set. Click <strong style="color:#f5a623;">Predict Winner 🚀</strong> in the sidebar to run the ML ensemble.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        current_venue_avg = VENUE_AVG_SCORES.get(venue, 160)
        pitch_type = "🔴 Batting Highway" if current_venue_avg >= 170 else ("🟡 Balanced" if current_venue_avg >= 155 else "🟢 Bowler's Pitch")
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #161b22, #12181f); border: 1px solid #30363d; border-top: 3px solid #0969da; border-radius: 12px; padding: 1.5rem; height: 100%;">
            <div style="font-size: 0.8rem; font-weight: 700; color: #4a9eff; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;">
                🔎 Pre-Match Intel
            </div>
            <div style="margin-bottom: 1rem;">
                <div style="font-size: 0.75rem; color: #8b949e; margin-bottom: 0.2rem;">Historical Venue Average</div>
                <div style="font-size: 1.4rem; font-weight: 700; color: #e6edf3;">{current_venue_avg} <span style="font-size:0.9rem; font-weight:400; color:#8b949e;">runs</span></div>
            </div>
            <div style="margin-bottom: 1rem;">
                <div style="font-size: 0.75rem; color: #8b949e; margin-bottom: 0.2rem;">Surface Analysis</div>
                <div style="font-size: 0.95rem; font-weight: 500; color: #e6edf3;">{pitch_type}</div>
            </div>
            <div style="padding-top: 1rem; border-top: 1px solid #21262d;">
                <div style="font-size: 0.8rem; color: #8b949e; line-height: 1.5; font-style: italic;">
                    "The model will heavily weight the {pitch_type.split(' ')[1]} nature of {venue} when calculating the impact of {toss_winner}'s decision to {toss_decision.lower()}."
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Prediction Output State (After Click) ──
else:
    X_live, venue_avg, win_pct_diff, home_adv_diff, is_chasing = build_feature_vector(
        team1, team2, venue, toss_winner, toss_decision
    )

    xgb_probs = xgb_model.predict_proba(X_live)[0]
    rf_probs  = rf_model.predict_proba(X_live)[0]

    t1_prob = float(xgb_probs[1])
    t2_prob = float(xgb_probs[0])
    predicted_winner = team1 if t1_prob >= t2_prob else team2
    confidence_label, confidence_class = get_confidence(max(t1_prob, t2_prob))

    # Row 1: Winner + Probabilities
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown(f"""
        <div class="winner-card">
            <div class="winner-trophy">🏆</div>
            <div class="winner-label">Predicted Winner</div>
            <div class="winner-name">{predicted_winner}</div>
            <div><span class="badge {confidence_class}">{confidence_label}</span></div>
        </div>
        """, unsafe_allow_html=True)

        rf_winner = team1 if rf_probs[1] >= rf_probs[0] else team2
        agreement = "✅ Both models agree" if rf_winner == predicted_winner else "⚠️ Models disagree"
        agree_color = "#28a745" if rf_winner == predicted_winner else "#ffc107"
        st.markdown(f"""
        <div style="background:#161b22; border:1px solid #21262d; border-radius:10px;
                    padding:0.9rem 1.25rem; display:flex; justify-content:space-between;
                    align-items:center; font-size:0.85rem;">
            <span style="color:#8b949e;">Model Consensus</span>
            <span style="color:{agree_color}; font-weight:600;">{agreement}</span>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown(f"""
        <div class="prob-row">
            <div class="prob-team-name">
                <span>{team1}</span>
                <span class="prob-pct">{t1_prob*100:.1f}%</span>
            </div>
            <div class="prob-track">
                <div class="prob-fill-t1" style="width:{t1_prob*100:.1f}%;"></div>
            </div>
        </div>
        <div class="prob-row">
            <div class="prob-team-name">
                <span>{team2}</span>
                <span class="prob-pct">{t2_prob*100:.1f}%</span>
            </div>
            <div class="prob-track">
                <div class="prob-fill-t2" style="width:{t2_prob*100:.1f}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ✨ Polished Random Forest Validation Card (Safely nested here) ✨
        st.markdown(f"""
        <div style="background: #11151c; border: 1px solid #21262d; border-radius: 8px;
                    padding: 0.75rem 1.25rem; display: flex; align-items: center; 
                    gap: 0.5rem; font-size: 0.8rem; color: #8b949e; margin-top: 0.5rem;
                    letter-spacing: 0.2px;">
            <span style="font-weight: 600; color: #4a9eff; text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.5px;">
                Random Forest Check →
            </span>
            <span>{team1}</span> 
            <strong style="color: #e6edf3;">{rf_probs[1]*100:.1f}%</strong>
            <span style="color: #30363d; margin: 0 0.25rem;">|</span>
            <span>{team2}</span> 
            <strong style="color: #e6edf3;">{rf_probs[0]*100:.1f}%</strong>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: AI Commentary + Tale of the Tape
    col_ai, col_tape = st.columns([1.1, 0.9], gap="large")

    with col_ai:
        h2h = get_h2h(team1, team2)
        with st.spinner("🤖 Generating AI match analysis..."):
            commentary = get_ai_commentary(
                team1, team2, venue, t1_prob, t2_prob,
                venue_avg, win_pct_diff, home_adv_diff, is_chasing, h2h
            )
        st.markdown(f"""
        <div class="ai-card">
            <div class="ai-label">🤖 AI Match Analyst</div>
            <div class="ai-text">{commentary}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_tape:
        pitch_type = "🔴 Batting Highway" if venue_avg >= 170 else ("🟡 Balanced" if venue_avg >= 155 else "🟢 Bowler's Pitch")
        home_text  = f"{team1} +home" if home_adv_diff > 0 else (f"{team2} +home" if home_adv_diff < 0 else "Neutral")
        chasing_team = team1 if is_chasing else team2

        h2h_display = "No data"
        if h2h[0]:
            h2h_display = f"{team1} {h2h[1]}–{h2h[2]} {team2}"

        st.markdown(f"""
        <div class="tape-card">
            <div class="tape-title">📊 Match Insights</div>
            <div class="tape-row">
                <span class="tape-metric">Venue Avg Score</span>
                <span class="tape-val tape-val-highlight">{venue_avg} runs</span>
            </div>
            <div class="tape-row">
                <span class="tape-metric">Pitch Type</span>
                <span class="tape-val">{pitch_type}</span>
            </div>
            <div class="tape-row">
                <span class="tape-metric">Home Advantage</span>
                <span class="tape-val">{home_text}</span>
            </div>
            <div class="tape-row">
                <span class="tape-metric">Chasing Team</span>
                <span class="tape-val">{chasing_team}</span>
            </div>
            <div class="tape-row">
                <span class="tape-metric">Win % Edge</span>
                <span class="tape-val tape-val-highlight">{abs(win_pct_diff):.1f}% → {team1 if win_pct_diff > 0 else team2}</span>
            </div>
            <div class="tape-row">
                <span class="tape-metric">Head-to-Head</span>
                <span class="tape-val">{h2h_display}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Under the Hood Modals
    with st.expander("📊 How does the AI know? — Model Internals"):
        st.markdown("""
        <div style="font-size:0.85rem; color:#8b949e; line-height:1.8; margin-bottom:1rem;">
        The XGBoost model was trained on <strong style="color:#e6edf3;">1090+ IPL matches</strong> 
        from 2008–2024 using <strong style="color:#e6edf3;">9 engineered features</strong>. 
        No player-level data is used — only pre-match, publicly available information.
        In T20 cricket, a 55–60% accuracy ceiling is realistic; 
        multi-million dollar betting firms with live tracking reach ~62–65%.
        </div>
        """, unsafe_allow_html=True)

        feat_importances = {
            "win_pct_diff":        13.95,
            "home_advantage_diff": 12.53,
            "team1_is_chasing":    12.41,
            "venue_avg_score":     11.64,
            "season":              11.20,
            "venue_encoded":       11.08,
            "toss_decision_field": 10.45,
            "team1_won_toss":       9.22,
            "venue_is_highway":     7.52,
        }

        for feat, imp in feat_importances.items():
            bar_w = int(imp / 14 * 100)
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:1rem; margin-bottom:0.5rem;">
                <div style="width:160px; font-size:0.78rem; color:#8b949e;">{feat}</div>
                <div style="flex:1; background:#21262d; border-radius:4px; height:8px;">
                    <div style="width:{bar_w}%; background:linear-gradient(90deg,#f5a623,#e8651a);
                                height:8px; border-radius:4px;"></div>
                </div>
                <div style="width:40px; font-size:0.8rem; color:#f5a623; text-align:right;">{imp}%</div>
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
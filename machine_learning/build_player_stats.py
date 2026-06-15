import pandas as pd
import json
import os

# 1. Define Paths
base = os.path.dirname(os.path.abspath(__file__))
deliveries_path = os.path.join(base, "dataset", "deliveries.csv")  # Make sure this file exists!
output_path = os.path.join(base, "..", "data", "processed", "franchise_players.json")

print("⏳ Loading 250k+ deliveries data...")
df = pd.read_csv(deliveries_path)

franchise_stars = {}
teams = df['batting_team'].unique()

print("⚙️ Crunching Top 3 Batsmen & Bowlers for every franchise...")
for team in teams:
    # ── BATTING STATS ──
    team_bat = df[df['batting_team'] == team]
    bat_stats = team_bat.groupby('batter').agg(
        runs=('batsman_runs', 'sum'),
        balls=('batsman_runs', 'count') # Rough approximation; ignoring wides for simplicity here
    ).reset_index()
    
    # Get dismissals for average calculation
    dismissals = df[(df['batting_team'] == team) & (df['is_wicket'] == 1)].groupby('player_dismissed').size().reset_index(name='outs')
    bat_stats = bat_stats.merge(dismissals, left_on='batter', right_on='player_dismissed', how='left').fillna({'outs': 0})
    
    # Calculate Avg and Strike Rate
    bat_stats['avg'] = bat_stats.apply(lambda x: x['runs'] / x['outs'] if x['outs'] > 0 else x['runs'], axis=1)
    bat_stats['sr'] = (bat_stats['runs'] / bat_stats['balls']) * 100
    
    # Sort and take Top 3
    top_batters = bat_stats.sort_values(by='runs', ascending=False).head(3)
    bat_list = []
    for _, row in top_batters.iterrows():
        bat_list.append([row['batter'], str(int(row['runs'])), f"{row['avg']:.1f}", f"{row['sr']:.1f}"])

    # ── BOWLING STATS ──
    team_bowl = df[df['bowling_team'] == team]
    
    # Wickets (excluding run outs)
    valid_wickets = ['caught', 'bowled', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']
    wickets_df = team_bowl[(team_bowl['is_wicket'] == 1) & (team_bowl['dismissal_kind'].isin(valid_wickets))]
    bowl_stats = wickets_df.groupby('bowler').size().reset_index(name='wickets')
    
    # Runs Conceded & Balls Bowled
    runs_conceded = team_bowl.groupby('bowler')['total_runs'].sum().reset_index(name='runs_given')
    
    # Dynamically check which column format your dataset uses for extras
    if 'extras_type' in team_bowl.columns:
        legal_deliveries = team_bowl[team_bowl['extras_type'].isna() | (team_bowl['extras_type'] == 'legbyes') | (team_bowl['extras_type'] == 'byes')]
    elif 'wide_runs' in team_bowl.columns and 'noball_runs' in team_bowl.columns:
        legal_deliveries = team_bowl[(team_bowl['wide_runs'] == 0) & (team_bowl['noball_runs'] == 0)]
    else:
        # Safe fallback if extras columns aren't found
        legal_deliveries = team_bowl
        
    balls_bowled = legal_deliveries.groupby('bowler').size().reset_index(name='legal_balls')
    
    # Merge and calculate
    bowl_stats = bowl_stats.merge(runs_conceded, on='bowler').merge(balls_bowled, on='bowler')
    bowl_stats['overs'] = bowl_stats['legal_balls'] / 6
    bowl_stats['econ'] = bowl_stats['runs_given'] / bowl_stats['overs']
    bowl_stats['avg'] = bowl_stats['runs_given'] / bowl_stats['wickets']
    
    # Sort and take Top 3
    top_bowlers = bowl_stats.sort_values(by='wickets', ascending=False).head(3)
    bowl_list = []
    for _, row in top_bowlers.iterrows():
        bowl_list.append([row['bowler'], str(int(row['wickets'])), f"{row['econ']:.2f}", f"{row['avg']:.1f}"])

    # Save to dictionary
    franchise_stars[team] = {"bat": bat_list, "bowl": bowl_list}

# 3. Save the dynamically generated JSON
with open(output_path, 'w') as f:
    json.dump(franchise_stars, f, indent=4)

print(f"✅ Success! Dynamic dataset saved to: {output_path}")
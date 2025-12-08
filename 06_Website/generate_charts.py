"""
Generate Altair charts and save as HTML files
This creates static visualizations that can be embedded in the website
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from modules.data_processor import FootballDataProcessor
from modules.visualizations import PlayerVisualizations
import json

# Initialize
data_path = '../data/players_data_light-2024_2025.csv'
processor = FootballDataProcessor(data_path)
df = processor.load_and_clean(min_minutes=450)
viz = PlayerVisualizations()

print(f"Loaded {len(df)} players")

# Create output directory
os.makedirs('static/charts', exist_ok=True)
os.makedirs('static/data', exist_ok=True)

# Generate example charts that will be embedded in HTML pages

# 1. League comparison scatter
print("Generating league comparison scatter...")
chart = viz.create_scatter_explorer(
    df[df['Position'].isin(['FW', 'MF'])],
    x_metric='PrgC_per90',
    y_metric='xGxAG_per90',
    color_by='Comp'
)
chart.save('static/charts/league_scatter.html')

# 2. Position distribution - use position-appropriate metrics
print("Generating position analysis...")
position_metrics = {
    'GK': 'Save%',      # Goalkeepers ranked by Save Percentage
    'DF': 'Tkl_per90',  # Defenders ranked by Tackles per 90
    'MF': 'PrgC_per90', # Midfielders ranked by Progressive Carries per 90
    'FW': 'Gls_per90'   # Forwards ranked by Goals per 90
}
for pos, metric in position_metrics.items():
    chart = viz.create_top_players_chart(df, metric, n=15, position=pos)
    chart.save(f'static/charts/top_{pos.lower()}.html')

# 3. League comparison box plots
print("Generating league comparisons...")
chart = viz.create_league_comparison(df[df['Position'] != 'GK'], 'Tkl_per90')
chart.save('static/charts/league_tackles.html')

chart = viz.create_league_comparison(df[df['Position'] != 'GK'], 'Cmp%')
chart.save('static/charts/league_passing.html')

# 4. Generate data for dropdowns
print("Generating metadata...")
metadata = {
    'leagues': processor.get_leagues(),
    'positions': processor.get_positions(),
    'teams': processor.get_teams(),
    'players': processor.get_player_list()[:100],
    'total_players': len(df)
}

with open('static/data/metadata.json', 'w') as f:
    json.dump(metadata, f)

# 5. Save processed data as JSON for client-side filtering
print("Saving processed data...")
df_export = df[[
    'Player_Clean', 'Squad', 'Comp', 'Position', 'Age',
    'Gls_per90', 'Ast_per90', 'xG_per90', 'xAG_per90',
    'PrgC_per90', 'Tkl_per90', 'Touches_per90', 'Cmp%'
]].head(500)

df_export.to_json('static/data/players_sample.json', orient='records')

print("✓ Chart generation complete!")
print(f"Charts saved to: static/charts/")
print(f"Data saved to: static/data/")

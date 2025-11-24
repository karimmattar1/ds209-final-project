"""
Football Player Scout Tool - Altair Chart Generator
DS209 Final Project - Karim Mattar
UC Berkeley MIDS

This script generates interactive Altair charts and exports them for the website.
Run this script to regenerate the charts when data updates.
"""

import pandas as pd
import numpy as np
import altair as alt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import json
from pathlib import Path

# Enable Altair to handle larger datasets
alt.data_transformers.disable_max_rows()

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_PATH = SCRIPT_DIR.parent / 'data' / 'players_data_light-2024_2025.csv'
OUTPUT_DIR = SCRIPT_DIR / 'charts'

# Create output directory
OUTPUT_DIR.mkdir(exist_ok=True)

def load_data():
    """Load and prepare player data."""
    df = pd.read_csv(DATA_PATH)
    df = df[df['Min'] >= 450].copy()

    # Create per-90 metrics
    df['Goals_per_90'] = (df['Gls'] / df['90s']).round(2)
    df['Assists_per_90'] = (df['Ast'] / df['90s']).round(2)
    df['xG_per_90'] = (df['xG'] / df['90s']).round(2)
    df['xAG_per_90'] = (df['xAG'] / df['90s']).round(2)
    df['GA_per_90'] = (df['G+A'] / df['90s']).round(2)
    df['PrgC_per_90'] = (df['PrgC'] / df['90s']).round(2)
    df['PrgP_per_90'] = (df['PrgP'] / df['90s']).round(2)
    df['Tkl_per_90'] = (df['Tkl'] / df['90s']).round(2)
    df['Int_per_90'] = (df['Int'] / df['90s']).round(2)
    df['SCA_per_90'] = (df['SCA'] / df['90s']).round(2)

    # Simplified position
    def simplify_pos(pos):
        if pd.isna(pos): return 'Unknown'
        if 'GK' in pos: return 'GK'
        if 'FW' in pos: return 'FW'
        if 'MF' in pos: return 'MF'
        if 'DF' in pos: return 'DF'
        return 'Unknown'

    df['Position'] = df['Pos'].apply(simplify_pos)

    # Clean league names
    df['League'] = df['Comp'].str.replace('eng ', '').str.replace('es ', '').str.replace('de ', '').str.replace('it ', '').str.replace('fr ', '')

    # Age groups
    df['Age_Group'] = pd.cut(df['Age'], bins=[0, 21, 25, 29, 35, 50],
                             labels=['U21', '22-25', '26-29', '30-35', '36+'])

    return df

def create_scatter_explorer(df):
    """Create interactive scatter plot explorer with Altair selections."""

    # Create dropdown selections for axes
    x_dropdown = alt.binding_select(
        options=['Goals_per_90', 'Assists_per_90', 'xG_per_90', 'xAG_per_90',
                 'GA_per_90', 'PrgC_per_90', 'PrgP_per_90', 'Tkl_per_90',
                 'Int_per_90', 'SCA_per_90', 'Age'],
        name='X-Axis: '
    )
    x_param = alt.param('x_metric', value='xG_per_90', bind=x_dropdown)

    y_dropdown = alt.binding_select(
        options=['Goals_per_90', 'Assists_per_90', 'xG_per_90', 'xAG_per_90',
                 'GA_per_90', 'PrgC_per_90', 'PrgP_per_90', 'Tkl_per_90',
                 'Int_per_90', 'SCA_per_90', 'Age'],
        name='Y-Axis: '
    )
    y_param = alt.param('y_metric', value='Goals_per_90', bind=y_dropdown)

    # Position filter
    position_dropdown = alt.binding_select(
        options=[None, 'FW', 'MF', 'DF', 'GK'],
        labels=['All Positions', 'Forward', 'Midfielder', 'Defender', 'Goalkeeper'],
        name='Position: '
    )
    position_select = alt.selection_point(fields=['Position'], bind=position_dropdown)

    # League filter
    leagues = ['All'] + sorted(df['League'].unique().tolist())
    league_dropdown = alt.binding_select(
        options=[None] + df['League'].unique().tolist(),
        labels=['All Leagues'] + df['League'].unique().tolist(),
        name='League: '
    )
    league_select = alt.selection_point(fields=['League'], bind=league_dropdown)

    # Color scheme
    position_colors = alt.Scale(
        domain=['FW', 'MF', 'DF', 'GK'],
        range=['#ef4444', '#3b82f6', '#8b5cf6', '#f59e0b']
    )

    chart = alt.Chart(df).mark_circle(size=80, opacity=0.7).encode(
        x=alt.X('xG_per_90:Q', title='Expected Goals per 90'),
        y=alt.Y('Goals_per_90:Q', title='Goals per 90'),
        color=alt.Color('Position:N', scale=position_colors, title='Position'),
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('Squad:N', title='Team'),
            alt.Tooltip('League:N', title='League'),
            alt.Tooltip('Position:N', title='Position'),
            alt.Tooltip('Age:Q', title='Age'),
            alt.Tooltip('Goals_per_90:Q', format='.2f', title='Goals/90'),
            alt.Tooltip('xG_per_90:Q', format='.2f', title='xG/90'),
            alt.Tooltip('Assists_per_90:Q', format='.2f', title='Assists/90'),
            alt.Tooltip('Min:Q', format=',d', title='Minutes')
        ]
    ).add_params(
        position_select,
        league_select
    ).transform_filter(
        position_select
    ).transform_filter(
        league_select
    ).properties(
        title={
            'text': 'Player Scatter Explorer',
            'subtitle': 'Filter by position and league, hover for details'
        },
        width=800,
        height=500
    ).configure_title(
        fontSize=18,
        anchor='start',
        color='#166534'
    ).configure_axis(
        labelColor='#374151',
        titleColor='#166534',
        gridColor='#e5e7eb'
    ).configure_legend(
        titleColor='#166534',
        labelColor='#374151'
    ).interactive()

    return chart

def create_position_comparison(df, position='FW'):
    """Create a scatter plot for a specific position."""

    pos_df = df[df['Position'] == position].copy()

    if position == 'FW':
        x_metric, y_metric = 'xG_per_90', 'Goals_per_90'
        x_title, y_title = 'Expected Goals per 90', 'Goals per 90'
    elif position == 'MF':
        x_metric, y_metric = 'PrgP_per_90', 'SCA_per_90'
        x_title, y_title = 'Progressive Passes per 90', 'Shot Creating Actions per 90'
    else:
        x_metric, y_metric = 'Tkl_per_90', 'Int_per_90'
        x_title, y_title = 'Tackles per 90', 'Interceptions per 90'

    # League selection
    league_selection = alt.selection_point(fields=['League'], bind='legend')

    # Brush selection for highlighting
    brush = alt.selection_interval()

    position_colors = {
        'Premier League': '#6366f1',
        'La Liga': '#ef4444',
        'Bundesliga': '#f59e0b',
        'Serie A': '#3b82f6',
        'Ligue 1': '#10b981'
    }

    chart = alt.Chart(pos_df).mark_circle(size=100).encode(
        x=alt.X(f'{x_metric}:Q', title=x_title, scale=alt.Scale(zero=False)),
        y=alt.Y(f'{y_metric}:Q', title=y_title, scale=alt.Scale(zero=False)),
        color=alt.condition(
            league_selection,
            alt.Color('League:N', scale=alt.Scale(
                domain=list(position_colors.keys()),
                range=list(position_colors.values())
            )),
            alt.value('lightgray')
        ),
        opacity=alt.condition(league_selection, alt.value(0.8), alt.value(0.2)),
        tooltip=[
            'Player:N', 'Squad:N', 'League:N', 'Age:Q',
            alt.Tooltip(f'{x_metric}:Q', format='.2f'),
            alt.Tooltip(f'{y_metric}:Q', format='.2f'),
            alt.Tooltip('Gls:Q', title='Goals'),
            alt.Tooltip('Ast:Q', title='Assists')
        ]
    ).add_params(
        league_selection
    ).properties(
        title=f'{position} Comparison: {x_title} vs {y_title}',
        width=700,
        height=450
    ).interactive()

    return chart

def create_league_comparison(df):
    """Create box plots comparing leagues across key metrics."""

    outfield = df[df['Position'] != 'GK'].copy()

    # Reshape data for faceted box plots
    metrics = ['Goals_per_90', 'Assists_per_90', 'xG_per_90', 'PrgC_per_90', 'Tkl_per_90']
    metric_labels = {
        'Goals_per_90': 'Goals/90',
        'Assists_per_90': 'Assists/90',
        'xG_per_90': 'xG/90',
        'PrgC_per_90': 'Prog Carries/90',
        'Tkl_per_90': 'Tackles/90'
    }

    melted = outfield.melt(
        id_vars=['Player', 'League', 'Position'],
        value_vars=metrics,
        var_name='Metric',
        value_name='Value'
    )
    melted['Metric_Label'] = melted['Metric'].map(metric_labels)

    chart = alt.Chart(melted).mark_boxplot(extent='min-max', size=20).encode(
        x=alt.X('League:N', title=''),
        y=alt.Y('Value:Q', title='Value'),
        color=alt.Color('League:N', legend=None, scale=alt.Scale(
            domain=['Premier League', 'La Liga', 'Bundesliga', 'Serie A', 'Ligue 1'],
            range=['#6366f1', '#ef4444', '#f59e0b', '#3b82f6', '#10b981']
        )),
        column=alt.Column('Metric_Label:N', title='', header=alt.Header(labelFontSize=12, labelColor='#166534'))
    ).properties(
        width=120,
        height=300,
        title='League Comparison Across Key Metrics'
    ).configure_title(
        fontSize=16,
        anchor='start',
        color='#166534'
    )

    return chart

def create_age_performance(df):
    """Create scatter showing age vs performance."""

    attackers = df[df['Position'].isin(['FW', 'MF'])].copy()

    chart = alt.Chart(attackers).mark_circle(size=60, opacity=0.6).encode(
        x=alt.X('Age:Q', title='Age', scale=alt.Scale(domain=[17, 40])),
        y=alt.Y('GA_per_90:Q', title='Goals + Assists per 90'),
        color=alt.Color('Position:N', scale=alt.Scale(
            domain=['FW', 'MF'],
            range=['#ef4444', '#3b82f6']
        )),
        tooltip=['Player:N', 'Squad:N', 'Age:Q',
                 alt.Tooltip('GA_per_90:Q', format='.2f'),
                 alt.Tooltip('Gls:Q'), alt.Tooltip('Ast:Q')]
    ).properties(
        title='Age vs Goal Contributions (Forwards & Midfielders)',
        width=700,
        height=400
    ).interactive()

    # Add trend line
    regression = chart.transform_regression(
        'Age', 'GA_per_90'
    ).mark_line(color='#333', strokeDash=[5,5], strokeWidth=2)

    return (chart + regression)

def create_player_database_view(df):
    """Create an interactive data table view with sorting."""

    # Select key columns for display
    display_df = df[['Player', 'Squad', 'League', 'Position', 'Age', 'Min',
                     'Gls', 'Ast', 'xG', 'xAG', 'Goals_per_90', 'Assists_per_90']].copy()

    # Create a text-based table representation using Altair
    # (For actual interactive table, we'll use DataTables.js in HTML)

    # Bar chart of top scorers
    top_scorers = df.nlargest(20, 'Gls')[['Player', 'Squad', 'Gls', 'xG', 'Position']].copy()

    chart = alt.Chart(top_scorers).mark_bar().encode(
        x=alt.X('Gls:Q', title='Goals'),
        y=alt.Y('Player:N', sort='-x', title=''),
        color=alt.Color('Position:N', scale=alt.Scale(
            domain=['FW', 'MF', 'DF'],
            range=['#ef4444', '#3b82f6', '#8b5cf6']
        )),
        tooltip=['Player:N', 'Squad:N', 'Gls:Q', alt.Tooltip('xG:Q', format='.1f')]
    ).properties(
        title='Top 20 Scorers (2024-25 Season)',
        width=600,
        height=500
    )

    return chart

def export_data_for_web(df):
    """Export cleaned data as JSON for web consumption."""

    # Select columns needed for the website
    web_df = df[['Player', 'Squad', 'League', 'Position', 'Pos', 'Age', 'Min',
                 'Gls', 'Ast', 'G+A', 'xG', 'xAG',
                 'Goals_per_90', 'Assists_per_90', 'xG_per_90', 'xAG_per_90',
                 'GA_per_90', 'PrgC_per_90', 'PrgP_per_90', 'Tkl_per_90',
                 'Int_per_90', 'SCA_per_90']].copy()

    # Round floats
    float_cols = web_df.select_dtypes(include=['float64']).columns
    web_df[float_cols] = web_df[float_cols].round(2)

    # Export as JSON
    web_df.to_json(OUTPUT_DIR / 'players_data.json', orient='records')
    print(f"Exported {len(web_df)} players to players_data.json")

    return web_df

def main():
    print("Loading data...")
    df = load_data()
    print(f"Loaded {len(df)} players")

    print("\nGenerating charts...")

    # 1. Scatter Explorer
    scatter = create_scatter_explorer(df)
    scatter.save(str(OUTPUT_DIR / 'scatter_explorer.html'))
    scatter.save(str(OUTPUT_DIR / 'scatter_explorer.json'))
    print("- Scatter explorer saved")

    # 2. Position-specific charts
    for pos in ['FW', 'MF', 'DF']:
        chart = create_position_comparison(df, pos)
        chart.save(str(OUTPUT_DIR / f'{pos.lower()}_comparison.html'))
        chart.save(str(OUTPUT_DIR / f'{pos.lower()}_comparison.json'))
        print(f"- {pos} comparison saved")

    # 3. League comparison
    league_chart = create_league_comparison(df)
    league_chart.save(str(OUTPUT_DIR / 'league_comparison.html'))
    league_chart.save(str(OUTPUT_DIR / 'league_comparison.json'))
    print("- League comparison saved")

    # 4. Age vs Performance
    age_chart = create_age_performance(df)
    age_chart.save(str(OUTPUT_DIR / 'age_performance.html'))
    age_chart.save(str(OUTPUT_DIR / 'age_performance.json'))
    print("- Age performance saved")

    # 5. Top scorers
    scorers = create_player_database_view(df)
    scorers.save(str(OUTPUT_DIR / 'top_scorers.html'))
    scorers.save(str(OUTPUT_DIR / 'top_scorers.json'))
    print("- Top scorers saved")

    # 6. Export data for web
    export_data_for_web(df)

    print("\nAll charts generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")

if __name__ == '__main__':
    main()

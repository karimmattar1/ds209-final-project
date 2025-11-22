"""
Football Player Scout Tool
DS209 Final Project - Karim Mattar
UC Berkeley MIDS
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

# Get the directory of this script for proper path resolution
SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_PATH = SCRIPT_DIR.parent / 'data' / 'players_data_light-2024_2025.csv'

st.set_page_config(
    page_title="Scout Tool",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============ CSS ============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Hide defaults */
    #MainMenu, footer, header, .stDeployButton {display: none !important;}
    [data-testid="stSidebar"] {display: none;}

    /* Gradient Background - like the old project */
    .stApp {
        background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 50%, #f0fdf4 100%) !important;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 0 !important;
        padding-bottom: 3rem;
    }

    * { font-family: 'Inter', -apple-system, sans-serif !important; }

    /* Cards with shadows - like old project */
    .card {
        background: white;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #e5e7eb;
    }

    .filter-card {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
    }

    .player-card {
        background: white;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
    }

    .similar-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 12px;
        transition: box-shadow 0.2s, transform 0.2s;
    }

    .similar-card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }

    /* Text */
    h1, h2, h3, h4 { color: #166534 !important; font-weight: 700 !important; }
    p, span, label, div, li, td { color: #374151 !important; }
    strong { color: #166534 !important; }

    .page-title {
        color: #166534 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem;
    }

    .page-subtitle {
        color: #6b7280 !important;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }

    /* Form elements */
    .stSelectbox > div > div {
        background: white !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
    }

    .stSelectbox > div > div:hover { border-color: #16a34a !important; }
    .stSelectbox > div > div:focus-within {
        border-color: #16a34a !important;
        box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.15) !important;
    }

    .stSelectbox label { color: #166534 !important; font-weight: 600 !important; font-size: 0.875rem !important; }

    /* Dropdown - FORCE LIGHT */
    div[data-baseweb="popover"] {
        background: white !important;
        background-color: white !important;
    }

    div[data-baseweb="popover"] > div {
        background: white !important;
        background-color: white !important;
    }

    ul[role="listbox"] {
        background: white !important;
        background-color: white !important;
    }

    li[role="option"] {
        background: white !important;
        background-color: white !important;
        color: #374151 !important;
    }

    li[role="option"]:hover {
        background: #f0fdf4 !important;
        background-color: #f0fdf4 !important;
        color: #166534 !important;
    }

    li[role="option"][aria-selected="true"] {
        background: #dcfce7 !important;
        background-color: #dcfce7 !important;
        color: #166534 !important;
    }

    [data-baseweb="select"] span { color: #374151 !important; }
    [data-baseweb="select"] svg { fill: #6b7280 !important; }

    .stSlider label { color: #166534 !important; font-weight: 600 !important; }
    .stSlider [data-testid="stTickBarMin"], .stSlider [data-testid="stTickBarMax"] { color: #6b7280 !important; }

    /* Pill Badge */
    .pill {
        display: inline-flex;
        background: #dcfce7;
        color: #166534 !important;
        padding: 8px 16px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.875rem;
        margin-bottom: 1rem;
    }

    .stat-chip {
        display: inline-block;
        background: #dcfce7;
        color: #166534 !important;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .similarity-score {
        background: #166534;
        color: white !important;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.875rem;
        font-weight: 600;
    }

    /* Nav Buttons - pill shaped */
    .stButton > button {
        background: white !important;
        color: #166534 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 50px !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background: #f0fdf4 !important;
        border-color: #166534 !important;
    }

    /* Primary button (active nav) */
    .stButton > button[kind="primary"] {
        background: #166534 !important;
        color: white !important;
        border: 1px solid #166534 !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: #14532d !important;
    }

    .stDownloadButton > button {
        background: #166534 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
    }

    .stDownloadButton > button:hover {
        background: #14532d !important;
    }

    /* DATAFRAME - FORCE LIGHT BACKGROUND */
    [data-testid="stDataFrame"],
    [data-testid="stDataFrame"] > div,
    [data-testid="stDataFrame"] iframe,
    .stDataFrame,
    .stDataFrame > div {
        background: white !important;
        background-color: white !important;
        border-radius: 12px !important;
        border: 1px solid #e5e7eb !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }

    [data-testid="stDataFrame"] * {
        color: #374151 !important;
    }

    /* Plotly charts */
    .stPlotlyChart {
        background: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
    }

    .stAlert {
        background: #fffbeb !important;
        border: 1px solid #fcd34d !important;
        border-radius: 8px !important;
    }

    .card table { width: 100%; }
    .card td { padding: 12px 0; border-bottom: 1px solid #e5e7eb; color: #374151 !important; }
    .card tr:last-child td { border-bottom: none; }
    .card ul { padding-left: 20px; margin: 8px 0; }
    .card li { padding: 6px 0; color: #374151 !important; }
</style>
""", unsafe_allow_html=True)

# ============ SESSION STATE ============
if 'page' not in st.session_state:
    st.session_state.page = 'compare'

# ============ LOAD DATA ============
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df = df[df['Min'] >= 450].copy()

    df['Goals per 90'] = (df['Gls'] / df['90s']).round(2)
    df['Assists per 90'] = (df['Ast'] / df['90s']).round(2)
    df['xG per 90'] = (df['xG'] / df['90s']).round(2)
    df['xAG per 90'] = (df['xAG'] / df['90s']).round(2)
    df['G+A per 90'] = (df['G+A'] / df['90s']).round(2)
    df['Prog Carries per 90'] = (df['PrgC'] / df['90s']).round(2)
    df['Prog Passes per 90'] = (df['PrgP'] / df['90s']).round(2)
    df['Tackles per 90'] = (df['Tkl'] / df['90s']).round(2)
    df['Interceptions per 90'] = (df['Int'] / df['90s']).round(2)
    df['Shot Creating per 90'] = (df['SCA'] / df['90s']).round(2)

    def simplify_pos(pos):
        if pd.isna(pos): return 'Unknown'
        if 'GK' in pos: return 'GK'
        if 'FW' in pos: return 'FW'
        if 'MF' in pos: return 'MF'
        if 'DF' in pos: return 'DF'
        return 'Unknown'

    df['Position'] = df['Pos'].apply(simplify_pos)
    df['League'] = df['Comp'].str.replace('eng ', '').str.replace('es ', '').str.replace('de ', '').str.replace('it ', '').str.replace('fr ', '')
    return df

df = load_data()

METRIC_NAMES = {
    'Goals per 90': 'Goals per 90',
    'Assists per 90': 'Assists per 90',
    'xG per 90': 'Expected Goals per 90',
    'xAG per 90': 'Expected Assists per 90',
    'G+A per 90': 'Goals + Assists per 90',
    'Prog Carries per 90': 'Progressive Carries per 90',
    'Prog Passes per 90': 'Progressive Passes per 90',
    'Tackles per 90': 'Tackles per 90',
    'Interceptions per 90': 'Interceptions per 90',
    'Shot Creating per 90': 'Shot Creating Actions per 90',
    'Age': 'Age'
}

COLORS = {
    'positions': {'FW': '#ef4444', 'MF': '#3b82f6', 'DF': '#8b5cf6', 'GK': '#f59e0b'},
    'leagues': {'Premier League': '#6366f1', 'La Liga': '#ef4444', 'Bundesliga': '#f59e0b', 'Serie A': '#3b82f6', 'Ligue 1': '#10b981'}
}

# ============ SIMILARITY FUNCTION ============
def find_similar_players(player_name, df, n=5):
    metrics = ['Goals per 90', 'Assists per 90', 'xG per 90', 'xAG per 90',
               'Prog Carries per 90', 'Prog Passes per 90', 'Tackles per 90', 'Interceptions per 90']
    player_data = df[df['Player'] == player_name]
    if len(player_data) == 0:
        return pd.DataFrame()
    position = player_data['Position'].iloc[0]
    pos_df = df[df['Position'] == position].copy()
    X = pos_df[metrics].fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    player_idx = pos_df[pos_df['Player'] == player_name].index[0]
    player_idx_in_array = list(pos_df.index).index(player_idx)
    similarities = cosine_similarity([X_scaled[player_idx_in_array]], X_scaled)[0]
    pos_df['Similarity'] = similarities
    similar = pos_df[pos_df['Player'] != player_name].nlargest(n, 'Similarity')
    return similar[['Player', 'Squad', 'League', 'Age', 'Similarity', 'Goals per 90', 'Assists per 90']]

# ============ HEADER - Single row with logo + nav buttons ============
header_cols = st.columns([1.5, 1, 1, 1, 1, 1])

with header_cols[0]:
    st.markdown('<h2 style="margin:0;padding:10px 0;">⚽ Scout Tool</h2>', unsafe_allow_html=True)

with header_cols[1]:
    if st.button("📊 Compare", key="nav_compare", use_container_width=True, type="primary" if st.session_state.page == 'compare' else "secondary"):
        st.session_state.page = 'compare'
        st.rerun()
with header_cols[2]:
    if st.button("🔍 Similar", key="nav_similar", use_container_width=True, type="primary" if st.session_state.page == 'similar' else "secondary"):
        st.session_state.page = 'similar'
        st.rerun()
with header_cols[3]:
    if st.button("📈 Explore", key="nav_explore", use_container_width=True, type="primary" if st.session_state.page == 'explore' else "secondary"):
        st.session_state.page = 'explore'
        st.rerun()
with header_cols[4]:
    if st.button("📋 Database", key="nav_database", use_container_width=True, type="primary" if st.session_state.page == 'database' else "secondary"):
        st.session_state.page = 'database'
        st.rerun()
with header_cols[5]:
    if st.button("ℹ️ About", key="nav_about", use_container_width=True, type="primary" if st.session_state.page == 'about' else "secondary"):
        st.session_state.page = 'about'
        st.rerun()

st.divider()

# ============ PAGE CONTENT ============
if st.session_state.page == 'compare':  # COMPARE
    st.markdown('<p class="page-title">Player Comparison</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Compare two players side-by-side using percentile rankings</p>', unsafe_allow_html=True)

    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1.2, 1.2, 1.2, 2])
    with c1: league = st.selectbox("League", ['All'] + sorted(df['League'].unique().tolist()), key="c_lg")
    with c2: pos = st.selectbox("Position", ['All', 'FW', 'MF', 'DF', 'GK'], key="c_pos")
    with c3: mins = st.selectbox("Minimum Minutes", [450, 900, 1350, 1800], index=1, key="c_min")
    with c4: ages = st.slider("Age Range", 16, 40, (18, 35), key="c_age")
    st.markdown('</div>', unsafe_allow_html=True)

    fdf = df.copy()
    if league != 'All': fdf = fdf[fdf['League'] == league]
    if pos != 'All': fdf = fdf[fdf['Position'] == pos]
    fdf = fdf[(fdf['Age'] >= ages[0]) & (fdf['Age'] <= ages[1]) & (fdf['Min'] >= mins)]

    st.markdown(f'<div class="pill">✓ {len(fdf)} players found</div>', unsafe_allow_html=True)

    players = sorted(fdf['Player'].unique().tolist())
    if len(players) >= 2:
        c1, c2 = st.columns(2)
        with c1: p1 = st.selectbox("Select Player 1", players, index=0, key="p1")
        with c2: p2 = st.selectbox("Select Player 2", players, index=min(1, len(players)-1), key="p2")

        p1d, p2d = df[df['Player'] == p1].iloc[0], df[df['Player'] == p2].iloc[0]
        position = p1d['Position']

        if position == 'FW':
            metrics = ['Goals per 90', 'Assists per 90', 'xG per 90', 'xAG per 90', 'Shot Creating per 90', 'Prog Carries per 90']
            chart_names = ['Goals', 'Assists', 'xG', 'xAG', 'Shot Creating', 'Prog Carries']
        elif position == 'MF':
            metrics = ['Goals per 90', 'Assists per 90', 'Prog Passes per 90', 'Prog Carries per 90', 'Tackles per 90', 'Interceptions per 90']
            chart_names = ['Goals', 'Assists', 'Prog Passes', 'Prog Carries', 'Tackles', 'Interceptions']
        elif position == 'DF':
            metrics = ['Tackles per 90', 'Interceptions per 90', 'Prog Passes per 90', 'Prog Carries per 90', 'Goals per 90', 'Assists per 90']
            chart_names = ['Tackles', 'Interceptions', 'Prog Passes', 'Prog Carries', 'Goals', 'Assists']
        else:
            metrics = ['Goals per 90', 'Assists per 90', 'xG per 90', 'xAG per 90', 'Shot Creating per 90', 'Prog Carries per 90']
            chart_names = ['Goals', 'Assists', 'xG', 'xAG', 'Shot Creating', 'Prog Carries']

        pos_df = df[df['Position'] == position]
        def pct(d, m): return (pos_df[m] < d[m]).sum() / len(pos_df) * 100 if not pd.isna(d[m]) else 0

        v1, v2 = [pct(p1d, m) for m in metrics], [pct(p2d, m) for m in metrics]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=v1+[v1[0]], theta=chart_names+[chart_names[0]], fill='toself', name=p1, line=dict(color='#166534', width=3), fillcolor='rgba(22,101,52,0.2)'))
        fig.add_trace(go.Scatterpolar(r=v2+[v2[0]], theta=chart_names+[chart_names[0]], fill='toself', name=p2, line=dict(color='#3b82f6', width=3), fillcolor='rgba(59,130,246,0.2)'))
        fig.update_layout(
            polar=dict(bgcolor='#fafafa', radialaxis=dict(visible=True, range=[0,100], gridcolor='#e5e5e5'), angularaxis=dict(gridcolor='#e5e5e5', tickfont=dict(color='#166534', size=12))),
            showlegend=True, legend=dict(font=dict(color='#166534'), bgcolor='white'),
            paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#166534'), height=480, margin=dict(t=60,b=40,l=80,r=80)
        )
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'''<div class="player-card"><h3 style="color:#166534 !important;">🟢 {p1}</h3><p><strong>Team:</strong> {p1d['Squad']}</p><p><strong>League:</strong> {p1d['League']}</p><p><strong>Age:</strong> {int(p1d['Age'])} <span class="stat-chip">{p1d['Pos']}</span></p><p><strong>Minutes:</strong> {int(p1d['Min']):,}</p><hr style="border:none;border-top:1px solid #e0e5e1;margin:14px 0;"><p><strong>Goals:</strong> {int(p1d['Gls'])} <span style="color:#6b7b6b;">(xG: {p1d['xG']:.1f})</span></p><p><strong>Assists:</strong> {int(p1d['Ast'])} <span style="color:#6b7b6b;">(xAG: {p1d['xAG']:.1f})</span></p></div>''', unsafe_allow_html=True)
        with c2:
            st.markdown(f'''<div class="player-card"><h3 style="color:#3b82f6 !important;">🔵 {p2}</h3><p><strong>Team:</strong> {p2d['Squad']}</p><p><strong>League:</strong> {p2d['League']}</p><p><strong>Age:</strong> {int(p2d['Age'])} <span class="stat-chip">{p2d['Pos']}</span></p><p><strong>Minutes:</strong> {int(p2d['Min']):,}</p><hr style="border:none;border-top:1px solid #e0e5e1;margin:14px 0;"><p><strong>Goals:</strong> {int(p2d['Gls'])} <span style="color:#6b7b6b;">(xG: {p2d['xG']:.1f})</span></p><p><strong>Assists:</strong> {int(p2d['Ast'])} <span style="color:#6b7b6b;">(xAG: {p2d['xAG']:.1f})</span></p></div>''', unsafe_allow_html=True)
    else:
        st.warning("Adjust filters to show at least 2 players.")

elif st.session_state.page == 'similar':  # SIMILAR
    st.markdown('<p class="page-title">Find Similar Players</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Discover statistically similar players using machine learning</p>', unsafe_allow_html=True)

    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1:
        all_players = sorted(df['Player'].unique().tolist())
        selected_player = st.selectbox("Select a Player", all_players, key="sim_player")
    with c2:
        n_similar = st.selectbox("Show Top", [3, 5, 10], index=1, key="n_sim")
    st.markdown('</div>', unsafe_allow_html=True)

    player_data = df[df['Player'] == selected_player].iloc[0]
    st.markdown(f'''<div class="player-card">
        <h3 style="margin-bottom:12px;">Selected: {selected_player}</h3>
        <p><strong>Team:</strong> {player_data['Squad']} | <strong>League:</strong> {player_data['League']} | <strong>Position:</strong> <span class="stat-chip">{player_data['Position']}</span> | <strong>Age:</strong> {int(player_data['Age'])}</p>
        <p><strong>Stats:</strong> {int(player_data['Gls'])} goals, {int(player_data['Ast'])} assists, {player_data['xG']:.1f} xG in {int(player_data['Min'])} minutes</p>
    </div>''', unsafe_allow_html=True)

    similar = find_similar_players(selected_player, df, n_similar)

    if len(similar) > 0:
        st.markdown(f"### Top {n_similar} Similar Players")
        st.markdown(f"<p class='page-subtitle'>Based on per-90 metrics for {player_data['Position']} position</p>", unsafe_allow_html=True)

        for i, (_, row) in enumerate(similar.iterrows(), 1):
            sim_pct = int(row['Similarity'] * 100)
            st.markdown(f'''<div class="similar-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <strong style="font-size:1.1rem;">{i}. {row['Player']}</strong>
                        <p style="margin:4px 0;">{row['Squad']} • {row['League']} • Age {int(row['Age'])}</p>
                        <p style="margin:0;color:#6b7b6b !important;">{row['Goals per 90']:.2f} G/90 • {row['Assists per 90']:.2f} A/90</p>
                    </div>
                    <span class="similarity-score">{sim_pct}% match</span>
                </div>
            </div>''', unsafe_allow_html=True)

        st.markdown('''<div class="card" style="margin-top:1.5rem;">
            <h4>How it works</h4>
            <p>Uses <strong>cosine similarity</strong> on standardized per-90 metrics (goals, assists, xG, xAG, progressive carries/passes, tackles, interceptions). Players are compared only within their position group.</p>
        </div>''', unsafe_allow_html=True)

elif st.session_state.page == 'explore':  # EXPLORE
    st.markdown('<p class="page-title">Scatter Explorer</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Visualize player distributions across different metrics</p>', unsafe_allow_html=True)

    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns([1, 1, 1, 1, 1.2, 1.2])
    with c1: lg2 = st.selectbox("League", ['All'] + sorted(df['League'].unique().tolist()), key="s_lg")
    with c2: ps2 = st.selectbox("Position", ['All', 'FW', 'MF', 'DF', 'GK'], key="s_pos")
    with c3: mn2 = st.selectbox("Min Minutes", [450, 900, 1350, 1800], index=1, key="s_min")
    with c4: clr = st.selectbox("Color By", ['Position', 'League'], key="s_clr")
    metric_options = list(METRIC_NAMES.keys())
    with c5: xm = st.selectbox("X-Axis", metric_options, index=2, key="xm")
    with c6: ym = st.selectbox("Y-Axis", metric_options, index=0, key="ym")
    st.markdown('</div>', unsafe_allow_html=True)

    sdf = df.copy()
    if lg2 != 'All': sdf = sdf[sdf['League'] == lg2]
    if ps2 != 'All': sdf = sdf[sdf['Position'] == ps2]
    sdf = sdf[sdf['Min'] >= mn2]

    st.markdown(f'<div class="pill">✓ {len(sdf)} players</div>', unsafe_allow_html=True)

    cm = COLORS['positions'] if clr == 'Position' else COLORS['leagues']
    fig = px.scatter(sdf, x=xm, y=ym, color=clr, color_discrete_map=cm, hover_data=['Player', 'Squad', 'Age', 'Gls', 'Ast'], labels={xm: METRIC_NAMES[xm], ym: METRIC_NAMES[ym]}, opacity=0.85)
    fig.update_traces(marker=dict(size=11, line=dict(width=1.5, color='white')))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#fafafa', font=dict(color='#166534'), height=550, xaxis=dict(gridcolor='#e5e5e5'), yaxis=dict(gridcolor='#e5e5e5'), legend=dict(bgcolor='white'))
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.page == 'database':  # DATABASE
    st.markdown('<p class="page-title">Player Database</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Browse and filter the complete player database</p>', unsafe_allow_html=True)

    st.markdown('<div class="filter-card">', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns([1.2, 1.2, 1.2, 1.2, 2])
    with c1: lg3 = st.selectbox("League", ['All'] + sorted(df['League'].unique().tolist()), key="t_lg")
    with c2: ps3 = st.selectbox("Position", ['All', 'FW', 'MF', 'DF', 'GK'], key="t_pos")
    with c3: mn3 = st.selectbox("Min Minutes", [450, 900, 1350, 1800], index=1, key="t_min")
    with c4:
        sort_options = {'Goals + Assists per 90': 'G+A per 90', 'Goals per 90': 'Goals per 90', 'Assists per 90': 'Assists per 90', 'Expected Goals per 90': 'xG per 90', 'Minutes Played': 'Min'}
        srt_display = st.selectbox("Sort By", list(sort_options.keys()), key="srt")
        srt = sort_options[srt_display]
    with c5: ag3 = st.slider("Age Range", 16, 40, (18, 35), key="t_age")
    st.markdown('</div>', unsafe_allow_html=True)

    tdf = df.copy()
    if lg3 != 'All': tdf = tdf[tdf['League'] == lg3]
    if ps3 != 'All': tdf = tdf[tdf['Position'] == ps3]
    tdf = tdf[(tdf['Age'] >= ag3[0]) & (tdf['Age'] <= ag3[1]) & (tdf['Min'] >= mn3)]

    st.markdown(f'<div class="pill">✓ {len(tdf)} players</div>', unsafe_allow_html=True)

    display_cols = {'Player': 'Player', 'Squad': 'Team', 'League': 'League', 'Position': 'Pos', 'Age': 'Age', 'Min': 'Minutes', 'Gls': 'Goals', 'Ast': 'Assists', 'G+A': 'G+A', 'xG': 'xG', 'xAG': 'xAG', 'G+A per 90': 'G+A/90', 'Prog Carries per 90': 'PrgC/90'}
    cols = list(display_cols.keys())
    display_df = tdf[cols].copy()
    display_df.columns = list(display_cols.values())

    # Use st.table for guaranteed light background, or style dataframe
    st.dataframe(
        display_df.sort_values(display_cols.get(srt, srt), ascending=False).style.set_properties(**{'background-color': 'white', 'color': '#4a5d4a'}),
        use_container_width=True,
        height=500
    )
    st.download_button("📥 Download CSV", tdf[cols].to_csv(index=False), "players.csv", "text/csv")

elif st.session_state.page == 'about':  # ABOUT
    st.markdown('<p class="page-title">About This Tool</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Learn about the visualization, data, and methodology</p>', unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('''<div class="card">
            <h3 style="margin-bottom:12px;">Visualization Goals</h3>
            <p style="font-size:1.05rem;line-height:1.8;">
                This tool enables <strong>data-driven player scouting</strong> by providing interactive visualizations that help users:
            </p>
            <ul>
                <li>Compare players using radar charts with percentile rankings</li>
                <li>Discover similar players using machine learning (cosine similarity)</li>
                <li>Explore metric distributions across leagues and positions</li>
                <li>Filter and sort players by advanced statistics</li>
            </ul>
        </div>''', unsafe_allow_html=True)

        st.markdown('''<div class="card">
            <h3 style="margin-bottom:12px;">Key Metrics Explained</h3>
            <table>
                <tr><td style="width:160px;"><strong>xG (Expected Goals)</strong></td><td>Measures quality of scoring chances based on shot location and type</td></tr>
                <tr><td><strong>xAG (Expected Assists)</strong></td><td>Quality of chances created for teammates</td></tr>
                <tr><td><strong>Progressive Carries</strong></td><td>Ball carries that move significantly toward the opponent's goal</td></tr>
                <tr><td><strong>Progressive Passes</strong></td><td>Passes that move the ball significantly toward goal</td></tr>
                <tr><td><strong>SCA</strong></td><td>Shot-Creating Actions - actions leading directly to shots</td></tr>
            </table>
        </div>''', unsafe_allow_html=True)

        st.markdown('''<div class="card">
            <h3 style="margin-bottom:12px;">Technology Stack</h3>
            <p><strong>Why Streamlit?</strong> Chosen for rapid prototyping and native Python/Pandas integration.</p>
            <table>
                <tr><td style="width:140px;"><strong>Framework</strong></td><td>Streamlit (Python)</td></tr>
                <tr><td><strong>Visualization</strong></td><td>Plotly (interactive charts)</td></tr>
                <tr><td><strong>Data Processing</strong></td><td>Pandas, NumPy</td></tr>
                <tr><td><strong>ML (Similar Players)</strong></td><td>scikit-learn (cosine similarity)</td></tr>
            </table>
        </div>''', unsafe_allow_html=True)

    with c2:
        st.markdown('''<div class="card">
            <h3 style="margin-bottom:12px;">Intended Audience</h3>
            <ul>
                <li><strong>Fantasy Football Managers</strong></li>
                <li><strong>Football Enthusiasts</strong></li>
                <li><strong>Amateur Scouts</strong></li>
                <li><strong>Data Analysts</strong></li>
            </ul>
        </div>''', unsafe_allow_html=True)

        st.markdown('''<div class="card">
            <h3 style="margin-bottom:12px;">Data Source</h3>
            <p><strong>Source:</strong> FBref via Kaggle</p>
            <p><strong>Season:</strong> 2024-25</p>
            <p><strong>Coverage:</strong> Big 5 European Leagues</p>
            <p><strong>Players:</strong> ~2,500 with 450+ minutes</p>
        </div>''', unsafe_allow_html=True)

        st.markdown('''<div class="card" style="text-align:center;">
            <p style="color:#6b7b6b !important;font-size:0.85rem;margin-bottom:8px;">Created by</p>
            <p style="font-size:1.3rem;font-weight:700;color:#166534 !important;margin-bottom:4px;">Karim Mattar</p>
            <p style="color:#6b7b6b !important;">UC Berkeley MIDS<br>DS209 Data Visualization</p>
        </div>''', unsafe_allow_html=True)

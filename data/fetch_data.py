"""
Fetch player statistics from FBref for the Big 5 European Leagues
"""

import pandas as pd
import requests
from io import StringIO
import time
import os

# FBref URLs for Big 5 leagues player stats (2024-2025 season)
LEAGUE_URLS = {
    'Premier_League': 'https://fbref.com/en/comps/9/stats/Premier-League-Stats',
    'La_Liga': 'https://fbref.com/en/comps/12/stats/La-Liga-Stats',
    'Bundesliga': 'https://fbref.com/en/comps/20/stats/Bundesliga-Stats',
    'Serie_A': 'https://fbref.com/en/comps/11/stats/Serie-A-Stats',
    'Ligue_1': 'https://fbref.com/en/comps/13/stats/Ligue-1-Stats',
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_league_stats(url, league_name):
    """Fetch player stats table from FBref"""
    print(f"Fetching {league_name}...")
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()

        # Read all tables from the HTML
        tables = pd.read_html(StringIO(response.text))

        # The main stats table is usually one of the first few
        for i, table in enumerate(tables):
            cols = table.columns.tolist()
            # Check for Player column (handle multi-index)
            has_player = any('Player' in str(c) for c in cols)
            if has_player and len(table) > 20:  # Main table has many rows
                df = table.copy()
                # Handle multi-level columns
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = ['_'.join([str(c) for c in col]).strip() for col in df.columns.values]
                df['League'] = league_name
                # Remove rows that are headers repeated in table
                df = df[df.iloc[:, 0] != 'Player']
                df = df[df.iloc[:, 0] != 'Rk']
                print(f"  Found {len(df)} players")
                return df

        print(f"  Warning: Could not find player table")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

def main():
    all_players = []

    for league_name, url in LEAGUE_URLS.items():
        df = fetch_league_stats(url, league_name)
        if df is not None:
            all_players.append(df)
        # Be respectful to FBref servers - they rate limit
        print("  Waiting 5 seconds...")
        time.sleep(5)

    if all_players:
        # Combine all leagues
        combined_df = pd.concat(all_players, ignore_index=True)

        # Save to CSV
        output_path = os.path.join(os.path.dirname(__file__), 'player_stats_2024_2025.csv')
        combined_df.to_csv(output_path, index=False)
        print(f"\nSaved {len(combined_df)} players to {output_path}")

        # Also save a summary
        print("\nLeague breakdown:")
        print(combined_df['League'].value_counts())

        # Print columns
        print("\nColumns available:")
        print(combined_df.columns.tolist()[:20], "...")
    else:
        print("No data fetched!")

if __name__ == "__main__":
    main()

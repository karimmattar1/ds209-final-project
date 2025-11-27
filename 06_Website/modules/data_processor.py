"""
Data processing module for Football Scout Tool
Handles data loading, cleaning, and feature engineering
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

class FootballDataProcessor:
    """Process and prepare football player statistics for visualization"""

    def __init__(self, data_path):
        """Initialize with path to CSV data"""
        self.data_path = data_path
        self.df = None
        self.df_filtered = None
        self.scaler = StandardScaler()

    def load_and_clean(self, min_minutes=450):
        """Load data and apply basic cleaning"""
        self.df = pd.read_csv(self.data_path)

        # Filter for players with meaningful playing time
        self.df_filtered = self.df[self.df['Min'] >= min_minutes].copy()

        # Create per-90 metrics
        self._create_per90_metrics()

        # Simplify positions
        self.df_filtered['Position'] = self.df_filtered['Pos'].apply(self._simplify_position)

        # Create age groups
        self.df_filtered['Age_Group'] = pd.cut(
            self.df_filtered['Age'],
            bins=[0, 21, 23, 27, 32, 50],
            labels=['U21', '21-23', '24-27', '28-32', '33+']
        )

        # Performance vs expectation
        self.df_filtered['Goals_minus_xG'] = self.df_filtered['Gls'] - self.df_filtered['xG']
        self.df_filtered['Ast_minus_xAG'] = self.df_filtered['Ast'] - self.df_filtered['xAG']

        # Clean player names
        self.df_filtered['Player_Clean'] = self.df_filtered['Player'].str.strip()

        return self.df_filtered

    def _create_per90_metrics(self):
        """Create per-90 minute statistics"""
        metrics = [
            ('Gls', 'Gls_per90'),
            ('Ast', 'Ast_per90'),
            ('xG', 'xG_per90'),
            ('xAG', 'xAG_per90'),
            ('G+A', 'G+A_per90'),
            ('PrgC', 'PrgC_per90'),
            ('Tkl', 'Tkl_per90'),
            ('Int', 'Int_per90'),
            ('Blocks', 'Blocks_per90'),
            ('Sh', 'Sh_per90'),
            ('SoT', 'SoT_per90'),
            ('Touches', 'Touches_per90'),
            ('PrgP', 'PrgP_per90'),
            ('CrsPA', 'CrsPA_per90'),
            ('Carries', 'Carries_per90'),
        ]

        for original, per90 in metrics:
            if original in self.df_filtered.columns:
                self.df_filtered[per90] = self.df_filtered[original] / self.df_filtered['90s']

        # Combined metrics
        if 'xG' in self.df_filtered.columns and 'xAG' in self.df_filtered.columns:
            self.df_filtered['xGxAG_per90'] = (
                self.df_filtered['xG'] + self.df_filtered['xAG']
            ) / self.df_filtered['90s']

    @staticmethod
    def _simplify_position(pos):
        """Simplify position strings to main categories"""
        if pd.isna(pos):
            return 'Unknown'
        pos_upper = str(pos).upper()
        if 'GK' in pos_upper:
            return 'GK'
        elif 'FW' in pos_upper:
            return 'FW'
        elif 'MF' in pos_upper:
            return 'MF'
        elif 'DF' in pos_upper:
            return 'DF'
        return 'Unknown'

    def get_player_data(self, player_name):
        """Get all data for a specific player"""
        return self.df_filtered[
            self.df_filtered['Player_Clean'].str.contains(player_name, case=False, na=False)
        ]

    def get_players_by_filters(self, positions=None, leagues=None, age_min=None, age_max=None, teams=None):
        """Filter players by multiple criteria"""
        df = self.df_filtered.copy()

        if positions:
            df = df[df['Position'].isin(positions)]

        if leagues:
            df = df[df['Comp'].isin(leagues)]

        if age_min:
            df = df[df['Age'] >= age_min]

        if age_max:
            df = df[df['Age'] <= age_max]

        if teams:
            df = df[df['Squad'].isin(teams)]

        return df

    def find_similar_players(self, player_name, n_similar=10, position_filter=True):
        """Find statistically similar players using cosine similarity"""
        player_data = self.get_player_data(player_name)

        if len(player_data) == 0:
            return pd.DataFrame()

        player = player_data.iloc[0]
        position = player['Position']

        # Filter to same position if requested
        if position_filter and position != 'Unknown':
            comparison_df = self.df_filtered[self.df_filtered['Position'] == position].copy()
        else:
            comparison_df = self.df_filtered.copy()

        # Key metrics for similarity
        metrics = [
            'Gls_per90', 'Ast_per90', 'xG_per90', 'xAG_per90',
            'PrgC_per90', 'Tkl_per90', 'Int_per90', 'Touches_per90',
            'Cmp%', 'PrgP_per90'
        ]

        # Filter to available metrics
        available_metrics = [m for m in metrics if m in comparison_df.columns]

        # Prepare data for similarity calculation
        X = comparison_df[available_metrics].fillna(0)
        player_vector = player[available_metrics].fillna(0).values.reshape(1, -1)

        # Calculate cosine similarity
        similarities = cosine_similarity(player_vector, X)[0]

        # Add similarity scores
        comparison_df['Similarity'] = similarities

        # Exclude the player themselves
        comparison_df = comparison_df[
            comparison_df['Player_Clean'] != player['Player_Clean']
        ]

        # Return top N similar players
        return comparison_df.nlargest(n_similar, 'Similarity')[
            ['Player_Clean', 'Squad', 'Comp', 'Position', 'Age', 'Similarity'] + available_metrics
        ]

    def get_position_specific_metrics(self, position):
        """Get the most relevant metrics for each position"""
        metrics_by_position = {
            'GK': ['Saves', 'Save%', 'CS%', 'PSxG', 'Cmp%'],
            'DF': ['Tkl_per90', 'Int_per90', 'Blocks_per90', 'PrgP_per90', 'Cmp%', 'Clr'],
            'MF': ['xGxAG_per90', 'PrgC_per90', 'PrgP_per90', 'Cmp%', 'Touches_per90', 'Tkl_per90'],
            'FW': ['Gls_per90', 'xG_per90', 'Sh_per90', 'SoT_per90', 'G-xG', 'Touches_per90']
        }

        return metrics_by_position.get(position, [])

    def get_percentile_ranks(self, player_name, metrics):
        """Calculate percentile ranks for a player across specified metrics"""
        player_data = self.get_player_data(player_name)

        if len(player_data) == 0:
            return {}

        player = player_data.iloc[0]
        position = player['Position']

        # Compare within same position
        position_players = self.df_filtered[self.df_filtered['Position'] == position]

        percentiles = {}
        for metric in metrics:
            if metric in position_players.columns:
                player_value = player[metric]
                if pd.notna(player_value):
                    percentile = (position_players[metric] < player_value).sum() / len(position_players) * 100
                    percentiles[metric] = percentile
                else:
                    percentiles[metric] = 0

        return percentiles

    def get_leagues(self):
        """Get list of all leagues"""
        return sorted(self.df_filtered['Comp'].unique())

    def get_teams(self, league=None):
        """Get list of teams, optionally filtered by league"""
        if league:
            return sorted(self.df_filtered[self.df_filtered['Comp'] == league]['Squad'].unique())
        return sorted(self.df_filtered['Squad'].unique())

    def get_positions(self):
        """Get list of positions"""
        return sorted([p for p in self.df_filtered['Position'].unique() if p != 'Unknown'])

    def get_player_list(self, position=None, league=None):
        """Get list of player names, optionally filtered"""
        df = self.df_filtered.copy()

        if position:
            df = df[df['Position'] == position]

        if league:
            df = df[df['Comp'] == league]

        return sorted(df['Player_Clean'].unique())

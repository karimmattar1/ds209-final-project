"""
Altair visualization modules for Football Scout Tool
All charts use Altair for interactivity
"""

import altair as alt
import pandas as pd
import numpy as np


class PlayerVisualizations:
    """Create interactive Altair visualizations for player analysis"""

    def __init__(self):
        # Enable larger datasets
        alt.data_transformers.disable_max_rows()

        # Color schemes
        self.league_colors = {
            'Premier League': '#3D195B',
            'La Liga': '#EE8707',
            'Bundesliga': '#D20515',
            'Serie A': '#024494',
            'Ligue 1': '#00529B',
            'fr Ligue 1': '#00529B',
            'eng Premier League': '#3D195B',
            'es La Liga': '#EE8707',
            'de Bundesliga': '#D20515',
            'it Serie A': '#024494'
        }

        self.position_colors = {
            'GK': '#FDB913',
            'DF': '#00A650',
            'MF': '#0072CE',
            'FW': '#EF3340'
        }

    def create_radar_chart(self, player1_data, player2_data, metrics):
        """Create radar chart comparing two players"""
        # Prepare data for radar chart
        categories = []
        player1_values = []
        player2_values = []

        for metric in metrics:
            if metric in player1_data and metric in player2_data:
                categories.append(metric)
                player1_values.append(float(player1_data[metric]))
                player2_values.append(float(player2_data[metric]))

        if not categories:
            return alt.Chart().mark_text(text="No data available for comparison")

        # Create DataFrame for plotting
        data = pd.DataFrame({
            'Metric': categories * 2,
            'Value': player1_values + player2_values,
            'Player': [player1_data['Player_Clean']] * len(categories) +
                     [player2_data['Player_Clean']] * len(categories)
        })

        # Calculate angles for each metric
        n_metrics = len(categories)
        angles = [(i * 360 / n_metrics) for i in range(n_metrics)]
        data['Angle'] = angles * 2

        # Convert to radians and calculate x, y coordinates
        data['Angle_rad'] = data['Angle'] * np.pi / 180
        data['X'] = data['Value'] * np.cos(data['Angle_rad'])
        data['Y'] = data['Value'] * np.sin(data['Angle_rad'])

        # Create the base chart
        base = alt.Chart(data).encode(
            x=alt.X('X:Q', axis=None, scale=alt.Scale(domain=[-1.2, 1.2])),
            y=alt.Y('Y:Q', axis=None, scale=alt.Scale(domain=[-1.2, 1.2])),
            color=alt.Color('Player:N', legend=alt.Legend(title='Player', orient='top'))
        )

        # Create lines connecting the points
        lines = base.mark_line(point=True, strokeWidth=2).encode(
            order='Metric:N',
            tooltip=['Player:N', 'Metric:N', alt.Tooltip('Value:Q', format='.2f')]
        )

        # Create text labels for metrics
        label_data = pd.DataFrame({
            'Metric': categories,
            'Angle': angles
        })
        label_data['Angle_rad'] = label_data['Angle'] * np.pi / 180
        label_data['X'] = 1.15 * np.cos(label_data['Angle_rad'])
        label_data['Y'] = 1.15 * np.sin(label_data['Angle_rad'])

        labels = alt.Chart(label_data).mark_text(
            fontSize=11,
            fontWeight='bold'
        ).encode(
            x='X:Q',
            y='Y:Q',
            text='Metric:N'
        )

        # Combine
        chart = (lines + labels).properties(
            width=500,
            height=500,
            title={
                'text': f"Player Comparison: {player1_data['Player_Clean']} vs {player2_data['Player_Clean']}",
                'fontSize': 16
            }
        ).configure_view(
            strokeWidth=0
        )

        return chart

    def create_scatter_explorer(self, df, x_metric, y_metric, color_by='Position', size_metric=None):
        """Create interactive scatter plot for exploring player metrics"""
        # Create selection for interaction
        selection = alt.selection_point(fields=['Player_Clean'], on='mouseover', empty=False)

        base = alt.Chart(df).encode(
            x=alt.X(f'{x_metric}:Q',
                   title=x_metric.replace('_', ' ').title(),
                   scale=alt.Scale(zero=False)),
            y=alt.Y(f'{y_metric}:Q',
                   title=y_metric.replace('_', ' ').title(),
                   scale=alt.Scale(zero=False)),
            tooltip=[
                alt.Tooltip('Player_Clean:N', title='Player'),
                alt.Tooltip('Squad:N', title='Team'),
                alt.Tooltip('Comp:N', title='League'),
                alt.Tooltip('Position:N', title='Position'),
                alt.Tooltip('Age:Q', title='Age'),
                alt.Tooltip(f'{x_metric}:Q', title=x_metric, format='.2f'),
                alt.Tooltip(f'{y_metric}:Q', title=y_metric, format='.2f')
            ]
        )

        # Size encoding
        if size_metric and size_metric in df.columns:
            base = base.encode(
                size=alt.Size(f'{size_metric}:Q',
                            title=size_metric.replace('_', ' ').title(),
                            scale=alt.Scale(range=[50, 500]))
            )
        else:
            base = base.encode(size=alt.value(100))

        # Color encoding
        if color_by == 'Position':
            color_scale = alt.Scale(
                domain=list(self.position_colors.keys()),
                range=list(self.position_colors.values())
            )
        elif color_by == 'Comp':
            # Use league colors if available, otherwise default scheme
            color_scale = alt.Scale(scheme='tableau10')
        else:
            color_scale = alt.Scale(scheme='tableau10')

        base = base.encode(
            color=alt.Color(f'{color_by}:N',
                          title=color_by,
                          scale=color_scale,
                          legend=alt.Legend(orient='right'))
        )

        # Points
        points = base.mark_circle(opacity=0.7).encode(
            opacity=alt.condition(selection, alt.value(1.0), alt.value(0.4))
        ).add_params(selection)

        # Chart
        chart = points.properties(
            width=700,
            height=500,
            title={
                'text': f'{y_metric.replace("_", " ").title()} vs {x_metric.replace("_", " ").title()}',
                'fontSize': 16
            }
        ).interactive()

        return chart

    def create_player_comparison_bars(self, player1_data, player2_data, metrics):
        """Create grouped bar chart comparing two players"""
        categories = []
        values = []
        players = []

        for metric in metrics:
            if metric in player1_data.index and metric in player2_data.index:
                categories.extend([metric, metric])
                values.extend([float(player1_data[metric]), float(player2_data[metric])])
                players.extend([player1_data['Player_Clean'], player2_data['Player_Clean']])

        df = pd.DataFrame({
            'Metric': categories,
            'Value': values,
            'Player': players
        })

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Metric:N', title='', axis=alt.Axis(labelAngle=-45)),
            y=alt.Y('Value:Q', title='Value'),
            color=alt.Color('Player:N', legend=alt.Legend(title='Player', orient='top')),
            xOffset='Player:N',
            tooltip=['Player:N', 'Metric:N', alt.Tooltip('Value:Q', format='.2f')]
        ).properties(
            width=600,
            height=400,
            title={
                'text': 'Statistical Comparison',
                'fontSize': 14
            }
        )

        return chart

    def create_distribution_plot(self, df, metric, position=None):
        """Create histogram showing distribution of a metric"""
        if position:
            df = df[df['Position'] == position]
            title = f'Distribution of {metric.replace("_", " ").title()} for {position}s'
        else:
            title = f'Distribution of {metric.replace("_", " ").title()}'

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X(f'{metric}:Q',
                   bin=alt.Bin(maxbins=30),
                   title=metric.replace('_', ' ').title()),
            y=alt.Y('count()', title='Number of Players'),
            tooltip=[
                alt.Tooltip(f'{metric}:Q', bin=True, title=metric),
                alt.Tooltip('count()', title='Count')
            ]
        ).properties(
            width=600,
            height=300,
            title={'text': title, 'fontSize': 14}
        )

        return chart

    def create_league_comparison(self, df, metric):
        """Create box plots comparing a metric across leagues"""
        chart = alt.Chart(df).mark_boxplot(extent='min-max').encode(
            x=alt.X('Comp:N', title='League', axis=alt.Axis(labelAngle=-45)),
            y=alt.Y(f'{metric}:Q', title=metric.replace('_', ' ').title()),
            color=alt.Color('Comp:N', legend=None)
        ).properties(
            width=600,
            height=400,
            title={
                'text': f'{metric.replace("_", " ").title()} by League',
                'fontSize': 14
            }
        )

        return chart

    def create_similar_players_chart(self, similar_df):
        """Create bar chart showing similar players and their similarity scores"""
        chart = alt.Chart(similar_df.head(10)).mark_bar().encode(
            x=alt.X('Similarity:Q', title='Similarity Score', scale=alt.Scale(domain=[0, 1])),
            y=alt.Y('Player_Clean:N',
                   title='Player',
                   sort='-x'),
            color=alt.Color('Comp:N', title='League', scale=alt.Scale(scheme='tableau10')),
            tooltip=[
                alt.Tooltip('Player_Clean:N', title='Player'),
                alt.Tooltip('Squad:N', title='Team'),
                alt.Tooltip('Comp:N', title='League'),
                alt.Tooltip('Age:Q', title='Age'),
                alt.Tooltip('Similarity:Q', title='Similarity', format='.3f')
            ]
        ).properties(
            width=600,
            height=400,
            title={
                'text': 'Most Similar Players',
                'fontSize': 14
            }
        )

        return chart

    def create_age_progression_chart(self, df, metric):
        """Create line chart showing how a metric varies with age"""
        # Calculate average by age
        age_data = df.groupby('Age')[metric].mean().reset_index()

        chart = alt.Chart(age_data).mark_line(point=True, strokeWidth=3).encode(
            x=alt.X('Age:Q', title='Age'),
            y=alt.Y(f'{metric}:Q', title=metric.replace('_', ' ').title()),
            tooltip=[
                alt.Tooltip('Age:Q', title='Age'),
                alt.Tooltip(f'{metric}:Q', title=metric, format='.2f')
            ]
        ).properties(
            width=600,
            height=300,
            title={
                'text': f'{metric.replace("_", " ").title()} by Age',
                'fontSize': 14
            }
        )

        return chart

    def create_top_players_chart(self, df, metric, n=20, position=None):
        """Create bar chart of top N players by metric"""
        if position:
            df = df[df['Position'] == position]
            title = f'Top {n} {position}s by {metric.replace("_", " ").title()}'
        else:
            title = f'Top {n} Players by {metric.replace("_", " ").title()}'

        top_players = df.nlargest(n, metric)

        chart = alt.Chart(top_players).mark_bar().encode(
            x=alt.X(f'{metric}:Q', title=metric.replace('_', ' ').title()),
            y=alt.Y('Player_Clean:N',
                   title='Player',
                   sort='-x'),
            color=alt.Color('Comp:N', title='League', scale=alt.Scale(scheme='tableau10')),
            tooltip=[
                alt.Tooltip('Player_Clean:N', title='Player'),
                alt.Tooltip('Squad:N', title='Team'),
                alt.Tooltip('Comp:N', title='League'),
                alt.Tooltip('Position:N', title='Position'),
                alt.Tooltip(f'{metric}:Q', title=metric, format='.2f')
            ]
        ).properties(
            width=600,
            height=500,
            title={'text': title, 'fontSize': 14}
        )

        return chart

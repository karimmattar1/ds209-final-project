DS209 Final Project Proposal

Karim Mattar
UC Berkeley MIDS


PROJECT CONCEPT: FOOTBALL PLAYER SCOUT TOOL

I'm building an interactive web-based visualization tool that helps users discover, compare, and analyze football players across Europe's top 5 leagues. The tool enables data-driven player scouting by visualizing performance metrics, identifying similar players, and letting users explore statistical trends in an intuitive way.

The leagues covered are the Premier League (England), La Liga (Spain), Bundesliga (Germany), Serie A (Italy), and Ligue 1 (France).


TARGET USERS

The primary users are fantasy football managers looking for undervalued players and wanting to compare options, casual fans who want to understand player performance beyond just goals and assists, and data-curious football enthusiasts interested in exploring advanced metrics like expected goals and progressive passes.

Secondary users include amateur scouts and analysts, football bloggers and content creators, and students studying sports analytics.


TASKS USERS WILL PERFORM

Users will be able to compare players by selecting two players and viewing side-by-side radar charts showing key metrics with percentile rankings. They can filter and discover players by position, age, league, team, and statistical thresholds. The tool lets users find similar players by selecting any player and discovering statistically similar alternatives, which is useful for finding budget options or replacement targets. Users can explore metrics through interactive scatter plots and understand what advanced stats mean through the visualizations. Finally, they can analyze players by position, viewing position-specific metrics that matter most for each role.


EXAMPLE INSIGHTS

The visualization will help answer questions like "Which young midfielders under 23 have the best expected goal contributions per 90 minutes?" to identify breakout talents before they become household names. Users can ask "How does Salah compare to other Premier League wingers this season?" to contextualize star players against their peers. They can explore "Which defenders provide the most progressive passing?" to find ball-playing center-backs for possession-based tactics. And they can discover "Who are the most clinical finishers outperforming their expected goals?" to find players who convert chances at elite rates.


DATA SOURCE

The primary dataset is Football Players Stats 2024-2025 from Kaggle, originally sourced from FBref (Football Reference). It contains over 250 columns of statistics for approximately 2,500 players and is updated weekly in CSV format.

The key metrics available include basic information like name, age, position, team, league, and nationality. Playing time metrics include matches, starts, minutes, and 90s played. Attacking metrics cover goals, assists, expected goals, expected assists, shots, and shot accuracy. Passing metrics include pass completion percentage, progressive passes, and key passes. Defending metrics cover tackles, interceptions, blocks, and clearances. Possession metrics include touches, carries, progressive carries, and take-ons.


PROPOSED VISUALIZATIONS

The tool will feature radar charts for multi-dimensional player comparison, scatter plots for two-metric comparisons with player labels, player cards showing summary stats with percentile rankings, sortable and filterable data tables, and a similar players feature using statistical clustering.


TECHNOLOGY STACK

Data processing will use Python with Pandas. The web framework will be Streamlit with Plotly for interactive visualizations. The application will be hosted on Streamlit Cloud.

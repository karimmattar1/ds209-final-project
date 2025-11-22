# DS209 Final Project Proposal

## Team Members
- Karim Mattar (Solo Project)

---

## Project Concept: Football Player Scout Tool

### Overview
An interactive web-based visualization tool that helps users discover, compare, and analyze football (soccer) players across Europe's top 5 leagues. The tool enables data-driven player scouting by visualizing performance metrics, identifying similar players, and tracking statistical trends.

### Target Leagues
- Premier League (England)
- La Liga (Spain)
- Bundesliga (Germany)
- Serie A (Italy)
- Ligue 1 (France)

---

## Target Users

### Primary Users
1. **Fantasy Football Managers** - Looking for undervalued players, comparing options, tracking form
2. **Casual Fans** - Wanting to understand player performance beyond goals/assists
3. **Data-curious Football Enthusiasts** - Exploring advanced metrics like xG, progressive passes, etc.

### Secondary Users
- Amateur scouts and analysts
- Football bloggers/content creators
- Students studying sports analytics

---

## Key Tasks Users Will Perform

1. **Compare Players** - Select 2-4 players and view side-by-side radar charts showing key metrics
2. **Filter & Discover** - Filter players by position, age, league, team, and statistical thresholds
3. **Find Similar Players** - Select a player and discover statistically similar alternatives (useful for finding budget options)
4. **Explore Metrics** - Understand what advanced stats mean (xG, progressive carries, etc.) through interactive tooltips
5. **Analyze by Position** - View position-specific metrics (e.g., save % for goalkeepers, tackle success for defenders)

---

## Example Insights

1. **"Which young midfielders (<23) have the best xG+xA per 90 minutes?"**
   - Insight: Identify breakout talents before they become household names

2. **"How does Salah compare to other Premier League wingers this season?"**
   - Insight: Contextualize star players against their peers using radar charts

3. **"Which defenders provide the most progressive passing?"**
   - Insight: Find ball-playing center-backs for possession-based tactics

4. **"Who are the most undervalued players based on performance vs. playing time?"**
   - Insight: Discover hidden gems getting limited minutes but excelling when they play

---

## Data Source

### Primary Dataset
**Football Players Stats (2024-2025)** - Kaggle
- Source: https://www.kaggle.com/datasets/hubertsidorowicz/football-players-stats-2024-2025
- Origin: FBref (Football Reference)
- Size: 250+ columns, ~2500 players
- Update frequency: Weekly
- Format: CSV

### Key Metrics Available
| Category | Example Metrics |
|----------|-----------------|
| Basic | Name, Age, Position, Team, League, Nationality |
| Playing Time | Matches, Starts, Minutes, 90s played |
| Attacking | Goals, Assists, xG, xAG, Shots, Shot accuracy |
| Passing | Pass completion %, Progressive passes, Key passes |
| Defending | Tackles, Interceptions, Blocks, Clearances |
| Possession | Touches, Carries, Progressive carries, Take-ons |
| Goalkeeping | Save %, Clean sheets, Goals conceded, xG prevented |

---

## Proposed Visualizations

1. **Radar/Spider Charts** - Multi-dimensional player comparison
2. **Scatter Plots** - Two-metric comparisons with player labels (e.g., xG vs Goals)
3. **Player Cards** - Summary view with key stats and percentile rankings
4. **Data Tables** - Sortable, filterable player lists
5. **Distribution Charts** - Show where a player ranks vs. peers
6. **Similar Players Network** - Visual clustering of statistically similar players

---

## Technology Stack

| Component | Tool |
|-----------|------|
| Data Processing | Python (Pandas) |
| Exploratory Viz | Altair / Tableau |
| Web Framework | Observable / D3.js |
| Hosting | DigitalOcean / GitHub Pages |

---

## Team Charter

### Communication
- Primary: Slack/Discord group chat
- Secondary: Email for formal submissions
- Response time: Within 24 hours

### Meetings
- Weekly sync: [Day/Time TBD]
- Location: Zoom / In-person as needed
- Ad-hoc meetings as needed before deadlines

### Workload Balance
- Tasks assigned based on strengths and availability
- Rotate presentation responsibilities
- All members contribute to usability testing (3 subjects each)

### Conflict Resolution
1. Discuss openly in team meeting
2. If unresolved, seek instructor guidance
3. Document all major decisions

### Accountability
- Missed deadline = team discussion within 24 hours
- Consistent issues = escalate to instructor

---

## Timeline (Rough)

| Milestone | Deliverable |
|-----------|-------------|
| Week 1-2 | Exploratory Visualization |
| Week 3-4 | Prototype Development |
| Week 5 | Midterm Presentation |
| Week 6-7 | Usability Testing |
| Week 8 | Final Presentation & Website |

---

## Questions for Instructor
1. Is the scope appropriate for a team of [X] members?
2. Any concerns with using Kaggle-sourced FBref data?
3. Suggestions for making the "similar players" feature more robust?

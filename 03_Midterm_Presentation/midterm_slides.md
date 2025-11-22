# Football Player Scout Tool
## DS209 Data Visualization - Midterm Presentation
### Karim Mattar | UC Berkeley MIDS

---

# Problem Statement

**Challenge:** Football scouts and analysts need to efficiently compare players across leagues

- Manually comparing player statistics is time-consuming
- Traditional scouting relies on subjective assessment
- Difficulty finding similar players across different leagues
- No unified tool for position-specific analysis

---

# Solution: Scout Tool

An interactive web application for football player analysis

**Key Features:**
- Side-by-side player comparison with radar charts
- Find similar players using machine learning (cosine similarity)
- Position-based exploration with scatter plots
- Searchable player database with filters

---

# Data Source

**FBref 2024-2025 Season Data**

| Metric | Value |
|--------|-------|
| Players | ~2,500 (450+ minutes played) |
| Leagues | Big 5 European (Premier League, La Liga, Bundesliga, Serie A, Ligue 1) |
| Statistics | 50+ metrics per player |
| Categories | Goals, assists, xG, xAG, progressive actions, defensive stats |

---

# Visualization 1: Player Comparison

**Radar Chart with Percentile Rankings**

- Compares two players across 10 key metrics
- Uses percentile rankings for fair comparison
- Position-filtered for meaningful comparisons
- Color-coded for easy differentiation

*Example: Comparing Erling Haaland vs Kylian Mbappe*

---

# Visualization 2: Find Similar Players

**Cosine Similarity Algorithm**

- Selects a player and finds statistically similar alternatives
- Uses position-specific metrics for accurate matching
- Shows similarity scores (0-100%)
- Useful for finding transfer targets or replacements

*Key insight: Discovers hidden gems in smaller leagues*

---

# Visualization 3: Position Explorer

**Interactive Scatter Plots**

- X/Y axis selection from 15+ metrics
- Filter by position, league, age range
- Hover for detailed player info
- Identify outliers and trends

*Example: xG vs Goals reveals clinical finishers*

---

# Technical Implementation

**Stack:**
- Frontend: Streamlit with custom CSS
- Charts: Plotly (interactive)
- ML: scikit-learn (StandardScaler, cosine_similarity)
- Data: Pandas, NumPy

**Deployment:** Streamlit Cloud (live URL available)

---

# Design Decisions

1. **Green color scheme** - Associated with football pitches
2. **Card-based layout** - Clean, modern aesthetic
3. **Pill-shaped navigation** - Intuitive tab switching
4. **Minimal sidebar** - Maximizes chart space
5. **White backgrounds** - Professional, readable

---

# Next Steps

1. **Usability Study** - Test with 3 users, gather feedback
2. **Iterate on UI** - Improve based on user insights
3. **Record Demo Video** - 2-3 minute walkthrough
4. **Final Presentation** - Complete project showcase

---

# Live Demo

**Scout Tool**

[Live App URL]

*Demo: Player comparison, similar players, and exploration features*

---

# Thank You

**Questions?**

Karim Mattar
UC Berkeley MIDS
DS209 Data Visualization

GitHub: github.com/karimmattar1/ds209-final-project

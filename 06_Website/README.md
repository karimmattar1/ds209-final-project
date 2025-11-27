# Football Scout Tool

An interactive web-based visualization tool for discovering, comparing, and analyzing professional football (soccer) players across Europe's Top 5 Leagues.

**Created by:** Karim Mattar
**Course:** DS209 Final Project, UC Berkeley MIDS
**Season:** 2024-2025

---

## Features

- **Player Comparison:** Side-by-side radar charts and statistical comparisons
- **Interactive Explorer:** Scatter plots with dynamic filtering by position, age, league, and team
- **Similar Players Finder:** Discover statistically similar players using advanced metrics
- **Position Analysis:** View position-specific top performers and league comparisons
- **Interactive Visualizations:** All charts built with Altair (Vega-Lite) for rich interactivity

---

## Tech Stack

- **Visualization:** Altair (Vega-Lite) - primary visualization tool
- **Frontend:** HTML5, CSS3, JavaScript (ES6)
- **Data Processing:** Python, Pandas, scikit-learn
- **Deployment:** Static site (Berkeley iSchool server compatible)

---

## Project Structure

```
06_Website/
├── index.html              # Home page
├── explore.html            # Interactive scatter plots
├── compare.html            # Player comparison
├── similar.html            # Similar players finder
├── analysis.html           # Position analysis
├── generate_charts.py      # Python script to generate visualizations
├── run_server.py          # Local development server
├── modules/
│   ├── data_processor.py   # Data cleaning and processing
│   └── visualizations.py   # Altair chart creation functions
├── static/
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   ├── js/
│   │   ├── app.js          # Main JavaScript
│   │   ├── explore.js      # Explorer page logic
│   │   ├── compare.js      # Comparison page logic
│   │   └── similar.js      # Similar players logic
│   ├── charts/             # Generated Altair charts (HTML)
│   └── data/               # Processed data (JSON)
└── README.md              # This file
```

---

## Data Source

**Dataset:** [Football Players Stats 2024-2025](https://www.kaggle.com/datasets/hubertsidorowicz/football-players-stats-2024-2025)
**Original Source:** FBref (Football Reference)
**Coverage:** 2,000+ players across 5 leagues (Premier League, La Liga, Bundesliga, Serie A, Ligue 1)
**Statistics:** 250+ metrics including goals, assists, expected goals (xG), progressive carries, tackles, and more

---

## Setup and Installation

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install pandas numpy altair scikit-learn
   ```

2. **Generate visualizations and data:**
   ```bash
   cd 06_Website
   python3 generate_charts.py
   ```

   This will create:
   - Altair charts in `static/charts/`
   - Processed data in `static/data/`

3. **Run local server:**
   ```bash
   python3 run_server.py
   ```

4. **Open in browser:**
   - Navigate to: http://localhost:8000

---

## Usage

### Home Page
- Overview of features and leagues covered
- Quick navigation to all tools

### Player Explorer
- Select X and Y axis metrics
- Filter by position and league
- Interactive scatter plot with hover tooltips
- Export charts as images

### Player Comparison
- Search for two players
- View side-by-side player cards
- Interactive bar chart comparison
- All metrics normalized per 90 minutes

### Similar Players Finder
- Enter a player name
- Choose to filter by position or search all positions
- View similarity scores and player profiles
- Based on cosine similarity across multiple metrics

### Position Analysis
- Top performers by position (GK, DF, MF, FW)
- League-wide comparisons
- Position-specific metrics

---

## Key Metrics Explained

- **xG (Expected Goals):** Quality of scoring chances based on historical data
- **xAG (Expected Assisted Goals):** Quality of chances created for teammates
- **Progressive Carries:** Times a player moves the ball significantly closer to goal
- **per 90:** All metrics normalized per 90 minutes for fair comparison
- **Cmp%:** Pass completion percentage
- **Tkl:** Tackles made

---

## Deployment to Berkeley iSchool Server

The site is designed as a static website that can be deployed to any web server:

1. Upload the entire `06_Website/` folder to your server
2. Ensure all files maintain their relative paths
3. The site requires no backend - all processing is client-side or pre-generated

### File Checklist for Deployment:
- [ ] All HTML files (index.html, explore.html, etc.)
- [ ] `static/css/style.css`
- [ ] `static/js/*.js` files
- [ ] `static/charts/` directory with generated visualizations
- [ ] `static/data/` directory with JSON data files

---

## Development Notes

### Regenerating Charts

If you update the data or want to regenerate visualizations:

```bash
python3 generate_charts.py
```

### Adding New Visualizations

1. Add new chart functions in `modules/visualizations.py`
2. Call them in `generate_charts.py`
3. Embed in HTML using `<iframe>` or JavaScript `vegaEmbed()`

### Modifying Styles

All styles are in `static/css/style.css`. The site uses:
- CSS Grid for layouts
- CSS Variables for theming
- Responsive design (mobile-friendly)

---

## Browser Compatibility

- Chrome/Edge: ✓ Full support
- Firefox: ✓ Full support
- Safari: ✓ Full support
- Mobile browsers: ✓ Responsive design

---

## Performance Notes

- Charts are pre-generated for fast loading
- Data is sampled (500 players) for client-side filtering
- All visualizations use Vega-Lite for efficient rendering
- Total site size: ~20MB (includes all charts and data)

---

## Future Enhancements

Potential additions for future versions:
- Real-time data updates from APIs
- User accounts and saved comparisons
- More advanced statistical models
- Team-level analysis
- Video highlights integration

---

## Credits

**Author:** Karim Mattar
**Course:** DS209 Data Visualization, UC Berkeley MIDS
**Data:** FBref via Kaggle
**Visualization Library:** Altair (Vega-Lite)
**Semester:** Fall 2024

---

## License

This project is created for educational purposes as part of UC Berkeley MIDS coursework.

---

## Contact

For questions or feedback about this project:
- UC Berkeley MIDS DS209 Final Project
- Data Source: https://www.kaggle.com/datasets/hubertsidorowicz/football-players-stats-2024-2025

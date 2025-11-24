# Football Player Scout Tool
## DS209 Data Visualization - Final Presentation
### Karim Mattar | UC Berkeley MIDS

---

# Agenda

1. Problem & Motivation
2. Solution Overview
3. Data & Methods
4. Visualizations Deep Dive
5. Technical Implementation
6. Usability Study Results
7. Key Insights & Learnings
8. Live Demo
9. Future Work

---

# Problem Statement

## The Challenge

Football clubs spend **$7+ billion annually** on player transfers

**Current pain points:**
- Scouts manually compare players across 50+ statistics
- Subjective assessments lead to expensive mistakes
- Hidden gems in smaller leagues go unnoticed
- No unified tool for position-specific analysis

**Target users:** Scouts, analysts, fantasy football players, fans

---

# Solution: Scout Tool

## An Interactive Player Analysis Platform

| Feature | Purpose |
|---------|---------|
| **Compare** | Side-by-side radar charts with percentile rankings |
| **Similar** | ML-powered player similarity matching |
| **Explore** | Custom scatter plots for pattern discovery |
| **Database** | Searchable, filterable player table |

**Live URL:** [Streamlit Cloud Link]

---

# Data Source

## FBref 2024-2025 Season

| Attribute | Details |
|-----------|---------|
| **Source** | FBref (StatsBomb data) |
| **Players** | ~2,500 (filtered: 450+ minutes) |
| **Leagues** | Premier League, La Liga, Bundesliga, Serie A, Ligue 1 |
| **Metrics** | 50+ per player |

**Key statistics used:**
- Goals, Assists, xG, xAG (attacking)
- Progressive Carries, Progressive Passes (buildup)
- Tackles, Interceptions (defensive)
- Shot-Creating Actions (creativity)

---

# Visualization 1: Player Comparison

## Radar Chart with Percentile Rankings

**Design choices:**
- Percentile normalization (0-100 scale)
- Position-filtered comparisons
- 10 key metrics selected per position
- Overlapping traces for direct comparison

**Why radar charts?**
- Intuitive for multi-dimensional comparison
- Quickly identifies strengths/weaknesses
- Common in sports analytics (familiar to users)

*Screenshot: Haaland vs Mbappe comparison*

---

# Visualization 2: Similar Players

## Cosine Similarity Algorithm

**Process:**
1. Filter by position (ensures fair comparison)
2. Select relevant metrics for position
3. StandardScaler normalization
4. Cosine similarity calculation
5. Return top N matches with scores

**Value proposition:**
- Discover undervalued players in smaller leagues
- Find replacement options for departing stars
- Identify emerging talents with similar profiles

---

# Visualization 3: Position Explorer

## Interactive Scatter Plots

**Features:**
- User-selectable X/Y axes (15+ metrics)
- Filter by position, league, age range
- Hover tooltips with player details
- Color coding by league

**Insights enabled:**
- "Which midfielders have high xG but low goals?" (unlucky finishers)
- "Who are the most progressive defenders?" (modern full-backs)
- "Which young forwards outperform their xG?" (clinical finishers)

---

# Technical Architecture

## Stack

```
Frontend:     HTML, CSS, JavaScript
Charts:       Altair / Vega-Lite (interactive)
Data:         Pandas, NumPy
Tables:       DataTables.js
Deployment:   Berkeley iSchool Server
Version Ctrl: GitHub
```

## Key Features
- Static HTML site (easy to deploy)
- Vega-Embed for chart rendering
- Altair's native interactivity (selections, filters)
- Pre-generated JSON chart specs

---

# Design Decisions

## Visual Design

| Decision | Rationale |
|----------|-----------|
| Green color palette | Football pitch association |
| Card-based layout | Modern, clean aesthetic |
| Pill-shaped nav buttons | Clear active states |
| White backgrounds | Professional, readable |
| Inter font | Clean, modern typography |

## UX Design
- No sidebar (maximizes chart space)
- Position filter first (guides users)
- Tooltips on all charts (self-service exploration)

---

# Usability Study

## Method

- **Participants:** 3 users (varied football knowledge)
- **Protocol:** Think-aloud with 4 task-based scenarios
- **Metrics:** Task completion, time, SUS score

## Tasks Tested
1. Compare Haaland vs Mbappe
2. Find players similar to Salah
3. Find highest xG midfielder in Premier League
4. Filter database for young La Liga forwards

---

# Usability Findings

## What Worked Well
- Radar chart immediately understood
- Navigation intuitive
- Similar player feature was "surprising and useful"

## Issues Identified

| Issue | Severity | Fix Applied |
|-------|----------|-------------|
| Dropdown hard to see in dark mode | Medium | Forced light backgrounds |
| Unclear what percentile means | Low | Added tooltip explanation |
| Mobile layout broken | Medium | Responsive CSS adjustments |

## SUS Score: XX/100
*(Fill in after conducting study)*

---

# Key Insights

## Technical Learnings

1. **Altair strengths** - Native interactivity, easy to embed in HTML
2. **Vega-Lite ecosystem** - Powerful grammar for visualization
3. **Static site benefits** - Easy deployment on iSchool server

## Domain Insights

1. **xG vs Goals** reveals clinical vs lucky finishers
2. **Similar players** often found in overlooked leagues
3. **Progressive stats** better predict modern player value

---

# Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Large JSON chart specs | Pre-generate and cache charts |
| Data embedding in Vega | Export JSON data separately |
| Large dataset performance | Filter to 450+ min players |
| Interactive table | Use DataTables.js with custom filters |

---

# Future Work

## Short-term
- Add historical season data for trend analysis
- Include goalkeeper-specific metrics
- Export comparison images (PNG)

## Long-term
- Player value prediction model
- Integration with transfer market data
- Team-level analysis features
- Mobile-optimized version

---

# Live Demo

## Scout Tool

**[LIVE DEMO - 2 minutes]**

1. Compare: Haaland vs Mbappe
2. Similar: Find alternatives to Salah
3. Explore: xG vs Goals scatter
4. Database: Quick search

---

# Summary

## What We Built
A functional, deployed web application for football player analysis

## Key Accomplishments
- 4 interactive visualization types
- ML-powered similarity matching
- Professional UI/UX design
- Deployed to production (Streamlit Cloud)

## Impact
Makes professional-level player analysis accessible to everyone

---

# Thank You

## Questions?

**Karim Mattar**
UC Berkeley MIDS
DS209 Data Visualization

**Resources:**
- GitHub: github.com/karimmattar1/ds209-final-project
- Live App: [Streamlit URL]
- Data: FBref.com

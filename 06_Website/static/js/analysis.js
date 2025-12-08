// Analysis page JavaScript - Top Players Ranking
let playerData = [];

// Load data on page load
document.addEventListener('DOMContentLoaded', function() {
    loadPlayerData();
    populateFilters();
});

async function loadPlayerData() {
    try {
        const response = await fetch('static/data/players_sample.json');
        playerData = await response.json();
        console.log('Loaded ' + playerData.length + ' players');
        updateAnalysisChart();
    } catch (error) {
        console.error('Error loading player data:', error);
        document.getElementById('analysis-chart').innerHTML = '<p style="color: red;">Error loading data</p>';
    }
}

async function populateFilters() {
    try {
        const response = await fetch('static/data/metadata.json');
        const metadata = await response.json();

        // Populate league filter
        const leagueSelect = document.getElementById('league-filter');
        if (leagueSelect && metadata.leagues) {
            metadata.leagues.forEach(league => {
                const option = document.createElement('option');
                option.value = league;
                option.textContent = league;
                option.selected = true;
                leagueSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading filters:', error);
    }
}

function updateAnalysisChart() {
    const positionFilter = document.getElementById('position-filter');
    const leagueFilter = document.getElementById('league-filter');
    const rankMetric = document.getElementById('rank-metric').value;
    const topN = parseInt(document.getElementById('top-n').value);

    // Get selected values
    const selectedPositions = Array.from(positionFilter.selectedOptions).map(opt => opt.value);
    const selectedLeagues = Array.from(leagueFilter.selectedOptions).map(opt => opt.value);

    // Get age filter
    const maxAge = parseFloat(document.getElementById('age-filter').value) || 99;

    // Filter data
    let filteredData = playerData.filter(player => {
        const positionMatch = selectedPositions.length === 0 || selectedPositions.includes(player.Position);
        const leagueMatch = selectedLeagues.length === 0 || selectedLeagues.includes('all') || selectedLeagues.includes(player.Comp);
        const ageMatch = !player.Age || player.Age <= maxAge;
        return positionMatch && leagueMatch && ageMatch;
    });

    // Sort by selected metric (descending) and take top N
    filteredData.sort((a, b) => (b[rankMetric] || 0) - (a[rankMetric] || 0));
    const topPlayers = filteredData.slice(0, topN);

    // Update results count
    document.getElementById('results-count').textContent = 'Found ' + filteredData.length + ' players, showing top ' + topPlayers.length;

    console.log('Showing top ' + topPlayers.length + ' of ' + filteredData.length + ' players');

    // Create horizontal bar chart spec
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "width": 600,
        "height": topN * 28,
        "data": {"values": topPlayers},
        "mark": {
            "type": "bar",
            "cornerRadiusEnd": 4
        },
        "encoding": {
            "y": {
                "field": "Player_Clean",
                "type": "nominal",
                "title": null,
                "sort": {
                    "field": rankMetric,
                    "order": "descending"
                },
                "axis": {
                    "labelLimit": 150
                }
            },
            "x": {
                "field": rankMetric,
                "type": "quantitative",
                "title": formatMetricName(rankMetric)
            },
            "color": {
                "field": "Position",
                "type": "nominal",
                "title": "Position",
                "scale": {
                    "domain": ["GK", "DF", "MF", "FW"],
                    "range": ["#FDB913", "#00A650", "#0072CE", "#EF3340"]
                }
            },
            "tooltip": [
                {"field": "Player_Clean", "type": "nominal", "title": "Player"},
                {"field": "Squad", "type": "nominal", "title": "Team"},
                {"field": "Comp", "type": "nominal", "title": "League"},
                {"field": "Position", "type": "nominal", "title": "Position"},
                {"field": "Age", "type": "quantitative", "title": "Age"},
                {"field": rankMetric, "type": "quantitative", "title": formatMetricName(rankMetric), "format": ".2f"}
            ]
        },
        "title": {
            "text": "Top " + topPlayers.length + " Players by " + formatMetricName(rankMetric),
            "fontSize": 16
        },
        "config": {
            "view": {"strokeWidth": 0},
            "axis": {
                "labelFontSize": 12,
                "titleFontSize": 13
            }
        }
    };

    // Render chart
    vegaEmbed('#analysis-chart', spec, {
        "actions": {
            "export": true,
            "source": false,
            "compiled": false,
            "editor": false
        }
    }).catch(console.error);
}

function formatMetricName(metric) {
    return metric
        .replace(/_/g, ' ')
        .replace(/per90/g, 'per 90')
        .replace(/\b\w/g, l => l.toUpperCase());
}

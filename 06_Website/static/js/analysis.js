// Analysis page JavaScript
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
    const xMetric = document.getElementById('x-metric').value;
    const yMetric = document.getElementById('y-metric').value;

    // Get selected values
    const selectedPositions = Array.from(positionFilter.selectedOptions).map(opt => opt.value);
    const selectedLeagues = Array.from(leagueFilter.selectedOptions).map(opt => opt.value);

    // Get filter values (age and metric threshold)
    const maxAge = parseFloat(document.getElementById('age-filter').value) || 99;
    const minMetric = parseFloat(document.getElementById('metric-min').value) || 0;

    // Filter data
    let filteredData = playerData.filter(player => {
        const positionMatch = selectedPositions.length === 0 || selectedPositions.includes(player.Position);
        const leagueMatch = selectedLeagues.length === 0 || selectedLeagues.includes('all') || selectedLeagues.includes(player.Comp);
        const ageMatch = !player.Age || player.Age <= maxAge;
        const metricMatch = (player[xMetric] || 0) >= minMetric;
        return positionMatch && leagueMatch && ageMatch && metricMatch;
    });

    // Update results count
    document.getElementById('results-count').textContent = 'Showing ' + filteredData.length + ' players';

    console.log('Filtered to ' + filteredData.length + ' players');

    // Create Vega-Lite spec
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "width": 700,
        "height": 500,
        "data": {"values": filteredData},
        "mark": {
            "type": "circle",
            "size": 100,
            "opacity": 0.7
        },
        "selection": {
            "hover": {
                "type": "single",
                "on": "mouseover",
                "empty": "none"
            }
        },
        "encoding": {
            "x": {
                "field": xMetric,
                "type": "quantitative",
                "title": formatMetricName(xMetric),
                "scale": {"zero": false}
            },
            "y": {
                "field": yMetric,
                "type": "quantitative",
                "title": formatMetricName(yMetric),
                "scale": {"zero": false}
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
            "opacity": {
                "condition": {"selection": "hover", "value": 1},
                "value": 0.7
            },
            "tooltip": [
                {"field": "Player_Clean", "type": "nominal", "title": "Player"},
                {"field": "Squad", "type": "nominal", "title": "Team"},
                {"field": "Comp", "type": "nominal", "title": "League"},
                {"field": "Position", "type": "nominal", "title": "Position"},
                {"field": "Age", "type": "quantitative", "title": "Age"},
                {"field": xMetric, "type": "quantitative", "title": formatMetricName(xMetric), "format": ".2f"},
                {"field": yMetric, "type": "quantitative", "title": formatMetricName(yMetric), "format": ".2f"}
            ]
        },
        "title": {
            "text": formatMetricName(yMetric) + " vs " + formatMetricName(xMetric),
            "fontSize": 16
        },
        "config": {
            "view": {"strokeWidth": 0}
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

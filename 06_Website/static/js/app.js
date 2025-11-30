// Main JavaScript for Football Scout Tool

// Load metadata on page load
document.addEventListener('DOMContentLoaded', function() {
    loadMetadata();
});

async function loadMetadata() {
    try {
        const response = await fetch('static/data/metadata.json');
        const metadata = await response.json();

        // Update total players count
        const totalPlayersEl = document.getElementById('total-players');
        if (totalPlayersEl) {
            totalPlayersEl.textContent = metadata.total_players.toLocaleString() + '+';
        }

        // Store metadata globally for other pages
        window.footballData = {
            leagues: metadata.leagues,
            positions: metadata.positions,
            teams: metadata.teams,
            players: metadata.players
        };

        console.log('Metadata loaded successfully');
    } catch (error) {
        console.error('Error loading metadata:', error);
    }
}

// Embed Altair chart from HTML file
function embedChart(containerId, chartPath) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error('Container not found');
        return;
    }

    // Show loading state
    container.innerHTML = '<div class="loading">Loading visualization</div>';

    // Load the chart HTML
    fetch(chartPath)
        .then(response => response.text())
        .then(html => {
            container.innerHTML = html;
        })
        .catch(error => {
            console.error('Error loading chart:', error);
            container.innerHTML = '<p style="color: red;">Error loading visualization</p>';
        });
}

// Helper function to create Vega-Lite spec dynamically
function createScatterSpec(data, xMetric, yMetric, colorBy) {
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "width": 700,
        "height": 500,
        "data": {"values": data},
        "mark": {
            "type": "circle",
            "size": 100,
            "opacity": 0.7
        },
        "encoding": {
            "x": {
                "field": xMetric,
                "type": "quantitative",
                "title": xMetric.replace(/_/g, ' ').replace(/per90/g, 'per 90'),
                "scale": {"zero": false}
            },
            "y": {
                "field": yMetric,
                "type": "quantitative",
                "title": yMetric.replace(/_/g, ' ').replace(/per90/g, 'per 90'),
                "scale": {"zero": false}
            },
            "color": {
                "field": colorBy,
                "type": "nominal",
                "title": colorBy,
                "scale": {"scheme": "tableau10"}
            },
            "tooltip": [
                {"field": "Player_Clean", "type": "nominal", "title": "Player"},
                {"field": "Squad", "type": "nominal", "title": "Team"},
                {"field": "Comp", "type": "nominal", "title": "League"},
                {"field": "Position", "type": "nominal", "title": "Position"},
                {"field": "Age", "type": "quantitative", "title": "Age"},
                {"field": xMetric, "type": "quantitative", "title": xMetric, "format": ".2f"},
                {"field": yMetric, "type": "quantitative", "title": yMetric, "format": ".2f"}
            ]
        },
        "title": {
            "text": yMetric + " vs " + xMetric,
            "fontSize": 16
        },
        "config": {
            "view": {"strokeWidth": 0}
        }
    };
}

// Render Vega-Lite spec
function renderVegaLite(containerId, spec) {
    vegaEmbed('#' + containerId, spec, {
        "actions": {
            "export": true,
            "source": false,
            "compiled": false,
            "editor": false
        }
    }).catch(console.error);
}

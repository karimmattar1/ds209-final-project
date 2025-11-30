// Player comparison JavaScript
let playerData = [];
let selectedPlayer1 = null;
let selectedPlayer2 = null;

document.addEventListener('DOMContentLoaded', function() {
    loadPlayerData();
    setupAutocomplete();
});

async function loadPlayerData() {
    try {
        const response = await fetch('static/data/players_sample.json');
        playerData = await response.json();
        console.log('Loaded ' + playerData.length + ' players for comparison');
    } catch (error) {
        console.error('Error loading player data:', error);
    }
}

function setupAutocomplete() {
    const inputs = ['player1', 'player2'];

    inputs.forEach(inputId => {
        const input = document.getElementById(inputId);
        const dropdownId = inputId + '-dropdown';

        // Create dropdown container
        const dropdown = document.createElement('div');
        dropdown.id = dropdownId;
        dropdown.className = 'autocomplete-dropdown';
        dropdown.style.display = 'none';
        input.parentNode.appendChild(dropdown);

        // Input event listener
        input.addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();

            if (query.length < 2) {
                dropdown.style.display = 'none';
                return;
            }

            // Filter players
            const matches = playerData.filter(p =>
                p.Player_Clean.toLowerCase().includes(query)
            ).slice(0, 10); // Limit to 10 results

            if (matches.length === 0) {
                dropdown.style.display = 'none';
                return;
            }

            // Populate dropdown
            dropdown.innerHTML = matches.map(player => `
                <div class="autocomplete-item" data-player="${player.Player_Clean}">
                    <div class="player-name">${player.Player_Clean}</div>
                    <div class="player-info">${player.Squad} • ${player.Comp} • ${player.Position}</div>
                </div>
            `).join('');

            dropdown.style.display = 'block';

            // Add click listeners to dropdown items
            dropdown.querySelectorAll('.autocomplete-item').forEach(item => {
                item.addEventListener('click', function() {
                    const playerName = this.dataset.player;
                    input.value = playerName;
                    dropdown.style.display = 'none';

                    // Store selected player
                    if (inputId === 'player1') {
                        selectedPlayer1 = playerData.find(p => p.Player_Clean === playerName);
                    } else {
                        selectedPlayer2 = playerData.find(p => p.Player_Clean === playerName);
                    }
                });
            });
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!input.contains(e.target) && !dropdown.contains(e.target)) {
                dropdown.style.display = 'none';
            }
        });
    });
}

function comparePlayer() {
    const player1Name = document.getElementById('player1').value;
    const player2Name = document.getElementById('player2').value;

    if (!player1Name || !player2Name) {
        alert('Please select both players');
        return;
    }

    const player1 = playerData.find(p => p.Player_Clean === player1Name);
    const player2 = playerData.find(p => p.Player_Clean === player2Name);

    if (!player1 || !player2) {
        alert('Player not found');
        return;
    }

    displayComparison(player1, player2);
}

function displayComparison(player1, player2) {
    // Show results section
    document.getElementById('comparison-result').style.display = 'block';

    // Display player cards
    displayPlayerCard('player1-card', player1);
    displayPlayerCard('player2-card', player2);

    // Create comparison chart
    createComparisonChart(player1, player2);
}

function displayPlayerCard(cardId, player) {
    const card = document.getElementById(cardId);
    card.innerHTML = `
        <h3>${player.Player_Clean}</h3>
        <div class="team">${player.Squad} | ${player.Comp}</div>
        <div class="stats">
            <div class="stat">
                <div class="stat-value">${player.Position}</div>
                <div class="stat-label">Position</div>
            </div>
            <div class="stat">
                <div class="stat-value">${player.Age}</div>
                <div class="stat-label">Age</div>
            </div>
            <div class="stat">
                <div class="stat-value">${player.Gls_per90?.toFixed(2) || 'N/A'}</div>
                <div class="stat-label">Goals/90</div>
            </div>
            <div class="stat">
                <div class="stat-value">${player.Ast_per90?.toFixed(2) || 'N/A'}</div>
                <div class="stat-label">Assists/90</div>
            </div>
            <div class="stat">
                <div class="stat-value">${player.xG_per90?.toFixed(2) || 'N/A'}</div>
                <div class="stat-label">xG/90</div>
            </div>
            <div class="stat">
                <div class="stat-value">${player.PrgC_per90?.toFixed(2) || 'N/A'}</div>
                <div class="stat-label">Prog. Carries/90</div>
            </div>
        </div>
    `;
}

function createComparisonChart(player1, player2) {
    const metrics = ['Gls_per90', 'Ast_per90', 'xG_per90', 'xAG_per90', 'PrgC_per90', 'Tkl_per90'];

    const data = [];
    metrics.forEach(metric => {
        if (player1[metric] !== undefined && player2[metric] !== undefined) {
            data.push({
                Metric: metric.replace(/_/g, ' ').replace('per90', '/90'),
                Player: player1.Player_Clean,
                Value: player1[metric] || 0
            });
            data.push({
                Metric: metric.replace(/_/g, ' ').replace('per90', '/90'),
                Player: player2.Player_Clean,
                Value: player2[metric] || 0
            });
        }
    });

    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "width": 600,
        "height": 400,
        "data": {"values": data},
        "mark": "bar",
        "encoding": {
            "x": {
                "field": "Metric",
                "type": "nominal",
                "axis": {"labelAngle": -45}
            },
            "y": {
                "field": "Value",
                "type": "quantitative"
            },
            "color": {
                "field": "Player",
                "type": "nominal",
                "scale": {"scheme": "category10"}
            },
            "xOffset": {"field": "Player"},
            "tooltip": [
                {"field": "Player", "type": "nominal"},
                {"field": "Metric", "type": "nominal"},
                {"field": "Value", "type": "quantitative", "format": ".2f"}
            ]
        },
        "title": {
            "text": "Statistical Comparison",
            "fontSize": 16
        }
    };

    vegaEmbed('#comparison-chart', spec, {
        "actions": {
            "export": true,
            "source": false,
            "compiled": false,
            "editor": false
        }
    }).catch(console.error);
}

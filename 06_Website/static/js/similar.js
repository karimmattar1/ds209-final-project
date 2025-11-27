// Similar players finder JavaScript
let playerData = [];

document.addEventListener('DOMContentLoaded', function() {
    loadPlayerData();
});

async function loadPlayerData() {
    try {
        const response = await fetch('static/data/players_sample.json');
        playerData = await response.json();

        // Populate player datalist
        const datalist = document.getElementById('player-list-similar');
        playerData.forEach(player => {
            const option = document.createElement('option');
            option.value = player.Player_Clean;
            datalist.appendChild(option);
        });

        console.log('Loaded ' + playerData.length + ' players');
    } catch (error) {
        console.error('Error loading player data:', error);
    }
}

function findSimilarPlayers() {
    const playerName = document.getElementById('player-search').value;
    const positionFilter = document.getElementById('position-filter-similar').value === 'true';

    if (!playerName) {
        alert('Please enter a player name');
        return;
    }

    const targetPlayer = playerData.find(p => p.Player_Clean === playerName);

    if (!targetPlayer) {
        alert('Player not found');
        return;
    }

    const similarPlayers = calculateSimilarity(targetPlayer, positionFilter);
    displaySimilarPlayers(targetPlayer, similarPlayers);
}

function calculateSimilarity(targetPlayer, positionFilter) {
    const metrics = ['Gls_per90', 'Ast_per90', 'xG_per90', 'xAG_per90', 'PrgC_per90', 'Tkl_per90', 'Touches_per90', 'Cmp%'];

    // Filter players
    let candidates = playerData.filter(p => p.Player_Clean !== targetPlayer.Player_Clean);
    if (positionFilter) {
        candidates = candidates.filter(p => p.Position === targetPlayer.Position);
    }

    // Calculate similarity scores
    candidates.forEach(player => {
        let similarity = 0;
        let validMetrics = 0;

        metrics.forEach(metric => {
            if (targetPlayer[metric] !== undefined && player[metric] !== undefined &&
                targetPlayer[metric] !== null && player[metric] !== null) {
                const diff = Math.abs(targetPlayer[metric] - player[metric]);
                const maxVal = Math.max(targetPlayer[metric], player[metric], 1);
                similarity += (1 - (diff / maxVal));
                validMetrics++;
            }
        });

        player.Similarity = validMetrics > 0 ? similarity / validMetrics : 0;
    });

    // Sort by similarity and return top 10
    return candidates.sort((a, b) => b.Similarity - a.Similarity).slice(0, 10);
}

function displaySimilarPlayers(targetPlayer, similarPlayers) {
    document.getElementById('similar-result').style.display = 'block';

    // Update description
    document.getElementById('similarity-description').textContent =
        'Showing top 10 players most similar to ' + targetPlayer.Player_Clean + ' (' + targetPlayer.Position + ') based on statistical profile';

    // Create chart
    const spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "width": 600,
        "height": 400,
        "data": {"values": similarPlayers},
        "mark": "bar",
        "encoding": {
            "x": {
                "field": "Similarity",
                "type": "quantitative",
                "title": "Similarity Score",
                "scale": {"domain": [0, 1]}
            },
            "y": {
                "field": "Player_Clean",
                "type": "nominal",
                "title": "Player",
                "sort": "-x"
            },
            "color": {
                "field": "Comp",
                "type": "nominal",
                "title": "League",
                "scale": {"scheme": "category10"}
            },
            "tooltip": [
                {"field": "Player_Clean", "type": "nominal", "title": "Player"},
                {"field": "Squad", "type": "nominal", "title": "Team"},
                {"field": "Comp", "type": "nominal", "title": "League"},
                {"field": "Age", "type": "quantitative", "title": "Age"},
                {"field": "Similarity", "type": "quantitative", "title": "Similarity", "format": ".3f"}
            ]
        },
        "title": {
            "text": "Most Similar Players",
            "fontSize": 16
        }
    };

    vegaEmbed('#similar-players-chart', spec, {
        "actions": {
            "export": true,
            "source": false,
            "compiled": false,
            "editor": false
        }
    }).catch(console.error);

    // Create player cards
    const listDiv = document.getElementById('similar-players-list');
    listDiv.innerHTML = '<h2>Player Details</h2><div class="player-grid"></div>';
    const grid = listDiv.querySelector('.player-grid');

    similarPlayers.slice(0, 6).forEach(player => {
        const card = document.createElement('div');
        card.className = 'player-card';
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
                    <div class="stat-value">${(player.Similarity * 100).toFixed(1)}%</div>
                    <div class="stat-label">Similarity</div>
                </div>
                <div class="stat">
                    <div class="stat-value">${player.Gls_per90?.toFixed(2) || 'N/A'}</div>
                    <div class="stat-label">Goals/90</div>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

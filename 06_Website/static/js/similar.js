// Similar players finder JavaScript
let playerData = [];

document.addEventListener('DOMContentLoaded', function() {
    loadPlayerData();
    setupAutocomplete();
});

async function loadPlayerData() {
    try {
        const response = await fetch('static/data/players_sample.json');
        playerData = await response.json();
        console.log('Loaded ' + playerData.length + ' players');
    } catch (error) {
        console.error('Error loading player data:', error);
    }
}

function setupAutocomplete() {
    const input = document.getElementById('player-search');
    const dropdownId = 'player-search-dropdown';

    // Create dropdown container
    const dropdown = document.createElement('div');
    dropdown.id = dropdownId;
    dropdown.className = 'autocomplete-dropdown';
    dropdown.style.display = 'none';
    input.parentNode.appendChild(dropdown);

    // Show suggestions on focus (even without typing)
    input.addEventListener('focus', function() {
        if (playerData.length > 0 && this.value.length < 2) {
            showSuggestedPlayers(dropdown, input);
        }
    });

    // Input event listener
    input.addEventListener('input', function() {
        const query = this.value.toLowerCase().trim();

        if (query.length < 2) {
            // Show suggested players when input is cleared
            showSuggestedPlayers(dropdown, input);
            return;
        }

        // Filter players by search query
        const matches = playerData.filter(p =>
            p.Player_Clean.toLowerCase().includes(query)
        ).slice(0, 10); // Limit to 10 results

        if (matches.length === 0) {
            dropdown.innerHTML = '<div class="autocomplete-item" style="color: #6b7280;">No players found</div>';
            dropdown.style.display = 'block';
            return;
        }

        // Populate dropdown with search results
        populateDropdown(dropdown, matches, input);
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!input.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });
}

function showSuggestedPlayers(dropdown, input) {
    // Show a mix of popular players from different leagues/positions
    const popularPlayers = playerData
        .filter(p => p.Gls_per90 > 0.2 || p.Ast_per90 > 0.15 || p.PrgC_per90 > 3)
        .sort(() => Math.random() - 0.5)
        .slice(0, 10);

    if (popularPlayers.length === 0) return;

    dropdown.innerHTML = '<div style="padding: 0.5rem 1rem; color: #6b7280; font-size: 0.85rem; border-bottom: 1px solid #e5e7eb;">Suggested players (click to select):</div>' +
        popularPlayers.map(player => `
            <div class="autocomplete-item" data-player="${player.Player_Clean}">
                <div class="player-name">${player.Player_Clean}</div>
                <div class="player-info">${player.Squad} • ${player.Comp} • ${player.Position}</div>
            </div>
        `).join('');

    dropdown.style.display = 'block';
    addDropdownClickListeners(dropdown, input);
}

function populateDropdown(dropdown, players, input) {
    dropdown.innerHTML = players.map(player => `
        <div class="autocomplete-item" data-player="${player.Player_Clean}">
            <div class="player-name">${player.Player_Clean}</div>
            <div class="player-info">${player.Squad} • ${player.Comp} • ${player.Position}</div>
        </div>
    `).join('');

    dropdown.style.display = 'block';
    addDropdownClickListeners(dropdown, input);
}

function addDropdownClickListeners(dropdown, input) {
    dropdown.querySelectorAll('.autocomplete-item[data-player]').forEach(item => {
        item.addEventListener('click', function() {
            const playerName = this.dataset.player;
            input.value = playerName;
            dropdown.style.display = 'none';
        });
    });
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

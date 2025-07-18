document.addEventListener('DOMContentLoaded', function() {
    let popularityChart = null;

    // Fetch anime data and update the display
    async function fetchAndDisplayAnime() {
        try {
            const response = await fetch('/api/anime');
            const data = await response.json();
            updateTable(data);
            updateChart(data);
        } catch (error) {
            console.error('Error fetching anime data:', error);
        }
    }

    // Update the table with anime data
    function updateTable(data) {
        const tbody = document.getElementById('animeTableBody');
        tbody.innerHTML = '';

        data.forEach((anime, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${anime.title}</td>
                <td>${anime.members.toLocaleString()}</td>
                <td>${anime.score ? anime.score.toFixed(2) : 'N/A'}</td>
                <td>${anime.source}</td>
            `;
            tbody.appendChild(row);
        });
    }

    // Update the popularity chart
    function updateChart(data) {
        const ctx = document.getElementById('popularityChart').getContext('2d');
        
        // Destroy existing chart if it exists
        if (popularityChart) {
            popularityChart.destroy();
        }

        // Prepare data for chart
        const labels = data.slice(0, 10).map(anime => anime.title);
        const members = data.slice(0, 10).map(anime => anime.members);

        popularityChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Member Count',
                    data: members,
                    backgroundColor: 'rgba(52, 152, 219, 0.8)',
                    borderColor: 'rgba(52, 152, 219, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Handle refresh button click
    document.getElementById('refreshData').addEventListener('click', async () => {
        try {
            const response = await fetch('/api/update', {
                method: 'POST'
            });
            const result = await response.json();
            if (result.status === 'success') {
                fetchAndDisplayAnime();
            }
        } catch (error) {
            console.error('Error updating data:', error);
        }
    });

    // Handle source filter changes
    document.getElementById('sourceFilter').addEventListener('change', function(e) {
        const source = e.target.value;
        fetchAndDisplayAnime(source);
    });

    // Initial data load
    fetchAndDisplayAnime();
});

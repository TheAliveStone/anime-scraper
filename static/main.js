document.addEventListener('DOMContentLoaded', function () {
    const refreshBtn = document.getElementById('refreshData');
    const animeTableBody = document.getElementById('animeTableBody');
    const sourceFilter = document.getElementById('sourceFilter');

    // Fetch and render anime data
    function fetchAnimeData(source = 'all') {
        fetch('/api/anime')
            .then(res => res.json())
            .then(data => {
                // Filter if needed
                const filtered = source === 'all' ? data : data.filter(a => a.source === source);
                renderTable(filtered);
            });
    }

    function renderTable(animeList) {
        animeTableBody.innerHTML = '';
        animeList.forEach(anime => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${anime.rank}</td>
                <td>${anime.title}</td>
                <td>${anime.members}</td>
                <td>${anime.score}</td>
                <td>${anime.source}</td>
            `;
            animeTableBody.appendChild(row);
        });
    }

    // Refresh button event
    refreshBtn.addEventListener('click', function () {
        refreshBtn.disabled = true;
        refreshBtn.textContent = "Refreshing...";
        fetch('/api/update', { method: 'POST' })
            .then(res => res.json())
            .then(result => {
                // Optionally show a success message
                fetchAnimeData(sourceFilter.value);
            })
            .catch(err => {
                alert('Error refreshing data!');
                console.error(err);
            })
            .finally(() => {
                refreshBtn.disabled = false;
                refreshBtn.textContent = "Refresh Data";
            });
    });

    // Source filter event
    sourceFilter.addEventListener('change', function () {
        fetchAnimeData(this.value);
    });

    // On load fetch data
    fetchAnimeData();
});
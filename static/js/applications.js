function runSearch() {
    const searchInput = document.getElementById('searchInput');
    const query = searchInput.value;


        fetch(`/applications/search/?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => {
                renderResults(data.results);
            });
}

document.getElementById('searchInput').addEventListener('input', runSearch);

function renderResults(results) {
    const listContainer = document.getElementById('teamList');
    listContainer.innerHTML = ''; // Clear previous entries

    if (results.length === 0) {
        const emptyItem = document.createElement('li');
        emptyItem.className = 'list-group-item';
        emptyItem.textContent = 'No results found.';
        listContainer.appendChild(emptyItem);
        return;
    }

    results.forEach(item => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';

        // Content div
        const infoDiv = document.createElement('div');
        const nameEl = document.createElement('strong');
        nameEl.textContent = item.name;

        const subEl = document.createElement('small');
        subEl.className = 'text-muted d-block';
        if (item.type === 'team') {
            subEl.textContent = item.moto || 'Team info not available';
        } else if (item.type === 'facility') {
            subEl.textContent = item.location || 'Facility location unknown';
        }

        infoDiv.appendChild(nameEl);
        infoDiv.appendChild(document.createElement('br'));
        infoDiv.appendChild(subEl);

        // Link
        const applyLink = document.createElement('a');
        applyLink.className = 'btn btn-sm btn-outline-primary';
        applyLink.textContent = 'Apply';

        if (item.type === 'team') {
            applyLink.href = `/applications/${item.pk}/team-application/`;
        } else if (item.type === 'facility') {
            applyLink.href = `/applications/${item.pk}/facility-application/`;
        }

        // Combine
        li.appendChild(infoDiv);
        li.appendChild(applyLink);

        listContainer.appendChild(li);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function submitAction(applicationId, action) {
    const formData = new FormData();
    formData.append('id', applicationId);
    formData.append('action', action);

    fetch('/applications/accept-reject/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`application-${data.id}`).remove();
                runSearch();
            } else {
                alert(data.error || 'Action failed');
            }
        }
    )
}


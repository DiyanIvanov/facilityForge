const searchInput = document.getElementById('searchInput');
const resultsContainer = document.getElementById('teamList');

searchInput.addEventListener('input', function () {
    const query = this.value;

    if (query.length < 0) {
        resultsContainer.innerHTML = '';  // Clear if input is too short
        return;
    }

    fetch(`/applications/search/?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
            renderResults(data.results);
        });
});

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

        // Button
        const button = document.createElement('button');
        button.className = 'btn btn-sm btn-outline-primary';
        button.textContent = 'Apply';
        button.onclick = () => applyTo(item.type, item.id);

        // Combine
        li.appendChild(infoDiv);
        li.appendChild(button);

        listContainer.appendChild(li);
    });
}

function applyTo(type, id) {
    // Replace this with your actual application logic or form submission
    alert(`Applying to ${type} with ID ${id}`);
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
    formData.append('application_id', applicationId);
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
            } else {
                alert(data.error || 'Action failed');
            }
        })
}


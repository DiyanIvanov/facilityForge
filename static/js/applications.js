const searchInput = document.getElementById('searchInput');
const listItems = document.querySelectorAll('#teamList li');

searchInput.addEventListener('input', function () {
    const searchTerm = this.value.toLowerCase();
    listItems.forEach(item => {
        const text = item.innerText.toLowerCase();
        item.style.display = text.includes(searchTerm) ? '' : 'none';
    });
});

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


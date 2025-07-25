document.addEventListener("DOMContentLoaded", function () {
    const tiles = document.querySelectorAll(".filter-tile");

    tiles.forEach(tile => {
        tile.addEventListener("click", function () {
            const filterType = this.getAttribute("data-filter-type");
            const filterValue = this.getAttribute("data-filter-value");

            let url = "/tickets/";

            // Build query parameters
            const params = new URLSearchParams();
            if (filterType === "priority" && filterValue !== "all") {
                params.append("priority", filterValue);
            } else if (filterType === "facility") {
                params.append("facility", filterValue);
            }

            // Append params to URL
            const fetchUrl = params.toString() ? `${url}?${params.toString()}` : url;
            // Send GET request
            fetch(fetchUrl)
                .then(response => {
                    if (!response.ok) throw new Error("Network response was not ok");
                    return response.json(); // or response.text() depending on your backend
                })
                .then(data => renderTickets(data))
                .catch(error => {
                    console.error("There was a problem fetching tickets:", error);
                });
        });
    });
});

function renderTickets(tickets) {
    const list = document.getElementById("ticket-list");
    list.innerHTML = ""; // Clear existing content

    if (!tickets || tickets.length === 0) {
        const li = document.createElement("li");
        li.className = "list-group-item text-muted";
        li.textContent = "No tickets found.";
        list.appendChild(li);
        return;
    }

    tickets.forEach(ticket => {
        const li = document.createElement("li");
        li.className = "list-group-item d-flex justify-content-between align-items-center";

        // Link to update page
        const link = document.createElement("a");
        link.href = `/tickets/${ticket.ticket_id}/update/`; // Adjust URL pattern if needed
        link.className = "text-decoration-none text-dark flex-grow-1";

        // Ticket content inside the link
        const contentDiv = document.createElement("div");
        const strong = document.createElement("strong");
        strong.textContent = `Facility: ${ticket.facility_name}`;
        const br = document.createElement("br");
        const small = document.createElement("small");
        small.className = "text-muted";
        small.textContent = ticket.description;

        contentDiv.appendChild(strong);
        contentDiv.appendChild(br);
        contentDiv.appendChild(small);
        link.appendChild(contentDiv);

        // Priority badge
        const badge = document.createElement("span");
        badge.className = `badge bg-${ticket.priority.toLowerCase()} ms-3`;
        badge.textContent = ticket.priority;

        li.appendChild(link);
        li.appendChild(badge);
        list.appendChild(li);
    });
}
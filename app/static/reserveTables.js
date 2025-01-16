document.addEventListener("DOMContentLoaded", () => {
    const tables = document.querySelectorAll(".table");

    tables.forEach((table) => {
        table.addEventListener("click", () => {
            const tableId = table.dataset.id;
            const tableSize = table.dataset.size;

            const userConfirmed = confirm(`Reserve Table ${tableId}? Size: ${tableSize}`);
            if (userConfirmed) {
                fetch("/makeReserve", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        table_id: tableId,
                        size: tableSize,
                        date: document.body.dataset.date,
                        time: document.body.dataset.time,
                        num: document.body.dataset.num,
                    }),
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.success) {
                            alert("Table reserved successfully!");
                            location.reload();
                        } else {
                            alert("Failed to reserve table. Please try again.");
                        }
                    })
                    .catch((error) => {
                        console.error("Error:", error);
                        alert("An error occurred while reserving the table.");
                    });
            }
        });
    });
});

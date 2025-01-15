function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();

    const data = ev.dataTransfer.getData("text");
    const element = document.getElementById(data);
    const restaurant = document.body.dataset.restaurantName;
    const x = ev.target.dataset.x;
    const y = ev.target.dataset.y;

    const seats = prompt(`How many seats for table ${data}?`, "6");

    if (seats && !isNaN(seats) && parseInt(seats, 10) > 0) {
        ev.target.appendChild(element);

        console.log(`Table dropped into div at (${x}, ${y}) with ${seats} seats`);

        //this sends to flask
        fetch("/add_table", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                restaurant_name: restaurant,
                x: x,
                y: y,
                seats: parseInt(seats, 10),
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log("Success:", data);
            })
            .catch((error) => {
                console.error("Failure:", error);
            });
    } else {
        console.log(`bad: ${data}`);

        const originalContainer = document.querySelector("#imageContainer");
        originalContainer.appendChild(element);
    }
}

const gridContainer = document.querySelector("#grid");

for (let y = 0; y < 10; y++) {
    for (let x = 0; x < 10; x++) {
        const div = document.createElement("div");
        div.dataset.x = x;
        div.dataset.y = y;

        div.addEventListener("dragover", allowDrop);
        div.addEventListener("drop", drop);

        gridContainer.appendChild(div);
    }
}

const draggables = document.querySelectorAll(".dragitem");

draggables.forEach((draggable) => {
    draggable.addEventListener("dragstart", drag);
});

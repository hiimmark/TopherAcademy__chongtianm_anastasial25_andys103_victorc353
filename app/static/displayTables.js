const tables = document.querySelectorAll(".table");

tables.forEach((table) => {
  console.log("(" + table.dataset.xCoor + "," + table.dataset.yCoor + ")");
  moveTo(table, table.dataset.xCoor, table.dataset.yCoor);
});

function moveTo(table, x, y) {
  const targetDiv = document.querySelector(`[data-x="${x}"][data-y="${y}"]`);

  if (targetDiv) {
    targetDiv.appendChild(table);
    table.setAttribute("draggable", "false");
  } else {
    console.error(`Div at (${x}, ${y}) not found`);
  }
}

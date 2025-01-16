const tables = document.querySelectorAll(".table");

tables.forEach((table) => {
  console.log("(" + table.dataset.xCoor + "," + table.dataset.yCoor + ")");
  moveTo(table, table.dataset.xCoor, table.dataset.yCoor);
});

function moveTo(table, x, y) {
  let xRight = document.querySelector(`[data-x="${x}"]`)};
  xRight.forEach((element) => console.log(element));
};

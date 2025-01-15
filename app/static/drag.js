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

  ev.target.appendChild(element);

  console.log(`${data} in ${ev.target.id}`);
}

const draggables = document.querySelectorAll(".dragitem");

draggables.forEach(draggable => {
  draggable.addEventListener("dragstart", drag);
});

const div1 = document.querySelector("#div1");

const div2 = document.querySelector("#div2");

[div1, div2].forEach(div => {
  div.addEventListener("dragover", allowDrop);

  div.addEventListener("drop", drop);
});

//import "./styles.css";

const data = [
  { row: 1, playerName: "DJ", numHits: 1, playerType: "player" },
  { row: 1, playerName: "Kathy", numHits: 0, playerType: "player" },
  { row: 1, playerName: "Kai", numHits: 2, playerType: "player" },
  { row: 1, playerName: "Krystal", numHits: 2, playerType: "player" },
  { row: 1, playerName: "Goku", numHits: 2, playerType: "player" },
  { row: 2, playerName: "Tony", numHits: 0, playerType: "player" },
  { row: 2, playerName: "Tobin", numHits: 2, playerType: "player" },
  { row: 2, playerName: "Lala", numHits: 0, playerType: "player" },
  { row: 2, playerName: "Anish", numHits: 2, playerType: "player" },
  { row: 2, playerName: "Deba", numHits: 0, playerType: "player" },
  { row: 3, playerName: "Tim", numHits: 2, playerType: "player" },
  { row: 3, playerName: "Vincent", numHits: 1, playerType: "player" },
  { row: 3, playerName: "Arjun", numHits: 2, playerType: "player" },
  { row: 3, playerName: "Abir", numHits: 1, playerType: "player" },
  { row: 3, playerName: "Tina", numHits: 0, playerType: "player" },
  { row: 4, playerName: "Ajay", numHits: 0, playerType: "player" },
  { row: 4, playerName: "Victoria", numHits: 2, playerType: "player" },
  { row: 4, playerName: "Nikhil", numHits: 0, playerType: "removed" },
  { row: 4, playerName: "", numHits: 0, playerType: "hidden" },
  { row: 4, playerName: "Aarti", numHits: 2, playerType: "player" },
  { row: 5, playerName: "Mitoo", numHits: 3, playerType: "moderator" }
];

const $chart = document.getElementById("chart");

const createElement = (elementName, innerHTML, className) => {
  const $el = document.createElement(elementName);
  $el.innerHTML = innerHTML;
  $el.className = className;
  return $el;
};

data.forEach(d => {
  let $row = $chart.querySelector(`.row-${d.row}`);
  if (!$row) {
    const $rowNumber = createElement("div", d.row, "row-number");
    $row = createElement("div", "", `row row-${d.row}`);
    $row.appendChild($rowNumber);
    $chart.appendChild($row);
  }
  const state = d.numHits ? (d.numHits < 2 ? "dead" : "injured") : "";
  const emptyClass = d.playerType == "hide" ? "empty" : "";
  const hitsString = "x".repeat(d.numHits);
  var isRemoved = "";
  if (d.playerType == "hidden") {
    isRemoved = "empty";
  } else if (d.playerType == "removed") {
    isRemoved = "removed";
  }

  const $element = createElement(
    "div",
    `<div>${d.playerName}</div><div class="hit">${hitsString}</div>`,
    `player ${state} ${emptyClass} ${isRemoved}`
  );
  // if (d.playerType == "hide") {
  //   $element.addClass("empty");
  // }
  $row.appendChild($element);
});

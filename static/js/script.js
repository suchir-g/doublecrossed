function initializeGame() {
  const width = document.getElementById("width").value;
  const height = document.getElementById("height").value;
  const player = document.getElementById("startingPlayer").value;

  fetch("/start", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      width: parseInt(width),
      height: parseInt(height),
      player: parseInt(player),
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("Game started successfully!");
        buildGameBoard(parseInt(width), parseInt(height));
      } else {
        alert("Failed to start game: " + data.message);
      }
    })
    .catch((error) => console.error("Error starting game:", error));
}

function makeMove(row, col, type) {
  console.log(`Making move at row ${row}, col ${col}, type ${type}`);

  // Assuming the player is always 0 for simplicity; modify as needed
  const moveDetails = {
    lineType: type,
    vPos: row,
    hPos: col,
    player: 0,
  };

  fetch("/move", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(moveDetails),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (data.successful) {
        updateGameBoard(data.gameState); // Assuming gameState contains the necessary data to update the UI
      } else {
        alert("Move was not successful: " + data.message);
      }
    })
    .catch((error) => {
      console.error("Error making move:", error);
      alert("Failed to make move. See console for details.");
    });
}

function updateGameBoard(gameState) {
  // Example gameState structure: {boxes: [...], horizontalLines: [...], verticalLines: [...]}

  const container = document.getElementById("gameContainer");
  const width = document.getElementById("width").value;
  const height = document.getElementById("height").value;

  for (let i = 0; i < height - 1; i++) {
    for (let j = 0; j < width - 1; j++) {
      const boxElement = document.getElementById(`box-${i}-${j}`);
      const boxState = gameState.boxes[i][j];
      if (boxState !== -1) {
        boxElement.textContent = boxState === 0 ? "Player" : "AI";
      }
    }
  }

  // Update lines based on gameState
  gameState.horizontalLines.forEach((row, i) => {
    row.forEach((lineState, j) => {
      const lineElement = document.querySelector(
        `.horizontal[data-row="${i}"][data-col="${j}"]`
      );
      if (lineState === 1) {
        lineElement.style.backgroundColor = "black"; // Line is marked
      }
    });
  });

  gameState.verticalLines.forEach((col, i) => {
    col.forEach((lineState, j) => {
      const lineElement = document.querySelector(
        `.vertical[data-row="${i}"][data-col="${j}"]`
      );
      if (lineState === 1) {
        lineElement.style.backgroundColor = "black"; // Line is marked
      }
    });
  });
}

function buildGameBoard(width, height) {
  const container = document.getElementById("gameContainer");
  container.innerHTML = ""; // Clear the board
  for (let i = 0; i < height; i++) {
    for (let j = 0; j < width; j++) {
      container.appendChild(createElement("dot"));

      if (j < width - 1) {
        container.appendChild(createElement("horizontal"));
      }
      if (i < height - 1) {
        container.appendChild(createElement("vertical"));
      }
      if (i < height - 1 && j < width - 1) {
        container.appendChild(createElement("box"));
      }
    }
  }
}

function createElement(type) {
  const el = document.createElement("div");
  el.className = type;
  return el;
}

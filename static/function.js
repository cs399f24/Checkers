fetch('/static/checkersboard.json')
    .then(response => response.json())
    .then(data => {
        board = data.board;
        currentPlayer = data.currentPlayer;
        buildBoard(displayCounter);
    });
let currentPlayer = 1; // Assuming 1 is one player and -1 is the other
let capturedPosition = [];
let posNewPosition = [];
let readyToMove = null;

class Piece {
    constructor(row, column) {
        this.row = row;
        this.column = column;
    }

    compare(other) {
        return this.row === other.row && this.column === other.column;
    }
}

// function movePiece(e) {
//     let piece = e.target;
//     const row = parseInt(piece.getAttribute("data-row"));
//     const column = parseInt(piece.getAttribute("data-column"));
//     let p = new Piece(row, column);

//     if (capturedPosition.length > 0) {
//         enableToCapture(p);
//     } else {
//         if (posNewPosition.length > 0) {
//             enableToMove(p);
//         }
//     }

//     if (currentPlayer === board[row][column]) {
//         let player = reverse(currentPlayer);
//         if (!findPieceCaptured(p, player)) {
//             findPossibleNewPosition(p, player);
//         }
//     }
// }

function enableToCapture(p) {
    let find = false;
    let pos = null;
    let old = null;
    capturedPosition.forEach((element) => {
        if (element.newPosition.compare(p)) {
            find = true;
            pos = element.newPosition;
            old = element.pieceCaptured;
            return;
        }
    });

    if (find) {
        board[pos.row][pos.column] = currentPlayer;
        board[readyToMove.row][readyToMove.column] = 0;
        board[old.row][old.column] = 0;

        readyToMove = null;
        capturedPosition = [];
        posNewPosition = [];
        displayCurrentPlayer();
        buildBoard();

        currentPlayer = reverse(currentPlayer);
    } else {
        buildBoard();
    }
}

function enableToMove(p) {
    let find = false;
    posNewPosition.forEach((pos) => {
        if (pos.compare(p)) {
            find = true;
            return;
        }
    });

    if (find) {
        moveThePiece(p);
    } else {
        buildBoard();
    }
}
  
function moveThePiece(newPosition) {
    board[newPosition.row][newPosition.column] = currentPlayer;
    board[readyToMove.row][readyToMove.column] = 0;

    readyToMove = null;
    posNewPosition = [];
    capturedPosition = [];

    currentPlayer = reverse(currentPlayer);

    displayCurrentPlayer();
    buildBoard();

    //notify server of move
    const socket = io();
    socket.emit('game_update', { board: board, currentPlayer: currentPlayer });
}

function findPossibleNewPosition(piece, player) {
    if (board[piece.row + player][piece.column + 1] === 0) {
        readyToMove = piece;
        markPossiblePosition(piece, player, 1);
    }

    if (board[piece.row + player][piece.column - 1] === 0) {
        readyToMove = piece;
        markPossiblePosition(piece, player, -1);
    }
}

function markPossiblePosition(piece, player, direction) {
    posNewPosition.push(new Piece(piece.row + player, piece.column + direction));
}
  
function reverse(player) {
    return player === 1 ? -1 : 1;
}
  function buildBoard() {
    game.innerHTML = "";
    let black = 0;
    let white = 0;
    for (let i = 0; i < board.length; i++) {
        const element = board[i];
        let row = document.createElement("div");
        row.setAttribute("class", "row");
  
        for (let j = 0; j < element.length; j++) {
            const elmt = element[j];
            let col = document.createElement("div");
            let piece = document.createElement("div");
            let caseType = "";
            let occupied = "";
  
            if (i % 2 === 0) {
                caseType = j % 2 === 0 ? "Whitecase" : "blackCase";
            } else {
                caseType = j % 2 !== 0 ? "Whitecase" : "blackCase";
            }
  
            if (board[i][j] === 1) {
                occupied = "whitePiece";
            } else if (board[i][j] === -1) {
                occupied = "blackPiece";
            } else {
                occupied = "empty";
            }
  
            piece.setAttribute("class", "occupied " + occupied);
  
            piece.setAttribute("row", i);
            piece.setAttribute("column", j);
            piece.setAttribute("data-position", i + "-" + j);
  
            piece.addEventListener("click", movePiece);
  
            col.appendChild(piece);
  
            col.setAttribute("class", "column " + caseType);
            row.appendChild(col);
  
            if (board[i][j] === -1) {
                black++;
            } else if (board[i][j] === 1) {
                white++;
            }
  
            displayCounter(black, white);
        }
  
        game.appendChild(row);
    }
  
    if (black === 0 || white === 0) {
        modalOpen(black);
    }
  }
  
  function displayCurrentPlayer() {
    var container = document.getElementById("next-player");
    if (container.classList.contains("whitePiece")) {
        container.setAttribute("class", "occupied blackPiece");
    } else {
        container.setAttribute("class", "occupied whitePiece");
    }
  }
  
  function findPieceCaptured(p, player) {
    capturedPosition = [];
    let directions = [[player, 1], [player, -1], [-player, 1], [-player, -1]];

    directions.forEach((direction) => {
        let newRow = p.row + direction[0];
        let newColumn = p.column + direction[1];
        let jumpRow = p.row + 2 * direction[0];
        let jumpColumn = p.column + 2 * direction[1];

        if (0 <= newRow && newRow < board.length && 0 <= newColumn && newColumn < board[0].length) {
            if (board[newRow][newColumn] === reverse(currentPlayer) && board[jumpRow][jumpColumn] === 0) {
                capturedPosition.push({
                    newPosition: new Piece(jumpRow, jumpColumn),
                    pieceCaptured: new Piece(newRow, newColumn)
                });
            }
        }
    });

    return capturedPosition.length > 0;
}
  
function displayCurrentPlayer() {
    console.log(`Current Player: ${currentPlayer === 1 ? 'White' : 'Black'}`);
}
  
  function modalOpen(black) {
    document.getElementById("winner").innerHTML = black === 0 ? "White" : "Black";
    document.getElementById("loser").innerHTML = black !== 0 ? "White" : "Black";
    modal.classList.add("effect");
  }
  
  function modalClose() {
    modal.classList.remove("effect");
  }
  
  function reverse(player) {
    return player === -1 ? 1 : -1;
  }



// Event listener for piece movement
document.querySelectorAll('.cell .occupied').forEach(piece => {
    piece.addEventListener('click', movePiece);
});
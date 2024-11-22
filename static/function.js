let board, currentPlayer, capturedPosition = [], posNewPosition = [], readyToMove = null;

// Fetch the initial board state
fetch('/static/checkersboard.json')
    .then(response => response.json())
    .then(data => {
        board = data.board;
        currentPlayer = data.currentPlayer;
        buildBoard();
    });

// Piece class to encapsulate row and column
class Piece {
    constructor(row, column) {
        this.row = row;
        this.column = column;
    }

    compare(other) {
        return this.row === other.row && this.column === other.column;
    }
}

// Function to handle moving a piece
function moveThePiece(newPosition) {
    if (!readyToMove) return;

    const { row, column } = readyToMove;

    // Check if the current player owns the piece being moved
    if (currentPlayer === board[row][column]) {
        let opponent = reverse(currentPlayer);

        // Determine valid moves or captures
        if (!findPieceCaptured(readyToMove, opponent)) {
            findPossibleNewPosition(readyToMove, opponent);
        }

        // Update the board
        board[newPosition.row][newPosition.column] = currentPlayer;
        board[row][column] = 0;

        // Reset state
        readyToMove = null;
        posNewPosition = [];
        capturedPosition = [];

        // Switch to the other player
        currentPlayer = reverse(currentPlayer);

        // Update the UI
        displayCurrentPlayer();
        buildBoard();

        // Notify the server of the move
        const socket = io(); // Initialize socket globally
        socket.emit('game_update', { board: board, currentPlayer: currentPlayer });
    }
}

// Enable capturing logic
function enableToCapture(p) {
    let find = false, pos = null, old = null;

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

        // Reset state
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

// Enable moving logic
function enableToMove(p) {
    let find = posNewPosition.some(pos => pos.compare(p));

    if (find) {
        moveThePiece(p);
    } else {
        buildBoard();
    }
}

// Determine possible moves
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

// Mark possible move positions
function markPossiblePosition(piece, player, direction) {
    posNewPosition.push(new Piece(piece.row + player, piece.column + direction));
}

// Reverse the player turn
function reverse(player) {
    return player === 1 ? -1 : 1;
}

// Build the game board
function buildBoard() {
    const game = document.getElementById('game');
    game.innerHTML = ""; // Clear the board

    let black = 0, white = 0;

    for (let i = 0; i < board.length; i++) {
        let row = document.createElement("div");
        row.setAttribute("class", "row");

        for (let j = 0; j < board[i].length; j++) {
            let col = document.createElement("div");
            let piece = document.createElement("div");
            let caseType = (i % 2 === 0) ? (j % 2 === 0 ? "Whitecase" : "blackCase") : (j % 2 !== 0 ? "Whitecase" : "blackCase");
            let occupied = board[i][j] === 1 ? "whitePiece" : board[i][j] === -1 ? "blackPiece" : "empty";

            piece.setAttribute("class", `occupied ${occupied}`);
            piece.setAttribute("row", i);
            piece.setAttribute("column", j);
            piece.setAttribute("data-position", `${i}-${j}`);
            piece.addEventListener("click", (e) => {
                const row = parseInt(e.target.getAttribute("row"));
                const column = parseInt(e.target.getAttribute("column"));
                moveThePiece(new Piece(row, column));
            });

            col.setAttribute("class", `column ${caseType}`);
            col.appendChild(piece);
            row.appendChild(col);

            if (board[i][j] === -1) black++;
            if (board[i][j] === 1) white++;
        }
        game.appendChild(row);
    }

    displayCounter(black, white);

    if (black === 0 || white === 0) {
        modalOpen(black);
    }
}

// Display the current player
function displayCurrentPlayer() {
    const container = document.getElementById("next-player");
    container.setAttribute("class", `occupied ${currentPlayer === 1 ? "whitePiece" : "blackPiece"}`);
}

// Display the counters for each player's pieces
function displayCounter(black, white) {
    document.getElementById("white-player-count-pieces").textContent = white;
    document.getElementById("black-player-count-pieces").textContent = black;
}

// Open the modal for game over
function modalOpen(black) {
    const modal = document.getElementById("easyModal");
    document.getElementById("winner").textContent = black === 0 ? "White" : "Black";
    document.getElementById("loser").textContent = black !== 0 ? "White" : "Black";
    modal.classList.add("effect");
}

// Close the modal
function modalClose() {
    const modal = document.getElementById("easyModal");
    modal.classList.remove("effect");
}

// Find pieces that can be captured
function findPieceCaptured(p, player) {
    capturedPosition = [];
    let directions = [[player, 1], [player, -1], [-player, 1], [-player, -1]];

    directions.forEach(([dRow, dCol]) => {
        let newRow = p.row + dRow;
        let newColumn = p.column + dCol;
        let jumpRow = p.row + 2 * dRow;
        let jumpColumn = p.column + 2 * dCol;

        if (
            newRow >= 0 && newRow < board.length &&
            newColumn >= 0 && newColumn < board[0].length &&
            board[newRow][newColumn] === reverse(currentPlayer) &&
            board[jumpRow]?.[jumpColumn] === 0
        ) {
            capturedPosition.push({
                newPosition: new Piece(jumpRow, jumpColumn),
                pieceCaptured: new Piece(newRow, newColumn),
            });
        }
    });

    return capturedPosition.length > 0;
}
const board = document.getElementById('board');
const boardSize = 8;
let squares = [];
let selectedPiece = null;
let currentPlayer = 'player1';
let myPlayer = null;
const socket = io();  // Connect to the WebSocket

// Initialize board and join the game
initializeBoard();
socket.emit('join');

// Handle messages from the server
socket.on('assign', (data) => {
    myPlayer = data.player;
    alert(`You are ${myPlayer}`);
});

socket.on('start', () => alert('Game started!'));

socket.on('move', (data) => {
    movePiece(data.fromRow, data.fromCol, data.toRow, data.toCol, data.isKingMove);
    switchPlayer();
});

socket.on('reset', () => {
    alert('Opponent disconnected, game reset.');
    resetGame();
});

// Initialize the board with pieces
function initializeBoard() {
    for (let row = 0; row < boardSize; row++) {
        squares[row] = [];
        for (let col = 0; col < boardSize; col++) {
            const square = document.createElement('div');
            square.classList.add('square', (row + col) % 2 === 0 ? 'white' : 'black');
            square.dataset.row = row;
            square.dataset.col = col;
            square.addEventListener('click', handleSquareClick);

            // Add initial pieces
            if (row < 3 && (row + col) % 2 !== 0) {
                addPiece(square, 'player1');
            } else if (row > 4 && (row + col) % 2 !== 0) {
                addPiece(square, 'player2');
            }

            board.appendChild(square);
            squares[row][col] = square;
        }
    }
}

// Handle square click for movement
function handleSquareClick(event) {
    if (currentPlayer !== myPlayer) return;  // Only allow move if it's the player's turn

    const square = event.currentTarget;
    const row = parseInt(square.dataset.row);
    const col = parseInt(square.dataset.col);

    if (selectedPiece) {
        if (isLegalMove(selectedPiece.row, selectedPiece.col, row, col)) {
            const isKingMove = (myPlayer === 'player1' && row === boardSize - 1) || 
                               (myPlayer === 'player2' && row === 0);
            movePiece(selectedPiece.row, selectedPiece.col, row, col, isKingMove);

            // Send move to the server
            socket.emit('move', {
                fromRow: selectedPiece.row,
                fromCol: selectedPiece.col,
                toRow: row,
                toCol: col,
                isKingMove
            });

            switchPlayer();
            selectedPiece = null;
        } else {
            selectedPiece = null;
        }
    } else if (square.firstChild && square.firstChild.classList.contains(myPlayer)) {
        selectedPiece = { row, col };
    }
}

// Move piece and check king
function movePiece(fromRow, fromCol, toRow, toCol, isKingMove) {
    const piece = squares[fromRow][fromCol].firstChild;
    squares[toRow][toCol].appendChild(piece);
    squares[fromRow][fromCol].removeChild(piece);

    if (isKingMove) {
        piece.classList.add('king');
    }
}

// Switch turn to other player
function switchPlayer() {
    currentPlayer = currentPlayer === 'player1' ? 'player2' : 'player1';
}

// Reset game when one player disconnects
function resetGame() {
    board.innerHTML = '';
    squares = [];
    initializeBoard();
}

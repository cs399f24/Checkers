const board = document.getElementById('board');
const boardSize = 8;
let squares = [];
let selectedPiece = null;
let currentPlayer = 'player1'; // 'player1' for red, 'player2' for black

// Initialize the board with squares and pieces
function initializeBoard() {
  for (let row = 0; row < boardSize; row++) {
    squares[row] = [];
    for (let col = 0; col < boardSize; col++) {
      const square = document.createElement('div');
      square.classList.add('square', (row + col) % 2 === 0 ? 'white' : 'black');
      square.dataset.row = row;
      square.dataset.col = col;
      square.addEventListener('click', handleSquareClick);

      // Place pieces
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

// Add a piece to a specific square
function addPiece(square, player) {
  const piece = document.createElement('div');
  piece.classList.add('piece', player);
  square.appendChild(piece);
}

// Handle square click for movement
function handleSquareClick(event) {
  const square = event.currentTarget;
  const row = parseInt(square.dataset.row);
  const col = parseInt(square.dataset.col);
  
  if (selectedPiece) {
    if (isLegalMove(selectedPiece.row, selectedPiece.col, row, col)) {
      movePiece(selectedPiece.row, selectedPiece.col, row, col);
      checkKing(row, col);
      switchPlayer();
      selectedPiece = null;
    } else {
      selectedPiece = null;
    }
  } else if (square.firstChild && square.firstChild.classList.contains(currentPlayer)) {
    selectedPiece = { row, col };
  }
}

// Check if a move is legal
function isLegalMove(fromRow, fromCol, toRow, toCol) {
  const piece = squares[fromRow][fromCol].firstChild;
  const direction = piece.classList.contains('player1') ? 1 : -1;
  const rowDiff = toRow - fromRow;
  const colDiff = Math.abs(toCol - fromCol);

  if (rowDiff === direction && colDiff === 1 && !squares[toRow][toCol].firstChild) {
    return true;
  }

  if (rowDiff === 2 * direction && colDiff === 2) {
    const midRow = (fromRow + toRow) / 2;
    const midCol = (fromCol + toCol) / 2;
    const midPiece = squares[midRow][midCol].firstChild;

    if (midPiece && !midPiece.classList.contains(currentPlayer)) {
      squares[midRow][midCol].removeChild(midPiece);
      return true;
    }
  }

  return false;
}

// Move a piece on the board
function movePiece(fromRow, fromCol, toRow, toCol) {
  const piece = squares[fromRow][fromCol].firstChild;
  squares[toRow][toCol].appendChild(piece);
  squares[fromRow][fromCol].removeChild(piece);
}

// Check if a piece should be promoted to king
function checkKing(row, col) {
  const piece = squares[row][col].firstChild;
  if ((piece.classList.contains('player1') && row === boardSize - 1) ||
      (piece.classList.contains('player2') && row === 0)) {
    piece.classList.add('king');
  }
}

// Switch the current player
function switchPlayer() {
  currentPlayer = currentPlayer === 'player1' ? 'player2' : 'player1';
}

// Initialize the game
initializeBoard();

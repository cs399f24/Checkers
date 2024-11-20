class Piece {
    constructor(row, column) {
      this.row = row;
      this.column = column;
    }
  
    compare(piece) {
      return piece.row === this.row && piece.column === this.column;
    }
  }
  const modal = document.getElementById("easyModal");
  let game = document.getElementById("game");
  let currentPlayer = 1;
  let posNewPosition = [];
  let capturedPosition = [];
  let board = require("https://checkers-game-cs399.s3.us-east-1.amazonaws.com/checkersboard.json")["board"];
  
  builBoard();
  
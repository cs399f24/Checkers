from flask import Flask, Response, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import boto3
import requests
from botocore.exceptions import ClientError
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Path to JSON file for initial board state
INITIAL_BOARD_PATH = "inplay.json"

# S3 bucket URL for the game template
bucket_url = "https://checkers-game-cs399.s3.amazonaws.com/templates/index.html"

# Route to get the game template
@app.route('/test')
def test():
    return "Hello World"

# Route to get the game template
@app.route('/')
def index():
    with open(INITIAL_BOARD_PATH, 'r') as f:
        board_data = json.load(f)
    #     game = json.load(f)
    # board = game["board"]
    return render_template('index.html', board=board_data['board'])

class Piece:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def compare(self, other):
        return self.row == other.row and self.column == other.column

def move_piece(event):
    piece = event['target']
    row = int(piece['row'])
    column = int(piece['column'])
    p = Piece(row, column)

    global board, current_player, captured_position, pos_new_position, ready_to_move

    if captured_position:
        enable_to_capture(p)
    elif pos_new_position:
        enable_to_move(p)

    if current_player == board[row][column]:
        player = reverse(current_player)
        if not find_piece_captured(p, player):
            find_possible_new_position(p, player)

def enable_to_capture(p):
    find = False
    pos = None
    old = None
    for element in captured_position:
        if element['new_position'].compare(p):
            find = True
            pos = element['new_position']
            old = element['piece_captured']
            break

    if find:
        board[pos.row][pos.column] = current_player
        board[ready_to_move.row][ready_to_move.column] = 0
        board[old.row][old.column] = 0

        global ready_to_move, captured_position, pos_new_position, current_player
        ready_to_move = None
        captured_position = []
        pos_new_position = []
        display_current_player()
        build_board()

        current_player = reverse(current_player)
    else:
        build_board()

def enable_to_move(p):
    possible_moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal directions

    for direction in directions:
        new_row = p.row + direction[0]
        new_column = p.column + direction[1]

        if 0 <= new_row < len(board) and 0 <= new_column < len(board[0]):
            if board[new_row][new_column] == 0:  # Check if the new position is empty
                possible_moves.append(Piece(new_row, new_column))

    return possible_moves

def reverse(player):
    return -1 if player == 1 else 1

def find_piece_captured(p, player):
    captured_positions = []
    directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]  # Jump directions

    for direction in directions:
        new_row = p.row + direction[0]
        new_column = p.column + direction[1]
        mid_row = p.row + direction[0] // 2
        mid_column = p.column + direction[1] // 2

        if 0 <= new_row < len(board) and 0 <= new_column < len(board[0]):
            if board[new_row][new_column] == 0 and board[mid_row][mid_column] == -player:
                captured_positions.append({
                    'new_position': Piece(new_row, new_column),
                    'piece_captured': Piece(mid_row, mid_column)
                })

    return captured_positions

def find_possible_new_position(p, player):
    global pos_new_position, captured_position
    pos_new_position = enable_to_move(p)
    captured_position = find_piece_captured(p, player)

def display_current_player():
    print(f"Current Player: {'White' if current_player == 1 else 'Black'}")

def build_board():
    for row in board:
        print(' '.join(str(cell) for cell in row))
    print()


#Websocket to handl game updates
@socketio.on('game_update')
def handle_game_update(data):
    emit('game_update', data, broadcast=True)

# Websocket to handle chat messages
@socketio.on('connect')
def handle_connect():
    print("Client connected")

# Websocket to handle client disconnect
@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)
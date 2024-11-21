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
INITIAL_BOARD_PATH = "static/inplay.json"

# S3 bucket URL for the game template
bucket_url = "https://checkers-game-cs399.s3.amazonaws.com/templates/index.html"

# S3 bucket name
@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

# Route to get the game template
@app.route('/test')
def test():
    return "Hello World"

# Route to get the game template
@app.route('/')
def index():
    with open(INITIAL_BOARD_PATH, 'r') as f:
        game = json.load(f)
    board = game["board"]
    return render_template('index.html', board=board)

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
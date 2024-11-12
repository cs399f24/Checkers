<<<<<<< HEAD
from flask import Flask, request, jsonify, render_template
import json
=======
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO
>>>>>>> 9cdb2e4d07493dc3e47fd6bd5bed16ad2c722274
import boto3
from botocore.exceptions import ClientError
from flask_socketio import SocketIO, emit
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
<<<<<<< HEAD
socketio = SocketIO(app)

# DynamoDB configuration
GAME_TABLE_NAME = "checkers-db"  # Change to your game state table name
REGION = "us-east-1"

# Create DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name=REGION)
game_table = dynamodb.Table(GAME_TABLE_NAME)

# S3 configuration
S3_BUCKET_NAME = os.getenv('checkers-bucket')  # Ensure you have this environment variable set
s3 = boto3.client('s3')

# Fetch game state from DynamoDB
def get_game_state_from_dynamodb():
    try:
        response = game_table.get_item(Key={'game_id': 'checkers_game'})
        if 'Item' in response:
            return response['Item']
        else:
            return {
                "board": [
                    [0, -1, 0, -1, 0, -1, 0, -1],
                    [-1, 0, -1, 0, -1, 0, -1, 0],
                    [0, -1, 0, -1, 0, -1, 0, -1],
                    [-1, 0, -1, 0, -1, 0, -1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 1, 0, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0, 1, 0],
                    [0, 1, 0, 1, 0, 1, 0, 1],
                    [1, 0, 1, 0, 1, 0, 1, 0],
                ],
                "currentPlayer": 1
            }
    except ClientError as e:
        raise Exception("Failed to get item from DynamoDB: " + str(e))

# Update game state in DynamoDB
def update_game_state_in_dynamodb(game_state):
    try:
        game_table.put_item(
            Item={
                'game_id': 'checkers_game',
                'board': game_state['board'],
                'currentPlayer': game_state['currentPlayer']
            }
        )
    except ClientError as e:
        raise Exception("Failed to update DynamoDB: " + str(e))

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Get game state route
@app.route('/get_game_state', methods=['GET'])
def get_game_state():
    try:
        game_state = get_game_state_from_dynamodb()
        return jsonify(game_state)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Make move route
@app.route('/make_move', methods=['POST'])
def make_move():
    try:
        data = request.get_json()
        if 'board' in data and 'currentPlayer' in data:
            update_game_state_in_dynamodb(data)
            socketio.emit('game_update', data)  # Emit the updated game state to all connected clients
            return jsonify({"message": "Game state updated successfully"}), 200
        else:
            return jsonify({"error": "Invalid game state data"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# File upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Upload file to S3
    try:
        s3.upload_fileobj(file, S3_BUCKET_NAME, file.filename)
        return jsonify({"message": "File uploaded successfully"}), 200
    except ClientError as e:
        return jsonify({"error": str(e)}), 500

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)
=======




if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
    
>>>>>>> 9cdb2e4d07493dc3e47fd6bd5bed16ad2c722274

from flask import Flask, Response, render_template
from flask_socketio import SocketIO
import boto3
import requests
from botocore.exceptions import ClientError
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)

bucket_name = 'checkers-bucket'



# Home route
@app.route('/')
def index():
    return render_template('index.html', bucket_name=bucket_name)

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

    # Initialize a session using Amazon DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1',  )

# Function to create the DynamoDB table
def create_table():
    table = dynamodb.create_table(
        TableName='checkers-game',
        KeySchema=[
            {
                'AttributeName': 'GameID',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'GameID',
                'AttributeType': 'S'  # String
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    
    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='checkers-game')
    print("Table created successfully.")

# Function to update the game state
def update_game(game_id, board_state, last_move_by):
    table = dynamodb.Table('checkers-game', region_name='us-east-1')
    
    next_turn = 'Player2' if last_move_by == 'Player1' else 'Player1'
    
    try:
        response = table.update_item(
            Key={
                'GameID': game_id
            },
            UpdateExpression='SET BoardState = :boardState, LastMoveBy = :lastMoveBy, CurrentTurn = :nextTurn',
            ExpressionAttributeValues={
                ':boardState': board_state,
                ':lastMoveBy': last_move_by,
                ':nextTurn': next_turn
            },
            ReturnValues="UPDATED_NEW"
        )
        print("Game updated successfully:", response)
    except ClientError as e:
        print("Error updating game:", e.response['Error']['Message'])

# Function to retrieve the current game state
def get_game(game_id):
    table = dynamodb.Table('checkers-game', region_name='us-east-1')
    
    try:
        response = table.get_item(Key={'GameID': game_id})
        if 'Item' in response:
            print("Game data:", json.dumps(response['Item'], indent=4))
        else:
            print("Game not found.")
    except ClientError as e:
        print("Error retrieving game:", e.response['Error']['Message'])

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)
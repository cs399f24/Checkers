from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO
from botocore.exceptions import ClientError
import json
import boto3
import os

app = Flask(__name__)


# Initialize a session using Amazon DynamoDB
dynamodb = boto3.resource('dynamodb')

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
    table = dynamodb.Table('checkers-game')
    
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
    table = dynamodb.Table('checkers-game')
    
    try:
        response = table.get_item(Key={'GameID': game_id})
        if 'Item' in response:
            print("Game data:", json.dumps(response['Item'], indent=4))
        else:
            print("Game not found.")
    except ClientError as e:
        print("Error retrieving game:", e.response['Error']['Message'])



if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
    
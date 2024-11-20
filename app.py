from flask import Flask, Response, render_template, send_from_directory
from flask_socketio import SocketIO
import boto3
import requests
from botocore.exceptions import ClientError
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)

bucket_url = "https://checkers-game-cs399.s3.amazonaws.com/templates/index.html"

@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

@app.route('/test')
def test():
    return "Hello World"

@app.route('/')
def index():
    # Fetch the HTML content from the S3 bucket
    try:
        response = requests.get(bucket_url)
        response.raise_for_status()  # Raise an error for bad status codes
        # html_content = response.text  # Get the HTML content from the response
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Checkers</title>
            <link rel="stylesheet" href="https://checkers-game-cs399.s3.amazonaws.com/static/styles.css" />


            <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.0/socket.io.js"></script>
        </head>
        <body>
            <div class="container">
                <div class="next-player counter">
                    <div class="occupied whitePiece" id="next-player"></div>
                    Player
                </div>
                <div class="game" id="game"></div>
                <div class="counter">
                    <div>
                        <div class="occupied whitePiece"></div>
                        <span id="white-player-count-pieces">10</span>
                    </div>
                    <div>
                        <div class="occupied blackPiece"></div>
                        <span id="black-player-count-pieces">10</span>
                    </div>
                </div>
            </div>

            <div id="easyModal" class="modal">
                <div class="modal-content">
                    <div class="modal-body">
                        <p>The <strong id="winner"></strong> player won the game !!</p>
                        <p><span id="loser"></span>, would you take your revenge ???</p>
                        <div class="btn-container">
                            <button class="btn" onclick="location.reload()">Yes</button>
                            <button class="btn" onclick="modalClose()">No</button>
                        </div>
                    </div>
                </div>
            </div>

            <script src="static/function.js"></script>
            <script src="static/script.js"></script>
                <script>
                //$(function(){
                //    var checkerboard = [];
                //    $.getJSON("checkersboard.json", function(data){
                //        checkerboard = data.board;
                //        renderBoard(checkerboard);
                //    });
                //});

                function renderBoard(board) {
                    const game = document.getElementById("game");
                    game.innerHTML = "";
                    for (let i = 0; i < board.length; i++) {
                        const row = document.createElement("div");
                        row.className = "row";
                        for (let j = 0; j < board[i].length; j++) {
                            const col = document.createElement("div");
                            col.className = "square " + (board[i][j] === -1 ? "black" : "white");
                            if (board[i][j] !== 0) {
                                const piece = document.createElement("div");
                                piece.className = "piece " + (board[i][j] === 1 ? "player1" : "player2");
                                col.appendChild(piece);
                            }
                            row.appendChild(col);
                        }
                        game.appendChild(row);
                    }
                }
            </script>
            <script>
                const socket = io();

                socket.on('game_update', function(data) {
                    // Update the game board with the new game state
                    updateGameBoard(data);
                });

                function updateGameBoard(gameState) {
                    // Logic to update the game board UI based on the new game state
                    console.log("Game state updated:", gameState);
                    // Here you would render the new game state on the board
                }
            </script>
        </body>
        </html>
        """

        return Response(html_content, mimetype='text/html')  # Serve the HTML c>
    except requests.RequestException as e:
        return f"Error fetching HTML from S3: {str(e)}", 500
    # # Fetch the HTML content from the S3 bucket
    # try:
    #     response = requests.get(bucket_url)
    #     response.raise_for_status()  # Raise an error for bad status codes
    #     html_content = response.text  # Get the HTML content from the response
    #     return Response(html_content, mimetype='text/html')  # Serve the HTML c>
    # except requests.RequestException as e:
    #     return f"Error fetching HTML from S3: {str(e)}", 500

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

    # Initialize a session using Amazon DynamoDB
# dynamodb = boto3.resource('dynamodb', region_name='us-east-1',  )

# # Function to create the DynamoDB table
# def create_table():
#     table = dynamodb.create_table(
#         TableName='checkers-game',
#         KeySchema=[
#             {
#                 'AttributeName': 'GameID',
#                 'KeyType': 'HASH'  # Partition key
#             }
#         ],
#         AttributeDefinitions=[
#             {
#                 'AttributeName': 'GameID',
#                 'AttributeType': 'S'  # String
#             }
#         ],
#         ProvisionedThroughput={
#             'ReadCapacityUnits': 5,
#             'WriteCapacityUnits': 5
#         }
#     )
    
#     # Wait until the table exists.
#     table.meta.client.get_waiter('table_exists').wait(TableName='checkers-game')
#     print("Table created successfully.")

# # Function to update the game state
# def update_game(game_id, board_state, last_move_by):
#     table = dynamodb.Table('checkers-game', region_name='us-east-1')
    
#     next_turn = 'Player2' if last_move_by == 'Player1' else 'Player1'
    
#     try:
#         response = table.update_item(
#             Key={
#                 'GameID': game_id
#             },
#             UpdateExpression='SET BoardState = :boardState, LastMoveBy = :lastMoveBy, CurrentTurn = :nextTurn',
#             ExpressionAttributeValues={
#                 ':boardState': board_state,
#                 ':lastMoveBy': last_move_by,
#                 ':nextTurn': next_turn
#             },
#             ReturnValues="UPDATED_NEW"
#         )
#         print("Game updated successfully:", response)
#     except ClientError as e:
#         print("Error updating game:", e.response['Error']['Message'])

# # Function to retrieve the current game state
# def get_game(game_id):
#     table = dynamodb.Table('checkers-game', region_name='us-east-1')
    
#     try:
#         response = table.get_item(Key={'GameID': game_id})
#         if 'Item' in response:
#             print("Game data:", json.dumps(response['Item'], indent=4))
#         else:
#             print("Game not found.")
#     except ClientError as e:
#         print("Error retrieving game:", e.response['Error']['Message'])

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)
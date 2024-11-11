from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit, join_room
import boto3
import os

app = Flask(__name__)
app.secret_key = os.getenv('Flask_SECRET_KEY', 'default_secret_key') #set secret key for session
socketio = SocketIO(app , cors_allowed_origins="*") 

#Initialize S3 services
s3 = boto3.client('s3')

#function to get the bucket name 
def get_bucket_name():
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        if 'your-bucket-prefix' in bucket['Name']:
            return bucket['Name']
    return 'defualt-bucket-name'

# # Store connections and player assignments
bucket_name = 'Checkers'
players = []
room_id = "checkers_game"  # We'll use a single game room for simplicity

@app.route('/')
def index():
    bucket_name = get_bucket_name()
    return render_template('index.html', bucket_name=bucket_name)

# When a player connects, assign them a player number and join them to the room
@socketio.on('join')
def on_join():
    if len(players) >= 2:  
        emit('error', {'message': 'Game full'})
        return

    player = 'player1' if len(players) == 0 else 'player2'
    players.append(player)
    join_room(room_id)
    emit('player_assigned', {'player': player})

    if len(players) == 2:
        emit('start', room=room_id)

# Handle moves sent by a player
@socketio.on('move')
def on_move(data):
    emit('move', data, room=room_id)

# Handle player disconnect
@socketio.on('disconnect')
def on_disconnect():
    if request.sid in players:
        players.remove(request.sid)
    emit('reset', room=room_id)

# Endpoint to start a new game
@app.route('/start', methods=['POST']) # this function allows the POST method
def start_game():
    game_state = {}  # Initialize game state
    return jsonify(game_state) # this is required when sending any JSON value from flask, it basically sets the content-type headers and a few other helpful things, this should also be followed by `, 200` as a status code for the function but it does default to 200 iirc. 
@app.route('/state', methods=['GET']) # the methods='GET' is optional, as its the same as the default value

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
    # socketio.run(app, host="0.0.0.0", port=8080)

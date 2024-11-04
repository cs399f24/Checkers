from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit, join_room
import boto3

app = Flask(__name__)
app.secret_key = 'secret' #set secret key for session
socketio = SocketIO(app)

#Cognito
cognito = boto3.client('cognito-idp', region_name='your-region')
cognito_client_id = 'your-cognito-client-id'

# Store connections and player assignments
bucket_name = 'Checkers'
players = []
room_id = "checkers_game"  # We'll use a single game room for simplicity

#route user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    try:
        response = cognito.initiate_auth(
            ClientId=cognito_client_id,
            AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={'USERNAME': username, 'PASSWORD': password}
        )
        # Save the token in session for subsequent requests
        session['token'] = response['AuthenticationResult']['IdToken']
        return redirect(url_for('index'))
    except cognito.exceptions.NotAuthorizedException:
        return jsonify({"error": "Invalid credentials"}), 401
    
    return render_template('login.html')

# Check if the user is authenticated before allowing them to join the game
def is_authenticated():
    token = session.get('token')
    if not token:
        return False

    # Optionally, add token validation logic here if needed

    return True

@app.route('/')
def index():
    if not is_authenticated():
        return redirect(url_for('login'))
    return render_template('index.html', bucket_name=bucket_name)

# When a player connects, assign them a player number and join them to the room
@socketio.on('join')
def on_join():
    if not is_authenticated():
        emit('error', {'message': 'User not authenticated'})
        return

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

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
    socketio.run(app, host="0.0.0.0", port=8080)
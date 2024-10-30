from flask import Flask, render_template, request, redirect, url_for
# from flask_cognito import CognitoAuth
#from flask_socketio import SocketIO, emit, join_room, leave_room
#import boto3

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# app.config['COGNITO_REGION'] = 'your-region'
# app.config['COGNITO_USERPOOL_ID'] = 'your-user-pool-id'
# app.config['COGNITO_APP_CLIENT_ID'] = 'your-app-client-id'
# app.config['COGNITO_APP_CLIENT_SECRET'] = 'your-app-client-secret'
# app.config['COGNITO_CHECK_TOKEN_EXPIRATION'] = False

# cognito = CognitoAuth(app)
#socketio = SocketIO(app)

# Store connections and player assignments
#s3 = boto3.client('s3')
bucket_name = 'Checkers'

# players = []
# room_id = "checkers_game"  # We'll use a single game room for simplicity

@app.route('/')
def index():
    return render_template('index.html', bucket_name=bucket_name)

#@app.route('/login')
#def login():
#    return redirect(cognito.get_sign_in_url())

#@app.route('/logout')
#def logout():
#    return redirect(cognito.get_sign_out_url())

# @app.route('/callback')
# def callback():
#     access_token = cognito.get_access_token(request.args)
#     if access_token:
#         return redirect(url_for('index'))
#     else:
#         return 'Login failed', 401

# When a player connects, assign them a player number and join them to the room
# @socketio.on('join')
# @cognito.auth_required
# def on_join():
#     if len(players) >= 2:
#         emit('error', {'message': 'Game full'})
#         return

#     player = 'player1' if len(players) == 0 else 'player2'
#     players.append(player)
#     join_room(room_id)
#     emit('player_assigned', {'player': player})

#     if len(players) == 2:
#         emit('start', room=room_id)
#     pass

# Handle moves sent by a player
#@socketio.on('move')
#def on_move(data):
#    emit('move', data, room=room_id)

# Handle player disconnect
#@socketio.on('disconnect')
#def on_disconnect():
#    if request.sid in players:
#        players.remove(request.sid)
#    emit('reset', room=room_id)

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
    #socketio.run(app, host='0.0.0.0', port=8080)

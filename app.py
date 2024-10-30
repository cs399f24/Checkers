from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Store connections and player assignments
players = []
room_id = "checkers_game"  # We'll use a single game room for simplicity

@app.route('/')
def index():
    return render_template('index.html')

# When a player connects, assign them a player number and join them to the room
@socketio.on('join')
def on_join():
    if len(players) >= 2:
        emit('error', {'message': 'Game full'})
        return

    player = 'player1' if len(players) == 0 else 'player2'
    players.append(player)
    join_room(room_id)
    emit('assign', {'player': player}, room=request.sid)

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
    socketio.run(app, host='0.0.0.0', port=8080)

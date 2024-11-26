from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit

app = Flask(__name__)
socketio = SocketIO(app)

waiting_player = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    global waiting_player
    if waiting_player:
        room = f"room-{waiting_player['sid']}-{request.sid}"
        join_room(room)
        join_room(room, sid=waiting_player['sid'])
        emit('startGame', {'room': room}, room=room)
        waiting_player = None
    else:
        waiting_player = {'sid': request.sid}

@socketio.on('makeMove')
def on_make_move(data):
    room = data['room']
    cell_index = data['cellIndex']
    emit('opponentMove', {'cellIndex': cell_index}, room=room, include_self=False)

@socketio.on('disconnect')
def on_disconnect():
    global waiting_player
    if waiting_player and waiting_player['sid'] == request.sid:
        waiting_player = None

if __name__ == '__main__':
    socketio.run(app, port=5000)

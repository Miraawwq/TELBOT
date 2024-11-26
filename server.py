from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit, disconnect
from flask_socketio import send

app = Flask(__name__)
socketio = SocketIO(app)

waiting_player = None  # Это будет хранить информацию о первом игроке.

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    global waiting_player
    print(f"Player connected: {request.sid}")

    if waiting_player:
        # Если есть ожидающий игрок, создаем игру
        room = f"room-{waiting_player['sid']}-{request.sid}"
        join_room(room)
        emit('startGame', {'room': room}, room=room)
        waiting_player = None  # Освобождаем место для нового игрока
    else:
        # Если нет ожидающего игрока, то этот игрок ждет
        waiting_player = {'sid': request.sid}
        print(f"Player {request.sid} is waiting for an opponent.")

@socketio.on('makeMove')
def on_make_move(data):
    room = data['room']
    cell_index = data['cellIndex']
    emit('opponentMove', {'cellIndex': cell_index}, room=room, include_self=False)

@socketio.on('disconnect')
def on_disconnect():
    global waiting_player
    print(f"Player disconnected: {request.sid}")
    if waiting_player and waiting_player['sid'] == request.sid:
        waiting_player = None

if __name__ == '__main__':
    socketio.run(app, port=5000)

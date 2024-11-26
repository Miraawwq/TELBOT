from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit, disconnect
from collections import defaultdict

app = Flask(__name__)
socketio = SocketIO(app)

# Лобби и информация о играх
lobbies = defaultdict(list)

@app.route('/')
def index():
    return render_template('index.html')

# Подключение нового игрока
@socketio.on('connect')
def on_connect():
    print(f"Player connected: {request.sid}")
    emit('updateLobbies', list(lobbies.keys()))  # Обновляем список доступных лобби

# Отключение игрока
@socketio.on('disconnect')
def on_disconnect():
    for lobby in lobbies.values():
        if request.sid in lobby:
            lobby.remove(request.sid)
            if len(lobby) == 0:
                del lobbies[lobby[0]]  # Удаляем пустое лобби
            break
    print(f"Player disconnected: {request.sid}")
    emit('updateLobbies', list(lobbies.keys()), broadcast=True)

# Создание лобби
@socketio.on('createLobby')
def create_lobby(nickname):
    lobby_id = f"lobby-{nickname}-{request.sid}"
    lobbies[lobby_id].append(request.sid)
    print(f"Lobby created: {lobby_id} by {nickname}")
    emit('updateLobbies', list(lobbies.keys()), broadcast=True)

# Присоединение к лобби
@socketio.on('joinLobby')
def join_lobby(lobby_id, nickname):
    if lobby_id in lobbies and len(lobbies[lobby_id]) < 2:
        lobbies[lobby_id].append(request.sid)
        join_room(lobby_id)
        emit('startGame', {'room': lobby_id, 'nickname': nickname}, room=lobby_id)
        print(f"{nickname} joined {lobby_id}")
        if len(lobbies[lobby_id]) == 2:
            # Начинаем игру для двух игроков
            emit('startGame', {'room': lobby_id}, room=lobby_id)
        emit('updateLobbies', list(lobbies.keys()), broadcast=True)
    else:
        emit('error', 'Lobby is full or does not exist.')

# Ход игрока
@socketio.on('makeMove')
def on_make_move(data):
    room = data['room']
    cell_index = data['cellIndex']
    emit('opponentMove', {'cellIndex': cell_index}, room=room, include_self=False)

if __name__ == '__main__':
    socketio.run(app, port=5000)

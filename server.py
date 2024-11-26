from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import math

app = Flask(__name__)
socketio = SocketIO(app)

# Игровые объекты
players = {}

# Размер поля
FIELD_WIDTH = 800
FIELD_HEIGHT = 600

# Стартовые параметры игрока
START_RADIUS = 10
START_X = FIELD_WIDTH // 2
START_Y = FIELD_HEIGHT // 2

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join_game')
def on_join_game(data):
    player_id = data['player_id']
    # Инициализация нового игрока
    players[player_id] = {
        'x': START_X,
        'y': START_Y,
        'radius': START_RADIUS
    }
    # Отправляем всем игрокам обновленный список игроков
    emit('game_state', players, broadcast=True)

@socketio.on('move_player')
def on_move_player(data):
    player_id = data['player_id']
    move_x = data['move_x']
    move_y = data['move_y']
    
    # Обновляем позицию игрока
    if player_id in players:
        players[player_id]['x'] += move_x
        players[player_id]['y'] += move_y
        
        # Поглощение других игроков
        for other_player_id, other_player in players.items():
            if other_player_id != player_id:
                distance = math.sqrt((other_player['x'] - players[player_id]['x'])**2 + 
                                     (other_player['y'] - players[player_id]['y'])**2)
                if distance < players[player_id]['radius'] + other_player['radius']:
                    # Игрок поглощает другого
                    players[player_id]['radius'] += other_player['radius'] // 2
                    del players[other_player_id]  # Удаляем поглощенного игрока
                    break

    # Отправляем обновленное состояние игры
    emit('game_state', players, broadcast=True)

@socketio.on('disconnect')
def on_disconnect():
    player_id = request.sid
    if player_id in players:
        del players[player_id]
        emit('game_state', players, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, port=5000)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import json

app = Flask(__name__)
socketio = SocketIO(app)

# Настройки игры
GAME_WIDTH = 600
GAME_HEIGHT = 400
FOOD_SIZE = 10
SNAKE_SIZE = 10

# Структура для хранения состояний игроков
players = {}

# Функция для генерации случайной еды
def generate_food():
    return {
        'x': random.randint(0, (GAME_WIDTH - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE,
        'y': random.randint(0, (GAME_HEIGHT - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE
    }

# Когда новый игрок подключается
@socketio.on('join_game')
def join_game(data):
    player_id = data['player_id']
    players[player_id] = {
        'x': GAME_WIDTH // 4 if len(players) == 0 else 3 * GAME_WIDTH // 4,
        'y': GAME_HEIGHT // 2,
        'direction': 'right',
        'body': [(GAME_WIDTH // 4, GAME_HEIGHT // 2)] if len(players) == 0 else [(3 * GAME_WIDTH // 4, GAME_HEIGHT // 2)],
        'score': 0
    }
    food = generate_food()  # генерируем еду
    emit('game_state', {'players': players, 'food': food}, broadcast=True)

# Управление змейкой
@socketio.on('move_player')
def move_player(data):
    player_id = data['player_id']
    direction = data['direction']
    
    # Обновляем направление игрока
    if player_id in players:
        player = players[player_id]
        if direction == 'up' and player['direction'] != 'down':
            player['direction'] = 'up'
        elif direction == 'down' and player['direction'] != 'up':
            player['direction'] = 'down'
        elif direction == 'left' and player['direction'] != 'right':
            player['direction'] = 'left'
        elif direction == 'right' and player['direction'] != 'left':
            player['direction'] = 'right'

# Логика движения змейки
def move_snakes():
    food = generate_food()  # генерируем новую еду
    for player_id, player in players.items():
        x, y = player['body'][0]  # голова змейки

        if player['direction'] == 'up':
            y -= SNAKE_SIZE
        elif player['direction'] == 'down':
            y += SNAKE_SIZE
        elif player['direction'] == 'left':
            x -= SNAKE_SIZE
        elif player['direction'] == 'right':
            x += SNAKE_SIZE

        # Добавляем новую голову
        new_head = (x, y)

        # Проверка на столкновение с собой
        if new_head in player['body']:
            players.pop(player_id)  # Игрок проиграл, удаляем его
            break
        
        # Добавляем новую голову к телу змейки
        player['body'] = [new_head] + player['body'][:-1]

        # Проверка на столкновение с едой
        if (x, y) == (food['x'], food['y']):
            player['body'].append(player['body'][-1])  # Добавляем новый сегмент
            player['score'] += 1
            food = generate_food()  # генерируем новую еду

    return food

# Игровой цикл
def game_loop():
    food = move_snakes()  # Двигаем змей
    socketio.emit('game_state', {'players': players, 'food': food}, broadcast=True)

# Запускаем игровой цикл каждую 1/10 секунды
socketio.start_background_task(game_loop)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, port=5000)

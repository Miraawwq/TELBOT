from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

# Очередь игроков
players_queue = []

# Активные игры
games = {}

@app.route("/")
def index():
    """Главная страница для рендера HTML."""
    return render_template("index.html")

@app.route("/connect", methods=["POST"])
def connect():
    """Подключение игрока к очереди."""
    user_id = request.json["userId"]

    # Если игрока нет в очереди, добавить
    if user_id not in players_queue:
        players_queue.append(user_id)

    # Если хватает игроков, создать игру
    if len(players_queue) >= 2:
        player1 = players_queue.pop(0)
        player2 = players_queue.pop(0)

        # Случайно назначить X или O
        player1_mark = random.choice(["X", "O"])
        player2_mark = "O" if player1_mark == "X" else "X"

        # Создать ID игры
        game_id = f"{player1}_{player2}"
        games[game_id] = {
            "board": [""] * 9,
            "turn": player1,  # Кто начинает
            "players": {player1: player1_mark, player2: player2_mark},
        }

        return jsonify({"gameId": game_id, "mark": games[game_id]["players"][user_id], "currentTurn": "X"})

    # Если нет противника
    return jsonify({"message": "Waiting for opponent..."})

@app.route("/move/<game_id>", methods=["POST"])
def move(game_id):
    """Обработка хода игрока."""
    index = request.json["index"]  # Клетка на доске
    user_id = request.json["userId"]
    game = games.get(game_id)

    # Проверка валидности хода
    if game and game["turn"] == user_id and game["board"][index] == "":
        mark = game["players"][user_id]
        game["board"][index] = mark

        # Проверить победителя
        winner = check_winner(game["board"])

        # Если нет победителя, передать ход
        if not winner:
            game["turn"] = next(player for player in game["players"] if player != user_id)

        return jsonify({"board": game["board"], "currentTurn": game["turn"], "winner": winner})

    return jsonify({"error": "Invalid move"}), 400

def check_winner(board):
    """Проверить победителя на доске."""
    win_positions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Горизонтали
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Вертикали
        [0, 4, 8], [2, 4, 6],            # Диагонали
    ]
    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] != "":
            return board[pos[0]]
    if "" not in board:
        return "Draw"  # Ничья
    return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

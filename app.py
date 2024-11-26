from flask import Flask, request, jsonify
import random

app = Flask(__name__)

players_queue = []
games = {}

@app.route("/connect", methods=["POST"])
def connect():
    user_id = request.json["userId"]
    if user_id not in players_queue:
        players_queue.append(user_id)

    if len(players_queue) >= 2:
        player1 = players_queue.pop(0)
        player2 = players_queue.pop(0)
        game_id = f"{player1}_{player2}"
        games[game_id] = {"board": [""] * 9, "turn": player1, "players": {player1: "X", player2: "O"}}
        return jsonify({"gameId": game_id, "mark": "X", "currentTurn": "X" if user_id == player1 else "O"})

    return jsonify({"message": "Waiting for opponent..."})

@app.route("/move/<game_id>", methods=["POST"])
def move(game_id):
    index = request.json["index"]
    mark = request.json["mark"]
    game = games[game_id]

    if game["board"][index] == "":
        game["board"][index] = mark
        game["turn"] = "O" if mark == "X" else "X"
        winner = check_winner(game["board"])
        return jsonify({"board": game["board"], "currentTurn": game["turn"], "winner": winner})

    return jsonify({"error": "Invalid move"}), 400

def check_winner(board):
    win_positions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6],
    ]
    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] != "":
            return board[pos[0]]
    if "" not in board:
        return "Draw"
    return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

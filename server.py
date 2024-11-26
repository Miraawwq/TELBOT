from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Список всех нарисованных линий
drawings = []

@app.route('/')
def index():
    return render_template('index.html')

# Когда кто-то рисует, добавляем линии в список и отправляем их всем
@socketio.on('draw')
def handle_draw(data):
    # Добавляем полученные координаты в общий список
    drawings.append(data)
    # Отправляем данные о рисовании всем пользователям
    emit('draw', data, broadcast=True)

# Когда пользователь заходит на страницу, отсылаем все нарисованные линии
@socketio.on('get_drawings')
def send_drawings():
    for drawing in drawings:
        emit('draw', drawing)

# Очистка холста для всех пользователей
@socketio.on('clear')
def clear_canvas():
    drawings.clear()
    emit('clear', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, port=5000)

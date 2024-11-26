from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

# Обработка рисования
@socketio.on('draw')
def handle_draw(data):
    # Отправляем координаты другим пользователям для отображения рисования
    emit('draw', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, port=5000)

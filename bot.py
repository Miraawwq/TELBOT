import os
from flask import Flask, render_template, request
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Файл с данными пользователей
USER_DATA_FILE = "users.txt"

# Чтение данных из файла
def load_users():
    """Загрузка пользователей из текстового файла"""
    users = {}
    try:
        with open(USER_DATA_FILE, "r") as file:
            for line in file:
                surname, login, password = line.strip().split(":")
                users[surname.lower()] = (login, password)
    except FileNotFoundError:
        print("Файл users.txt не найден!")
    return users

@app.route('/')
def home():
    return render_template('index.html', message=None)

@app.route('/submit', methods=['POST'])
def submit():
    surname = request.form['surname'].strip().lower()
    users = load_users()
    if surname in users:
        login, password = users[surname]
        message = f"Your login: {login}\nYour password: {password}"
    else:
        message = "Surname not found. Please check the input."
    
    return render_template('index.html', message=message)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Файл с данными пользователей
USER_DATA_FILE = "users.txt"

# URL вашего Power Automate Flow
POWER_AUTOMATE_URL = "https://prod-63.westeurope.logic.azure.com:443/workflows/33afcf5655dd40f9aa54fd641b888372/triggers/manual/paths/invoke?api-version=2016-06-01"  # Вставьте ваш URL

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

        # Отправка сообщения в Teams через Power Automate
        data = {
            "name": surname.capitalize(),
            "login": login,
            "password": password
        }
        response = requests.post(POWER_AUTOMATE_URL, json=data)

        # Проверяем успешность отправки
        if response.status_code == 200:
            return render_template('index.html', message=f"Message successfully sent to {surname.capitalize()} in Teams!")
        else:
            return render_template('index.html', message="Failed to send message to Teams.")
    else:
        return render_template('index.html', message="Surname not found. Please check the input.")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 8443)))

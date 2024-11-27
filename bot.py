import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, filters

# Файл с данными пользователей
USER_DATA_FILE = "users.txt"

# Чтение данных из файла
def load_users():
    """Загрузка пользователей из текстового файла"""
    users = {}
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            surname, login, password = line.strip().split(":")
            users[surname.lower()] = (login, password)
    return users

# Обработчик текстовых сообщений
def handle_message(update: Update, context: CallbackContext):
    """Обработка сообщений с фамилией и отправка логина и пароля"""
    users = load_users()
    surname = update.message.text.strip().lower()

    if surname in users:
        login, password = users[surname]
        update.message.reply_text(f"Ваш логин: {login}\nВаш пароль: {password}")
    else:
        update.message.reply_text("Фамилия не найдена. Проверьте ввод.")

# Главная функция запуска бота
def main():
    # Получение токена из переменной окружения
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("Не указан TELEGRAM_BOT_TOKEN в переменных окружения!")

    # Инициализация Updater
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Добавление обработчика для текстовых сообщений
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

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
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка сообщений с фамилией и отправка логина и пароля"""
    users = load_users()
    surname = update.message.text.strip().lower()

    if surname in users:
        login, password = users[surname]
        await update.message.reply_text(f"Ваш логин: {login}\nВаш пароль: {password}")
    else:
        await update.message.reply_text("Фамилия не найдена. Проверьте ввод.")

# Главная функция запуска бота
def main():
    # Получение токена из переменной окружения
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise ValueError("Не указан TELEGRAM_BOT_TOKEN в переменных окружения!")

    # Создание приложения Telegram Bot
    app = ApplicationBuilder().token(TOKEN).build()

    # Добавление обработчика для текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()

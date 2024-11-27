import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

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

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ответ на команду /start"""
    await update.message.reply_text("Enter your last name in English")

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
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    PORT = int(os.getenv("PORT", "8443"))
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://telbot-h594.onrender.com/")

    app = ApplicationBuilder().token(TOKEN).build()

    # Добавление обработчиков
    app.add_handler(CommandHandler("start", start))  # Обработчик команды /start
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # Обработчик текстовых сообщений

    # Запуск с вебхуком
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
    )

if __name__ == "__main__":
    main()

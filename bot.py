from telegram.ext import CommandHandler, MessageHandler, ApplicationBuilder, ContextTypes, filters
from telegram import Update
import logging
import os
import asyncio

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Функция для загрузки данных из файла
def load_data(file_path):
    data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(';')
            if len(parts) == 3:
                surname, login, password = parts
                data[surname.lower()] = (login, password)
    return data

# Загружаем данные из файла
DATA_FILE = 'data.txt'
user_data = load_data(DATA_FILE)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши свою фамилию, чтобы получить логин и пароль.")

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    surname = update.message.text.strip().lower()
    if surname in user_data:
        login, password = user_data[surname]
        await update.message.reply_text(f"Ваш логин: {login}\nВаш пароль: {password}")
    else:
        await update.message.reply_text("Извините, ваша фамилия не найдена. Убедитесь, что вы ввели ее правильно.")

# Основная функция для запуска бота
async def main():
    # Получаем токен, URL вебхука и порт из переменных среды
    API_TOKEN = os.getenv("API_TOKEN")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    PORT = int(os.getenv("PORT", 5000))  # Используем порт из переменной окружения

    if not API_TOKEN or not WEBHOOK_URL:
        raise ValueError("Необходимо установить переменные окружения API_TOKEN и WEBHOOK_URL")

    app = ApplicationBuilder().token(API_TOKEN).build()

    # Обработчики команд и сообщений
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Устанавливаем вебхук
    await app.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")

    print("Бот запущен!")
    # Указываем порт и слушателя для работы вебхука
    await app.run_webhook(port=PORT, listen="0.0.0.0")

# Запуск с учетом уже работающего события
if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError as e:
        if str(e) == "This event loop is already running":
            asyncio.run(main())
        else:
            raise

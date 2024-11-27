import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    MessageHandler, 
    ContextTypes, 
    filters
)

# Функция обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Здравствуйте! Напишите свою фамилию, чтобы получить логин и пароль.")

# Функция обработки сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    surname = update.message.text.strip()  # Получаем фамилию из сообщения
    try:
        # Читаем файл с данными
        with open("data.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        # Поиск фамилии в файле
        for line in lines:
            stored_surname, login, password = line.strip().split(",")
            if stored_surname.lower() == surname.lower():
                await update.message.reply_text(f"Ваши данные:\nЛогин: {login}\nПароль: {password}")
                return
        # Если фамилия не найдена
        await update.message.reply_text("Фамилия не найдена. Проверьте правильность ввода.")
    except FileNotFoundError:
        await update.message.reply_text("Ошибка: файл с данными не найден.")
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")

# Основная функция для запуска бота
async def main():
    # Токен и URL вебхука из переменных окружения
    API_TOKEN = os.getenv("API_TOKEN")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")

    app = ApplicationBuilder().token(API_TOKEN).build()

    # Обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Устанавливаем вебхук
    await app.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")

    print("Бот запущен!")
    # Запускаем веб-сервер для обработки вебхуков
    await app.run_webhook(port=8000, listen="0.0.0.0")

# Запуск программы
if __name__ == "__main__":
    asyncio.run(main())

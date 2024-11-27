import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Включение логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Установите ваш токен
TOKEN = 'YOUR_BOT_TOKEN'
PORT = 8443  # Порт для вебхуков, вы можете изменить по своему усмотрению

async def start(update: Update, context: CallbackContext):
    """Отправить сообщение при команде /start."""
    await update.message.reply_text("Привет! Я ваш Telegram бот.")

async def main():
    """Основная функция для запуска бота."""
    # Создание экземпляра бота
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))

    # Попытка запустить вебхук
    await application.run_webhook(port=PORT, listen="0.0.0.0", url_path="/webhook")

# Проверка, если уже работает цикл событий
loop = asyncio.get_event_loop()

if loop.is_running():
    # Если цикл уже работает, используем create_task для добавления задачи
    loop.create_task(main())
else:
    # Если цикл не запущен, запускаем его
    loop.run_until_complete(main())

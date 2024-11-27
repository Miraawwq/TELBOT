from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Файл с данными пользователей
USER_DATA_FILE = "users.txt"

# Чтение данных из файла
def load_users():
    users = {}
    with open(USER_DATA_FILE, "r") as file:
        for line in file:
            surname, login, password = line.strip().split(":")
            users[surname.lower()] = (login, password)
    return users

# Главная функция обработки сообщений
def handle_message(update: Update, context: CallbackContext):
    users = load_users()
    surname = update.message.text.strip().lower()
    
    if surname in users:
        login, password = users[surname]
        update.message.reply_text(f"Ваш логин: {login}\nВаш пароль: {password}")
    else:
        update.message.reply_text("Фамилия не найдена. Проверьте ввод.")

# Запуск бота
def main():
    TOKEN = "7538272830:AAFZpUeFmrWTQLdIiKM-bgNDBLBnC9-X2C4"
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Обработка текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

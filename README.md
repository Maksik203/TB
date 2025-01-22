import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import sqlite3

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Создание базы данных
def create_db():
    conn = sqlite3.connect('fitness_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            subscription INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    conn = sqlite3.connect('fitness_bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()
    
    update.message.reply_text('Добро пожаловать! Используйте /subscribe для подписки на фитнес советы.')

# Команда /subscribe
def subscribe(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    conn = sqlite3.connect('fitness_bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET subscription = 1 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    update.message.reply_text('Вы подписались на платные фитнес советы!')

# Команда /unsubscribe
def unsubscribe(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    conn = sqlite3.connect('fitness_bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET subscription = 0 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    update.message.reply_text('Вы отписались от платных фитнес советов.')

# Команда /exercises
def exercises(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    conn = sqlite3.connect('fitness_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT subscription FROM users WHERE user_id = ?', (user_id,))
    subscription = cursor.fetchone()[0]
    conn.close()
    
    if subscription:
        update.message.reply_text('Вот Ваши упражнения для набора/сброса веса: [Список упражнений]')
    else:
        update.message.reply_text('Подпишитесь, чтобы получить доступ к большему количеству упражнений!')

def main() -> None:
    create_db()
    updater = Updater("YOUR_TOKEN_HERE")

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Регистрация обработчиков команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("subscribe", subscribe))
    dispatcher.add_handler(CommandHandler("unsubscribe", unsubscribe))
    dispatcher.add_handler(CommandHandler("exercises", exercises))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

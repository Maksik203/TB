import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
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

# Инициализация бота и диспетчера
API_TOKEN = "YOUR_API_TOKEN"  # Замените на Ваш токен
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Команда /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    conn = sqlite3.connect('fitness_bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()
    
    await message.reply('Добро пожаловать! Используйте /subscribe для подписки на фитнес советы.')

# Команда /subscribe
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    user_id = message.from_user.id
    conn = sqlite3.connect('fitness_bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET subscription = 1 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    await message.reply('Вы подписались на платные фитнес советы!')

# Команда /unsubscribe
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    user_id = message.from_user.id
    conn = sqlite3.connect('fitness_bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET subscription = 0 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    await message.reply('Вы отписались от платных фитнес советов.')

# Команда /exercises
@dp.message_handler(commands=['exercises'])
async def exercises(message: types.Message):
    user_id = message.from_user.id
    conn = sqlite3.connect('fitness_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT subscription FROM users WHERE user_id = ?', (user_id,))
    subscription = cursor.fetchone()[0]
    conn.close()
    
    if subscription:
        await message.reply('Вот Ваши упражнения для набора/сброса веса: [Список упражнений]')
    else:
        await message.reply('Подпишитесь, чтобы получить доступ к большему количеству упражнений!')

# Новая команда /send_video
@dp.message_handler(commands=['send_video'])
async def send_video(message: types.Message):
    user_id = message.from_user.id
    conn = sqlite3.connect('fitness_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT subscription FROM users WHERE user_id = ?', (user_id,))
    subscription = cursor.fetchone()[0]
    conn.close()
    
    if subscription:
        video_path = 'path/to/your/video.mp4'  # Укажите путь к Вашему видео
        with open(video_path, 'rb') as video:
            await message.reply_video(video=video, caption='Вот Ваше видео с упражнениями!')
    else:
        await message.reply('Подпишитесь, чтобы получить доступ к видео!')

if __name__ == '__main__':
    create_db()
    executor.start_polling(dp, skip_updates=True)

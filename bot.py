import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.utils import executor

API_TOKEN = '7927202797:AAFxl7ZdIrZd-_61ZiYObNOJr4INwYsJekQ'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Клавиатура с кнопками
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["Программисты", "Политика", "Вовочка", "Животные","Любовь","Армия","Любовника","Учитель","Электрик"]
keyboard.add(*buttons)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Выберите тему анекдота:", reply_markup=keyboard)

# Обработчик нажатий на кнопки
@dp.message_handler(filters.Text(equals=buttons))
async def send_joke(message: types.Message):
    if message.text == "Программисты":
        await message.answer("— Вчера долго пыталась объяснить бабуле, что работаю программистом.— Удалось?— Короче, сошлись на том, что чиню телевизоры и развожу мышей.")
    elif message.text == "Политика":
        await message.answer("-Рабинович, я вам уже третий анекдот про политику расказываю, а вы все не смеётесь! -Моня, простите... Я таки думал, шо это новости ")
    elif message.text == "Вовочка":
        await message.answer("Девочки:если Ввочка скажет хоть 1 плохое слово на уроке встаем и уходим урок географии  Учитель: назавите дети назавите что строят в нашем городе. дети:Школы, больницы магазины.Вовочка:бордель Девочки:встают и уходят Вовочка:куда вы там только фундамент положили.")
    elif message.text == "Животные":
        await message.answer("Летит орел из жопу глист вылазит и говарит копитан какая высота Орел:3км Глист:слыш ты там не обосрись, братва волнуется")
    elif message.text == "Любовь":
        await message.answer("Встреча заблудившегося туриста с русалкой приятна вдвойне: тут тебе и любовь, и уха!")
    elif message.text == "Армия":
        await message.answer("— Але! Да, я. Ну здравствуй, здравствуй! Нет. Нет, радость моя, сегодня не приду. Нет-нет, не получится! И завтра не приду, глупышка. Да не смогу. Ну не расстраивайся. Ну давай все пока. Нет ты первый клади. Ну давай. Ну пока. Ну все давай, пока.— Дорогой, кто это был?— Военкомат.")
    elif message.text == "Любовника":
        await message.answer("Муж приходит домой с явными признаками измены. Жена:— Ну хорошо! Я завтра тоже…— Не смей, дура!— Это почему же?— Когда я — значит мы их, а если ты — то они нас! ")
    elif message.text == "Учитель":
        await message.answer("Учительница на уроке природоведения задает вопрос: — Дети, чего звери больше всего боятся в лесу? Ответ хором: — Машу!")
    elif message.text == "Электрик":
        await message.answer("Сидят два электрика на столбе и спорят. — Земля! — Нет, фаза. Внизу проходит старушка. Электрики ей: — Бабуля, подай провод! Старушка подала и пошла дальше. — Я же говорил земля, а ты фаза-фаза…")
        
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


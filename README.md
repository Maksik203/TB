# TB
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
bot = Bot(token='')
dp = Dispatcher(bot)
# Создаем первую клавиатуру
button_save = KeyboardButton('Сохранить логин и пароль')
button_return = KeyboardButton('Узнать логин и пароль')
keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_save, button_return)
# Создаем вторую клавиатуру
button_yes = KeyboardButton('Да')
button_no = KeyboardButton('Нет')
keyboard2 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_yes, button_no)
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Выберите опцию:", reply_markup=keyboard1)
@dp.message_handler(lambda message: message.text.lower() == 'привет')
async def handle_hi(message: types.Message):
    await message.reply("Что вы хотите сделать?", reply_markup=keyboard1)
@dp.message_handler(lambda message: message.text == 'Сохранить логин и пароль')
async def handle_hi(message: types.Message):
    await message.reply("Введи название сайта")
    
@dp.message_handler(lambda message: '.ru' in message.text)
async def save_pas(message: types.Message):
    f = open('user pasword.txt','a',encoding = 'ANSI')
    f.write(f'{message.from_user.id} {message.text}\n')
    f.close()
@dp.message_handler(lambda message: message.text.lower() == 'пока')
async def handle_bye(message: types.Message):
    await message.reply("До свидания!", reply_markup=types.ReplyKeyboardRemove())
@dp.message_handler(lambda message: message.text.lower() in ['да', 'нет'])
async def handle_yes_no(message: types.Message):
    if message.text.lower() == 'да':
        await message.reply("Вы выбрали 'Да'.", reply_markup=keyboard1)
    else:
        await message.reply("Вы выбрали 'Нет'.", reply_markup=keyboard1)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

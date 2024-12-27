import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from DB import DB

API_TOKEN = ''  
db = DB('db.db')
# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):

    # Создание кнопок
    buttons = [
        types.KeyboardButton("Мой профиль"),
        types.KeyboardButton("Топ 5🏆"),
    ]
    
    # Создание клавиатуры
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(buttons[0])
    keyboard.add(buttons[1])


    user = db.get_user(message['from']['id'])
    if(user == None):
        db.add_user(name=message['from']['first_name'], tgName=message['from']['username'], tgId=message['from']['id'], count=0)
    await message.reply("Привет! Я блефуешь-бот.\nНапиши любое сообщение", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == 'Мой профиль')
async def handle_button_click(message: types.Message):
    user = db.get_user(message['from']['id'])
    if(user == None):
        db.add_user(name=message['from']['first_name'], tgName=message['from']['username'], tgId=message['from']['id'], count=0)
        user = db.get_user(message['from']['id'])
    await message.answer(f"Имя:  {user[1]}  @{user[2]}\nКоличество блефуешь: {user[3]}")

@dp.message_handler(lambda message: message.text == 'Топ 5🏆')
async def handle_button_click(message: types.Message):
    users = db.get_top_five()
    response_message = "Топ 5 пользователей:\n"
    for user in users:
        response_message += f"@{user[2]}: {user[3]}\n" 
    await message.answer(response_message)


@dp.message_handler()
async def echo(message: types.Message):
    db.addCount(message['from']['id'])
    await message.answer("Блефуешь?🤨")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    

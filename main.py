from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from config import token 
import logging
import time
import sqlite3

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO) 

direction_buttons = [ 
    types.KeyboardButton('Меню'),
    types.KeyboardButton('О нас'),
    types.KeyboardButton('Адрес'),
    types.KeyboardButton('Заказать еду') 
] 

direction_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*direction_buttons) 

database = sqlite3.connect('users.db')
cursor = database.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT,
        username VARCHAR(255),
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        date_joined VARCHAR(255)
    ); 
""")
cursor.connection.commit()

database = sqlite3.connect('users.db')
cursor = database.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        name VARCHAR(255),
        phone VARCHAR(255),
        address VARCHAR(255)
    ); 
""")
cursor.connection.commit()

@dp.message_handler(commands='start')
async def start(message:types.Message):
    cursor = database.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    if result == []:
        cursor.execute(f"INSERT INTO users VALUES ('{message.from_user.id}', '{message.from_user.username}', '{message.from_user.first_name}', '{message.from_user.last_name}', '{time.ctime()}');")
    database.commit()
    await message.answer(f"Здравствуйте {message.from_user.full_name}!\nВыберите что вы хотите узнать", reply_markup=direction_keyboard)

@dp.message_handler(text='Меню') 
async def ojak_kebab(message:types.Message):
     await message.answer_photo('https://nambafood.kg/dish_image/150910.png') 
     await message.reply("""Вали кебаб на 4 человек
1000 г
3200 сом""")
     
     await message.answer_photo('https://nambafood.kg/dish_image/163138.png') 
     await message.reply("""Шефим кебаб
420 сом""") 
     
     await message.answer_photo('https://nambafood.kg/dish_image/163139.png') 
     await message.reply("""Симит кебаб
420 сом""") 
     
     await message.answer_photo('https://nambafood.kg/dish_image/163137.png') 
     await message.reply("""Форель на мангале целиком
700 сом""") 

@dp.message_handler(text='О нас') 
async def ojak_kebab(message:types.Message):
    await message.reply("""Кафе "Ожак Кебап" на протяжении 18 лет радует своих гостей с изысканными турецкими блюдами в особенности своим кебабом.
Наше кафе отличается от многих кафе своими доступными ценами и быстрым сервисом.
В 2016 году по голосованию на сайте "Horeca" были удостоены "Лучшее кафе на каждый день" и мы стараемся оправдать доверие наших гостей.
Мы не добавляем консерванты, усилители вкуса, красители, ароматизаторы, растительные и животные жиры, вредные добавки с маркировкой «Е».
 У нас строгий контроль качества: наши филиалы придерживаются норм Кырпотребнадзор и санэпидемстанции. Мы используем только сертифицированную мясную и рыбную продукцию от крупных поставщиков.""") 
    
@dp.message_handler(text='Адрес')  
async def ojak_kebab(message:types.Message):
    await message.reply("""Исы Ахунбаева ,97а+996700505333""") 

class Orders(StatesGroup):
    name = State()
    phone = State()
    address = State()

@dp.message_handler(text='Заказать еду')  
async def ojak_kebab(message:types.Message, state:FSMContext):
    await message.reply("Хорошо, введите свое имя")
    await Orders.name.set()
 

@dp.message_handler(state=Orders.name)
async def name(message:types.Message, state:FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите свой номер телефона")
    await Orders.phone.set()



@dp.message_handler(state=Orders.phone)
async def address(message:types.Message, state:FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Введите свой адрес")
    await Orders.address.set()
    
@dp.message_handler(state=Orders.address)
async def phone(message:types.Message, state:FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()
    cursor = database.cursor()
    cursor.execute(f"INSERT INTO orders VALUES('{data['name']}','{data['phone']}','{data['address']}');")
    database.commit()
    await state.finish()
    await message.answer('Спасибо за заказ!')



executor.start_polling(dp)

# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/Ilimbek4445/ojak_kebeb.git
# git push -u origin main
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta

API_TOKEN = '7143801443:AAHNzs17FTEDCyKwHX7URFDONJ2Px5WrlN0'
ADMIN_ID = 342674896
VPN_SUBSCRIPTION_LINK = 'https://s.creati.win/sub/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzNDI2NzQ4OTYifQ.wVunTH7ngB4dwqrBbUq5qT6UBpRUUSZP5JrCKAqoGQw#✨SiriusVPN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

users = {}  # user_id: expire_date

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(
    KeyboardButton("Оплатить подписку"),
    KeyboardButton("Проверить подписку"),
)
main_menu.add(
    KeyboardButton("Получить ключ"),
    KeyboardButton("Инструкция"),
)
main_menu.add(
    KeyboardButton("Список серверов"),
    KeyboardButton("Тех поддержка"),
)

instruction_menu = ReplyKeyboardMarkup(resize_keyboard=True)
instruction_menu.add(
    KeyboardButton("Для Android"),
    KeyboardButton("Для iPhone"),
)
instruction_menu.add(
    KeyboardButton("Назад"),
)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Добро пожаловать в VPN бот!", reply_markup=main_menu)

@dp.message_handler(lambda msg: msg.text == "Оплатить подписку")
async def pay_sub(message: types.Message):
    await message.answer("Для оплаты переведите 200₽ по СБП на номер:\n\n"
                         "+79061800102 (Тинькофф)\n\n"
                         "После оплаты напишите /activate")

@dp.message_handler(commands=['activate'])
async def activate_user(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Только админ может активировать подписки.")
        return

    target_id = message.reply_to_message.from_user.id if message.reply_to_message else message.from_user.id
    users[target_id] = datetime.now() + timedelta(days=30)
    await message.answer(f"Пользователь {target_id} получил подписку на 30 дней.")

@dp.message_handler(lambda msg: msg.text == "Проверить подписку")
async def check_sub(message: types.Message):
    expire = users.get(message.from_user.id)
    if expire:
        days_left = (expire - datetime.now()).days
        await message.answer(f"Подписка активна. Осталось дней: {days_left}")
    else:
        await message.answer("У вас нет активной подписки.")

@dp.message_handler(lambda msg: msg.text == "Получить ключ")
async def get_key(message: types.Message):
    expire = users.get(message.from_user.id)
    if expire and expire > datetime.now():
        await message.answer(f"Вот ваша ссылка для подключения:\n{VPN_SUBSCRIPTION_LINK}")
    else:
        await message.answer("Подписка не активна.")

@dp.message_handler(lambda msg: msg.text == "Список серверов")
async def list_servers(message: types.Message):
    await message.answer("Список серверов:\n\n1. 🇳🇱 Нидерланды\n2. 🇫🇷 Франция\n3. 🇩🇪 Германия\n4. 🇸🇬 Сингапур")

@dp.message_handler(lambda msg: msg.text == "Тех поддержка")
async def support(message: types.Message):
    await message.answer("Напишите администратору: tg://user?id=342674896")

@dp.message_handler(lambda msg: msg.text == "Инструкция")
async def instruction(message: types.Message):
    await message.answer("Выберите устройство:", reply_markup=instruction_menu)

@dp.message_handler(lambda msg: msg.text == "Для Android")
async def android_instruction(message: types.Message):
    await message.answer(f"1. Установите приложение V2RayTun из Play Market\n"
                         f"2. Нажмите 'Импорт' и вставьте эту ссылку:\n{VPN_SUBSCRIPTION_LINK}")

@dp.message_handler(lambda msg: msg.text == "Для iPhone")
async def iphone_instruction(message: types.Message):
    await message.answer(f"1. Установите приложение Streisand из App Store\n"
                         f"2. Откройте его и вставьте эту ссылку:\n{VPN_SUBSCRIPTION_LINK}")

@dp.message_handler(lambda msg: msg.text == "Назад")
async def back(message: types.Message):
    await message.answer("Главное меню", reply_markup=main_menu)

if __name__ == '__main__':
    executor.start_polling(dp)

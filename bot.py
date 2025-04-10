import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = '7143801443:AAFHgOFsDrphPPXRODN65XXdG7JhHKsEy84'
USER_ID = 34267896
SUPPORT_ID = '@serhiobk'

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(commands=["start", "help"])
async def send_welcome(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Оплатить подписку", callback_data="pay")
    builder.button(text="Проверить подписку", callback_data="check")
    builder.button(text="Техподдержка", url=f"https://t.me/{SUPPORT_ID.lstrip('@')}")
    builder.button(text="Список серверов", callback_data="servers")
    builder.button(text="Получить ключ", callback_data="key")
    builder.button(text="Инструкция", callback_data="instruction")
    await message.answer("Привет! Я бот для VPN-сервиса. Выберите опцию:", reply_markup=builder.as_markup())

@dp.callback_query(lambda c: c.data == "pay")
async def pay_subscription(callback: types.CallbackQuery):
    await callback.message.answer("Реквизиты для оплаты по СБП:\n\nНомер: +79061800102\nСумма: 200₽ на 30 дней")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "check")
async def check_sub(callback: types.CallbackQuery):
    await callback.message.answer("У вас осталось 30 дней подписки (заглушка)")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "servers")
async def servers(callback: types.CallbackQuery):
    await callback.message.answer("Список серверов:\n1. USA\n2. Germany\n3. Russia\n4. Japan")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "key")
async def get_key(callback: types.CallbackQuery):
    await callback.message.answer("Ваш VPN-ключ: VPN-KEY-EXAMPLE")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "instruction")
async def show_instruction(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="Для Android", callback_data="android_instr")
    builder.button(text="Для iPhone", callback_data="iphone_instr")
    await callback.message.answer("Выберите платформу:", reply_markup=builder.as_markup())
    await callback.answer()

@dp.callback_query(lambda c: c.data == "android_instr")
async def android_instr(callback: types.CallbackQuery):
    await callback.message.answer("Инструкция для Android:\nСкачайте V2RayTun\n1. Откройте приложение\n2. Введите ключ и сервер\n3. Подключитесь.")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "iphone_instr")
async def iphone_instr(callback: types.CallbackQuery):
    await callback.message.answer("Инструкция для iPhone:\nСкачайте Streisand\n1. Откройте приложение\n2. Введите ключ и сервер\n3. Подключитесь.")
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, DefaultBotProperties
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = '7143801443:AAEBG6BRDI5ae7P7S0URS414T14aHONbyWE'
USER_ID = 34267896
SUPPORT_ID = '@serhiobk'

# Исправлено: новый способ указания parse_mode (без DeprecationWarning)
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher(storage=MemoryStorage())
router = Router()

@router.message()
async def handle_all_messages(message: Message):
    if message.text in ["/start", "/help"]:
        builder = InlineKeyboardBuilder()
        
        builder.button(text="Оплатить подписку", callback_data="pay")
        builder.button(text="Проверить подписку", callback_data="check")
        builder.button(text="Техподдержка", url=f"https://t.me/{SUPPORT_ID.lstrip('@')}")
        builder.button(text="Список серверов", callback_data="servers")
        builder.button(text="Получить ключ", callback_data="key")
        builder.button(text="Инструкция", callback_data="instruction")
        
        # Каждая кнопка в отдельном ряду
        builder.adjust(1)
        
        await message.answer("Привет! Я бот для VPN-сервиса. Выберите опцию:", reply_markup=builder.as_markup())

@router.callback_query(lambda c: c.data == "pay")
async def pay_subscription(callback: types.CallbackQuery):
    await callback.message.answer("Реквизиты для оплаты по СБП:\n\nНомер: +79061800102\nСумма: 200₽ на 30 дней")
    await callback.answer()

@router.callback_query(lambda c: c.data == "check")
async def check_sub(callback: types.CallbackQuery):
    await callback.message.answer("У вас осталось 30 дней подписки (заглушка)")
    await callback.answer()

@router.callback_query(lambda c: c.data == "servers")
async def servers(callback: types.CallbackQuery):
    await callback.message.answer("Список серверов:\n1. USA\n2. Germany\n3. Russia\n4. Japan")
    await callback.answer()

@router.callback_query(lambda c: c.data == "key")
async def get_key(callback: types.CallbackQuery):
    await callback.message.answer("Ваш VPN-ключ: VPN-KEY-EXAMPLE")
    await callback.answer()

@router.callback_query(lambda c: c.data == "instruction")
async def show_instruction(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="Для Android", callback_data="android_instr")
    builder.button(text="Для iPhone", callback_data="iphone_instr")
    builder.adjust(1)  # Кнопки в отдельных рядах
    await callback.message.answer("Выберите платформу:", reply_markup=builder.as_markup())
    await callback.answer()

@router.callback_query(lambda c: c.data == "android_instr")
async def android_instr(callback: types.CallbackQuery):
    await callback.message.answer(
        "Инструкция для Android:\n"
        "1. Скачайте приложение V2RayTun из Play Market\n"
        "2. Введите ваш ключ и адрес сервера\n"
        "3. Подключитесь и пользуйтесь VPN"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "iphone_instr")
async def iphone_instr(callback: types.CallbackQuery):
    await callback.message.answer(
        "Инструкция для iPhone:\n"
        "1. Скачайте приложение Streisand из App Store\n"
        "2. Введите ваш ключ и адрес сервера\n"
        "3. Подключитесь и пользуйтесь VPN"
    )
    await callback.answer()

async def main():
    # Удаляем вебхук и убеждаемся, что нет конфликта
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Подключаем роутер и запускаем бота
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

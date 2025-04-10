import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = '7143801443:AAEBG6BRDI5ae7P7S0URS414T14aHONbyWE'
ADMIN_ID = 34267896
SUPPORT_USERNAME = '@serhiobk'
VPN_LINK = "https://s.creati.win/sub/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzNDI2NzQ4OTYifQ.wVunTH7ngB4dwqrBbUq5qT6UBpRUUSZP5JrCKAqoGQw#%E2%9C%A8SiriusVPN"

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

@router.message()
async def handle_all_messages(message: Message):
    if message.text == "/start":
        builder = InlineKeyboardBuilder()
        builder.button(text="▶️ Старт", callback_data="main_menu")
        await message.answer(
            "<b>Добро пожаловать в SiriusVPN</b>\n"
            "Надёжный VPN-доступ в одно касание.",
            reply_markup=builder.as_markup()
        )
    else:
        await message.answer("Нажмите /start для начала.")

@router.callback_query(lambda c: c.data == "main_menu")
async def show_main_menu(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="1️⃣ Оплатить подписку", callback_data="pay")
    builder.button(text="2️⃣ Проверить подписку", callback_data="check")
    builder.button(text="3️⃣ Техподдержка", url=f"https://t.me/{SUPPORT_USERNAME.lstrip('@')}")
    builder.button(text="4️⃣ Список серверов", callback_data="servers")
    builder.button(text="5️⃣ Получить ключ", callback_data="key")
    builder.button(text="6️⃣ Инструкция", callback_data="instruction")
    builder.adjust(1)

    await callback.message.answer(
        "<b>Меню управления:</b>\nВыберите нужный пункт ниже:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "pay")
async def pay_subscription(callback: types.CallbackQuery):
    await callback.message.answer(
        "<b>Оплата подписки:</b>\n\n"
        "СБП (Тинькофф)\n"
        "Номер: <code>+79061800102</code>\n"
        "Сумма: 200₽ / 30 дней"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "check")
async def check_sub(callback: types.CallbackQuery):
    await callback.message.answer(
        "<b>Статус подписки:</b>\nОсталось: <code>30 дней</code> (заглушка)"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "servers")
async def servers(callback: types.CallbackQuery):
    await callback.message.answer(
        "<b>Список серверов:</b>\n"
        "🇺🇸 USA\n"
        "🇩🇪 Germany\n"
        "🇷🇺 Russia\n"
        "🇯🇵 Japan"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "key")
async def get_key(callback: types.CallbackQuery):
    await callback.message.answer(
        f"<b>Ваш VPN-ключ:</b>\n\n<code>{VPN_LINK}</code>"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "instruction")
async def show_instruction(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text="📱 Для Android", callback_data="android_instr")
    builder.button(text="📱 Для iPhone", callback_data="iphone_instr")
    builder.adjust(1)
    await callback.message.answer("Выберите вашу платформу:", reply_markup=builder.as_markup())
    await callback.answer()

@router.callback_query(lambda c: c.data == "android_instr")
async def android_instr(callback: types.CallbackQuery):
    await callback.message.answer(
        "<b>Инструкция для Android:</b>\n\n"
        "1. Скачайте <b>V2RayTun</b> из Google Play\n"
        "2. Вставьте ссылку из кнопки 'Получить ключ'\n"
        "3. Нажмите 'Подключиться'"
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "iphone_instr")
async def iphone_instr(callback: types.CallbackQuery):
    await callback.message.answer(
        "<b>Инструкция для iPhone:</b>\n\n"
        "1. Скачайте <b>Streisand</b> из App Store\n"
        "2. Вставьте ссылку из кнопки 'Получить ключ'\n"
        "3. Подключитесь"
    )
    await callback.answer()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

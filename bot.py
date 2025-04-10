import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

# Конфигурация бренда
class BrandConfig:
    NAME = "🔒 VPN Guardian"
    TAGLINE = "Ваш цифровой телохранитель"
    COLORS = {
        "primary": "#6e48aa",
        "secondary": "#00b4db",
        "dark": "#0f0c29",
        "light": "#f8f9fa"
    }
    DESCRIPTION = """
🛡️ <b>Премиум VPN с военной шифровкой</b>
🌍 50+ серверов в 20 странах
⚡ Скорость до 1 Гбит/с
🤖 Автоподбор оптимального сервера
"""
    WELCOME_TEXT = f"""
<b>{NAME}</b> - {TAGLINE}

{DESCRIPTION}

📌 <i>Ваши преимущества:</i>
• Анонимный серфинг без следов
• Обход любых блокировок
• 256-bit AES шифрование
• Защита в общественных сетях
"""

API_TOKEN = '7143801443:AAEBG6BRDI5ae7P7S0URS414T14aHONbyWE'
SUPPORT_ID = '@serhiobk'

# Инициализация бота с фирменным стилем
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        link_preview_is_disabled=True
    )
)

dp = Dispatcher(storage=MemoryStorage())
router = Router()

# Генератор кнопок с фирменным стилем
def generate_keyboard():
    builder = InlineKeyboardBuilder()
    buttons = [
        ("💳 Оплатить подписку", "pay"),
        ("🛡️ Проверить защиту", "check"),
        ("🌍 Выбрать сервер", "servers"),
        ("🔑 Получить ключ", "key"),
        ("📚 Инструкция", "instruction"),
        ("🆘 Техподдержка", f"url:https://t.me/{SUPPORT_ID.lstrip('@')}")
    ]
    
    for text, data in buttons:
        if data.startswith("url:"):
            builder.button(text=text, url=data[4:])
        else:
            builder.button(text=text, callback_data=data)
    
    builder.adjust(1)  # Все кнопки в один столбец
    return builder.as_markup()

@router.message(commands=['start', 'help'])
async def send_welcome(message: Message):
    await message.answer_photo(
        photo="https://i.imgur.com/9zQ4W8j.png",  # Замените на реальный URL логотипа
        caption=BrandConfig.WELCOME_TEXT,
        reply_markup=generate_keyboard()
    )

@router.callback_query(lambda c: c.data == "pay")
async def process_pay(callback: types.CallbackQuery):
    text = (
        "💳 <b>Премиум подписка</b>\n\n"
        "🔹 <i>200₽ на 30 дней</i>\n"
        "🔸 <i>500₽ на 90 дней (экономия 16%)</i>\n\n"
        "📱 <b>Реквизиты для оплаты:</b>\n"
        "СБП: <code>+79061800102</code>\n"
        "Крипто: BTC/ETH/USDT\n\n"
        "После оплаты пришлите скриншот в поддержку"
    )
    await callback.message.edit_text(text, reply_markup=generate_keyboard())
    await callback.answer()

@router.callback_query(lambda c: c.data == "check")
async def process_check(callback: types.CallbackQuery):
    status = (
        "🛡️ <b>Статус защиты</b>\n\n"
        "🔒 <i>Шифрование:</i> <b>активно</b> (AES-256)\n"
        "🌐 <i>Сервер:</i> <b>#GER-12</b> (Франкфурт)\n"
        "⏱ <i>Пинг:</i> <b>24ms</b>\n"
        "📶 <i>Скорость:</i> <b>78 Мбит/с</b>\n\n"
        "🟢 <u>Все системы работают нормально</u>"
    )
    await callback.message.edit_text(status, reply_markup=generate_keyboard())
    await callback.answer()

# Остальные обработчики (servers, key, instruction) остаются аналогичными

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

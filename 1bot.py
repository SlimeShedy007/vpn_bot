import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_polling
from aiogram.utils import ParseMode

API_TOKEN = '7143801443:AAFHgOFsDrphPPXRODN65XXdG7JhHKsEy84'
USER_ID = 34267896
SUPPORT_ID = '@serhiobk'

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я бот для VPN-сервиса. Вот что я могу:\n\n"
        "1. Оплатить подписку\n"
        "2. Проверить подписку\n"
        "3. Техподдержка - @serhiobk\n"
        "4. Список серверов\n"
        "5. Получить ключ (только после подписки)\n"
        "6. Инструкция\n\n"
        "Если нужна помощь, пиши в техподдержку: @serhiobk"
    )

@dp.message_handler(commands=['techsupport'])
async def tech_support(message: types.Message):
    await message.reply(f"Если у вас возникли проблемы, напишите в техподдержку: {SUPPORT_ID}")

@dp.message_handler(commands=['check_sub'])
async def check_subscription(message: types.Message):
    # Here, we can check if the user has a valid subscription, for now just mock it
    days_left = 30  # Mock example
    await message.reply(f"У вас осталось {days_left} дней подписки!")

@dp.message_handler(commands=['servers'])
async def list_servers(message: types.Message):
    await message.reply("Список доступных серверов:\n1. USA\n2. Germany\n3. Russia\n4. Japan")

@dp.message_handler(commands=['get_key'])
async def get_vpn_key(message: types.Message):
    # Check if user is subscribed
    is_subscribed = True  # Mock subscription check
    if is_subscribed:
        vpn_key = "VPN-KEY-EXAMPLE"
        await message.reply(f"Ваш VPN-ключ: {vpn_key}")
    else:
        await message.reply("Подписка не активирована. Пожалуйста, оплатите подписку для получения ключа.")

@dp.message_handler(commands=['instructions'])
async def instructions(message: types.Message):
    await message.reply("Выберите платформу:\n1. Android\n2. iPhone")

@dp.message_handler(commands=['android'])
async def android_instructions(message: types.Message):
    await message.reply("Для Android: Скачайте и установите V2RayTun.\n1. Откройте приложение.\n2. Введите ключ и сервер.\n3. Подключитесь.")

@dp.message_handler(commands=['iphone'])
async def iphone_instructions(message: types.Message):
    await message.reply("Для iPhone: Скачайте и установите Streisand.\n1. Откройте приложение.\n2. Введите ключ и сервер.\n3. Подключитесь.")

if __name__ == '__main__':
    start_polling(dp, skip_updates=True)


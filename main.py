import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '8077162426:AAFFVBr3GWVwELsxYRQjvPVnOzqNxIyen50'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("✅ Bot is online! Your new setup is working.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True

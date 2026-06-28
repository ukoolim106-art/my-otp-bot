import logging
from aiogram import Bot, Dispatcher, executor, types

TOKEN = '8077162426:AAHkbm0XHTQClncR-v4-pMpxuKcLli_dCzk'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Bot is working perfectly!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

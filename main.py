import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '8077162426:AAFFVBr3GWVwELsxYRQjvPVnOzqNxIyen50'
ADMIN_ID = 8531139387

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # মেনু ডিজাইন
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📱 Get Number", callback_data='get_number'),
        types.InlineKeyboardButton("📊 Active Number", callback_data='active_number')
    )
    await message.answer("✅ Bot is Online and Running!\nWelcome to Sojib Number Bot.", reply_markup=markup)

@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("👑 Welcome Boss! You are in Admin Panel.")
    else:
        await message.answer("❌ You are not the admin.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '8077162426:AAFFVBr3GWVwELsxYRQjvPVnOzqNxIyen50'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Start Message with Design
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📱 Get Number", callback_data='get_number'),
        types.InlineKeyboardButton("📊 Active Number", callback_data='active_number'),
        types.InlineKeyboardButton("👑 Admin Panel", callback_data='admin_panel')
    )
    
    text = (f"👋 Hello {message.from_user.first_name}!\n\n"
            "✨ Welcome to Sojib Number Bot.\n"
            "📌 Click below to get started.")
    
    await message.answer(text, reply_markup=markup)

# Handler for buttons
@dp.callback_query_handler(lambda c: c.data == 'get_number')
async def get_number(callback: types.CallbackQuery):
    await callback.message.edit_text("🌍 Select Country:\n\n🇮🇩 Indonesia\n🇸🇳 Senegal\n🇺🇸 USA", 
                                     reply_markup=None)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

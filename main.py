import logging
from aiogram import Bot, Dispatcher, executor, types

# কনফিগারেশন
API_TOKEN = '8077162426:AAHkbm0XHTQClncR-v4-pMpxuKcLli_dCzk'
ADMIN_ID = 8531139387

# লগিং
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Start Command
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📱 Get Number", callback_data='get_number'),
        types.InlineKeyboardButton("📊 Active Number", callback_data='active_number'),
        types.InlineKeyboardButton("🏆 Leaderboard", callback_data='leaderboard')
    )
    await message.answer(f"👋 WELCOME {message.from_user.full_name}!\nTHIS IS [SOJIB NUMBER BOT].", reply_markup=markup)

# Admin Panel
@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("👑 **Admin Panel:** আপনি কন্ট্রোল প্যানেলে আছেন।")
    else:
        await message.answer("❌ অনুমতি নেই।")

# Get Number Menu
@dp.callback_query_handler(lambda c: c.data == 'get_number')
async def get_number(callback: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🇮🇩 Indonesia", callback_data='indonesia'),
        types.InlineKeyboardButton("🇸🇳 Senegal", callback_data='senegal'),
        types.InlineKeyboardButton("⬅️ Back", callback_data='start')
    )
    await bot.edit_message_text("🌍 Select a country for WhatsApp:", 
                                chat_id=callback.message.chat.id, 
                                message_id=callback.message.message_id, 
                                reply_markup=markup)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

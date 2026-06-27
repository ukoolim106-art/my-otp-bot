import logging
from aiogram import Bot, Dispatcher, executor, types

# আপনার বটের টোকেন এবং অ্যাডমিন আইডি
API_TOKEN = '8077162426:AAHkbm0XHTQClncR-v4-pMpxuKcLli_dCzk'
ADMIN_ID = 8531139387

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# স্টার্ট কমান্ড
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("📱 Get Number", callback_data='get_number')
    item2 = types.InlineKeyboardButton("📊 Active Number", callback_data='active_number')
    item3 = types.InlineKeyboardButton("🏆 Leaderboard", callback_data='leaderboard')
    markup.add(item1, item2, item3)
    
    welcome_text = f"👋 WELCOME {message.from_user.full_name}!\nTHIS IS [SOJIB NUMBER BOT].\n\n📌 PLEASE SELECT A BUTTON BELOW:"
    await message.answer(welcome_text, reply_markup=markup)

# অ্যাডমিন প্যানেল কমান্ড
@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("👑 **Admin Panel:**\nস্বাগতম বস! আপনি এখন বটের কন্ট্রোল প্যানেলে আছেন।", parse_mode="Markdown")
    else:
        await message.answer("❌ দুঃখিত, আপনি এই কমান্ডটি ব্যবহার করার অনুমতি নেই।")

# বাটন হ্যান্ডলার
@dp.callback_query_handler(lambda c: c.data == 'get_number')
async def process_get_number(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "🌍 Select a country for WhatsApp:")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

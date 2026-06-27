from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# আপনার দেওয়া কনফিগারেশন
API_TOKEN = '8077162426:AAHkbm0XHTQClncR-v4-pMpxuKcLli_dCzk'
ADMIN_ID = 8531139387

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# স্টার্ট কমান্ড এবং মেনু
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # ইউজারকে মেনু দেখানো
    markup = InlineKeyboardMarkup(row_width=2)
    item1 = InlineKeyboardButton("📱 Get Number", callback_data='get_number')
    item2 = InlineKeyboardButton("📊 Active Number", callback_data='active_number')
    item3 = InlineKeyboardButton("🏆 Leaderboard", callback_data='leaderboard')
    
    markup.add(item1, item2, item3)
    
    welcome_text = (f"👋 WELCOME {message.from_user.full_name}!\n"
                    "THIS IS [SOJIB NUMBER BOT].\n\n"
                    "📌 PLEASE SELECT A BUTTON BELOW:")
    
    await message.answer(welcome_text, reply_markup=markup)

# বাটন হ্যান্ডলার
@dp.callback_query_handler(lambda c: c.data == 'get_number')
async def get_number(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "🌍 Select a country for WhatsApp:")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

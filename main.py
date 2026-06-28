import logging
import json
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '8077162426:AAHkbm0XHTQClncR-v4-pMpxuKcLli_dCzk'
ADMIN_ID = 8531139387

# নম্বরগুলো জমা রাখার ফাইল
DATA_FILE = 'numbers.json'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# নম্বর যোগ করার ফাংশন
def save_number(country, number):
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except:
        data = {}
    
    if country not in data:
        data[country] = []
    data[country].append(number)
    
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# অ্যাডমিন প্যানেল আপডেট
@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("➕ Add Number", callback_data='adm_add'),
            types.InlineKeyboardButton("📊 View Numbers", callback_data='adm_view')
        )
        await message.answer("👑 **Admin Panel**", reply_markup=markup)

# নম্বর যোগ করার লজিক (উদাহরণ হিসেবে)
@dp.callback_query_handler(lambda c: c.data == 'adm_add')
async def add_number_instr(callback: types.CallbackQuery):
    await callback.message.answer("নম্বর যোগ করতে এভাবে লিখুন:\n/add [দেশ] [নম্বর]\nযেমন: /add Indonesia +6281234567")

@dp.message_handler(commands=['add'])
async def add_number(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        parts = message.text.split()
        if len(parts) >= 3:
            country = parts[1]
            number = parts[2]
            save_number(country, number)
            await message.answer(f"✅ সফলভাবে {country} এর জন্য নম্বরটি সেভ হয়েছে: {number}")
        else:
            await message.answer("❌ সঠিক ফরমেট: /add [দেশ] [নম্বর]")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

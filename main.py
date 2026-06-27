import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8077162426:AAHjtB_wOsHfY573O238gTnSE_fySDYtC6w"
ADMIN_ID = 8531139387

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# কান্ট্রি ডিটেকশন লজিক
def get_country_info(number):
    if number.startswith("+880"): return "🇧🇩 Bangladesh", "BD"
    elif number.startswith("+91"): return "🇮🇳 India", "IN"
    elif number.startswith("+1"): return "🇺🇸 USA/Canada", "US"
    elif number.startswith("+44"): return "🇬🇧 UK", "UK"
    elif number.startswith("+62"): return "🇮🇩 Indonesia", "ID"
    elif number.startswith("+92"): return "🇵🇰 Pakistan", "PK"
    return "🌐 Global", "XX"

# ডাটা স্টোরেজ
available_numbers = {}

# স্টার্ট মেনু
def main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🌐 𝙂𝙀𝙏 𝙉𝙀𝙒 𝙉𝙐𝙈𝘽𝙀𝙍 ✨")],
        [KeyboardButton(text="👤 𝙐𝙎𝙀𝙍 𝙋𝙍𝙊𝙁𝙄𝙇𝙀 🛡️")]
    ], resize_keyboard=True)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("🔥 **SUPER FAST OTP BOT** 🔥", reply_markup=main_menu())

# ফাইল আপলোড হ্যান্ডলার (অ্যাডমিন)
@dp.message(F.document)
async def handle_file(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        file_path = "numbers.txt"
        await bot.download(message.document, destination=file_path)
        
        with open(file_path, "r") as f:
            lines = f.readlines()
        
        stats = {}
        for line in lines:
            num = line.strip()
            country, _ = get_country_info(num)
            if country not in stats: stats[country] = []
            stats[country].append(num)
        
        global available_numbers
        available_numbers = stats
        
        report = "✅ ফাইল আপডেট হয়েছে!\n\n"
        for c, n in stats.items():
            report += f"{c}: {len(n)} টি নাম্বার\n"
        await message.answer(report)

# গেট নাম্বার মেনু
@dp.message(F.text == "🌐 𝙂𝙀𝙏 𝙉𝙀𝙒 𝙉𝙐𝙈𝘽𝙀𝙍 ✨")
async def get_number(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇧🇩 Bangladesh", callback_data="get_BD")],
        [InlineKeyboardButton(text="🇮🇳 India", callback_data="get_IN")]
    ])
    await message.answer("সার্ভিস বেছে নিন:", reply_markup=markup)

@dp.callback_query(F.data.startswith("get_"))
async def send_number(call: types.CallbackQuery):
    await call.message.answer("💳 পেমেন্ট করতে অ্যাডমিনের সাথে যোগাযোগ করুন।")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

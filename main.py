import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# আপনার দেওয়া কনফিগারেশন
BOT_TOKEN = "8077162426:AAHjtB_wOsHfY573O238gTnSE_fySDYtC6w"
ADMIN_ID = 8531139387

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ডাটাবেস স্টোরেজ
available_numbers = {"BD": [], "IN": [], "US": [], "UK": [], "ID": [], "PK": []}

def get_country_code(number):
    if number.startswith("+880"): return "BD"
    elif number.startswith("+91"): return "IN"
    elif number.startswith("+1"): return "US"
    elif number.startswith("+44"): return "UK"
    elif number.startswith("+62"): return "ID"
    elif number.startswith("+92"): return "PK"
    return None

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🌐 𝙂𝙀𝙏 𝙉𝙀𝙒 𝙉𝙐𝙈𝘽𝙀𝙍 ✨")]], resize_keyboard=True)
    await message.answer("🔥 *WELCOME TO OTP BOT*\n\nনিচের বাটন থেকে আপনার নাম্বার নিন:", reply_markup=kb, parse_mode="Markdown")

@dp.message(F.document)
async def handle_file(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = "numbers.txt"
    await bot.download_file(file.file_path, file_path)
    
    new_data = {"BD": [], "IN": [], "US": [], "UK": [], "ID": [], "PK": []}
    count = 0
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            num = line.strip()
            if not num: continue
            code = get_country_code(num)
            if code and code in new_data:
                new_data[code].append(num)
                count += 1
    
    global available_numbers
    available_numbers = new_data
    
    await message.answer(f"✅ সাকসেসফুল! মোট {count} টি নাম্বার আপডেট হয়েছে।\n\n"
                         f"🇧🇩 BD: {len(available_numbers['BD'])}\n"
                         f"🇮🇳 IN: {len(available_numbers['IN'])}\n"
                         f"🇺🇸 US: {len(available_numbers['US'])}\n"
                         f"🇬🇧 UK: {len(available_numbers['UK'])}\n"
                         f"🇮🇩 ID: {len(available_numbers['ID'])}\n"
                         f"🇵🇰 PK: {len(available_numbers['PK'])}")

@dp.message(F.text == "🌐 𝙂𝙀𝙏 𝙉𝙀𝙒 𝙉𝙐𝙈𝘽𝙀𝙍 ✨")
async def show_countries(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇧🇩 Bangladesh", callback_data="get_BD"), InlineKeyboardButton(text="🇮🇳 India", callback_data="get_IN")],
        [InlineKeyboardButton(text="🇺🇸 USA", callback_data="get_US"), InlineKeyboardButton(text="🇬🇧 UK", callback_data="get_UK")],
        [InlineKeyboardButton(text="🇮🇩 Indonesia", callback_data="get_ID"), InlineKeyboardButton(text="🇵🇰 Pakistan", callback_data="get_PK")]
    ])
    await message.answer("দেশ সিলেক্ট করুন:", reply_markup=markup)

@dp.callback_query(F.data.startswith("get_"))
async def send_number(call: types.CallbackQuery):
    code = call.data.split("_")[1]
    if available_numbers.get(code) and len(available_numbers[code]) > 0:
        number = available_numbers[code].pop(0)
        await call.message.answer(f"✅ আপনার নাম্বার: `{number}`")
        await call.answer("নাম্বার দেওয়া হয়েছে!")
    else:
        await call.answer("❌ দুঃখিত, এই দেশের নাম্বার শেষ!", show_alert=True)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

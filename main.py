import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# আপনার টোকেন এবং অ্যাডমিন আইডি
BOT_TOKEN = "8077162426:AAHjtB_wOsHfY573O238gTnSE_fySDYtC6w"
ADMIN_ID = 8531139387

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# মেমোরিতে নাম্বার জমা রাখার জায়গা
available_numbers = {"BD": [], "IN": [], "US": []}

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🌐 𝙂𝙀𝙏 𝙉𝙀𝙒 𝙉𝙐𝙈𝘽𝙀𝙍 ✨")]], resize_keyboard=True)
    await message.answer("🔥 *WELCOME TO OTP BOT*\n\nনিচের বাটন থেকে নাম্বার নিন:", reply_markup=kb, parse_mode="Markdown")

# অ্যাডমিন প্যানেল: ফাইল আপলোড করলেই নাম্বার অটো সেট হয়ে যাবে
@dp.message(F.document)
async def handle_file(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        file = await bot.get_file(message.document.file_id)
        file_path = "numbers.txt"
        await bot.download_file(file.file_path, file_path)
        
        with open(file_path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
        
        # নতুন ডাটা লোড করা
        global available_numbers
        available_numbers = {"BD": [], "IN": [], "US": []}
        
        for num in lines:
            if num.startswith("+880"): available_numbers["BD"].append(num)
            elif num.startswith("+91"): available_numbers["IN"].append(num)
            elif num.startswith("+1"): available_numbers["US"].append(num)
            
        await message.answer(f"✅ সাকসেসফুল! ডাটাবেস আপডেট হয়েছে:\n\n🇧🇩 BD: {len(available_numbers['BD'])}\n🇮🇳 IN: {len(available_numbers['IN'])}\n🇺🇸 US: {len(available_numbers['US'])}")

# ইউজার মেনু
@dp.message(F.text == "🌐 𝙂𝙀𝙏 𝙉𝙀𝙒 𝙉𝙐𝙈𝘽𝙀𝙍 ✨")
async def show_countries(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇧🇩 Bangladesh", callback_data="get_BD")],
        [InlineKeyboardButton(text="🇮🇳 India", callback_data="get_IN")]
    ])
    await message.answer("সার্ভিস বেছে নিন:", reply_markup=markup)

# নাম্বার সেন্ড লজিক
@dp.callback_query(F.data.startswith("get_"))
async def send_number(call: types.CallbackQuery):
    code = call.data.split("_")[1]
    if available_numbers.get(code) and len(available_numbers[code]) > 0:
        number = available_numbers[code].pop(0) # ফাইল থেকে নাম্বারটি তুলে নিচ্ছে
        await call.message.answer(f"✅ আপনার নাম্বার: `{number}`")
        await call.answer("নাম্বার দেওয়া হয়েছে!")
    else:
        await call.answer("❌ দুঃখিত, এই দেশের নাম্বার শেষ!", show_alert=True)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import logging
import asyncio
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
    return "🌐 Global", "XX"

# ডাটা স্টোরেজ
available_numbers = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🌐 𝙂𝙀𝙏 𝙉𝙀𝙒 𝙉𝙐𝙈𝘽𝙀𝙍 ✨")]
    ], resize_keyboard=True)
    await message.answer("🔥 *SUPER FAST OTP BOT*\n\nনিচে থেকে নাম্বার নিন:", reply_markup=kb, parse_mode="Markdown")

@dp.message(F.document)
async def handle_file(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        file_path = "numbers.txt"
        await bot.download(message.document, destination=file_path)
        with open(file_path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
        
        global available_numbers
        available_numbers = {"BD": [], "IN": [], "US": []}
        for num in lines:
            _, code = get_country_info(num)
            if code in available_numbers: available_numbers[code].append(num)
        
        await message.answer("✅ ফাইল আপডেট হয়েছে! নাম্বার রেডি।")

@dp.message(F.text == "🌐 𝙂𝙀𝙏 𝙉𝙀𝙒 𝙉𝙐𝙈𝘽𝙀𝙍 ✨")
async def show_countries(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇧🇩 Bangladesh", callback_data="get_BD")],
        [InlineKeyboardButton(text="🇮🇳 India", callback_data="get_IN")]
    ])
    await message.answer("দেশ সিলেক্ট করুন:", reply_markup=markup)

@dp.callback_query(F.data.startswith("get_"))
async def send_number(call: types.CallbackQuery):
    code = call.data.split("_")[1]
    if available_numbers.get(code) and len(available_numbers[code]) > 0:
        number = available_numbers[code].pop(0) # ফাইল থেকে নাম্বারটি তুলে নিচ্ছে
        await call.message.answer(f"✅ আপনার নাম্বার: `{number}`")
    else:
        await call.message.answer("❌ দুঃখিত, এই দেশের কোনো নাম্বার অবশিষ্ট নেই।")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# আপনার টোকেন বসান
BOT_TOKEN = "8077162426:AAHjtB_wOsHfY573O238gTnSE_fySDYtC6w" 
ADMIN_ID = 8531139387

# ডাটাবেজ বা ডিকশনারি (সার্ভিস এবং এপিআই কী স্টোর করার জন্য)
services = {"WhatsApp": "NOT_SET", "Telegram": "NOT_SET", "Facebook": "NOT_SET", "Instagram": "NOT_SET"}

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# মেনু জেনারেটর (ডাইনামিক)
def get_main_menu():
    kb = []
    row = []
    for s in services.keys():
        row.append(KeyboardButton(text=f"🔥 {s} 𝘾𝙊𝘿𝙀 🔥"))
        if len(row) == 2:
            kb.append(row); row = []
    kb.append([KeyboardButton(text="🌐 𝙂𝙀𝙏 𝙉𝙀𝙒 𝙉𝙐𝙈𝘽𝙀𝙍 ✨"), KeyboardButton(text="👤 𝙐𝙎𝙀𝙍 𝙋𝙍𝙊𝙁𝙄𝙇𝙀 🛡️")])
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("🔥 **SUPER FAST OTP** 🔥\nসার্ভিস সিলেক্ট করুন:", reply_markup=get_main_menu())

# অ্যাডমিন প্যানেল (সার্ভিস ও কী সেট করার জন্য)
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        text = "👑 **অ্যাডমিন প্যানেল**\n\nসার্ভিস কী সেট করতে লিখুন:\n`/set সার্ভিস নাম কী`\n\nউদাহরণ:\n`/set WhatsApp 12345ABC`"
        await message.answer(text, parse_mode="Markdown")

@dp.message(Command("set"))
async def set_service(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        args = message.text.split(maxsplit=2)
        if len(args) == 3:
            service, key = args[1], args[2]
            services[service] = key
            await message.answer(f"✅ {service} এর কী আপডেট হয়েছে!")
        else:
            await message.answer("❌ ভুল ফরমেট। লিখুন: /set সার্ভিস কী")

# ইউজার ক্লিক করলে কী দেখাবে
@dp.message(F.text.contains("𝘾𝙊𝘿𝙀"))
async def handle_service(message: types.Message):
    service = message.text.split(" ")[1] # সার্ভিসের নাম বের করা
    key = services.get(service, "NOT_SET")
    await message.answer(f"✅ আপনি {service} সিলেক্ট করেছেন!\n🔑 অ্যাক্টিভ কী: `{key}`")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

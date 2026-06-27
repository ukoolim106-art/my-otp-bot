import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# আপনার দেওয়া কনফিগারেশন সেট করা হয়েছে
BOT_TOKEN = "8077162426:AAHjtB_wOsHfY573O238gTnSE_fySDYtC6w"
ADMIN_ID = 8531139387

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
users_db = set()

# ১. মেইন মেনু ডিজাইন
def user_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌐 𝙂𝙀𝙏 𝙉𝙀𝙒 𝙉𝙐𝙈𝘽𝙀𝙍 ✨")],
            [KeyboardButton(text="👤 𝙐𝙎𝙀𝙍 𝙋𝙍𝙊𝙁𝙄𝙇𝙀 🛡️")]
        ],
        resize_keyboard=True
    )

# ২. স্টার্ট কমান্ড
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    users_db.add(message.from_user.id)
    text = "🔥 **𝙎𝙐𝙋𝙀𝙍 𝙁𝘼𝙎𝙏 𝙊𝙏𝙋 𝘽𝙊𝙏** 🔥\n\nস্বাগতম! নিচে থেকে সার্ভিস বেছে নিন।"
    await message.answer(text, reply_markup=user_main_menu(), parse_mode="Markdown")

# ৩. গেট নিউ নাম্বারে ক্লিক করলে সার্ভিস মেনু
@dp.message(F.text == "🌐 𝙂𝙀𝙏 𝙉𝙀𝙒 𝙉𝙐𝙈𝘽𝙀𝙍 ✨")
async def show_service_menu(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 WhatsApp", callback_data="buy_whatsapp")],
        [InlineKeyboardButton(text="🚀 Telegram", callback_data="buy_telegram")],
        [InlineKeyboardButton(text="💎 Facebook", callback_data="buy_facebook")],
        [InlineKeyboardButton(text="⚡ Instagram", callback_data="buy_instagram")]
    ])
    await message.answer("✨ *আপনার প্রয়োজনীয় সার্ভিসটি সিলেক্ট করুন:*", reply_markup=markup, parse_mode="Markdown")

# ৪. সার্ভিস সিলেক্ট করার পর রেসপন্স
@dp.callback_query(F.data.startswith("buy_"))
async def process_buy(callback: types.CallbackQuery):
    service = callback.data.split("_")[1].upper()
    await callback.message.answer(f"✅ আপনি *{service}* সিলেক্ট করেছেন!\n\n💳 পেমেন্ট কনফার্ম করতে অ্যাডমিনের সাথে যোগাযোগ করুন।")
    await callback.answer()

# ৫. প্রোফাইল চেক
@dp.message(F.text == "👤 𝙐𝙎𝙀𝙍 𝙋𝙍𝙊𝙁𝙄𝙇𝙀 🛡️")
async def profile_cmd(message: types.Message):
    await message.answer(f"👤 আপনার আইডি: `{message.from_user.id}`\n🛡️ স্ট্যাটাস: অ্যাক্টিভ")

# ৬. অ্যাডমিন প্যানেল
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📊 STATS", callback_data="stats"), InlineKeyboardButton(text="📢 BROADCAST", callback_data="bc")]
        ])
        await message.answer("👑 **অ্যাডমিন কন্ট্রোল প্যানেল**", reply_markup=kb)

@dp.callback_query(F.data == "stats")
async def send_stats(call: types.CallbackQuery):
    await call.message.answer(f"📈 মোট ইউজার: {len(users_db)}")

@dp.callback_query(F.data == "bc")
async def ask_bc(call: types.CallbackQuery):
    await call.message.answer("📩 মেসেজটি লিখুন (যেমন: /send হ্যালো সবাইকে)")

@dp.message(Command("send"))
async def broadcast(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        text = message.text.replace("/send", "").strip()
        for uid in users_db:
            try: await bot.send_message(uid, text)
            except: continue
        await message.answer("✅ মেসেজ পাঠানো হয়েছে।")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

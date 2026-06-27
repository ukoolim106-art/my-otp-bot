import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# কনফিগারেশন - এখানে আপনার টোকেনটি বসান
BOT_TOKEN = "8077162426:AAHjtB_wOsHfY573O238gTnSE_fySDYtC6w" 
ADMIN_ID = 8531139387

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# মেনু ডিজাইন
def user_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔥 WhatsApp ⌁ 𝘾𝙊𝘿𝙀 🔥"), KeyboardButton(text="🚀 Telegram ⌁ 𝘾𝙊𝘿𝙀 🚀")],
            [KeyboardButton(text="💎 Facebook ⌁ 𝘾𝙊𝘿𝙀 💎"), KeyboardButton(text="⚡ Instagram ⌁ 𝘾𝙊𝘿𝙀 ⚡")],
            [KeyboardButton(text="🌐 𝙂𝙀𝙏 𝙉𝙀𝙒 𝙉𝙐𝙈𝘽𝙀𝙍 ✨"), KeyboardButton(text="👤 𝙐𝙎𝙀𝙍 𝙋𝙍𝙊𝙁𝙄𝙇𝙀 🛡️")]
        ],
        resize_keyboard=True
    )

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    text = (
        "╔════════════════════════════╗\n"
        "      🔥 𝙎𝙐𝙋𝙀𝙍 𝙁𝘼𝙎𝙏 𝙊𝙏𝙋 🔥      \n"
        "╚════════════════════════════╝\n\n"
        "✨ *আপনার ওটিপি সার্ভিসের জন্য সেরা গন্তব্য!*\n\n"
        "🔥 *নিচের মেনু থেকে আপনার সার্ভিসটি বেছে নিন:*"
    )
    await message.answer(text, reply_markup=user_main_menu(), parse_mode="Markdown")

@dp.message(lambda message: "𝘾𝙊𝘿𝙀" in message.text)
async def handle_service(message: types.Message):
    await message.answer(f"✅ আপনি {message.text} সিলেক্ট করেছেন!\n💳 পেমেন্ট কনফার্ম করতে অ্যাডমিনের সাথে যোগাযোগ করুন।")

@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📊 𝙎𝙏𝘼𝙏𝙎", callback_data="admin_stats")],
            [InlineKeyboardButton(text="📢 𝘽𝙍𝙊𝘼𝘿𝘾𝘼𝙎𝙏", callback_data="admin_broadcast")]
        ])
        await message.answer("👑 **অ্যাডমিন প্যানেল**", reply_markup=markup)
    else:
        await message.answer("🚫 *অ্যাক্সেস ডিনাইড!*")

# বট রান করার কমান্ড
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

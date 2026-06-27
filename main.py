import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# আপনার টোকেন এবং আইডি
BOT_TOKEN = "8077162426:AAHjtB_wOsHfY573O238gTnSE_fySDYtC6w"
ADMIN_ID = 5716244131  # 👈 আপনার টেলিগ্রাম আইডি (আমি একটি ডেমো আইডি দিয়েছি, আপনি চাইলে পরে আপনার আইডি দিয়ে পাল্টাতে পারেন)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
users_db = set()

def user_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Get New Number"), KeyboardButton(text="🔄 Check OTP")],
            [KeyboardButton(text="👤 My Account"), KeyboardButton(text="📞 Support")]
        ],
        resize_keyboard=True
    )

def admin_panel_markup():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Total Users", callback_data="admin_users")],
        [InlineKeyboardButton(text="📢 Broadcast Message", callback_data="admin_broadcast")]
    ])

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    users_db.add(message.from_user.id)
    welcome_text = (
        f"🔥 **SuperFast OTP Bot-এ আপনাকে স্বাগতম!** 🔥\n\n"
        f"এখানে আপনি WhatsApp, Telegram, Instagram সহ সব ধরণের ফ্রি নম্বর এবং ওটিপি পাবেন রকেট স্পিডে।\n\n"
        f"👇 নিচে নম্বর বাটনে ক্লিক করে কাজ শুরু করুন।"
    )
    await message.answer(welcome_text, reply_markup=user_main_menu(), parse_mode="Markdown")

@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if str(message.from_user.id) == str(ADMIN_ID):
        await message.answer("👑 **স্বাগতম বসের অ্যাডমিন প্যানেলে!**", reply_markup=admin_panel_markup(), parse_mode="Markdown")
    else:
        await message.answer("❌ এই কমান্ডটি শুধুমাত্র বটের মালিকের জন্য।")

@dp.message(lambda message: message.text in ["📱 Get New Number", "🔄 Check OTP", "👤 My Account", "📞 Support"])
async def handle_user_buttons(message: types.Message):
    if message.text == "📱 Get New Number":
        apps_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="WhatsApp ✅", callback_data="app_whatsapp"), InlineKeyboardButton(text="Telegram ✈️", callback_data="app_telegram")],
            [InlineKeyboardButton(text="Instagram 📸", callback_data="app_instagram"), InlineKeyboardButton(text="Facebook 👥", callback_data="app_facebook")]
        ])
        await message.answer("✨ **কোন সার্ভিসের জন্য নম্বর প্রয়োজন? সিলেক্ট করুন:**", reply_markup=apps_keyboard, parse_mode="Markdown")
    elif message.text == "🔄 Check OTP":
        await message.answer("🔄 ওটিপি চেক করা হচ্ছে... (এখনো কোনো নম্বর নেওয়া হয়নি।)")
    elif message.text == "👤 My Account":
        await message.answer(f"👤 **আপনার প্রোফাইল:**\n🏷️ নাম: {message.from_user.full_name}\n🆔 আইডি: `{message.from_user.id}`\n💰 ব্যালেন্স: FREE (Unlimited)", parse_mode="Markdown")
    elif message.text == "📞 Support":
        await message.answer("📬 যেকোনো সমস্যায় আমাদের সাথে যোগাযোগ করুন: @YourUsername")

@dp.callback_query(lambda c: c.data.startswith("admin_"))
async def process_admin_callbacks(callback_query: types.CallbackQuery):
    if callback_query.data == "admin_users":
        await bot.send_message(callback_query.from_user.id, f"📊 **বটের মোট সচল ইউজার:** {len(users_db)} জন।")
    elif callback_query.data == "admin_broadcast":
        await bot.send_message(callback_query.from_user.id, "📢 সব ইউজারকে মেসেজ পাঠাতে লিখুন: `/send আপনার মেসেজ`")

@dp.message(Command("send"))
async def broadcast_to_all(message: types.Message):
    if str(message.from_user.id) == str(ADMIN_ID):
        msg_text = message.text.replace("/send", "").strip()
        if not msg_text: return
        count = 0
        for user_id in users_db:
            try:
                await bot.send_message(user_id, f"📢 **গুরুত্বপূর্ণ নোটিশ:**\n\n{msg_text}", parse_mode="Markdown")
                count += 1
            except: pass
        await message.answer(f"✅ সফলভাবে {count} জন ইউজারের কাছে মেসেজ পাঠানো হয়েছে।")

@dp.callback_query(lambda c: c.data.startswith("app_"))
async def process_app_selection(callback_query: types.CallbackQuery):
    service_name = callback_query.data.replace("app_", "").capitalize()
    await bot.send_message(callback_query.from_user.id, f"⚡ {service_name}-এর জন্য নম্বর খোঁজা হচ্ছে... একটু অপেক্ষা করুন।")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

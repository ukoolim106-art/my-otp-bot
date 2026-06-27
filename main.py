import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

# কনফিগারেশন
BOT_TOKEN = "8077162426:AAHjtB_wOsHfY573O238gTnSE_fySDYtC6w"
ADMIN_ID = 8531139387

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ডাটাবেস স্টোরেজ
db = {"BD": [], "IN": [], "US": [], "UK": [], "ID": [], "PK": []}

def get_code(num):
    if num.startswith("+880"): return "BD"
    elif num.startswith("+91"): return "IN"
    elif num.startswith("+1"): return "US"
    elif num.startswith("+44"): return "UK"
    elif num.startswith("+62"): return "ID"
    elif num.startswith("+92"): return "PK"
    return None

# --- অ্যাডমিন কমান্ডস ---
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 বর্তমান স্ট্যাটাস", callback_data="admin_stats")],
        [InlineKeyboardButton(text="🔄 ডাটা রিসেট (ফাঁকা)", callback_data="admin_reset")]
    ])
    await message.answer("🛠 **অ্যাডমিন কন্ট্রোল প্যানেল**", reply_markup=kb)

@dp.callback_query(F.data.startswith("admin_"))
async def admin_actions(call: types.CallbackQuery):
    if call.data == "admin_stats":
        report = "📊 **ডাটাবেস স্ট্যাটাস:**\n"
        for k, v in db.items(): report += f"{k}: {len(v)} টি\n"
        await call.message.answer(report)
    elif call.data == "admin_reset":
        for k in db: db[k] = []
        await call.message.answer("✅ ডাটাবেস রিসেট করা হয়েছে।")
    await call.answer()

# --- ফাইল আপলোড হ্যান্ডলার ---
@dp.message(F.document)
async def handle_file(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    
    file = await bot.get_file(message.document.file_id)
    await bot.download_fileNormally I can help with things like this, but I don't seem to have access to that content. You can try again or ask me for something else.

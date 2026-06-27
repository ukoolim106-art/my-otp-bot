from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ১. গেট নিউ নাম্বারে ক্লিক করলে সার্ভিস মেনু দেখাবে
@dp.message(F.text == "🌐 𝙂𝙀𝙏 𝙉𝙀𝙒 𝙉𝙐𝙈𝘽𝙀𝙍 ✨")
async def show_service_menu(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔥 WhatsApp", callback_data="buy_whatsapp")],
        [InlineKeyboardButton(text="🚀 Telegram", callback_data="buy_telegram")],
        [InlineKeyboardButton(text="💎 Facebook", callback_data="buy_facebook")],
        [InlineKeyboardButton(text="⚡ Instagram", callback_data="buy_instagram")]
    ])
    await message.answer("✨ *সার্ভিস সিলেক্ট করুন:*", reply_markup=markup, parse_mode="Markdown")

# ২. ইউজার সার্ভিস সিলেক্ট করলে যা হবে
@dp.callback_query(F.data.startswith("buy_"))
async def process_buy(callback: types.CallbackQuery):
    service = callback.data.split("_")[1].upper()
    await callback.message.answer(f"✅ আপনি *{service}* সিলেক্ট করেছেন!\n\n💳 পেমেন্ট কনফার্ম করতে অ্যাডমিনের সাথে যোগাযোগ করুন।")
    await callback.answer()

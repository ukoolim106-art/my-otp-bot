import telebot
from telebot import types

# আপনার দেওয়া কনফিগারেশন
BOT_TOKEN = "8077162426:AAHjtB_wOsHfY573O238gTnSE_fySDYtC6w"
ADMIN_ID = 8531139387

bot = telebot.TeleBot(BOT_TOKEN)

# স্টার্ট কমান্ড
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🌐 𝙂𝙀𝙏 𝙉𝙀𝙒 𝙉𝙐𝙈𝘽𝙀𝙍 ✨"))
    bot.send_message(message.chat.id, "🔥 *WELCOME TO OTP BOT*\n\nআপনার কাজ শুরু করতে নিচের বাটনটি চাপুন:", 
                     reply_markup=markup, parse_mode="Markdown")

# এডমিন চেকিং ফাংশন
def is_admin(user_id):
    return user_id == ADMIN_ID

# বটের মূল কাজ বা বাটন হ্যান্ডলিং এখানে যোগ করুন
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text == "🌐 𝙂𝙀𝙏 𝙉𝙀𝙒 𝙉𝙐𝙈𝘽𝙀𝙍 ✨":
        bot.reply_to(message, "আপনি নতুন নাম্বার নেওয়ার অপশনে আছেন।")
    
    # এডমিন প্যানেল উদাহরণ
    if message.text == "/admin" and is_admin(message.chat.id):
        bot.reply_to(message, "স্বাগতম এডমিন! আপনি কন্ট্রোল প্যানেলে আছেন।")

print("🤖 বট সফলভাবে চালু হয়েছে!")
bot.infinity_polling()

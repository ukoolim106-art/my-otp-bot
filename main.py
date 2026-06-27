import telebot
from telebot import types
import sqlite3
import pyotp
import re
from datetime import datetime

# ==================== [ কনফিগারেশন ] ====================
BOT_TOKEN = "8077162426:AAHjtB_wOsHfY573O238gTnSE_fySDYtC6w"  
SUPER_ADMIN_ID = 8531139387                                  
# =======================================================

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# --- ডেটাবেজ সেটআপ ---
def init_db():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, balance REAL DEFAULT 0.0, otp_success INTEGER DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS admins (user_id INTEGER PRIMARY KEY, username TEXT)''')
    cursor.execute("INSERT OR IGNORE INTO admins (user_id, username) VALUES (?, ?)", (SUPER_ADMIN_ID, "Owner"))
    conn.commit()
    conn.close()

init_db()

# --- মেইন মেনু ---
def main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("📞 Go Number"), types.KeyboardButton("💸 Withdraw"), types.KeyboardButton("💰 Balance"))
    if user_id == SUPER_ADMIN_ID:
        markup.add(types.KeyboardButton("🎛️ Control Panel"))
    return markup

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.chat.id
    bot.send_message(user_id, "👋 স্বাগতম! আপনার বট এখন চালু আছে।", reply_markup=main_menu(user_id))

print("🤖 Bot is running...")
bot.infinity_polling()

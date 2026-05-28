import os
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ Bot Working 😈")

@bot.message_handler(func=lambda m: True)
def reply(message):
    bot.reply_to(message, f"Reply: {message.text}")

print("BOT STARTED")

bot.infinity_polling(
    skip_pending=True,
    none_stop=True,
    timeout=60,
    long_polling_timeout=60
)
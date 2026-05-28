import telebot
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):

    bot.reply_to(
        message,
        "✅ Bot Successfully Started 😈"
    )

@bot.message_handler(func=lambda message: True)
def reply(message):

    bot.reply_to(
        message,
        f"👀 Tumne bola:\n{message.text}"
    )

print("✅ Bot Started")

bot.infinity_polling()
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# ================= TOKEN =================
BOT_TOKEN = "8721070900:AAHLjGo_CuLQz6iNIHXKQhoYHxFZQd8Pj7k"

bot = telebot.TeleBot(BOT_TOKEN)

# ================= START =================
@bot.message_handler(commands=['start'])
def start(message):

    args = message.text.split()

    # Anonymous message receive
    if len(args) > 1:
        target_id = args[1]

        if str(message.from_user.id) == str(target_id):
            bot.reply_to(message, "❌ Khud ko message nahi bhej sakte")
            return

        msg = bot.send_message(
            message.chat.id,
            "✍️ Anonymous message bhejo:"
        )

        bot.register_next_step_handler(
            msg,
            send_anon,
            target_id
        )

        return

    # User ka personal link
    username = bot.get_me().username

    link = f"https://t.me/{username}?start={message.chat.id}"

    markup = types.InlineKeyboardMarkup()

    share_btn = types.InlineKeyboardButton(
        "📤 Share Link",
        url=f"https://t.me/share/url?url={link}"
    )

    markup.add(share_btn)

    text = f"""
🔥 Welcome {message.from_user.first_name}

📩 Your Anonymous Link:

{link}

Is link ko share karo aur anonymous messages pao 😈
"""

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=markup
    )

# ================= SEND ANON MESSAGE =================
def send_anon(message, target_id):

    try:
        text = f"""
📩 New Anonymous Message

{message.text}
"""

        bot.send_message(target_id, text)

        bot.reply_to(
            message,
            "✅ Anonymous message send ho gaya"
        )

    except Exception as e:
        bot.reply_to(
            message,
            f"❌ Error: {e}"
        )

# ================= KEEP ALIVE =================
app = Flask('')

@app.route('/')
def home():
    return "Bot Running Successfully"

def run():
    app.run(
        host='0.0.0.0',
        port=8080
    )

def keep_alive():
    t = Thread(target=run)
    t.start()

# ================= RUN BOT =================
print("✅ Bot Started Successfully")

keep_alive()

bot.infinity_polling(skip_pending=True)
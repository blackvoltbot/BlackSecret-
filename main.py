import telebot
import requests
import os
from flask import Flask
from threading import Thread

# ================= BOT =================

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])

# ================= AI FUNCTION =================

def ask_ai(question):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
        "Content-Type": "application/json"
    }

    data = {

        "model": "llama3-8b-8192",

        "messages": [

            {
                "role": "system",

                "content": """

You are a smart AI Teacher Bot.

Rules:
- Hindi me answer do
- English me bhi answer do
- Hinglish samjho
- User jis language me baat kare usi language me jawab do

Teach students from Class 1 to 8.

Subjects:
- Math
- Science
- English
- Hindi
- GK
- SST

Style:
- Fast reply
- Easy explanation
- Short answers
- Student friendly

"""
            },

            {
                "role": "user",
                "content": question
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    result = response.json()

    return result['choices'][0]['message']['content']

# ================= START =================

@bot.message_handler(commands=['start'])
def start(message):

    text = """

🤖 AI Teacher Bot

📚 Class 1 to 8 Study Help

Subjects:
✅ Math
✅ Science
✅ English
✅ Hindi
✅ GK
✅ SST

💬 Hindi + English + Hinglish Support

🧠 Koi bhi question pucho 😈

"""

    bot.reply_to(message, text)

# ================= HELP =================

@bot.message_handler(commands=['help'])
def help_command(message):

    text = """

📌 Commands

/start - Start Bot
/help - Commands
/about - About Bot

"""

    bot.reply_to(message, text)

# ================= ABOUT =================

@bot.message_handler(commands=['about'])
def about(message):

    bot.reply_to(
        message,
        "🤖 Smart AI Teacher Bot 😈"
    )

# ================= AI CHAT =================

@bot.message_handler(func=lambda message: True)
def ai_chat(message):

    try:

        thinking = bot.reply_to(
            message,
            "🤔 Soch raha hu..."
        )

        answer = ask_ai(message.text)

        bot.edit_message_text(
            answer,
            chat_id=message.chat.id,
            message_id=thinking.message_id
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
    return "AI Teacher Bot Running"

def run():

    app.run(
        host='0.0.0.0',
        port=8080
    )

def keep_alive():

    t = Thread(target=run)
    t.start()

# ================= RUN BOT =================

print("✅ AI Teacher Bot Started")

keep_alive()

bot.infinity_polling(skip_pending=True)
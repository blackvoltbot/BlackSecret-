import os
import telebot
import requests
from flask import Flask
from threading import Thread

# ================= TOKENS =================

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

# ================= FLASK =================

app = Flask('')

@app.route('/')
def home():
    return "Biology AI Bot Running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ================= AI FUNCTION =================

def ask_ai(question):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",

        "messages": [
            {
                "role": "system",
                "content": """
You are the world's best Biology AI Teacher.

Teach Class 11 and 12 NCERT Biology deeply.

Support:
- Hindi
- English
- Hinglish

Rules:
- Explain deeply and simply
- Give notes
- Give examples
- Give diagrams using text symbols
- Give NCERT style answers
- Explain chapterwise
- Explain line by line if user asks
- Answer all biology questions only

Topics:
- Cell
- DNA
- Genetics
- Evolution
- Human Physiology
- Plant Physiology
- Reproduction
- Biotechnology
- Ecology
- Biomolecules
- Respiration
- Photosynthesis
- Human Health
- Microbes
- Nervous System
- Digestion
- Breathing
- Circulation
- All NCERT Biology Chapters

If user asks for diagram:
Make clean text diagrams.

Always answer like a smart teacher.
"""
            },

            {
                "role": "user",
                "content": question
            }
        ],

        "temperature": 0.7,
        "max_tokens": 2000
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    result = response.json()

    return result["choices"][0]["message"]["content"]

# ================= COMMANDS =================

@bot.message_handler(commands=['start'])
def start(message):

    text = """
🧬 Biology AI Teacher Bot

✅ Ask Any Biology Question

Examples:
- DNA kya hota hai
- Cell diagram banao
- Photosynthesis explain karo
- Genetics notes do
- Respiration process

Languages:
✅ Hindi
✅ English
✅ Hinglish
"""

    bot.reply_to(message, text)

# ================= CHAT =================

@bot.message_handler(func=lambda message: True)
def biology_ai(message):

    try:

        bot.send_chat_action(
            message.chat.id,
            "typing"
        )

        answer = ask_ai(message.text)

        if len(answer) > 4000:
            answer = answer[:4000]

        bot.reply_to(
            message,
            answer
        )

    except Exception as e:

        bot.reply_to(
            message,
            f"❌ Error: {e}"
        )

# ================= RUN =================

print("✅ Biology AI Teacher Bot Started")

keep_alive()

bot.infinity_polling(skip_pending=True)
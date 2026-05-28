import telebot
import requests
import os

# ================= TOKENS =================

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# ================= BOT =================

bot = telebot.TeleBot(BOT_TOKEN)

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

Explain:
- Full NCERT Biology
- Definitions
- Diagrams
- Processes
- Examples
- Important Questions
- Board Preparation
- NEET Preparation
- PYQs
- Notes
- Tricks
- Mnemonics

Biology Topics:
- Cell Structure
- Biomolecules
- Human Physiology
- Plant Physiology
- Genetics
- Evolution
- Ecology
- Biotechnology
- Reproduction
- Human Health
- Microbes
- Biodiversity
- All Biology Chapters

Rules:
- Give detailed answers
- Explain step by step
- Use easy language
- Student friendly tone
- Make difficult topics easy
- If user asks for diagram:
  make clean text diagrams using ASCII symbols

Example diagram style:

Heart Diagram:

      AORTA
        |
   ----------
   |        |
 LEFT     RIGHT
 ATRIUM   ATRIUM
   |        |
 VENTRICLE VENTRICLE

If user asks non-biology questions:
Reply:
❌ Ye bot sirf Biology subject ke liye bana hai.

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

    return result["choices"][0]["message"]["content"]

# ================= START =================

@bot.message_handler(commands=['start'])
def start(message):

    text = """

🧬 Biology AI Teacher Bot

📚 Full NCERT Biology

🎯 NEET + Board Preparation

✅ Hindi Support
✅ English Support
✅ Hinglish Support
✅ Deep Explanation
✅ Diagram Support
✅ Important Questions
✅ Notes + Tricks

💬 Ask Any Biology Question 😈

Examples:
- DNA replication explain karo
- Heart diagram banao
- Mendel law kya hai?
- Photosynthesis process
- Human reproduction notes

"""

    bot.reply_to(message, text)

# ================= HELP =================

@bot.message_handler(commands=['help'])
def help_command(message):

    text = """

📌 Commands

/start - Start Bot
/help - Commands List

💬 Ask Any Biology Question

Examples:
- Cell diagram banao
- Ecology explain karo
- Biomolecules notes do
- Respiration process

"""

    bot.reply_to(message, text)

# ================= BIOLOGY AI CHAT =================

@bot.message_handler(func=lambda message: True)
def biology_ai(message):

    try:

        bot.send_chat_action(
            message.chat.id,
            "typing"
        )

        answer = ask_ai(message.text)

        # Telegram message limit protection
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

bot.infinity_polling()
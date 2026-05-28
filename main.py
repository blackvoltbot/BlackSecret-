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

    try:

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        SYSTEM_PROMPT = """

You are the world's best Biology AI Teacher.

Teach Class 11 and 12 NCERT Biology deeply.

Languages:
- Hindi
- English
- Hinglish

Reply in the same language the user uses.

Teach:
- Full NCERT Biology
- NEET Biology
- Board Biology
- Diagrams
- Notes
- PYQs
- Important Questions
- Tricks and Mnemonics

Topics:
- Cell
- Biomolecules
- Genetics
- Evolution
- Ecology
- Biotechnology
- Human Physiology
- Plant Physiology
- Reproduction
- Human Health
- Biodiversity
- All Biology Chapters

IMPORTANT:
If user asks for diagrams,
make neat ASCII diagrams.

Rules:
- Easy language
- Deep explanation
- Step by step teaching
- Student friendly

If user asks non-biology questions:
Reply:
❌ Ye bot sirf Biology subject ke liye bana hai.

"""

        data = {

            "model": "llama-3.1-8b-instant",

            "messages": [

                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
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

        if "choices" in result:

            return result["choices"][0]["message"]["content"]

        else:

            return f"❌ API Error:\n{result}"

    except Exception as e:

        return f"❌ Error:\n{e}"

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
✅ Diagram Support
✅ Deep Explanation

💬 Ask Any Biology Question 😈

Examples:
- DNA replication explain karo
- Heart diagram banao
- Mendel law kya hai?

"""

    bot.reply_to(message, text)

# ================= HELP =================

@bot.message_handler(commands=['help'])
def help_command(message):

    text = """

📌 Commands

/start - Start Bot
/help - Commands List

💬 Ask Biology Questions

"""

    bot.reply_to(message, text)

# ================= AI CHAT =================

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
            f"❌ Bot Error:\n{e}"
        )

# ================= RUN =================

print("✅ Biology AI Teacher Bot Started")

bot.infinity_polling(skip_pending=True)
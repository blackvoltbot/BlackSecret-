# =========================================
#        BLACK VOLT ANONYMOUS BOT
# =========================================

# INSTALL:
# pip install pyTelegramBotAPI

import telebot
import json
import os
import time

# =========================================
# CONFIG
# =========================================

TOKEN = "8721070900: AAHLjGo_CuLQz6iNIHXKQ
hoYHxFZQd8Pj7k"
ADMIN_CHAT_ID = 7492353753

bot = telebot.TeleBot(TOKEN)

USERS_FILE = "users.json"
REPLY_FILE = "reply_map.json"

# =========================================
# LOAD JSON
# =========================================

def load_json(file):

    if os.path.exists(file):

        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)

        except:
            return {}

    return {}

# =========================================
# SAVE JSON
# =========================================

def save_json(file, data):

    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# =========================================
# START
# =========================================

@bot.message_handler(commands=['start'])
def start(message):

    users = load_json(USERS_FILE)

    uid = str(message.chat.id)

    if uid not in users:

        users[uid] = {
            "name": message.chat.first_name or "Unknown",
            "username": message.chat.username or "NoUsername"
        }

        save_json(USERS_FILE, users)

    text = """
🔥 Welcome to Black Volt Anonymous Bot

📩 Yahan aap anonymous message bhej sakte ho.
🔒 Aapki identity hidden rahegi.
💬 Admin ka reply yahin aayega.

📸 Photos
🎥 Videos
📄 Files
🎤 Voice
😂 Stickers

✅ Sab supported hai.

👇 Ab message bhejo.
"""

    bot.reply_to(message, text)

# =========================================
# USERS COMMAND
# =========================================

@bot.message_handler(commands=['users'])
def users(message):

    if message.chat.id != ADMIN_CHAT_ID:
        return

    users = load_json(USERS_FILE)

    if not users:

        bot.reply_to(message, "❌ Koi user nahi.")
        return

    text = "📋 Registered Users\n\n"

    for uid, info in users.items():

        text += f"""
👤 {info['name']}
📛 @{info['username']}
🆔 {uid}

"""

    bot.reply_to(message, text)

# =========================================
# USER -> ADMIN
# =========================================

@bot.message_handler(
    func=lambda m: m.chat.id != ADMIN_CHAT_ID,
    content_types=[
        'text',
        'photo',
        'video',
        'document',
        'audio',
        'voice',
        'sticker'
    ]
)
def user_message(message):

    try:

        bot.reply_to(
            message,
            "✅ Message anonymously send ho gaya."
        )

        header = f"""
📨 NEW ANONYMOUS MESSAGE

👤 {message.chat.first_name}
🆔 {message.chat.id}
"""

        sent = None

        # TEXT
        if message.content_type == "text":

            sent = bot.send_message(
                ADMIN_CHAT_ID,
                f"{header}\n\n💬 {message.text}"
            )

        # PHOTO
        elif message.content_type == "photo":

            sent = bot.send_photo(
                ADMIN_CHAT_ID,
                message.photo[-1].file_id,
                caption=header
            )

        # VIDEO
        elif message.content_type == "video":

            sent = bot.send_video(
                ADMIN_CHAT_ID,
                message.video.file_id,
                caption=header
            )

        # DOCUMENT
        elif message.content_type == "document":

            sent = bot.send_document(
                ADMIN_CHAT_ID,
                message.document.file_id,
                caption=header
            )

        # AUDIO
        elif message.content_type == "audio":

            sent = bot.send_audio(
                ADMIN_CHAT_ID,
                message.audio.file_id
            )

            bot.send_message(ADMIN_CHAT_ID, header)

        # VOICE
        elif message.content_type == "voice":

            sent = bot.send_voice(
                ADMIN_CHAT_ID,
                message.voice.file_id
            )

            bot.send_message(ADMIN_CHAT_ID, header)

        # STICKER
        elif message.content_type == "sticker":

            sent = bot.send_sticker(
                ADMIN_CHAT_ID,
                message.sticker.file_id
            )

            bot.send_message(ADMIN_CHAT_ID, header)

        # SAVE REPLY MAP
        if sent:

            reply_map = load_json(REPLY_FILE)

            reply_map[str(sent.message_id)] = str(message.chat.id)

            save_json(REPLY_FILE, reply_map)

    except Exception as e:

        print(e)

# =========================================
# ADMIN REPLY
# =========================================

@bot.message_handler(
    func=lambda m:
    m.chat.id == ADMIN_CHAT_ID
    and m.reply_to_message is not None,
    content_types=[
        'text',
        'photo',
        'video',
        'document',
        'audio',
        'voice',
        'sticker'
    ]
)
def admin_reply(message):

    try:

        reply_map = load_json(REPLY_FILE)

        replied_id = str(message.reply_to_message.message_id)

        if replied_id not in reply_map:

            bot.reply_to(message, "❌ User not found.")
            return

        target_user = reply_map[replied_id]

        # TEXT
        if message.content_type == "text":

            bot.send_message(
                target_user,
                f"📩 Admin Reply\n\n{message.text}"
            )

        # PHOTO
        elif message.content_type == "photo":

            bot.send_photo(
                target_user,
                message.photo[-1].file_id,
                caption="📸 Admin sent a photo"
            )

        # VIDEO
        elif message.content_type == "video":

            bot.send_video(
                target_user,
                message.video.file_id,
                caption="🎥 Admin sent a video"
            )

        # DOCUMENT
        elif message.content_type == "document":

            bot.send_document(
                target_user,
                message.document.file_id,
                caption="📄 Admin sent a file"
            )

        # AUDIO
        elif message.content_type == "audio":

            bot.send_audio(
                target_user,
                message.audio.file_id
            )

        # VOICE
        elif message.content_type == "voice":

            bot.send_voice(
                target_user,
                message.voice.file_id
            )

        # STICKER
        elif message.content_type == "sticker":

            bot.send_sticker(
                target_user,
                message.sticker.file_id
            )

        bot.reply_to(message, "✅ Reply sent.")

    except Exception as e:

        print(e)

        bot.reply_to(message, "⚠️ Error.")

# =========================================
# ADMIN HELP
# =========================================

@bot.message_handler(func=lambda m: m.chat.id == ADMIN_CHAT_ID)
def admin_help(message):

    text = """
🛠 ADMIN PANEL

/users → User list

💬 Kisi bhi forwarded message par direct reply karo.
Reply automatically user tak pahunch jayega.
"""

    bot.reply_to(message, text)

# =========================================
# START BOT
# =========================================

print("🤖 Black Volt Bot Running...")

while True:

    try:

        bot.infinity_polling(
            timeout=20,
            long_polling_timeout=10
        )

    except Exception as e:

        print(f"⚠️ Error: {e}")

        time.sleep(5)

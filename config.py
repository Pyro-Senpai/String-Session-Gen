# (©)Pyro-Senpai

import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", "123456"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

START_MSG = "<b>💖 ʜᴇʏ {mention}! 🥀,</b>\n<b><blockquote>ɪ ᴄᴀɴ ʜᴇʟᴘ ʏᴏᴜ ɢᴇɴᴇʀᴀᴛᴇ sᴇᴄᴜʀᴇ ᴘʏʀᴏɢʀᴀᴍ ᴀɴᴅ ᴘʏʀᴏғᴏʀᴋ sᴛʀɪɴɢ sᴇssɪᴏɴs ғᴏʀ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛs sᴀғᴇʟʏ ᴀɴᴅ ᴇᴀsɪʟʏ.</blockquote></b>\n<b><blockquote>ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ: <a href='https://t.me/PyroSznpai'>Pyro Senpai</a></blockquote></b>"
START_PIC = "https://graph.org/file/e08200bae7bae43e9c89d-0c7c4b63a1de688a36.jpg"

ABOUT_TEXT = "<b><blockquote>🌀 ᴛʜɪs ɪs ᴀ sɪᴍᴘʟᴇ ᴘʏʀᴏɢʀᴀᴍ sᴛʀɪɴɢ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴏʀ ʙoᴛ.</blockquote></b>"
HELP_TEXT = "<b><blockquote>❓ ʜᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs:\n/start - sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n/generate - ɢᴇɴᴇʀᴀᴛᴇ ᴀ sᴛʀɪɴɢ sᴇssɪᴏɴ</blockquote></b>"

MESSAGE_EFFECT_ID = "5104841245755180586"
PORT = int(os.environ.get("PORT", "8080"))

# Database Configuration
DATABASE_URI = os.environ.get("DATABASE_URI", "")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "session")

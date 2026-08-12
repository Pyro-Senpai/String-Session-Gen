# (©)Pyro-Senpai

import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", "123456"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

START_MSG = "<b>💖 ʜᴇʏ {mention}! 🥀,</b>\n<b><blockquote>ɪ ᴄᴀɴ ʜᴇʟᴘ ʏᴏᴜ ɢᴇɴᴇʀᴀᴛᴇ sᴇᴄᴜʀᴇ ᴘʏʀᴏɢʀᴀᴍ ᴀɴᴅ ᴘʏʀᴏғᴏʀᴋ sᴛʀɪɴɢ sᴇssɪᴏɴs ғᴏʀ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛs sᴀғᴇʟʏ ᴀɴᴅ ᴇᴀsɪʟʏ.</blockquote></b>"
START_PIC = "https://telegra.ph/file/aad055c98c566adfb7dcd-b42f72ff4d1de29e86.jpg"

ABOUT_TEXT = "<b><blockquote>🌀 ᴛʜɪs ɪs ᴀ sɪᴍᴘʟᴇ ᴘʏʀᴏɢʀᴀᴍ sᴛʀɪɴɢ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴏʀ boᴛ.</blockquote></b>"
HELP_TEXT = "<b><blockquote>❓ ʜᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs:\n/start - sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n/string - ɢᴇɴᴇʀᴀᴛᴇ ᴀ sᴛʀɪɴɢ sᴇssɪᴏɴ<blockquote></b>"

MESSAGE_EFFECT_ID = "5104841245755180586"
PORT = int(os.environ.get("PORT", "8080"))

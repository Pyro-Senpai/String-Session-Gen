# (©)Pyro-Senpai

import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", "123456"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

START_MSG = "👋 Hello! Send /generate to create a Pyrofog String Session."
START_PIC = ""

ABOUT_TEXT = "ℹ️ This is a simple session generator bot built with Pyrofog and Pyromode."
HELP_TEXT = "❓ Here are the available commands:\n/start - Start the bot\n/generate - Generate a session"

MESSAGE_EFFECT_ID = "5104841245755180586"
PORT = int(os.environ.get("PORT", "8080"))

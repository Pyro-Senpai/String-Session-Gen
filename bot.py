# (©)Pyro-Senpai

from pyrogram import Client
import config

app = Client(
    "SessionGeneratorBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="plugins")
)

if __name__ == "__main__":
    print("Bot is starting...")
    app.run(port=config.PORT)

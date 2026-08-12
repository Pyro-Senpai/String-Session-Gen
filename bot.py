# (©)Pyro-Senpai

from aiohttp import web
from pyrofork import Client
import config
import asyncio

# Aiohttp web server for Koyeb health check
async def handle(request):
    return web.Response(text="Bot is running!")

app_web = web.Application()
app_web.add_routes([web.get("/", handle)])

async class Application:
    def __init__(self):
        self.bot = Client(
            "SessionGeneratorBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            plugins=dict(root="plugins")
        )

    async def start(self):
        await self.bot.start()
        print("Bot is Started.")
        
        # Start aiohttp web server
        runner = web.AppRunner(app_web)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", config.PORT)
        await site.start()
        print(f"Web server started on port {config.PORT}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = Application()
    loop.run_until_complete(app.start())
    asyncio.get_event_loop().run_forever()
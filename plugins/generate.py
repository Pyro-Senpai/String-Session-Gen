# (©)Pyro-Senpai

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import SessionPasswordNeeded

@Client.on_message(filters.command("string") & filters.private)
async def generate_session(client: Client, message: Message):
    chat_id = message.chat.id

    try:
        # Ask for API ID
        api_id_msg = await client.ask(chat_id, "🆔 Please send your API ID:", timeout=300)
        API_ID = int(api_id_msg.text.strip())
    except asyncio.TimeoutError:
        await message.reply("⏳ Time out. Please try again.")
        return
    except ValueError:
        await message.reply("❌ Invalid API ID. It must be a number. Please try again.")
        return

    try:
        # Ask for API Hash
        api_hash_msg = await client.ask(chat_id, "🔐 Please send your API HASH:", timeout=300)
        API_HASH = api_hash_msg.text.strip()
    except asyncio.TimeoutError:
        await message.reply("⏳ Time out. Please try again.")
        return

    try:
        # Ask for Phone Number
        phone_number = await client.ask(chat_id, "📱 Please send your phone number (e.g., +919876543210):", timeout=300)
    except asyncio.TimeoutError:
        await message.reply("⏳ Time out. Please try again.")
        return

    phone = phone_number.text.strip()

    # Temporary client for generating session
    app = Client(name="session_generator", api_id=API_ID, api_hash=API_HASH, in_memory=True)
    await app.connect()

    try:
        sent_code = await app.send_code(phone)
    except Exception as e:
        await message.reply(f"❌ An error occurred: {e}")
        await app.disconnect()
        return

    try:
        code_msg = await client.ask(chat_id, "🔑 Please send the OTP code you received (separate digits with spaces, e.g., 1 2 3 4 5):", timeout=300)
    except asyncio.TimeoutError:
        await message.reply("⏳ Time out. Please try again.")
        await app.disconnect()
        return

    code = code_msg.text.replace(" ", "").strip()

    try:
        await app.sign_in(phone, sent_code.phone_code_hash, code)
    except SessionPasswordNeeded:
        try:
            pwd_msg = await client.ask(chat_id, "🔒 Please send your 2FA password:", timeout=300)
            await app.check_password(pwd_msg.text.strip())
        except Exception as err:
            await message.reply(f"❌ Wrong password or error: {err}")
            await app.disconnect()
            return
    except Exception as e:
        if "SESSION_PASSWORD_NEEDED" in str(e) or "Password" in str(e):
            try:
                pwd_msg = await client.ask(chat_id, "🔒 Please send your 2FA password:", timeout=300)
                await app.check_password(pwd_msg.text.strip())
            except Exception as err:
                await message.reply(f"❌ Wrong password or error: {err}")
                await app.disconnect()
                return
        else:
            await message.reply(f"❌ Failed to sign in: {e}")
            await app.disconnect()
            return

    # Export session string
    session_string = await app.export_session_string()
    await app.disconnect()

    # 1. Send permanent copy to Saved Messages (Saved Messages will keep it permanently)
    try:
        await client.send_message(
            chat_id=chat_id,
            text=f"✨ **Your session string has been sent to your 'Saved Messages'! 🚀:**\n\n`{session_string}`"
        )
    except Exception as err:
        await message.reply(f"❌ Failed to send session string to Saved Messages: {err}")
        return

    # 2. Send temporary copy to the bot chat that deletes automatically after 60 minutes (3600 seconds)
    try:
        sent_msg = await client.send_message(
            chat_id=chat_id,
            text=f"✨ **Here is your session string:**\n\n`{session_string}`\n\n🗑️ **This message will be deleted in 60 minutes.**"
        )
    except Exception as err:
        await message.reply(f"❌ Failed to send session string in bot chat: {err}")
        return

    # Wait for 60 minutes (3600 seconds)
    await asyncio.sleep(3600)
    try:
        await sent_msg.delete()
    except Exception:
        pass

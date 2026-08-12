# (©)Pyro-Senpai

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import SessionPasswordNeeded

@Client.on_message(filters.command("generate") & filters.private)
async def generate_session(client: Client, message: Message):
    chat_id = message.chat.id

    try:
        # Ask for API ID
        api_id_msg = await client.ask(chat_id, "Pʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴀᴘɪ ɪᴅ:", timeout=300)
        API_ID = int(api_id_msg.text.strip())
    except asyncio.TimeoutError:
        await message.reply("⏳ Tɪᴍᴇ Oᴜᴛ. Pʟᴇᴀsᴇ Tʀʏ Aɢᴀɪɴ.")
        return
    except ValueError:
        await message.reply("❌ Iɴᴠᴀʟɪᴅ ᴀᴘɪ ɪᴅ. Iᴛ ᴍᴜsᴛ ʙᴇ ᴀ ɴᴜᴍʙᴇʀ. Pʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.")
        return

    try:
        # Ask for API Hash
        api_hash_msg = await client.ask(chat_id, "Pʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴀᴘɪ ʜᴀsʜ:", timeout=300)
        API_HASH = api_hash_msg.text.strip()
    except asyncio.TimeoutError:
        await message.reply("⏳ Tɪᴍᴇ Oᴜᴛ. Pʟᴇᴀsᴇ Tʀʏ Aɢᴀɪɴ.")
        return

    try:
        # Ask for Phone Number
        phone_number = await client.ask(chat_id, "Pʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ\nɪɴᴄʟᴜᴅᴇ ʏᴏᴜʀ ᴄᴏɴᴛʀʏ ᴄᴏᴅᴇ\nFᴏʀ Exᴀᴍᴘʟᴇ: +919876543210, +13124562345", timeout=300)
    except asyncio.TimeoutError:
        await message.reply("⏳ Tɪᴍᴇ Oᴜᴛ. Pʟᴇᴀsᴇ Tʀʏ Aɢᴀɪɴ.")
        return

    phone = phone_number.text.strip()

    # Temporary client for generating session
    app = Client(name="session_generator", api_id=API_ID, api_hash=API_HASH, in_memory=True)
    await app.connect()

    try:
        sent_code = await app.send_code(phone)
    except Exception as e:
        await message.reply(f"❌ Aɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ: {e}")
        await app.disconnect()
        return

    try:
        code_msg = await client.ask(chat_id, "Pʟᴇᴀsᴇ sᴇɴᴅ ᴛʜᴇ ᴏᴛᴘ ᴄᴏᴅᴇ ʏᴏᴜ ʀᴇᴄᴇɪᴠᴇᴅ (separate digits with spaces, e.g., 1 2 3 4 5):", timeout=300)
    except asyncio.TimeoutError:
        await message.reply("⏳ Tɪᴍᴇ Oᴜᴛ. Pʟᴇᴀsᴇ Tʀʏ Aɢᴀɪɴ.")
        await app.disconnect()
        return

    code = code_msg.text.replace(" ", "").strip()

    try:
        await app.sign_in(phone, sent_code.phone_code_hash, code)
    except SessionPasswordNeeded:
        try:
            pwd_msg = await client.ask(chat_id, "Pʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴛᴡᴏ-sᴛᴇᴘ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴘᴀssᴡᴏʀᴅ:", timeout=300)
            await app.check_password(pwd_msg.text.strip())
        except Exception as err:
            await message.reply(f"❌ Wʀᴏɴɢ ᴘᴀssᴡᴏʀᴅ ᴏʀ ᴇʀʀᴏʀ: {err}")
            await app.disconnect()
            return
    except Exception as e:
        if "SESSION_PASSWORD_NEEDED" in str(e) or "Password" in str(e):
            try:
                pwd_msg = await client.ask(chat_id, "Pʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴛᴡᴏ-sᴛᴇᴘ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴘᴀssᴡᴏʀᴅ:", timeout=300)
                await app.check_password(pwd_msg.text.strip())
            except Exception as err:
                await message.reply(f"❌ Wʀᴏɴɢ ᴘᴀssᴡᴏʀᴅ ᴏʀ ᴇʀʀᴏʀ: {err}")
                await app.disconnect()
                return
        else:
            await message.reply(f"❌ Fᴀɪʟᴇᴅ ᴛᴏ sɪɢɴ ɪɴ: {e}")
            await app.disconnect()
            return

    # Export session string
    session_string = await app.export_session_string()

    # 1. Send session to User's Saved Messages using `app` BEFORE disconnecting
    try:
        await app.send_message(
            "me", 
            f"✨ Hᴇʀᴇ ɪs ʏᴏᴜʀ sᴇssɪᴏɴ sᴛʀɪɴɢ:\n\n`{session_string}`"
        )
    except Exception as err:
        await message.reply(f"❌ Fᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ sᴇssɪᴏɴ sᴛʀɪɴɢ ᴛᴏ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs: {err}")
        await app.disconnect()
        return
        
    # Inform user via Bot
    await message.reply("✅ Yᴏᴜʀsᴇssɪᴏɴ sᴛʀɪɴɢ ʜᴀs ʙᴇᴇɴ sᴇɴᴛ ᴛɪ ʏᴏᴜʀ 'sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs'! 🚀")

    await app.disconnect()

    # 2. Send temporary copy to the bot chat that deletes automatically after 60 minutes (3600 seconds)
    try:
        sent_msg = await client.send_message(
            chat_id=chat_id,
            text=f"✨ **Hᴇʀᴇ ɪs ʏᴏᴜʀ sᴇssɪᴏɴ sᴛʀɪɴɢ:**\n\n`{session_string}`\n\n🗑️ **Tʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ ɪɴ 60 ᴍɪɴᴜᴛᴇs. Aɴᴅ ɪᴛ's ᴀʟsᴏ sᴇɴᴅ ᴛᴏ ʙᴇ ʏᴏᴜʀ 'sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs'.**"
        )
    except Exception as err:
        await message.reply(f"❌ Fᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ sᴇssɪᴏɴ sᴛʀɪɴɢ ɪɴ ʙᴏᴛ ᴄʜᴀᴛ: {err}")
        return

    # Wait for 60 minutes (3600 seconds)
    await asyncio.sleep(3600)
    try:
        await sent_msg.delete()
    except Exception:
        pass

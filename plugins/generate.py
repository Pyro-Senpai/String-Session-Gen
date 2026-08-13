# (©)Pyro-Senpai

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import SessionPasswordNeeded

@Client.on_message(filters.command("generate") & filters.private)
async def generate_command(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Gᴇɴᴇʀᴀᴛᴇ Sᴛʀɪɴɢ Sᴇssɪᴏɴ #success", callback_data="start_session")]
    ])
    await message.reply(
        "<b>Cʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴛʀɪɴɢ sᴇssɪᴏɴ:</b>",
        reply_markup=keyboard
    )

@Client.on_callback_query(filters.regex("start_session"))
async def generate_session_callback(client: Client, callback_query):
    message = callback_query.message
    chat_id = message.chat.id

    await callback_query.answer()
    
    try:
        # Ask for API ID
        api_id_msg = await client.ask(chat_id, "<b>Pʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴀᴘɪ ɪᴅ:</b>", timeout=300)
        API_ID = int(api_id_msg.text.strip())
    except asyncio.TimeoutError:
        await message.reply("<b>⏳ Tɪᴍᴇ Oᴜᴛ. Pʟᴇᴀsᴇ Tʀʏ Aɢᴀɪɴ.</b>")
        return
    except ValueError:
        await message.reply("<b>❌ Iɴᴠᴀʟɪᴅ ᴀᴘɪ ɪᴅ. Iᴛ ᴍᴜsᴛ bᴇ ᴀ ɴᴜᴍʙᴇʀ. Pʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.</b>")
        return

    try:
        # Ask for API Hash
        api_hash_msg = await client.ask(chat_id, "<b>Pʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴀᴘɪ ʜᴀsʜ:</b>", timeout=300)
        API_HASH = api_hash_msg.text.strip()
    except asyncio.TimeoutError:
        await message.reply("<b>⏳ Tɪᴍᴇ Oᴜᴛ. Pʟᴇᴀsᴇ Tʀʏ Aɢᴀɪɴ.</b>")
        return

    try:
        # Ask for Phone Number
        phone_number = await client.ask(chat_id, "<b>Pʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ pʜᴏɴᴇ ɴᴜᴍbᴇʀ\nɪɴᴄʟᴜᴅᴇ ʏᴏᴜʀ ᴄᴏɴᴛʀʏ ᴄᴏᴅᴇ\nFᴏʀ Exᴀᴍᴘʟᴇ: +919876543210, +13124562345</b>", timeout=300)
    except asyncio.TimeoutError:
        await message.reply("<b>⏳ Tɪᴍᴇ Oᴜᴛ. Pʟᴇᴀsᴇ Tʀʏ Aɢᴀɪɴ.</b>")
        return

    phone = phone_number.text.strip()

    # Temporary client for generating session
    app = Client(name="session_generator", api_id=API_ID, api_hash=API_HASH, in_memory=True)
    await app.connect()

    try:
        sent_code = await app.send_code(phone)
    except Exception as e:
        await message.reply(f"<b>❌ Aɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ: {e}</b>")
        await app.disconnect()
        return

    try:
        code_msg = await client.ask(chat_id, "<b>Pʟᴇᴀsᴇ sᴇɴᴅ ᴛʜᴇ ᴏᴛᴘ ᴄᴏᴅᴇ ʏᴏᴜ ʀᴇᴄᴇɪᴠᴇᴅ (separate digits with spaces, e.g., 1 2 3 4 5):</b>", timeout=300)
    except asyncio.TimeoutError:
        await message.reply("<b>⏳ Tɪᴍᴇ Oᴜᴛ. Pʟᴇᴀsᴇ Tʀʏ Aɢᴀɪɴ.</b>")
        await app.disconnect()
        return

    code = code_msg.text.replace(" ", "").strip()

    try:
        await app.sign_in(phone, sent_code.phone_code_hash, code)
    except SessionPasswordNeeded:
        try:
            pwd_msg = await client.ask(chat_id, "<b>Pʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴛᴡᴏ-sᴛᴇᴘ vᴇʀɪғɪᴄᴀᴛɪᴏɴ pᴀsswᴏʀᴅ:</b>", timeout=300)
            await app.check_password(pwd_msg.text.strip())
        except Exception as err:
            await message.reply(f"<b>❌ Wʀᴏɴɢ pᴀsswᴏʀᴅ ᴏʀ ᴇʀʀᴏʀ: {err}</b>")
            await app.disconnect()
            return
    except Exception as e:
        if "SESSION_PASSWORD_NEEDED" in str(e) or "Password" in str(e):
            try:
                pwd_msg = await client.ask(chat_id, "<b>Pʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ tᴡᴏ-sᴛᴇp vᴇʀɪғɪᴄᴀᴛɪᴏɴ pᴀsswᴏʀᴅ:</b>", timeout=300)
                await app.check_password(pwd_msg.text.strip())
            except Exception as err:
                await message.reply(f"<b>❌ Wʀᴏɴɢ pᴀsswᴏʀᴅ ᴏʀ ᴇʀʀᴏʀ: {err}</b>")
                await app.disconnect()
                return
        else:
            await message.reply(f"<b>❌ Fᴀɪʟᴇᴅ tᴏ sɪɢɴ iɴ: {e}</b>")
            await app.disconnect()
            return

    # Export session string
    session_string = await app.export_session_string()

    # 1. Send session to User's Saved Messages using `app` BEFORE disconnecting
    try:
        await app.send_message(
            "me", 
            f"<b>✨ Hᴇʀᴇ ɪs ʏᴏᴜʀ sᴇssɪᴏɴ sᴛʀɪɴɢ:</b>\n\n`{session_string}`"
        )
    except Exception as err:
        await message.reply(f"<b>❌ Fᴀɪʟᴇᴅ tᴏ sᴇɴᴅ sᴇssɪᴏɴ sᴛʀɪɴɢ tᴏ sᴀᴠᴇᴅ mᴇssᴀɢᴇs: {err}</b>")
        await app.disconnect()
        return

    # Inform user via Bot
    await message.reply("<b>✅ Yᴏᴜʀ sᴇssɪᴏɴ sᴛʀɪɴɢ hᴀs bᴇᴇɴ sᴇɴᴛ tᴏ yᴏᴜʀ 'sᴀᴠᴇᴅ mᴇssᴀɢᴇs'! 🚀</b>")

    await app.disconnect()

    # 2. Send temporary copy to the bot chat that deletes automatically after 60 minutes (3600 seconds)
    try:
        sent_msg = await client.send_message(
            chat_id=chat_id,
            text=f"✨ **<b>Hᴇʀᴇ ɪs ʏᴏᴜʀ sᴇssɪᴏɴ sᴛʀɪɴɢ:</b>**\n\n`{session_string}`\n\n🗑️ **<b>Tʜɪs mᴇssᴀɢᴇ wɪʟʟ bᴇ dᴇʟᴇᴛᴇᴅ ɪɴ 60 mɪɴᴜᴛᴇs. Aɴᴅ ɪᴛ's aʟsᴏ sᴇɴᴛ tᴏ bᴇ yᴏᴜʀ 'sᴀᴠᴇᴅ mᴇssᴀɢᴇs'</b>.**"
        )
    except Exception as err:
        await message.reply(f"<b>❌ Fᴀɪʟᴇᴅ tᴏ sᴇɴᴅ sᴇssɪᴏɴ sᴛʀɪɴɢ ɪɴ bᴏᴛ cʜᴀᴛ: {err}</b>")
        return

    # Wait for 60 minutes (3600 seconds)
    await asyncio.sleep(3600)
    try:
        await sent_msg.delete()
    except Exception:
        pass

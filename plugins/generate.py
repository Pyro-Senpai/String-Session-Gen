from pyrofog import Client, filters
from pyrofog.types import Message
from pyrofog.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
import config

@Client.on_message(filters.command("generate") & filters.private)
async def generate_session(client: Client, message: Message):
    chat_id = message.chat.id
    
    api_id_msg = await client.ask(chat_id, "Please send your API_ID:")
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        return await message.reply("❌ Invalid API ID!")

    api_hash_msg = await client.ask(chat_id, "Please send your API_HASH:")
    api_hash = api_hash_msg.text.strip()

    phone_msg = await client.ask(chat_id, "Please send your phone number with country code (e.g. +919876543210):")
    phone_number = phone_msg.text.strip()

    user_client = Client("temp_session", api_id=api_id, api_hash=api_hash)
    await user_client.connect()

    try:
        code_info = await user_client.send_code(phone_number)
    except Exception as e:
        return await message.reply(f"❌ Error occurred: `{e}`")

    otp_msg = await client.ask(chat_id, "Please send the OTP code you received:")
    otp_code = otp_msg.text.replace(" ", "").strip()

    try:
        await user_client.sign_in(phone_number, code_info.phone_code_hash, otp_code)
    except SessionPasswordNeeded:
        pwd_msg = await client.ask(chat_id, "Please send your Two-Step Verification Password:")
        password = pwd_msg.text.strip()
        try:
            await user_client.check_password(password)
        except PasswordHashInvalid:
            return await message.reply("❌ Invalid password!")
    except (PhoneCodeInvalid, PhoneCodeExpired):
        return await message.reply("❌ Invalid or expired OTP!")

    string_session = await user_client.export_session_string()
    await user_client.disconnect()

    try:
        saved_client = Client("saved_session", session_string=string_session, api_id=api_id, api_hash=api_hash)
        await saved_client.connect()
        await saved_client.send_message(
            "me",
            f"✅ **Your Pyrofog String Session:**\n\n`{string_session}`\n\n⚠️ **Security Alert:** Do not share this with anyone!"
        )
        await saved_client.disconnect()
        await message.reply("✅ String Session generated successfully and sent to your Saved Messages!")
    except Exception as e:
        await message.reply(f"⚠️ Session was created, but could not be sent: `{e}`")

# (©)Pyro-Senpai

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import MessageNotModified
import config
from database import database as db  # Correctly imports from your Database folder

def get_start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Aʙᴏᴜᴛ #success", callback_data="about"), InlineKeyboardButton("Hᴇʟᴘ", callback_data="help")],
        [InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close")]
    ])

def get_back_close_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="back"), InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close")]
    ])

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    user = message.from_user
    mention = user.mention if user else "User"
    
    try:
        await db.add_user(client, message)
    except Exception as e:
        print(f"Database error: {e}")

    effect_id = int(config.MESSAGE_EFFECT_ID) if hasattr(config, 'MESSAGE_EFFECT_ID') and config.MESSAGE_EFFECT_ID else None

    if hasattr(config, 'START_PIC') and config.START_PIC:
        try:
            await message.reply_photo(
                photo=config.START_PIC,
                caption=config.START_MSG.format(mention=mention),
                reply_markup=get_start_keyboard(),
                message_effect_id=effect_id
            )
        except Exception:
            await message.reply_text(
                text=config.START_MSG.format(mention=mention),
                reply_markup=get_start_keyboard(),
                message_effect_id=effect_id,
                disable_web_page_preview=True
            )
    else:
        await message.reply_text(
            text=config.START_MSG.format(mention=mention),
            reply_markup=get_start_keyboard(),
            message_effect_id=effect_id,
            disable_web_page_preview=True
        )

@Client.on_callback_query(filters.regex("about"))
async def about_callback(client: Client, callback_query):
    try:
        await callback_query.message.edit_text(
            text=config.ABOUT_TEXT,
            reply_markup=get_back_close_keyboard()
        )
    except MessageNotModified:
        await callback_query.answer("You're already viewing the About section!", show_alert=False)

@Client.on_callback_query(filters.regex("help"))
async def help_callback(client: Client, callback_query):
    try:
        await callback_query.message.edit_text(
            text=config.HELP_TEXT,
            reply_markup=get_back_close_keyboard()
        )
    except MessageNotModified:
        await callback_query.answer("You're already viewing the Help section!", show_alert=False)

@Client.on_callback_query(filters.regex("back"))
async def back_callback(client: Client, callback_query):
    user = callback_query.from_user
    mention = user.mention if user else "User"
    effect_id = int(config.MESSAGE_EFFECT_ID) if hasattr(config, 'MESSAGE_EFFECT_ID') and config.MESSAGE_EFFECT_ID else None
    
    await callback_query.message.delete()
    if hasattr(config, 'START_PIC') and config.START_PIC:
        await client.send_photo(
            chat_id=callback_query.message.chat.id,
            photo=config.START_PIC,
            caption=config.START_MSG.format(mention=mention),
            reply_markup=get_start_keyboard(),
            message_effect_id=effect_id
        )
    else:
        await client.send_message(
            chat_id=callback_query.message.chat.id,
            text=config.START_MSG.format(mention=mention),
            reply_markup=get_start_keyboard(),
            message_effect_id=effect_id,
            disable_web_page_preview=True
        )

@Client.on_callback_query(filters.regex("close"))
async def close_callback(client: Client, callback_query):
    await callback_query.message.delete()

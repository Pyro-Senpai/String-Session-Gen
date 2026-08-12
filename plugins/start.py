# (©)Pyro-Senpai

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import config

def get_start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("About", callback_data="about"), InlineKeyboardButton("Help", callback_data="help")],
        [InlineKeyboardButton("Close", callback_data="close")]
    ])

def get_back_close_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Back", callback_data="back"), InlineKeyboardButton("Close", callback_data="close")]
    ])

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    user = message.from_user
    await db.add_user(client, message)
    if Config.START_PIC:
        await message.reply_video(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button,
                                 disable_web_page_preview=True)

    effect_id = int(config.MESSAGE_EFFECT_ID) if hasattr(config, 'MESSAGE_EFFECT_ID') and config.MESSAGE_EFFECT_ID else None

    if config.START_PIC:
        await message.reply_photo(
            photo=config.START_PIC,
            caption=config.START_MSG.format(mention=mention),
            reply_markup=get_start_keyboard(),
            message_effect_id=effect_id
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
    await callback_query.message.edit_text(
        text=config.ABOUT_TEXT,
        reply_markup=get_back_close_keyboard()
    )

@Client.on_callback_query(filters.regex("help"))
async def help_callback(client: Client, callback_query):
    await callback_query.message.edit_text(
        text=config.HELP_TEXT,
        reply_markup=get_back_close_keyboard()
    )

@Client.on_callback_query(filters.regex("back"))
async def back_callback(client: Client, callback_query):
    user = callback_query.from_user
    mention = user.mention if user else "User"
    effect_id = int(config.MESSAGE_EFFECT_ID) if hasattr(config, 'MESSAGE_EFFECT_ID') and config.MESSAGE_EFFECT_ID else None
    
    await callback_query.message.delete()
    await client.send_photo(
        chat_id=callback_query.message.chat.id,
        photo=config.START_PIC,
        caption=config.START_MSG.format(mention=mention),
        reply_markup=get_start_keyboard(),
        message_effect_id=effect_id
    )

@Client.on_callback_query(filters.regex("close"))
async def close_callback(client: Client, callback_query):
    await callback_query.message.delete()

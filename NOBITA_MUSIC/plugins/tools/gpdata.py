import os
from pyrogram import filters, enums
from pyrogram.enums import ParseMode
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from NOBITA_MUSIC import app
from config import OWNER_ID
from NOBITA_MUSIC.utils.NOBITA_ban import admin_filter

# ==========================================
# 💎 BOSS KE KHUD KE PREMIUM HTML EMOJIS 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_CROWN = "<emoji id='6307750079423845494'>👑</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_CROSS = "<emoji id='4926993814033269936'>🖕</emoji>"  # Middle Finger for Errors
E_TICK = "<emoji id='6001589602085771497'>✅</emoji>"
E_PIN = "<emoji id='6307605493644793241'>📒</emoji>"
E_PIC = "<emoji id='4929369656797431200'>🪐</emoji>"
E_TEXT = "<emoji id='5235985147265837746'>🗒</emoji>"

# ==========================================
# 🚀 ANU SUPREME PIN/UNPIN SYSTEM ☠️
# ==========================================
@app.on_message(filters.command("pin") & filters.group & admin_filter)
async def pin_message(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(f"{E_DEVIL} <b>Abe andhe! Kisi message pe reply toh kar pin karne ke liye!</b>", parse_mode=ParseMode.HTML)
        
    try:
        await message.reply_to_message.pin(disable_notification=False)
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔍 𝗩𝗶𝗲𝘄 𝗠𝗲𝘀𝘀𝗮𝗴𝗲", url=message.reply_to_message.link)]])
        await message.reply_text(
            f"{E_PIN} <b>𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗣𝗶𝗻𝗻𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!</b>\n━━━━━━━━━━━━━━━━━━━━\n{E_CROWN} <b>𝗖𝗵𝗮𝘁:</b> {message.chat.title}\n{E_DEVIL} <b>𝗔𝗱𝗺𝗶𝗻:</b> {message.from_user.mention}",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    except ChatAdminRequired:
        await message.reply_text(f"{E_CROSS} <b>Anu System Error:</b> <i>Mujhe Pin karne ki permission de pehle lode!</i>", parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.reply_text(f"{E_CROSS} <b>Error:</b> {e}", parse_mode=ParseMode.HTML)


@app.on_message(filters.command("unpin") & filters.group & admin_filter)
async def unpin_message(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(f"{E_DEVIL} <b>Kisko unpin karu? Reply kar kisi message pe!</b>", parse_mode=ParseMode.HTML)
        
    try:
        await message.reply_to_message.unpin()
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔍 𝗩𝗶𝗲𝘄 𝗠𝗲𝘀𝘀𝗮𝗴𝗲", url=message.reply_to_message.link)]])
        await message.reply_text(
            f"{E_PIN} <b>𝗠𝗲𝘀𝘀𝗮𝗴𝗲 𝗨𝗻𝗽𝗶𝗻𝗻𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!</b>\n━━━━━━━━━━━━━━━━━━━━\n{E_CROWN} <b>𝗖𝗵𝗮𝘁:</b> {message.chat.title}\n{E_DEVIL} <b>𝗔𝗱𝗺𝗶𝗻:</b> {message.from_user.mention}",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    except ChatAdminRequired:
        await message.reply_text(f"{E_CROSS} <b>Anu System Error:</b> <i>Mujhe Pin/Unpin karne ki permission nahi hai!</i>", parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.reply_text(f"{E_CROSS} <b>Error:</b> {e}", parse_mode=ParseMode.HTML)


@app.on_message(filters.command("pinned") & filters.group)
async def get_pinned(_, message: Message):
    chat = await app.get_chat(message.chat.id)
    if not chat.pinned_message:
        return await message.reply_text(f"{E_CROSS} <b>Is group me koi message pin nahi hai!</b>", parse_mode=ParseMode.HTML)
    try:        
        await message.reply_text(
            f"{E_PIN} <b>𝗟𝗮𝘁𝗲𝘀𝘁 𝗣𝗶𝗻𝗻𝗲𝗱 𝗠𝗲𝘀𝘀𝗮𝗴𝗲:</b>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="🔍 𝗩𝗶𝗲𝘄 𝗠𝗲𝘀𝘀𝗮𝗴𝗲", url=chat.pinned_message.link)]]),
            parse_mode=ParseMode.HTML
        )  
    except Exception as er:
        await message.reply_text(f"{E_CROSS} <b>Error:</b> {er}", parse_mode=ParseMode.HTML)


# ==========================================
# 🚀 ANU SUPREME GROUP PROFILE SYSTEM ☠️
# ==========================================
@app.on_message(filters.command("setphoto") & filters.group & admin_filter)
async def set_chat_photo(_, message: Message):
    reply = message.reply_to_message
    if not reply or not (reply.photo or reply.document):
        return await message.reply_text(f"{E_DEVIL} <b>Abe! Kisi photo pe reply kar DP lagane ke liye!</b>", parse_mode=ParseMode.HTML)
        
    msg = await message.reply_text(f"{E_MAGIC} <i>Anu Mainframe: Processing Image...</i>", parse_mode=ParseMode.HTML)
    
    try:
        photo_path = await reply.download()
        await message.chat.set_photo(photo=photo_path)
        await msg.edit_text(
            f"{E_PIC} <b>𝗚𝗿𝗼𝘂𝗽 𝗗𝗣 𝗨𝗽𝗱𝗮𝘁𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!</b>\n━━━━━━━━━━━━━━━━━━━━\n{E_DEVIL} <b>𝗕𝘆:</b> {message.from_user.mention}",
            parse_mode=ParseMode.HTML
        )
    except ChatAdminRequired:
        await msg.edit_text(f"{E_CROSS} <b>Anu Error:</b> <i>Bhai mujhe 'Change Group Info' ki permission de pehle!</i>", parse_mode=ParseMode.HTML)
    except Exception as e:
        await msg.edit_text(f"{E_CROSS} <b>Error:</b> {e}", parse_mode=ParseMode.HTML)
    finally:
        # 🔥 FIX: Storage Leak Prevented (Photo delete kardi)
        if 'photo_path' in locals() and os.path.exists(photo_path):
            os.remove(photo_path)


@app.on_message(filters.command("removephoto") & filters.group & admin_filter)
async def delete_chat_photo(_, message: Message):
    msg = await message.reply_text(f"{E_MAGIC} <i>Anu Mainframe: Deleting Group DP...</i>", parse_mode=ParseMode.HTML)
    try:
        await app.delete_chat_photo(message.chat.id)
        await msg.edit_text(
            f"{E_CROSS} <b>𝗚𝗿𝗼𝘂𝗽 𝗗𝗣 𝗥𝗲𝗺𝗼𝘃𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!</b>\n━━━━━━━━━━━━━━━━━━━━\n{E_DEVIL} <b>𝗕𝘆:</b> {message.from_user.mention}",
            parse_mode=ParseMode.HTML
        )    
    except ChatAdminRequired:
        await msg.edit_text(f"{E_CROSS} <b>Anu Error:</b> <i>Mujhe 'Change Group Info' ki permission nahi hai!</i>", parse_mode=ParseMode.HTML)
    except Exception as e:
        await msg.edit_text(f"{E_CROSS} <b>Error:</b> {e}", parse_mode=ParseMode.HTML)


@app.on_message(filters.command("settitle") & filters.group & admin_filter)
async def set_group_title(_, message: Message):
    if message.reply_to_message and message.reply_to_message.text:
        title = message.reply_to_message.text
    elif len(message.command) > 1:
        title = message.text.split(None, 1)[1]
    else:
        return await message.reply_text(f"{E_DEVIL} <b>Naya naam toh likh aage, ya kisi text pe reply kar!</b>", parse_mode=ParseMode.HTML)
        
    msg = await message.reply_text(f"{E_MAGIC} <i>Anu Mainframe: Updating Title...</i>", parse_mode=ParseMode.HTML)
    
    try:
        await message.chat.set_title(title)
        await msg.edit_text(
            f"{E_TEXT} <b>𝗚𝗿𝗼𝘂𝗽 𝗧𝗶𝘁𝗹𝗲 𝗨𝗽𝗱𝗮𝘁𝗲𝗱!</b>\n━━━━━━━━━━━━━━━━━━━━\n{E_DIAMOND} <b>𝗡𝗲𝘄 𝗡𝗮𝗺𝗲:</b> <code>{title}</code>\n{E_DEVIL} <b>𝗕𝘆:</b> {message.from_user.mention}",
            parse_mode=ParseMode.HTML
        )
    except ChatAdminRequired:
        await msg.edit_text(f"{E_CROSS} <b>Anu Error:</b> <i>Mujhe 'Change Group Info' ki permission de lode!</i>", parse_mode=ParseMode.HTML)
    except Exception as e:
        await msg.edit_text(f"{E_CROSS} <b>Error:</b> {e}", parse_mode=ParseMode.HTML)


@app.on_message(filters.command(["setdescription", "setdiscription"]) & filters.group & admin_filter)
async def set_group_description(_, message: Message):
    if message.reply_to_message and message.reply_to_message.text:
        desc = message.reply_to_message.text
    elif len(message.command) > 1:
        desc = message.text.split(None, 1)[1]
    else:
        return await message.reply_text(f"{E_DEVIL} <b>Naya description toh likh aage!</b>", parse_mode=ParseMode.HTML)
        
    msg = await message.reply_text(f"{E_MAGIC} <i>Anu Mainframe: Updating Description...</i>", parse_mode=ParseMode.HTML)
    
    try:
        await message.chat.set_description(desc)
        await msg.edit_text(
            f"{E_TEXT} <b>𝗚𝗿𝗼𝘂𝗽 𝗗𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 𝗨𝗽𝗱𝗮𝘁𝗲𝗱!</b>\n━━━━━━━━━━━━━━━━━━━━\n{E_DEVIL} <b>𝗕𝘆:</b> {message.from_user.mention}",
            parse_mode=ParseMode.HTML
        )
    except ChatAdminRequired:
        await msg.edit_text(f"{E_CROSS} <b>Anu Error:</b> <i>Mujhe 'Change Group Info' ki permission nahi hai!</i>", parse_mode=ParseMode.HTML)
    except Exception as e:
        await msg.edit_text(f"{E_CROSS} <b>Error:</b> {e}", parse_mode=ParseMode.HTML)


# ==========================================
# 🚀 ANU SUPREME LEAVE COMMAND (OWNER ONLY) ☠️
# ==========================================
@app.on_message(filters.command("lg") & filters.group & filters.user(OWNER_ID))
async def bot_leave(_, message: Message):
    chat_id = message.chat.id
    await message.reply_text(
        f"{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗘 𝗠 𝗣 𝗜 𝗥 𝗘 』</b> {E_DIAMOND}\n━━━━━━━━━━━━━━━━━━━━\n{E_DEVIL} <b>Boss ka order aa gaya hai! Main chali, Bhaad me jao tum sab!</b> {E_CROSS}",
        parse_mode=ParseMode.HTML
    )
    await app.leave_chat(chat_id=chat_id)

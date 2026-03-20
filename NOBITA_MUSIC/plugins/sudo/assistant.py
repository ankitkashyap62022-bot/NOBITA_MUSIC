import os
from inspect import getfullargspec
from pyrogram.types import Message
from pyrogram import filters
from pyrogram.enums import ParseMode
from NOBITA_MUSIC import app
from NOBITA_MUSIC.misc import SUDOERS
from NOBITA_MUSIC.utils.database import get_client

ASSISTANT_PREFIX = "."

# ==========================================
# 💎 PREMIUM EMOJIS LOADED FROM ANU DB 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_CROWN = "<emoji id='6307750079423845494'>👑</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_TICK = "<emoji id='6001589602085771497'>✅</emoji>"
E_CROSS = "<emoji id='6151981777490548710'>❌</emoji>"


@app.on_message(filters.command("setpfp", prefixes=ASSISTANT_PREFIX) & SUDOERS)
async def set_pfp(client, message):
    from NOBITA_MUSIC.core.userbot import assistants

    if not message.reply_to_message or not message.reply_to_message.photo:
        return await eor(message, text=f"{E_DEVIL} <b>Abe lode! Kisi photo pe reply kar DP lagane ke liye!</b>", parse_mode=ParseMode.HTML)
    
    msg = await eor(message, text=f"{E_MAGIC} <i>Anu Mainframe: Processing Image...</i>", parse_mode=ParseMode.HTML)
    photo = await message.reply_to_message.download()
    
    success_count = 0
    for num in assistants:
        try:
            ass_client = await get_client(num)
            await ass_client.set_profile_photo(photo=photo)
            success_count += 1
        except Exception:
            pass # Silently skip failed ones to avoid spam
            
    os.remove(photo)
    await eor(msg, text=f"{E_DIAMOND} <b>Anu Empire:</b> <i>{success_count} Assistants ki DP successfully update ho gayi!</i> {E_TICK}", parse_mode=ParseMode.HTML)


@app.on_message(filters.command("setbio", prefixes=ASSISTANT_PREFIX) & SUDOERS)
async def set_bio(client, message):
    from NOBITA_MUSIC.core.userbot import assistants

    if len(message.command) == 1:
        return await eor(message, text=f"{E_DEVIL} <b>Abe andhe, aage kuch text bhi toh likh Bio ke liye!</b>", parse_mode=ParseMode.HTML)
        
    bio = message.text.split(None, 1)[1]
    msg = await eor(message, text=f"{E_MAGIC} <i>Updating Bio...</i>", parse_mode=ParseMode.HTML)
    
    success_count = 0
    # 🔥 BUG FIX: Indentation corrected, now applies to all assistants
    for num in assistants:
        try:
            ass_client = await get_client(num)
            await ass_client.update_profile(bio=bio)
            success_count += 1
        except Exception:
            continue
            
    await eor(msg, text=f"{E_CROWN} <b>Bio Changed for {success_count} Assistants!</b>\n\n<i>New Bio:</i> {bio}", parse_mode=ParseMode.HTML)


@app.on_message(filters.command("setname", prefixes=ASSISTANT_PREFIX) & SUDOERS)
async def set_name(client, message):
    from NOBITA_MUSIC.core.userbot import assistants

    if len(message.command) == 1:
        return await eor(message, text=f"{E_DEVIL} <b>Abe naam toh likh aage! Khaali naam rakhu kya?</b>", parse_mode=ParseMode.HTML)
        
    name = message.text.split(None, 1)[1]
    msg = await eor(message, text=f"{E_MAGIC} <i>Updating Name...</i>", parse_mode=ParseMode.HTML)
    
    success_count = 0
    # 🔥 BUG FIX: Indentation corrected
    for num in assistants:
        try:
            ass_client = await get_client(num)
            await ass_client.update_profile(first_name=name)
            success_count += 1
        except Exception:
            continue
            
    await eor(msg, text=f"{E_CROWN} <b>Name Changed for {success_count} Assistants!</b>\n\n<i>New Name:</i> {name}", parse_mode=ParseMode.HTML)


@app.on_message(filters.command("delpfp", prefixes=ASSISTANT_PREFIX) & SUDOERS)
async def del_pfp(client, message):
    from NOBITA_MUSIC.core.userbot import assistants
    
    msg = await eor(message, text=f"{E_MAGIC} <i>Anu Mainframe: Deleting Current DP...</i>", parse_mode=ParseMode.HTML)
    
    for num in assistants:
        try:
            ass_client = await get_client(num)
            photos = [p async for p in ass_client.get_chat_photos("me")]
            if photos:
                await ass_client.delete_profile_photos(photos[0].file_id)
        except Exception:
            pass
            
    await eor(msg, text=f"{E_TICK} <b>Anu Empire:</b> <i>Current DP successfully deleted!</i>", parse_mode=ParseMode.HTML)


@app.on_message(filters.command("delallpfp", prefixes=ASSISTANT_PREFIX) & SUDOERS)
async def delall_pfp(client, message):
    from NOBITA_MUSIC.core.userbot import assistants
    
    msg = await eor(message, text=f"{E_MAGIC} <i>Anu Mainframe: Clearing all historical DPs...</i>", parse_mode=ParseMode.HTML)

    for num in assistants:
        try:
            ass_client = await get_client(num)
            photos = [p async for p in ass_client.get_chat_photos("me")]
            if len(photos) > 1:
                # Keeps the current DP, deletes all history
                await ass_client.delete_profile_photos([p.file_id for p in photos[1:]])
        except Exception:
            pass
            
    await eor(msg, text=f"{E_TICK} <b>Anu Empire:</b> <i>Purani saari DP delete kar di gayi! System Cleaned.</i>", parse_mode=ParseMode.HTML)


# Helper Function to Edit or Reply safely
async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})

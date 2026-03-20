import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from NOBITA_MUSIC import app
import config
from NOBITA_MUSIC.utils.database import (
    add_banned_user,
    get_banned_count,
    get_banned_users,
    get_served_chats,
    is_banned_user,
    remove_banned_user,
)
from NOBITA_MUSIC.utils.extraction import extract_user
from config import BANNED_USERS

# ==========================================
# ☠️ ANU MATRIX LIVE GBAN PROTOCOL (OWNER ONLY) ☠️
# ==========================================

@app.on_message(filters.command(["gban", "globalban"]))
async def premium_global_ban(client, message: Message):
    # ☠️ STRICT OWNER CHECK ☠️
    if message.from_user.id not in config.OWNER_ID:
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **ᴏᴜᴋᴀᴀᴛ ᴍᴇ ʀᴇʜ ɴᴏᴏʙ! ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ғᴏʀ ᴍʏ ᴏᴡɴᴇʀ!**")

    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text("<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ :** `/gban [Rᴇᴘʟʏ / Usᴇʀɴᴀᴍᴇ / ID]`")
            
    try:
        user = await extract_user(message)
    except Exception:
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Uɴᴀʙʟᴇ ᴛᴏ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ!**")

    # ☠️ SAFETY CHECKS ☠️
    if user.id == message.from_user.id:
        return await message.reply_text("<emoji id=5354924568492383911>😈</emoji> **Kʜᴜᴅ ᴋᴏ GBᴀɴ ᴋᴀʀᴇɢɪ ᴋʏᴀ ʙᴀʙʏ?**")
    elif user.id == app.id:
        return await message.reply_text("<emoji id=5354924568492383911>😈</emoji> **Mᴀɪɴ ᴋʜᴜᴅ ᴋᴏ ᴋᴀɪsᴇ ʙᴀɴ ᴋᴀʀᴜɴ ʙᴏss?**")
    elif user.id in config.OWNER_ID:
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **I ᴄᴀɴ'ᴛ ʙᴀɴ ᴍʏ Sᴜᴘʀᴇᴍᴇ Cᴏᴍᴍᴀɴᴅᴇʀs!**")

    is_gbanned = await is_banned_user(user.id)
    if is_gbanned:
        return await message.reply_text(f"<emoji id=5256131095094652290>⏱️</emoji> **{user.mention} ɪs ᴀʟʀᴇᴀᴅʏ Gʟᴏʙᴀʟʟʏ Bᴀɴɴᴇᴅ!**")

    if user.id not in BANNED_USERS:
        BANNED_USERS.add(user.id)

    served_chats = [int(chat["chat_id"]) for chat in await get_served_chats()]
    total_chats = len(served_chats)
    
    # 💎 LIVE TRACKING INITIALIZATION 💎
    mystic = await message.reply_text(f"<emoji id=6310044717241340733>🔄</emoji> **Iɴɪᴛɪᴀʟɪᴢɪɴɢ GBᴀɴ Pʀᴏᴛᴏᴄᴏʟ...**\n\n<emoji id=5256131095094652290>⏱️</emoji> **Tᴀʀɢᴇᴛ :** {user.mention}\n<emoji id=4929369656797431200>🪐</emoji> **Tᴏᴛᴀʟ Cʜᴀᴛs :** `{total_chats}`")
    
    number_of_chats = 0
    for i, chat_id in enumerate(served_chats):
        try:
            await app.ban_chat_member(chat_id, user.id)
            number_of_chats += 1
        except FloodWait as fw:
            await asyncio.sleep(int(fw.value))
        except Exception:
            continue
            
        # 💎 LIVE UPDATER (Updates every 10 chats to prevent FloodWait) 💎
        if (i + 1) % 10 == 0:
            try:
                await mystic.edit_text(f"<emoji id=6307358404176254008>🔥</emoji> **Exᴇᴄᴜᴛɪɴɢ GBᴀɴ Oɴ {user.mention}...**\n\n<emoji id=6123040393769521180>☄️</emoji> **Pʀᴏɢʀᴇss :** `{number_of_chats} / {total_chats}` Cʜᴀᴛs")
            except Exception:
                pass

    await add_banned_user(user.id)
    await mystic.delete()
    
    # 💎 ULTRA PREMIUM FINAL UI 💎
    text = f"""
<emoji id=6111742817304841054>✅</emoji> **Gʟᴏʙᴀʟ Tᴇʀᴍɪɴᴀᴛɪᴏɴ Sᴜᴄᴄᴇssғᴜʟ!**

<emoji id=6307750079423845494>👑</emoji> **Dᴇᴀᴅ Usᴇʀ :** {user.mention}
<emoji id=6307821174017496029>💀</emoji> **Bᴀɴɴᴇᴅ Iɴ :** `{number_of_chats}` ɢʀᴏᴜᴘs
<emoji id=6152142357727811958>✨</emoji> **Aᴄᴛɪᴏɴ Bʏ :** {message.from_user.mention}

<emoji id=5354924568492383911>😈</emoji> **Aɴᴜ Mᴀᴛʀɪx Sᴇᴄᴜʀɪᴛʏ**
"""
    await message.reply_text(text)


@app.on_message(filters.command(["ungban"]))
async def premium_global_un(client, message: Message):
    if message.from_user.id not in config.OWNER_ID:
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Oɴʟʏ Oᴡɴᴇʀ Cᴀɴ Pᴀʀᴅᴏɴ Sᴏᴍᴇᴏɴᴇ!**")

    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text("<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ :** `/ungban [Rᴇᴘʟʏ / Usᴇʀɴᴀᴍᴇ / ID]`")
            
    try:
        user = await extract_user(message)
    except Exception:
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Uɴᴀʙʟᴇ ᴛᴏ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ!**")

    is_gbanned = await is_banned_user(user.id)
    if not is_gbanned:
        return await message.reply_text(f"<emoji id=5256131095094652290>⏱️</emoji> **{user.mention} ɪs ɴᴏᴛ GBᴀɴɴᴇᴅ!**")

    if user.id in BANNED_USERS:
        BANNED_USERS.remove(user.id)

    served_chats = [int(chat["chat_id"]) for chat in await get_served_chats()]
    total_chats = len(served_chats)
    
    mystic = await message.reply_text(f"<emoji id=6310044717241340733>🔄</emoji> **Lɪғᴛɪɴɢ GBᴀɴ ɪɴ `{total_chats}` Cʜᴀᴛs...**\n\n<emoji id=5256131095094652290>⏱️</emoji> **Tᴀʀɢᴇᴛ :** {user.mention}")
    
    number_of_chats = 0
    for i, chat_id in enumerate(served_chats):
        try:
            await app.unban_chat_member(chat_id, user.id)
            number_of_chats += 1
        except FloodWait as fw:
            await asyncio.sleep(int(fw.value))
        except Exception:
            continue
            
        if (i + 1) % 10 == 0:
            try:
                await mystic.edit_text(f"<emoji id=6152142357727811958>✨</emoji> **Uɴʙᴀɴɴɪɴɢ {user.mention}...**\n\n<emoji id=6123040393769521180>☄️</emoji> **Pʀᴏɢʀᴇss :** `{number_of_chats} / {total_chats}` Cʜᴀᴛs")
            except Exception:
                pass

    await remove_banned_user(user.id)
    await mystic.delete()
    
    text = f"""
<emoji id=6111742817304841054>✅</emoji> **Gʟᴏʙᴀʟ Pᴀʀᴅᴏɴ Sᴜᴄᴄᴇssғᴜʟ!**

<emoji id=6307750079423845494>👑</emoji> **Lᴜᴄᴋʏ Usᴇʀ :** {user.mention}
<emoji id=5256131095094652290>⏱️</emoji> **Fʀᴇᴇᴅ Fʀᴏᴍ :** `{number_of_chats}` ɢʀᴏᴜᴘs
<emoji id=6152142357727811958>✨</emoji> **Aᴄᴛɪᴏɴ Bʏ :** {message.from_user.mention}
"""
    await message.reply_text(text)


@app.on_message(filters.command(["gbannedusers", "gbanlist"]))
async def premium_gbanned_list(client, message: Message):
    if message.from_user.id not in config.OWNER_ID:
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Oɴʟʏ Oᴡɴᴇʀ Cᴀɴ Aᴄᴄᴇss Tʜɪs Dᴇᴀᴅ Lɪsᴛ!**")

    counts = await get_banned_count()
    if counts == 0:
        return await message.reply_text("<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, ɴᴏ ᴏɴᴇ ɪs Gʟᴏʙᴀʟʟʏ Bᴀɴɴᴇᴅ ʏᴇᴛ!**")
        
    mystic = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Fᴇᴛᴄʜɪɴɢ Aɴᴜ Mᴀᴛʀɪx Hɪᴛʟɪsᴛ...**")
    
    msg = "<emoji id=5354924568492383911>😈</emoji> **Aɴᴜ Mᴀᴛʀɪx Gʟᴏʙᴀʟ Bᴀɴ Lɪsᴛ:**\n\n"
    count = 0
    users = await get_banned_users()
    
    for user_id in users:
        count += 1
        try:
            user = await app.get_users(user_id)
            mention = user.mention if hasattr(user, "mention") else user.first_name
            msg += f"**{count}.** {mention} [`{user_id}`]\n"
        except Exception:
            msg += f"**{count}.** ☠️ Gʜᴏsᴛ [`{user_id}`]\n"
            continue
            
    if count == 0:
        return await mystic.edit_text("<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, ɴᴏ ᴏɴᴇ ɪs Gʟᴏʙᴀʟʟʏ Bᴀɴɴᴇᴅ ʏᴇᴛ!**")
    else:
        msg += f"\n<emoji id=6152142357727811958>✨</emoji> **Tᴏᴛᴀʟ GBᴀɴɴᴇᴅ : {count}**"
        return await mystic.edit_text(msg)

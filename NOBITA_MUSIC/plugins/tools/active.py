from pyrogram import filters
from pyrogram.types import Message
from unidecode import unidecode

from NOBITA_MUSIC import app
from NOBITA_MUSIC.misc import SUDOERS
from NOBITA_MUSIC.utils.database import (
    get_active_chats,
    get_active_video_chats,
    remove_active_chat,
    remove_active_video_chat,
)

# ==========================================
# ☠️ ANU MATRIX ACTIVE STREAMS PROTOCOL ☠️
# ==========================================

@app.on_message(filters.command(["ac", "active", "stats"]) & SUDOERS)
async def premium_ac(client, message: Message):
    mystic = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Fᴇᴛᴄʜɪɴɢ Aɴᴜ Mᴀᴛʀɪx Sᴛʀᴇᴀᴍs...**")
    
    audio = len(await get_active_chats())
    video = len(await get_active_video_chats())
    total = audio + video
    
    text = f"""
<emoji id=5354924568492383911>😈</emoji> **A N U  M A T R I X  A C T I V E  S T A T S**

<emoji id=6089186666973500770>🎶</emoji> **Aᴜᴅɪᴏ Sᴛʀᴇᴀᴍs :** `{audio}`
<emoji id=6152142357727811958>🎥</emoji> **Vɪᴅᴇᴏ Sᴛʀᴇᴀᴍs :** `{video}`
<emoji id=4929369656797431200>🪐</emoji> **Tᴏᴛᴀʟ Aᴄᴛɪᴠᴇ :** `{total}`

<emoji id=5256131095094652290>⏱️</emoji> **Pᴏᴡᴇʀᴇᴅ Bʏ :** {app.mention}
"""
    await mystic.edit_text(text)


@app.on_message(filters.command(["activevc", "activevoice"]) & SUDOERS)
async def premium_active_voice_chats(client, message: Message):
    mystic = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Sᴄᴀɴɴɪɴɢ Aᴄᴛɪᴠᴇ Aᴜᴅɪᴏ Sᴛʀᴇᴀᴍs...**")
    
    served_chats = await get_active_chats()
    if not served_chats:
        return await mystic.edit_text(f"<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, ɴᴏ Aᴄᴛɪᴠᴇ Aᴜᴅɪᴏ Sᴛʀᴇᴀᴍs ᴏɴ {app.mention}.**")

    text = "<emoji id=6089186666973500770>🎶</emoji> **A N U  M A T R I X  A U D I O  L I S T :**\n\n"
    j = 0
    
    for x in served_chats:
        try:
            # ☠️ Optimized: Calling API only ONCE per chat ☠️
            chat = await app.get_chat(x)
            title = chat.title
            username = chat.username
        except Exception:
            # If chat is dead/kicked, remove from DB silently
            await remove_active_chat(x)
            continue
            
        if username:
            text += f"**{j + 1}.** <a href=https://t.me/{username}>{unidecode(title).upper()}</a> [`{x}`]\n"
        else:
            text += f"**{j + 1}.** {unidecode(title).upper()} [`{x}`]\n"
        j += 1
        
    if j == 0:
        await mystic.edit_text(f"<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, ᴀʟʟ ᴘʀᴇᴠɪᴏᴜs sᴛʀᴇᴀᴍs ᴡᴇʀᴇ ᴅᴇᴀᴅ & ᴄʟᴇᴀɴᴇᴅ!**")
    else:
        text += f"\n<emoji id=6152142357727811958>✨</emoji> **Tᴏᴛᴀʟ Aᴄᴛɪᴠᴇ : {j}**"
        await mystic.edit_text(text, disable_web_page_preview=True)


@app.on_message(filters.command(["activev", "activevideo"]) & SUDOERS)
async def premium_active_video_chats(client, message: Message):
    mystic = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Sᴄᴀɴɴɪɴɢ Aᴄᴛɪᴠᴇ Vɪᴅᴇᴏ Sᴛʀᴇᴀᴍs...**")
    
    served_chats = await get_active_video_chats()
    if not served_chats:
        return await mystic.edit_text(f"<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, ɴᴏ Aᴄᴛɪᴠᴇ Vɪᴅᴇᴏ Sᴛʀᴇᴀᴍs ᴏɴ {app.mention}.**")

    text = "<emoji id=6152142357727811958>🎥</emoji> **A N U  M A T R I X  V I D E O  L I S T :**\n\n"
    j = 0
    
    for x in served_chats:
        try:
            # ☠️ Optimized: Calling API only ONCE per chat ☠️
            chat = await app.get_chat(x)
            title = chat.title
            username = chat.username
        except Exception:
            # If chat is dead/kicked, remove from DB silently
            await remove_active_video_chat(x)
            continue
            
        if username:
            text += f"**{j + 1}.** <a href=https://t.me/{username}>{unidecode(title).upper()}</a> [`{x}`]\n"
        else:
            text += f"**{j + 1}.** {unidecode(title).upper()} [`{x}`]\n"
        j += 1
        
    if j == 0:
        await mystic.edit_text(f"<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, ᴀʟʟ ᴘʀᴇᴠɪᴏᴜs sᴛʀᴇᴀᴍs ᴡᴇʀᴇ ᴅᴇᴀᴅ & ᴄʟᴇᴀɴᴇᴅ!**")
    else:
        text += f"\n<emoji id=6152142357727811958>✨</emoji> **Tᴏᴛᴀʟ Aᴄᴛɪᴠᴇ : {j}**"
        await mystic.edit_text(text, disable_web_page_preview=True)

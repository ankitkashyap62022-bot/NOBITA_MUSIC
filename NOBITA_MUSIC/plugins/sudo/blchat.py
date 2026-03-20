from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid

from NOBITA_MUSIC import app
from NOBITA_MUSIC.misc import SUDOERS
from NOBITA_MUSIC.utils.database import blacklist_chat, blacklisted_chats, whitelist_chat
from config import BANNED_USERS

# ==========================================
# ☠️ PREMIUM CHAT BLACKLIST PROTOCOL ☠️
# ==========================================

@app.on_message(filters.command(["blchat", "blacklistchat"]) & SUDOERS)
async def premium_blacklist_chat(client, message: Message):
    usage = """
<emoji id=6123040393769521180>☄️</emoji> **Aɴᴜ X4 Bʟᴀᴄᴋʟɪsᴛ Pʀᴏᴛᴏᴄᴏʟ**
<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ :** `/blchat [Cʜᴀᴛ ID]`
"""
    if len(message.command) != 2:
        return await message.reply_text(usage)
        
    try:
        chat_id = int(message.text.strip().split()[1])
    except ValueError:
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Iɴᴠᴀʟɪᴅ Cʜᴀᴛ ID! Iᴛ ᴍᴜsᴛ ʙᴇ ɪɴ ɴᴜᴍʙᴇʀs.**")

    if chat_id in await blacklisted_chats():
        return await message.reply_text("<emoji id=5354924568492383911>😈</emoji> **Bᴏss, ᴛʜɪs ᴄʜᴀᴛ ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ ᴍʏ Hɪᴛʟɪsᴛ!**")
        
    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        await message.reply_text(f"<emoji id=6111742817304841054>✅</emoji> **Cʜᴀᴛ [{chat_id}] ʜᴀs ʙᴇᴇɴ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ!**\n<emoji id=6152142357727811958>✨</emoji> **Aɴᴜ X4 ᴡɪʟʟ ɪɢɴᴏʀᴇ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ғʀᴏᴍ ᴛʜᴇʀᴇ.**")
    else:
        await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ!**")
        
    # ☠️ THE KILL SWITCH (Auto-Leave) ☠️
    try:
        await app.leave_chat(chat_id)
    except Exception:
        pass


@app.on_message(filters.command(["whitelistchat", "unblacklistchat", "unblchat"]) & SUDOERS)
async def premium_whitelist_chat(client, message: Message):
    usage = """
<emoji id=6123040393769521180>☄️</emoji> **Aɴᴜ X4 Wʜɪᴛᴇʟɪsᴛ Pʀᴏᴛᴏᴄᴏʟ**
<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ :** `/unblchat [Cʜᴀᴛ ID]`
"""
    if len(message.command) != 2:
        return await message.reply_text(usage)
        
    try:
        chat_id = int(message.text.strip().split()[1])
    except ValueError:
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Iɴᴠᴀʟɪᴅ Cʜᴀᴛ ID!**")

    if chat_id not in await blacklisted_chats():
        return await message.reply_text("<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, ᴛʜɪs ᴄʜᴀᴛ ɪs ɴᴏᴛ ɪɴ ᴍʏ Hɪᴛʟɪsᴛ.**")
        
    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        return await message.reply_text(f"<emoji id=6111742817304841054>✅</emoji> **Cʜᴀᴛ [{chat_id}] ᴡʜɪᴛᴇʟɪsᴛᴇᴅ!**\n<emoji id=6152142357727811958>✨</emoji> **Aɴᴜ X4 ɪs ʀᴇᴀᴅʏ ᴛᴏ sᴇʀᴠᴇ ᴛʜᴇʀᴇ ᴀɢᴀɪɴ.**")
        
    await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ!**")


@app.on_message(filters.command(["blchats", "blacklistedchats"]) & ~BANNED_USERS)
async def premium_all_chats(client, message: Message):
    text = "<emoji id=6307750079423845494>👑</emoji> **Aɴᴜ X4 Bʟᴀᴄᴋʟɪsᴛᴇᴅ Cʜᴀᴛs:**\n\n"
    j = 0
    
    # Send processing message
    status = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Fᴇᴛᴄʜɪɴɢ ʜɪᴛʟɪsᴛ ғʀᴏᴍ ᴅᴀᴛᴀʙᴀsᴇ...**")
    
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        try:
            chat = await app.get_chat(chat_id)
            title = chat.title
        except Exception:
            title = "☠️ Dᴇᴀᴅ/Pʀɪᴠᴀᴛᴇ Zᴏɴᴇ"
            
        j = 1
        text += f"**{count}. {title}** [`{chat_id}`]\n"
        
    if j == 0:
        await status.edit_text("<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, ɴᴏ ᴄʜᴀᴛs ᴀʀᴇ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ʏᴇᴛ!**")
    else:
        text += f"\n<emoji id=5354924568492383911>😈</emoji> **Pᴏᴡᴇʀᴇᴅ ʙʏ » {app.name}**"
        await status.edit_text(text)

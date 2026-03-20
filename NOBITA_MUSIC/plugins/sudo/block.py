from pyrogram import filters
from pyrogram.types import Message

from NOBITA_MUSIC import app
from NOBITA_MUSIC.misc import SUDOERS
from NOBITA_MUSIC.utils.database import add_gban_user, remove_gban_user
from NOBITA_MUSIC.utils.extraction import extract_user
from config import BANNED_USERS

# ==========================================
# ☠️ ANU X4 BLOCK / UNBLOCK PROTOCOL ☠️
# ==========================================

@app.on_message(filters.command("block") & SUDOERS)
async def premium_useradd(client, message: Message):
    usage = "<emoji id=6123040393769521180>☄️</emoji> **Aɴᴜ X4 Bʟᴏᴄᴋ Pʀᴏᴛᴏᴄᴏʟ**\n<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ:** `/block [Rᴇᴘʟʏ / Usᴇʀɴᴀᴍᴇ / ID]`"
    
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(usage)
            
    # ☠️ EXTRACTION WITH ERROR HANDLING ☠️
    try:
        user = await extract_user(message)
    except Exception:
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Uɴᴀʙʟᴇ ᴛᴏ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ!**")

    if user.id in BANNED_USERS:
        return await message.reply_text(f"<emoji id=5354924568492383911>😈</emoji> **Bᴏss, {user.mention} ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ ᴍʏ ʙʟᴀᴄᴋʟɪsᴛ!**")
        
    await add_gban_user(user.id)
    BANNED_USERS.add(user.id)
    
    # 💎 ULTRA PREMIUM BAN UI 💎
    text = f"""
<emoji id=6111742817304841054>✅</emoji> **Bʟᴏᴄᴋ Pʀᴏᴛᴏᴄᴏʟ Exᴇᴄᴜᴛᴇᴅ!**

<emoji id=6307750079423845494>👑</emoji> **Uɴғᴏʀᴛᴜɴᴀᴛᴇ Usᴇʀ :** {user.mention}
<emoji id=5256131095094652290>⏱️</emoji> **Sᴛᴀᴛᴜs :** `Bʟᴏᴄᴋᴇᴅ Fʀᴏᴍ Aɴᴜ X4`
<emoji id=6152142357727811958>✨</emoji> **Rᴇᴀsᴏɴ :** Oᴜᴋᴀᴀᴛ ʙʜᴜʟ ɢᴀʏᴀ ᴛʜᴀ ʙᴀʙʏ ᴋᴇ sᴀᴀᴍɴᴇ!

<emoji id=5354924568492383911>😈</emoji> **Aᴄᴛɪᴏɴ Bʏ :** {message.from_user.mention}
"""
    await message.reply_text(text)


@app.on_message(filters.command("unblock") & SUDOERS)
async def premium_userdel(client, message: Message):
    usage = "<emoji id=6123040393769521180>☄️</emoji> **Aɴᴜ X4 Uɴʙʟᴏᴄᴋ Pʀᴏᴛᴏᴄᴏʟ**\n<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ:** `/unblock [Rᴇᴘʟʏ / Usᴇʀɴᴀᴍᴇ / ID]`"
    
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(usage)
            
    try:
        user = await extract_user(message)
    except Exception:
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Uɴᴀʙʟᴇ ᴛᴏ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ!**")

    if user.id not in BANNED_USERS:
        return await message.reply_text(f"<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, {user.mention} ɪs ɴᴏᴛ ɪɴ ᴏᴜʀ ʙʟᴀᴄᴋʟɪsᴛ!**")
        
    await remove_gban_user(user.id)
    BANNED_USERS.remove(user.id)
    
    # 💎 ULTRA PREMIUM UNBAN UI 💎
    text = f"""
<emoji id=6111742817304841054>✅</emoji> **Uɴʙʟᴏᴄᴋ Pʀᴏᴛᴏᴄᴏʟ Exᴇᴄᴜᴛᴇᴅ!**

<emoji id=6307750079423845494>👑</emoji> **Lᴜᴄᴋʏ Usᴇʀ :** {user.mention}
<emoji id=5256131095094652290>⏱️</emoji> **Sᴛᴀᴛᴜs :** `Fʀᴇᴇᴅ Fʀᴏᴍ Aɴᴜ X4 Jᴀɪʟ`
<emoji id=6152142357727811958>✨</emoji> **Wᴀʀɴɪɴɢ :** Fɪʀ sᴇ ᴜɴɢʟɪ ᴍᴀᴛ ᴋᴀʀɴᴀ!

<emoji id=5354924568492383911>😈</emoji> **Aᴄᴛɪᴏɴ Bʏ :** {message.from_user.mention}
"""
    await message.reply_text(text)


@app.on_message(filters.command(["blocklist", "blocked", "gbanlist"]) & SUDOERS)
async def premium_sudoers_list(client, message: Message):
    if not BANNED_USERS:
        return await message.reply_text("<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, ɴᴏ ᴏɴᴇ ɪs ʙʟᴏᴄᴋᴇᴅ ʏᴇᴛ! Yᴏᴜʀ ᴇᴍᴘɪʀᴇ ɪs ᴘᴇᴀᴄᴇғᴜʟ.**")
        
    # ☠️ FAKE LOADING FOR HACKER FEEL ☠️
    mystic = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Fᴇᴛᴄʜɪɴɢ Aɴᴜ X4 Pʀɪsᴏɴᴇʀs Lɪsᴛ...**")
    
    msg = "<emoji id=5354924568492383911>😈</emoji> **Aɴᴜ X4 Dɪɢɪᴛᴀʟ Jᴀɪʟ:**\n\n"
    count = 0
    
    for users in BANNED_USERS:
        try:
            user = await app.get_users(users)
            mention = user.mention if hasattr(user, "mention") else user.first_name
            count += 1
        except Exception:
            continue
        msg += f"**{count}.** {mention} [`{users}`]\n"
        
    if count == 0:
        return await mystic.edit_text("<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, ɴᴏ ᴏɴᴇ ɪs ʙʟᴏᴄᴋᴇᴅ ʏᴇᴛ!**")
    else:
        msg += f"\n<emoji id=6152142357727811958>✨</emoji> **Tᴏᴛᴀʟ Pʀɪsᴏɴᴇʀs : {count}**"
        return await mystic.edit_text(msg)

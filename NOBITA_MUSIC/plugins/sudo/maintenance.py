from pyrogram import filters
from pyrogram.types import Message

from NOBITA_MUSIC import app
from NOBITA_MUSIC.misc import SUDOERS
from NOBITA_MUSIC.utils.database import (
    is_maintenance,
    maintenance_off,
    maintenance_on,
)

# ==========================================
# ☠️ ANU MATRIX MAINTENANCE PROTOCOL ☠️
# ==========================================

@app.on_message(filters.command(["maintenance", "maint"]) & SUDOERS)
async def premium_maintenance(client, message: Message):
    usage = "<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ:** `/maintenance [on | off]`"
    
    if len(message.command) != 2:
        return await message.reply_text(usage)
        
    state = message.text.split(None, 1)[1].strip().lower()
    
    # Check current system status from Database
    current_state = await is_maintenance()
    
    # ☠️ STATE: ENABLE / ON (LOCKDOWN) ☠️
    if state in ["enable", "on", "true"]:
        if current_state:
            return await message.reply_text("<emoji id=5354924568492383911>😈</emoji> **Bᴏss, Sʏsᴛᴇᴍ Mᴀɪɴᴛᴇɴᴀɴᴄᴇ ɪs ᴀʟʀᴇᴀᴅʏ Aᴄᴛɪᴠᴇ!**")
        
        await maintenance_on()
        text = f"""
<emoji id=6111742817304841054>✅</emoji> **Mᴀɪɴᴛᴇɴᴀɴᴄᴇ Pʀᴏᴛᴏᴄᴏʟ Eɴᴀʙʟᴇᴅ!**

<emoji id=6152142357727811958>✨</emoji> **Sᴛᴀᴛᴜs :** `Oғғʟɪɴᴇ ᴛᴏ Pᴜʙʟɪᴄ`
<emoji id=5256131095094652290>⏱️</emoji> **Aᴄᴛɪᴏɴ :** Nᴏʀᴍᴀʟ ᴜsᴇʀs ᴄᴀɴ'ᴛ ᴜsᴇ {app.mention} ɴᴏᴡ. Oɴʟʏ Sᴜᴅᴏᴇʀs ᴄᴀɴ!

<emoji id=6307750079423845494>👑</emoji> **Aᴄᴛɪᴏɴ Bʏ :** {message.from_user.mention}
"""
        await message.reply_text(text)
        
    # ☠️ STATE: DISABLE / OFF (PUBLIC MODE) ☠️
    elif state in ["disable", "off", "false"]:
        if not current_state:
            return await message.reply_text("<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, Sʏsᴛᴇᴍ ɪs ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ ɴᴏʀᴍᴀʟʟʏ!**")
            
        await maintenance_off()
        text = f"""
<emoji id=6307821174017496029>❌</emoji> **Mᴀɪɴᴛᴇɴᴀɴᴄᴇ Pʀᴏᴛᴏᴄᴏʟ Dɪsᴀʙʟᴇᴅ!**

<emoji id=6152142357727811958>✨</emoji> **Sᴛᴀᴛᴜs :** `Oɴʟɪɴᴇ ᴛᴏ Pᴜʙʟɪᴄ`
<emoji id=4929369656797431200>🪐</emoji> **Aᴄᴛɪᴏɴ :** {app.mention} ɪs ɴᴏᴡ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴇᴠᴇʀʏᴏɴᴇ ʙᴀʙʏ!

<emoji id=6307750079423845494>👑</emoji> **Aᴄᴛɪᴏɴ Bʏ :** {message.from_user.mention}
"""
        await message.reply_text(text)
        
    else:
        await message.reply_text(usage)

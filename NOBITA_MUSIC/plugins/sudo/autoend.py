from pyrogram import filters
from pyrogram.types import Message

from NOBITA_MUSIC import app
from NOBITA_MUSIC.misc import SUDOERS
from NOBITA_MUSIC.utils.database import autoend_off, autoend_on

# ==========================================
# ☠️ PREMIUM AUTO-END PROTOCOL ☠️
# ==========================================
@app.on_message(filters.command("autoend") & SUDOERS)
async def premium_auto_end_stream(_, message: Message):
    # 💎 ADVANCED USAGE MENU 💎
    usage = """
<emoji id=6123040393769521180>☄️</emoji> **Aᴜᴛᴏ-Eɴᴅ Sᴇʀᴠᴇʀ Pʀᴏᴛᴏᴄᴏʟ** <emoji id=6123040393769521180>☄️</emoji>

<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ :** `/autoend [enable | disable]`
<emoji id=5354924568492383911>😈</emoji> **Aʟᴛ :** `/autoend [on | off]`

<emoji id=6152142357727811958>✨</emoji> **Nᴏᴛᴇ:** Eɴᴀʙʟɪɴɢ ᴛʜɪs ᴡɪʟʟ sᴀᴠᴇ ʏᴏᴜʀ sᴇʀᴠᴇʀ Rᴀᴍ/CPU ʙʏ ᴀᴜᴛᴏ-ʟᴇᴀᴠɪɴɢ ᴇᴍᴘᴛʏ VCs!
"""

    if len(message.command) != 2:
        return await message.reply_text(usage)
        
    state = message.text.split(None, 1)[1].strip().lower()
    
    # ☠️ STATE: ENABLE / ON ☠️
    if state in ["enable", "on", "true"]:
        await autoend_on()
        text = f"""
<emoji id=6111742817304841054>✅</emoji> **Aᴜᴛᴏ-Eɴᴅ Pʀᴏᴛᴏᴄᴏʟ Aᴄᴛɪᴠᴀᴛᴇᴅ!**

<emoji id=6152142357727811958>✨</emoji> **Sᴛᴀᴛᴜs :** `Eɴᴀʙʟᴇᴅ`
<emoji id=5256131095094652290>⏱️</emoji> **Aᴄᴛɪᴏɴ :** Asꜱɪsᴛᴀɴᴛ ᴡɪʟʟ ɴᴏᴡ ᴀᴜᴛᴏ-ʟᴇᴀᴠᴇ ᴇᴍᴘᴛʏ VCs.
<emoji id=6307346833534359338>🍷</emoji> **Bᴇɴᴇғɪᴛ :** Sᴀᴠɪɴɢ Sᴇʀᴠᴇʀ Rᴀᴍ & CPU Mᴀsᴛᴇʀ!

<emoji id=6307750079423845494>👑</emoji> **Aᴄᴛɪᴏɴ Bʏ:** {message.from_user.mention}
"""
        await message.reply_text(text)
        
    # ☠️ STATE: DISABLE / OFF ☠️
    elif state in ["disable", "off", "false"]:
        await autoend_off()
        text = f"""
<emoji id=6307821174017496029>❌</emoji> **Aᴜᴛᴏ-Eɴᴅ Pʀᴏᴛᴏᴄᴏʟ Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ!**

<emoji id=6152142357727811958>✨</emoji> **Sᴛᴀᴛᴜs :** `Dɪsᴀʙʟᴇᴅ`
<emoji id=5256131095094652290>⏱️</emoji> **Aᴄᴛɪᴏɴ :** Asꜱɪsᴛᴀɴᴛ ᴡɪʟʟ sᴛᴀʏ ɪɴ VC 24x7 ᴇᴠᴇɴ ɪғ ɪᴛ's ᴇᴍᴘᴛʏ.
<emoji id=4929369656797431200>🪐</emoji> **Wᴀʀɴɪɴɢ :** Tʜɪs ᴍɪɢʜᴛ ᴄᴏɴsᴜᴍᴇ ᴍᴏʀᴇ Sᴇʀᴠᴇʀ CPU ʙᴀʙʏ!

<emoji id=6307750079423845494>👑</emoji> **Aᴄᴛɪᴏɴ Bʏ:** {message.from_user.mention}
"""
        await message.reply_text(text)
        
    else:
        await message.reply_text(usage)

import os
from pyrogram import filters
from pyrogram.types import Message

from NOBITA_MUSIC import app
from NOBITA_MUSIC.misc import SUDOERS
from NOBITA_MUSIC.utils.database import add_off, add_on

# ==========================================
# ☠️ ANU MATRIX LOGGER & COOKIES PROTOCOL ☠️
# ==========================================

@app.on_message(filters.command(["logger", "log"]) & SUDOERS)
async def premium_logger(client, message: Message):
    usage = "<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ :** `/logger [on | off]`"
    
    if len(message.command) != 2:
        return await message.reply_text(usage)
        
    state = message.text.split(None, 1)[1].strip().lower()
    
    # ☠️ ENABLE / ON ☠️
    if state in ["enable", "on", "true"]:
        await add_on(2)
        text = """
<emoji id=6111742817304841054>✅</emoji> **Lᴏɢɢᴇʀ Pʀᴏᴛᴏᴄᴏʟ Aᴄᴛɪᴠᴀᴛᴇᴅ!**
<emoji id=6152142357727811958>✨</emoji> **Bᴏss, I ᴡɪʟʟ ɴᴏᴡ sᴇɴᴅ ᴀʟʟ sᴇᴀʀᴄʜ/ᴘʟᴀʏ ʟᴏɢs ᴛᴏ ᴛʜᴇ ʟᴏɢ ɢʀᴏᴜᴘ.**
"""
        await message.reply_text(text)
        
    # ☠️ DISABLE / OFF ☠️
    elif state in ["disable", "off", "false"]:
        await add_off(2)
        text = """
<emoji id=6307821174017496029>❌</emoji> **Lᴏɢɢᴇʀ Pʀᴏᴛᴏᴄᴏʟ Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ!**
<emoji id=5256131095094652290>⏱️</emoji> **Lᴏɢs sᴇɴᴅɪɴɢ ʜᴀs ʙᴇᴇɴ sᴛᴏᴘᴘᴇᴅ sᴇᴄʀᴇᴛʟʏ.**
"""
        await message.reply_text(text)
        
    else:
        await message.reply_text(usage)


@app.on_message(filters.command(["cookies"]) & SUDOERS)
async def get_cookies_log(client, message: Message):
    file_path = "cookies/logs.csv"
    
    # ☠️ CRASH PROTECTION (Check if file exists before sending) ☠️
    if os.path.exists(file_path):
        mystic = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Eхᴛʀᴀᴄᴛɪɴɢ ᴄᴏᴏᴋɪᴇs ʟᴏɢs ғʀᴏᴍ Sᴇʀᴠᴇʀ...**")
        
        await message.reply_document(
            document=file_path,
            caption="<emoji id=5354924568492383911>😈</emoji> **Aɴᴜ Mᴀᴛʀɪx Cᴏᴏᴋɪᴇs & Lᴏɢs Dᴀᴛᴀ!**\n<emoji id=6152142357727811958>✨</emoji> **Bᴏss, ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴀᴛᴛᴀᴄʜᴇᴅ ғɪʟᴇ ʙᴇʟᴏᴡ.**"
        )
        await mystic.delete()
    else:
        await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Bᴏss, Cᴏᴏᴋɪᴇs Lᴏɢ ғɪʟᴇ (logs.csv) ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴛʜᴇ Sᴇʀᴠᴇʀ!**")

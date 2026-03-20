from pyrogram import filters
from pyrogram.types import Message
from gpytranslate import Translator

from NOBITA_MUSIC import app

# ==========================================
# ☠️ ANU MATRIX PREMIUM TRANSLATOR ☠️
# ==========================================

trans = Translator()

@app.on_message(filters.command(["tr", "translate"]))
async def premium_translate(client, message: Message):
    reply_msg = message.reply_to_message
    
    # ☠️ CRASH PROTECTION: Check if replied
    if not reply_msg:
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Bᴏss, Rᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʀᴀɴsʟᴀᴛᴇ ɪᴛ!**")
        
    # ☠️ CRASH PROTECTION: Safe Text Extraction
    to_translate = reply_msg.text or reply_msg.caption
    if not to_translate:
        return await message.reply_text("<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, Tʜᴇʀᴇ ɪs ɴᴏ ᴛᴇxᴛ ɪɴ ᴛʜᴀᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʀᴀɴsʟᴀᴛᴇ!**")

    mystic = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Bʀᴇᴀᴋɪɴɢ Lᴀɴɢᴜᴀɢᴇ Bᴀʀʀɪᴇʀs...**")

    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        # 💎 SMART LOGIC: Default to Hindi if English, else Default to English 💎
        dest = "hi" if source == "en" else "en"

    # ☠️ API CRASH PROTECTOR ☠️
    try:
        translation = await trans(to_translate, sourcelang=source, targetlang=dest)
        
        # 💎 PREMIUM MATRIX UI 💎
        reply_text = f"""
<emoji id=5354924568492383911>😈</emoji> **A N U  M A T R I X  T R A N S L A T E**
━━━━━━━━━━━━━━━━━━━━
<emoji id=4929369656797431200>🪐</emoji> **Sᴏᴜʀᴄᴇ:** `{source}`
<emoji id=6307750079423845494>👑</emoji> **Tᴀʀɢᴇᴛ:** `{dest}`

<emoji id=6152142357727811958>✨</emoji> **Tʀᴀɴsʟᴀᴛɪᴏɴ :**
{translation.text}
━━━━━━━━━━━━━━━━━━━━
<emoji id=6111742817304841054>✅</emoji> **Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** {message.from_user.mention}
"""
        await mystic.edit_text(reply_text)
        
    except Exception as e:
        await mystic.edit_text(f"<emoji id=6307821174017496029>❌</emoji> **Tʀᴀɴsʟᴀᴛɪᴏɴ Fᴀɪʟᴇᴅ!**\n<emoji id=5256131095094652290>⏱️</emoji> `API Mɪɢʜᴛ ʙᴇ ᴅᴏᴡɴ.`\n\n`Eʀʀᴏʀ: {e}`")


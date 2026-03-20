import re
import aiohttp
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from NOBITA_MUSIC import app
from config import BOT_USERNAME

# ==========================================
# ☠️ ANU MATRIX VC (VOICE CHAT) PROTOCOL ☠️
# ==========================================

@app.on_message(filters.video_chat_started)
async def premium_vc_started(client, message: Message):
    text = f"""
<emoji id=5354924568492383911>😈</emoji> **A N U  M A T R I X  V C  S Y S T E M**
━━━━━━━━━━━━━━━━━━━━
<emoji id=6111742817304841054>✅</emoji> **Sᴛᴀᴛᴜs :** `Vɪᴅᴇᴏ/Vᴏɪᴄᴇ Cʜᴀᴛ Sᴛᴀʀᴛᴇᴅ!`
<emoji id=4929369656797431200>🪐</emoji> **Cʜᴀᴛ :** {message.chat.title}
━━━━━━━━━━━━━━━━━━━━
"""
    await message.reply_text(text)


@app.on_message(filters.video_chat_ended)
async def premium_vc_ended(client, message: Message):
    text = f"""
<emoji id=6307821174017496029>❌</emoji> **A N U  M A T R I X  V C  S Y S T E M**
━━━━━━━━━━━━━━━━━━━━
<emoji id=5256131095094652290>⏱️</emoji> **Sᴛᴀᴛᴜs :** `Vɪᴅᴇᴏ/Vᴏɪᴄᴇ Cʜᴀᴛ Eɴᴅᴇᴅ!`
<emoji id=4929369656797431200>🪐</emoji> **Cʜᴀᴛ :** {message.chat.title}
━━━━━━━━━━━━━━━━━━━━
"""
    await message.reply_text(text)


@app.on_message(filters.video_chat_members_invited)
async def premium_vc_invited(client, message: Message):
    text = f"<emoji id=6123040393769521180>☄️</emoji> **{message.from_user.mention} ɪs ɪɴᴠɪᴛɪɴɢ ᴍᴇᴍʙᴇʀs ᴛᴏ VC!**\n\n<emoji id=6152142357727811958>✨</emoji> **Iɴᴠɪᴛᴇᴅ Usᴇʀs :**\n"
    
    for user in message.video_chat_members_invited.users:
        text += f"➻ [{user.first_name}](tg://user?id={user.id})\n"

    add_link = f"https://t.me/{BOT_USERNAME}?startgroup=true"
    
    await message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎧 Jᴏɪɴ Vᴏɪᴄᴇ Cʜᴀᴛ 🎧", url=add_link)]
        ]),
    )


# ==========================================
# ☠️ ANU MATRIX SAFE MATH CALCULATOR ☠️
# ==========================================

@app.on_message(filters.command(["math", "calc"]))
async def premium_math(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ:** `/math [Eхᴘʀᴇssɪᴏɴ]`\n<emoji id=6152142357727811958>✨</emoji> **Eхᴀᴍᴘʟᴇ:** `/math 2+2*4`")
        
    expression = message.text.split(None, 1)[1]
    
    # ☠️ HACKER SHIELD: Only allow numbers and basic math symbols (No Alphabets allowed)
    if not re.match(r'^[0-9+\-*/().\s]+$', expression):
        return await message.reply_text("<emoji id=6307821174017496029>💀</emoji> **Nɪᴄᴇ Tʀʏ Hᴀᴄᴋᴇʀ! Oɴʟʏ Mᴀᴛʜ Nᴜᴍʙᴇʀs Aʟʟᴏᴡᴇᴅ.**")
        
    try:
        # Safe evaluation with no built-ins
        result = eval(expression, {"__builtins__": None}, {})
        text = f"""
<emoji id=5354924568492383911>😈</emoji> **A N U  M A T R I X  C A L C**
━━━━━━━━━━━━━━━━━━━━
<emoji id=6307605493644793241>📒</emoji> **Qᴜᴇʀʏ:** `{expression}`
<emoji id=6111742817304841054>✅</emoji> **Rᴇsᴜʟᴛ:** `{result}`
━━━━━━━━━━━━━━━━━━━━
"""
        await message.reply_text(text)
    except Exception:
        await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Iɴᴠᴀʟɪᴅ Mᴀᴛʜ Eхᴘʀᴇssɪᴏɴ!**")


# ==========================================
# 💎 PREMIUM GOOGLE SEARCH ENGINE 💎
# ==========================================

@app.on_message(filters.command(["spg", "search"]))
async def premium_search(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ:** `/search [Qᴜᴇʀʏ]`")

    query = message.text.split(None, 1)[1]
    mystic = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Sᴇᴀʀᴄʜɪɴɢ ᴏɴ Gᴏᴏɢʟᴇ...**")
    
    # ⚠️ Boss, Put your Google API Key below carefully! (Don't share it)
    GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY_HERE" 
    CX = "ec8db9e1f9e41e65e"
    
    url = f"https://content-customsearch.googleapis.com/customsearch/v1?cx={CX}&q={query}&key={GOOGLE_API_KEY}&start=1"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"x-referer": "https://explorer.apis.google.com"}) as r:
                response = await r.json()
                
                if not response.get("items"):
                    return await mystic.edit_text(f"<emoji id=5256131095094652290>⏱️</emoji> **Nᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ ғᴏʀ:** `{query}`")
                    
                result_text = f"<emoji id=6123040393769521180>☄️</emoji> **Gᴏᴏɢʟᴇ Sᴇᴀʀᴄʜ Rᴇsᴜʟᴛs**\n\n"
                
                count = 1
                for item in response["items"][:5]: # Top 5 results only to avoid clutter
                    title = item["title"]
                    link = item["link"]
                    result_text += f"**{count}.** [{title}]({link})\n"
                    count += 1
                    
                result_text += f"\n<emoji id=6307750079423845494>👑</emoji> **Rᴇǫᴜᴇsᴛᴇᴅ Bʏ:** {message.from_user.mention}"
                
                # ☠️ Pyrogram Keyboard (Not Telethon!)
                markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔍 Mᴏʀᴇ Rᴇsᴜʟᴛs", url=f"https://www.google.com/search?q={query.replace(' ', '+')}")]])
                
                await mystic.edit_text(result_text, reply_markup=markup, disable_web_page_preview=True)
                
    except Exception as e:
        await mystic.edit_text(f"<emoji id=6307821174017496029>❌</emoji> **Sᴇᴀʀᴄʜ Fᴀɪʟᴇᴅ!**\n`{e}`")

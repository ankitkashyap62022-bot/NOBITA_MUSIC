import random
import asyncio
import aiohttp
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from NOBITA_MUSIC import app 

SUPPORT_CHAT = "NOB1TA_SUPPORT"
CUTIE = "https://64.media.tumblr.com/d701f53eb5681e87a957a547980371d2/tumblr_nbjmdrQyje1qa94xto1_500.gif"

# ==========================================
# ☠️ ANU MATRIX ASYNC GIF MATCHER ☠️
# ==========================================
async def get_anime_gif():
    # 💎 ASYNC HTTP REQUEST (NO BOT FREEZE!) 💎
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://nekos.best/api/v2/happy") as resp:
                data = await resp.json()
                return data["results"][0]['url']
    except Exception:
        # Fallback GIF if API is down
        return "https://media.tenor.com/bCZIjhJVyFsAAAAC/cat-stare.gif"


# ==========================================
# ☠️ ANU MATRIX PREMIUM WISH ENGINE ☠️
# ==========================================
@app.on_message(filters.command(["wish", "iwish"]))
async def premium_wish(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("<emoji id=4929369656797431200>🪐</emoji> **Bᴀʙʏ, ᴛᴇʟʟ ᴍᴇ ʏᴏᴜʀ ᴡɪsʜ!**\n✨ **Exᴀᴍᴘʟᴇ:** `/wish I ᴡᴀɴᴛ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ`")

    mystic = await m.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Cᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ᴛʜᴇ Sᴛᴀʀs...**")

    text = m.text.split(None, 1)[1]
    wish_count = random.randint(1, 100)
    url = await get_anime_gif()

    # 💎 DYNAMIC ROMANTIC RESPONSES 💎
    if wish_count <= 30:
        remark = "💔 **Tᴏᴜɢʜ ʟᴜᴄᴋ ʙᴀʙʏ, ʙᴜᴛ ᴍɪʀᴀᴄʟᴇs ᴅᴏ ʜᴀᴘᴘᴇɴ!**"
    elif wish_count <= 70:
        remark = "❤️‍🩹 **Tʜᴇ sᴛᴀʀs ᴀʀᴇ ᴀʟɪɢɴɪɴɢ... Kᴇᴇᴘ ʜᴏᴘɪɴɢ!**"
    else:
        remark = "💖 **Yᴏᴜʀ ᴡɪsʜ ɪs ᴍʏ ᴄᴏᴍᴍᴀɴᴅ! Gʀᴀɴᴛᴇᴅ sᴏᴏɴ.**"

    wish_text = f"""
<emoji id=5361877607732230009>💘</emoji> **Aɴᴜ Mᴀᴛʀɪx Mᴀɢɪᴄ ᴡɪsʜ** <emoji id=5361877607732230009>💘</emoji>

<emoji id=5854743260840596378>👤</emoji> **Wɪsʜᴇʀ:** {m.from_user.mention}
<emoji id=6123040393769521180>☄️</emoji> **Wɪsʜ:** `{text}`

<emoji id=6307358404176254008>🔥</emoji> **Pʀᴏʙᴀʙɪʟɪᴛʏ:** **{wish_count}%**
{remark}
"""
    try:
        await m.reply_animation(
            animation=url,
            caption=wish_text,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✨ Sᴜᴘᴘᴏʀᴛ ✨", url=f"https://t.me/{SUPPORT_CHAT}")]]),
            reply_to_message_id=m.id
        )
        await mystic.delete()
    except Exception as e:
        await mystic.edit_text(f"❌ **Eʀʀᴏʀ Dᴇᴛᴇᴄᴛᴇᴅ!**\n`{e}`")


# ==========================================
# ☠️ ANU MATRIX PREMIUM CUTENESS METER ☠️
# ==========================================
@app.on_message(filters.command(["cute", "cuteness"]))
async def premium_cute(_, m: Message):
    # Smart Target Detection
    target = m.reply_to_message.from_user if m.reply_to_message else m.from_user
    
    mystic = await m.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Sᴄᴀɴɴɪɴɢ Cᴜᴛᴇɴᴇss Lᴇᴠᴇʟs...**")
    await asyncio.sleep(0.5)

    mm = random.randint(1, 100)

    # 💎 DYNAMIC ROMANTIC RESPONSES 💎
    if mm <= 30:
        remark = "😐 **Yᴏᴜ ʜᴀᴠᴇ ᴀ ʜɪᴅᴅᴇɴ ᴄʜᴀʀᴍ, ᴊᴜsᴛ ᴠᴇʀʏ... ʜɪᴅᴅᴇɴ.**"
    elif mm <= 70:
        remark = "🥰 **Aᴡᴡ! Pʀᴇᴛᴛʏ ᴅᴀᴍɴ ᴄᴜᴛᴇ, I ᴍᴜsᴛ sᴀʏ.**"
    else:
        remark = "🥵 **Iʟʟᴇɢᴀʟ ʟᴇᴠᴇʟs ᴏғ ᴄᴜᴛᴇɴᴇss! Aʀʀᴇsᴛ ᴛʜɪs ᴘᴇʀsᴏɴ!**"

    cute_text = f"""
<emoji id=5314782352226958463>💖</emoji> **Aɴᴜ Mᴀᴛʀɪx Cᴜᴛᴇɴᴇss Mᴇᴛᴇʀ** <emoji id=5314782352226958463>💖</emoji>

<emoji id=5854743260840596378>👤</emoji> **Tᴀʀɢᴇᴛ:** {target.mention}
<emoji id=6307358404176254008>🔥</emoji> **Cᴜᴛᴇɴᴇss:** **{mm}%**

{remark}
"""
    try:
        await m.reply_document(
            document=CUTIE,
            caption=cute_text,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✨ Sᴜᴘᴘᴏʀᴛ ✨", url=f"https://t.me/{SUPPORT_CHAT}")]]),
            reply_to_message_id=m.reply_to_message.id if m.reply_to_message else m.id
        )
        await mystic.delete()
    except Exception as e:
        await mystic.edit_text(f"❌ **Eʀʀᴏʀ Dᴇᴛᴇᴄᴛᴇᴅ!**\n`{e}`")

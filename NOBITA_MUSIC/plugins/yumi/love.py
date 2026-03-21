import asyncio
import hashlib
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import MessageNotModified

from NOBITA_MUSIC import app

# ==========================================
# ☠️ ANU MATRIX PREMIUM SOULMATE ENGINE ☠️
# ==========================================

def get_premium_message(love_percentage):
    if love_percentage <= 30:
        return [
            "<emoji id=5260342787882103328>💔</emoji> **Aʟᴇʀᴛ! Fʀɪᴇɴᴅᴢᴏɴᴇ ᴅᴇᴛᴇᴄᴛᴇᴅ! Mᴏᴠᴇ ᴏɴ ʙᴏss.**",
            "<emoji id=5260342787882103328>💔</emoji> **Nᴀʜ, ɴᴏᴛ ᴍᴇᴀɴᴛ ᴛᴏ ʙᴇ. Sᴀᴠᴇ ʏᴏᴜʀ ᴛᴇᴀʀs!**",
            "<emoji id=5260342787882103328>💔</emoji> **Oᴜᴄʜ! Tʜᴀᴛ's ᴀ ᴅɪsᴀsᴛᴇʀ ᴡᴀɪᴛɪɴɢ ᴛᴏ ʜᴀᴘᴘᴇɴ!**"
        ]
    elif love_percentage <= 60:
        return [
            "<emoji id=5328250499642698740>❤️‍🩹</emoji> **Gᴏᴏᴅ sᴛᴀʀᴛ! Iᴛ ɴᴇᴇᴅs ᴀ ʟɪᴛᴛʟᴇ ᴍᴏʀᴇ ᴍᴀɢɪᴄ.**",
            "<emoji id=5328250499642698740>❤️‍🩹</emoji> **Tʜᴇʀᴇ ɪs ᴀ ᴄʜᴀɴᴄᴇ... Bᴜᴛ ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴡᴏʀᴋ ʜᴀʀᴅ!**",
            "<emoji id=5328250499642698740>❤️‍🩹</emoji> **50-50 ᴄʜᴀɴᴄᴇ! Lᴇᴛ's ʜᴏᴘᴇ ғᴏʀ ᴛʜᴇ ʙᴇsᴛ!**"
        ]
    elif love_percentage <= 85:
        return [
            "<emoji id=5361877607732230009>💘</emoji> **Wᴏᴡ! Tʜᴇ ᴄʜᴇᴍɪsᴛʀʏ ɪs ᴏɴ ғɪʀᴇ ʙʀᴏ!**",
            "<emoji id=5361877607732230009>💘</emoji> **Sᴛʀᴏɴɢ ᴄᴏɴɴᴇᴄᴛɪᴏɴ! Cʜᴇʀɪsʜ ᴛʜɪs ʙᴏɴᴅ.**",
            "<emoji id=5361877607732230009>💘</emoji> **Lᴏᴏᴋs ʟɪᴋᴇ sᴏᴍᴇᴏɴᴇ ɪs ɪɴ ᴅᴇᴇᴘ ʟᴏᴠᴇ!**"
        ]
    else:
        return [
            "<emoji id=5314782352226958463>💖</emoji> **Pᴇʀғᴇᴄᴛ Mᴀᴛᴄʜ! A ᴍᴀᴛᴄʜ ᴍᴀᴅᴇ ɪɴ ʜᴇᴀᴠᴇɴ!**",
            "<emoji id=5314782352226958463>💖</emoji> **Sᴏᴜʟᴍᴀᴛᴇs ᴅᴇᴛᴇᴄᴛᴇᴅ! Wʜᴇɴ ɪs ᴛʜᴇ ᴡᴇᴅᴅɪɴɢ?**",
            "<emoji id=5314782352226958463>💖</emoji> **Dᴇsᴛɪɴᴇᴅ ᴛᴏ ʙᴇ ᴛᴏɢᴇᴛʜᴇʀ. 100% Pᴜʀᴇ Lᴏᴠᴇ!**"
        ]

@app.on_message(filters.command(["love", "couple", "match"]))
async def premium_love_command(client, message: Message):
    # ☠️ SAFE SPLITTING & ERROR HANDLING ☠️
    if len(message.command) < 3:
        return await message.reply_text("<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ:** `/love [Nᴀᴍᴇ 1] [Nᴀᴍᴇ 2]`\n<emoji id=6152142357727811958>✨</emoji> **Eхᴀᴍᴘʟᴇ:** `/love Nobita Shizuka`")

    name1 = message.command[1].strip()
    name2 = message.command[2].strip()

    # 💎 PREMIUM ANIMATION UI 💎
    mystic = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Sᴄᴀɴɴɪɴɢ Hᴇᴀʀᴛʙᴇᴀᴛs...**")
    await asyncio.sleep(0.5)
    await mystic.edit_text("<emoji id=6123040393769521180>☄️</emoji> **Mᴀᴛᴄʜɪɴɢ Dᴇsᴛɪɴʏ ᴀɴᴅ DNA...**")
    await asyncio.sleep(0.5)

    # ☠️ SOULMATE HASH ALGORITHM (Consistent Results) ☠️
    # Combines names alphabetically so 'Ram Sita' & 'Sita Ram' give the same result
    seed_string = "".join(sorted([name1.lower(), name2.lower()]))
    hash_val = int(hashlib.md5(seed_string.encode()).hexdigest(), 16)
    love_percentage = (hash_val % 91) + 10  # Generates 10 to 100%

    import random
    love_message = random.choice(get_premium_message(love_percentage))

    # 💎 PREMIUM FINAL RESPONSE 💎
    final_text = f"""
<emoji id=5361877607732230009>💘</emoji> **Aɴᴜ Mᴀᴛʀɪx Lᴏᴠᴇ Cᴀʟᴄᴜʟᴀᴛᴏʀ** <emoji id=5361877607732230009>💘</emoji>

<emoji id=5854743260840596378>👦</emoji> **Bᴏʏ:** `{name1}`
<emoji id=5854753555826870233>👧</emoji> **Gɪʀʟ:** `{name2}`

<emoji id=6307358404176254008>🔥</emoji> **Lᴏᴠᴇ Pᴇʀᴄᴇɴᴛᴀɢᴇ:** **{love_percentage}%**

{love_message}
"""
    
    # Adding a cute inline button
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("✨ Tʀʏ Yᴏᴜʀ Mᴀᴛᴄʜ ✨", switch_inline_query_current_chat="")]]
    )

    try:
        await mystic.edit_text(final_text, reply_markup=keyboard)
    except MessageNotModified:
        pass

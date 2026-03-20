import asyncio
from uuid import uuid4

from pyrogram import filters, raw
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BOT_USERNAME
from NOBITA_MUSIC import app

# ==========================================
# ☠️ ANU MATRIX PREMIUM STICKER PROTOCOL ☠️
# ==========================================

@app.on_message(filters.command(["st", "sendsticker"]))
async def premium_generate_sticker(client, message: Message):
    # ☠️ FIXED: Added async and await to prevent bot freeze ☠️
    if len(message.command) == 2:
        sticker_id = message.command[1]
        try:
            await client.send_sticker(message.chat.id, sticker=sticker_id)
        except Exception as e:
            await message.reply_text(f"<emoji id=6307821174017496029>❌</emoji> **Sᴛɪᴄᴋᴇʀ Sᴇɴᴅ Fᴀɪʟᴇᴅ!**\n`{e}`")
    else:
        await message.reply_text("<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ:** `/st [Sᴛɪᴄᴋᴇʀ_ID]`")


@app.on_message(filters.command(["stickerid", "stid"]))
async def premium_sticker_id(client, msg: Message):
    # ☠️ FIXED: Added missing 'return' statements to prevent crash ☠️
    if not msg.reply_to_message or not msg.reply_to_message.sticker:
        return await msg.reply_text("<emoji id=6307821174017496029>❌</emoji> **Bᴏss, Rᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴛᴏ ɢᴇᴛ ɪᴛs ID!**")        
        
    st_in = msg.reply_to_message.sticker
    
    # 💎 PREMIUM MATRIX UI 💎
    text = f"""
<emoji id=5354924568492383911>😈</emoji> **A N U  M A T R I X  S T I C K E R  I N F O**
━━━━━━━━━━━━━━━━━━━━
<emoji id=6123040393769521180>☄️</emoji> **Fɪʟᴇ ID :** `{st_in.file_id}`

<emoji id=5256131095094652290>⏱️</emoji> **Uɴɪǫᴜᴇ ID :** `{st_in.file_unique_id}`
━━━━━━━━━━━━━━━━━━━━
"""
    await msg.reply_text(text)


@app.on_message(filters.command("packkang"))
async def premium_packkang(client, message: Message):  
    txt = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Iɴɪᴛɪᴀʟɪᴢɪɴɢ Pᴀᴄᴋ Cʟᴏɴɪɴɢ...**")
    
    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await txt.edit("<emoji id=6307821174017496029>❌</emoji> **Bᴏss, Rᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴛᴏ ᴄʟᴏɴᴇ ᴛʜᴇ ᴡʜᴏʟᴇ ᴘᴀᴄᴋ!**")
        
    if message.reply_to_message.sticker.is_animated or message.reply_to_message.sticker.is_video:
        return await txt.edit("<emoji id=5256131095094652290>⏱️</emoji> **I ᴄᴀɴ ᴏɴʟʏ ᴄʟᴏɴᴇ Nᴏɴ-Aɴɪᴍᴀᴛᴇᴅ sᴛɪᴄᴋᴇʀs ғᴏʀ ɴᴏᴡ ʙᴀʙʏ!**")
        
    if len(message.command) < 2:
        pack_name = f"{message.from_user.first_name}'s Elite Pack by @{BOT_USERNAME}"
    else:
        pack_name = message.text.split(maxsplit=1)[1]
        
    short_name = message.reply_to_message.sticker.set_name
    if not short_name:
        return await txt.edit("<emoji id=6307821174017496029>❌</emoji> **Tʜɪs sᴛɪᴄᴋᴇʀ ᴅᴏᴇsɴ'ᴛ ʙᴇʟᴏɴɢ ᴛᴏ ᴀɴʏ ᴘᴀᴄᴋ!**")

    await txt.edit("<emoji id=6123040393769521180>☄️</emoji> **Fᴇᴛᴄʜɪɴɢ Pᴀᴄᴋ Dᴀᴛᴀ Fʀᴏᴍ Tᴇʟᴇɢʀᴀᴍ Sᴇʀᴠᴇʀs...**")
    
    try:
        stickers = await app.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=short_name),
                hash=0
            )
        )
    except Exception as e:
        return await txt.edit(f"<emoji id=6307821174017496029>❌</emoji> **Fᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ sᴛɪᴄᴋᴇʀs!**\n`{e}`")
        
    shits = stickers.documents
    sticks = []
    
    for i in shits:
        sex = raw.types.InputDocument(
            id=i.id,
            access_hash=i.access_hash,
            file_reference=i.thumbs[0].bytes if i.thumbs else b""
        )
        
        # ☠️ FIXED: Smart Emoji Extraction to prevent Array Index Crash ☠️
        emoji = "✨"
        for attr in i.attributes:
            if isinstance(attr, raw.types.DocumentAttributeSticker):
                emoji = attr.alt or "✨"
                break
                
        sticks.append(
            raw.types.InputStickerSetItem(
                document=sex,
                emoji=emoji
            )
        )

    try:
        await txt.edit("<emoji id=6310044717241340733>🔄</emoji> **Cʀᴇᴀᴛɪɴɢ Nᴇᴡ Aɴᴜ Mᴀᴛʀɪx Pᴀᴄᴋ...**")
        
        # ☠️ FIXED: Valid Pack Shortname (Must start with letter) ☠️
        unique_id = str(uuid4().hex)[:10]
        new_short_name = f"a{unique_id}_by_{app.me.username}"
        user_id = await app.resolve_peer(message.from_user.id)
        
        await app.invoke(
            raw.functions.stickers.CreateStickerSet(
                user_id=user_id,
                title=pack_name,
                short_name=new_short_name,
                stickers=sticks,
            )
        )
        
        # 💎 PREMIUM SUCCESS UI 💎
        final_text = f"""
<emoji id=6111742817304841054>✅</emoji> **Pᴀᴄᴋ Cʟᴏɴᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!**

<emoji id=6307750079423845494>👑</emoji> **Pᴀᴄᴋ Nᴀᴍᴇ :** `{pack_name}`
<emoji id=6152142357727811958>✨</emoji> **Tᴏᴛᴀʟ Sᴛɪᴄᴋᴇʀs :** `{len(sticks)}`
<emoji id=5354924568492383911>😈</emoji> **Oᴡɴᴇʀ :** {message.from_user.mention}
"""
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("✨ Aᴅᴅ Cʟᴏɴᴇᴅ Pᴀᴄᴋ ✨", url=f"http://t.me/addstickers/{new_short_name}")]])
        await txt.edit(final_text, reply_markup=keyboard)
        
    except Exception as e:
        await txt.edit(f"<emoji id=6307821174017496029>❌</emoji> **Eʀʀᴏʀ ᴡʜɪʟᴇ ᴄʀᴇᴀᴛɪɴɢ ᴘᴀᴄᴋ:**\n`{e}`")

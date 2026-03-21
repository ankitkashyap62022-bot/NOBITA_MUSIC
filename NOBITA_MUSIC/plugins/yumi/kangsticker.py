import os
import imghdr
import asyncio
from traceback import format_exc

from pyrogram import filters
from pyrogram.errors import (
    PeerIdInvalid, ShortnameOccupyFailed, StickerEmojiInvalid,
    StickerPngDimensions, StickerPngNopng, UserIsBlocked,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from NOBITA_MUSIC import app
from config import BOT_USERNAME
from NOBITA_MUSIC.utils.errors import capture_err

from NOBITA_MUSIC.utils.files import (
    get_document_from_file_id, resize_file_to_sticker_size, upload_document,
)
from NOBITA_MUSIC.utils.stickerset import (
    add_sticker_to_set, create_sticker, create_sticker_set, get_sticker_set_by_name,
)

# ==========================================
# ☠️ ANU MATRIX PREMIUM STICKER ENGINE ☠️
# ==========================================

MAX_STICKERS = 120 
SUPPORTED_TYPES = ["jpeg", "png", "webp"]

@app.on_message(filters.command(["get_sticker", "getsticker", "stickerid"]))
@capture_err
async def premium_sticker_image(_, message: Message):
    reply = message.reply_to_message

    if not reply:
        return await message.reply_text("<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ!**")

    if not reply.sticker:
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Tʜᴀᴛ's ɴᴏᴛ ᴀ sᴛɪᴄᴋᴇʀ!** Rᴇᴘʟʏ ᴛᴏ ᴀ ᴠᴀʟɪᴅ sᴛɪᴄᴋᴇʀ.")

    mystic = await message.reply_text("<emoji id=6123040393769521180>☄️</emoji> **Exᴛʀᴀᴄᴛɪɴɢ sᴛɪᴄᴋᴇʀ ᴅᴀᴛᴀ...**")
    
    # ☠️ Smart Unique ID Generation ☠️
    file_name = f"{reply.sticker.file_unique_id}.png"
    f = await reply.download(file_name)

    caption = f"<emoji id=6307358404176254008>🔥</emoji> **Aɴᴜ Mᴀᴛʀɪx Sᴛɪᴄᴋᴇʀ Eхᴛʀᴀᴄᴛᴏʀ**\n\n<emoji id=5354924568492383911>😈</emoji> **Eᴍᴏᴊɪ:** {reply.sticker.emoji}\n<emoji id=4929369656797431200>🪐</emoji> **Iᴅ:** `{reply.sticker.file_id}`"

    await asyncio.gather(
        message.reply_photo(f, caption=caption),
        message.reply_document(f)
    )

    await mystic.delete()
    # 💎 ASYNC CLEANUP (No Server Freeze) 💎
    if os.path.exists(f):
        await asyncio.to_thread(os.remove, f)


@app.on_message(filters.command(["kang", "steal"]))
@capture_err
async def premium_kang(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ:**\nRᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴏʀ ɪᴍᴀɢᴇ ᴡɪᴛʜ `/kang` ᴛᴏ sᴛᴇᴀʟ ɪᴛ!")
        
    if not message.from_user:
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Aɴᴏɴʏᴍᴏᴜs Aᴅᴍɪɴs ᴄᴀɴ'ᴛ ᴋᴀɴɢ sᴛɪᴄᴋᴇʀs!**")

    msg = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Sᴛᴇᴀʟɪɴɢ Sᴛɪᴄᴋᴇʀ...** Pʟᴇᴀsᴇ ᴡᴀɪᴛ!")

    # ☠️ SMART EMOJI EXTRACTOR ☠️
    args = message.text.split()
    if len(args) > 1:
        sticker_emoji = str(args[1])
    elif message.reply_to_message.sticker and message.reply_to_message.sticker.emoji:
        sticker_emoji = message.reply_to_message.sticker.emoji
    else:
        sticker_emoji = "😈" # Default Premium Emoji

    doc = message.reply_to_message.photo or message.reply_to_message.document
    try:
        if message.reply_to_message.sticker:
            sticker = await create_sticker(
                await get_document_from_file_id(message.reply_to_message.sticker.file_id),
                sticker_emoji,
            )
        elif doc:
            if doc.file_size > 10000000:
                return await msg.edit("<emoji id=6307821174017496029>❌</emoji> **Fɪʟᴇ ɪs ᴛᴏᴏ ʟᴀʀɢᴇ ᴛᴏ ᴋᴀɴɢ!**")

            await msg.edit("<emoji id=6123040393769521180>☄️</emoji> **Dᴏᴡɴʟᴏᴀᴅɪɴɢ ᴀɴᴅ Rᴇsɪᴢɪɴɢ...**")
            temp_file_path = await app.download_media(doc)
            image_type = imghdr.what(temp_file_path)
            
            if image_type not in SUPPORTED_TYPES:
                await asyncio.to_thread(os.remove, temp_file_path)
                return await msg.edit(f"<emoji id=6307821174017496029>❌</emoji> **Fᴏʀᴍᴀᴛ ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ:** `{image_type}`")
                
            try:
                temp_file_path = await resize_file_to_sticker_size(temp_file_path)
            except Exception as e:
                await asyncio.to_thread(os.remove, temp_file_path)
                return await msg.edit(f"<emoji id=6307821174017496029>❌</emoji> **Eʀʀᴏʀ ʀᴇsɪᴢɪɴɢ ɪᴍᴀɢᴇ!**\n`{e}`")

            await msg.edit("<emoji id=6307358404176254008>🔥</emoji> **Uᴘʟᴏᴀᴅɪɴɢ ᴛᴏ Tᴇʟᴇɢʀᴀᴍ...**")
            sticker = await create_sticker(
                await upload_document(client, temp_file_path, message.chat.id),
                sticker_emoji,
            )
            # 💎 ASYNC CLEANUP 💎
            if os.path.exists(temp_file_path):
                await asyncio.to_thread(os.remove, temp_file_path)
                
        else:
            return await msg.edit("<emoji id=6307821174017496029>❌</emoji> **I ᴄᴀɴ ᴏɴʟʏ ᴋᴀɴɢ Sᴛɪᴄᴋᴇʀs ᴏʀ Iᴍᴀɢᴇs!**")
            
    except ShortnameOccupyFailed:
        return await msg.edit("<emoji id=6307821174017496029>❌</emoji> **Cʜᴀɴɢᴇ ʏᴏᴜʀ Fɪʀsᴛ Nᴀᴍᴇ ᴛᴏ ᴋᴀɴɢ!**")
    except Exception as e:
        return await msg.edit(f"<emoji id=6307821174017496029>❌</emoji> **Eʀʀᴏʀ:** `{e}`")

    # ☠️ PREMIUM PACK GENERATOR ☠️
    packnum = 0
    packname = f"f{message.from_user.id}_by_{BOT_USERNAME}"
    limit = 0
    
    try:
        while True:
            if limit >= 50:
                return await msg.delete()

            stickerset = await get_sticker_set_by_name(client, packname)
            if not stickerset:
                stickerset = await create_sticker_set(
                    client,
                    message.from_user.id,
                    f"{message.from_user.first_name[:32]}'s ᴘᴀᴄᴋ ʙʏ @{BOT_USERNAME}",
                    packname,
                    [sticker],
                )
            elif stickerset.set.count >= MAX_STICKERS:
                packnum += 1
                packname = f"f{packnum}_{message.from_user.id}_by_{BOT_USERNAME}"
                limit += 1
                continue
            else:
                try:
                    await add_sticker_to_set(client, stickerset, sticker)
                except StickerEmojiInvalid:
                    return await msg.edit("<emoji id=6307821174017496029>❌</emoji> **Iɴᴠᴀʟɪᴅ Eᴍᴏᴊɪ!**")
            break

        # 💎 PREMIUM INLINE BUTTON RESPONSE 💎
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("✨ Vɪᴇᴡ Yᴏᴜʀ Pᴀᴄᴋ ✨", url=f"t.me/addstickers/{packname}")]]
        )
        await msg.edit(
            f"<emoji id=6111742817304841054>✅</emoji> **Sᴛɪᴄᴋᴇʀ Sᴜᴄᴄᴇssғᴜʟʟʏ Sᴛᴏʟᴇɴ!**\n\n<emoji id=5354924568492383911>😈</emoji> **Eᴍᴏᴊɪ:** {sticker_emoji}\n<emoji id=4929369656797431200>🪐</emoji> **Kᴀɴɢᴇᴅ Bʏ:** {message.from_user.mention}",
            reply_markup=keyboard
        )

    except (PeerIdInvalid, UserIsBlocked):
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("⌯ Sᴛᴀʀᴛ Iɴ PM ⌯", url=f"t.me/{BOT_USERNAME}?start=kang")]]
        )
        await msg.edit(
            "<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, I ɴᴇᴇᴅ ᴛᴏ ᴍᴇssᴀɢᴇ ʏᴏᴜ ɪɴ PM ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴀ ᴘᴀᴄᴋ!**",
            reply_markup=keyboard,
        )
    except StickerPngNopng:
        await msg.edit("<emoji id=6307821174017496029>❌</emoji> **Sᴛɪᴄᴋᴇʀs ᴍᴜsᴛ ʙᴇ ᴠᴀʟɪᴅ PNG ғɪʟᴇs!**")
    except StickerPngDimensions:
        await msg.edit("<emoji id=6307821174017496029>❌</emoji> **Iɴᴠᴀʟɪᴅ PNG ᴅɪᴍᴇɴsɪᴏɴs ᴀғᴛᴇʀ ʀᴇsɪᴢɪɴɢ!**")

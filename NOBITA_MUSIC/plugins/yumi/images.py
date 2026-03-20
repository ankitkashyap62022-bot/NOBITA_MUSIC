import os
import shutil
import asyncio
from re import findall
from bing_image_downloader import downloader
from pyrogram import filters
from pyrogram.types import InputMediaPhoto, Message

from NOBITA_MUSIC import app

# ==========================================
# ☠️ ANU MATRIX PREMIUM IMAGE SEARCH ☠️
# ==========================================

def perform_image_download(query, lim, download_dir):
    # ☠️ Running heavy sync download in background thread ☠️
    downloader.download(query, limit=lim, output_dir=download_dir, adult_filter_off=True, force_replace=False, timeout=60)

@app.on_message(filters.command(["img", "image", "pic"]))
async def premium_google_img_search(client, message: Message):
    chat_id = message.chat.id

    if len(message.command) < 2:
        return await message.reply_text("<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ:** `/img [Qᴜᴇʀʏ]` ᴏʀ `/img [Qᴜᴇʀʏ] lim=5`\n<emoji id=6152142357727811958>✨</emoji> **Eхᴀᴍᴘʟᴇ:** `/img Iron Man lim=4`")

    query = message.text.split(None, 1)[1]

    # ☠️ SMART LIMIT EXTRACTOR ☠️
    lim_match = findall(r"lim=\d+", query)
    lim = 6 # Default Limit
    if lim_match:
        try:
            lim = int(lim_match[0].replace("lim=", ""))
            query = query.replace(lim_match[0], "").strip()
        except:
            pass
            
    # ☠️ ABUSE PROTECTOR (Max 10 Images to prevent server lag)
    if lim > 10:
        lim = 10

    mystic = await message.reply_text(f"<emoji id=6310044717241340733>🔄</emoji> **Sᴇᴀʀᴄʜɪɴɢ ɪᴍᴀɢᴇs ғᴏʀ:** `{query}`...")
    download_dir = "downloads"
    images_dir = os.path.join(download_dir, query)

    try:
        await mystic.edit_text("<emoji id=6123040393769521180>☄️</emoji> **Dᴏᴡɴʟᴏᴀᴅɪɴɢ HD Iᴍᴀɢᴇs...**")
        
        # 💎 ASYNC THREAD EXECUTION (No Bot Freeze!) 💎
        await asyncio.to_thread(perform_image_download, query, lim, download_dir)
        
        if not os.path.exists(images_dir) or not os.listdir(images_dir):
            return await mystic.edit_text(f"<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, I ᴄᴏᴜʟᴅɴ'ᴛ ғɪɴᴅ ᴀɴʏ ɪᴍᴀɢᴇs ғᴏʀ:** `{query}`")
            
        lst = [os.path.join(images_dir, img) for img in os.listdir(images_dir)][:lim]
        
        await mystic.edit_text("<emoji id=6307358404176254008>🔥</emoji> **Uᴘʟᴏᴀᴅɪɴɢ Aʟʙᴜᴍ ᴛᴏ Tᴇʟᴇɢʀᴀᴍ...**")
        
        # 💎 SENDING MEDIA GROUP 💎
        media_group = [InputMediaPhoto(media=img) for img in lst]
        # Adding caption to the first image only
        media_group[0] = InputMediaPhoto(media=lst[0], caption=f"<emoji id=5354924568492383911>😈</emoji> **A N U  M A T R I X  I M A G E S**\n\n<emoji id=4929369656797431200>🪐</emoji> **Qᴜᴇʀʏ:** `{query}`\n<emoji id=6111742817304841054>✅</emoji> **Rᴇǫᴜᴇsᴛᴇᴅ Bʏ:** {message.from_user.mention}")

        await app.send_media_group(
            chat_id=chat_id,
            media=media_group,
            reply_to_message_id=message.id
        )
        await mystic.delete()
        
    except Exception as e:
        await mystic.edit_text(f"<emoji id=6307821174017496029>❌</emoji> **Aɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ!**\n`{e}`")
        
    finally:
        # ☠️ AUTO-CLEANUP STORAGE (Never fills up your server!) ☠️
        if os.path.exists(images_dir):
            try:
                shutil.rmtree(images_dir)
            except:
                pass

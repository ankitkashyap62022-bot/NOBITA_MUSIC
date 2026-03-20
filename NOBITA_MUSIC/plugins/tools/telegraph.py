import os
import aiohttp
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from NOBITA_MUSIC import app

# ==========================================
# ☠️ ANU MATRIX TELEGRAPH / CATBOX UPLOADER ☠️
# ==========================================

async def upload_file_async(file_path):
    # ☠️ PREMIUM ASYNC UPLOAD (No Bot Freezes!) ☠️
    url = "https://catbox.moe/user/api.php"
    data = {"reqtype": "fileupload", "json": "true"}
    
    try:
        async with aiohttp.ClientSession() as session:
            with open(file_path, "rb") as f:
                form = aiohttp.FormData(data)
                form.add_field("fileToUpload", f, filename=os.path.basename(file_path))
                
                async with session.post(url, data=form) as response:
                    if response.status == 200:
                        text = await response.text()
                        return True, text.strip()
                    else:
                        return False, f"Eʀʀᴏʀ: {response.status}"
    except Exception as e:
        return False, str(e)


@app.on_message(filters.command(["tgm", "tgt", "telegraph", "tl", "link"]))
async def premium_get_link_group(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Bᴏss, Rᴇᴘʟʏ ᴛᴏ ᴀ Pʜᴏᴛᴏ ᴏʀ Vɪᴅᴇᴏ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴀ ʟɪɴᴋ!**")

    media = message.reply_to_message
    file_size = 0
    
    if media.photo:
        file_size = media.photo.file_size
    elif media.video:
        file_size = media.video.file_size
    elif media.document:
        file_size = media.document.file_size
    elif media.animation:
        file_size = media.animation.file_size
    else:
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **I ᴄᴀɴ ᴏɴʟʏ ᴜᴘʟᴏᴀᴅ Pʜᴏᴛᴏs, Vɪᴅᴇᴏs ᴀɴᴅ Dᴏᴄᴜᴍᴇɴᴛs!**")

    # ☠️ 200MB LIMIT CHECK ☠️
    if file_size > 200 * 1024 * 1024:
        return await message.reply_text("<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, ғɪʟᴇ ɪs ᴛᴏᴏ ʙɪɢ! Pʟᴇᴀsᴇ sᴇɴᴅ ᴀ ғɪʟᴇ ᴜɴᴅᴇʀ 200MB.**")

    mystic = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Iɴɪᴛɪᴀʟɪᴢɪɴɢ Aɴᴜ Mᴀᴛʀɪx Uᴘʟᴏᴀᴅᴇʀ...**")
    local_path = None

    try:
        async def progress(current, total):
            try:
                percent = current * 100 / total
                # Update message only at certain intervals to avoid FloodWait
                if int(percent) % 20 == 0:
                    await mystic.edit_text(f"<emoji id=6123040393769521180>☄️</emoji> **Dᴏᴡɴʟᴏᴀᴅɪɴɢ Tᴏ Sᴇʀᴠᴇʀ:** `{percent:.1f}%`")
            except Exception:
                pass

        # 💎 DOWNLOADING 💎
        local_path = await media.download(progress=progress)
        
        if not local_path:
            return await mystic.edit_text("<emoji id=6307821174017496029>❌</emoji> **Fᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴍᴇᴅɪᴀ!**")

        await mystic.edit_text("<emoji id=6307358404176254008>🔥</emoji> **Uᴘʟᴏᴀᴅɪɴɢ Tᴏ Cʟᴏᴜᴅ (Cᴀᴛʙᴏx)...**")

        # 💎 UPLOADING (ASYNC) 💎
        success, upload_path = await upload_file_async(local_path)

        if success:
            text = f"""
<emoji id=6111742817304841054>✅</emoji> **Mᴇᴅɪᴀ Uᴘʟᴏᴀᴅᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!**

<emoji id=6152142357727811958>✨</emoji> **Lɪɴᴋ :** `{upload_path}`
<emoji id=5354924568492383911>😈</emoji> **Gᴇɴᴇʀᴀᴛᴇᴅ Bʏ :** {message.from_user.mention}
"""
            markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔗 Oᴘᴇɴ Lɪɴᴋ", url=upload_path)]])
            await mystic.edit_text(text, reply_markup=markup, disable_web_page_preview=True)
        else:
            await mystic.edit_text(f"<emoji id=6307821174017496029>❌</emoji> **Uᴘʟᴏᴀᴅ Fᴀɪʟᴇᴅ!**\n`{upload_path}`")

    except Exception as e:
        await mystic.edit_text(f"<emoji id=6307821174017496029>❌</emoji> **Aɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ:**\n`{e}`")
        
    finally:
        # ☠️ CRASH-PROOF CLEANUP ☠️
        if local_path and os.path.exists(local_path):
            try:
                os.remove(local_path)
            except:
                pass

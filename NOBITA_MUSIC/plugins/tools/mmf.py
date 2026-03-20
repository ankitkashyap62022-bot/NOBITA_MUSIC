import os
import textwrap
import asyncio
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import Message

from NOBITA_MUSIC import app

# ==========================================
# ☠️ ANU MATRIX MEME GENERATOR ☠️
# ==========================================

@app.on_message(filters.command(["mmf", "meme"]))
async def premium_mmf(client, message: Message):
    reply_message = message.reply_to_message

    # ☠️ VALIDATION CHECKS (Crash Protection) ☠️
    if not reply_message or not (reply_message.photo or reply_message.sticker):
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Bᴏss, ʀᴇᴘʟʏ ᴛᴏ ᴀ Pʜᴏᴛᴏ ᴏʀ Sᴛɪᴄᴋᴇʀ ᴛᴏ ᴍᴇᴍɪғʏ ɪᴛ!**")

    if len(message.command) < 2:
        return await message.reply_text("<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ:** `/mmf Uᴘᴘᴇʀ Tᴇxᴛ ; Lᴏᴡᴇʀ Tᴇxᴛ`\n<emoji id=6152142357727811958>✨</emoji> **Exᴀᴍᴘʟᴇ:** `/mmf Anu Matrix ; OP Boss`")

    mystic = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Aɴᴜ Mᴀᴛʀɪx Mᴇᴍᴇ Pʀᴏᴄᴇssᴏʀ Sᴛᴀʀᴛᴇᴅ...**\n<emoji id=5256131095094652290>⏱️</emoji> `Dᴏᴡɴʟᴏᴀᴅɪɴɢ ɪᴍᴀɢᴇ...`")
    
    text = message.text.split(None, 1)[1]
    
    try:
        file_path = await app.download_media(reply_message)
        await mystic.edit_text("<emoji id=6123040393769521180>☄️</emoji> **Mᴀᴋɪɴɢ ɪᴛ ᴀ Mᴀsᴛᴇʀᴘɪᴇᴄᴇ...**")
        
        # ☠️ Running Heavy PIL Code in Thread to prevent Bot Freeze ☠️
        meme_path = await asyncio.to_thread(draw_text_advanced, file_path, text)
        
        await message.reply_document(
            document=meme_path,
            caption=f"<emoji id=5354924568492383911>😈</emoji> **Mᴇᴍᴇ Cʀᴇᴀᴛᴇᴅ Bʏ Aɴᴜ Mᴀᴛʀɪx!**\n<emoji id=6307750079423845494>👑</emoji> **Rᴇǫᴜᴇsᴛᴇᴅ Bʏ:** {message.from_user.mention}"
        )
        
        await mystic.delete()
        
        # ☠️ Cleanup Junk Files ☠️
        if os.path.exists(meme_path):
            os.remove(meme_path)
            
    except Exception as e:
        await mystic.edit_text(f"<emoji id=6307821174017496029>❌</emoji> **Fᴀɪʟᴇᴅ Tᴏ Pʀᴏᴄᴇss Mᴇᴍᴇ!**\n`{e}`")


def draw_text_advanced(image_path, text):
    img = Image.open(image_path)
    os.remove(image_path)
    
    # ☠️ Prevent WebP conversion error by ensuring RGB mode ☠️
    if img.mode != "RGB":
        img = img.convert("RGB")

    i_width, i_height = img.size

    # ☠️ FONT CRASH PROTECTOR ☠️
    try:
        if os.name == "nt":
            fnt = "arial.ttf"
        else:
            fnt = "./KUKU/assets/default.ttf"
        m_font = ImageFont.truetype(fnt, int((70 / 640) * i_width))
    except Exception:
        # Agar font file nahi mili, toh bot crash nahi hoga, default font use karega!
        m_font = ImageFont.load_default()

    if ";" in text:
        upper_text, lower_text = text.split(";", 1)
    else:
        upper_text = text
        lower_text = ""

    draw = ImageDraw.Draw(img)
    current_h, pad = 10, 5

    # ☠️ FIX for Deprecated 'textsize' in new Python versions ☠️
    def get_text_size(txt, font):
        try:
            bbox = draw.textbbox((0, 0), txt, font=font)
            return bbox[2] - bbox[0], bbox[3] - bbox[1]
        except AttributeError:
            return draw.textsize(txt, font=font)

    if upper_text:
        for u_text in textwrap.wrap(upper_text.strip(), width=15):
            u_width, u_height = get_text_size(u_text, m_font)

            # Stroke/Outline effect (Black border for white text)
            draw.text((((i_width - u_width) / 2) - 2, int((current_h / 640) * i_width)), u_text, font=m_font, fill="black")
            draw.text((((i_width - u_width) / 2) + 2, int((current_h / 640) * i_width)), u_text, font=m_font, fill="black")
            draw.text((((i_width - u_width) / 2), int(((current_h / 640) * i_width)) - 2), u_text, font=m_font, fill="black")
            draw.text((((i_width - u_width) / 2), int(((current_h / 640) * i_width)) + 2), u_text, font=m_font, fill="black")
            
            # Main White Text
            draw.text((((i_width - u_width) / 2), int((current_h / 640) * i_width)), u_text, font=m_font, fill="white")

            current_h += u_height + pad

    if lower_text:
        for l_text in textwrap.wrap(lower_text.strip(), width=15):
            u_width, u_height = get_text_size(l_text, m_font)
            y_pos = i_height - u_height - int((20 / 640) * i_width)

            # Stroke/Outline effect
            draw.text((((i_width - u_width) / 2) - 2, y_pos), l_text, font=m_font, fill="black")
            draw.text((((i_width - u_width) / 2) + 2, y_pos), l_text, font=m_font, fill="black")
            draw.text((((i_width - u_width) / 2), y_pos - 2), l_text, font=m_font, fill="black")
            draw.text((((i_width - u_width) / 2), y_pos + 2), l_text, font=m_font, fill="black")
            
            # Main White Text
            draw.text((((i_width - u_width) / 2), y_pos), l_text, font=m_font, fill="white")

            current_h += u_height + pad

    image_name = "anu_memify.webp"
    img.save(image_name, "webp")
    return image_name

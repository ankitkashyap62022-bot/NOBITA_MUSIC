import io
import asyncio
import qrcode
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from NOBITA_MUSIC import app

# ==========================================
# ☠️ ANU MATRIX PREMIUM QR ENGINE ☠️
# ==========================================

def generate_premium_qr(text):
    # ☠️ High-Error Correction for Premium Look ☠️
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H, 
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    # 💎 Black QR on White BG (100% Scannable by all cameras) 💎
    img = qr.make_image(fill_color="black", back_color="white")

    img_bytes = io.BytesIO()
    img_bytes.name = "AnuMatrix_QR.png" # Telegram needs a filename
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return img_bytes


@app.on_message(filters.command(["qr", "qrcode", "makeqr"]))
async def premium_qr_handler(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ:** `/qr [Tᴇxᴛ ᴏʀ Lɪɴᴋ]`\n<emoji id=6152142357727811958>✨</emoji> **Exᴀᴍᴘʟᴇ:** `/qr https://google.com`")

    input_text = message.text.split(None, 1)[1]

    # 💎 ANIMATED UI 💎
    mystic = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Gᴇɴᴇʀᴀᴛɪɴɢ Pʀᴇᴍɪᴜᴍ QR Cᴏᴅᴇ...**")

    try:
        # ☠️ ASYNC THREAD (No Bot Freeze!) ☠️
        qr_image = await asyncio.to_thread(generate_premium_qr, input_text)

        caption = f"<emoji id=5354924568492383911>😈</emoji> **Aɴᴜ Mᴀᴛʀɪx QR Gᴇɴᴇʀᴀᴛᴏʀ**\n\n<emoji id=4929369656797431200>🪐</emoji> **Dᴀᴛᴀ:** `{input_text}`\n<emoji id=6111742817304841054>✅</emoji> **Gᴇɴᴇʀᴀᴛᴇᴅ Bʏ:** {message.from_user.mention}"
        
        # Adding a cool inline button to share
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("✨ Sʜᴀʀᴇ Mʏ QR ✨", switch_inline_query=input_text)]]
        )

        await message.reply_photo(
            photo=qr_image, 
            caption=caption,
            reply_markup=keyboard,
            reply_to_message_id=message.id
        )
        await mystic.delete()

    except Exception as e:
        await mystic.edit_text(f"<emoji id=6307821174017496029>❌</emoji> **Fᴀɪʟᴇᴅ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ QR Cᴏᴅᴇ!**\n`{e}`")

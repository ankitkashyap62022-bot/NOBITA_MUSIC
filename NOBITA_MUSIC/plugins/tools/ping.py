from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup
from NOBITA_MUSIC import app
from NOBITA_MUSIC.core.call import NOBITA
from NOBITA_MUSIC.utils import bot_sys_stats
from NOBITA_MUSIC.utils.inline.extras import botplaylist_markup
from NOBITA_MUSIC.utils.decorators.language import language
from NOBITA_MUSIC.misc import SUDOERS, mongodb
from config import BANNED_USERS
import config
import aiohttp
import asyncio

# ☠️ MONSTER DATABASE SETUP FOR PING PIC ☠️
pingdb = mongodb.ping_pic

async def get_ping_image():
    data = await pingdb.find_one({"_id": "ping_pic"})
    if not data:
        fallback = "https://telegra.ph/file/82b13eddfc5eb944b76e2.jpg"
        return config.PING_IMG_URL if config.PING_IMG_URL else fallback
    return data["url"]

async def set_ping_image(url):
    await pingdb.update_one({"_id": "ping_pic"}, {"$set": {"url": url}}, upsert=True)


# ☠️ COMMAND: /setpingpic (SUDOERS ONLY) ☠️
@app.on_message(filters.command(["setpingpic"]) & SUDOERS)
async def set_ping_pic_cmd(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply_text("<emoji id=4926993814033269936>🖕</emoji> **Boss! Please reply to an image with `/setpingpic` to update it.**")

    # Extracting photo ID and saving to database
    photo = message.reply_to_message.photo.file_id
    await set_ping_image(photo)
    await message.reply_text("<emoji id=6111742817304841054>✅</emoji> **Boom! <emoji id=6307821174017496029>🔥</emoji> Ping Menu picture successfully updated! Check it with `/ping`.**")


# ☠️ MAIN PING COMMAND ☠️
@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    # 💎 FETCH DYNAMIC PING IMAGE FROM DB 💎
    PING_IMG = await get_ping_image()

    # 🔥 ANTI-CRASH IMAGE SENDER (अगर इमेज डेड है, तो क्रैश नहीं होगा) 🔥
    try:
        response = await message.reply_photo(
            photo=PING_IMG,
            caption=_["ping_1"].format(app.mention),
        )
    except Exception:
        # अगर फोटो नहीं मिली, तो सीधा टेक्स्ट मैसेज भेजेगा!
        response = await message.reply_text(
            text=_["ping_1"].format(app.mention),
        )

    start = datetime.now()
    pytgping = await NOBITA.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    
    # 🔥 ANTI-CRASH SAFE EDIT (फोटो और टेक्स्ट दोनों को एडिट करने का लॉजिक) 🔥
    try:
        await response.edit_caption(
            caption=_["ping_2"].format(
                resp, app.mention, UP, RAM, CPU, DISK, pytgping
            ),
            reply_markup=InlineKeyboardMarkup(botplaylist_markup(_)),
        )
    except Exception:
        try:
            await response.edit_text(
                text=_["ping_2"].format(
                    resp, app.mention, UP, RAM, CPU, DISK, pytgping
                ),
                reply_markup=InlineKeyboardMarkup(botplaylist_markup(_)),
            )
        except Exception:
            pass

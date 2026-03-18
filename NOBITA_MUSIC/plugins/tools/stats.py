import platform
from sys import version as pyver

import psutil
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.errors import MessageIdInvalid
from pyrogram.types import InputMediaPhoto, Message
from pytgcalls.__version__ import __version__ as pytgver

import config
from NOBITA_MUSIC import app
from NOBITA_MUSIC.core.userbot import assistants
from NOBITA_MUSIC.misc import SUDOERS, mongodb
from NOBITA_MUSIC.plugins import ALL_MODULES
from NOBITA_MUSIC.utils.database import get_served_chats, get_served_users, get_sudoers
from NOBITA_MUSIC.utils.decorators.language import language, languageCB
from NOBITA_MUSIC.utils.inline.stats import back_stats_buttons, stats_buttons
from config import BANNED_USERS

# ☠️ MONSTER DATABASE SETUP FOR STATS PIC ☠️
statsdb = mongodb.stats_pic

async def get_stats_image():
    data = await statsdb.find_one({"_id": "stats_pic"})
    if not data:
        fallback = "https://telegra.ph/file/2973150dd62fd27a3a6ba.jpg"
        return config.STATS_IMG_URL if config.STATS_IMG_URL else fallback
    return data["url"]

async def set_stats_image(url):
    await statsdb.update_one({"_id": "stats_pic"}, {"$set": {"url": url}}, upsert=True)


# ☠️ COMMAND: /setstatspic ☠️
@app.on_message(filters.command(["setstatspic"]) & filters.user(SUDOERS))
async def set_stats_pic_cmd(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply_text("☠️ **ब्रो! किसी फोटो (Image) पर रिप्लाई करके `/setstatspic` लिख!**")

    # फोटो का ID निकालना और डेटाबेस में डालना
    photo = message.reply_to_message.photo.file_id
    await set_stats_image(photo)
    await message.reply_text("ꜱᴛᴀᴛꜱ ᴩɪᴄ ꜱᴀᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜰᴜʟʟʏ ⚡❤️‍🔥")


# ☠️ BUG FIXED: 'from_user', works in PM too! ☠️
@app.on_message(filters.command(["stats", "gstats"]) & ~BANNED_USERS)
@language
async def stats_global(client, message: Message, _):
    upl = stats_buttons(_, True if message.from_user.id in SUDOERS else False)

    # 💎 NEW PREMIUM UI INJECTED (Main Menu)
    caption = f"""┌ **ᴀɴᴜ ᴍᴀᴛʀɪx ꜱʏꜱᴛᴇᴍ** ™
**ꜱᴛᴀᴛꜱ ᴀɴᴅ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ :**

**ꜱᴛᴀᴛᴜꜱ :** ᴏɴʟɪɴᴇ & ʀᴇᴀᴅʏ!
**ᴘɪɴɢ :** ᴜʟᴛʀᴀ ꜰᴀꜱᴛ

**ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <a href='https://t.me/Reflex_x_zara'>𝗠𝗢𝗡𝗦𝗧𝗘𝗥 𝗫 𝗥𝗘𝗙𝗟𝗘𝗫</a>**"""

    STATS_IMG = await get_stats_image()
    try:
        await message.reply_photo(photo=STATS_IMG, caption=caption, reply_markup=upl)
    except Exception as e:
        await message.reply_text(caption, reply_markup=upl)


@app.on_callback_query(filters.regex("stats_back") & ~BANNED_USERS)
@languageCB
async def home_stats(client, CallbackQuery, _):
    upl = stats_buttons(_, True if CallbackQuery.from_user.id in SUDOERS else False)
    # Main menu caption when clicking "Back"
    caption = f"""┌ **ᴀɴᴜ ᴍᴀᴛʀɪx ꜱʏꜱᴛᴇᴍ** ™
**ꜱᴛᴀᴛꜱ ᴀɴᴅ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ :**

**ꜱᴛᴀᴛᴜꜱ :** ᴏɴʟɪɴᴇ & ʀᴇᴀᴅʏ!
**ᴘɪɴɢ :** ᴜʟᴛʀᴀ ꜰᴀꜱᴛ

**ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <a href='https://t.me/Reflex_x_zara'>𝗠𝗢𝗡𝗦𝗧𝗘𝗥 𝗫 𝗥𝗘𝗙𝗟𝗘𝗫</a>**"""

    STATS_IMG = await get_stats_image()
    med = InputMediaPhoto(media=STATS_IMG, caption=caption)
    
    # Anti-crash logic
    try:
        await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    except Exception:
        try:
            await CallbackQuery.edit_message_text(text=caption, reply_markup=upl)
        except Exception:
            pass


@app.on_callback_query(filters.regex("TopOverall") & ~BANNED_USERS)
@languageCB
async def overall_stats(client, CallbackQuery, _):
    await CallbackQuery.answer("⚡ Fetching Network Stats...")
    upl = back_stats_buttons(_)

    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())

    # 💎 YORSA STYLE ADVANCED UI 💎
    text = f"""┌ **ᴀɴᴜ ᴍᴀᴛʀɪx ꜱʏꜱᴛᴇᴍ** ™
**ꜱᴛᴀᴛꜱ ᴀɴᴅ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ :**

**ᴀꜱꜱɪꜱᴛᴀɴᴛꜱ :** {len(assistants)}
**ʙʟᴏᴄᴋᴇᴅ :** {len(BANNED_USERS)}
**ᴄʜᴀᴛꜱ :** {served_chats}
**ᴜꜱᴇʀꜱ :** {served_users}
**ᴍᴏᴅᴜʟᴇꜱ :** {len(ALL_MODULES)}
**ꜱᴜᴅᴏᴇʀꜱ :** {len(SUDOERS)}

**ᴀᴜᴛᴏ ʟᴇᴀᴠɪɴɢ ᴀꜱꜱɪꜱᴛᴀɴᴛ :** {config.AUTO_LEAVING_ASSISTANT}
**ᴘʟᴀʏ ᴅᴜʀᴀᴛɪᴏɴ ʟɪᴍɪᴛ :** {config.DURATION_LIMIT_MIN} ᴍɪɴᴜᴛᴇꜱ"""

    STATS_IMG = await get_stats_image()
    med = InputMediaPhoto(media=STATS_IMG, caption=text)
    
    # Anti-crash logic
    try:
        await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    except Exception:
        try:
            await CallbackQuery.edit_message_text(text=text, reply_markup=upl)
        except Exception as e:
            await CallbackQuery.message.reply_photo(photo=STATS_IMG, caption=text, reply_markup=upl)


# ☠️ REMOVED bot_stats_sudo FUNCTION BECAUSE SERVER STATS IS DEAD ☠️

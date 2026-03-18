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
    await message.reply_text("✅ **बूम! 💥 Stats Menu की नई पिक्चर सेट हो गई बॉस! अब `/stats` चेक कर!**")


# ☠️ BUG FIXED: 'from_user', works in PM too! ☠️
@app.on_message(filters.command(["stats", "gstats"]) & ~BANNED_USERS)
@language
async def stats_global(client, message: Message, _):
    upl = stats_buttons(_, True if message.from_user.id in SUDOERS else False)
    
    # 💎 NEW PREMIUM UI INJECTED
    caption = f"""<emoji id=4929369656797431200>🪐</emoji> **ᴀɴᴜ ᴍᴀᴛʀɪx ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛꜱ** <emoji id=4929369656797431200>🪐</emoji>\n\n➻ <emoji id=6123040393769521180>☄️</emoji> **ꜱᴛᴀᴛᴜꜱ :** ᴏɴʟɪɴᴇ & ʀᴇᴀᴅʏ!\n➻ <emoji id=6154635934135490309>💗</emoji> **ᴘɪɴɢ :** ᴜʟᴛʀᴀ ꜰᴀꜱᴛ\n\n<emoji id=6310022800023229454>✡️</emoji> **ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <a href='https://t.me/Reflex_x_zara'>𝗠𝗢𝗡𝗦𝗧𝗘𝗥 𝗫 𝗥𝗘𝗙𝗟𝗘𝗫</a>**"""
    
    STATS_IMG = await get_stats_image()
    try:
        await message.reply_photo(photo=STATS_IMG, caption=caption, reply_markup=upl)
    except Exception as e:
        await message.reply_text(caption, reply_markup=upl)


@app.on_callback_query(filters.regex("stats_back") & ~BANNED_USERS)
@languageCB
async def home_stats(client, CallbackQuery, _):
    upl = stats_buttons(_, True if CallbackQuery.from_user.id in SUDOERS else False)
    caption = f"""<emoji id=4929369656797431200>🪐</emoji> **ᴀɴᴜ ᴍᴀᴛʀɪx ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛꜱ** <emoji id=4929369656797431200>🪐</emoji>\n\n➻ <emoji id=6123040393769521180>☄️</emoji> **ꜱᴛᴀᴛᴜꜱ :** ᴏɴʟɪɴᴇ & ʀᴇᴀᴅʏ!\n➻ <emoji id=6154635934135490309>💗</emoji> **ᴘɪɴɢ :** ᴜʟᴛʀᴀ ꜰᴀꜱᴛ\n\n<emoji id=6310022800023229454>✡️</emoji> **ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <a href='https://t.me/Reflex_x_zara'>𝗠𝗢𝗡𝗦𝗧𝗘𝗥 𝗫 𝗥𝗘𝗙𝗟𝗘𝗫</a>**"""
    
    STATS_IMG = await get_stats_image()
    med = InputMediaPhoto(media=STATS_IMG, caption=caption)
    try:
        await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    except:
        await CallbackQuery.edit_message_text(text=caption, reply_markup=upl)


@app.on_callback_query(filters.regex("TopOverall") & ~BANNED_USERS)
@languageCB
async def overall_stats(client, CallbackQuery, _):
    await CallbackQuery.answer("⚡ Fetching Overall Stats...")
    upl = back_stats_buttons(_)
    
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    
    # 💎 NEW OVERALL STATS UI
    text = f"""<emoji id=6310022800023229454>✡️</emoji> **ᴀɴᴜ ᴍᴀᴛʀɪx ɴᴇᴛᴡᴏʀᴋ** <emoji id=6310022800023229454>✡️</emoji>\n
➻ <emoji id=6307605493644793241>📒</emoji> **ᴛᴏᴛᴀʟ ᴄʜᴀᴛꜱ :** {served_chats}
➻ <emoji id=6152142357727811958>🦋</emoji> **ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ :** {served_users}
➻ <emoji id=6123040393769521180>☄️</emoji> **ᴀꜱꜱɪꜱᴛᴀɴᴛꜱ :** {len(assistants)}
➻ <emoji id=5998881015320287132>💊</emoji> **ᴍᴏᴅᴜʟᴇꜱ ʟᴏᴀᴅᴇᴅ :** {len(ALL_MODULES)}
➻ <emoji id=6310044717241340733>🔄</emoji> **ꜱᴜᴅᴏᴇʀꜱ ᴀᴄᴛɪᴠᴇ :** {len(SUDOERS)}
➻ <emoji id=4926993814033269936>🖕</emoji> **ʙʟᴏᴄᴋᴇᴅ ᴛʀᴀꜱʜ :** {len(BANNED_USERS)}"""

    STATS_IMG = await get_stats_image()
    med = InputMediaPhoto(media=STATS_IMG, caption=text)
    try:
        await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    except MessageIdInvalid:
        await CallbackQuery.message.reply_photo(photo=STATS_IMG, caption=text, reply_markup=upl)


@app.on_callback_query(filters.regex("bot_stats_sudo"))
@languageCB
async def bot_stats(client, CallbackQuery, _):
    if CallbackQuery.from_user.id not in SUDOERS:
        return await CallbackQuery.answer("❌ You are not the Supreme Commander!", show_alert=True)
    
    await CallbackQuery.answer("⚡ Hacking Server Status...")
    upl = back_stats_buttons(_)
    
    p_core = psutil.cpu_count(logical=False)
    ram = str(round(psutil.virtual_memory().total / (1024.0**3))) + " ɢʙ"
    
    try:
        cpu_freq = psutil.cpu_freq().current
        cpu_freq = f"{round(cpu_freq / 1000, 2)}ɢʜᴢ" if cpu_freq >= 1000 else f"{round(cpu_freq, 2)}ᴍʜᴢ"
    except:
        cpu_freq = "ʟᴏᴄᴋᴇᴅ 🔒"
        
    hdd = psutil.disk_usage("/")
    total = hdd.total / (1024.0**3)
    used = hdd.used / (1024.0**3)
    
    # 💎 NEW SERVER/BOT STATS UI
    text = f"""<emoji id=4929369656797431200>🪐</emoji> **ᴍᴏɴꜱᴛᴇʀ ᴋᴇʀɴᴇʟ ꜱᴇʀᴠᴇʀ** <emoji id=4929369656797431200>🪐</emoji>\n
➻ <emoji id=6123040393769521180>☄️</emoji> **ᴏꜱ :** {platform.system()}
➻ <emoji id=6154635934135490309>💗</emoji> **ʀᴀᴍ :** {ram}
➻ <emoji id=6307605493644793241>📒</emoji> **ᴄᴘᴜ :** {cpu_freq} ({p_core} ᴄᴏʀᴇꜱ)
➻ <emoji id=6310022800023229454>✡️</emoji> **ꜱᴛᴏʀᴀɢᴇ :** {str(used)[:4]}ɢʙ / {str(total)[:4]}ɢʙ
➻ <emoji id=5998881015320287132>💊</emoji> **ᴘʏʀᴏɢʀᴀᴍ :** ᴠ{pyrover}
➻ <emoji id=6152142357727811958>🦋</emoji> **ᴘʏᴛɢᴄᴀʟʟꜱ :** ᴠ{pytgver}"""

    STATS_IMG = await get_stats_image()
    med = InputMediaPhoto(media=STATS_IMG, caption=text)
    try:
        await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    except MessageIdInvalid:
        await CallbackQuery.message.reply_photo(photo=STATS_IMG, caption=text, reply_markup=upl)

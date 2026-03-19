import platform
import asyncio  # 🔥 ADDED FOR ANIMATION DELAY
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


# ☠️ CRITICAL BUG FIXED & PREMIUM EMOJIS ADDED ☠️
@app.on_message(filters.command(["setstatspic"]) & SUDOERS)
async def set_stats_pic_cmd(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply_text("<emoji id=4926993814033269936>🖕</emoji> **Boss! Please reply to an image with `/setstatspic` to update it.**")

    photo = message.reply_to_message.photo.file_id
    await set_stats_image(photo)
    await message.reply_text("<emoji id=6111742817304841054>✅</emoji> **Boom! <emoji id=6307821174017496029>🔥</emoji> Stats Menu picture successfully updated! Check it with `/stats`.**")


# ☠️ MAIN STATS COMMAND (ADVANCED UI) ☠️
@app.on_message(filters.command(["stats", "gstats"]) & ~BANNED_USERS)
@language
async def stats_global(client, message: Message, _):
    sudoers_list = await get_sudoers()
    upl = stats_buttons(_, True if message.from_user.id in sudoers_list else False)

    caption = f"""┌ <emoji id=4929369656797431200>🪐</emoji> **ᴀɴᴜ ᴍᴀᴛʀɪx ꜱʏꜱᴛᴇᴍ** ™
├━━━━━━━━━━━━━━━━━━━━
├ <emoji id=6001589602085771497>✅</emoji> **ꜱᴛᴀᴛᴜꜱ :** ᴏɴʟɪɴᴇ & ʀᴇᴀᴅʏ!
└ <emoji id=6123040393769521180>☄️</emoji> **ᴘɪɴɢ :** ᴜʟᴛʀᴀ ꜰᴀꜱᴛ

<emoji id=6310022800023229454>✡️</emoji> **ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <a href='https://t.me/MONSTER_FUCK_BITCHES'>𝗠𝗢𝗡𝗦𝗧𝗘𝗥 𝗫 𝗥𝗘𝗙𝗟𝗘𝗫</a>**"""

    STATS_IMG = await get_stats_image()
    try:
        await message.reply_photo(photo=STATS_IMG, caption=caption, reply_markup=upl)
    except Exception as e:
        await message.reply_text(caption, reply_markup=upl)


@app.on_callback_query(filters.regex("stats_back") & ~BANNED_USERS)
@languageCB
async def home_stats(client, CallbackQuery, _):
    sudoers_list = await get_sudoers()
    upl = stats_buttons(_, True if CallbackQuery.from_user.id in sudoers_list else False)
    
    caption = f"""┌ <emoji id=4929369656797431200>🪐</emoji> **ᴀɴᴜ ᴍᴀᴛʀɪx ꜱʏꜱᴛᴇᴍ** ™
├━━━━━━━━━━━━━━━━━━━━
├ <emoji id=6001589602085771497>✅</emoji> **ꜱᴛᴀᴛᴜꜱ :** ᴏɴʟɪɴᴇ & ʀᴇᴀᴅʏ!
└ <emoji id=6123040393769521180>☄️</emoji> **ᴘɪɴɢ :** ᴜʟᴛʀᴀ ꜰᴀꜱᴛ

<emoji id=6310022800023229454>✡️</emoji> **ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <a href='https://t.me/MONSTER_FUCK_BITCHES'>𝗠𝗢𝗡𝗦𝗧𝗘𝗥 𝗫 𝗥𝗘𝗙𝗟𝗘𝗫</a>**"""

    STATS_IMG = await get_stats_image()
    med = InputMediaPhoto(media=STATS_IMG, caption=caption)
    
    try:
        await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    except Exception:
        pass


# ☠️ THE ANIMATED NETWORK STATS ☠️
@app.on_callback_query(filters.regex("TopOverall") & ~BANNED_USERS)
@languageCB
async def overall_stats(client, CallbackQuery, _):
    await CallbackQuery.answer("⚡ Hacking Network Core...", show_alert=False)
    upl = back_stats_buttons(_)
    STATS_IMG = await get_stats_image()

    # 🔥 THE MATRIX LOADING ANIMATION (FLOODWAIT SAFE) 🔥
    try:
        load_1 = f"<emoji id=6310044717241340733>🔄</emoji> **ᴀɴᴜ ᴍᴀᴛʀɪx : ʙʏᴘᴀꜱꜱɪɴɢ ꜰɪʀᴇᴡᴀʟʟ...**\n`[■■■□□□□□□□] 30%`"
        await CallbackQuery.edit_message_media(media=InputMediaPhoto(media=STATS_IMG, caption=load_1), reply_markup=upl)
        await asyncio.sleep(0.4)
        
        load_2 = f"<emoji id=5354924568492383911>😈</emoji> **ᴀɴᴜ ᴍᴀᴛʀɪx : ᴇxᴛʀᴀᴄᴛɪɴɢ ᴅᴀᴛᴀ...**\n`[■■■■■■■■□□] 80%`"
        await CallbackQuery.edit_message_media(media=InputMediaPhoto(media=STATS_IMG, caption=load_2), reply_markup=upl)
        await asyncio.sleep(0.4)
    except:
        pass # Agar spam hua to animation skip hoke direct open hoga (NO CRASH)

    # FETCHING REAL DATA
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    sudoers_list = await get_sudoers()
    banned_list = config.BANNED_USERS

    # 💎 THE FINAL ADVANCED PREMIUM UI 💎
    text = f"""┌ <emoji id=4929195195225867512>💎</emoji> **ᴀɴᴜ ᴍᴀɪɴꜰʀᴀᴍᴇ ɴᴇᴛᴡᴏʀᴋ** <emoji id=4929195195225867512>💎</emoji>
├━━━━━━━━━━━━━━━━━━━━
├ <emoji id=6307750079423845494>👑</emoji> **ᴀꜱꜱɪꜱᴛᴀɴᴛꜱ :** `{len(assistants)}`
├ <emoji id=4926993814033269936>🖕</emoji> **ʙʟᴏᴄᴋᴇᴅ :** `{len(banned_list)}`
├ <emoji id=6307605493644793241>📒</emoji> **ᴄʜᴀᴛꜱ :** `{served_chats}`
├ <emoji id=6152142357727811958>🦋</emoji> **ᴜꜱᴇʀꜱ :** `{served_users}`
├ <emoji id=5998881015320287132>💊</emoji> **ᴍᴏᴅᴜʟᴇꜱ :** `{len(ALL_MODULES)}`
├ <emoji id=5354924568492383911>😈</emoji> **ꜱᴜᴅᴏᴇʀꜱ :** `{len(sudoers_list)}`
├━━━━━━━━━━━━━━━━━━━━
├ <emoji id=6310044717241340733>🔄</emoji> **ᴀᴜᴛᴏ ʟᴇᴀᴠᴇ :** `{config.AUTO_LEAVING_ASSISTANT}`
└ <emoji id=6111778259374971023>🔥</emoji> **ᴘʟᴀʏ ʟɪᴍɪᴛ :** `{config.DURATION_LIMIT_MIN} ᴍɪɴꜱ`"""

    med_final = InputMediaPhoto(media=STATS_IMG, caption=text)
    try:
        await CallbackQuery.edit_message_media(media=med_final, reply_markup=upl)
    except Exception:
        try:
            await CallbackQuery.edit_message_text(text=text, reply_markup=upl)
        except Exception as e:
            pass

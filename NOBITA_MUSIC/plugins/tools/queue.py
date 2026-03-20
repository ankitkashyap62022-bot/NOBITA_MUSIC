import asyncio
import os

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import CallbackQuery, InputMediaPhoto, Message

import config
from NOBITA_MUSIC import app
from NOBITA_MUSIC.misc import db
from NOBITA_MUSIC.utils import NOBITABin, get_channeplayCB, seconds_to_min
from NOBITA_MUSIC.utils.database import get_cmode, is_active_chat, is_music_playing
from NOBITA_MUSIC.utils.decorators.language import language, languageCB
from NOBITA_MUSIC.utils.inline import queue_back_markup, queue_markup
from config import BANNED_USERS

basic = {}


def get_image(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"
    else:
        return config.YOUTUBE_IMG_URL


def get_duration(playing):
    file_path = playing[0]["file"]
    if "index_" in file_path or "live_" in file_path:
        return "Unknown"
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return "Unknown"
    else:
        return "Inline"


# ==========================================
# ☠️ ANU MATRIX PREMIUM QUEUE SYSTEM ☠️
# ==========================================

@app.on_message(filters.command(["queue", "cqueue", "player", "cplayer", "playing", "cplaying"]) & filters.group & ~BANNED_USERS)
@language
async def premium_get_queue(client, message: Message, _):
    if message.command[0][0] == "c":
        chat_id = await get_cmode(message.chat.id)
        if chat_id is None:
            return await message.reply_text(_["setting_7"])
        try:
            await app.get_chat(chat_id)
        except:
            return await message.reply_text(_["cplay_4"])
        cplay = True
    else:
        chat_id = message.chat.id
        cplay = False

    if not await is_active_chat(chat_id):
        return await message.reply_text(_["general_5"])

    got = db.get(chat_id)
    if not got:
        return await message.reply_text(_["queue_2"])

    file = got[0]["file"]
    videoid = got[0]["vidid"]
    user = got[0]["by"]
    title = (got[0]["title"]).title()
    typo = (got[0]["streamtype"]).title()
    DUR = get_duration(got)

    if "live_" in file or "vid_" in file:
        IMAGE = get_image(videoid)
    elif "index_" in file:
        IMAGE = config.STREAM_IMG_URL
    else:
        if videoid == "telegram":
            IMAGE = config.TELEGRAM_AUDIO_URL if typo == "Audio" else config.TELEGRAM_VIDEO_URL
        elif videoid == "soundcloud":
            IMAGE = config.SOUNCLOUD_IMG_URL
        else:
            IMAGE = get_image(videoid)

    send = _["queue_6"] if DUR == "Unknown" else _["queue_7"]
    cap = _["queue_8"].format(app.mention, title, typo, user, send)
    
    upl = (
        queue_markup(_, DUR, "c" if cplay else "g", videoid)
        if DUR == "Unknown"
        else queue_markup(_, DUR, "c" if cplay else "g", videoid, seconds_to_min(got[0]["played"]), got[0]["dur"])
    )
    
    basic[videoid] = True
    mystic = await message.reply_photo(IMAGE, caption=cap, reply_markup=upl)
    
    # 💎 LIVE PROGRESS BAR UPDATER 💎
    if DUR != "Unknown":
        try:
            while db[chat_id][0]["vidid"] == videoid:
                await asyncio.sleep(5)
                if await is_active_chat(chat_id):
                    if basic[videoid]:
                        if await is_music_playing(chat_id):
                            try:
                                buttons = queue_markup(
                                    _, DUR, "c" if cplay else "g", videoid,
                                    seconds_to_min(db[chat_id][0]["played"]), db[chat_id][0]["dur"]
                                )
                                await mystic.edit_reply_markup(reply_markup=buttons)
                            except FloodWait:
                                pass
                        else:
                            pass
                    else:
                        break
                else:
                    break
        except:
            return


@app.on_callback_query(filters.regex("GetTimer") & ~BANNED_USERS)
async def quite_timer(client, CallbackQuery: CallbackQuery):
    try:
        await CallbackQuery.answer()
    except:
        pass


@app.on_callback_query(filters.regex("GetQueued") & ~BANNED_USERS)
@languageCB
async def premium_queued_tracks(client, CallbackQuery: CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    what, videoid = callback_request.split("|")
    
    try:
        chat_id, channel = await get_channeplayCB(_, what, CallbackQuery)
    except:
        return
        
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(_["general_5"], show_alert=True)
        
    got = db.get(chat_id)
    if not got:
        return await CallbackQuery.answer(_["queue_2"], show_alert=True)
        
    if len(got) == 1:
        return await CallbackQuery.answer(_["queue_5"], show_alert=True)
        
    await CallbackQuery.answer()
    basic[videoid] = False
    buttons = queue_back_markup(_, what)
    
    med = InputMediaPhoto(media=config.YOUTUBE_IMG_URL, caption=_["queue_1"]) # Used configured image
    await CallbackQuery.edit_message_media(media=med)
    
    j = 0
    msg = "<emoji id=6123040393769521180>☄️</emoji> **A N U  M A T R I X  Q U E U E**\n\n"
    
    for x in got:
        j += 1
        if j == 1:
            msg += f"<emoji id=6307358404176254008>🔥</emoji> **Nᴏᴡ Pʟᴀʏɪɴɢ :**\n<emoji id=6089186666973500770>🎶</emoji> **Tɪᴛʟᴇ :** {x['title']}\n<emoji id=5256131095094652290>⏱️</emoji> **Dᴜʀᴀᴛɪᴏɴ :** {x['dur']}\n<emoji id=5042302287087666158>💖</emoji> **Bʏ :** {x['by']}\n\n"
        elif j == 2:
            msg += f"<emoji id=6111742817304841054>✅</emoji> **Nᴇxᴛ Uᴘ (Qᴜᴇᴜᴇ) :**\n<emoji id=6089186666973500770>🎶</emoji> **Tɪᴛʟᴇ :** {x['title']}\n<emoji id=5256131095094652290>⏱️</emoji> **Dᴜʀᴀᴛɪᴏɴ :** {x['dur']}\n<emoji id=5042302287087666158>💖</emoji> **Bʏ :** {x['by']}\n\n"
        else:
            msg += f"<emoji id=6152142357727811958>✨</emoji> **Tɪᴛʟᴇ :** {x['title']}\n<emoji id=5256131095094652290>⏱️</emoji> **Dᴜʀᴀᴛɪᴏɴ :** {x['dur']}\n<emoji id=5042302287087666158>💖</emoji> **Bʏ :** {x['by']}\n\n"
            
    if "Nᴇxᴛ Uᴘ" in msg:
        if len(msg) < 700:
            await asyncio.sleep(1)
            return await CallbackQuery.edit_message_text(msg, reply_markup=buttons)
            
        # ☠️ BUG FIXED HERE (NOBITABin instead of RAUSHANBin) ☠️
        link = await NOBITABin(msg)
        med = InputMediaPhoto(media=link, caption=f"<emoji id=5354924568492383911>😈</emoji> **Bᴏss, ᴛʜᴇ ǫᴜᴇᴜᴇ ɪs ᴛᴏᴏ ʟᴏɴɢ!**\n<emoji id=6307605493644793241>📒</emoji> <a href='{link}'>Cʟɪᴄᴋ Hᴇʀᴇ Tᴏ Vɪᴇᴡ Fᴜʟʟ Qᴜᴇᴜᴇ</a>")
        await CallbackQuery.edit_message_media(media=med, reply_markup=buttons)
    else:
        await asyncio.sleep(1)
        return await CallbackQuery.edit_message_text(msg, reply_markup=buttons)


@app.on_callback_query(filters.regex("queue_back_timer") & ~BANNED_USERS)
@languageCB
async def premium_queue_back(client, CallbackQuery: CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cplay = callback_data.split(None, 1)[1]
    
    try:
        chat_id, channel = await get_channeplayCB(_, cplay, CallbackQuery)
    except:
        return
        
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(_["general_5"], show_alert=True)
        
    got = db.get(chat_id)
    if not got:
        return await CallbackQuery.answer(_["queue_2"], show_alert=True)
        
    await CallbackQuery.answer(_["set_cb_5"], show_alert=True)
    
    file = got[0]["file"]
    videoid = got[0]["vidid"]
    user = got[0]["by"]
    title = (got[0]["title"]).title()
    typo = (got[0]["streamtype"]).title()
    DUR = get_duration(got)

    if "live_" in file or "vid_" in file:
        IMAGE = get_image(videoid)
    elif "index_" in file:
        IMAGE = config.STREAM_IMG_URL
    else:
        if videoid == "telegram":
            IMAGE = config.TELEGRAM_AUDIO_URL if typo == "Audio" else config.TELEGRAM_VIDEO_URL
        elif videoid == "soundcloud":
            IMAGE = config.SOUNCLOUD_IMG_URL
        else:
            IMAGE = get_image(videoid)

    send = _["queue_6"] if DUR == "Unknown" else _["queue_7"]
    cap = _["queue_8"].format(app.mention, title, typo, user, send)
    
    upl = (
        queue_markup(_, DUR, cplay, videoid)
        if DUR == "Unknown"
        else queue_markup(_, DUR, cplay, videoid, seconds_to_min(got[0]["played"]), got[0]["dur"])
    )
    
    basic[videoid] = True
    med = InputMediaPhoto(media=IMAGE, caption=cap)
    mystic = await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    
    if DUR != "Unknown":
        try:
            while db[chat_id][0]["vidid"] == videoid:
                await asyncio.sleep(5)
                if await is_active_chat(chat_id):
                    if basic[videoid]:
                        if await is_music_playing(chat_id):
                            try:
                                buttons = queue_markup(
                                    _, DUR, cplay, videoid,
                                    seconds_to_min(db[chat_id][0]["played"]), db[chat_id][0]["dur"]
                                )
                                await mystic.edit_reply_markup(reply_markup=buttons)
                            except FloodWait:
                                pass
                        else:
                            pass
                    else:
                        break
                else:
                    break
        except:
            return

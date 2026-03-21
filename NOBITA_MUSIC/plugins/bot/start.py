import time
import random
from pyrogram import filters
from pyrogram.enums import ChatType, ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from NOBITA_MUSIC import app
from NOBITA_MUSIC.misc import _boot_
# ☠️ SUDO SYSTEM TERMINATED - Removed sudoers_list import! ☠️
from NOBITA_MUSIC.utils import bot_sys_stats
from NOBITA_MUSIC.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from NOBITA_MUSIC.utils.decorators.language import LanguageStart
from NOBITA_MUSIC.utils.formatters import get_readable_time
from NOBITA_MUSIC.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

# ==========================================
# 💎 BOSS KE KHUD KE PREMIUM HTML EMOJIS 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_CROWN = "<emoji id='6307750079423845494'>👑</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_CROSS = "<emoji id='4926993814033269936'>🖕</emoji>"
E_TICK = "<emoji id='6111742817304841054'>✅</emoji>"
E_LOAD = "<emoji id='6310044717241340733'>🔄</emoji>"
E_STAR = "<emoji id='6309709550878463216'>🌟</emoji>"

# 🔥 MONGODB DATABASES FOR DYNAMIC MEDIA 🔥
from NOBITA_MUSIC.core.mongo import mongodb
start_db = mongodb.start_media
ply_db = mongodb.custom_play_thumb  
log_db = mongodb.custom_log_thumb  # ☠️ NEW: Database for /setlogpic

async def get_start_media():
    """Fetches the custom start media from MongoDB."""
    doc = await start_db.find_one({"_id": "custom_start"})
    if doc:
        return doc.get("type"), doc.get("file_id")
    # ☠️ Fallback Video if nothing is set yet
    return "video", "https://telegra.ph/file/1a3c152717eb9d2e94dc2.mp4"

async def set_start_media(media_type, file_id):
    """Saves the custom start media to MongoDB."""
    await start_db.update_one(
        {"_id": "custom_start"},
        {"$set": {"type": media_type, "file_id": file_id}},
        upsert=True
    )

async def get_custom_thumb():
    """Fetches the custom play thumbnail from MongoDB."""
    doc = await ply_db.find_one({"_id": "custom_thumb"})
    if doc:
        return doc.get("file_id")
    return None

# ==========================================
# ☠️ THE /setstart COMMAND (OWNER ONLY)
# ==========================================
@app.on_message(filters.command(["setstart"]) & filters.user(config.OWNER_ID))
async def set_start_cmd(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(f"{E_DEVIL} **ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴘʜᴏᴛᴏ ᴏʀ ᴠɪᴅᴇᴏ ᴛᴏ sᴇᴛ ɪᴛ ᴀs sᴛᴀʀᴛ ᴍᴇᴅɪᴀ ᴍʏ ʟᴏʀᴅ!**", parse_mode=ParseMode.HTML)

    mystic = await message.reply_text(f"{E_LOAD} <b>ᴜᴘᴅᴀᴛɪɴɢ ᴀɴᴜ ᴍᴀᴛʀɪx ᴅᴀᴛᴀʙᴀsᴇ...</b>", parse_mode=ParseMode.HTML)

    if message.reply_to_message.photo:
        file_id = message.reply_to_message.photo.file_id
        await set_start_media("photo", file_id)
        return await mystic.edit_text(f"{E_TICK} **sᴛᴀʀᴛ ᴘʜᴏᴛᴏ ᴜᴘᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!** {E_DEVIL}", parse_mode=ParseMode.HTML)

    elif message.reply_to_message.video:
        file_id = message.reply_to_message.video.file_id
        await set_start_media("video", file_id)
        return await mystic.edit_text(f"{E_TICK} **sᴛᴀʀᴛ ᴠɪᴅᴇᴏ ᴜᴘᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!** {E_DEVIL}", parse_mode=ParseMode.HTML)

    else:
        return await mystic.edit_text(f"{E_CROSS} **ʙᴀʙʏ, ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴏɴʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ ᴏʀ ᴠɪᴅᴇᴏ!**", parse_mode=ParseMode.HTML)

# ==========================================
# ☠️ THE /setply COMMAND (OWNER ONLY)
# ==========================================
@app.on_message(filters.command(["setply", "setplay"]) & filters.user(config.OWNER_ID))
async def set_ply_cmd(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply_text(f"{E_DEVIL} **ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ ᴛᴏ sᴇᴛ ɪᴛ ᴀs ᴘʟᴀʏ ᴛʜᴜᴍʙɴᴀɪʟ ᴍʏ ʟᴏʀᴅ!**", parse_mode=ParseMode.HTML)

    mystic = await message.reply_text(f"{E_LOAD} <b>ᴜᴘᴅᴀᴛɪɴɢ ᴀɴᴜ ᴍᴀᴛʀɪx ᴅᴀᴛᴀʙᴀsᴇ...</b>", parse_mode=ParseMode.HTML)
    file_id = message.reply_to_message.photo.file_id

    await ply_db.update_one(
        {"_id": "custom_thumb"},
        {"$set": {"file_id": file_id}},
        upsert=True
    )
    return await mystic.edit_text(f"{E_TICK} **ᴘʟᴀʏ ᴘʜᴏᴛᴏ ᴜᴘᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ! ᴀʟʟ sᴏɴɢs ᴡɪʟʟ ᴜsᴇ ᴛʜɪs ɴᴏᴡ.** {E_DEVIL}", parse_mode=ParseMode.HTML)

# ==========================================
# ☠️ THE /setlogpic COMMAND (OWNER ONLY)
# ==========================================
@app.on_message(filters.command(["setlogpic", "setleftpic"]) & filters.user(config.OWNER_ID))
async def set_log_pic(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(f"{E_DEVIL} **हैकर वार्निंग:** किसी फोटो या वीडियो का रिप्लाई करके <code>/setlogpic</code> लिखो बॉस!", parse_mode=ParseMode.HTML)

    mystic = await message.reply_text(f"{E_LOAD} <b>ᴜᴘᴅᴀᴛɪɴɢ ᴀɴᴜ ᴍᴀᴛʀɪx ᴅᴀᴛᴀʙᴀsᴇ...</b>", parse_mode=ParseMode.HTML)

    if message.reply_to_message.photo:
        file_id = message.reply_to_message.photo.file_id
    elif message.reply_to_message.video:
        file_id = message.reply_to_message.video.file_id
    else:
        # 🔥 FIX: Added 'return' to prevent UnboundLocalError Crash!
        return await mystic.edit_text(f"{E_CROSS} **एरर:** सिर्फ फोटो या वीडियो ही सपोर्टेड है!", parse_mode=ParseMode.HTML)

    await log_db.update_one({"_id": "custom_log"}, {"$set": {"file_id": file_id}}, upsert=True)
    await mystic.edit_text(f"{E_STAR} **ᴀɴᴜ ᴍᴀᴛʀɪx ʟᴏɢ-ᴍᴇᴅɪᴀ ᴜᴘᴅᴀᴛᴇᴅ!**\n\nअब जब भी बॉट किसी ग्रुप में जायेगा या लेफ्ट होगा, तो तेरी सेट की हुई यही मीडिया लॉग ग्रुप में गिरेगी! {E_DEVIL}", parse_mode=ParseMode.HTML)

# ==========================================
# 🚀 MAIN START COMMANDS
# ==========================================
@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    media_type, file_id = await get_start_media() # Fetch Custom Media

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        
        # 🆘 HELP MODULE
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            if media_type == "photo":
                return await message.reply_photo(photo=file_id, caption=_["help_1"].format(config.SUPPORT_CHAT), reply_markup=keyboard)
            else:
                return await message.reply_video(video=file_id, caption=_["help_1"].format(config.SUPPORT_CHAT), reply_markup=keyboard)

        # 👑 SUDO MODULE (DESTROYED - OWNER ONLY RULE)
        if name[0:3] == "sud":
            toxic_reply = f"""
{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗘 𝗠 𝗣 𝗜 𝗥 𝗘 』</b> {E_DIAMOND}
━━━━━━━━━━━━━━━━━━━━
{E_CROSS} <b>SUDO SYSTEM TERMINATED!</b>

{E_DEVIL} <i>Yahan koi Sudo-Vudo nahi chalta lode.</i>
{E_CROWN} <b>Sirf ek hi Baap hai is bot ka: Mera Owner!</b>
━━━━━━━━━━━━━━━━━━━━
"""
            return await message.reply_text(toxic_reply, parse_mode=ParseMode.HTML)

        # 🔎 TRACK INFO MODULE
        if name[0:3] == "inf":
            m = await message.reply_text(f"{E_LOAD} <b>Fᴇᴛᴄʜɪɴɢ ɪɴғᴏ...</b>", parse_mode=ParseMode.HTML)
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
                
            searched_text = _["start_6"].format(title, duration, views, published, channellink, channel, app.mention)
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(chat_id=message.chat.id, photo=thumbnail, caption=searched_text, reply_markup=key)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
    else:
        # 🏡 NORMAL START MENU
        out = private_panel(_)
        if media_type == "photo":
            await message.reply_photo(photo=file_id, caption=_["start_2"].format(message.from_user.mention, app.mention), reply_markup=InlineKeyboardMarkup(out))
        else:
            await message.reply_video(video=file_id, caption=_["start_2"].format(message.from_user.mention, app.mention), reply_markup=InlineKeyboardMarkup(out))

        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
            )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    media_type, file_id = await get_start_media() # Fetch Custom Media

    if media_type == "photo":
        await message.reply_photo(photo=file_id, caption=_["start_1"].format(app.mention, get_readable_time(uptime)), reply_markup=InlineKeyboardMarkup(out))
    else:
        await message.reply_video(video=file_id, caption=_["start_1"].format(app.mention, get_readable_time(uptime)), reply_markup=InlineKeyboardMarkup(out))

    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                media_type, file_id = await get_start_media() # Fetch Custom Media

                if media_type == "photo":
                    await message.reply_photo(photo=file_id, caption=_["start_3"].format(message.from_user.mention, app.mention, message.chat.title, app.mention), reply_markup=InlineKeyboardMarkup(out))
                else:
                    await message.reply_video(video=file_id, caption=_["start_3"].format(message.from_user.mention, app.mention, message.chat.title, app.mention), reply_markup=InlineKeyboardMarkup(out))

                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)

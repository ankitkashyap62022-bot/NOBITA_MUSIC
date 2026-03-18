from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ParseMode
from config import LOGGER_ID as LOG_GROUP_ID
from NOBITA_MUSIC import app 
from pyrogram.errors import RPCError
from typing import Union, Optional
import asyncio, os, aiohttp
from pathlib import Path

# ☠️ ANU MATRIX DATABASE CONNECTION ☠️
from NOBITA_MUSIC.core.mongo import mongodb
log_db = mongodb.custom_log_thumb

# अगर तूने /setlogpic से फोटो सेट नहीं की है, तो ये डिफ़ॉल्ट चलेगी
FALLBACK_PHOTO = "https://telegra.ph/file/2973150dd62fd27a3a6ba.jpg"

@app.on_message(filters.new_chat_members, group=2)
async def join_watcher(_, message):    
    chat = message.chat
    
    try:
        link = await app.export_chat_invite_link(chat.id)
    except:
        link = "No Link Available"
        
    for member in message.new_chat_members:
        if member.id == app.id:
            count = await app.get_chat_members_count(chat.id)
            
            # 💎 FETCHING CUSTOM PIC FROM DATABASE 💎
            db_pic = await log_db.find_one({"_id": "custom_log"})
            log_pic = db_pic.get("file_id") if db_pic else FALLBACK_PHOTO
            
            msg = (
                f"<emoji id=6309709550878463216>🌟</emoji> <b>ᴀɴᴜ ᴍᴀᴛʀɪx ᴀᴅᴅᴇᴅ ɪɴ ɴᴇᴡ ɢʀᴏᴜᴘ</b> <emoji id=6309709550878463216>🌟</emoji>\n\n"
                f"➻ <emoji id=4929483658114368660>💎</emoji> <b>ᴄʜᴀᴛ ɴᴀᴍᴇ :</b> {chat.title}\n"
                f"➻ <emoji id=6307821174017496029>🔥</emoji> <b>ᴄʜᴀᴛ ɪᴅ :</b> <code>{chat.id}</code>\n"
                f"➻ <emoji id=6307750079423845494>👑</emoji> <b>ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :</b> @{chat.username}\n"
                f"➻ <emoji id=6307569802466563145>🎶</emoji> <b>ɢʀᴏᴜᴘ ᴍᴇᴍʙᴇʀs :</b> {count}\n"
                f"➻ <emoji id=5999210495146465994>💖</emoji> <b>ᴀᴅᴅᴇᴅ ʙʏ :</b> {message.from_user.mention}\n\n"
                f"➻ <emoji id=5352542184493031170>😈</emoji> <b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <a href='https://t.me/Reflex_x_zara'>𝗠𝗢𝗡𝗦𝗧𝗘𝗥 𝗫 𝗥𝗘𝗙𝗟𝗘𝗫</a></b>"
            )
            
            button = InlineKeyboardMarkup([[InlineKeyboardButton("☠️ ᴠɪᴇᴡ ᴛᴀʀɢᴇᴛ ɢʀᴏᴜᴘ ☠️", url=f"{link}")]]) if link != "No Link Available" else None
            
            try:
                try:
                    await app.send_photo(LOG_GROUP_ID, photo=log_pic, caption=msg, reply_markup=button, parse_mode=ParseMode.HTML)
                except:
                    await app.send_video(LOG_GROUP_ID, video=log_pic, caption=msg, reply_markup=button, parse_mode=ParseMode.HTML)
            except Exception as e:
                print(e)

@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    if (await app.get_me()).id == message.left_chat_member.id:
        remove_by = message.from_user.mention if message.from_user else "𝐔ɴᴋɴᴏᴡɴ 𝐔sᴇʀ"
        title = message.chat.title
        chat_id = message.chat.id
        
        # 💎 FETCHING CUSTOM PIC FROM DATABASE 💎
        db_pic = await log_db.find_one({"_id": "custom_log"})
        log_pic = db_pic.get("file_id") if db_pic else FALLBACK_PHOTO

        left_msg = (
            f"<emoji id=5352542184493031170>😈</emoji> <b>ᴀɴᴜ ᴍᴀᴛʀɪx ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ɢʀᴏᴜᴘ</b>\n\n"
            f"➻ <emoji id=4929483658114368660>💎</emoji> <b>ᴄʜᴀᴛ ᴛɪᴛʟᴇ :</b> {title}\n"
            f"➻ <emoji id=6307821174017496029>🔥</emoji> <b>ᴄʜᴀᴛ ɪᴅ :</b> <code>{chat_id}</code>\n"
            f"➻ <emoji id=5999210495146465994>💖</emoji> <b>ʀᴇᴍᴏᴠᴇᴅ ʙʏ :</b> {remove_by}\n\n"
            f"➻ <emoji id=6309709550878463216>🌟</emoji> <b>ʙᴏᴛ :</b> @{app.username}"
        )
        
        try:
            try:
                await app.send_photo(LOG_GROUP_ID, photo=log_pic, caption=left_msg, parse_mode=ParseMode.HTML)
            except:
                await app.send_video(LOG_GROUP_ID, video=log_pic, caption=left_msg, parse_mode=ParseMode.HTML)
        except Exception as e:
            print(e)

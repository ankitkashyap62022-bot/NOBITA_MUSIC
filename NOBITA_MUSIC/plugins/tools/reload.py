import asyncio
import time
from os import getenv

from pyrogram import Client, filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from NOBITA_MUSIC import app
from NOBITA_MUSIC.core.call import NOBITA # ☠️ FIXED IMPORT
from NOBITA_MUSIC.misc import db
from NOBITA_MUSIC.utils.database import get_assistant, get_authuser_names, get_cmode
from NOBITA_MUSIC.utils.decorators import ActualAdminCB, AdminActual
from NOBITA_MUSIC.utils.formatters import alpha_to_int, get_readable_time
from config import BANNED_USERS, adminlist, lyrical

rel = {}

# ==========================================
# ☠️ ANU MATRIX ADMIN CACHE & SYSTEM PROTOCOL ☠️
# ==========================================

@app.on_message(filters.command(["admincache", "reload", "refresh"]) & filters.group & ~BANNED_USERS)
async def premium_reload_admin_cache(client, message: Message):
    try:
        if message.chat.id not in rel:
            rel[message.chat.id] = {}
        else:
            saved = rel[message.chat.id]
            if saved > time.time():
                left = get_readable_time((int(saved) - int(time.time())))
                return await message.reply_text(f"<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, ᴀʟʀᴇᴀᴅʏ ʀᴇғʀᴇsʜᴇᴅ!**\n<emoji id=6123040393769521180>☄️</emoji> Wᴀɪᴛ `{left}` ʙᴇғᴏʀᴇ ʀᴇʟᴏᴀᴅɪɴɢ ᴀɢᴀɪɴ.")
                
        mystic = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Sʏɴᴄɪɴɢ Aɴᴜ Mᴀᴛʀɪx Aᴅᴍɪɴ Dᴀᴛᴀʙᴀsᴇ...**")
        
        adminlist[message.chat.id] = []
        async for user in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
            if user.privileges.can_manage_video_chats:
                adminlist[message.chat.id].append(user.user.id)
                
        authusers = await get_authuser_names(message.chat.id)
        for user in authusers:
            user_id = await alpha_to_int(user)
            adminlist[message.chat.id].append(user_id)
            
        now = int(time.time()) + 180
        rel[message.chat.id] = now
        
        await mystic.edit_text("<emoji id=6111742817304841054>✅</emoji> **Aᴅᴍɪɴ Cᴀᴄʜᴇ Uᴘᴅᴀᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!**\n<emoji id=6152142357727811958>✨</emoji> Aʟʟ ɴᴇᴡ ᴀᴅᴍɪɴs ᴄᴀɴ ɴᴏᴡ ᴄᴏɴᴛʀᴏʟ ᴍᴇ.")
    except Exception as e:
        await message.reply_text(f"<emoji id=6307821174017496029>❌</emoji> **Fᴀɪʟᴇᴅ Tᴏ Rᴇʟᴏᴀᴅ Cᴀᴄʜᴇ!**\n<emoji id=5256131095094652290>⏱️</emoji> Mᴀᴋᴇ sᴜʀᴇ I ᴀᴍ ᴀɴ ᴀᴅᴍɪɴ ʜᴇʀᴇ.\n`{e}`")


@app.on_message(filters.command(["reboot"]) & filters.group & ~BANNED_USERS)
@AdminActual
async def premium_restartbot(client, message: Message, _):
    mystic = await message.reply_text(f"<emoji id=6310044717241340733>🔄</emoji> **Rᴇʙᴏᴏᴛɪɴɢ {app.mention} Fᴏʀ Tʜɪs Cʜᴀᴛ...**")
    await asyncio.sleep(1)
    
    try:
        db[message.chat.id] = []
        await NOBITA.stop_stream_force(message.chat.id) # ☠️ BUG FIXED (RAUSHAN to NOBITA) ☠️
    except:
        pass
        
    userbot = await get_assistant(message.chat.id)
    try:
        if message.chat.username:
            await userbot.resolve_peer(message.chat.username)
        else:
            await userbot.resolve_peer(message.chat.id)
    except:
        pass
        
    chat_id = await get_cmode(message.chat.id)
    if chat_id:
        try:
            got = await app.get_chat(chat_id)
        except:
            pass
        userbot = await get_assistant(chat_id)
        try:
            if got.username:
                await userbot.resolve_peer(got.username)
            else:
                await userbot.resolve_peer(chat_id)
        except:
            pass
        try:
            db[chat_id] = []
            await NOBITA.stop_stream_force(chat_id) # ☠️ BUG FIXED ☠️
        except:
            pass
            
    return await mystic.edit_text(f"<emoji id=6111742817304841054>✅</emoji> **{app.mention} Rᴇʙᴏᴏᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!**\n<emoji id=6152142357727811958>✨</emoji> `Yᴏᴜ ᴄᴀɴ ɴᴏᴡ ᴘʟᴀʏ ᴍᴜsɪᴄ ᴀɢᴀɪɴ.`")


# ==========================================
# 💎 PREMIUM CALLBACK HANDLERS 💎
# ==========================================

@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def premium_close_menu(_, query: CallbackQuery):
    try:
        await query.answer()
        await query.message.delete()
        umm = await query.message.reply_text(
            f"<emoji id=6307821174017496029>❌</emoji> **Mᴇɴᴜ Cʟᴏsᴇᴅ Bʏ:** {query.from_user.mention}"
        )
        await asyncio.sleep(3)
        await umm.delete()
    except:
        pass


@app.on_callback_query(filters.regex("stop_downloading") & ~BANNED_USERS)
@ActualAdminCB
async def premium_stop_download(client, CallbackQuery: CallbackQuery, _):
    message_id = CallbackQuery.message.id
    task = lyrical.get(message_id)
    
    if not task:
        return await CallbackQuery.answer("» Dᴏᴡɴʟᴏᴀᴅ ᴀʟʀᴇᴀᴅʏ ғɪɴɪsʜᴇᴅ ᴏʀ ɴᴏᴛ ғᴏᴜɴᴅ!", show_alert=True)
    if task.done() or task.cancelled():
        return await CallbackQuery.answer("» Dᴏᴡɴʟᴏᴀᴅ ᴀʟʀᴇᴀᴅʏ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴏʀ ᴄᴀɴᴄᴇʟʟᴇᴅ!", show_alert=True)
        
    if not task.done():
        try:
            task.cancel()
            try:
                lyrical.pop(message_id)
            except:
                pass
            await CallbackQuery.answer("» Dᴏᴡɴʟᴏᴀᴅ Cᴀɴᴄᴇʟʟᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!", show_alert=True)
            return await CallbackQuery.edit_message_text(
                f"<emoji id=6307821174017496029>❌</emoji> **Dᴏᴡɴʟᴏᴀᴅɪɴɢ Iɴᴛᴇʀʀᴜᴘᴛᴇᴅ!**\n<emoji id=5354924568492383911>😈</emoji> **Aᴄᴛɪᴏɴ Bʏ:** {CallbackQuery.from_user.mention}"
            )
        except:
            return await CallbackQuery.answer("» Fᴀɪʟᴇᴅ ᴛᴏ sᴛᴏᴘ ᴛʜᴇ ᴅᴏᴡɴʟᴏᴀᴅ!", show_alert=True)
            
    await CallbackQuery.answer("» Fᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴛʜᴇ ʀᴜɴɴɪɴɢ ᴛᴀsᴋ!", show_alert=True)

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.types import Message

from NOBITA_MUSIC import app
from NOBITA_MUSIC.utils.database import set_cmode
from NOBITA_MUSIC.utils.decorators.admins import AdminActual
from config import BANNED_USERS

@app.on_message(filters.command(["channelplay"]) & filters.group & ~BANNED_USERS)
@AdminActual
async def playmode_(client, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text(_["cplay_1"].format(message.chat.title))
        
    query = message.text.split(None, 2)[1].lower().strip()
    
    if query == "disable":
        await set_cmode(message.chat.id, None)
        return await message.reply_text(_["cplay_7"])
        
    elif query == "linked":
        chat = await app.get_chat(message.chat.id)
        if chat.linked_chat:
            chat_id = chat.linked_chat.id
            await set_cmode(message.chat.id, chat_id)
            return await message.reply_text(
                _["cplay_3"].format(chat.linked_chat.title, chat.linked_chat.id)
            )
        else:
            return await message.reply_text(_["cplay_2"])
            
    else:
        try:
            chat = await app.get_chat(query)
        except:
            return await message.reply_text(_["cplay_4"])
            
        if chat.type != ChatType.CHANNEL:
            return await message.reply_text(_["cplay_5"])
            
        # 🔥 BUG FIX: Variables ko pehle define kar diya taaki crash na ho
        crid = None
        cusn = None
        
        try:
            async for user in app.get_chat_members(
                chat.id, filter=ChatMembersFilter.ADMINISTRATORS
            ):
                if user.status == ChatMemberStatus.OWNER:
                    cusn = user.user.username if user.user.username else "No Username"
                    crid = user.user.id
                    break # 🔥 FIX: Owner milte hi loop rok diya (CPU bachane ke liye)
        except:
            return await message.reply_text(_["cplay_4"])
            
        # 🔥 FIX: Agar owner fetch nahi hua to safe exit
        if not crid:
            return await message.reply_text("⚠️ <b>Anu System Error:</b> <i>Mujhe is channel ka owner nahi mil raha! Kya main wahan admin hoon?</i>")
            
        if crid != message.from_user.id:
            return await message.reply_text(_["cplay_6"].format(chat.title, cusn))
            
        await set_cmode(message.chat.id, chat.id)
        return await message.reply_text(_["cplay_3"].format(chat.title, chat.id))

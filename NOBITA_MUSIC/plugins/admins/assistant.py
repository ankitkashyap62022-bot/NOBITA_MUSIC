import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserAlreadyParticipant, InviteRequestSent, FloodWait
from NOBITA_MUSIC import app
from NOBITA_MUSIC.utils.NOBITA_ban import admin_filter
from NOBITA_MUSIC.utils.database import get_assistant
from config import OWNER_ID # ☠️ IMPORTING OWNER ID ☠️

# ==========================================
# ☠️ 1. USERBOT JOIN COMMAND (SMART LOGIC) ☠️
# ==========================================
@app.on_message(filters.group & filters.command(["userbotjoin", f"userbotjoin@{app.username}"]))
async def join_group(client, message):
    chat_id = message.chat.id
    userbot = await get_assistant(chat_id)
    
    done = await message.reply("<emoji id=6310044717241340733>🔄</emoji> **Pʀᴏᴄᴇssɪɴɢ... Iɴᴠɪᴛɪɴɢ Asꜱɪsᴛᴀɴᴛ ᴛᴏ ᴛʜᴇ ᴄʜᴀᴛ!**")
    await asyncio.sleep(1)

    try:
        # Check if Assistant is banned and Unban it
        userbot_member = await app.get_chat_member(chat_id, userbot.id)
        if userbot_member.status in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
            await app.unban_chat_member(chat_id, userbot.id)
            await done.edit_text("<emoji id=5998881015320287132>💊</emoji> **Asꜱɪsᴛᴀɴᴛ ᴡᴀs ʙᴀɴɴᴇᴅ! Uɴʙᴀɴɴɪɴɢ ᴀɴᴅ ʀᴇ-ɪɴᴠɪᴛɪɴɢ...**")
            await asyncio.sleep(1)
    except Exception:
        pass # If bot is not admin or userbot is not banned, ignore

    # The Hard & Smart Join Logic
    try:
        if message.chat.username:
            # Join via Public Username
            await userbot.join_chat(message.chat.username)
        else:
            # Join via Invite Link (For Private Groups)
            invite_link = await app.create_chat_invite_link(chat_id)
            await userbot.join_chat(invite_link.invite_link)
            
        await done.edit_text("<emoji id=6111742817304841054>✅</emoji> **Asꜱɪsᴛᴀɴᴛ Sᴜᴄᴄᴇssғᴜʟʟʏ Jᴏɪɴᴇᴅ!** <emoji id=5352870513267973607>✨</emoji>")
        
    except UserAlreadyParticipant:
        await done.edit_text("<emoji id=4929369656797431200>🪐</emoji> **Asꜱɪsᴛᴀɴᴛ ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ ᴛʜɪs ᴄʜᴀᴛ ʙᴀʙʏ!**")
    except InviteRequestSent:
        await done.edit_text("<emoji id=6152142357727811958>🦋</emoji> **Iɴᴠɪᴛᴇ ʀᴇǫᴜᴇsᴛ sᴇɴᴛ! Aᴅᴍɪɴ ɴᴇᴇᴅs ᴛᴏ ᴀᴘᴘʀᴏᴠᴇ.**")
    except Exception as e:
        await done.edit_text(
            f"<emoji id=6307821174017496029>🔥</emoji> **Fᴀɪʟᴇᴅ ᴛᴏ ɪɴᴠɪᴛᴇ Asꜱɪsᴛᴀɴᴛ!**\n\n"
            f"**Rᴇᴀsᴏɴ:** ɪ ɴᴇᴇᴅ `Iɴᴠɪᴛᴇ Usᴇʀs` & `Bᴀɴ Usᴇʀs` ᴀᴅᴍɪɴ ᴘᴏᴡᴇʀ ᴛᴏ ᴅᴏ ᴛʜɪs.\n"
            f"**Eʀʀᴏʀ:** `{e}`\n\n"
            f"**Asꜱɪsᴛᴀɴᴛ ID:** @{userbot.username}"
        )


# ==========================================
# ☠️ 2. USERBOT LEAVE COMMAND (ADMINS ONLY) ☠️
# ==========================================
@app.on_message(filters.command("userbotleave") & filters.group & admin_filter)
async def leave_one(client, message):
    try:
        userbot = await get_assistant(message.chat.id)
        await userbot.leave_chat(message.chat.id)
        await app.send_message(
            message.chat.id, 
            "<emoji id=6123040393769521180>☄️</emoji> **Asꜱɪsᴛᴀɴᴛ Sᴜᴄᴄᴇssғᴜʟʟʏ Lᴇғᴛ Tʜᴇ Cʜᴀᴛ!**"
        )
    except Exception as e:
        await message.reply(f"❌ **Eʀʀᴏʀ:** `{e}`")


# ==========================================
# ☠️ 3. LEAVE ALL COMMAND (STRICTLY OWNER ONLY) ☠️
# ==========================================
@app.on_message(filters.command(["leaveall", f"leaveall@{app.username}"]))
async def leave_all(client, message):
    # 🔒 STRICT OWNER LOCK 🔒
    if message.from_user.id != OWNER_ID:
        return await message.reply("<emoji id=5354924568492383911>😈</emoji> **Oᴜᴋᴀᴀᴛ ᴍᴇ ʀᴇʜ ʟᴏᴅᴇ! Tʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ғᴏʀ ᴍʏ Sᴜᴘʀᴇᴍᴇ Oᴡɴᴇʀ!**")

    left = 0
    failed = 0
    status_msg = await message.reply("<emoji id=6310044717241340733>🔄</emoji> **Mᴏɴsᴛᴇʀ Pʀᴏᴛᴏᴄᴏʟ Iɴɪᴛɪᴀᴛᴇᴅ! Asꜱɪsᴛᴀɴᴛ ɪs ʟᴇᴀᴠɪɴɢ ᴀʟʟ ᴄʜᴀᴛs...**")
    
    try:
        userbot = await get_assistant(message.chat.id)
        async for dialog in userbot.get_dialogs():
            # 🛡️ THE SAFE ZONE (Support Group) 🛡️
            if dialog.chat.id == -1002344707828:
                continue
                
            try:
                await userbot.leave_chat(dialog.chat.id)
                left += 1
                await asyncio.sleep(2) # Anti-Flood Wait
            except Exception:
                failed += 1
                
            # Edit message every 5 leaves to avoid Telegram API FloodWait
            if (left + failed) % 5 == 0:
                try:
                    await status_msg.edit_text(
                        f"<emoji id=4929369656797431200>🪐</emoji> **Mᴀss Lᴇᴀᴠᴇ ɪɴ ᴘʀᴏɢʀᴇss...**\n\n"
                        f"<emoji id=6111742817304841054>✅</emoji> **Lᴇғᴛ:** `{left}`\n"
                        f"<emoji id=6307821174017496029>❌</emoji> **Fᴀɪʟᴇᴅ:** `{failed}`"
                    )
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception:
                    pass

    finally:
        await status_msg.edit_text(
            f"<emoji id=6307750079423845494>👑</emoji> **Asꜱɪsᴛᴀɴᴛ Mᴀss Lᴇᴀᴠᴇ Cᴏᴍᴘʟᴇᴛᴇᴅ Bᴏss!**\n\n"
            f"<emoji id=6111742817304841054>✅</emoji> **Sᴜᴄᴄᴇssғᴜʟʟʏ Lᴇғᴛ:** `{left}` ᴄʜᴀᴛs.\n"
            f"<emoji id=6307821174017496029>❌</emoji> **Fᴀɪʟᴇᴅ/Aᴅᴍɪɴ Issᴜᴇs:** `{failed}` ᴄʜᴀᴛs."
        )

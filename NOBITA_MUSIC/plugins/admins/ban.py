import asyncio
import datetime
from pyrogram import filters, enums
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired, UserAdminInvalid, FloodWait
from NOBITA_MUSIC import app

# ☠️ MEMORY FOR WARNS ☠️
WARNS = {}

# ==========================================
# ☠️ HELPER FUNCTIONS (ADVANCED TARGETING) ☠️
# ==========================================
async def is_admin(chat_id, user_id, client):
    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]
    except:
        return False

async def get_target_user(client, message):
    user = None
    reason = "No reason provided." # Default Reason
    
    # 🎯 TARGETING BY REPLY
    if message.reply_to_message:
        user = message.reply_to_message.from_user
        if len(message.command) > 1:
            reason = message.text.split(None, 1)[1]
            
    # 🎯 TARGETING BY USERNAME OR NUMERIC ID
    elif len(message.command) > 1:
        target = message.command[1]
        try:
            target = int(target) # Checking if it's a Numeric ID
        except ValueError:
            pass # It's a Username
        
        try:
            user = await client.get_users(target)
        except Exception:
            return None, None
            
        if len(message.command) > 2:
            reason = message.text.split(None, 2)[2]
            
    return user, reason

# ==========================================
# ☠️ 1. BAN COMMAND ☠️
# ==========================================
@app.on_message(filters.command(["ban", "sban"]) & filters.group)
async def premium_ban(client, message):
    if not await is_admin(message.chat.id, message.from_user.id, client):
        return await message.reply("<emoji id=5354924568492383911>😈</emoji> **ᴏᴜᴋᴀᴀᴛ ᴍᴇ ʀᴇʜ! ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ.**")

    target_user, reason = await get_target_user(client, message)
    if not target_user:
        return await message.reply("<emoji id=6307821174017496029>🔥</emoji> **ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ɢɪᴠᴇ ᴜꜱᴇʀɴᴀᴍᴇ/ɪᴅ ᴛᴏ ʙᴀɴ.**")

    if target_user.id == client.me.id:
        return await message.reply("<emoji id=4929369656797431200>🪐</emoji> **ᴍᴜᴊʜᴇ ʜɪ ʙᴀɴ ᴋᴀʀᴇɢᴀ? ɢᴀᴅʜᴀ ʜᴀɪ ᴋʏᴀ!**")

    if await is_admin(message.chat.id, target_user.id, client):
        return await message.reply("<emoji id=6123040393769521180>☄️</emoji> **ᴀᴅᴍɪɴ ᴋᴏ ʙᴀɴ ɴᴀʜɪ ᴋᴀʀ ꜱᴀᴋᴛᴀ ʙᴀʙᴜ!**")

    try:
        await client.ban_chat_member(message.chat.id, target_user.id)
        await message.reply(
            f"<emoji id=6123040393769521180>☄️</emoji> **Bᴀɴɴᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n"
            f"<emoji id=5354924568492383911>😈</emoji> **Usᴇʀ:** {target_user.mention}\n"
            f"<emoji id=6307750079423845494>👑</emoji> **Aᴅᴍɪɴ:** {message.from_user.mention}\n"
            f"<emoji id=6307821174017496029>🔥</emoji> **Rᴇᴀsᴏɴ:** `{reason}`"
        )
    except Exception as e:
        await message.reply(f"❌ **Eʀʀᴏʀ:** `{e}`")

# ==========================================
# ☠️ 2. UNBAN COMMAND ☠️
# ==========================================
@app.on_message(filters.command(["unban"]) & filters.group)
async def premium_unban(client, message):
    if not await is_admin(message.chat.id, message.from_user.id, client):
        return await message.reply("<emoji id=5354924568492383911>😈</emoji> **ᴏᴜᴋᴀᴀᴛ ᴍᴇ ʀᴇʜ!**")

    target_user, _ = await get_target_user(client, message)
    if not target_user:
        return await message.reply("<emoji id=6307821174017496029>🔥</emoji> **ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ɢɪᴠᴇ ᴜꜱᴇʀɴᴀᴍᴇ/ɪᴅ.**")

    try:
        await client.unban_chat_member(message.chat.id, target_user.id)
        await message.reply(
            f"<emoji id=6111742817304841054>✅</emoji> **Uɴʙᴀɴɴᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n"
            f"<emoji id=6152142357727811958>🦋</emoji> **Usᴇʀ:** {target_user.mention}\n"
            f"<emoji id=6307750079423845494>👑</emoji> **Aᴅᴍɪɴ:** {message.from_user.mention}"
        )
    except Exception as e:
        await message.reply(f"❌ **Eʀʀᴏʀ:** `{e}`")

# ==========================================
# ☠️ 3. KICK COMMAND ☠️
# ==========================================
@app.on_message(filters.command(["kick"]) & filters.group)
async def premium_kick(client, message):
    if not await is_admin(message.chat.id, message.from_user.id, client):
        return await message.reply("<emoji id=5354924568492383911>😈</emoji> **ᴏᴜᴋᴀᴀᴛ ᴍᴇ ʀᴇʜ!**")

    target_user, reason = await get_target_user(client, message)
    if not target_user:
        return await message.reply("<emoji id=6307821174017496029>🔥</emoji> **ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ɢɪᴠᴇ ᴜꜱᴇʀɴᴀᴍᴇ/ɪᴅ.**")

    if await is_admin(message.chat.id, target_user.id, client):
        return await message.reply("<emoji id=6123040393769521180>☄️</emoji> **ᴀᴅᴍɪɴ ᴋᴏ ᴋɪᴄᴋ ɴᴀʜɪ ᴋᴀʀ ꜱᴀᴋᴛᴀ!**")

    try:
        await client.ban_chat_member(message.chat.id, target_user.id)
        await asyncio.sleep(0.5)
        await client.unban_chat_member(message.chat.id, target_user.id)
        
        await message.reply(
            f"<emoji id=4929369656797431200>🪐</emoji> **Kɪᴄᴋᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!** (Nɪᴋᴀʟ Lᴀᴜᴅᴇ)\n\n"
            f"<emoji id=5354924568492383911>😈</emoji> **Usᴇʀ:** {target_user.mention}\n"
            f"<emoji id=6307750079423845494>👑</emoji> **Aᴅᴍɪɴ:** {message.from_user.mention}\n"
            f"<emoji id=6307821174017496029>🔥</emoji> **Rᴇᴀsᴏɴ:** `{reason}`"
        )
    except Exception as e:
        await message.reply(f"❌ **Eʀʀᴏʀ:** `{e}`")

# ==========================================
# ☠️ 4. MUTE & UNMUTE COMMANDS ☠️
# ==========================================
@app.on_message(filters.command(["mute"]) & filters.group)
async def premium_mute(client, message):
    if not await is_admin(message.chat.id, message.from_user.id, client):
        return await message.reply("<emoji id=5354924568492383911>😈</emoji> **ᴏᴜᴋᴀᴀᴛ ᴍᴇ ʀᴇʜ!**")

    target_user, reason = await get_target_user(client, message)
    if not target_user:
        return await message.reply("<emoji id=6307821174017496029>🔥</emoji> **ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ɢɪᴠᴇ ᴜꜱᴇʀɴᴀᴍᴇ/ɪᴅ.**")

    if await is_admin(message.chat.id, target_user.id, client):
        return await message.reply("<emoji id=6123040393769521180>☄️</emoji> **ᴀᴅᴍɪɴ ᴋᴏ ᴍᴜᴛᴇ ɴᴀʜɪ ᴋᴀʀ ꜱᴀᴋᴛᴀ!**")

    try:
        await client.restrict_chat_member(message.chat.id, target_user.id, ChatPermissions(can_send_messages=False))
        await message.reply(
            f"<emoji id=5998881015320287132>💊</emoji> **Mᴜᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n"
            f"<emoji id=5354924568492383911>😈</emoji> **Usᴇʀ:** {target_user.mention}\n"
            f"<emoji id=6307750079423845494>👑</emoji> **Aᴅᴍɪɴ:** {message.from_user.mention}\n"
            f"<emoji id=6307821174017496029>🔥</emoji> **Rᴇᴀsᴏɴ:** `{reason}`"
        )
    except Exception as e:
        await message.reply(f"❌ **Eʀʀᴏʀ:** `{e}`")

@app.on_message(filters.command(["unmute"]) & filters.group)
async def premium_unmute(client, message):
    if not await is_admin(message.chat.id, message.from_user.id, client):
        return await message.reply("<emoji id=5354924568492383911>😈</emoji> **ᴏᴜᴋᴀᴀᴛ ᴍᴇ ʀᴇʜ!**")

    target_user, _ = await get_target_user(client, message)
    if not target_user:
        return await message.reply("<emoji id=6307821174017496029>🔥</emoji> **ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ɢɪᴠᴇ ᴜꜱᴇʀɴᴀᴍᴇ/ɪᴅ.**")

    try:
        await client.restrict_chat_member(
            message.chat.id, target_user.id, 
            ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
        )
        await message.reply(
            f"<emoji id=6111742817304841054>✅</emoji> **Uɴᴍᴜᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!** ʙᴏʟɴᴇ ᴋɪ ᴀᴀᴢᴀᴀᴅɪ!\n\n"
            f"<emoji id=6152142357727811958>🦋</emoji> **Usᴇʀ:** {target_user.mention}\n"
            f"<emoji id=6307750079423845494>👑</emoji> **Aᴅᴍɪɴ:** {message.from_user.mention}"
        )
    except Exception as e:
        await message.reply(f"❌ **Eʀʀᴏʀ:** `{e}`")


# ==========================================
# ☠️ 5. PURGE COMMAND (CLEAN CHAT) ☠️
# ==========================================
@app.on_message(filters.command(["purge"]) & filters.group)
async def premium_purge(client, message):
    if not await is_admin(message.chat.id, message.from_user.id, client):
        return await message.reply("<emoji id=5354924568492383911>😈</emoji> **ᴏᴜᴋᴀᴀᴛ ᴍᴇ ʀᴇʜ ʟᴏᴅᴇ!**")

    if not message.reply_to_message:
        return await message.reply("<emoji id=6307821174017496029>🔥</emoji> **Rᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴘᴜʀɢᴇ ғʀᴏᴍ ᴛʜᴇʀᴇ!**")

    message_ids = []
    for message_id in range(message.reply_to_message.id, message.id):
        message_ids.append(message_id)
        if len(message_ids) == 100:
            await client.delete_messages(chat_id=message.chat.id, message_ids=message_ids, revoke=True)
            message_ids = []
            
    if len(message_ids) > 0:
        await client.delete_messages(chat_id=message.chat.id, message_ids=message_ids, revoke=True)
        
    await message.delete()
    del_msg = await message.reply(f"<emoji id=6111742817304841054>✅</emoji> **Cʜᴀᴛ Pᴜʀɢᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ!** Kᴀᴄʜʀᴀ sᴀᴀғ ᴋᴀʀ ᴅɪʏᴀ ᴍᴀᴀʟɪᴋ.")
    await asyncio.sleep(4)
    await del_msg.delete()


# ==========================================
# ☠️ 6. WARN COMMAND ☠️
# ==========================================
@app.on_message(filters.command(["warn"]) & filters.group)
async def premium_warn(client, message):
    if not await is_admin(message.chat.id, message.from_user.id, client):
        return await message.reply("<emoji id=5354924568492383911>😈</emoji> **ᴏᴜᴋᴀᴀᴛ ᴍᴇ ʀᴇʜ!**")

    target_user, reason = await get_target_user(client, message)
    if not target_user:
        return await message.reply("<emoji id=6307821174017496029>🔥</emoji> **ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜꜱᴇʀ ᴏʀ ɢɪᴠᴇ ᴜꜱᴇʀɴᴀᴍᴇ/ɪᴅ.**")

    if await is_admin(message.chat.id, target_user.id, client):
        return await message.reply("<emoji id=6123040393769521180>☄️</emoji> **ᴀᴅᴍɪɴ ᴋᴏ ᴡᴀʀɴ ɴᴀʜɪ ᴋᴀʀ ꜱᴀᴋᴛᴀ!**")

    chat_id = message.chat.id
    user_id = target_user.id

    if chat_id not in WARNS:
        WARNS[chat_id] = {}
    if user_id not in WARNS[chat_id]:
        WARNS[chat_id][user_id] = 0

    WARNS[chat_id][user_id] += 1
    current_warns = WARNS[chat_id][user_id]

    if current_warns >= 3:
        try:
            await client.ban_chat_member(chat_id, user_id)
            del WARNS[chat_id][user_id] # Reset warns after ban
            await message.reply(
                f"<emoji id=6123040393769521180>☄️</emoji> **Mᴀx ᴡᴀʀɴɪɴɢs ʀᴇᴀᴄʜᴇᴅ (3/3). Usᴇʀ ʙᴀɴɴᴇᴅ!**\n\n"
                f"<emoji id=5354924568492383911>😈</emoji> **Usᴇʀ:** {target_user.mention}\n"
                f"<emoji id=6307821174017496029>🔥</emoji> **Lᴀsᴛ Rᴇᴀsᴏɴ:** `{reason}`"
            )
        except Exception as e:
            await message.reply(f"❌ **Eʀʀᴏʀ:** `{e}`")
    else:
        await message.reply(
            f"<emoji id=6307346833534359338>🍷</emoji> **Wᴀʀɴɪɴɢ Issᴜᴇᴅ!** ({current_warns}/3)\n\n"
            f"<emoji id=5354924568492383911>😈</emoji> **Usᴇʀ:** {target_user.mention}\n"
            f"<emoji id=6307750079423845494>👑</emoji> **Aᴅᴍɪɴ:** {message.from_user.mention}\n"
            f"<emoji id=6307821174017496029>🔥</emoji> **Rᴇᴀsᴏɴ:** `{reason}`\n\n"
            f"*(Sᴜᴅʜᴀʀ ᴊᴀ ʙʜᴀɪ, 3 ᴡᴀʀɴɪɴɢ ᴘᴇ sɪᴅʜᴀ ʙᴀɴ ʜᴏɢᴀ!)*"
        )

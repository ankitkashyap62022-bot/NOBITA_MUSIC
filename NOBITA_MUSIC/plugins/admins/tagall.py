import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from NOBITA_MUSIC import app
from NOBITA_MUSIC.misc import mongodb

# ☠️ MONSTER KERNEL DATABASE & TRACKER ☠️
tagdb = mongodb.tagall_db  # Permanent DB for Restart Recovery
spam_chats = []
TAG_DATA = {} # RAM storage for initial menu

# 🔥 ADMIN CHECK FUNCTION 🔥
async def is_admin(chat_id, user_id, client):
    try:
        participant = await client.get_chat_member(chat_id, user_id)
        if participant.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return True
    except UserNotParticipant:
        pass
    return False

# ☠️ STEP 1: INITIATE TAG-ALL MENU ☠️
@app.on_message(filters.command(["tagall", "mentionall", "all"]) & filters.group)
async def monster_tagall_menu(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(chat_id, user_id, client):
        return await message.reply("<emoji id=4926993814033269936>🖕</emoji> **ᴏᴜᴋᴀᴀᴛ ᴍᴇ ʀᴇʜ ʟᴏᴅᴇ! ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ.**")

    if chat_id in spam_chats:
        return await message.reply("<emoji id=6310044717241340733>🔄</emoji> **ᴛᴀɢ-ᴀʟʟ ɪꜱ ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ! ꜱᴛᴏᴘ ɪᴛ ꜰɪʀꜱᴛ.**")

    reply = message.reply_to_message
    cmd_text = message.text.split(None, 1)[1] if len(message.command) > 1 else ""

    mode = "text"
    text_content = ""
    media_msg_id = None

    if reply:
        if reply.media:
            mode = "media"
            media_msg_id = reply.id
            text_content = reply.caption.html if reply.caption else ""
            if cmd_text: text_content = cmd_text + "\n\n" + text_content
        else:
            mode = "text"
            text_content = reply.text.html if reply.text else ""
            if cmd_text: text_content = cmd_text + "\n\n" + text_content
    else:
        mode = "text"
        text_content = cmd_text

    TAG_DATA[chat_id] = {
        "mode": mode,
        "text": text_content,
        "media_id": media_msg_id,
        "from_chat": chat_id,
        "initiator": message.from_user.mention
    }

    menu_btns = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✦ 1 / 1 ✦", callback_data="tagbtn_1"),
            InlineKeyboardButton("✦ 2 / 2 ✦", callback_data="tagbtn_2"),
            InlineKeyboardButton("✦ 5 / 5 ✦", callback_data="tagbtn_5")
        ],
        [
            InlineKeyboardButton("⛌ ᴄᴀɴᴄᴇʟ ⛌", callback_data="tagbtn_cancel")
        ]
    ])

    await message.reply_text(
        f"<emoji id=4929369656797431200>🪐</emoji> **ᴀɴᴜ ᴍᴀɪɴꜰʀᴀᴍᴇ ᴛᴀɢɢɪɴɢ ꜱʏꜱᴛᴇᴍ**\n\n"
        f"<emoji id=6307750079423845494>👑</emoji> ꜱᴇʟᴇᴄᴛ ʜᴏᴡ ᴍᴀɴʏ ᴜꜱᴇʀꜱ ᴛᴏ ᴛᴀɢ ᴘᴇʀ ᴍᴇꜱꜱᴀɢᴇ:",
        reply_markup=menu_btns
    )


# ☠️ STEP 2: DB GENERATION & TAGGING ENGINE ☠️
@app.on_callback_query(filters.regex(r"^tagbtn_"))
async def tagall_callback_handler(client, CallbackQuery):
    chat_id = CallbackQuery.message.chat.id
    user_id = CallbackQuery.from_user.id
    action = CallbackQuery.data.split("_")[1]

    if not await is_admin(chat_id, user_id, client):
        return await CallbackQuery.answer("🖕 Oukaat Me Raho! Only Admins!", show_alert=True)

    if action == "cancel":
        if chat_id in TAG_DATA: del TAG_DATA[chat_id]
        return await CallbackQuery.message.delete()

    limit = int(action)

    if chat_id in spam_chats:
        return await CallbackQuery.answer("⚠️ System is already tagging!", show_alert=True)

    data = TAG_DATA.get(chat_id, {"mode": "text", "text": "", "media_id": None, "from_chat": chat_id, "initiator": "Admin"})
    
    stop_btn = InlineKeyboardMarkup([[InlineKeyboardButton("⛌ ꜱᴛᴏᴘ ᴛᴀɢᴀʟʟ ⛌", callback_data=f"stop_tag_{chat_id}")]])
    
    msg = await CallbackQuery.edit_message_text(
        f"<emoji id=6123040393769521180>☄️</emoji> **ᴀɴᴜ ᴍᴀᴛʀɪx : ᴇxᴛʀᴀᴄᴛɪɴɢ ᴜꜱᴇʀꜱ...**\n"
        f"⏳ `Please wait... fetching database.`",
        reply_markup=stop_btn
    )

    # 💾 Fetch all members and save to DB for Restart Recovery
    all_users = []
    async for member in client.get_chat_members(chat_id):
        if not member.user.is_bot and not member.user.is_deleted:
            all_users.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")
    
    await tagdb.update_one(
        {"_id": chat_id},
        {"$set": {"users": all_users, "mode": data["mode"], "text": data["text"], "media_id": data["media_id"], "from_chat": data["from_chat"], "limit": limit}},
        upsert=True
    )

    spam_chats.append(chat_id)
    await msg.edit_text(
        f"<emoji id=6123040393769521180>☄️</emoji> **ᴀɴᴜ ᴍᴀᴛʀɪx ᴛᴀɢ-ᴀʟʟ ɪɴɪᴛɪᴀᴛᴇᴅ!**\n"
        f"<emoji id=6307821174017496029>🔥</emoji> **ᴍᴏᴅᴇ:** `{limit} ᴜꜱᴇʀꜱ / ᴍᴇꜱꜱᴀɢᴇ`\n"
        f"<emoji id=5998881015320287132>💊</emoji> **ʀᴇQᴜᴇꜱᴛᴇᴅ ʙʏ:** {data['initiator']}\n"
        f"<emoji id=6307605493644793241>📒</emoji> **ᴛᴀʀɢᴇᴛꜱ:** `{len(all_users)}`",
        reply_markup=stop_btn
    )

    await process_tags(client, chat_id)


# ☠️ THE CORE LOOP (FAST MODE + AUTO-RESUME) ☠️
async def process_tags(client, chat_id):
    while chat_id in spam_chats:
        # Fetch remaining users from DB
        job = await tagdb.find_one({"_id": chat_id})
        if not job or not job.get("users"):
            break # Tagging complete
        
        limit = job.get("limit", 2)
        pending_users = job["users"]
        
        # Take chunks
        to_tag = pending_users[:limit]
        remaining = pending_users[limit:]
        
        tags_str = " ".join(to_tag)
        final_text = f"{job['text']}\n\n{tags_str}" if job['text'] else tags_str

        # Send Payload
        try:
            if job["mode"] == "media" and job["media_id"]:
                await client.copy_message(chat_id, job["from_chat"], job["media_id"], caption=final_text)
            else:
                await client.send_message(chat_id, final_text)
        except FloodWait as e:
            # 🔥 ANTI-BAN: Respect Telegram's limit automatically 🔥
            await asyncio.sleep(e.value + 0.5)
            continue # Retry same chunk
        except Exception:
            pass # Ignore deleted media or random blocks

        # Update DB (Remove tagged users)
        await tagdb.update_one({"_id": chat_id}, {"$set": {"users": remaining}})
        
        if not remaining:
            break
            
        # 🔥 FAST MODE DELAY (1.5 SECONDS) 🔥
        await asyncio.sleep(1.5)

    # Cleanup when done
    if chat_id in spam_chats:
        spam_chats.remove(chat_id)
    
    # If DB is empty, tagging is successfully fully completed
    job = await tagdb.find_one({"_id": chat_id})
    if job and not job.get("users"):
        await client.send_message(chat_id, "<emoji id=6111742817304841054>✅</emoji> **ᴛᴀɢ-ᴀʟʟ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ! ᴅᴀᴛᴀʙᴀꜱᴇ ᴄʟᴇᴀʀᴇᴅ.**")
        await tagdb.delete_one({"_id": chat_id})


# ☠️ AUTO-RESUME ON BOT RESTART (MAGIC ENGINE) ☠️
async def auto_resume_tagging():
    await asyncio.sleep(15) # Give bot 15 seconds to fully connect to Telegram
    try:
        async for job in tagdb.find({"users": {"$exists": True, "$ne": []}}):
            chat_id = job["_id"]
            if chat_id not in spam_chats:
                spam_chats.append(chat_id)
                # Automatically start tagging where it left off
                asyncio.create_task(process_tags(app, chat_id))
    except Exception:
        pass

# Start the background task automatically
asyncio.create_task(auto_resume_tagging())


# ☠️ FULL STOP COMMAND & BUTTON HANDLER ☠️
@app.on_message(filters.command(["tagoff", "tagstop", "stoptag"]) & filters.group)
async def stop_tag_cmd(client, message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        return await message.reply("<emoji id=4926993814033269936>🖕</emoji> **ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ꜱᴛᴏᴘ ᴛʜɪꜱ!**")
    
    # 🔥 WIPE FROM DATABASE SO IT DOESN'T AUTO-RESUME 🔥
    await tagdb.delete_one({"_id": chat_id})
    
    if chat_id in spam_chats:
        spam_chats.remove(chat_id)
        await message.reply("<emoji id=4929369656797431200>🪐</emoji> **ᴛᴀɢ-ᴀʟʟ ᴀʙᴏʀᴛᴇᴅ & ᴡɪᴘᴇᴅ ꜰʀᴏᴍ ᴅᴀᴛᴀʙᴀꜱᴇ!**")
    else:
        await message.reply("<emoji id=6310022800023229454>✡️</emoji> **ɴᴏ ᴛᴀɢ-ᴀʟʟ ɪꜱ ʀᴜɴɴɪɴɢ ᴄᴜʀʀᴇɴᴛʟʏ.**")

@app.on_callback_query(filters.regex(r"^stop_tag_"))
async def stop_tag_button(client, CallbackQuery):
    chat_id = int(CallbackQuery.data.split("_")[2])
    user_id = CallbackQuery.from_user.id
    
    if not await is_admin(chat_id, user_id, client):
        return await CallbackQuery.answer("🖕 Only Admins can stop this!", show_alert=True)
        
    # 🔥 WIPE FROM DATABASE SO IT DOESN'T AUTO-RESUME 🔥
    await tagdb.delete_one({"_id": chat_id})
    
    if chat_id in spam_chats:
        spam_chats.remove(chat_id)
        await CallbackQuery.answer("🛑 Tagging Stopped & DB Cleared!", show_alert=True)
        await CallbackQuery.edit_message_text("<emoji id=4929369656797431200>🪐</emoji> **ᴛᴀɢ-ᴀʟʟ ᴀʙᴏʀᴛᴇᴅ ʙʏ ᴀᴅᴍɪɴ!**")
    else:
        await CallbackQuery.answer("It's not running!", show_alert=True)

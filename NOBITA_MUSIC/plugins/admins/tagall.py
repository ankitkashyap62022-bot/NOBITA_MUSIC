import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from NOBITA_MUSIC import app

# ☠️ MONSTER KERNEL SPAM TRACKER ☠️
spam_chats = []

# 🔥 ADMIN CHECK FUNCTION 🔥
async def is_admin(chat_id, user_id, client):
    try:
        participant = await client.get_chat_member(chat_id, user_id)
        if participant.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return True
    except UserNotParticipant:
        pass
    return False

# ☠️ THE ULTRA TAG-ALL ENGINE ☠️
@app.on_message(filters.command(["tagall", "tagall1", "tagall5"]) & filters.group)
async def monster_tagall(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # 1. Admin Verification
    if not await is_admin(chat_id, user_id, client):
        return await message.reply("<emoji id=4926993814033269936>🖕</emoji> **ᴏᴜᴋᴀᴀᴛ ᴍᴇ ʀᴇʜ ʟᴏᴅᴇ! ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ.**")

    # 2. Check if already running
    if chat_id in spam_chats:
        return await message.reply("<emoji id=6310044717241340733>🔄</emoji> **ᴛᴀɢ-ᴀʟʟ ɪꜱ ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ! ꜱᴛᴏᴘ ɪᴛ ꜰɪʀꜱᴛ.**")

    # 3. Dynamic Limit Checker (1, 2, or 5)
    cmd = message.command[0].lower()
    limit = 1 if cmd == "tagall1" else 5 if cmd == "tagall5" else 2

    # 4. Text & Reply Checker
    text_to_add = message.text.split(None, 1)[1] if len(message.command) > 1 else ""
    reply = message.reply_to_message

    # 5. Start The Process
    spam_chats.append(chat_id)
    
    stop_btn = InlineKeyboardMarkup([[InlineKeyboardButton("⛌ ꜱᴛᴏᴘ ᴛᴀɢᴀʟʟ ⛌", callback_data=f"stop_tag_{chat_id}")]])
    await message.reply_text(
        f"<emoji id=6123040393769521180>☄️</emoji> **ᴀɴᴜ ᴍᴀᴛʀɪx ᴛᴀɢ-ᴀʟʟ ɪɴɪᴛɪᴀᴛᴇᴅ!**\n"
        f"<emoji id=6307821174017496029>🔥</emoji> **ᴍᴏᴅᴇ:** `{limit} ᴜꜱᴇʀꜱ / ᴍᴇꜱꜱᴀɢᴇ`\n"
        f"<emoji id=5998881015320287132>💊</emoji> **ʀᴇQᴜᴇꜱᴛᴇᴅ ʙʏ:** {message.from_user.mention}",
        reply_markup=stop_btn
    )

    tags = ""
    count = 0

    try:
        async for member in client.get_chat_members(chat_id):
            if chat_id not in spam_chats:
                break
            if member.user.is_bot or member.user.is_deleted:
                continue
            
            # 💎 Clean Mention
            tags += f"[{member.user.first_name}](tg://user?id={member.user.id}) "
            count += 1
            
            # Send when limit is reached
            if count >= limit:
                final_text = f"{text_to_add}\n\n{tags}" if text_to_add else tags
                try:
                    if reply:
                        await reply.reply_text(final_text) # Replies to exact media/premium text
                    else:
                        await client.send_message(chat_id, final_text)
                except Exception:
                    pass # Skips individual errors safely
                
                await asyncio.sleep(2.5) # Anti-Flood Wait (Very Important)
                tags = ""
                count = 0
                
        # Send remaining tags if loop ends
        if tags and chat_id in spam_chats:
            final_text = f"{text_to_add}\n\n{tags}" if text_to_add else tags
            try:
                if reply:
                    await reply.reply_text(final_text)
                else:
                    await client.send_message(chat_id, final_text)
            except Exception:
                pass

    finally:
        # Cleanup when done
        if chat_id in spam_chats:
            spam_chats.remove(chat_id)
            await client.send_message(chat_id, "<emoji id=6111742817304841054>✅</emoji> **ᴛᴀɢ-ᴀʟʟ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**")


# ☠️ STOP COMMAND & BUTTON HANDLER ☠️
@app.on_message(filters.command(["tagoff", "tagstop", "stoptag"]) & filters.group)
async def stop_tag_cmd(client, message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        return await message.reply("<emoji id=4926993814033269936>🖕</emoji> **ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ꜱᴛᴏᴘ ᴛʜɪꜱ!**")
    
    if chat_id in spam_chats:
        spam_chats.remove(chat_id)
        await message.reply("<emoji id=4929369656797431200>🪐</emoji> **ᴛᴀɢ-ᴀʟʟ ᴀʙᴏʀᴛᴇᴅ ʙʏ ᴀᴅᴍɪɴ!**")
    else:
        await message.reply("<emoji id=6307605493644793241>📒</emoji> **ɴᴏ ᴛᴀɢ-ᴀʟʟ ɪꜱ ʀᴜɴɴɪɴɢ ᴄᴜʀʀᴇɴᴛʟʏ.**")


@app.on_callback_query(filters.regex(r"^stop_tag_"))
async def stop_tag_button(client, CallbackQuery):
    chat_id = int(CallbackQuery.data.split("_")[2])
    user_id = CallbackQuery.from_user.id
    
    if not await is_admin(chat_id, user_id, client):
        return await CallbackQuery.answer("🖕 Only Admins can stop this!", show_alert=True)
        
    if chat_id in spam_chats:
        spam_chats.remove(chat_id)
        await CallbackQuery.answer("🛑 Tagging Stopped Successfully!", show_alert=True)
        await CallbackQuery.edit_message_text("<emoji id=4929369656797431200>🪐</emoji> **ᴛᴀɢ-ᴀʟʟ ᴀʙᴏʀᴛᴇᴅ ʙʏ ᴀᴅᴍɪɴ!**")
    else:
        await CallbackQuery.answer("It's not running!", show_alert=True)

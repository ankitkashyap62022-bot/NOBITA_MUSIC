import asyncio
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from pyrogram.errors import FloodWait
from NOBITA_MUSIC import app

# 🛡️ THE SAFE ZONES (Yahan owner ki bhi nahi sunega bot) 🛡️
PROTECTED_GCS = [
    -1003892666526, 
    -1002688178004, 
    -1003544870055, 
    -1003201139840
]

# ==========================================
# ☠️ STEP 1: INITIATE MASS COMMANDS ☠️
# ==========================================
@app.on_message(filters.command(["banall", "unbanall", "kickall", "muteall", "unmuteall"]) & filters.group)
async def mass_action_trigger(client, message):
    chat_id = message.chat.id
    
    # 🛡️ PROTECTED GC CHECK 🛡️
    if chat_id in PROTECTED_GCS:
        return await message.reply("<emoji id=5354924568492383911>😈</emoji> **ᴏᴜᴋᴀᴀᴛ ᴍᴇ ʀᴇʜ ʟᴏᴅᴇ! ʏᴇ ᴍᴇʀᴇ ᴍᴀᴀʟɪᴋ ᴋᴀ ɢʀᴏᴜᴘ ʜᴀɪ, ʏᴀʜᴀ ᴏᴡɴᴇʀ ʙʜɪ ʙᴏʟᴇɢᴀ ᴛᴏ ʙʜɪ ᴋɪꜱɪ ᴋɪ ɢᴀɴᴅ ɴᴀʜɪ ᴍᴀʀᴜɴɢᴀ!** 🖕🗿")

    # Command details
    action = message.command[0].lower()
    user_id = message.from_user.id

    # 💎 FIRST CONFIRMATION 💎
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ ʏᴇꜱ", callback_data=f"mass_step1_{action}_{user_id}"),
            InlineKeyboardButton("❌ ɴᴏ", callback_data=f"mass_cancel_{user_id}")
        ]
    ])
    
    await message.reply(
        f"<emoji id=6307821174017496029>🔥</emoji> **ᴀʀᴇ ʏᴏᴜ ꜱᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴇxᴇᴄᴜᴛᴇ `{action.upper()}` ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ?** ❓", 
        reply_markup=keyboard
    )


# ==========================================
# ☠️ STEP 2: FIRST INLINE CONFIRMATION ☠️
# ==========================================
@app.on_callback_query(filters.regex(r"^mass_step1_"))
async def mass_step_one(client, CallbackQuery):
    data = CallbackQuery.data.split("_")
    action = data[2]
    user_id = int(data[3])

    if CallbackQuery.from_user.id != user_id:
        return await CallbackQuery.answer("🖕 Jisne command di hai, wahi click karega lode!", show_alert=True)

    # 💎 SECOND CONFIRMATION (100% SURE) 💎
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ 100% ꜱᴜʀᴇ", callback_data=f"mass_step2_{action}_{user_id}"),
            InlineKeyboardButton("❌ ᴀʙᴏʀᴛ", callback_data=f"mass_cancel_{user_id}")
        ]
    ])
    
    await CallbackQuery.edit_message_text(
        f"<emoji id=4929195195225867512>💎</emoji> **ᴀʀᴇ ʏᴏᴜ 100% ꜱᴜʀᴇ ʙᴀʙʏ? ᴇᴋ ʙᴀᴀʀ ꜱᴛᴀʀᴛ ʜᴜᴀ ᴛᴏʜ ʀᴜᴋᴇɢᴀ ɴᴀʜɪ!** ❓", 
        reply_markup=keyboard
    )


# ==========================================
# ☠️ STEP 3: EXECUTION ENGINE (ULTRA FAST) ☠️
# ==========================================
@app.on_callback_query(filters.regex(r"^mass_step2_"))
async def mass_step_two(client, CallbackQuery):
    data = CallbackQuery.data.split("_")
    action = data[2]
    user_id = int(data[3])
    chat_id = CallbackQuery.message.chat.id

    if CallbackQuery.from_user.id != user_id:
        return await CallbackQuery.answer("🖕 Apne kaam se kaam rakh!", show_alert=True)

    await CallbackQuery.edit_message_text(f"<emoji id=6123040393769521180>☄️</emoji> **ᴛᴀʀɢᴇᴛ ʟᴏᴄᴋᴇᴅ! ɪɴɪᴛɪᴀᴛɪɴɢ `{action.upper()}` ᴘʀᴏᴛᴏᴄᴏʟ... ᴍᴀᴜᴛ ᴋᴀ ɴᴀɴɢᴀ ɴᴀᴀᴄʜ ꜱᴛᴀʀᴛᴇᴅ!** 😈🍷")

    bot_me = await client.get_me()
    success = 0
    failed = 0

    # DANGEROUS LOOP STARTS HERE
    try:
        async for member in client.get_chat_members(chat_id):
            # Skip Bot itself, Admins, and Owners
            if member.user.id == bot_me.id:
                continue
            if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                continue

            try:
                if action == "banall":
                    await client.ban_chat_member(chat_id, member.user.id)
                
                elif action == "unbanall":
                    await client.unban_chat_member(chat_id, member.user.id)
                
                elif action == "kickall":
                    await client.ban_chat_member(chat_id, member.user.id)
                    await asyncio.sleep(0.5) # Slight delay to register ban before unban
                    await client.unban_chat_member(chat_id, member.user.id)
                
                elif action == "muteall":
                    await client.restrict_chat_member(chat_id, member.user.id, ChatPermissions(can_send_messages=False))
                
                elif action == "unmuteall":
                    await client.restrict_chat_member(
                        chat_id, 
                        member.user.id, 
                        ChatPermissions(
                            can_send_messages=True, 
                            can_send_media_messages=True, 
                            can_send_other_messages=True, 
                            can_add_web_page_previews=True
                        )
                    )
                
                success += 1
                await asyncio.sleep(0.2) # API FloodWait Bypass (Keeps it fast but safe)
                
            except FloodWait as e:
                # If Telegram rate-limits the bot, wait and resume
                await asyncio.sleep(e.value + 1)
            except Exception:
                failed += 1

        # FINAL REPORT
        await CallbackQuery.message.reply_text(
            f"<emoji id=6307750079423845494>👑</emoji> **{action.upper()} ᴘʀᴏᴛᴏᴄᴏʟ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!**\n\n"
            f"<emoji id=6111742817304841054>✅</emoji> **ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴛᴀʀɢᴇᴛᴇᴅ:** `{success}`\n"
            f"<emoji id=6310044717241340733>❌</emoji> **ꜰᴀɪʟᴇᴅ / ꜱᴋɪᴘᴘᴇᴅ (ᴀᴅᴍɪɴꜱ):** `{failed}`"
        )

    except Exception as e:
        await CallbackQuery.message.reply_text(f"⚠️ **Error Occurred:** `{e}`")


# ==========================================
# ☠️ CANCEL BUTTON HANDLER ☠️
# ==========================================
@app.on_callback_query(filters.regex(r"^mass_cancel_"))
async def mass_cancel(client, CallbackQuery):
    user_id = int(CallbackQuery.data.split("_")[2])
    
    if CallbackQuery.from_user.id != user_id:
        return await CallbackQuery.answer("🖕 Tu beech me mat bol!", show_alert=True)
        
    await CallbackQuery.edit_message_text("<emoji id=6152142357727811958>🦋</emoji> **ᴘʀᴏᴛᴏᴄᴏʟ ᴀʙᴏʀᴛᴇᴅ! ꜱᴀꜰᴇ ᴍᴏᴅᴇ ᴀᴄᴛɪᴠᴇ.** 💎")

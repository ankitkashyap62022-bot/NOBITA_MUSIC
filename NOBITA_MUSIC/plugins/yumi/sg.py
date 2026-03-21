import asyncio
import random

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import DeleteHistory

from NOBITA_MUSIC import userbot as us, app
from NOBITA_MUSIC.core.userbot import assistants

# ==========================================
# ☠️ ANU MATRIX PREMIUM INTEL ENGINE ☠️
# ==========================================

@app.on_message(filters.command(["sg", "sangmata", "namehistory"]))
async def premium_sg(client: Client, message: Message):
    # ☠️ SMART ARGUMENT PARSER ☠️
    target_user = None
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user.id
    elif len(message.command) > 1:
        target_user = message.command[1]
    else:
        return await message.reply_text("🪐 **Usᴀɢᴇ:**\nRᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴏʀ ᴛʏᴘᴇ `/sg [Usᴇʀɴᴀᴍᴇ/ID]`")

    # 💎 ANIMATED UI 💎
    mystic = await message.reply_text("🔄 **Iɴɪᴛɪᴀᴛɪɴɢ Sᴀɴɢᴍᴀᴛᴀ Sᴇᴀʀᴄʜ...**")

    try:
        user = await client.get_users(target_user)
    except Exception:
        return await mystic.edit_text("❌ **Iɴᴠᴀʟɪᴅ Usᴇʀ!** Pʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ Usᴇʀɴᴀᴍᴇ ᴏʀ ID.")

    bot_choices = ["sangmata_bot", "sangmata_beta_bot"]
    sg_bot = random.choice(bot_choices)

    if 1 not in assistants:
        return await mystic.edit_text("❌ **Assɪsᴛᴀɴᴛ Bᴏᴛ Nᴏᴛ Fᴏᴜɴᴅ!** Cʜᴇᴄᴋ ʏᴏᴜʀ Pʏʀᴏɢʀᴀᴍ Sᴇssɪᴏɴ.")
    
    ubot = us.one

    await mystic.edit_text("☄️ **Eхᴛʀᴀᴄᴛɪɴɢ Hɪsᴛᴏʀʏ ꜰʀᴏᴍ Dᴀᴛᴀʙᴀsᴇ...**\n*(Tʜɪs ᴍɪɢʜᴛ ᴛᴀᴋᴇ 2-3 sᴇᴄᴏɴᴅs)*")

    try:
        # Send Target ID to Sangmata
        send_msg = await ubot.send_message(sg_bot, f"{user.id}")
    except Exception as e:
        return await mystic.edit_text(f"❌ **Aᴄᴄᴇss Dᴇɴɪᴇᴅ ʙʏ Tᴇʟᴇɢʀᴀᴍ:** `{e}`")

    # ☠️ SMART DELAY (Wait for Sangmata to process) ☠️
    await asyncio.sleep(3)

    history_text = None
    # ☠️ FETCHING THE LATEST REPLY ☠️
    async for stalk in ubot.search_messages(sg_bot, limit=1):
        if not stalk.text:
            continue
        history_text = stalk.text
        break

    # 💎 CLEANUP TRACKS (Delete Chat History with Sangmata) 💎
    try:
        user_info = await ubot.resolve_peer(sg_bot)
        # In Pyrogram V2, use invoke instead of send for raw functions
        await ubot.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))
    except Exception:
        pass

    if not history_text:
        return await mystic.edit_text("⏱️ **Sᴀɴɢᴍᴀᴛᴀ ɪs Sʟᴇᴇᴘɪɴɢ ᴏʀ Sʟᴏᴡ!** Tʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.")

    # 💎 PREMIUM HTML/MARKDOWN FORMATTING 💎
    # Checking if user has no history
    if "No records found" in history_text or "No name changes" in history_text or "belum ada sejarah" in history_text.lower():
        final_text = f"🛡️ **Nᴀᴍᴇ Hɪsᴛᴏʀʏ Fᴏʀ:** {user.mention}\n\n⚠️ **Nᴏ Rᴇᴄᴏʀᴅs Fᴏᴜɴᴅ!** Tʜɪs ᴜsᴇʀ ɪs ʟᴏʏᴀʟ ᴛᴏ ᴛʜᴇɪʀ ɴᴀᴍᴇ."
    else:
        # Beautifying the raw output from Sangmata
        final_text = f"""
☠️ **Aɴᴜ Mᴀᴛʀɪx Iɴᴛᴇʟ Sᴇʀᴠɪᴄᴇ** ☠️

🎯 **Tᴀʀɢᴇᴛ:** {user.mention}
🆔 **ID:** `{user.id}`

📝 **Rᴇᴄᴏʀᴅs Fᴏᴜɴᴅ:**
<blockquote>{history_text}</blockquote>
"""

    await mystic.delete()
    await message.reply_text(final_text)


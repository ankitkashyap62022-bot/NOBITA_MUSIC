import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ParseMode
from pyrogram.errors import FloodWait

from NOBITA_MUSIC import app
from NOBITA_MUSIC.misc import SUDOERS
from NOBITA_MUSIC.utils.database import (
    get_active_chats,
    get_authuser_names,
    get_client,
    get_served_chats,
    get_served_users,
)
from NOBITA_MUSIC.utils.decorators.language import language
from NOBITA_MUSIC.utils.formatters import alpha_to_int
from config import adminlist

# ==========================================
# 💎 PREMIUM EMOJIS LOADED FROM ANU DB 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_CROWN = "<emoji id='6307750079423845494'>👑</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_BUTTERFLY = "<emoji id='6307643744623531146'>🦋</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_HEART = "<emoji id='6123125485661591081'>🩷</emoji>"
E_TICK = "<emoji id='6001589602085771497'>✅</emoji>"

IS_BROADCASTING = False

# ==========================================
# 🚀 ANU SUPREME BROADCAST SYSTEM (ALL MEDIA) ☠️
# ==========================================
@app.on_message(filters.command(["broadcast", "gcast"]) & SUDOERS)
@language
async def braodcast_message(client, message, _):
    global IS_BROADCASTING
    if IS_BROADCASTING:
        return await message.reply_text(f"{E_DEVIL} <b>Abe ruk ja! Ek broadcast pehle se chal raha hai. System ko saans lene de!</b>", parse_mode=ParseMode.HTML)

    # Variables for Message Copying or Sending
    x = message.reply_to_message.id if message.reply_to_message else None
    y = message.chat.id if message.reply_to_message else None
    query = ""

    if message.reply_to_message:
        query = message.text.split(None, 1)[1] if len(message.command) > 1 else ""
    else:
        if len(message.command) < 2:
            return await message.reply_text(f"{E_DEVIL} <b>Abe andhe! Command ke sath text ya kisi MEDIA/MESSAGE pe reply toh kar!</b>\n\n<i>Example:</i> <code>/gcast Hello -pin</code>", parse_mode=ParseMode.HTML)
        query = message.text.split(None, 1)[1]

    # Flags Setup (Smart parsing)
    is_pin = "-pin" in query
    is_pinloud = "-pinloud" in query
    is_user = "-user" in query
    is_assistant = "-assistant" in query
    is_nobot = "-nobot" in query

    # Clean the actual text to be sent (if not replying)
    clean_query = query.replace("-pinloud", "").replace("-pin", "").replace("-nobot", "").replace("-assistant", "").replace("-user", "").strip()

    if clean_query == "" and not message.reply_to_message:
        return await message.reply_text(f"{E_DEVIL} <b>Abe lode, khali message kya bheju? Kuch likh toh sahi ya kisi photo/video pe reply kar!</b>", parse_mode=ParseMode.HTML)

    IS_BROADCASTING = True
    anim = await message.reply_text(f"{E_MAGIC} <i>[ 𝗔𝗡𝗨 𝗠𝗔𝗜𝗡𝗙𝗥𝗔𝗠𝗘 ] ⇛ 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗜𝗻𝗶𝘁𝗶𝗮𝘁𝗲𝗱 (𝗠𝗲𝗱𝗶𝗮 𝗦𝘂𝗽𝗽𝗼𝗿𝘁𝗲𝗱)...</i>", parse_mode=ParseMode.HTML)

    sent_gc = 0
    pin_gc = 0
    sent_users = 0
    assistant_report = ""

    # 📡 1. G-CAST (GROUP BROADCAST - ALL MEDIA & TEXT)
    if not is_nobot:
        schats = await get_served_chats()
        for chat in schats:
            chat_id = int(chat["chat_id"])
            try:
                # 🔥 COPY_MESSAGE USE KIYA HAI = NO "FORWARDED FROM" TAG!
                m = await app.copy_message(chat_id, y, x) if message.reply_to_message else await app.send_message(chat_id, text=clean_query)
                
                # Auto Pin Logic (Bypass if no permission)
                if is_pin or is_pinloud:
                    try:
                        await m.pin(disable_notification=not is_pinloud)
                        pin_gc += 1
                    except:
                        pass # Agar power nahi hai, to silently skip kar dega
                
                sent_gc += 1
                await asyncio.sleep(0.1) # Fast but safe
            except FloodWait as fw:
                if int(fw.value) > 200:
                    continue
                await asyncio.sleep(int(fw.value))
            except:
                continue

    # 👤 2. DM CAST (USER BROADCAST)
    if is_user:
        susers = await get_served_users()
        for user in susers:
            user_id = int(user["user_id"])
            try:
                m = await app.copy_message(user_id, y, x) if message.reply_to_message else await app.send_message(user_id, text=clean_query)
                sent_users += 1
                await asyncio.sleep(0.1)
            except FloodWait as fw:
                if int(fw.value) > 200:
                    continue
                await asyncio.sleep(int(fw.value))
            except:
                continue

    # 🎧 3. ASSISTANT BROADCAST
    if is_assistant:
        from NOBITA_MUSIC.core.userbot import assistants 
        for num in assistants:
            sent_ass = 0
            client = await get_client(num)
            async for dialog in client.get_dialogs():
                try:
                    await client.copy_message(dialog.chat.id, y, x) if message.reply_to_message else await client.send_message(dialog.chat.id, text=clean_query)
                    sent_ass += 1
                    await asyncio.sleep(0.2)
                except FloodWait as fw:
                    if int(fw.value) > 200:
                        continue
                    await asyncio.sleep(int(fw.value))
                except:
                    continue
            assistant_report += f"\n   {E_BUTTERFLY} <b>Asst {num}:</b> {sent_ass} Chats"

    # ==========================================
    # 💎 FINAL PREMIUM REPORT
    # ==========================================
    final_report = f"""
{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗕 𝗥 𝗢 𝗔 𝗗 𝗖 𝗔 𝗦 𝗧  ☠️ 』</b> {E_DIAMOND}
━━━━━━━━━━━━━━━━━━━━
{E_CROWN} <b>𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗦𝘁𝗮𝘁𝘂𝘀 : 𝗖𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝗱!</b>

{E_TICK} <b>𝗚𝗿𝗼𝘂𝗽𝘀 (𝗚𝗖) :</b> {sent_gc}
📌 <b>𝗣𝗶𝗻𝗻𝗲𝗱 𝗜𝗻 :</b> {pin_gc}
👤 <b>𝗨𝘀𝗲𝗿𝘀 (𝗗𝗠) :</b> {sent_users}"""

    if is_assistant:
        final_report += f"\n\n{E_MAGIC} <b>𝗔𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝘁 𝗥𝗲𝗽𝗼𝗿𝘁:</b>{assistant_report}"

    final_report += f"\n━━━━━━━━━━━━━━━━━━━━\n{E_DEVIL} <i>𝗔𝗻𝘂 𝗠𝗮𝗶𝗻𝗳𝗿𝗮𝗺𝗲 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗘𝘅𝗲𝗰𝘂𝘁𝗲𝗱.</i> 🍷"

    await anim.edit_text(final_report, parse_mode=ParseMode.HTML)
    IS_BROADCASTING = False


# ==========================================
# 🧹 AUTO ADMIN CLEANER (Background Task)
# ==========================================
async def auto_clean():
    while not await asyncio.sleep(10):
        try:
            served_chats = await get_active_chats()
            for chat_id in served_chats:
                if chat_id not in adminlist:
                    adminlist[chat_id] = []
                    async for user in app.get_chat_members(
                        chat_id, filter=ChatMembersFilter.ADMINISTRATORS
                    ):
                        if user.privileges.can_manage_video_chats:
                            adminlist[chat_id].append(user.user.id)
                    authusers = await get_authuser_names(chat_id)
                    for user in authusers:
                        user_id = await alpha_to_int(user)
                        adminlist[chat_id].append(user_id)
        except:
            continue

asyncio.create_task(auto_clean())

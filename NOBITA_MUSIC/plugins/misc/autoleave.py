import asyncio
from datetime import datetime

from pyrogram.enums import ChatType, ParseMode
import config
from NOBITA_MUSIC import app
from NOBITA_MUSIC.core.call import NOBITA, autoend
from NOBITA_MUSIC.utils.database import get_client, is_active_chat, is_autoend

# ==========================================
# 💎 PREMIUM EMOJIS LOADED FROM ANU DB 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_CROWN = "<emoji id='6307750079423845494'>👑</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_FUCK = "<emoji id='4926993814033269936'>🖕</emoji>"

# ==========================================
# 🧹 ASSISTANT AUTO-LEAVE SYSTEM (OPTIMIZED)
# ==========================================
async def auto_leave():
    if config.AUTO_LEAVING_ASSISTANT:
        while not await asyncio.sleep(900):
            from NOBITA_MUSIC.core.userbot import assistants

            for num in assistants:
                client = await get_client(num)
                left = 0
                try:
                    async for i in client.get_dialogs():
                        if i.chat.type in [
                            ChatType.SUPERGROUP,
                            ChatType.GROUP,
                            ChatType.CHANNEL,
                        ]:
                            # 💡 FIX: Removed duplicate ID check and cleaned logic
                            if (
                                i.chat.id != config.LOGGER_ID
                                and i.chat.id != -1002344707828 # Tera VIP Support Group
                            ):
                                # 💡 FIX: CPU bachane ke liye 'continue' ki jagah 'break' lagaya
                                if left >= 20:
                                    break 
                                if not await is_active_chat(i.chat.id):
                                    try:
                                        await client.leave_chat(i.chat.id)
                                        left += 1
                                    except:
                                        continue
                except:
                    pass

asyncio.create_task(auto_leave())


# ==========================================
# 🎧 AUTO-END STREAM SYSTEM (SIGMA VIBE) ☠️
# ==========================================
async def auto_end():
    while not await asyncio.sleep(5):
        ender = await is_autoend()
        if not ender:
            continue
        for chat_id in autoend:
            timer = autoend.get(chat_id)
            if not timer:
                continue
            if datetime.now() > timer:
                if not await is_active_chat(chat_id):
                    autoend[chat_id] = {}
                    continue
                autoend[chat_id] = {}
                try:
                    # 🔥 FIX: VILLAIN ko hata kar tera NOBITA core laga diya
                    await NOBITA.stop_stream(chat_id)
                except:
                    continue
                try:
                    # ☠️ ANU EMPIRE EXTREME TOXIC MESSAGE
                    toxic_msg = f"""
{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗘 𝗠 𝗣 𝗜 𝗥 𝗘 』</b> {E_DIAMOND}
━━━━━━━━━━━━━━━━━━━━

{E_DEVIL} <b>𝗔𝗯𝗲 𝗕𝗵𝗶𝗸𝗵𝗮𝗿𝗶𝘆𝗼, 𝗩𝗖 𝗠𝗲𝗶𝗻 𝗞𝗼𝗶 𝗦𝘂𝗻𝗻𝗲 𝗪𝗮𝗹𝗮 𝗛𝗮𝗶 𝗡𝗮𝗵𝗶 𝗔𝘂𝗿 𝗕𝗼𝘁 𝗖𝗵𝗮𝗹𝗮 𝗥𝗮𝗸𝗵𝗮 𝗛𝗮𝗶!</b>

{E_CROWN} <i>𝗦𝘆𝘀𝘁𝗲𝗺 𝗡𝗲 𝗦𝘁𝗿𝗲𝗮𝗺 𝗕𝗮𝗻𝗱 𝗞𝗮𝗿 𝗗𝗶𝘆𝗮 𝗛𝗮𝗶. 𝗙𝗮𝗹𝘁𝘂 𝗠𝗲𝗶𝗻 𝗦𝗲𝗿𝘃𝗲𝗿 𝗞𝗮 𝗕𝗶𝗹𝗹 𝗠𝗮𝘁 𝗕𝗮𝗱𝗵𝗮𝗼!</i> {E_FUCK}
"""
                    await app.send_message(
                        chat_id,
                        toxic_msg,
                        parse_mode=ParseMode.HTML
                    )
                except:
                    continue

asyncio.create_task(auto_end())

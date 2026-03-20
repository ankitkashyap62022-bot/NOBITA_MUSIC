import asyncio
import importlib
import sys

from pyrogram import idle

import config
from NOBITA_MUSIC import LOGGER, app, userbot
# Imports wahi rahenge taaki folder ka structure na bigde
from NOBITA_MUSIC.core.call import NOBITA
from NOBITA_MUSIC.misc import sudo
from NOBITA_MUSIC.plugins import ALL_MODULES
from NOBITA_MUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    # ☠️ STRING SESSION CHECKER ☠️
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error(
            "☠️ [ 𝐀 𝐍 𝐔  𝐌 𝐀 𝐓 𝐑 𝐈 𝐗 ] - 𝐒𝐭𝐫𝐢𝐧𝐠 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐌𝐢𝐬𝐬𝐢𝐧𝐠! 𝐏𝐥𝐞𝐚𝐬𝐞 𝐅𝐢𝐥𝐥 𝐏𝐲𝐫𝐨𝐠𝐫𝐚𝐦 𝐕𝟐 𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐁𝐚𝐛𝐲! 🤬"
        )

    await sudo()
    
    # ☠️ DATABASE LOADER ☠️
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER(__name__).warning(f"⚠️ Database Warning: {e}")
        pass
        
    await app.start()
    
    # ==========================================
    # 💎 PREMIUM PLUGIN LOADER & CRASH PROTECTOR 💎
    # ==========================================
    for all_module in ALL_MODULES:
        try:
            importlib.import_module("NOBITA_MUSIC.plugins" + all_module)
        except Exception as e:
            # Agar ab YAML me error aayega toh bot poora crash nahi hoga, sirf yahan error dikhayega!
            LOGGER("ANU_MATRIX.plugins").error(f"⚠️ Plugin Crashed [{all_module}] : {e}")
            
    LOGGER("ANU_MATRIX.plugins").info("🦋 𝐀𝐥𝐥 𝐌𝐨𝐝𝐮𝐥𝐞𝐬 & 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲!...")
    
    await userbot.start()
    await NOBITA.start()
    await NOBITA.decorators()
    
    # ==========================================
    # ☠️ ANU MATRIX PREMIUM ASCII ART (SERVER UI) ☠️
    # ==========================================
    LOGGER("ANU_MATRIX").info(
        """
╔═════════════════════════════════════════╗
║  ☠️ 𝐀 𝐍 𝐔  𝐌 𝐀 𝐓 𝐑 𝐈 𝐗  𝐒 𝐘 𝐒 𝐓 𝐄 𝐌 ☠️  ║
║        [ 𝗦𝗲𝗿𝘃𝗲𝗿 𝗢𝗻𝗹𝗶𝗻𝗲 𝗕𝗮𝗯𝘆 ]           ║
╚═════════════════════════════════════════╝
        """
    )
    
    await idle()
    
    # ☠️ SHUTDOWN PROTOCOL ☠️
    await app.stop()
    await userbot.stop()
    LOGGER("ANU_MATRIX").info(
        """
╔═════════════════════════════════════════╗
║  💤 𝐀 𝐍 𝐔  𝐌 𝐀 𝐓 𝐑 𝐈 𝐗  𝐎 𝐅 𝐅 𝐋 𝐈 𝐍 𝐄 💤  ║
╚═════════════════════════════════════════╝
        """
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())

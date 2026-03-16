from pyrogram.types import InlineKeyboardButton

import config
from NOBITA_MUSIC import app


def start_panel(_):
    # 🔥 GROUP START BUTTONS 🔥
    buttons = [
        [
            InlineKeyboardButton(
                text="✚ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ ✚", url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text="🕸️ ᴍʏ ᴄʟᴜʙ", url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons


def private_panel(_):
    # ☠️ PRIVATE DM START BUTTONS (FIXED GC LINK) ☠️
    buttons = [
        [
            InlineKeyboardButton(
                text="✚ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴩ ✚",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            # 👑 Owner ID & 🕸️ Support Group Chat 
            InlineKeyboardButton(text="👑 ᴏᴡɴᴇʀ", user_id=config.OWNER_ID),
            InlineKeyboardButton(text="🕸️ ᴍʏ ᴄʟᴜʙ", url=config.SUPPORT_CHAT),
        ],
        [
            InlineKeyboardButton(text="🛠 ʜᴇʟᴩ & ᴄᴏᴍᴍᴀɴᴅs", callback_data="settings_back_helper")
        ],
    ]
    return buttons

from pyrogram.types import InlineKeyboardButton

import config
from NOBITA_MUSIC import app


def start_panel(_):
    # 🔥 ANU MATRIX GROUP START BUTTONS 🔥
    buttons = [
        [
            InlineKeyboardButton(
                text="🍷 ᴀᴅᴅ ᴀɴᴜ 🍷", url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text="☠️ ꜱʏꜱᴛᴇᴍ", url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons


def private_panel(_):
    # ☠️ ANU MATRIX PRIVATE DM START BUTTONS ☠️
    buttons = [
        [
            InlineKeyboardButton(
                text="🍷 ᴀᴅᴅ ᴀɴᴜ ᴛᴏ ɢʀᴏᴜᴘ 🍷",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            # 👑 Owner ID & ☠️ System Chat (Perfectly sized)
            InlineKeyboardButton(text="👑 ᴏᴡɴᴇʀ", user_id=config.OWNER_ID),
            InlineKeyboardButton(text="☠️ ꜱʏꜱᴛᴇᴍ", url=config.SUPPORT_CHAT),
        ],
        [
            InlineKeyboardButton(text="💎 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅꜱ 💎", callback_data="settings_back_helper")
        ],
    ]
    return buttons

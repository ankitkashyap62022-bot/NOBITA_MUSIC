from pyrogram.types import InlineKeyboardButton

import config
from NOBITA_MUSIC import app


def start_panel(_):
    # 🔥 ANU MATRIX GROUP START BUTTONS 🔥
    buttons = [
        [
            InlineKeyboardButton(
                text="🍷 ᴀᴅᴅ ᴀɴᴜ ᴍᴀᴛʀɪx 🍷", url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text="☠️ ꜱʏꜱᴛᴇᴍ ᴄʜᴀᴛ ☠️", url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons


def private_panel(_):
    # ☠️ ANU MATRIX PRIVATE DM START BUTTONS ☠️
    buttons = [
        [
            InlineKeyboardButton(
                text="🍷 ᴀᴅᴅ ᴀɴᴜ ᴍᴀᴛʀɪx ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ 🍷",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            # 👑 Owner ID & ☠️ System Chat 
            InlineKeyboardButton(text="👑 ꜱᴜᴘʀᴇᴍᴇ ᴄᴏᴍᴍᴀɴᴅᴇʀ", user_id=config.OWNER_ID),
            InlineKeyboardButton(text="☠️ ꜱʏꜱᴛᴇᴍ ᴄʜᴀᴛ ☠️", url=config.SUPPORT_CHAT),
        ],
        [
            InlineKeyboardButton(text="💎 ᴄᴏᴍᴍᴀɴᴅꜱ & ʜᴇʟᴘ 💎", callback_data="settings_back_helper")
        ],
    ]
    return buttons


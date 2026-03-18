from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import SUPPORT_CHAT

# ☠️ ANU MATRIX / REFLEX SYSTEM LINKS ☠️
MY_MASTER_URL = "https://t.me/Reflex_x_zara"
MY_CLUB_URL = "https://t.me/FUCK_BY_REFLEX"
OUR_SERVER_URL = "https://t.me/BMW_USERBOT_II"

def botplaylist_markup(_):
    # 🔥 PING COMMAND BUTTONS (CLEAN UI + NEW SERVER) 🔥
    buttons = [
        [
            InlineKeyboardButton(text="ᴍ ʏ . ᴄ ʟ ᴜ ʙ", url=MY_CLUB_URL),
            InlineKeyboardButton(text="ᴍ ʏ . ᴍ ᴀ s ᴛ ᴇ ʀ", url=MY_MASTER_URL),
        ],
        [
            InlineKeyboardButton(text="ᴏ ᴜ ʀ . s ᴇ ʀ ᴠ ᴇ ʀ", url=OUR_SERVER_URL),
        ],
        [
            InlineKeyboardButton(text="ᴄ ʟ ᴏ s ᴇ", callback_data="close"),
        ],
    ]
    return buttons


def close_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ᴄ ʟ ᴏ s ᴇ",
                    callback_data="close",
                ),
            ]
        ]
    )
    return upl


def supp_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ᴍ ʏ . ᴄ ʟ ᴜ ʙ",
                    url=MY_CLUB_URL,
                ),
            ]
        ]
    )
    return upl

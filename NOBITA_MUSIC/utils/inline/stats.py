from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config

def stats_buttons(_, status):
    not_sudo = [InlineKeyboardButton(text="🦋 ɴᴇᴛᴡᴏʀᴋ ꜱᴛᴀᴛꜱ", callback_data="TopOverall")]

    sudo = [
        InlineKeyboardButton(text="🪐 ꜱᴇʀᴠᴇʀ ꜱᴛᴀᴛꜱ", callback_data="bot_stats_sudo"),
        InlineKeyboardButton(text="☄️ ɴᴇᴛᴡᴏʀᴋ ꜱᴛᴀᴛꜱ", callback_data="TopOverall"),
    ]

    upl = InlineKeyboardMarkup(
        [
            sudo if status else not_sudo,
            [
                # ☠️ SYSTEM CHAT AB AKELA MAST CHAUDA DIKHEGA ☠️
                InlineKeyboardButton(text="☠️ ꜱʏꜱᴛᴇᴍ ᴄʜᴀᴛ ☠️", url=config.SUPPORT_CHAT),
            ],
            [
                # 🛑 ABORT BUTTON NEECHE WALI LINE MEIN AYEGA 🛑
                InlineKeyboardButton(text="🛑 ᴀʙᴏʀᴛ", callback_data="close"),
            ],
        ]
    )
    return upl


def back_stats_buttons(_):
    upl = InlineKeyboardMarkup(
        [
            [
                # ☠️ GC LINK BUTTON ON BACK PAGE TOO ☠️
                InlineKeyboardButton(text="☠️ ꜱʏꜱᴛᴇᴍ ᴄʜᴀᴛ ☠️", url=config.SUPPORT_CHAT),
            ],
            [
                # YE DONO CHHOTE HAIN TOH EK SATH FIT HO JAYENGE
                InlineKeyboardButton(text="🍷 ʀᴇᴛᴜʀɴ", callback_data="stats_back"),
                InlineKeyboardButton(text="🛑 ᴀʙᴏʀᴛ", callback_data="close"),
            ],
        ]
    )
    return upl

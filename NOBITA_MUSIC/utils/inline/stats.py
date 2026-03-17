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
                # ☠️ HERE IS YOUR GC LINK BUTTON ☠️
                InlineKeyboardButton(text="☠️ ꜱʏꜱᴛᴇᴍ ᴄʜᴀᴛ ☠️", url=config.SUPPORT_CHAT),
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
                InlineKeyboardButton(text="🍷 ʀᴇᴛᴜʀɴ", callback_data="stats_back"),
                InlineKeyboardButton(text="🛑 ᴀʙᴏʀᴛ", callback_data="close"),
            ],
        ]
    )
    return upl

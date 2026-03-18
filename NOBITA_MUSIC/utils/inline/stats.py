from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config

def stats_buttons(_, status):
    # ☠️ NO EMOJIS, NO SERVER STATS, CLEAN UI ☠️
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="ɴᴇᴛᴡᴏʀᴋ ꜱᴛᴀᴛꜱ", callback_data="TopOverall")],
            [InlineKeyboardButton(text="ꜱʏꜱᴛᴇᴍ ᴄʜᴀᴛ", url=config.SUPPORT_CHAT)],
            [InlineKeyboardButton(text="ᴄʟᴏꜱᴇ", callback_data="close")]
        ]
    )

def back_stats_buttons(_):
    # ☠️ YORSA SS JAISA: BACK AUR CLOSE EK SATH ☠️
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="stats_back"),
                InlineKeyboardButton(text="ᴄʟᴏꜱᴇ", callback_data="close"),
            ]
        ]
    )

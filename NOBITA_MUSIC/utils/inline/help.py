from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from NOBITA_MUSIC import app

def help_pannel(_, START: Union[bool, int] = None):
    # 🛑 Close Button Cleaned
    first = [InlineKeyboardButton(text="ᴀʙᴏʀᴛ ᴀᴄᴄᴇss", callback_data=f"close")]
    
    # 🔙 Navigation Buttons Fixed (Bug Removed)
    second = [
        InlineKeyboardButton(
            text="ᴩʀᴇᴠ",
            callback_data=f"mbot_cb",
        ),
        InlineKeyboardButton(
            text="ʜᴏᴍᴇ",
            callback_data=f"settings_back_helper", # ☠️ BUG FIXED HERE (Added '_')
        ),
        InlineKeyboardButton(
            text="ɴᴇxᴛ",
            callback_data=f"mbot_cb",
        ),
    ]
    mark = second if START else first
    
    # 💎 Clean Premium Buttons (No Cringe Emojis)
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ᴀᴅᴍɪɴ",
                    callback_data="help_callback hb1",
                ),
                InlineKeyboardButton(
                    text="ᴀᴜᴛʜ",
                    callback_data="help_callback hb2",
                ),
                InlineKeyboardButton(
                    text="ʙ-ʟɪsᴛ",
                    callback_data="help_callback hb3",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="ʙʀᴏᴀᴅ",
                    callback_data="help_callback hb4",
                ),
                InlineKeyboardButton(
                    text="ɢ-ʙᴀɴ",
                    callback_data="help_callback hb5",
                ),
                InlineKeyboardButton(
                    text="ʟ-ᴜsᴇʀ",
                    callback_data="help_callback hb6",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="ɴʏx",
                    callback_data="help_callback hb7",
                ),
                InlineKeyboardButton(
                    text="ᴩʟᴀʏ",
                    callback_data="help_callback hb8",
                ),
                InlineKeyboardButton(
                    text="ᴩ-ʟɪsᴛ",
                    callback_data="help_callback hb9",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="ᴠ-ᴄʜᴀᴛ",
                    callback_data="help_callback hb10",
                ),
                InlineKeyboardButton(
                    text="sᴛᴀᴛs",
                    callback_data="help_callback hb11",
                ),
                InlineKeyboardButton(
                    text="ᴇxᴛʀᴀ",
                    callback_data="help_callback hb12",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="sᴏɴɢ",
                    callback_data="help_callback hb13",
                ),
                InlineKeyboardButton(
                    text="sᴏᴜɴᴅ",
                    callback_data="help_callback hb14",
                ),
                InlineKeyboardButton(
                    text="ʟʏʀɪᴄ",
                    callback_data="help_callback hb15",
                ),
            ],
            mark,
        ]
    )
    return upl


def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ʙᴀᴄᴋ ᴛᴏ ᴍᴀɪɴ",
                    callback_data=f"settings_back_helper",
                ),
            ]
        ]
    )
    return upl


def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="ᴀɴᴜ ʜᴇʟᴩ ᴄᴇɴᴛᴇʀ",
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]
    return buttons

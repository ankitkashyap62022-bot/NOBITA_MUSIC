from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Union
from NOBITA_MUSIC import app

def help_pannel(_, START: Union[bool, int] = None):
    # 🛑 Close Button with Hacking Vibes
    first = [InlineKeyboardButton(text="🛑 𝛥𝐵𝛩𝑅𝑇 𝛥𝐶𝐶𝛯𝑆𝑆", callback_data=f"close")]
    
    # 🔙 Navigation Buttons
    second = [
        InlineKeyboardButton(
            text="⬅️ 𝛲𝑅𝛯𝑉",
            callback_data=f"mbot_cb",
        ),
        InlineKeyboardButton(
            text="🏘 𝐻𝛩𝑀𝛯",
            callback_data=f"settingsback_helper",
        ),
        InlineKeyboardButton(
            text="𝛮𝛯𝑋𝑇 ➡️",
            callback_data=f"mbot_cb",
        ),
    ]
    mark = second if START else first
    
    # 💎 Main Help Buttons with Premium Emojis from ANU Mainframe
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="<emoji id=5256131095094652290>🎯</emoji> 𝛥𝐷𝑀𝐼𝛮",
                    callback_data="help_callback hb1",
                ),
                InlineKeyboardButton(
                    text="<emoji id=5256134032852278918>📡</emoji> 𝛥𝑈𝑇𝐻",
                    callback_data="help_callback hb2",
                ),
                InlineKeyboardButton(
                    text="<emoji id=6089186666973500770>🎶</emoji> 𝐵-𝐿𝐼𝑆𝑇",
                    callback_data="help_callback hb3",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="<emoji id=5438436750114439411>🏴‍☠️</emoji> 𝐵𝑅𝛩𝛥𝐷",
                    callback_data="help_callback hb4",
                ),
                InlineKeyboardButton(
                    text="<emoji id=5235985147265837746>🗒</emoji> 𝐺-𝐵𝛥𝛮",
                    callback_data="help_callback hb5",
                ),
                InlineKeyboardButton(
                    text="<emoji id=5195046451008257595>😏</emoji> 𝐿-𝑈𝑆𝛯𝑅",
                    callback_data="help_callback hb6",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="<emoji id=6194905702121609083>👺</emoji> 𝛮𝑌𝑋",
                    callback_data="help_callback hb7",
                ),
                InlineKeyboardButton(
                    text="<emoji id=6307358404176254008>🔥</emoji> 𝛲𝐿𝛥𝑌",
                    callback_data="help_callback hb8",
                ),
                InlineKeyboardButton(
                    text="<emoji id=4929201667741582387>⌚️</emoji> 𝛲-𝐿𝐼𝑆𝑇",
                    callback_data="help_callback hb9",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="<emoji id=6307373208928531138>😈</emoji> 𝑉-𝐶𝐻𝛥𝑇",
                    callback_data="help_callback hb10",
                ),
                InlineKeyboardButton(
                    text="<emoji id=6309709550878463216>🌟</emoji> 𝑆𝑇𝛥𝑇𝑆",
                    callback_data="help_callback hb11",
                ),
                InlineKeyboardButton(
                    text="<emoji id=5415655814079723871>🔝</emoji> 𝛯𝑋𝑇𝑅𝛥",
                    callback_data="help_callback hb12",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="<emoji id=6195199052682893171>𝪑</emoji> 𝑆𝛩𝛮𝐺",
                    callback_data="help_callback hb13",
                ),
                InlineKeyboardButton(
                    text="<emoji id=6201778989825006827>✅</emoji> 𝑆𝛩𝑈𝛮𝐷",
                    callback_data="help_callback hb14",
                ),
                InlineKeyboardButton(
                    text="<emoji id=5258500400918587241>✍️</emoji> 𝐿𝑌𝑅𝐼𝐶",
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
                    text="⬅️ 𝐵𝛥𝐶𝐾 𝑇𝛩 𝑀𝛥𝐼𝛮𝛥𝑀𝛯",
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
                text="<emoji id=6310024990456550445>🌟</emoji> 𝛥𝛮𝑈 𝛨𝛯𝐿𝛲 𝐶𝛯𝛮𝑇𝛯𝑅",
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]
    return buttons

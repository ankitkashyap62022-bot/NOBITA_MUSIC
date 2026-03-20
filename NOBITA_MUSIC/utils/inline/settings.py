from typing import Union
from pyrogram.types import InlineKeyboardButton

# ==========================================
# ⚙️ ANU EMPIRE : INLINE SETTINGS UI ☠️
# ==========================================

def setting_markup(_):
    # 💡 Jyada lamba na ho, isliye Playmode aur Vote Mode ko ek hi line me kar diya!
    buttons = [
        [
            InlineKeyboardButton(text=f"👑 {_['ST_B_1']}", callback_data="AU"),
            InlineKeyboardButton(text=f"🦋 {_['ST_B_3']}", callback_data="LG"),
        ],
        [
            InlineKeyboardButton(text=f"⚙️ {_['ST_B_2']}", callback_data="PM"),
            InlineKeyboardButton(text=f"🗳️ {_['ST_B_4']}", callback_data="VM"),
        ],
        [
            InlineKeyboardButton(text=f"❌ {_['CLOSE_BUTTON']}", callback_data="close"),
        ],
    ]
    return buttons


def vote_mode_markup(_, current, mode: Union[bool, str] = None):
    buttons = [
        [
            InlineKeyboardButton(text="✨ 𝗩𝗼𝘁𝗶𝗻𝗴 𝗠𝗼𝗱𝗲", callback_data="VOTEANSWER"),
            InlineKeyboardButton(
                text=f"✅ {_['ST_B_5']}" if mode == True else f"❌ {_['ST_B_6']}",
                callback_data="VOMODECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(text="➖ 2", callback_data="FERRARIUDTI M"),
            InlineKeyboardButton(
                text=f"📊 𝗖𝘂𝗿𝗿𝗲𝗻𝘁 : {current}",
                callback_data="ANSWERVOMODE",
            ),
            InlineKeyboardButton(text="➕ 2", callback_data="FERRARIUDTI A"),
        ],
        [
            InlineKeyboardButton(
                text=f"🔙 {_['BACK_BUTTON']}",
                callback_data="settings_helper",
            ),
            InlineKeyboardButton(text=f"❌ {_['CLOSE_BUTTON']}", callback_data="close"),
        ],
    ]
    return buttons


def auth_users_markup(_, status: Union[bool, str] = None):
    buttons = [
        [
            InlineKeyboardButton(text=f"🛡️ {_['ST_B_7']}", callback_data="AUTHANSWER"),
            InlineKeyboardButton(
                text=f"✅ {_['ST_B_8']}" if status == True else f"❌ {_['ST_B_9']}",
                callback_data="AUTH",
            ),
        ],
        [
            InlineKeyboardButton(text=f"📜 𝗔𝘂𝘁𝗵 𝗟𝗶𝘀𝘁", callback_data="AUTHLIST"),
        ],
        [
            InlineKeyboardButton(
                text=f"🔙 {_['BACK_BUTTON']}",
                callback_data="settings_helper",
            ),
            InlineKeyboardButton(text=f"❌ {_['CLOSE_BUTTON']}", callback_data="close"),
        ],
    ]
    return buttons


def playmode_users_markup(
    _,
    Direct: Union[bool, str] = None,
    Group: Union[bool, str] = None,
    Playtype: Union[bool, str] = None,
):
    buttons = [
        [
            InlineKeyboardButton(text=f"🔍 {_['ST_B_10']}", callback_data="SEARCHANSWER"),
            InlineKeyboardButton(
                text=f"✅ {_['ST_B_11']}" if Direct == True else f"❌ {_['ST_B_12']}",
                callback_data="MODECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(text=f"👑 {_['ST_B_13']}", callback_data="AUTHANSWER"),
            InlineKeyboardButton(
                text=f"✅ {_['ST_B_8']}" if Group == True else f"❌ {_['ST_B_9']}",
                callback_data="CHANNELMODECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(text=f"🎵 {_['ST_B_14']}", callback_data="PLAYTYPEANSWER"),
            InlineKeyboardButton(
                text=f"✅ {_['ST_B_8']}" if Playtype == True else f"❌ {_['ST_B_9']}",
                callback_data="PLAYTYPECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(
                text=f"🔙 {_['BACK_BUTTON']}",
                callback_data="settings_helper",
            ),
            InlineKeyboardButton(text=f"❌ {_['CLOSE_BUTTON']}", callback_data="close"),
        ],
    ]
    return buttons

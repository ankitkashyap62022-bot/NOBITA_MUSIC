from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from NOBITA_MUSIC import app
from NOBITA_MUSIC.utils.database import get_lang, set_lang
from NOBITA_MUSIC.utils.decorators import ActualAdminCB, language, languageCB
from config import BANNED_USERS
from strings import get_string, languages_present

# ==========================================
# 💎 BOSS KE KHUD KE PREMIUM HTML EMOJIS 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_CROWN = "<emoji id='6307750079423845494'>👑</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_LANG = "<emoji id='5041955142060999726'>🌈</emoji>"
E_CROSS = "<emoji id='4926993814033269936'>🖕</emoji>"

# ==========================================
# 🛠️ PURE PYROGRAM KEYBOARD GENERATOR ☠️
# ==========================================
def lanuages_keyboard(_):
    # 🔥 FIX: Removed third-party 'pykeyboard'. Using native Pyrogram list logic!
    buttons = []
    temp_row = []
    
    for i in languages_present:
        temp_row.append(
            InlineKeyboardButton(text=languages_present[i], callback_data=f"languages:{i}")
        )
        if len(temp_row) == 2:  # 2 buttons per row
            buttons.append(temp_row)
            temp_row = []
            
    if temp_row:
        buttons.append(temp_row)

    buttons.append([
        InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper"),
        InlineKeyboardButton(text="🗑 𝗖𝗹𝗼𝘀𝗲", callback_data="close"),
    ])
    
    return InlineKeyboardMarkup(buttons)

# ==========================================
# 🚀 ANU SUPREME LANGUAGE COMMAND ☠️
# ==========================================
@app.on_message(filters.command(["lang", "setlang", "language"]) & ~BANNED_USERS)
@language
async def langs_command(client, message: Message, _):
    keyboard = lanuages_keyboard(_)
    
    # 💎 Premium VIP Formatting
    premium_text = f"""
{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗟 𝗔 𝗡 𝗚 𝗨 𝗔 𝗚 𝗘  』</b> {E_DIAMOND}
━━━━━━━━━━━━━━━━━━━━
{E_LANG} <b>𝗔𝗽𝗻𝗶 𝗕𝗵𝗮𝘀𝗵𝗮 𝗖𝗵𝘂𝗻𝗶𝘆𝗲 :</b>
<i>Select your preferred language for the bot from the buttons below!</i>

{E_DEVIL} <i>Anu Empire Matrix.</i>
━━━━━━━━━━━━━━━━━━━━
"""
    await message.reply_text(
        premium_text,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )


@app.on_callback_query(filters.regex("LG") & ~BANNED_USERS)
@languageCB
async def lanuagecb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"languages:(.*?)") & ~BANNED_USERS)
@ActualAdminCB
async def language_markup(client, CallbackQuery, _):
    langauge = (CallbackQuery.data).split(":")[1]
    old = await get_lang(CallbackQuery.message.chat.id)
    
    if str(old) == str(langauge):
        return await CallbackQuery.answer(f"⚠️ {_['lang_4']}", show_alert=True)
        
    try:
        _ = get_string(langauge)
        await CallbackQuery.answer(f"✅ {_['lang_2']}", show_alert=True)
    except:
        _ = get_string(old)
        return await CallbackQuery.answer(f"{E_CROSS} {_['lang_3']}", show_alert=True)
        
    await set_lang(CallbackQuery.message.chat.id, langauge)
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)

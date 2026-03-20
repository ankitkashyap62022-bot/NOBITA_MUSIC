from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, Message

from NOBITA_MUSIC import app
from NOBITA_MUSIC.utils.database import get_playmode, get_playtype, is_nonadmin_chat
from NOBITA_MUSIC.utils.decorators import language
from NOBITA_MUSIC.utils.inline.settings import playmode_users_markup
from config import BANNED_USERS

# ==========================================
# 💎 PREMIUM EMOJIS LOADED FROM ANU DB 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_CROWN = "<emoji id='6307750079423845494'>👑</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"

# ==========================================
# 🚀 ANU SUPREME PLAYMODE MENU ☠️
# ==========================================
@app.on_message(
    # 🔥 BUG FIX: Removed empty string "" and random symbols. Ab bot spam nahi karega!
    filters.command(["playmode", "mode"], prefixes=["/", "!", "."])
    & filters.group
    & ~BANNED_USERS
)
@language
async def playmode_(client, message: Message, _):
    playmode = await get_playmode(message.chat.id)
    Direct = True if playmode == "Direct" else None
    
    is_non_admin = await is_nonadmin_chat(message.chat.id)
    Group = True if not is_non_admin else None
    
    playty = await get_playtype(message.chat.id)
    Playtype = None if playty == "Everyone" else True
    
    buttons = playmode_users_markup(_, Direct, Group, Playtype)
    
    # 💎 Premium Anu UI Text
    premium_text = f"{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗣 𝗟 𝗔 𝗬 𝗠 𝗢 𝗗 𝗘 』</b> {E_DIAMOND}\n━━━━━━━━━━━━━━━━━━━━\n"
    premium_text += f"{E_CROWN} <b>𝗖𝗵𝗮𝘁 :</b> {message.chat.title}\n\n"
    premium_text += f"{E_DEVIL} <i>𝗔𝗻𝘂 𝗦𝘆𝘀𝘁𝗲𝗺 𝗔𝗰𝗰𝗲𝘀𝘀 𝗚𝗿𝗮𝗻𝘁𝗲𝗱. 𝗔𝗽𝗻𝗶 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀 𝗖𝗼𝗻𝗳𝗶𝗴𝘂𝗿𝗲 𝗞𝗮𝗿!</i>"

    response = await message.reply_text(
        premium_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.HTML
    )

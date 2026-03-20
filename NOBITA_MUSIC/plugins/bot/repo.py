from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ParseMode
from NOBITA_MUSIC import app
from config import BOT_USERNAME
from NOBITA_MUSIC.utils.errors import capture_err

# ==========================================
# 💎 PREMIUM EMOJIS LOADED FROM ANU DB 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_CROWN = "<emoji id='6307750079423845494'>👑</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_BUTTERFLY = "<emoji id='6307643744623531146'>🦋</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_HEART = "<emoji id='6123125485661591081'>🩷</emoji>"

# Default Pic (Agar tu set karna bhool jaye)
ANU_REPO_PIC = "https://files.catbox.moe/tcz7s6.jpg"

# ==========================================
# 💀 EXTREME TOXIC SIGMA UI TEXT ☠️
# ==========================================
start_txt = f"""
{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗘 𝗠 𝗣 𝗜 𝗥 𝗘  ☠️ 』</b> {E_DIAMOND}
━━━━━━━━━━━━━━━━━━━━

{E_DEVIL} <b>𝗔𝗯𝗲 𝗕𝗵𝗶𝗸𝗵𝗮𝗿𝗶, 𝗥𝗲𝗽𝗼 𝗖𝗵𝗮𝗵𝗶𝘆𝗲 𝗧𝘂𝗷𝗵𝗲? 😂</b>
{E_CROWN} <b>𝗧𝗲𝗿𝗶 𝗔𝘂𝗸𝗮𝗮𝘁 𝗡𝗮𝗵𝗶 𝗛𝗮𝗶 𝗔𝗻𝘂 𝗠𝗮𝘁𝗿𝗶𝘅 𝗞𝗼 𝗛𝗮𝗮𝘁𝗵 𝗟𝗮𝗴𝗮𝗻𝗲 𝗞𝗶!</b>

⇛ <b>𝗖𝗵𝘂𝗽𝗰𝗵𝗮𝗽 𝗣𝗮𝗽𝗮 𝗕𝗼𝗹:</b> <a href='https://t.me/MONSTER_FUCK_BITCHES'>@MONSTER_FUCK_BITCHES</a>
⇛ <b>𝗪𝗮𝗿𝗻𝗮 𝗦𝘆𝘀𝘁𝗲𝗺 𝗙𝗮𝗮𝗱 𝗗𝗶𝘆𝗮 𝗝𝗮𝘆𝗲𝗴𝗮! 🖕💀</b>

{E_MAGIC} <b>𝗠𝗮𝗶𝗻 𝗕𝗼𝘁 :</b> @ANU_X_USERBOT
{E_BUTTERFLY} <b>𝗡𝗲𝘁𝘄𝗼𝗿𝗸 :</b> <a href='https://t.me/FUCK_BY_REFLEX'>𝗔𝗻𝘂 𝗠𝗮𝗶𝗻𝗳𝗿𝗮𝗺𝗲</a>

{E_HEART} <i>"𝗕𝗮𝗮𝗽 𝗕𝗮𝗮𝗽 𝗛𝗼𝘁𝗮 𝗛𝗮𝗶, 𝗢𝗿 𝗔𝗻𝘂 𝗦𝗮𝗯𝗸𝗮 𝗕𝗮𝗮𝗽 𝗛𝗮𝗶." 🍷</i>
━━━━━━━━━━━━━━━━━━━━
"""

# ==========================================
# 📸 COMMAND TO SET CUSTOM REPO PIC
# ==========================================
@app.on_message(filters.command("setrepopic") & filters.user("MONSTER_FUCK_BITCHES"))
async def set_repo_pic(_, msg):
    global ANU_REPO_PIC
    if not msg.reply_to_message or not msg.reply_to_message.photo:
        return await msg.reply_text(f"{E_DEVIL} <b>Abe andhe lode! 🤬 Bina photo ke command pel raha hai? Kisi image pe reply kar warna system hack kar lunga tera!</b>", parse_mode=ParseMode.HTML)
    
    # Save the new photo ID
    ANU_REPO_PIC = msg.reply_to_message.photo.file_id
    await msg.reply_text(f"{E_CROWN} <b>Anu Mainframe: Repo Pic Successfully Updated! 🍷</b>\n\n<i>Ab in bhikhariyo ko yahi pic dikhegi!</i> {E_HEART}", parse_mode=ParseMode.HTML)


# ==========================================
# 🚀 REPO COMMAND
# ==========================================
@app.on_message(filters.command("repo"))
async def repo_cmd(_, msg):
    buttons = [
        [ 
          InlineKeyboardButton("🦋 𝗔𝗱ᴅ 𝗠ᴇ 𝗜ɴ 𝗬ᴏᴜʀ 𝗚ʀᴏᴜᴘ 🦋", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ],
        [
          InlineKeyboardButton("💎 𝗔𝘂𝗸𝗮𝗮𝘁 𝗖𝗵𝗲𝗰𝗸 (𝗛𝗲𝗹𝗽)", url="https://t.me/BMW_USERBOT_II"),
          InlineKeyboardButton("👑 𝗕𝗮𝗮𝗽 (𝗢𝘄𝗻𝗲𝗿)", url="https://t.me/MONSTER_FUCK_BITCHES"),
        ],
        [
          InlineKeyboardButton("😈 𝗔𝗻𝘂 𝗦𝘂𝗽𝗽𝗼𝗿𝘁", url="https://t.me/FUCK_BY_REFLEX"),
          InlineKeyboardButton("✨ 𝗦𝘆𝘀𝘁𝗲𝗺 𝗖𝗼𝗿𝗲", url="https://t.me/ANU_X_USERBOT"),
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    try:
        await msg.reply_photo(
            photo=ANU_REPO_PIC,
            caption=start_txt,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML # Important for premium emojis
        )
    except Exception as e:
        capture_err(e)

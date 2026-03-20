import random
import re
from pyrogram import filters
from pyrogram.enums import ParseMode
from NOBITA_MUSIC import app

# ==========================================
# 💎 PREMIUM EMOJIS LOADED FROM ANU DB 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_CROWN = "<emoji id='6307750079423845494'>👑</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_SLEEP = "<emoji id='6309739370836399696'>🌙</emoji>"
E_HEART = "<emoji id='6123125485661591081'>🩷</emoji>"

# 🎭 Premium Stickers
STICKERS = [
    "CAACAgQAAx0Ce9_hCAACaEVlwn7HeZhgwyVfKHc3WUGC_447IAACLgwAAkQwKVPtub8VAR018x4E",
    "CAACAgIAAx0Ce9_hCAACaEplwn7dvj7G0-a1v3wlbN281RMX2QACUgwAAligOUoi7DhLVTsNsh4E",
    "CAACAgIAAx0Ce9_hCAACaFBlwn8AAZNB9mOUvz5oAyM7CT-5pjAAAtEKAALa7NhLvbTGyDLbe1IeBA",
    "CAACAgUAAx0CcmOuMwACldVlwn9ZHHF2-S-CuMSYabwwtVGC3AACOAkAAoqR2VYDjyK6OOr_Px4E",
    "CAACAgIAAx0Ce9_hCAACaFVlwn-fG58GKoEmmZpVovxEj4PodAACfwwAAqozQUrt2xSTf5Ac4h4E",
]

# ☠️ Toxic/Sigma Goodnight Dialogues
TOXIC_TEXTS = [
    f"<b>𝗖𝗵𝗮𝗹 𝗻𝗶𝗸𝗮𝗹 𝗮𝗯, 𝗰𝗵𝘂𝗽 𝗰𝗵𝗮𝗽 𝘀𝗼 𝗷𝗮!</b>\n<i>Faltu jag ke net mat phoonk...</i>",
    f"<b>𝗔𝗻𝘂 𝗠𝗮𝘁𝗿𝗶𝘅 𝗦𝗹𝗲𝗲𝗽 𝗠𝗼𝗱𝗲 𝗔𝗰𝘁𝗶𝘃𝗮𝘁𝗲𝗱.</b>\n<i>System off kar aur so ja lode!</i>",
    f"<b>𝗚𝗼𝗼𝗱 𝗡𝗶𝗴𝗵𝘁!</b>\n<i>Sote waqt Anu Empire ke baare me hi sochna!</i>",
    f"<b>𝗣𝘂𝗿𝗮 𝗱𝗶𝗻 𝘄𝗮𝘀𝘁𝗲 𝗸𝗮𝗿𝗸𝗲 𝗮𝗯 𝘀𝗼𝗻𝗲 𝗷𝗮 𝗿𝗮𝗵𝗮 𝗵𝗮𝗶?</b>\n<i>Sleep tight, nithalle!</i>"
]

# ==========================================
# 🚀 ANU SUPREME GOODNIGHT SYSTEM ☠️
# ==========================================
# 🔥 BUG FIX: Using Regex for smart detection without slash commands!
@app.on_message(filters.regex(r"(?i)^\s*(gn|good\s*night|goodnight|oodnight)\s*$") & ~filters.bot)
async def goodnight_command_handler(client, message):
    sender = message.from_user.mention
    
    # Randomly decide between sending a sticker OR a premium text response
    action = random.choice(["sticker", "text"])
    
    try:
        if action == "sticker":
            # Sends only sticker as a reply (Cleaner UI)
            sticker_id = random.choice(STICKERS)
            await message.reply_sticker(sticker=sticker_id)
            
        else:
            # Sends Premium Text with Toxic Dialogues
            random_text = random.choice(TOXIC_TEXTS)
            premium_reply = f"""
{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗡 𝗜 𝗚 𝗛 𝗧  』</b> {E_DIAMOND}
━━━━━━━━━━━━━━━━━━━━
{E_SLEEP} {sender}, {random_text} {E_DEVIL}
━━━━━━━━━━━━━━━━━━━━
"""
            await message.reply_text(premium_reply, parse_mode=ParseMode.HTML)
            
    except Exception as e:
        # Failsafe silently so bot never crashes
        pass

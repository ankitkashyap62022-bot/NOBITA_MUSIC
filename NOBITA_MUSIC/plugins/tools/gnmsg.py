import random
from pyrogram import filters
from pyrogram.enums import ParseMode
from NOBITA_MUSIC import app

# ==========================================
# 💎 BOSS KE KHUD KE PREMIUM EMOJIS 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_SLEEP = "<emoji id='6309739370836399696'>🌙</emoji>"
E_FINGER = "<emoji id='4926993814033269936'>🖕</emoji>"
E_STAR = "<emoji id='5352870513267973607'>✨</emoji>"

# ☠️ EXTREME TOXIC / ROASTING DIALOGUES (Gali Vibes) 🤬
TOXIC_TEXTS = [
    f"<b>So ja lode! Subah uth ke phir se wahi nallapanti karni hai tujhe!</b>",
    f"<b>Bada aaya Good Night bolne wala, shakal dekhi hai apni? Chup chap so ja!</b>",
    f"<b>Chal nikal ab, dimaag mat kha yaha!</b> {E_FINGER}",
    f"<b>Pura din waste karke ab sone ja raha hai berozgar? Padhle bsdk!</b>",
    f"<b>Good night? Teri zindagi me waise bhi andhera hi hai, ja so ja!</b>",
    f"<b>System off kar aur nikal yaha se! Faltu jag ke net mat phoonk nithalle!</b> {E_DEVIL}"
]

# ==========================================
# 🚀 ANU SUPREME TOXIC GOODNIGHT SYSTEM ☠️
# ==========================================
@app.on_message(filters.regex(r"(?i)^\s*(gn|good\s*night|goodnight|oodnight)\s*$") & ~filters.bot)
async def goodnight_command_handler(client, message):
    sender = message.from_user.mention
    
    # Picks a random roasting text
    random_text = random.choice(TOXIC_TEXTS)
    
    # 💎 PREMIUM UI Formatting
    premium_reply = f"""
{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗡 𝗜 𝗚 𝗛 𝗧  』</b> {E_DIAMOND}
━━━━━━━━━━━━━━━━━━━━
{E_SLEEP} {sender}, {random_text}
━━━━━━━━━━━━━━━━━━━━
"""
    try:
        await message.reply_text(premium_reply, parse_mode=ParseMode.HTML)
    except Exception:
        # Failsafe silently so bot never crashes
        pass

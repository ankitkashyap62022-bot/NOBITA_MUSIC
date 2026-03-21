import random
import asyncio
import hashlib
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from NOBITA_MUSIC import app

# ==========================================
# 💎 BOSS KE KHUD KE PREMIUM HTML EMOJIS 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_CROSS = "<emoji id='4926993814033269936'>🖕</emoji>"
E_LOAD = "<emoji id='6310044717241340733'>🔄</emoji>"
E_HEART = "<emoji id='6298684666182371615'>❤️</emoji>"
E_HEART_PINK = "<emoji id='6154635934135490309'>💗</emoji>"
E_SPARKLE_HEART = "<emoji id='5999210495146465994'>💖</emoji>"
E_FIRE = "<emoji id='6307821174017496029'>🔥</emoji>"

# ==========================================
# ☠️ ANU MATRIX PREMIUM SOULMATE ENGINE ☠️
# ==========================================
def get_premium_message(love_percentage):
    if love_percentage <= 30:
        return [
            f"{E_CROSS} <b>Abe kat jayega tera! Padhai pe dhyan de lode!</b>",
            f"{E_CROSS} <b>Ghanta love! Friendzone me marega tu! 😂</b>",
            f"{E_CROSS} <b>Shakal dekhi hai apni aaine me? Move on kar!</b>"
        ]
    elif love_percentage <= 60:
        return [
            f"{E_HEART_PINK} <b>Kuch chance hai, par paisa kharch karna padega! 💸</b>",
            f"{E_HEART_PINK} <b>Timepass theek chal raha hai, jyada ummid mat rakh!</b>",
            f"{E_HEART_PINK} <b>50-50 wala scene hai! Ek aadh saal me pata chal jayega!</b>"
        ]
    elif love_percentage <= 85:
        return [
            f"{E_HEART} <b>Bhai ka setting pakka ho gaya lagta hai! 🔥</b>",
            f"{E_HEART} <b>Chemistry badhiya hai, ab shadi ka card bhej dena!</b>",
            f"{E_HEART} <b>Oho! Full Ashiqui baazi chal rahi hai yaha toh! 😍</b>"
        ]
    else:
        return [
            f"{E_SPARKLE_HEART} <b>Made for each other! Ekdum Nibba-Nibbi pro max! 💍</b>",
            f"{E_SPARKLE_HEART} <b>Soulmates detected! Jalao auro ko bsdk! 😂</b>",
            f"{E_SPARKLE_HEART} <b>100% Pure Love! Bhai ne aukaat se baahar setting ki hai!</b>"
        ]

@app.on_message(filters.command(["love", "couple", "match"]))
async def premium_love_command(client, message: Message):
    if len(message.command) < 3:
        return await message.reply_text(
            f"{E_DEVIL} <b>Abe lode! Kiska kiske sath check karna hai naam toh likh!</b>\n{E_MAGIC} <b>Exᴀᴍᴘʟᴇ:</b> <code>/love Anu Boss</code>",
            parse_mode=ParseMode.HTML
        )

    name1 = message.command[1].strip()
    name2 = " ".join(message.command[2:]).strip()

    # 💎 CLEAN ANIMATION START (NO EDIT BUG) 💎
    mystic = await message.reply_text(f"{E_LOAD} <b>Anu Mainframe: Scanning Kundali & Heartbeats...</b>", parse_mode=ParseMode.HTML)
    await asyncio.sleep(1.5)
    
    try:
        # ☠️ SOULMATE HASH ALGORITHM ☠️
        # Generates the exact same percentage every time for the same pair!
        seed_string = "".join(sorted([name1.lower(), name2.lower()]))
        hash_val = int(hashlib.md5(seed_string.encode()).hexdigest(), 16)
        love_percentage = (hash_val % 91) + 10  # Generates 10 to 100%

        love_message = random.choice(get_premium_message(love_percentage))

        # 💎 FINAL RESPONSE WITH PREMIUM EMOJIS 💎
        final_text = f"""
{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗟 𝗢 𝗩 𝗘  𝗠 𝗘 𝗧 𝗘 𝗥 』</b> {E_DIAMOND}
━━━━━━━━━━━━━━━━━━━━

💖 <b>Nᴀᴍᴇ 1:</b> <code>{name1}</code>
💖 <b>Nᴀᴍᴇ 2:</b> <code>{name2}</code>

{E_FIRE} <b>Lᴏᴠᴇ Pᴇʀᴄᴇɴᴛᴀɢᴇ:</b> <code>{love_percentage}%</code>

{love_message}
━━━━━━━━━━━━━━━━━━━━
"""
        
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("✨ 𝗧𝗿𝘆 𝗬𝗼𝘂𝗿 𝗠𝗮𝘁𝗰𝗵 ✨", switch_inline_query_current_chat="")]]
        )

        # Deleting old loading msg to prevent Parse Mode edit bugs
        await mystic.delete()
        await message.reply_text(final_text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

    except Exception as e:
        await message.reply_text(f"{E_CROSS} <b>Anu System Fucked Up:</b>\n<code>{e}</code>", parse_mode=ParseMode.HTML)

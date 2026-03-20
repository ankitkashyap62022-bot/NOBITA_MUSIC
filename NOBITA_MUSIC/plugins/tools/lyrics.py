import random
import re
import string
import asyncio

import lyricsgenius as lg
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BANNED_USERS, lyrical
from strings import get_command
from NOBITA_MUSIC import app
from NOBITA_MUSIC.utils.decorators.language import language

# ==========================================
# 💎 BOSS KE KHUD KE PREMIUM HTML EMOJIS 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_CROSS = "<emoji id='4926993814033269936'>🖕</emoji>"
E_MUSIC = "<emoji id='6307569802466563145'>🎶</emoji>"
E_LOAD = "<emoji id='6310044717241340733'>🔄</emoji>"

###Commands
LYRICS_COMMAND = get_command("LYRICS_COMMAND")

# Genius API Setup
api_key = "Vd9FvPMOKWfsKJNG9RbZnItaTNIRFzVyyXFdrGHONVsGqHcHBoj3AI3sIlNuqzuf0ZNG8uLcF9wAd5DXBBnUzA"
y = lg.Genius(
    api_key,
    skip_non_songs=True,
    excluded_terms=["(Remix)", "(Live)"],
    remove_section_headers=True,
)
y.verbose = False

# 🛠️ Helper function to run Genius Sync search in Async background thread
def search_lyrics_sync(title):
    return y.search_song(title, get_full_info=False)


# ==========================================
# 🚀 ANU SUPREME LYRICS EXTRACTOR ☠️
# ==========================================
@app.on_message(filters.command(LYRICS_COMMAND) & ~BANNED_USERS)
@language
async def lrsearch(client, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text(
            f"{E_DEVIL} <b>Abe Lode! Gaane ka naam toh likh! Kiska lyrics nikalun?</b>\n{E_MAGIC} <i>Example:</i> <code>/lyrics Tum Hi Ho</code>", 
            parse_mode=ParseMode.HTML
        )
        
    title = message.text.split(None, 1)[1]
    m = await message.reply_text(f"{E_LOAD} <i>Anu Mainframe: Extracting Lyrics for '{title}'...</i>", parse_mode=ParseMode.HTML)
    
    try:
        # 🔥 FIX: Threading lagaya taaki bot hang na ho!
        S = await asyncio.to_thread(search_lyrics_sync, title)
        
        if S is None:
            return await m.edit_text(f"{E_CROSS} <b>Anu Error:</b> <i>Bhai ye kaisa kachra gaana hai? Genius database me iska koi wajood nahi!</i>", parse_mode=ParseMode.HTML)
            
        ran_hash = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        lyric = S.lyrics
        if "Embed" in lyric:
            lyric = re.sub(r"\d*Embed", "", lyric)
            
        lyrical[ran_hash] = lyric
        
        # 💎 PREMIUM UI FORMATTING
        premium_text = f"""
{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗟 𝗬 𝗥 𝗜 𝗖 𝗦 』</b> {E_DIAMOND}
━━━━━━━━━━━━━━━━━━━━

{E_MUSIC} <b>𝗦𝗼𝗻𝗴 𝗙𝗼𝘂𝗻𝗱 :</b> <code>{S.title}</code>
🎤 <b>𝗔𝗿𝘁𝗶𝘀𝘁 :</b> <code>{S.artist}</code>

{E_MAGIC} <i>Gaane ke bol padhne ke liye niche wala button daba!</i>
━━━━━━━━━━━━━━━━━━━━
"""
        upl = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="📖 𝗥𝗲𝗮𝗱 𝗟𝘆𝗿𝗶𝗰𝘀",
                        url=f"https://t.me/{app.username}?start=lyrics_{ran_hash}",
                    ),
                ]
            ]
        )
        await m.edit_text(premium_text, reply_markup=upl, parse_mode=ParseMode.HTML)
        
    except Exception as e:
        await m.edit_text(f"{E_CROSS} <b>System Fucked Up:</b>\n<pre>{str(e)}</pre>", parse_mode=ParseMode.HTML)

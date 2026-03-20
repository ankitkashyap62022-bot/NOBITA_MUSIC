import re
import aiohttp
from pyrogram import filters
from pyrogram.enums import ParseMode

from NOBITA_MUSIC import app
from config import LOGGER_ID

# ==========================================
# 💎 FRESH VIP EMOJIS FOR INSTA PLUGIN 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_FINGER = "<emoji id='4926993814033269936'>🖕</emoji>"
E_LOAD = "<emoji id='6310044717241340733'>🔄</emoji>"    # Rotating load emoji
E_INSTA = "<emoji id='6307447640711763730'>💟</emoji>"   # Pink heart for Insta
E_FLASH = "<emoji id='6123040393769521180'>☄️</emoji>"   # Comet/Flash

# ==========================================
# 🚀 ANU SUPREME INSTA DOWNLOADER ☠️
# ==========================================
@app.on_message(filters.command(["ig", "instagram", "reel", "reels"]))
async def download_instagram_video(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            f"{E_DEVIL} <b>Abe andhe! Instagram Reel ka link toh daal aage!</b>\n{E_FLASH} <i>Example:</i> <code>/ig [Reel_Link]</code>",
            parse_mode=ParseMode.HTML
        )
        
    url = message.text.split(None, 1)[1].strip()
    
    # Advanced Regex to strictly match Insta links
    if not re.match(r"^(https?://)?(www\.)?(instagram\.com|instagr\.am)/.*$", url):
        return await message.reply_text(
            f"{E_FINGER} <b>Ye kaisa sasta link hai? Asli Instagram Reel ka link bhej!</b>",
            parse_mode=ParseMode.HTML
        )
        
    msg = await message.reply_text(f"{E_LOAD} <i>Anu Mainframe: Extracting Reel...</i>", parse_mode=ParseMode.HTML)
    
    api_url = f"https://insta-dl.hazex.workers.dev/?url={url}"

    try:
        # 🔥 FIX: Using aiohttp instead of blocking requests.get
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    return await msg.edit_text(f"{E_FINGER} <b>Anu Error:</b> <i>API Server Down! API wale ki MKC!</i>", parse_mode=ParseMode.HTML)
                result = await response.json()
                
    except Exception as e:
        error_msg = f"{E_FINGER} <b>System Fucked Up:</b>\n<pre>{e}</pre>"
        try:
            await msg.edit_text(error_msg, parse_mode=ParseMode.HTML)
        except Exception:
            await message.reply_text(error_msg, parse_mode=ParseMode.HTML)
        return await app.send_message(LOGGER_ID, f"Insta Module Error:\n{e}")

    # Safe parsing
    if not result.get("error"):
        try:
            data = result.get("result", {})
            video_url = data.get("url")
            
            if not video_url:
                return await msg.edit_text(f"{E_FINGER} <b>Anu Error:</b> <i>Video link nahi mila! Account private hoga shayad.</i>", parse_mode=ParseMode.HTML)
                
            duration = data.get("duration", "Unknown")
            quality = data.get("quality", "HD")
            file_type = data.get("extension", "mp4")
            size = data.get("formattedSize", "Unknown")
            
            # 💎 FRESH PREMIUM UI
            caption = f"""
{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗜 𝗡 𝗦 𝗧 𝗔 』</b> {E_DIAMOND}
━━━━━━━━━━━━━━━━━━━━

{E_INSTA} <b>𝗥𝗲𝗲𝗹 𝗘𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆!</b>

{E_FLASH} <b>𝗤𝘂𝗮𝗹𝗶𝘁𝘆 :</b> <code>{quality}</code>
⏱ <b>𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 :</b> <code>{duration}</code>
💾 <b>𝗦𝗶𝘇𝗲 :</b> <code>{size}</code> ({file_type})

━━━━━━━━━━━━━━━━━━━━
{E_DEVIL} <i>Anu Empire Downloader</i>
"""
            await message.reply_video(video_url, caption=caption, parse_mode=ParseMode.HTML)
            await msg.delete()
            
        except Exception as e:
            await msg.edit_text(f"{E_FINGER} <b>Anu Error:</b> <i>Reel parsing failed. API badalni padegi.</i>", parse_mode=ParseMode.HTML)
            await app.send_message(LOGGER_ID, f"Insta Parsing Error:\n{e}")
    else:
        await msg.edit_text(f"{E_FINGER} <b>Anu Error:</b> <i>API ne error maara hai. Reel Private ho sakti hai.</i>", parse_mode=ParseMode.HTML)


MODULE = "Iɴsᴛᴀ"
HELP = """
<b>» /ig [URL]</b> - <i>Download Instagram Reels.</i>
<b>» /reel [URL]</b> - <i>Download Instagram Reels.</i>
"""

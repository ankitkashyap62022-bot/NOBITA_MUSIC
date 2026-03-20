import logging
import asyncio
from googlesearch import search
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from NOBITA_MUSIC import app
from SafoneAPI import SafoneAPI

# ==========================================
# 💎 BOSS KE KHUD KE PREMIUM EMOJIS 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_CROWN = "<emoji id='6307750079423845494'>👑</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_CROSS = "<emoji id='4926993814033269936'>🖕</emoji>"  # The Boss Error Emoji
E_TICK = "<emoji id='6001589602085771497'>✅</emoji>"
E_APP = "<emoji id='4929369656797431200'>🪐</emoji>"
E_SEARCH = "<emoji id='6307605493644793241'>📒</emoji>"

# 🛠️ Helper function to run sync Google search in async way
def safe_google_search(query):
    results = []
    try:
        # Limited to 5 results to prevent MessageTooLong Crash
        for count, result in enumerate(search(query, advanced=True)):
            if count >= 5:
                break
            results.append(result)
    except Exception as e:
        logging.exception(e)
    return results

# ==========================================
# 🚀 ANU SUPREME GOOGLE ENGINE ☠️
# ==========================================
@app.on_message(filters.command(["google", "gle"]))
async def google_search(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            f"{E_DEVIL} <b>Abe Lode! Google pe kya dhoondhna hai wo toh likh!</b>\n{E_MAGIC} <i>Example:</i> <code>/google Anu Empire</code>",
            parse_mode=ParseMode.HTML
        )

    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.command[1:])
        
    msg = await message.reply_text(f"{E_SEARCH} <i>Anu Mainframe: Hacking Google Database...</i>", parse_mode=ParseMode.HTML)
    
    try:
        search_results = await asyncio.to_thread(safe_google_search, user_input)
        
        if not search_results:
            return await msg.edit_text(f"{E_CROSS} <b>Anu Error:</b> <i>Google baba ko kuch nahi mila!</i>", parse_mode=ParseMode.HTML)

        txt = f"{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗚 𝗢 𝗢 𝗚 𝗟 𝗘  』</b> {E_DIAMOND}\n━━━━━━━━━━━━━━━━━━━━\n"
        txt += f"{E_SEARCH} <b>𝗤𝘂𝗲𝗿𝘆 :</b> <code>{user_input}</code>\n\n"
        
        for result in search_results:
            txt += f"{E_CROWN} <b><a href='{result.url}'>{result.title}</a></b>\n"
            txt += f"<i>{result.description[:150]}...</i>\n\n"
            
        txt += f"━━━━━━━━━━━━━━━━━━━━\n{E_DEVIL} <i>Anu Empire Search System.</i>"
        
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🌐 𝗢𝗽𝗲𝗻 𝗜𝗻 𝗕𝗿𝗼𝘄𝘀𝗲𝗿", url=f"https://www.google.com/search?q={user_input.replace(' ', '+')}")]])
        
        await msg.edit_text(txt, disable_web_page_preview=True, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        
    except Exception as e:
        await msg.edit_text(f"{E_CROSS} <b>System Error:</b> {e}", parse_mode=ParseMode.HTML)
        logging.exception(e)


# ==========================================
# 🚀 ANU SUPREME PLAYSTORE ENGINE ☠️
# ==========================================
@app.on_message(filters.command(["app", "apps"]))
async def app_search(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            f"{E_DEVIL} <b>Abe andhe! App ka naam toh bata!</b>\n{E_MAGIC} <i>Example:</i> <code>/app Free Fire</code>",
            parse_mode=ParseMode.HTML
        )

    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.command[1:])
        
    msg = await message.reply_text(f"{E_APP} <i>Anu Mainframe: Scanning Play Store...</i>", parse_mode=ParseMode.HTML)
    
    try:
        api_response = await SafoneAPI().apps(user_input, 1)
        
        if not api_response or not api_response.get("results"):
            return await msg.edit_text(f"{E_CROSS} <b>Anu Error:</b> <i>Play Store pe aisi koi app nahi hai!</i>", parse_mode=ParseMode.HTML)
            
        app_data = api_response["results"][0]
        
        icon = app_data.get("icon", "https://files.catbox.moe/tcz7s6.jpg")
        app_id = app_data.get("id", "Unknown")
        link = app_data.get("link", "https://play.google.com")
        title = app_data.get("title", "Unknown App")
        dev = app_data.get("developer", "Unknown Dev")
        description = app_data.get("description", "No Description")
        
        if len(description) > 400:
            description = description[:400] + "... [Read More On Playstore]"
            
        info = f"""
{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗣 𝗟 𝗔 𝗬 𝗦 𝗧 𝗢 𝗥 𝗘 』</b> {E_DIAMOND}
━━━━━━━━━━━━━━━━━━━━

{E_APP} <b>𝗔𝗽𝗽 𝗡𝗮𝗺𝗲 :</b> <a href='{link}'>{title}</a>
{E_CROWN} <b>𝗗𝗲𝘃𝗲𝗹𝗼𝗽𝗲𝗿 :</b> <code>{dev}</code>
🏷️ <b>𝗣𝗮𝗰𝗸𝗮𝗴𝗲 𝗜𝗗 :</b> <code>{app_id}</code>

{E_MAGIC} <b>𝗗𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 :</b>
<i>{description}</i>

━━━━━━━━━━━━━━━━━━━━
"""
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("📥 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗔𝗽𝗽", url=link)]])
        
        await message.reply_photo(photo=icon, caption=info, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        await msg.delete()
        
    except Exception as e:
        await msg.edit_text(f"{E_CROSS} <b>System Error:</b> {e}", parse_mode=ParseMode.HTML)

__MODULE__ = "𝗦𝗲𝗮𝗿𝗰𝗵"
__HELP__ = """
<b>» /google [Query]</b> - <i>Google Database bypass and fetch results.</i>
<b>» /app [App Name]</b> - <i>Playstore Database scanner for app details.</i>
"""

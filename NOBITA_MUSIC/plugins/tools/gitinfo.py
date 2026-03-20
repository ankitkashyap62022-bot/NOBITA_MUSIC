import aiohttp
from datetime import datetime
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from NOBITA_MUSIC import app

# ==========================================
# 💎 PREMIUM EMOJIS LOADED FROM ANU DB 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_CROWN = "<emoji id='6307750079423845494'>👑</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_CROSS = "<emoji id='6151981777490548710'>❌</emoji>"
E_TICK = "<emoji id='6001589602085771497'>✅</emoji>"

# ==========================================
# 🚀 ANU SUPREME GITHUB RECON TOOL ☠️
# ==========================================
@app.on_message(filters.command(["github", "git"]))
async def github(_, message):
    if len(message.command) < 2:
        return await message.reply_text(
            f"{E_DEVIL} <b>Abe andhe! Github username toh daal!</b>\n{E_MAGIC} <i>Example:</i> <code>/git MONSTER-FUCK-BITCHES</code>",
            parse_mode=ParseMode.HTML
        )

    username = message.text.split(None, 1)[1].strip()
    URL = f'https://api.github.com/users/{username}'

    # Hacking Feeling Load Message
    msg = await message.reply_text(f"{E_MAGIC} <i>Anu Mainframe: Scanning Github Database...</i>", parse_mode=ParseMode.HTML)

    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await msg.edit_text(f"{E_CROSS} <b>Anu Error:</b> <i>User '{username}' naam ka koi hacker/kida Github pe nahi mila! 😂</i>", parse_mode=ParseMode.HTML)
            
            result = await request.json()

            try:
                # 🔥 FIX: Safe fetching. Agar data nahi hai to default value lega aur crash nahi hoga!
                url = result.get('html_url', 'No Link')
                name = result.get('name') or username
                company = result.get('company') or "Nalla / Berozgar 😂" # Toxic Default
                bio = result.get('bio') or "No Bio provided."
                created_at = result.get('created_at', 'Unknown')
                avatar_url = result.get('avatar_url', 'https://files.catbox.moe/tcz7s6.jpg')
                blog = result.get('blog') or "No Website"
                location = result.get('location') or "Unknown Location"
                repositories = result.get('public_repos', 0)
                followers = result.get('followers', 0)
                following = result.get('following', 0)

                # 🔥 FIX: Parsing ugly ISO date into sexy readable date
                if created_at != 'Unknown':
                    try:
                        dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                        created_at = dt.strftime("%d %B %Y")
                    except:
                        pass

                # 💎 PREMIUM UI Formatting (Left aligned to look clean)
                caption = f"""
{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗚 𝗜 𝗧 𝗛 𝗨 𝗕  𝗦 𝗖 𝗔 𝗡 』</b> {E_DIAMOND}
━━━━━━━━━━━━━━━━━━━━

{E_CROWN} <b>𝗡𝗮𝗺𝗲 :</b> {name}
{E_MAGIC} <b>𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲 :</b> <a href='{url}'>{username}</a>
{E_TICK} <b>𝗕𝗶𝗼 :</b> <i>{bio}</i>

{E_DEVIL} <b>𝗥𝗲𝗽𝗼𝘀𝗶𝘁𝗼𝗿𝗶𝗲𝘀 :</b> <code>{repositories}</code>
👥 <b>𝗙𝗼𝗹𝗹𝗼𝘄𝗲𝗿𝘀 :</b> <code>{followers}</code> | <b>𝗙𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴 :</b> <code>{following}</code>
🏢 <b>𝗖𝗼𝗺𝗽𝗮𝗻𝘆 :</b> {company}
📍 <b>𝗟𝗼𝗰𝗮𝘁𝗶𝗼𝗻 :</b> {location}
🔗 <b>𝗕𝗹𝗼𝗴/𝗪𝗲𝗯 :</b> {blog}
📅 <b>𝗝𝗼𝗶𝗻𝗲𝗱 𝗢𝗻 :</b> {created_at}

━━━━━━━━━━━━━━━━━━━━
"""
                # Using the forceclose logic we implemented in eval for safe closing
                close_button = InlineKeyboardButton("🗑 𝗖𝗹𝗼𝘀𝗲", callback_data=f"forceclose abc|{message.from_user.id}")
                inline_keyboard = InlineKeyboardMarkup([[close_button]])

                # 🔥 FIX: Moved inside the Try block so it doesn't crash if variables fail!
                await message.reply_photo(
                    photo=avatar_url, 
                    caption=caption, 
                    reply_markup=inline_keyboard,
                    parse_mode=ParseMode.HTML
                )
                await msg.delete()

            except Exception as e:
                await msg.edit_text(f"{E_CROSS} <b>Anu System Error:</b> {str(e)}", parse_mode=ParseMode.HTML)

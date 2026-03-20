from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ParseMode
import requests
from NOBITA_MUSIC import app

# ==========================================
# 💎 PREMIUM EMOJIS LOADED FROM ANU DB 💎
# ==========================================
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_CROWN = "<emoji id='6307750079423845494'>👑</emoji>"
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"

# Function to chunk the repository info
def chunk_string(text, chunk_size):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def get_all_repository_info(github_username):
    github_api_url = f"https://api.github.com/users/{github_username}/repos"
    response = requests.get(github_api_url)
    
    if response.status_code != 200:
        return None # User not found ya API limit aagayi
        
    data = response.json()
    if not data:
        return "⚠️ Is bhikhari ke pas koi public repo nahi hai."

    # HTML formatted list with Premium Anu look
    repo_info = "\n\n".join([
        f"{E_CROWN} <b>Repo:</b> <a href='{repo['html_url']}'>{repo['name']}</a>\n"
        f"📝 <b>Desc:</b> {repo['description'] or 'No description'}\n"
        f"⭐ <b>Stars:</b> {repo['stargazers_count']} | 🍴 <b>Forks:</b> {repo['forks_count']}"
        for repo in data
    ])

    return repo_info


@app.on_message(filters.command("allrepo"))
async def all_repo_command(client, message):
    try:
        if len(message.command) > 1:
            github_username = message.command[1]
            
            # Ek loading message dikhate hain boss wali feel ke liye
            anim = await message.reply_text(f"{E_MAGIC} <i>Anu Mainframe: Fetching GitHub Data for '{github_username}'...</i>", parse_mode=ParseMode.HTML)

            repo_info = get_all_repository_info(github_username)
            await anim.delete() # Loading message hatao

            if not repo_info:
                return await message.reply_text(f"{E_DEVIL} <b>Abe andhe, ye kaisa username de diya? GITHUB pe exist nahi karta ye!</b>", parse_mode=ParseMode.HTML)

            # Split repository info (Limit 3500 to be safe for Telegram limits)
            chunked_repo_info = chunk_string(repo_info, 3500)  

            # 🔥 YE RAHA TERA FIX KIYA HUA BUTTON (ANU EMPIRE KA)
            anu_markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "💎 𝗝𝗼𝗶𝗻 𝗔𝗻𝘂 𝗘𝗺𝗽𝗶𝗿𝗲 💎",
                        url="https://t.me/FUCK_BY_REFLEX"
                    )
                ]
            ])

            # Ab chunk by chunk send karenge, aur button sirf AAKHRI wale message pe lagayenge
            for i, chunk in enumerate(chunked_repo_info):
                if i == len(chunked_repo_info) - 1:
                    await message.reply_text(chunk, reply_markup=anu_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
                else:
                    await message.reply_text(chunk, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        else:
            await message.reply_text(f"{E_DEVIL} <b>Abe Command poori likh:</b>\n<code>/allrepo <github_username></code>", parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.reply_text(f"❌ <b>Error in Anu Kernel:</b> {str(e)}", parse_mode=ParseMode.HTML)

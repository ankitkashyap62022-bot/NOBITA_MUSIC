import os
import random
from datetime import datetime
from PIL import Image, ImageDraw
from pyrogram import filters
from pyrogram.enums import ChatType, ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from NOBITA_MUSIC import app

# ==========================================
# 💎 PREMIUM EMOJIS LOADED FROM ANU DB 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_CROWN = "<emoji id='6307750079423845494'>👑</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_HEART = "<emoji id='6123125485661591081'>🩷</emoji>"

POLICE = [
    [
        InlineKeyboardButton(
            text="👑 𝗕𝗼𝘀𝘀 (𝗢𝘄𝗻𝗲𝗿)",
            url="https://t.me/MONSTER_FUCK_BITCHES",
        ),
    ],
]

def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    return dt_string.split(" ")

def dt_tom():
    now = dt()[0].split("/")
    return f"{int(now[0]) + 1}/{now[1]}/{now[2]}"

@app.on_message(filters.command("couples"))
async def ctest(_, message):
    cid = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(f"{E_DEVIL} <b>Abe Lode! Ye command sirf groups me kaam karti hai!</b>", parse_mode=ParseMode.HTML)
        
    try:
        msg = await message.reply_text(f"{E_MAGIC} <i>Anu Mainframe: Scanning Group for couples...</i>", parse_mode=ParseMode.HTML)
        
        # GET LIST OF USERS
        list_of_users = []
        async for i in app.get_chat_members(message.chat.id, limit=50):
            if not i.user.is_bot:
                list_of_users.append(i.user.id)

        if len(list_of_users) < 2:
            return await msg.edit_text(f"{E_DEVIL} <b>Group me log hi nahi hain, kiska joda banau?</b>", parse_mode=ParseMode.HTML)

        c1_id = random.choice(list_of_users)
        c2_id = random.choice(list_of_users)
        while c1_id == c2_id:
            c1_id = random.choice(list_of_users)

        photo1 = (await app.get_chat(c1_id)).photo
        photo2 = (await app.get_chat(c2_id)).photo
 
        N1 = (await app.get_users(c1_id)).mention 
        N2 = (await app.get_users(c2_id)).mention
         
        # Define paths
        p1_path = f"downloads/pfp1_{cid}.png"
        p2_path = f"downloads/pfp2_{cid}.png"
        out_path = f"downloads/test_{cid}.png"
        fallback_pic = "NOBITA_MUSIC/assets/upic.png"
        bg_pic = "NOBITA_MUSIC/assets/cppic.png"
        
        # Downloading DPs safely
        try:
            p1 = await app.download_media(photo1.big_file_id, file_name=p1_path)
        except Exception:
            p1 = fallback_pic
            
        try:
            p2 = await app.download_media(photo2.big_file_id, file_name=p2_path)
        except Exception:
            p2 = fallback_pic
            
        # Image Processing (Core PIL Logic kept intact)
        img1 = Image.open(p1).resize((437, 437))
        img2 = Image.open(p2).resize((437, 437))
        img = Image.open(bg_pic)

        mask = Image.new('L', img1.size, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + img1.size, fill=255)

        mask1 = Image.new('L', img2.size, 0)
        draw = ImageDraw.Draw(mask1) 
        draw.ellipse((0, 0) + img2.size, fill=255)

        img1.putalpha(mask)
        img2.putalpha(mask1)

        img.paste(img1, (116, 160), img1)
        img.paste(img2, (789, 160), img2)

        img.save(out_path)
    
        # 💎 PREMIUM SIGMA TEXT
        TXT = f"""
{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗠 𝗔 𝗧 𝗖 𝗛 𝗠 𝗔 𝗞 𝗜 𝗡 𝗚 』</b> {E_DIAMOND}
━━━━━━━━━━━━━━━━━━━━

{E_CROWN} <b>𝗔𝗮𝗷 𝗞𝗲 𝗡𝗶𝘁𝗵𝗮𝗹𝗹𝗲 𝗔𝗮𝘀𝗵𝗶𝗾 :</b>
⇛ {N1} + {N2} = {E_HEART}

{E_MAGIC} <i>Next shikaar kal select hoga: {dt_tom()}</i>
━━━━━━━━━━━━━━━━━━━━
"""
    
        await message.reply_photo(
            out_path, 
            caption=TXT, 
            reply_markup=InlineKeyboardMarkup(POLICE),
            parse_mode=ParseMode.HTML
        )
        await msg.delete()
        
    except Exception as e:
        await message.reply_text(f"{E_DEVIL} <b>System Error:</b> {e}", parse_mode=ParseMode.HTML)
        
    finally:
        # 🔥 BUG FIX: Safely removing files so server doesn't fill up
        for file in [p1_path, p2_path, out_path]:
            try:
                if os.path.exists(file):
                    os.remove(file)
            except Exception:
                pass

__mod__ = "COUPLES"
__help__ = """
**» /couples** - Get Todays Couples Of The Group In Interactive View
"""

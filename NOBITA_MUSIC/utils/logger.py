from pyrogram.enums import ParseMode

from NOBITA_MUSIC import app
from NOBITA_MUSIC.utils.database import is_on_off
from config import LOGGER_ID

async def play_logs(message, streamtype):
    if await is_on_off(2):
        # ☠️ BUG FIX: अगर कोई ऑडियो फाइल पर रिप्लाई करके प्ले करे तो क्रैश ना हो!
        if message.reply_to_message:
            query = "ᴀᴜᴅɪᴏ/ᴠɪᴅᴇᴏ ꜰɪʟᴇ ʀᴇᴘʟʏ 📁"
        else:
            try:
                query = message.text.split(None, 1)[1]
            except:
                query = "ᴜɴᴋɴᴏᴡɴ ǫᴜᴇʀʏ ❓"
                
        logger_text = f"""
<emoji id=6309709550878463216>🌟</emoji> <b>ᴀɴᴜ ᴍᴀᴛʀɪx ᴘʟᴀʏ ʟᴏɢ</b> <emoji id=6309709550878463216>🌟</emoji>

➻ <emoji id=4929483658114368660>💎</emoji> <b>ɢʀᴏᴜᴘ :</b> {message.chat.title} [<code>{message.chat.id}</code>]
➻ <emoji id=6307750079423845494>👑</emoji> <b>ᴜsᴇʀ :</b> {message.from_user.mention} [<code>{message.from_user.id}</code>]
➻ <emoji id=6307569802466563145>🎶</emoji> <b>ǫᴜᴇʀʏ :</b> <code>{query}</code>
➻ <emoji id=6307821174017496029>🔥</emoji> <b>sᴛʀᴇᴀᴍ ᴛʏᴘᴇ :</b> {streamtype}

<emoji id=5999210495146465994>💖</emoji> <b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <a href='https://t.me/Reflex_x_zara'>𝗠𝗢𝗡𝗦𝗧𝗘𝗥 𝗫 𝗥𝗘𝗙𝗟𝗘𝗫</a></b>"""
        
        if message.chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except Exception as e:
                print(f"Play Log Error: {e}") 
        return

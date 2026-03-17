from pyrogram.enums import ParseMode

from NOBITA_MUSIC import app
from NOBITA_MUSIC.utils.database import is_on_off
from config import LOGGER_ID

async def play_logs(message, streamtype):
    if await is_on_off(2):
        logger_text = f"""
<emoji id=5260342697075416641>✨</emoji> <b>ᴀɴᴜ ᴍᴀᴛʀɪx ᴘʟᴀʏ ʟᴏɢ</b> <emoji id=5260342697075416641>✨</emoji>

➻ <emoji id=5300882244562567554>🎧</emoji> <b>ɢʀᴏᴜᴘ :</b> {message.chat.title} [<code>{message.chat.id}</code>]
➻ <emoji id=5361730034607598816>👤</emoji> <b>ᴜsᴇʀ :</b> {message.from_user.mention} [<code>{message.from_user.id}</code>]
➻ <emoji id=5341253579075487737>🔍</emoji> <b>ǫᴜᴇʀʏ :</b> <code>{message.text.split(None, 1)[1]}</code>
➻ <emoji id=5341513244015328229>📻</emoji> <b>sᴛʀᴇᴀᴍ ᴛʏᴘᴇ :</b> {streamtype}

<emoji id=5258169229051460596>🖤</emoji> <b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ » <a href='https://t.me/MONSTER_FUCK_BITCHES'>𝗠𝗢𝗡𝗦𝗧𝗘𝗥 𝗫 𝗥𝗘𝗙𝗟𝗘𝗫</a></b>"""
        if message.chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except Exception as e:
                print(f"Log Error: {e}") # इससे अगर कोई एरर होगा तो तेरे टर्मिनल में दिख जाएगा!
        return

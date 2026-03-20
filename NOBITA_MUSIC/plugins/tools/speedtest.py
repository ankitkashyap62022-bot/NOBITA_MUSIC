import asyncio
import speedtest
from pyrogram import filters
from pyrogram.types import Message

from NOBITA_MUSIC import app
from NOBITA_MUSIC.misc import SUDOERS

# ==========================================
# ☠️ ANU MATRIX SPEEDTEST PROTOCOL ☠️
# ==========================================

def perform_speedtest():
    # ☠️ Pure synchronous heavy task for background thread ☠️
    test = speedtest.Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    return test.results.dict()

@app.on_message(filters.command(["speedtest", "spt"]) & SUDOERS)
async def premium_speedtest(client, message: Message):
    mystic = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Iɴɪᴛɪᴀʟɪᴢɪɴɢ Sᴘᴇᴇᴅᴛᴇsᴛ...**")
    
    try:
        await mystic.edit_text("<emoji id=6123040393769521180>☄️</emoji> **Cᴏɴɴᴇᴄᴛɪɴɢ Tᴏ Bᴇsᴛ Sᴇʀᴠᴇʀ...**")
        loop = asyncio.get_event_loop()
        
        # ☠️ Run the heavy speedtest in an executor to prevent bot freeze ☠️
        result = await loop.run_in_executor(None, perform_speedtest)
        
        await mystic.edit_text("<emoji id=6089186666973500770>🎶</emoji> **Tᴇsᴛɪɴɢ Dᴏᴡɴʟᴏᴀᴅ & Uᴘʟᴏᴀᴅ Sᴘᴇᴇᴅ...**")
        
        # 💎 PREMIUM MATRIX UI 💎
        output = f"""
<emoji id=5354924568492383911>😈</emoji> **A N U  M A T R I X  S P E E D T E S T**
━━━━━━━━━━━━━━━━━━━━
<emoji id=6111778259374971023>🔥</emoji> **ISP :** `{result['client']['isp']}`
<emoji id=4929369656797431200>🪐</emoji> **Cᴏᴜɴᴛʀʏ :** `{result['client']['country']}`

<emoji id=6307750079423845494>👑</emoji> **Sᴇʀᴠᴇʀ :** `{result['server']['name']}`
<emoji id=6152142357727811958>✨</emoji> **Sᴘᴏɴsᴏʀ :** `{result['server']['sponsor']}`
<emoji id=5256131095094652290>⏱️</emoji> **Pɪɴɢ/Lᴀᴛᴇɴᴄʏ :** `{result['ping']} ᴍs`
━━━━━━━━━━━━━━━━━━━━
"""
        # Sending the actual Speedtest Image with Stats
        await message.reply_photo(photo=result["share"], caption=output)
        await mystic.delete()
        
    except Exception as e:
        await mystic.edit_text(f"<emoji id=6307821174017496029>❌</emoji> **Sᴘᴇᴇᴅᴛᴇsᴛ Fᴀɪʟᴇᴅ!**\n<emoji id=5256131095094652290>⏱️</emoji> `Sᴇʀᴠᴇʀ ᴍɪɢʜᴛ ʙᴇ ᴅᴏᴡɴ ᴏʀ ʙʟᴏᴄᴋᴇᴅ.`\n\n`Eʀʀᴏʀ: {e}`")


import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.enums import ParseMode
from NOBITA_MUSIC import app
import config

# ==========================================
# ☠️ PREMIUM PRIVACY COMMAND ☠️
# ==========================================
@app.on_message(filters.command(["privacy", "privacypolicy"]))
async def premium_privacy(client, message: Message):
    
    # 💎 ULTRA PREMIUM UI TEXT WITH EMOJIS 💎
    TEXT = f"""
<emoji id=5354924568492383911>😈</emoji> **{app.name} Pʀɪᴠᴀᴄʏ & Sᴇᴄᴜʀɪᴛʏ Pʀᴏᴛᴏᴄᴏʟ!**

<emoji id=6152142357727811958>🦋</emoji> **Hᴇʏ {message.from_user.mention},**
Yᴏᴜʀ ᴘʀɪᴠᴀᴄʏ ɪs ᴏᴜʀ ᴛᴏᴘ ᴘʀɪᴏʀɪᴛʏ. Wᴇ ᴏᴘᴇʀᴀᴛᴇ ᴏɴ ᴀ sᴛʀɪᴄᴛ **Zᴇʀᴏ Lᴏɢs** ᴘᴏʟɪᴄʏ ғᴏʀ ᴘᴇʀsᴏɴᴀʟ ᴄʜᴀᴛs! 

<emoji id=4929369656797431200>🪐</emoji> **Dᴀᴛᴀ Cᴏʟʟᴇᴄᴛɪᴏɴ:** Wᴇ ᴏɴʟʏ sᴛᴏʀᴇ ɢʀᴏᴜᴘ IDs ᴀɴᴅ ʙᴀsɪᴄ ᴘʟᴀʏʙᴀᴄᴋ sᴇᴛᴛɪɴɢs ᴛᴏ ᴋᴇᴇᴘ ᴛʜᴇ ᴍᴜsɪᴄ ᴘʟᴀʏɪɴɢ sᴍᴏᴏᴛʜʟʏ.
<emoji id=6111742817304841054>✅</emoji> **Sᴇᴄᴜʀɪᴛʏ:** 100% Sᴀғᴇ, Sᴇᴄᴜʀᴇ & Eɴᴄʀʏᴘᴛᴇᴅ.
<emoji id=6307346833534359338>🍷</emoji> **Aɢʀᴇᴇᴍᴇɴᴛ:** Bʏ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ, ʏᴏᴜ ᴀɢʀᴇᴇ ᴛᴏ ᴏᴜʀ ᴏғғɪᴄɪᴀʟ Tᴇʀᴍs & Pʀɪᴠᴀᴄʏ Pᴏʟɪᴄʏ.

<emoji id=6307821174017496029>🔥</emoji> **Cʟɪᴄᴋ ʙᴇʟᴏᴡ ᴛᴏ ʀᴇᴀᴅ ᴛʜᴇ ғᴜʟʟ ᴘᴏʟɪᴄʏ:**
"""

    # 💎 ADVANCED BUTTON ROUTING 💎
    keyboard = InlineKeyboardMarkup(
        [
            [
                # Fixed the bug: Now it actually goes to the Privacy Link
                InlineKeyboardButton(
                    text="📄 Vɪᴇᴡ Pʀɪᴠᴀᴄʏ Pᴏʟɪᴄʏ", url=config.PRIVACY_LINK
                )
            ],
            [
                InlineKeyboardButton(
                    text="🛠 Sᴜᴘᴘᴏʀᴛ Tᴇᴀᴍ", url=config.SUPPORT_CHAT
                ),
                # Support channel link (if you have one, or just keep it simple)
                InlineKeyboardButton(
                    text="🍷 Uᴘᴅᴀᴛᴇs", url=config.SUPPORT_CHAT 
                )
            ]
        ]
    )
    
    # ☠️ ERROR HANDLING (HARD CODE) ☠️
    try:
        await message.reply_text(
            text=TEXT, 
            reply_markup=keyboard, 
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Privacy Command Error: {e}")

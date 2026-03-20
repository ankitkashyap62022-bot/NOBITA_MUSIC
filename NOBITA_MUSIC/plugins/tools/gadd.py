import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.errors import FloodWait
from pyrogram.enums import ParseMode

import config
from NOBITA_MUSIC import app
from NOBITA_MUSIC.utils.database import add_served_chat, get_assistant

# ==========================================
# 💎 PREMIUM EMOJIS LOADED FROM ANU DB 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_CROWN = "<emoji id='6307750079423845494'>👑</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_TICK = "<emoji id='6001589602085771497'>✅</emoji>"
E_CROSS = "<emoji id='6151981777490548710'>❌</emoji>"
E_LOAD = "<emoji id='6001859600121350616'>⏳</emoji>"

# ==========================================
# 🚀 ANU SUPREME GLOBAL ADDER (/gadd) ☠️
# ==========================================
@app.on_message(filters.command("gadd") & filters.user(config.OWNER_ID))
async def add_allbot(client, message: Message):
    command_parts = message.text.split(" ")
    if len(command_parts) != 2:
        return await message.reply_text(
            f"{E_DEVIL} <b>Abe andhe! Command dhang se likh!</b>\n\n{E_MAGIC} <i>Example:</i> <code>/gadd @Teri_Bot_Ka_Username</code>",
            parse_mode=ParseMode.HTML
        )

    bot_username = command_parts[1].replace("@", "")
    
    try:
        userbot = await get_assistant(message.chat.id)
        bot_to_add = await app.get_users(bot_username)
        app_id = bot_to_add.id
        
        done = 0
        failed = 0
        
        lol = await message.reply_text(
            f"{E_LOAD} <b>Anu Mainframe:</b> <i>Initializing Global Add for @{bot_username}...</i>",
            parse_mode=ParseMode.HTML
        )
        
        # Bot ko start message bhej raha hai (Active karne ke liye)
        try:
            await userbot.send_message(bot_username, "/start")
        except:
            pass
            
        async for dialog in userbot.get_dialogs():
            # Skip Private Chats and Your Support Group
            if dialog.chat.type in ["private", "bot"] or dialog.chat.id == -1002344707828:
                continue
                
            try:
                await userbot.add_chat_members(dialog.chat.id, app_id)
                done += 1
            except FloodWait as fw:
                # 🔥 FIX: Anti-Ban FloodWait Handler
                await asyncio.sleep(int(fw.value) + 2)
                failed += 1
            except Exception:
                failed += 1
                
            # 🔥 FIX: Edit limits bachane ke liye (Har 5 chat ke baad update karega)
            if (done + failed) % 5 == 0:
                try:
                    await lol.edit_text(
                        f"{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗚 𝗟 𝗢 𝗕 𝗔 𝗟  𝗔 𝗗 𝗗 』</b> {E_DIAMOND}\n━━━━━━━━━━━━━━━━━━━━\n"
                        f"{E_MAGIC} <b>𝗧𝗮𝗿𝗴𝗲𝘁:</b> @{bot_username}\n\n"
                        f"{E_TICK} <b>𝗦𝘂𝗰𝗰𝗲𝘀𝘀 :</b> <code>{done}</code> Chats\n"
                        f"{E_CROSS} <b>𝗙𝗮𝗶𝗹𝗲𝗱 :</b> <code>{failed}</code> Chats\n\n"
                        f"{E_DEVIL} <i>𝗔𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝘁 𝗔𝘁 𝗪𝗼𝗿𝗸:</i> @{userbot.username}",
                        parse_mode=ParseMode.HTML
                    )
                except:
                    pass
                    
            await asyncio.sleep(3)  # Rate Limit Safety

        # 💎 Final Success Message
        final_text = f"""
{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗚 𝗟 𝗢 𝗕 𝗔 𝗟  𝗔 𝗗 𝗗 』</b> {E_DIAMOND}
━━━━━━━━━━━━━━━━━━━━
{E_CROWN} <b>𝗧𝗮𝘀𝗸 𝗖𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝗱! 𝗕𝗼𝘁 𝗜𝗻𝗷𝗲𝗰𝘁𝗲𝗱.</b>

{E_MAGIC} <b>𝗧𝗮𝗿𝗴𝗲𝘁 𝗕𝗼𝘁 :</b> @{bot_username}
{E_TICK} <b>𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗔𝗱𝗱𝗲𝗱 :</b> <code>{done}</code> Chats
{E_CROSS} <b>𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱 :</b> <code>{failed}</code> Chats

{E_DEVIL} <i>𝗔𝗻𝘂 𝗦𝘆𝘀𝘁𝗲𝗺 𝗢𝘃𝗲𝗿𝗿𝗶𝗱𝗲 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹.</i> 🍷
━━━━━━━━━━━━━━━━━━━━
"""
        await lol.edit_text(final_text, parse_mode=ParseMode.HTML)
        
    except Exception as e:
        await message.reply_text(f"{E_CROSS} <b>System Error:</b> {str(e)}", parse_mode=ParseMode.HTML)

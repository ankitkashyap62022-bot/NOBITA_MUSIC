from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from NOBITA_MUSIC import app
from NOBITA_MUSIC.misc import SUDOERS
from NOBITA_MUSIC.utils.database import add_sudo, remove_sudo
from NOBITA_MUSIC.utils.extraction import extract_user
from config import BANNED_USERS, OWNER_ID

# ==========================================
# ☠️ ANU MATRIX SUDO (CO-OWNER) PROTOCOL ☠️
# ==========================================

@app.on_message(filters.command(["addsudo", "addadmin"]) & filters.user(OWNER_ID))
async def premium_useradd(client, message: Message):
    usage = "<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ :** `/addsudo [Rᴇᴘʟʏ / Usᴇʀɴᴀᴍᴇ / ID]`"
    
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(usage)
            
    try:
        user = await extract_user(message)
    except Exception:
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Uɴᴀʙʟᴇ ᴛᴏ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ!**")

    if user.id in SUDOERS:
        return await message.reply_text(f"<emoji id=5354924568492383911>😈</emoji> **Bᴏss, {user.mention} ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ ᴍʏ Sᴜᴅᴏ Pᴀɴᴇʟ!**")
        
    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply_text(f"<emoji id=6111742817304841054>✅</emoji> **Sᴜᴄᴄᴇssғᴜʟʟʏ Pʀᴏᴍᴏᴛᴇᴅ {user.mention} ᴀs Aɴᴜ Mᴀᴛʀɪx Sᴜᴅᴏ!**\n<emoji id=6152142357727811958>✨</emoji> Tʜᴇʏ ᴄᴀɴ ɴᴏᴡ ᴄᴏɴᴛʀᴏʟ ᴍʏ ᴄᴏʀᴇ ғᴇᴀᴛᴜʀᴇs.")
    else:
        await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ɪɴ Dᴀᴛᴀʙᴀsᴇ!**")


@app.on_message(filters.command(["delsudo", "rmsudo"]) & filters.user(OWNER_ID))
async def premium_userdel(client, message: Message):
    usage = "<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ :** `/delsudo [Rᴇᴘʟʏ / Usᴇʀɴᴀᴍᴇ / ID]`"
    
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(usage)
            
    try:
        user = await extract_user(message)
    except Exception:
        return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Uɴᴀʙʟᴇ ᴛᴏ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ!**")

    if user.id not in SUDOERS:
        return await message.reply_text(f"<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, {user.mention} ɪs ɴᴏᴛ ᴀ Sᴜᴅᴏ Usᴇʀ!**")
        
    removed = await remove_sudo(user.id)
    if removed:
        SUDOERS.remove(user.id)
        await message.reply_text(f"<emoji id=6111742817304841054>✅</emoji> **Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇᴍᴏᴛᴇᴅ {user.mention}!**\n<emoji id=6152142357727811958>✨</emoji> Sᴜᴅᴏ Pᴏᴡᴇʀs ʀᴇᴠᴏᴋᴇᴅ.")
    else:
        await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ɪɴ Dᴀᴛᴀʙᴀsᴇ!**")


@app.on_message(filters.command(["sudolist", "listsudo", "sudoers"]) & ~BANNED_USERS)
async def premium_sudoers_list(client, message: Message):
    keyboard = [[InlineKeyboardButton("☄️ Vɪᴇᴡ Sᴜᴅᴏ Mᴀᴛʀɪx ☄️", callback_data="check_sudo_list")]]
    reply_markups = InlineKeyboardMarkup(keyboard)
    
    # 💎 Replaced with Premium Hacker Vibe text 💎
    await message.reply_video(
        video="https://files.catbox.moe/tcz7s6.jpg", 
        caption="<emoji id=5354924568492383911>😈</emoji> **A N U  M A T R I X  S U D O  P A N E L**\n\n<emoji id=5256131095094652290>⏱️</emoji> ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴠɪᴇᴡ ᴛʜᴇ ᴇʟɪᴛᴇ ᴄᴏɴᴛʀᴏʟʟᴇʀs.\n\n<emoji id=6307821174017496029>⚠️</emoji> **Nᴏᴛᴇ:** Oɴʟʏ Aɴᴜ Mᴀᴛʀɪx Sᴜᴅᴏᴇʀs ᴄᴀɴ ᴠɪᴇᴡ ᴛʜɪs ʟɪsᴛ.", 
        reply_markup=reply_markups
    )
    

@app.on_callback_query(filters.regex("^check_sudo_list$"))
async def check_sudo_list(client, callback_query: CallbackQuery):
    if callback_query.from_user.id not in SUDOERS:
        # ☠️ Removed the cringe abuse, added a toxic hacker alert ☠️
        return await callback_query.answer("☠️ Oᴜᴋᴀᴀᴛ ᴍᴇ ʀᴇʜ Nᴏᴏʙ! Oɴʟʏ Sᴜᴅᴏᴇʀs ᴄᴀɴ ᴠɪᴇᴡ ᴛʜɪs Eʟɪᴛᴇ Lɪsᴛ! ☠️", show_alert=True)
    
    keyboard = []
    user = await app.get_users(OWNER_ID[0] if isinstance(OWNER_ID, list) else OWNER_ID)
    user_mention = (user.first_name if not hasattr(user, "mention") else user.mention)
    
    caption = f"<emoji id=6307750079423845494>👑</emoji> **L I S T  O F  S U P R E M E S**\n\n<emoji id=6111778259374971023>🔥</emoji> **Cʀᴇᴀᴛᴏʀ :** {user_mention}\n\n"
    keyboard.append([InlineKeyboardButton("👑 Vɪᴇᴡ Sᴜᴘʀᴇᴍᴇ Cʀᴇᴀᴛᴏʀ 👑", url=f"tg://openmessage?user_id={user.id}")])
    
    count = 1
    for user_id in SUDOERS:
        if user_id not in (OWNER_ID if isinstance(OWNER_ID, list) else [OWNER_ID]):
            try:
                sudo_user = await app.get_users(user_id)
                sudo_mention = sudo_user.mention if hasattr(sudo_user, "mention") else f"**Sᴜᴅᴏ {count} ɪᴅ:** `{user_id}`"
                caption += f"<emoji id=6152142357727811958>✨</emoji> **Sᴜᴅᴏ {count} »** {sudo_mention}\n"
                keyboard.append([InlineKeyboardButton(f"✨ Vɪᴇᴡ Sᴜᴅᴏ {count} ✨", url=f"tg://openmessage?user_id={user_id}")])
                count += 1
            except:
                continue

    keyboard.append([InlineKeyboardButton("« Bᴀᴄᴋ Tᴏ Mᴀɪɴ ", callback_data="back_to_main_menu")])

    if keyboard:
        reply_markup = InlineKeyboardMarkup(keyboard)
        await callback_query.message.edit_caption(caption=caption, reply_markup=reply_markup)


@app.on_callback_query(filters.regex("^back_to_main_menu$"))
async def back_to_main_menu(client, callback_query: CallbackQuery):
    keyboard = [[InlineKeyboardButton("☄️ Vɪᴇᴡ Sᴜᴅᴏ Mᴀᴛʀɪx ☄️", callback_data="check_sudo_list")]]
    reply_markupes = InlineKeyboardMarkup(keyboard)
    await callback_query.message.edit_caption(
        caption="<emoji id=5354924568492383911>😈</emoji> **A N U  M A T R I X  S U D O  P A N E L**\n\n<emoji id=5256131095094652290>⏱️</emoji> ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴠɪᴇᴡ ᴛʜᴇ ᴇʟɪᴛᴇ ᴄᴏɴᴛʀᴏʟʟᴇʀs.\n\n<emoji id=6307821174017496029>⚠️</emoji> **Nᴏᴛᴇ:** Oɴʟʏ Aɴᴜ Mᴀᴛʀɪx Sᴜᴅᴏᴇʀs ᴄᴀɴ ᴠɪᴇᴡ ᴛʜɪs ʟɪsᴛ.", 
        reply_markup=reply_markupes
    )


@app.on_message(filters.command(["delallsudo", "rmallsudo"]) & filters.user(OWNER_ID))
async def del_all_sudo(client, message: Message):
    # ☠️ The Mass Demotion Protocol ☠️
    owner_list = OWNER_ID if isinstance(OWNER_ID, list) else [OWNER_ID]
    count = len(SUDOERS) - len(owner_list) 
    
    if count <= 0:
        return await message.reply_text("<emoji id=5256131095094652290>⏱️</emoji> **Bᴏss, ᴛʜᴇʀᴇ ᴀʀᴇ ɴᴏ Sᴜᴅᴏᴇʀs ᴛᴏ ʀᴇᴍᴏᴠᴇ. Yᴏᴜ ᴀʀᴇ ᴛʜᴇ ᴏɴʟʏ Kɪɴɢ ʜᴇʀᴇ!**")
        
    for user_id in SUDOERS.copy():
        if user_id not in owner_list:
            removed = await remove_sudo(user_id)
            if removed:
                SUDOERS.remove(user_id)
                
    await message.reply_text(f"<emoji id=6111742817304841054>✅</emoji> **Mᴀss Dᴇᴍᴏᴛɪᴏɴ Sᴜᴄᴄᴇssғᴜʟ!**\n<emoji id=6152142357727811958>✨</emoji> Pᴜʀɢᴇᴅ `{count}` ᴜsᴇʀs ғʀᴏᴍ ᴛʜᴇ Sᴜᴅᴏ Mᴀᴛʀɪx.")

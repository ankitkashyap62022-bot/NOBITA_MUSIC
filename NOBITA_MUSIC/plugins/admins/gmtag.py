import asyncio
import random
import re
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from NOBITA_MUSIC import app
from NOBITA_MUSIC.misc import mongodb

# ☠️ MONSTER KERNEL DATABASE & TRACKER ☠️
tag_db = mongodb.gmgn_tags  # Single DB collection for GM/GN and Emojis
spam_chats = []
TAG_DATA = {} # RAM storage for initial menu

PREMIUM_EMOJIS = [
    "<emoji id=4929369656797431200>🪐</emoji>", "<emoji id=6123040393769521180>☄️</emoji>", 
    "<emoji id=6307821174017496029>🔥</emoji>", "<emoji id=6111742817304841054>✅</emoji>", 
    "<emoji id=4929195195225867512>💎</emoji>", "<emoji id=6152142357727811958>🦋</emoji>", 
    "<emoji id=6307750079423845494>👑</emoji>", "<emoji id=5998881015320287132>💊</emoji>", 
    "<emoji id=6307346833534359338>🍷</emoji>", "<emoji id=5354924568492383911>😈</emoji>", 
    "<emoji id=5352870513267973607>✨</emoji>", "<emoji id=6224236403153179330>🎀</emoji>", 
    "<emoji id=5999210495146465994>💖</emoji>"
]

# 🔥 ADMIN CHECK FUNCTION 🔥
async def is_admin(chat_id, user_id, client):
    try:
        participant = await client.get_chat_member(chat_id, user_id)
        if participant.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return True
    except UserNotParticipant:
        pass
    return False

# 🧹 EMOJI STRIPPER (Removes Normal Emojis)
def strip_normal_emojis(text):
    return re.sub(r'[\U00002600-\U000027BF\U00010000-\U0010FFFF]', '', text).strip()


# ==========================================
# ☠️ STEP 1: PREMIUM EMOJI EXTRACTOR ☠️
# ==========================================
@app.on_message(filters.command(["addpreme", "addemoji"]) & filters.group)
async def add_premium_emojis(client, message):
    if not await is_admin(message.chat.id, message.from_user.id, client):
        return await message.reply("<emoji id=4926993814033269936>🖕</emoji> **ᴏᴜᴋᴀᴀᴛ ᴍᴇ ʀᴇʜ ʟᴏᴅᴇ!**")

    raw_html = message.text.html if message.text else ""
    extracted_emojis = re.findall(r'<emoji id="\d+">.*?</emoji>', raw_html)
    
    if not extracted_emojis:
        return await message.reply("<emoji id=6307605493644793241>📒</emoji> **ɴᴏ ᴘʀᴇᴍɪᴜᴍ ᴇᴍᴏᴊɪꜱ ꜰᴏᴜɴᴅ ɪɴ ʏᴏᴜʀ ᴍᴇꜱꜱᴀɢᴇ!**")

    await tag_db.update_one(
        {"_id": "premium_emojis"}, 
        {"$addToSet": {"emojis": {"$each": extracted_emojis}}}, 
        upsert=True
    )
    await message.reply(f"<emoji id=6111742817304841054>✅</emoji> **ꜱᴀᴠᴇᴅ {len(extracted_emojis)} ᴘʀᴇᴍɪᴜᴍ ᴇᴍᴏᴊɪꜱ!**")


# ==========================================
# ☠️ STEP 2: ADD GM/GN MESSAGES (SILENT SAVE) ☠️
# ==========================================
@app.on_message(filters.command(["addgmtag", "addgntag"]) & filters.group)
async def add_dynamic_tag(client, message):
    if not await is_admin(message.chat.id, message.from_user.id, client):
        return await message.reply("<emoji id=4926993814033269936>🖕</emoji> **ᴏᴜᴋᴀᴀᴛ ᴍᴇ ʀᴇʜ ʟᴏᴅᴇ!**")

    cmd = message.command[0].lower()
    tag_type = "gm" if "gm" in cmd else "gn"
    
    raw_text = ""
    if message.reply_to_message and message.reply_to_message.text:
        raw_text = message.reply_to_message.text
    elif len(message.command) > 1:
        raw_text = message.text.split(None, 1)[1]
    else:
        return await message.reply(f"<emoji id=6307821174017496029>🔥</emoji> **ᴜꜱᴀɢᴇ:** `/{cmd} [Text]` ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ!")
    
    lines = raw_text.split('\n')
    clean_lines = []
    
    for line in lines:
        clean_str = strip_normal_emojis(line)
        if clean_str:  
            clean_lines.append(clean_str)
            
    if not clean_lines:
        return await message.reply("<emoji id=4926993814033269936>🖕</emoji> **No valid text found after removing emojis!**")

    await tag_db.update_one({"_id": tag_type}, {"$addToSet": {"msgs": {"$each": clean_lines}}}, upsert=True)
    # 🔥 FIXED: Now it only shows the number of lines added, not the whole script! 🔥
    await message.reply(f"<emoji id=6111742817304841054>✅</emoji> **{len(clean_lines)} {tag_type.upper()} ʟɪɴᴇꜱ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!**")


# ==========================================
# ☠️ STEP 3: INITIATE TAG MENU ☠️
# ==========================================
@app.on_message(filters.command(["gmtag", "gntag"]) & filters.group)
async def monster_gmgn_menu(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(chat_id, user_id, client):
        return await message.reply("<emoji id=4926993814033269936>🖕</emoji> **ᴏᴜᴋᴀᴀᴛ ᴍᴇ ʀᴇʜ ʟᴏᴅᴇ!**")

    if chat_id in spam_chats:
        return await message.reply("<emoji id=6310044717241340733>🔄</emoji> **ᴛᴀɢ-ᴀʟʟ ɪꜱ ᴀʟʀᴇᴀᴅʏ ʀᴜɴɴɪɴɢ! ꜱᴛᴏᴘ ɪᴛ ꜰɪʀꜱᴛ.**")

    cmd = message.command[0].lower()
    tag_type = "gm" if "gm" in cmd else "gn"

    data = await tag_db.find_one({"_id": tag_type})
    if not data or not data.get("msgs"):
        return await message.reply(f"<emoji id=6307605493644793241>📒</emoji> **ɴᴏ {tag_type.upper()} ᴍᴇꜱꜱᴀɢᴇꜱ ꜰᴏᴜɴᴅ! ᴀᴅᴅ ꜰɪʀꜱᴛ.**")

    emoji_data = await tag_db.find_one({"_id": "premium_emojis"})
    current_emojis = emoji_data["emojis"] if emoji_data and emoji_data.get("emojis") else PREMIUM_EMOJIS

    TAG_DATA[chat_id] = {
        "type": tag_type,
        "msgs": data["msgs"],
        "emojis": current_emojis,
        "initiator": message.from_user.mention
    }

    menu_btns = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✦ 1 / 1 ✦", callback_data="xtag_1"),
            InlineKeyboardButton("✦ 3 / 3 ✦", callback_data="xtag_3")
        ],
        [InlineKeyboardButton("⛌ ᴄᴀɴᴄᴇʟ ⛌", callback_data="xtag_cancel")]
    ])

    title = "ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ" if tag_type == "gm" else "ɢᴏᴏᴅ ɴɪɢʜᴛ"
    await message.reply_text(
        f"<emoji id=4929369656797431200>🪐</emoji> **ᴀɴᴜ ᴍᴀɪɴꜰʀᴀᴍᴇ {title} ᴛᴀɢɢᴇʀ**\n\n"
        f"<emoji id=6307750079423845494>👑</emoji> ꜱᴇʟᴇᴄᴛ ʜᴏᴡ ᴍᴀɴʏ ᴜꜱᴇʀꜱ ᴛᴏ ᴛᴀɢ ᴘᴇʀ ᴍᴇꜱꜱᴀɢᴇ:",
        reply_markup=menu_btns
    )


# ==========================================
# ☠️ STEP 4: TAGGING ENGINE (FAST + DOUBLE EMOJI) ☠️
# ==========================================
@app.on_callback_query(filters.regex(r"^xtag_"))
async def gmgn_callback_handler(client, CallbackQuery):
    chat_id = CallbackQuery.message.chat.id
    user_id = CallbackQuery.from_user.id
    action = CallbackQuery.data.split("_")[1]

    if not await is_admin(chat_id, user_id, client):
        return await CallbackQuery.answer("🖕 Oukaat Me Raho! Only Admins!", show_alert=True)

    if action == "cancel":
        if chat_id in TAG_DATA: del TAG_DATA[chat_id]
        return await CallbackQuery.message.delete()

    limit = int(action)

    if chat_id in spam_chats:
        return await CallbackQuery.answer("⚠️ System is already tagging!", show_alert=True)

    spam_chats.append(chat_id)
    data = TAG_DATA.get(chat_id)
    if not data:
        spam_chats.remove(chat_id)
        return await CallbackQuery.message.delete()
        
    stop_btn = InlineKeyboardMarkup([[InlineKeyboardButton("⛌ ꜱᴛᴏᴘ ᴛᴀɢ ⛌", callback_data=f"stopx_{chat_id}")]])
    tag_name = "ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ" if data["type"] == "gm" else "ɢᴏᴏᴅ ɴɪɢʜᴛ"
    
    await CallbackQuery.edit_message_text(
        f"<emoji id=6123040393769521180>☄️</emoji> **ᴀɴᴜ {tag_name} ɪɴɪᴛɪᴀᴛᴇᴅ!**\n"
        f"<emoji id=6307821174017496029>🔥</emoji> **ᴍᴏᴅᴇ:** `{limit} ᴜꜱᴇʀꜱ / ᴍᴇꜱꜱᴀɢᴇ`\n"
        f"<emoji id=5998881015320287132>💊</emoji> **ʀᴇQᴜᴇꜱᴛᴇᴅ ʙʏ:** {data['initiator']}",
        reply_markup=stop_btn
    )

    tags = ""
    count = 0

    try:
        async for member in client.get_chat_members(chat_id):
            if chat_id not in spam_chats:
                break
            if member.user.is_bot or member.user.is_deleted:
                continue
            
            tags += f"[{member.user.first_name}](tg://user?id={member.user.id}) "
            count += 1
            
            if count >= limit:
                random_msg = random.choice(data["msgs"])
                emoji_1 = random.choice(data["emojis"])
                emoji_2 = random.choice(data["emojis"])
                
                final_text = f"{tags} {emoji_1} {random_msg} {emoji_2}"
                
                try:
                    await client.send_message(chat_id, final_text)
                except FloodWait as e:
                    await asyncio.sleep(e.value + 0.5)
                except Exception:
                    pass
                
                await asyncio.sleep(1.5) 
                tags = ""
                count = 0
                
        if tags and chat_id in spam_chats:
            random_msg = random.choice(data["msgs"])
            emoji_1 = random.choice(data["emojis"])
            emoji_2 = random.choice(data["emojis"])
            final_text = f"{tags} {emoji_1} {random_msg} {emoji_2}"
            try:
                await client.send_message(chat_id, final_text)
            except Exception:
                pass

    finally:
        if chat_id in spam_chats:
            spam_chats.remove(chat_id)
            await client.send_message(chat_id, f"<emoji id=6111742817304841054>✅</emoji> **{tag_name} ᴛᴀɢɢɪɴɢ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!**")
        if chat_id in TAG_DATA: del TAG_DATA[chat_id]


# ==========================================
# ☠️ STEP 5: STOP COMMAND & BUTTON ☠️
# ==========================================
@app.on_message(filters.command(["gmstop", "gnstop"]) & filters.group)
async def stop_x_cmd(client, message):
    chat_id = message.chat.id
    if not await is_admin(chat_id, message.from_user.id, client):
        return await message.reply("<emoji id=4926993814033269936>🖕</emoji> **ᴏɴʟʏ ᴀᴅᴍɪɴꜱ ᴄᴀɴ ꜱᴛᴏᴘ ᴛʜɪꜱ!**")
    
    if chat_id in spam_chats:
        spam_chats.remove(chat_id)
        await message.reply("<emoji id=4929369656797431200>🪐</emoji> **ᴛᴀɢɢɪɴɢ ᴀʙᴏʀᴛᴇᴅ ʙʏ ᴀᴅᴍɪɴ!**")
    else:
        await message.reply("<emoji id=6310022800023229454>✡️</emoji> **ɴᴏ ᴛᴀɢɢɪɴɢ ɪꜱ ʀᴜɴɴɪɴɢ ᴄᴜʀʀᴇɴᴛʟʏ.**")

@app.on_callback_query(filters.regex(r"^stopx_"))
async def stop_x_button(client, CallbackQuery):
    chat_id = int(CallbackQuery.data.split("_")[1])
    user_id = CallbackQuery.from_user.id
    
    if not await is_admin(chat_id, user_id, client):
        return await CallbackQuery.answer("🖕 Only Admins can stop this!", show_alert=True)
        
    if chat_id in spam_chats:
        spam_chats.remove(chat_id)
        await CallbackQuery.answer("🛑 Stopped Successfully!", show_alert=True)
        await CallbackQuery.edit_message_text("<emoji id=4929369656797431200>🪐</emoji> **ᴛᴀɢɢɪɴɢ ᴀʙᴏʀᴛᴇᴅ ʙʏ ᴀᴅᴍɪɴ!**")
    else:
        await CallbackQuery.answer("It's not running!", show_alert=True)

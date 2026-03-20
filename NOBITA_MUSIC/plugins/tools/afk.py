import time, re
from config import BOT_USERNAME
from pyrogram.enums import MessageEntityType, ParseMode
from pyrogram import filters
from pyrogram.types import Message
from NOBITA_MUSIC import app
from NOBITA_MUSIC.mongo.readable_time import get_readable_time
from NOBITA_MUSIC.mongo.afkdb import add_afk, is_afk, remove_afk

# ==========================================
# 💎 PREMIUM EMOJIS LOADED FROM ANU DB 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_CROWN = "<emoji id='6307750079423845494'>👑</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_SLEEP = "<emoji id='6309739370836399696'>🌙</emoji>"


@app.on_message(filters.command(["afk", "brb"], prefixes=["/", "!"]))
async def active_afk(_, message: Message):
    if message.sender_chat:
        return
    user_id = message.from_user.id
    verifier, reasondb = await is_afk(user_id)
    
    # Agar user pehle se AFK tha aur wapas AFK command de raha hai
    if verifier:
        await remove_afk(user_id)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))
            
            back_text = f"{E_DEVIL} <b>{message.from_user.first_name}</b> ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ!\n{E_MAGIC} <i>ᴀᴡᴀʏ ғᴏʀ: {seenago}</i>"
            if reasonafk and reasonafk != "None":
                back_text += f"\n{E_DIAMOND} <i>ʀᴇᴀsᴏɴ:</i> <code>{reasonafk}</code>"

            if afktype in ["text", "text_reason"]:
                await message.reply_text(back_text, disable_web_page_preview=True, parse_mode=ParseMode.HTML)
            elif afktype == "animation":
                await message.reply_animation(data, caption=back_text, parse_mode=ParseMode.HTML)
            elif afktype == "photo":
                # 🔥 FIX: Using direct File_ID instead of heavy local downloads
                await message.reply_photo(photo=data, caption=back_text, parse_mode=ParseMode.HTML)
        except Exception:
            await message.reply_text(f"{E_DEVIL} <b>{message.from_user.first_name}</b> ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ!", disable_web_page_preview=True, parse_mode=ParseMode.HTML)

    # 🛑 SETTING AFK DETAILS
    details = {"type": "text", "time": time.time(), "data": None, "reason": None}
    
    if len(message.command) > 1 and not message.reply_to_message:
        details["type"] = "text_reason"
        details["reason"] = (message.text.split(None, 1)[1].strip())[:100]
        
    elif message.reply_to_message:
        if message.reply_to_message.animation:
            details["type"] = "animation"
            details["data"] = message.reply_to_message.animation.file_id
            if len(message.command) > 1:
                details["reason"] = (message.text.split(None, 1)[1].strip())[:100]
                
        elif message.reply_to_message.photo:
            # 🔥 FIX: No more app.download_media(). Direct fast file_id!
            details["type"] = "photo"
            details["data"] = message.reply_to_message.photo.file_id
            if len(message.command) > 1:
                details["reason"] = (message.text.split(None, 1)[1].strip())[:100]
                
        elif message.reply_to_message.sticker:
            if message.reply_to_message.sticker.is_animated:
                details["type"] = "text_reason" if len(message.command) > 1 else "text"
            else:
                details["type"] = "photo"
                details["data"] = message.reply_to_message.sticker.file_id
            if len(message.command) > 1:
                details["reason"] = (message.text.split(None, 1)[1].strip())[:100]

    await add_afk(user_id, details)
    
    # 💎 Premium AFK Set Message
    afk_msg = f"{E_SLEEP} <b>{message.from_user.first_name}</b> ɪs ɴᴏᴡ ᴀғᴋ!"
    if details["reason"]:
        afk_msg += f"\n{E_DIAMOND} <i>ʀᴇᴀsᴏɴ:</i> <code>{details['reason']}</code>"
    await message.reply_text(afk_msg, parse_mode=ParseMode.HTML)



chat_watcher_group = 1

@app.on_message(
    ~filters.me & ~filters.bot & ~filters.via_bot,
    group=chat_watcher_group,
)
async def chat_watcher_func(_, message):
    if message.sender_chat:
        return
    userid = message.from_user.id
    user_name = message.from_user.first_name
    
    # Check if command is /afk to ignore
    if message.entities:
        possible = ["/afk", f"/afk@{BOT_USERNAME}", "!afk", ".afk"]
        message_text = message.text or message.caption
        if message_text:
            for entity in message.entities:
                if entity.type == MessageEntityType.BOT_COMMAND:
                    if (message_text[0 : 0 + entity.length]).lower() in possible:
                        return

    msg = ""
    replied_user_id = 0

    # 1. Check if Sender was AFK and came back
    verifier, reasondb = await is_afk(userid)
    if verifier:
        await remove_afk(userid)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))
            
            back_text = f"{E_DEVIL} <b>{user_name[:25]}</b> ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ!\n{E_MAGIC} <i>ᴀᴡᴀʏ ғᴏʀ: {seenago}</i>\n\n"
            if reasonafk and reasonafk != "None":
                back_text = f"{E_DEVIL} <b>{user_name[:25]}</b> ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ!\n{E_MAGIC} <i>ᴀᴡᴀʏ ғᴏʀ: {seenago}</i>\n{E_DIAMOND} <i>ʀᴇᴀsᴏɴ:</i> <code>{reasonafk}</code>\n\n"

            if afktype in ["text", "text_reason"]:
                msg += back_text
            elif afktype == "animation":
                await message.reply_animation(data, caption=back_text, parse_mode=ParseMode.HTML)
            elif afktype == "photo":
                await message.reply_photo(photo=data, caption=back_text, parse_mode=ParseMode.HTML)
        except:
            msg += f"{E_DEVIL} <b>{user_name[:25]}</b> ɪs ʙᴀᴄᴋ ᴏɴʟɪɴᴇ!\n\n"

    # 2. Check if Replied User is AFK
    if message.reply_to_message and message.reply_to_message.from_user:
        replied_first_name = message.reply_to_message.from_user.first_name
        replied_user_id = message.reply_to_message.from_user.id
        verifier, reasondb = await is_afk(replied_user_id)
        if verifier:
            try:
                afktype = reasondb["type"]
                timeafk = reasondb["time"]
                data = reasondb["data"]
                reasonafk = reasondb["reason"]
                seenago = get_readable_time((int(time.time() - timeafk)))
                
                afk_text = f"{E_SLEEP} <b>{replied_first_name[:25]}</b> ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n"
                if reasonafk and reasonafk != "None":
                    afk_text += f"{E_CROWN} <i>ʀᴇᴀsᴏɴ:</i> <code>{reasonafk}</code>\n\n"
                else:
                    afk_text += "\n"

                if afktype in ["text", "text_reason"]:
                    msg += afk_text
                elif afktype == "animation":
                    await message.reply_animation(data, caption=afk_text, parse_mode=ParseMode.HTML)
                elif afktype == "photo":
                    await message.reply_photo(photo=data, caption=afk_text, parse_mode=ParseMode.HTML)
            except Exception:
                msg += f"{E_SLEEP} <b>{replied_first_name}</b> ɪs ᴀғᴋ,\n<i>Pata nahi kab aayega...</i>\n\n"

    # 3. Check if Mentioned User is AFK
    # 🔥 BUG FIX: Removed dangerous re.findall logic. Direct Pyrogram entity parsing!
    if message.entities and (message.text or message.caption):
        text = message.text or message.caption
        for ent in message.entities:
            try:
                user_id = None
                first_name = "User"
                
                if ent.type == MessageEntityType.MENTION:
                    username = text[ent.offset : ent.offset + ent.length]
                    user = await app.get_users(username)
                    user_id = user.id
                    first_name = user.first_name
                elif ent.type == MessageEntityType.TEXT_MENTION:
                    user_id = ent.user.id
                    first_name = ent.user.first_name
                
                if user_id and user_id != replied_user_id:
                    verifier, reasondb = await is_afk(user_id)
                    if verifier:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time((int(time.time() - timeafk)))
                        
                        afk_text = f"{E_SLEEP} <b>{first_name[:25]}</b> ɪs ᴀғᴋ sɪɴᴄᴇ {seenago}\n"
                        if reasonafk and reasonafk != "None":
                            afk_text += f"{E_CROWN} <i>ʀᴇᴀsᴏɴ:</i> <code>{reasonafk}</code>\n\n"
                        else:
                            afk_text += "\n"

                        if afktype in ["text", "text_reason"]:
                            msg += afk_text
                        elif afktype == "animation":
                            await message.reply_animation(data, caption=afk_text, parse_mode=ParseMode.HTML)
                        elif afktype == "photo":
                            await message.reply_photo(photo=data, caption=afk_text, parse_mode=ParseMode.HTML)
            except Exception:
                continue

    # Final Message Sending
    if msg != "":
        try:
            await message.reply_text(msg, disable_web_page_preview=True, parse_mode=ParseMode.HTML)
        except:
            return

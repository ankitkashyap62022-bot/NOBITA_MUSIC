import random
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from NOBITA_MUSIC import app
import config
from config import MONGO_DB_URI


SUPPORT_CHAT = "NOB1TA_SUPPORT"

# ==========================================
# 💎 BOSS KE KHUD KE PREMIUM HTML EMOJIS 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_CROSS = "<emoji id='4926993814033269936'>🖕</emoji>"
E_TICK = "<emoji id='6111742817304841054'>✅</emoji>"
E_LOAD = "<emoji id='6310044717241340733'>🔄</emoji>"
E_FIRE = "<emoji id='6307821174017496029'>🔥</emoji>"
E_PLANET = "<emoji id='4929369656797431200'>🪐</emoji>"
E_FLASH = "<emoji id='6123040393769521180'>☄️</emoji>"
E_HEART = "<emoji id='5999210495146465994'>💖</emoji>"

# ==========================================
# ☠️ ANU MATRIX PREMIUM MONGODB ENGINE ☠️
# ==========================================
mongo_client = AsyncIOMotorClient(MONGO_DB_URI)
db = mongo_client.AnuMatrixMediaDB
cute_collection = db.CuteMedia
wish_collection = db.WishMedia

# ==========================================
# 🧹 DATABASE WIPE COMMANDS (OWNER ONLY) ☠️
# ==========================================
@app.on_message(filters.command("clearcute") & filters.user(int(config.OWNER_ID)))
async def clear_cute_db(_, m: Message):
    await cute_collection.delete_many({})
    await m.reply_text(f"{E_TICK} **Bᴏss, Cᴜᴛᴇ Dᴀᴛᴀʙᴀsᴇ ᴋᴀ ᴘᴜʀᴀɴᴀ sᴀᴀʀᴀ ᴋᴀᴄʜʀᴀ sᴀᴀғ ᴋᴀʀ ᴅɪʏᴀ!**")

@app.on_message(filters.command("clearwish") & filters.user(int(config.OWNER_ID)))
async def clear_wish_db(_, m: Message):
    await wish_collection.delete_many({})
    await m.reply_text(f"{E_TICK} **Bᴏss, Wɪsʜ Dᴀᴛᴀʙᴀsᴇ ᴋᴀ ᴘᴜʀᴀɴᴀ sᴀᴀʀᴀ ᴋᴀᴄʜʀᴀ sᴀᴀғ ᴋᴀʀ ᴅɪʏᴀ!**")


# ==========================================
# ☠️ ADD MEDIA COMMANDS (LIFETIME SAVE) ☠️
# ==========================================
@app.on_message(filters.command(["addcutev", "addcute"]))
async def add_cute_media(_, m: Message):
    if not m.reply_to_message or not (m.reply_to_message.video or m.reply_to_message.animation):
        return await m.reply_text(f"{E_PLANET} **Bᴏss, ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴠɪᴅᴇᴏ ᴏʀ GIF ᴛᴏ ᴀᴅᴅ ɪᴛ ᴛᴏ ᴛʜᴇ Cᴜᴛᴇ ʟɪsᴛ!**", parse_mode=ParseMode.HTML)

    reply = m.reply_to_message
    media_type = "video" if reply.video else "animation"
    file_id = reply.video.file_id if reply.video else reply.animation.file_id

    await cute_collection.insert_one({"type": media_type, "file_id": file_id})
    total = await cute_collection.count_documents({})

    await m.reply_text(f"{E_TICK} **Sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴛᴏ Cᴜᴛᴇ Mᴇᴅɪᴀ Dᴀᴛᴀʙᴀsᴇ!**\n{E_FIRE} **Tᴏᴛᴀʟ Sᴀᴠᴇᴅ:** <code>{total}</code>", parse_mode=ParseMode.HTML)


@app.on_message(filters.command(["addwishv", "addwish"]))
async def add_wish_media(_, m: Message):
    if not m.reply_to_message or not (m.reply_to_message.video or m.reply_to_message.animation):
        return await m.reply_text(f"{E_PLANET} **Bᴏss, ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴠɪᴅᴇᴏ ᴏʀ GIF ᴛᴏ ᴀᴅᴅ ɪᴛ ᴛᴏ ᴛʜᴇ Wɪsʜ ʟɪsᴛ!**", parse_mode=ParseMode.HTML)

    reply = m.reply_to_message
    media_type = "video" if reply.video else "animation"
    file_id = reply.video.file_id if reply.video else reply.animation.file_id

    await wish_collection.insert_one({"type": media_type, "file_id": file_id})
    total = await wish_collection.count_documents({})

    await m.reply_text(f"{E_TICK} **Sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴛᴏ Wɪsʜ Mᴇᴅɪᴀ Dᴀᴛᴀʙᴀsᴇ!**\n{E_FIRE} **Tᴏᴛᴀʟ Sᴀᴠᴇᴅ:** <code>{total}</code>", parse_mode=ParseMode.HTML)


# ==========================================
# ☠️ ANU MATRIX PREMIUM WISH ENGINE ☠️
# ==========================================
@app.on_message(filters.command(["wish", "iwish"]))
async def premium_wish(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text(f"{E_PLANET} **Bᴀʙʏ, ᴛᴇʟʟ ᴍᴇ ʏᴏᴜʀ ᴡɪsʜ!**\n{E_MAGIC} **Exᴀᴍᴘʟᴇ:** <code>/wish I want to meet you</code>", parse_mode=ParseMode.HTML)

    random_media = await wish_collection.aggregate([{"$sample": {"size": 1}}]).to_list(length=1)

    if not random_media:
        return await m.reply_text(f"{E_CROSS} **Wɪsʜ Dᴀᴛᴀʙᴀsᴇ ɪs ᴇᴍᴘᴛʏ!**\nPʟᴇᴀsᴇ ᴜsᴇ <code>/addwishv</code> ʙʏ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴀ ᴠɪᴅᴇᴏ ꜰɪʀsᴛ.", parse_mode=ParseMode.HTML)

    mystic = await m.reply_text(f"{E_LOAD} **Cᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ᴛʜᴇ Sᴛᴀʀs...**", parse_mode=ParseMode.HTML)
    await asyncio.sleep(0.5)

    text = m.text.split(None, 1)[1]
    wish_count = random.randint(1, 100)

    if wish_count <= 30:
        remark = f"{E_CROSS} **Tᴏᴜɢʜ ʟᴜᴄᴋ ʙᴀʙʏ, ʙᴜᴛ ᴍɪʀᴀᴄʟᴇs ᴅᴏ ʜᴀᴘᴘᴇɴ!**"
    elif wish_count <= 70:
        remark = f"{E_FLASH} **Tʜᴇ sᴛᴀʀs ᴀʀᴇ ᴀʟɪɢɴɪɴɢ... Kᴇᴇᴘ ʜᴏᴘɪɴɢ!**"
    else:
        remark = f"{E_HEART} **Yᴏᴜʀ ᴡɪsʜ ɪs ᴍʏ ᴄᴏᴍᴍᴀɴᴅ! Gʀᴀɴᴛᴇᴅ sᴏᴏɴ.**"

    wish_text = f"""
{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗠 𝗔 𝗚 𝗜 𝗖  𝗪 𝗜 𝗦 𝗛 』</b> {E_DIAMOND}
━━━━━━━━━━━━━━━━━━━━
{E_HEART} <b>Wɪsʜᴇʀ:</b> {m.from_user.mention}
{E_FLASH} <b>Wɪsʜ:</b> <code>{text}</code>

{E_FIRE} <b>Pʀᴏʙᴀʙɪʟɪᴛʏ:</b> <b>{wish_count}%</b>
{remark}
━━━━━━━━━━━━━━━━━━━━
"""

    media_data = random_media[0]
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("✨ Sᴜᴘᴘᴏʀᴛ ✨", url=f"https://t.me/{SUPPORT_CHAT}")]])

    try:
        if media_data["type"] == "video":
            await m.reply_video(video=media_data["file_id"], caption=wish_text, reply_markup=markup, parse_mode=ParseMode.HTML)
        else:
            await m.reply_animation(animation=media_data["file_id"], caption=wish_text, reply_markup=markup, parse_mode=ParseMode.HTML)
        await mystic.delete()
        
    except Exception as e:
        # 🔥 SMART AUTO-CLEANER: Agar purani/invalid file aayi, to khud delete kar dega!
        if "DOCUMENT_INVALID" in str(e) or "FILE_REFERENCE" in str(e):
            await wish_collection.delete_one({"_id": media_data["_id"]})
            await mystic.edit_text(f"{E_CROSS} <b>Anu Matrix Auto-Clean:</b>\n<i>Ek purani dead video detect hui thi, maine use DB se uda diya! Wapas command do.</i>", parse_mode=ParseMode.HTML)
        else:
            await mystic.edit_text(f"{E_CROSS} **Eʀʀᴏʀ:** `{e}`")


# ==========================================
# ☠️ ANU MATRIX PREMIUM CUTENESS METER ☠️
# ==========================================
@app.on_message(filters.command(["cute", "cuteness"]))
async def premium_cute(_, m: Message):
    random_media = await cute_collection.aggregate([{"$sample": {"size": 1}}]).to_list(length=1)

    if not random_media:
        return await m.reply_text(f"{E_CROSS} **Cᴜᴛᴇ Dᴀᴛᴀʙᴀsᴇ ɪs ᴇᴍᴘᴛʏ!**\nPʟᴇᴀsᴇ ᴜsᴇ <code>/addcutev</code> ʙʏ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴀ ᴠɪᴅᴇᴏ ꜰɪʀsᴛ.", parse_mode=ParseMode.HTML)

    target = m.reply_to_message.from_user if m.reply_to_message else m.from_user
    mystic = await m.reply_text(f"{E_LOAD} **Sᴄᴀɴɴɪɴɢ Cᴜᴛᴇɴᴇss Lᴇᴠᴇʟs...**", parse_mode=ParseMode.HTML)
    await asyncio.sleep(0.5)

    mm = random.randint(1, 100)

    if mm <= 30:
        remark = f"{E_CROSS} **Yᴏᴜ ʜᴀᴠᴇ ᴀ ʜɪᴅᴅᴇɴ ᴄʜᴀʀᴍ, ᴊᴜsᴛ ᴠᴇʀʏ... ʜɪᴅᴅᴇɴ.**"
    elif mm <= 70:
        remark = f"{E_FLASH} **Aᴡᴡ! Pʀᴇᴛᴛʏ ᴅᴀᴍɴ ᴄᴜᴛᴇ, I ᴍᴜsᴛ sᴀʏ.**"
    else:
        remark = f"{E_HEART} **Iʟʟᴇɢᴀʟ ʟᴇᴠᴇʟs ᴏғ ᴄᴜᴛᴇɴᴇss! Aʀʀᴇsᴛ ᴛʜɪs ᴘᴇʀsᴏɴ!**"

    cute_text = f"""
{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗖 𝗨 𝗧 𝗘  𝗠 𝗘 𝗧 𝗘 𝗥 』</b> {E_DIAMOND}
━━━━━━━━━━━━━━━━━━━━
{E_HEART} <b>Tᴀʀɢᴇᴛ:</b> {target.mention}
{E_FIRE} <b>Cᴜᴛᴇɴᴇss:</b> <b>{mm}%</b>

{remark}
━━━━━━━━━━━━━━━━━━━━
"""

    media_data = random_media[0]
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("✨ Sᴜᴘᴘᴏʀᴛ ✨", url=f"https://t.me/{SUPPORT_CHAT}")]])

    try:
        if media_data["type"] == "video":
            await m.reply_video(video=media_data["file_id"], caption=cute_text, reply_markup=markup, parse_mode=ParseMode.HTML)
        else:
            await m.reply_animation(animation=media_data["file_id"], caption=cute_text, reply_markup=markup, parse_mode=ParseMode.HTML)
        await mystic.delete()
        
    except Exception as e:
        # 🔥 SMART AUTO-CLEANER FOR CUTE DB
        if "DOCUMENT_INVALID" in str(e) or "FILE_REFERENCE" in str(e):
            await cute_collection.delete_one({"_id": media_data["_id"]})
            await mystic.edit_text(f"{E_CROSS} <b>Anu Matrix Auto-Clean:</b>\n<i>Ek purani dead video thi DB me, maine use permanently delete kar diya! Phir se try kar.</i>", parse_mode=ParseMode.HTML)
        else:
            await mystic.edit_text(f"{E_CROSS} **Eʀʀᴏʀ:** `{e}`")

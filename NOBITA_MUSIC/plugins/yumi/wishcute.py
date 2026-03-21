import random
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from NOBITA_MUSIC import app
from config import MONGO_DB_URI

SUPPORT_CHAT = "NOB1TA_SUPPORT"

# ==========================================
# ☠️ ANU MATRIX PREMIUM MONGODB ENGINE ☠️
# ==========================================
# Connecting to MongoDB
mongo_client = AsyncIOMotorClient(MONGO_DB_URI)
db = mongo_client.AnuMatrixMediaDB
cute_collection = db.CuteMedia
wish_collection = db.WishMedia

# ==========================================
# ☠️ ADD MEDIA COMMANDS (LIFETIME SAVE) ☠️
# ==========================================
@app.on_message(filters.command(["addcutev", "addcute"]))
async def add_cute_media(_, m: Message):
    if not m.reply_to_message:
        return await m.reply_text("<emoji id=4929369656797431200>🪐</emoji> **Bᴏss, ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴠɪᴅᴇᴏ ᴏʀ GIF ᴛᴏ ᴀᴅᴅ ɪᴛ ᴛᴏ ᴛʜᴇ Cᴜᴛᴇ ʟɪsᴛ!**")
    
    reply = m.reply_to_message
    if reply.video:
        media_type, file_id = "video", reply.video.file_id
    elif reply.animation:
        media_type, file_id = "animation", reply.animation.file_id
    else:
        return await m.reply_text("<emoji id=6307821174017496029>❌</emoji> **I ᴄᴀɴ ᴏɴʟʏ sᴛᴏʀᴇ Vɪᴅᴇᴏs ᴏʀ GIFs ʙᴏss!**")
        
    # Saving to MongoDB
    await cute_collection.insert_one({"type": media_type, "file_id": file_id})
    total = await cute_collection.count_documents({})
    
    await m.reply_text(f"<emoji id=6111742817304841054>✅</emoji> **Sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴛᴏ Cᴜᴛᴇ Mᴇᴅɪᴀ Dᴀᴛᴀʙᴀsᴇ!**\n<emoji id=6307358404176254008>🔥</emoji> **Tᴏᴛᴀʟ Sᴀᴠᴇᴅ:** `{total}`")


@app.on_message(filters.command(["addwishv", "addwish"]))
async def add_wish_media(_, m: Message):
    if not m.reply_to_message:
        return await m.reply_text("<emoji id=4929369656797431200>🪐</emoji> **Bᴏss, ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴠɪᴅᴇᴏ ᴏʀ GIF ᴛᴏ ᴀᴅᴅ ɪᴛ ᴛᴏ ᴛʜᴇ Wɪsʜ ʟɪsᴛ!**")
    
    reply = m.reply_to_message
    if reply.video:
        media_type, file_id = "video", reply.video.file_id
    elif reply.animation:
        media_type, file_id = "animation", reply.animation.file_id
    else:
        return await m.reply_text("<emoji id=6307821174017496029>❌</emoji> **I ᴄᴀɴ ᴏɴʟʏ sᴛᴏʀᴇ Vɪᴅᴇᴏs ᴏʀ GIFs ʙᴏss!**")
        
    # Saving to MongoDB
    await wish_collection.insert_one({"type": media_type, "file_id": file_id})
    total = await wish_collection.count_documents({})
    
    await m.reply_text(f"<emoji id=6111742817304841054>✅</emoji> **Sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴛᴏ Wɪsʜ Mᴇᴅɪᴀ Dᴀᴛᴀʙᴀsᴇ!**\n<emoji id=6307358404176254008>🔥</emoji> **Tᴏᴛᴀʟ Sᴀᴠᴇᴅ:** `{total}`")


# ==========================================
# ☠️ ANU MATRIX PREMIUM WISH ENGINE ☠️
# ==========================================
@app.on_message(filters.command(["wish", "iwish"]))
async def premium_wish(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("<emoji id=4929369656797431200>🪐</emoji> **Bᴀʙʏ, ᴛᴇʟʟ ᴍᴇ ʏᴏᴜʀ ᴡɪsʜ!**\n<emoji id=6152142357727811958>✨</emoji> **Exᴀᴍᴘʟᴇ:** `/wish I ᴡᴀɴᴛ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ`")

    # Fast fetch one random item from MongoDB
    random_media = await wish_collection.aggregate([{"$sample": {"size": 1}}]).to_list(length=1)
    
    if not random_media:
        return await m.reply_text("⚠️ **Wɪsʜ Dᴀᴛᴀʙᴀsᴇ ɪs ᴇᴍᴘᴛʏ!**\nPʟᴇᴀsᴇ ᴜsᴇ `/addwishv` ʙʏ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴀ ᴠɪᴅᴇᴏ ꜰɪʀsᴛ.")

    mystic = await m.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Cᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ᴛʜᴇ Sᴛᴀʀs...**")
    await asyncio.sleep(0.5)

    text = m.text.split(None, 1)[1]
    wish_count = random.randint(1, 100)

    # 💎 DYNAMIC ROMANTIC RESPONSES 💎
    if wish_count <= 30:
        remark = "<emoji id=5260342787882103328>💔</emoji> **Tᴏᴜɢʜ ʟᴜᴄᴋ ʙᴀʙʏ, ʙᴜᴛ ᴍɪʀᴀᴄʟᴇs ᴅᴏ ʜᴀᴘᴘᴇɴ!**"
    elif wish_count <= 70:
        remark = "<emoji id=5328250499642698740>❤️‍🩹</emoji> **Tʜᴇ sᴛᴀʀs ᴀʀᴇ ᴀʟɪɢɴɪɴɢ... Kᴇᴇᴘ ʜᴏᴘɪɴɢ!**"
    else:
        remark = "<emoji id=5314782352226958463>💖</emoji> **Yᴏᴜʀ ᴡɪsʜ ɪs ᴍʏ ᴄᴏᴍᴍᴀɴᴅ! Gʀᴀɴᴛᴇᴅ sᴏᴏɴ.**"

    wish_text = f"""
<emoji id=5361877607732230009>💘</emoji> **Aɴᴜ Mᴀᴛʀɪx Mᴀɢɪᴄ ᴡɪsʜ** <emoji id=5361877607732230009>💘</emoji>

<emoji id=5854743260840596378>👤</emoji> **Wɪsʜᴇʀ:** {m.from_user.mention}
<emoji id=6123040393769521180>☄️</emoji> **Wɪsʜ:** `{text}`

<emoji id=6307358404176254008>🔥</emoji> **Pʀᴏʙᴀʙɪʟɪᴛʏ:** **{wish_count}%**
{remark}
"""
    
    media_data = random_media[0]
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("✨ Sᴜᴘᴘᴏʀᴛ ✨", url=f"https://t.me/{SUPPORT_CHAT}")]])

    try:
        if media_data["type"] == "video":
            await m.reply_video(video=media_data["file_id"], caption=wish_text, reply_markup=markup)
        else:
            await m.reply_animation(animation=media_data["file_id"], caption=wish_text, reply_markup=markup)
        
        # Fixing Edit Bug (Delete loading msg)
        await mystic.delete()
    except Exception as e:
        await mystic.edit_text(f"<emoji id=6307821174017496029>❌</emoji> **Eʀʀᴏʀ Dᴇᴛᴇᴄᴛᴇᴅ!**\n`{e}`")


# ==========================================
# ☠️ ANU MATRIX PREMIUM CUTENESS METER ☠️
# ==========================================
@app.on_message(filters.command(["cute", "cuteness"]))
async def premium_cute(_, m: Message):
    # Fast fetch one random item from MongoDB
    random_media = await cute_collection.aggregate([{"$sample": {"size": 1}}]).to_list(length=1)

    if not random_media:
        return await m.reply_text("⚠️ **Cᴜᴛᴇ Dᴀᴛᴀʙᴀsᴇ ɪs ᴇᴍᴘᴛʏ!**\nPʟᴇᴀsᴇ ᴜsᴇ `/addcutev` ʙʏ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴀ ᴠɪᴅᴇᴏ ꜰɪʀsᴛ.")

    target = m.reply_to_message.from_user if m.reply_to_message else m.from_user
    
    mystic = await m.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Sᴄᴀɴɴɪɴɢ Cᴜᴛᴇɴᴇss Lᴇᴠᴇʟs...**")
    await asyncio.sleep(0.5)

    mm = random.randint(1, 100)

    # 💎 DYNAMIC ROMANTIC RESPONSES 💎
    if mm <= 30:
        remark = "<emoji id=5260342787882103328>💔</emoji> **Yᴏᴜ ʜᴀᴠᴇ ᴀ ʜɪᴅᴅᴇɴ ᴄʜᴀʀᴍ, ᴊᴜsᴛ ᴠᴇʀʏ... ʜɪᴅᴅᴇɴ.**"
    elif mm <= 70:
        remark = "<emoji id=5328250499642698740>❤️‍🩹</emoji> **Aᴡᴡ! Pʀᴇᴛᴛʏ ᴅᴀᴍɴ ᴄᴜᴛᴇ, I ᴍᴜsᴛ sᴀʏ.**"
    else:
        remark = "<emoji id=5314782352226958463>💖</emoji> **Iʟʟᴇɢᴀʟ ʟᴇᴠᴇʟs ᴏғ ᴄᴜᴛᴇɴᴇss! Aʀʀᴇsᴛ ᴛʜɪs ᴘᴇʀsᴏɴ!**"

    cute_text = f"""
<emoji id=5314782352226958463>💖</emoji> **Aɴᴜ Mᴀᴛʀɪx Cᴜᴛᴇɴᴇss Mᴇᴛᴇʀ** <emoji id=5314782352226958463>💖</emoji>

<emoji id=5854743260840596378>👤</emoji> **Tᴀʀɢᴇᴛ:** {target.mention}
<emoji id=6307358404176254008>🔥</emoji> **Cᴜᴛᴇɴᴇss:** **{mm}%**

{remark}
"""

    media_data = random_media[0]
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("✨ Sᴜᴘᴘᴏʀᴛ ✨", url=f"https://t.me/{SUPPORT_CHAT}")]])

    try:
        if media_data["type"] == "video":
            await m.reply_video(video=media_data["file_id"], caption=cute_text, reply_markup=markup)
        else:
            await m.reply_animation(animation=media_data["file_id"], caption=cute_text, reply_markup=markup)
            
        # Fixing Edit Bug
        await mystic.delete()
    except Exception as e:
        await mystic.edit_text(f"<emoji id=6307821174017496029>❌</emoji> **Eʀʀᴏʀ Dᴇᴛᴇᴄᴛᴇᴅ!**\n`{e}`")

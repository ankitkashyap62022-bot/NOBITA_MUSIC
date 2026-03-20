from pyrogram import filters
from pyrogram.enums import ParseMode

from NOBITA_MUSIC import YouTube, app
from NOBITA_MUSIC.utils.channelplay import get_channeplayCB
from NOBITA_MUSIC.utils.decorators.language import languageCB
from NOBITA_MUSIC.utils.stream.stream import stream
from config import BANNED_USERS

# ==========================================
# 💎 PREMIUM EMOJIS LOADED FROM ANU DB 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_CROWN = "<emoji id='6307750079423845494'>👑</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_CROSS = "<emoji id='6151981777490548710'>❌</emoji>"

# ==========================================
# 🚀 ANU SUPREME LIVE STREAM HANDLER ☠️
# ==========================================
@app.on_callback_query(filters.regex("LiveStream") & ~BANNED_USERS)
@languageCB
async def play_live_stream(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    vidid, user_id, mode, cplay, fplay = callback_request.split("|")
    
    # 🛑 Authorization Check
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(f"⚠️ {_['playcb_1']}", show_alert=True)
        except:
            return
            
    try:
        chat_id, channel = await get_channeplayCB(_, cplay, CallbackQuery)
    except:
        return
        
    video = True if mode == "v" else None
    user_name = CallbackQuery.from_user.first_name
    await CallbackQuery.message.delete()
    
    try:
        await CallbackQuery.answer()
    except:
        pass
        
    # 💎 Premium Initial Message
    mystic = await CallbackQuery.message.reply_text(
        f"{E_MAGIC} <i>Anu Mainframe: Initializing Live Stream for {channel if channel else 'this chat'}...</i>",
        parse_mode=ParseMode.HTML
    )
    
    try:
        details, track_id = await YouTube.track(vidid, True)
    except:
        return await mystic.edit_text(f"{E_CROSS} <b>Anu Error:</b> {_['play_3']}", parse_mode=ParseMode.HTML)
        
    ffplay = True if fplay == "f" else None
    
    # 🎧 Check if it's actually a Live Stream
    if not details["duration_min"]:
        try:
            await stream(
                _,
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                CallbackQuery.message.chat.id,
                video,
                streamtype="live",
                forceplay=ffplay,
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else _["general_2"].format(ex_type)
            return await mystic.edit_text(f"{E_DEVIL} <b>System Fucked Up:</b> {err}", parse_mode=ParseMode.HTML)
    else:
        # ☠️ Toxic Sigma Reply for Normal Videos
        toxic_msg = f"{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗘 𝗠 𝗣 𝗜 𝗥 𝗘 』</b> {E_DIAMOND}\n\n{E_DEVIL} <b>Abe andhe lode, ye koi Live Stream nahi hai!</b>\n{E_CROWN} <i>Normal gaane bajane ke liye normal Play button use kar!</i>"
        return await mystic.edit_text(toxic_msg, parse_mode=ParseMode.HTML)
        
    # 🔥 FIX: Added Parentheses () to delete the processing message properly!
    await mystic.delete()

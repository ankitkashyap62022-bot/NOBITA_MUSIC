import asyncio
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultPhoto,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from youtubesearchpython.__future__ import VideosSearch

from NOBITA_MUSIC import app
from NOBITA_MUSIC.utils.inlinequery import answer
from config import BANNED_USERS

@app.on_inline_query(~BANNED_USERS)
async def premium_inline_query_handler(client, query):
    text = query.query.strip().lower()
    
    # ☠️ STEP 1: EMPTY QUERY HANDLER ☠️
    if text.strip() == "":
        try:
            await client.answer_inline_query(query.id, results=answer, cache_time=10)
        except Exception:
            pass
        return

    # ☠️ STEP 2: YOUTUBE ADVANCED SEARCH ENGINE ☠️
    try:
        answers = []
        search = VideosSearch(text, limit=15)
        results = (await search.next()).get("result")
        
        if not results:
            return

        # ☠️ STEP 3: DYNAMIC DATA EXTRACTION ☠️
        for result in results:
            title = result.get("title", "Unknown Title").title()
            duration = result.get("duration", "Unknown")
            views = result.get("viewCount", {}).get("short", "Unknown Views")
            
            try:
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            except Exception:
                thumbnail = "https://telegra.ph/file/default_music_thumb.jpg" 
                
            channellink = result.get("channel", {}).get("link", "https://youtube.com")
            channel = result.get("channel", {}).get("name", "Unknown Channel")
            link = result.get("link", "https://youtube.com")
            published = result.get("publishedTime", "Unknown")

            description = f"👀 {views} | ⏳ {duration} ᴍɪɴ | 🎥 {channel}"

            # 💎 THE SIGMA BYPASS BUTTONS (JioSaavn Linker) 💎
            buttons = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="🎥 ᴡᴀᴛᴄʜ ᴏɴ ʏᴏᴜᴛᴜʙᴇ", url=link),
                    InlineKeyboardButton(text="🍷 ꜱʜᴀʀᴇ", switch_inline_query=text)
                ],
                [
                    # ☠️ YAHAN MAGIC HAI! Ye direct chat me /play auto-fill kar dega! ☠️
                    InlineKeyboardButton(text="🎧 ᴘʟᴀʏ ɪɴ ᴠᴄ", switch_inline_query_current_chat=f"/play {title}"),
                    InlineKeyboardButton(text="📥 ᴅᴏᴡɴʟᴏᴀᴅ", switch_inline_query_current_chat=f"/song {title}")
                ]
            ])

            searched_text = f"""
<emoji id=6123040393769521180>☄️</emoji> **ʏᴏᴜᴛᴜʙᴇ ꜱᴇᴀʀᴄʜ ʀᴇꜱᴜʟᴛꜱ** <emoji id=6123040393769521180>☄️</emoji>

<emoji id=4929369656797431200>🪐</emoji> **ᴛɪᴛʟᴇ :** [{title}]({link})
<emoji id=5256131095094652290>⏱️</emoji> **ᴅᴜʀᴀᴛɪᴏɴ :** `{duration}`
<emoji id=6307346833534359338>🍷</emoji> **ᴠɪᴇᴡꜱ :** `{views}`
<emoji id=6307750079423845494>👑</emoji> **ᴄʜᴀɴɴᴇʟ :** [{channel}]({channellink})
<emoji id=6152142357727811958>✨</emoji> **ᴘᴜʙʟɪꜱʜᴇᴅ :** `{published}`

<emoji id=5354924568492383911>😈</emoji> **ᴘᴏᴡᴇʀᴇᴅ ʙʏ » {app.name}**"""

            answers.append(
                InlineQueryResultPhoto(
                    photo_url=thumbnail,
                    title=title,
                    thumb_url=thumbnail,
                    description=description,
                    caption=searched_text,
                    reply_markup=buttons,
                )
            )

        # ☠️ STEP 4: DELIVERING RESULTS ☠️
        if answers:
            try:
                await client.answer_inline_query(query.id, results=answers, cache_time=10)
            except Exception as e:
                pass
                
    except Exception as e:
        return

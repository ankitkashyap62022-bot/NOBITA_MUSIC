import asyncio
import os
import shutil
import socket
from datetime import datetime

import urllib3
import aiohttp
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import filters
from pyrogram.types import Message
from io import BytesIO

import config
from NOBITA_MUSIC import app
from NOBITA_MUSIC.misc import HAPP, SUDOERS, XCB
from NOBITA_MUSIC.utils.database import (
    get_active_chats,
    remove_active_chat,
    remove_active_video_chat,
)
from NOBITA_MUSIC.utils.pastebin import NOBITABin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================
# ☠️ ANU MATRIX SERVER CONTROLS ☠️
# ==========================================

async def is_heroku():
    return "heroku" in socket.getfqdn()

@app.on_message(filters.command(["get_log", "logs", "getlogs", "log"]) & SUDOERS)
async def premium_log(client, message: Message):
    mystic = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Eхᴛʀᴀᴄᴛɪɴɢ Aɴᴜ Mᴀᴛʀɪx Sᴇʀᴠᴇʀ Lᴏɢs...**")
    try:
        await message.reply_document(
            document="log.txt",
            caption="<emoji id=5354924568492383911>😈</emoji> **Bᴏss, ʜᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ʟᴀᴛᴇsᴛ sᴇʀᴠᴇʀ ʟᴏɢs!**"
        )
        await mystic.delete()
    except Exception as e:
        await mystic.edit_text(f"<emoji id=6307821174017496029>❌</emoji> **Fᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ʟᴏɢs!**\n\n`{e}`")


@app.on_message(filters.command(["update", "gitpull", "up"]) & SUDOERS)
async def premium_update(client, message: Message):
    if await is_heroku():
        if HAPP is None:
            return await message.reply_text("<emoji id=6307821174017496029>❌</emoji> **Hᴇʀᴏᴋᴜ API Kᴇʏ ᴏʀ Aᴘᴘ Nᴀᴍᴇ ɪs ᴍɪssɪɴɢ!**")
            
    response = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Sᴄᴀɴɴɪɴɢ Aɴᴜ Mᴀᴛʀɪx Mᴀɪɴғʀᴀᴍᴇ ꜰᴏʀ Uᴘᴅᴀᴛᴇs...**")
    
    try:
        repo = Repo()
    except GitCommandError:
        return await response.edit("<emoji id=6307821174017496029>❌</emoji> **Gɪᴛ Cᴏᴍᴍᴀɴᴅ Eʀʀᴏʀ!**")
    except InvalidGitRepositoryError:
        return await response.edit("<emoji id=6307821174017496029>❌</emoji> **Iɴᴠᴀʟɪᴅ Gɪᴛ Rᴇᴘᴏsɪᴛᴏʀʏ!**")
        
    os.system(f"git fetch origin {config.UPSTREAM_BRANCH} &> /dev/null")
    await asyncio.sleep(3) # Made it faster (7 to 3 seconds)
    
    verification = ""
    REPO_ = repo.remotes.origin.url.split(".git")[0]
    for checks in repo.iter_commits(f"HEAD..origin/{config.UPSTREAM_BRANCH}"):
        verification = str(checks.count())
        
    if verification == "":
        return await response.edit("<emoji id=6111742817304841054>✅</emoji> **Aɴᴜ Mᴀᴛʀɪx ɪs ᴀʟʀᴇᴀᴅʏ Uᴘ-Tᴏ-Dᴀᴛᴇ ʙᴀʙʏ!**")
        
    updates = ""
    ordinal = lambda format: "%d%s" % (
        format,
        "tsnrhtdd"[(format // 10 % 10 != 1) * (format % 10 < 4) * format % 10 :: 4],
    )
    for info in repo.iter_commits(f"HEAD..origin/{config.UPSTREAM_BRANCH}"):
        updates += f"<b>➣ #{info.count()}: <a href={REPO_}/commit/{info}>{info.summary}</a> ʙʏ -> {info.author}</b>\n\t\t\t\t<b>➥ Cᴏᴍᴍɪᴛᴇᴅ Oɴ :</b> {ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} {datetime.fromtimestamp(info.committed_date).strftime('%b')}, {datetime.fromtimestamp(info.committed_date).strftime('%Y')}\n\n"
        
    _update_response_ = "<emoji id=6123040393769521180>☄️</emoji> **A Nᴇᴡ Uᴘᴅᴀᴛᴇ Is Aᴠᴀɪʟᴀʙʟᴇ Fᴏʀ Aɴᴜ Mᴀᴛʀɪx!**\n\n<emoji id=5256131095094652290>⏱️</emoji> `Pᴜsʜɪɴɢ Uᴘᴅᴀᴛᴇs Tᴏ Sᴇʀᴠᴇʀ...`\n\n<b><u>Uᴘᴅᴀᴛᴇs Lᴏɢs:</u></b>\n\n"
    _final_updates_ = _update_response_ + updates
    
    if len(_final_updates_) > 4096:
        url = await NOBITABin(updates) # ☠️ BUG FIXED HERE ☠️
        nrs = await response.edit(
            f"<emoji id=6123040393769521180>☄️</emoji> **Aɴᴜ Mᴀᴛʀɪx Uᴘᴅᴀᴛᴇ Aᴠᴀɪʟᴀʙʟᴇ!**\n\n<emoji id=5256131095094652290>⏱️</emoji> `Pᴜsʜɪɴɢ Uᴘᴅᴀᴛᴇs Tᴏ Sᴇʀᴠᴇʀ...`\n\n<emoji id=6307605493644793241>📒</emoji> <a href='{url}'>Cʟɪᴄᴋ Hᴇʀᴇ Tᴏ Vɪᴇᴡ Uᴘᴅᴀᴛᴇs Lᴏɢ</a>",
            disable_web_page_preview=True
        )
    else:
        nrs = await response.edit(_final_updates_, disable_web_page_preview=True)
        
    os.system("git stash &> /dev/null && git pull")

    try:
        served_chats = await get_active_chats()
        for x in served_chats:
            try:
                await app.send_message(
                    chat_id=int(x),
                    text=f"<emoji id=6310044717241340733>🔄</emoji> **{app.mention} Sʏsᴛᴇᴍ Uᴘᴅᴀᴛɪɴɢ...**\n<emoji id=5256131095094652290>⏱️</emoji> Sᴛʀᴇᴀᴍ ᴡɪʟʟ ʀᴇsᴜᴍᴇ ɪɴ 15-20 sᴇᴄᴏɴᴅs!",
                )
                await remove_active_chat(x)
                await remove_active_video_chat(x)
            except:
                pass
        await response.edit(f"{nrs.text}\n\n<emoji id=6111742817304841054>✅</emoji> **Bᴏᴛ Uᴘᴅᴀᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ! Rᴇʙᴏᴏᴛɪɴɢ...**")
    except:
        pass

    if await is_heroku():
        try:
            os.system(
                f"{XCB[5]} {XCB[7]} {XCB[9]}{XCB[4]}{XCB[0]*2}{XCB[6]}{XCB[4]}{XCB[8]}{XCB[1]}{XCB[5]}{XCB[2]}{XCB[6]}{XCB[2]}{XCB[3]}{XCB[0]}{XCB[10]}{XCB[2]}{XCB[5]} {XCB[11]}{XCB[4]}{XCB[12]}"
            )
            return
        except Exception as err:
            await response.edit(f"{nrs.text}\n\n<emoji id=6307821174017496029>❌</emoji> **Fᴀɪʟᴇᴅ Tᴏ Rᴇsᴛᴀʀᴛ!**")
            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"⚠️ Uᴘᴅᴀᴛᴇ Eʀʀᴏʀ: `{err}`",
            )
    else:
        os.system("pip3 install -r requirements.txt")
        os.system(f"kill -9 {os.getpid()} && bash start")
        exit()


@app.on_message(filters.command(["restart", "reboot"]) & SUDOERS)
async def premium_restart(client, message: Message):
    response = await message.reply_text("<emoji id=6310044717241340733>🔄</emoji> **Iɴɪᴛɪᴀʟɪᴢɪɴɢ Aɴᴜ Mᴀᴛʀɪx Rᴇʙᴏᴏᴛ Sᴇǫᴜᴇɴᴄᴇ...**")
    
    # ☠️ WARN ACTIVE CHATS ☠️
    ac_chats = await get_active_chats()
    for x in ac_chats:
        try:
            await app.send_message(
                chat_id=int(x),
                text=f"<emoji id=6310044717241340733>🔄</emoji> **{app.mention} ɪs Rᴇʙᴏᴏᴛɪɴɢ...**\n\n<emoji id=5256131095094652290>⏱️</emoji> Yᴏᴜ ᴄᴀɴ sᴛᴀʀᴛ ᴘʟᴀʏɪɴɢ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 15-20 sᴇᴄᴏɴᴅs.",
            )
            await remove_active_chat(x)
            await remove_active_video_chat(x)
        except:
            pass

    # ☠️ FLUSH JUNK CACHE ☠️
    try:
        shutil.rmtree("downloads")
        shutil.rmtree("raw_files")
        shutil.rmtree("cache")
    except:
        pass
        
    await response.edit_text(
        "<emoji id=6111742817304841054>✅</emoji> **Sʏsᴛᴇᴍ Fʟᴜsʜᴇᴅ & Tᴇᴍᴘ Fɪʟᴇs Cʟᴇᴀʀᴇᴅ!**\n\n<emoji id=6123040393769521180>☄️</emoji> `Rᴇsᴛᴀʀᴛ Pʀᴏᴄᴇss Sᴛᴀʀᴛᴇᴅ... Wᴀɪᴛ 10 sᴇᴄᴏɴᴅs!`"
    )
    
    # ☠️ THE KILL SWITCH ☠️
    os.system(f"kill -9 {os.getpid()} && bash start")


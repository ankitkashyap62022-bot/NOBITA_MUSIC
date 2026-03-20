import os
import re
import subprocess
import sys
import traceback
from inspect import getfullargspec
from io import StringIO
from time import time
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from NOBITA_MUSIC import app
import config  # 🔥 FIX: For OWNER_ID

# ==========================================
# 💎 PREMIUM EMOJIS LOADED FROM ANU DB 💎
# ==========================================
E_DEVIL = "<emoji id='5352542184493031170'>😈</emoji>"
E_CROWN = "<emoji id='6307750079423845494'>👑</emoji>"
E_DIAMOND = "<emoji id='4929195195225867512'>💎</emoji>"
E_MAGIC = "<emoji id='5352870513267973607'>✨</emoji>"
E_CROSS = "<emoji id='6151981777490548710'>❌</emoji>"
E_TICK = "<emoji id='6001589602085771497'>✅</emoji>"

# Helper Functions
async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})

# ==========================================
# 🚀 ANU SUPREME PYTHON EXECUTOR (/eval) ☠️
# ==========================================
# 🔥 FIX: SUDOERS hata kar filters.user(config.OWNER_ID) laga diya (Only Owner Access)
@app.on_edited_message(filters.command("eval") & filters.user(config.OWNER_ID) & ~filters.forwarded & ~filters.via_bot)
@app.on_message(filters.command("eval") & filters.user(config.OWNER_ID) & ~filters.forwarded & ~filters.via_bot)
async def executor(client: app, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text=f"{E_DEVIL} <b>Abe Boss! Code toh likh jise execute karna hai!</b>\n<i>Example:</i> <code>/eval print('Anu is Queen')</code>", parse_mode=ParseMode.HTML)
        
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
        
    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
        
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success (No Output Returned)"
        
    # 💎 PREMIUM UI Formatting
    final_output = f"""
{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗧 𝗘 𝗥 𝗠 𝗜 𝗡 𝗔 𝗟 』</b> {E_DIAMOND}
━━━━━━━━━━━━━━━━━━━━
{E_MAGIC} <b>𝗘𝘅𝗲𝗰𝘂𝘁𝗲𝗱 :</b>
<pre language='python'>{evaluation}</pre>
"""
    if len(final_output) > 4096:
        filename = "Anu_Output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation))
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="⏳ 𝗘𝘅𝗲𝗰𝘂𝘁𝗶𝗼𝗻 𝗧𝗶𝗺𝗲", callback_data=f"runtime {t2-t1} Seconds")]]
        )
        await message.reply_document(
            document=filename,
            caption=f"{E_CROWN} <b>Anu Matrix: Result Document</b>\n\n<i>Code was too long for Telegram. Attached as file.</i>",
            quote=False,
            reply_markup=keyboard,
        )
        await message.delete()
        os.remove(filename)
    else:
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="⏳", callback_data=f"runtime {round(t2-t1, 3)} Seconds"),
                    InlineKeyboardButton(text="🗑 𝗖𝗹𝗼𝘀𝗲", callback_data=f"forceclose abc|{message.from_user.id}"),
                ]
            ]
        )
        await edit_or_reply(message, text=final_output, reply_markup=keyboard, parse_mode=ParseMode.HTML)


# ==========================================
# 🧹 BUTTON HANDLERS
# ==========================================
@app.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(f"⚡ Executed in: {runtime}", show_alert=True)

@app.on_callback_query(filters.regex("forceclose"))
async def forceclose_command(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(f"🖕 Teri aukaat nahi hai isko close karne ki!", show_alert=True)
        except:
            return
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except:
        return


# ==========================================
# 🚀 ANU SUPREME LINUX SHELL (/sh) ☠️
# ==========================================
# 🔥 FIX: Only Owner Access via config.OWNER_ID
@app.on_edited_message(filters.command("sh") & filters.user(config.OWNER_ID) & ~filters.forwarded & ~filters.via_bot)
@app.on_message(filters.command("sh") & filters.user(config.OWNER_ID) & ~filters.forwarded & ~filters.via_bot)
async def shellrunner(_, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text=f"{E_DEVIL} <b>Abe! Command de terminal ke liye!</b>\n<i>Example:</i> <code>/sh git pull</code>", parse_mode=ParseMode.HTML)
        
    text = message.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
            except Exception as err:
                await edit_or_reply(message, text=f"{E_CROSS} <b>Anu System Error:</b>\n<pre>{err}</pre>", parse_mode=ParseMode.HTML)
            output += f"<b>{code}</b>\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(etype=exc_type, value=exc_obj, tb=exc_tb)
            return await edit_or_reply(message, text=f"{E_CROSS} <b>Anu System Error:</b>\n<pre>{''.join(errors)}</pre>", parse_mode=ParseMode.HTML)
            
        output = process.stdout.read()[:-1].decode("utf-8")
        
    if str(output) == "\n":
        output = None
        
    if output:
        if len(output) > 4096:
            with open("Anu_Terminal.txt", "w+") as file:
                file.write(output)
            await app.send_document(
                message.chat.id,
                "Anu_Terminal.txt",
                reply_to_message_id=message.id,
                caption=f"{E_CROWN} <b>Anu Terminal Output</b>",
            )
            return os.remove("Anu_Terminal.txt")
            
        # 💎 PREMIUM UI for Shell
        shell_msg = f"{E_DIAMOND} <b>『 𝗔 𝗡 𝗨  𝗧 𝗘 𝗥 𝗠 𝗜 𝗡 𝗔 𝗟 』</b> {E_DIAMOND}\n━━━━━━━━━━━━━━━━━━━━\n{E_MAGIC} <b>𝗢𝘂𝘁𝗽𝘂𝘁 :</b>\n<pre>{output}</pre>"
        await edit_or_reply(message, text=shell_msg, parse_mode=ParseMode.HTML)
    else:
        await edit_or_reply(message, text=f"{E_TICK} <b>Anu Terminal:</b>\n<code>Command Executed Successfully. No output returned.</code>", parse_mode=ParseMode.HTML)
        
    await message.stop_propagation()

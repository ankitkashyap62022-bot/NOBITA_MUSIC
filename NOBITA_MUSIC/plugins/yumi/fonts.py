from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram.errors import MessageNotModified

from NOBITA_MUSIC.utils.NOBITA_font import Fonts
from NOBITA_MUSIC import app

# ==========================================
# ☠️ ANU MATRIX PREMIUM FONT GENERATOR ☠️
# ==========================================

# ☠️ Smart Dictionary Mapping (Removed the 40-line if-else garbage) ☠️
STYLE_MAP = {
    "typewriter": Fonts.typewriter, "outline": Fonts.outline, "serif": Fonts.serief,
    "bold_cool": Fonts.bold_cool, "cool": Fonts.cool, "small_cap": Fonts.smallcap,
    "script": Fonts.script, "script_bolt": Fonts.bold_script, "tiny": Fonts.tiny,
    "comic": Fonts.comic, "sans": Fonts.san, "slant_sans": Fonts.slant_san,
    "slant": Fonts.slant, "sim": Fonts.sim, "circles": Fonts.circles,
    "circle_dark": Fonts.dark_circle, "gothic": Fonts.gothic, "gothic_bolt": Fonts.bold_gothic,
    "cloud": Fonts.cloud, "happy": Fonts.happy, "sad": Fonts.sad, "special": Fonts.special,
    "squares": Fonts.square, "squares_bold": Fonts.dark_square, "andalucia": Fonts.andalucia,
    "manga": Fonts.manga, "stinky": Fonts.stinky, "bubbles": Fonts.bubbles,
    "underline": Fonts.underline, "ladybug": Fonts.ladybug, "rays": Fonts.rays,
    "birds": Fonts.birds, "slash": Fonts.slash, "stop": Fonts.stop,
    "skyline": Fonts.skyline, "arrows": Fonts.arrows, "qvnes": Fonts.rvnes,
    "strike": Fonts.strike, "frozen": Fonts.frozen
}

def get_font_buttons(page=1):
    if page == 1:
        return [
            [InlineKeyboardButton("𝚃𝚢𝚙𝚎𝚠𝚛𝚒𝚝𝚎𝚛", callback_data="style+typewriter"), InlineKeyboardButton("𝕆𝕦𝕥𝕝𝕚𝕟𝕖", callback_data="style+outline"), InlineKeyboardButton("𝐒𝐞𝐫𝐢𝐟", callback_data="style+serif")],
            [InlineKeyboardButton("𝑺𝒆𝒓𝒊𝒇", callback_data="style+bold_cool"), InlineKeyboardButton("𝑆𝑒𝑟𝑖𝑓", callback_data="style+cool"), InlineKeyboardButton("Sᴍᴀʟʟ Cᴀᴘs", callback_data="style+small_cap")],
            [InlineKeyboardButton("𝓈𝒸𝓇𝒾𝓅𝓉", callback_data="style+script"), InlineKeyboardButton("𝓼𝓬𝓻𝓲𝓹𝓽", callback_data="style+script_bolt"), InlineKeyboardButton("ᵗⁱⁿʸ", callback_data="style+tiny")],
            [InlineKeyboardButton("ᑕOᗰIᑕ", callback_data="style+comic"), InlineKeyboardButton("𝗦𝗮𝗻𝘀", callback_data="style+sans"), InlineKeyboardButton("𝙎𝙖𝙣𝙨", callback_data="style+slant_sans")],
            [InlineKeyboardButton("𝘚𝘢𝘯𝘴", callback_data="style+slant"), InlineKeyboardButton("𝖲𝖺𝗇𝗌", callback_data="style+sim"), InlineKeyboardButton("Ⓒ︎Ⓘ︎Ⓡ︎Ⓒ︎Ⓛ︎Ⓔ︎Ⓢ︎", callback_data="style+circles")],
            [InlineKeyboardButton("🅒︎🅘︎🅡︎🅒︎🅛︎🅔︎🅢︎", callback_data="style+circle_dark"), InlineKeyboardButton("𝔊𝔬𝔱𝔥𝔦𝔠", callback_data="style+gothic"), InlineKeyboardButton("𝕲𝖔𝖙𝖍𝖎𝖈", callback_data="style+gothic_bolt")],
            [InlineKeyboardButton("C͜͡l͜͡o͜͡u͜͡d͜͡s͜͡", callback_data="style+cloud"), InlineKeyboardButton("H̆̈ă̈p̆̈p̆̈y̆̈", callback_data="style+happy"), InlineKeyboardButton("S̑̈ȃ̈d̑̈", callback_data="style+sad")],
            [InlineKeyboardButton("❌ Cʟᴏsᴇ", callback_data="close"), InlineKeyboardButton("Nᴇxᴛ ➻", callback_data="font_page+2")]
        ]
    elif page == 2:
        return [
            [InlineKeyboardButton("🇸 🇵 🇪 🇨 🇮 🇦 🇱 ", callback_data="style+special"), InlineKeyboardButton("🅂🅀🅄🄰🅁🄴🅂", callback_data="style+squares"), InlineKeyboardButton("🆂︎🆀︎🆄︎🅰︎🆁︎🅴︎🆂︎", callback_data="style+squares_bold")],
            [InlineKeyboardButton("ꪖꪀᦔꪖꪶꪊᥴ𝓲ꪖ", callback_data="style+andalucia"), InlineKeyboardButton("爪卂几ᘜ卂", callback_data="style+manga"), InlineKeyboardButton("S̾t̾i̾n̾k̾y̾", callback_data="style+stinky")],
            [InlineKeyboardButton("B̥ͦu̥ͦb̥ͦb̥ͦl̥ͦe̥ͦs̥ͦ", callback_data="style+bubbles"), InlineKeyboardButton("U͟n͟d͟e͟r͟l͟i͟n͟e͟", callback_data="style+underline"), InlineKeyboardButton("꒒ꍏꀷꌩꌃꀎꁅ", callback_data="style+ladybug")],
            [InlineKeyboardButton("R҉a҉y҉s҉", callback_data="style+rays"), InlineKeyboardButton("B҈i҈r҈d҈s҈", callback_data="style+birds"), InlineKeyboardButton("S̸l̸a̸s̸h̸", callback_data="style+slash")],
            [InlineKeyboardButton("s⃠t⃠o⃠p⃠", callback_data="style+stop"), InlineKeyboardButton("S̺͆k̺͆y̺͆l̺͆i̺͆n̺͆e̺͆", callback_data="style+skyline"), InlineKeyboardButton("A͎r͎r͎o͎w͎s͎", callback_data="style+arrows")],
            [InlineKeyboardButton("ዪሀክቿነ", callback_data="style+qvnes"), InlineKeyboardButton("S̶t̶r̶i̶k̶e̶", callback_data="style+strike"), InlineKeyboardButton("F༙r༙o༙z༙e༙n༙", callback_data="style+frozen")],
            [InlineKeyboardButton("❌ Cʟᴏsᴇ", callback_data="close"), InlineKeyboardButton("➻ Bᴀᴄᴋ", callback_data="font_page+1")]
        ]

@app.on_message(filters.command(["font", "fonts"]))
async def premium_style_buttons(client, message: Message):
    # ☠️ CRASH PROTECTOR: Safe Text Extraction ☠️
    if message.reply_to_message and message.reply_to_message.text:
        text = message.reply_to_message.text
    elif len(message.command) > 1:
        text = message.text.split(None, 1)[1]
    else:
        return await message.reply_text("<emoji id=4929369656797431200>🪐</emoji> **Usᴀɢᴇ:**\n`/font [Tᴇxᴛ]` ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴛᴇxᴛ ᴍᴇssᴀɢᴇ!")

    # 💎 PREMIUM UI WRAPPER 💎
    formatted_text = f"<emoji id=6123040393769521180>☄️</emoji> **Aɴᴜ Mᴀᴛʀɪx Fᴏɴᴛs**\n\n`{text}`"
    
    await message.reply_text(
        formatted_text, 
        reply_markup=InlineKeyboardMarkup(get_font_buttons(1)), 
        quote=True
    )

@app.on_callback_query(filters.regex(r"^font_page\+"))
async def premium_font_pagination(client, query: CallbackQuery):
    page = int(query.data.split("+")[1])
    try:
        await query.message.edit_reply_markup(InlineKeyboardMarkup(get_font_buttons(page)))
    except MessageNotModified:
        pass
    await query.answer()

@app.on_callback_query(filters.regex(r"^style\+"))
async def premium_apply_style(client, query: CallbackQuery):
    style_name = query.data.split('+')[1]
    
    # ☠️ Smart Text Extraction from the Bot's own message ☠️
    # Original text is always stored inside the code block `text`
    try:
        original_text = query.message.text.split("`")[1]
    except IndexError:
        return await query.answer("❌ Eʀʀᴏʀ: ᴏʀɪɢɪɴᴀʟ ᴛᴇxᴛ ʟᴏsᴛ!", show_alert=True)

    cls = STYLE_MAP.get(style_name)
    if not cls:
        return await query.answer("❌ Fᴏɴᴛ ɴᴏᴛ ғᴏᴜɴᴅ!", show_alert=True)
        
    new_text = cls(original_text)
    formatted_text = f"<emoji id=6123040393769521180>☄️</emoji> **Aɴᴜ Mᴀᴛʀɪx Fᴏɴᴛs**\n\n`{new_text}`"
    
    try:
        await query.message.edit_text(formatted_text, reply_markup=query.message.reply_markup)
    except MessageNotModified:
        pass
    await query.answer(f"✨ Aᴘᴘʟɪᴇᴅ: {style_name}")

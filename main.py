import asyncio
import os
import yt_dlp
import nest_asyncio
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from aiohttp import web

# === اطلاعات خودت رو اینجا وارد کن ===
BOT_TOKEN = "8847979483:AAE9JXU1K9zNOXgnR-RW8Xc709a38ppB5ZM"
CHANNEL_ID = -1003082074546   
ADMIN_ID = 7108254317         
# =================================

API_ID = 2040    
API_HASH = "b18441a1ff607e10a989891a5462e627" 

app = Client("LiveBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call = PyTgCalls(app)
is_playing = False

admin_keyboard = ReplyKeyboardMarkup([["توقف پخش 🔴", "وضعیت ربات 📊"]], resize_keyboard=True)

# سرور مجازی فیک برای روشن نگه داشتن ربات
async def handle(request):
    return web.Response(text="Bot is running!")

async def web_server():
    app_web = web.Application()
    app_web.router.add_get('/', handle)
    runner = web.AppRunner(app_web)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

@app.on_message(filters.command("start") & filters.user(ADMIN_ID))
async def start_cmd(client, message):
    await message.reply("لینک سایت رو بفرست.", reply_markup=admin_keyboard)

@app.on_message(filters.regex("توقف پخش 🔴") & filters.user(ADMIN_ID))
async def stop_stream(client, message):
    global is_playing
    if is_playing:
        await call.leave_call(CHANNEL_ID)
        is_playing = False
        await message.reply("🔴 پخش متوقف شد.")

@app.on_message(filters.text & filters.user(ADMIN_ID))
async def handle_links(client, message):
    global is_playing
    text = message.text
    if text.startswith("http"):
        msg = await message.reply("⏳ در حال تنظیم کیفیت روی 480p و استخراج...")
        try:
            # این بخش کیفیت را روی 480p یا کمتر قفل می‌کند تا سرور قطع نشود
            ydl_opts = {'format': 'best[height<=480]', 'quiet': True, 'noplaylist': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=False)
                direct_url = info['url']
            
            await msg.edit_text("✅ اتصال به کانال...")
            await call.play(CHANNEL_ID, MediaStream(direct_url))
            is_playing = True
            await msg.edit_text("🎥 پخش زنده با کیفیت 480p شروع شد!")
        except Exception as e:
            await msg.edit_text(f"❌ خطا: {e}")

async def main():
    await app.start()
    await call.start()
    await web_server()
    from pyrogram import idle
    await idle()

nest_asyncio.apply()
asyncio.run(main())

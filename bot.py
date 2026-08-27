import os
import time
import math
import asyncio
import subprocess
import re
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- Hugging Face Port 7860 සඳහා Flask Web Server එක ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Telegram Splitter Bot is running actively!"

def run_web():
    web_app.run(host="0.0.0.0", port=7860)

web_thread = Thread(target=run_web, daemon=True)
web_thread.start()
# --------------------------------------------------

# Telegram API දත්ත
API_ID = int(os.environ.get("API_ID", "123456"))
API_HASH = os.environ.get("API_HASH", "your_api_hash")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "your_bot_token")

app = Client(
    "splitter_bot", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    bot_token=BOT_TOKEN,
    workers=16
)

USER_FILES = {}
LAST_UPDATE_TIME = {}

def humanbytes(size):
    if not size:
        return "0 B"
    power = 2**10
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size >= power and n < 4:
        size /= power
        n += 1
    return f"{round(size, 2)} {power_labels[n]}B"

def time_formatter(seconds):
    if not seconds or seconds < 0:
        return "0s"
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

# Live Progress, Speed, ETA පෙන්වන ප්‍රධාන Function එක
async def progress_bar(current, total, message, action_text, start_time):
    chat_id = message.chat.id
    now = time.time()
    
    if chat_id not in LAST_UPDATE_TIME:
        LAST_UPDATE_TIME[chat_id] = 0

    # තත්පර 10කට වරක් හෝ ක්‍රියාවලිය 100% වූ විට පමණක් update කිරීම
    if now - LAST_UPDATE_TIME[chat_id] >= 10 or current >= total:
        LAST_UPDATE_TIME[chat_id] = now
        percentage = (current * 100) / total if total > 0 else 0
        if percentage > 100:
            percentage = 100
        
        elapsed = now - start_time
        speed = current / elapsed if elapsed > 0 else 0
        eta = (total - current) / speed if speed > 0 else 0
        
        filled = int(percentage // 10)
        progress_str = f"[{'█' * filled}{'░' * (10 - filled)}]"
        
        text = (
            f"⚡ **{action_text}**\n\n"
            f"{progress_str} **{percentage:.1f}%**\n\n"
            f"📁 **Done:** {humanbytes(current)} / {humanbytes(total)}\n"
            f"🚀 **Speed:** {humanbytes(speed)}/s\n"
            f"⏱️ **ETA:** {time_formatter(eta)}\n"
            f"⏳ **Elapsed:** {time_formatter(elapsed)}"
        )
        try:
            await message.edit_text(text)
        except Exception:
            pass

# Start Command Response
@app.on_message(filters.command("start"))
async def start_command(client, message):
    welcome_text = (
        "👋 **ආයුබෝවන්! File Splitter Bot වෙත සාදරයෙන් පිළිගනිමු.**\n\n"
        "ඔබට ඕනෑම විශාල ගොනුවක් (4GB දක්වා) Telegram හරහා මට එවිය හැක.\n"
        "මම එය **500MB** හෝ **1GB** කොටස් වලට කඩා (.zip format) ඔබට නැවත ලබා දෙන්නෙමි.\n\n"
        "🔹 **භාවිතා කරන ආකාරය:**\n"
        "ඔබට කඩා ගැනීමට අවශ්‍ය ගොනුව මෙතැනට එවා ලබා දෙන බටන් වලින් ප්‍රමාණය තෝරන්න."
    )
    await message.reply_text(welcome_text)

# ගොනුව ලැබුණු පසු Download කිරීම
@app.on_message(filters.document | filters.video | filters.audio)
async def handle_file(client, message):
    user_id = message.from_user.id
    status_msg = await message.reply_text("📥 **ගොනුව බාගත කිරීම ආරම්භ කරයි...**")
    
    os.makedirs("downloads", exist_ok=True)
    start_time = time.time()
    
    try:
        if message.document:
            original_name = message.document.file_name or "archive"
        elif message.video:
            original_name = message.video.file_name or "video.mp4"
        elif message.audio:
            original_name = message.audio.file_name or "audio.mp3"
        else:
            original_name = "archive"

        file_path = await message.download(
            file_name="downloads/",
            progress=progress_bar,
            progress_args=(status_msg, "Downloading File", start_time)
        )
        
        USER_FILES[user_id] = {
            "path": file_path,
            "name": original_name
        }
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✂️ 500MB Parts", callback_data="split_500m"),
                InlineKeyboardButton("✂️ 1GB Parts", callback_data="split_1g")
            ]
        ])
        
        await status_msg.edit_text(
            f"✅ **ගොනුව සාර්ථකව බාගත කරන ලදී!**\n📁 `{original_name}`\n\n"
            "මෙම ගොනුව කඩා (Split) බෙදා හැරිය යුතු ප්‍රමාණය (Size) පහත බොත්තම් වලින් තෝරන්න:",
            reply_markup=keyboard
        )
    except Exception as e:
        await status_msg.edit_text(f"❌ දෝෂයක් සිදු විය: `{str(e)}`")

# බටන් එක ක්ලික් කළ පසු Split කර Upload කිරීම
@app.on_callback_query(filters.regex("^split_"))
async def split_and_upload(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in USER_FILES:
        await callback_query.answer("ගොනුව හමුවී නැත. කරුණාකර නැවත File එක එවා උත්සාහ කරන්න.", show_alert=True)
        return

    data = callback_query.data
    size_arg = "500m" if "500m" in data else "1g"
    size_text = "500MB" if "500m" in data else "1GB"
    
    file_info = USER_FILES[user_id]
    file_path = file_info["path"]
    original_name = file_info["name"]
    
    status_msg = callback_query.message
    
    output_dir = f"downloads/split_{user_id}"
    os.makedirs(output_dir, exist_ok=True)
    
    total_file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 1
    
    try:
        # නම විශ්ලේෂණය කර Base නම සහ Input Part අංකය (උදා: .001 මඟින් Part01) ලබා ගැනීම
        match = re.search(r'(.+?)(?:\.zip)?\.(\d+)$', original_name, re.IGNORECASE)
        if match:
            clean_base = match.group(1).replace(".", "_")
            input_part = match.group(2).zfill(2)
        else:
            base_name, _ = os.path.splitext(original_name)
            if base_name.lower().endswith('.zip'):
                base_name = base_name[:-4]
            clean_base = base_name.replace(".", "_")
            input_part = "01"

        archive_name = os.path.join(output_dir, "archive.zip")
        
        # -tzip මඟින් .zip format එකෙන් සහ -mx0 මඟින් compression රහිතව වේගයෙන් split කරයි
        cmd = ["7z", "a", "-tzip", "-mx0", f"-v{size_arg}", archive_name, file_path]
        
        # Splitting Process එක Background එකේ ධාවනය කිරීම
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        split_start_time = time.time()
        
        # Splitting සිදුවන අතරතුර Output Folder එකේ ප්‍රමාණය මැන Live Progress පෙන්වීම
        while process.poll() is None:
            current_split_size = sum(
                os.path.getsize(os.path.join(output_dir, f)) 
                for f in os.listdir(output_dir) 
                if os.path.isfile(os.path.join(output_dir, f))
            )
            current_split_size = min(current_split_size, total_file_size)
            
            await progress_bar(
                current_split_size, 
                total_file_size, 
                status_msg, 
                f"Splitting File ({size_text} Parts)", 
                split_start_time
            )
            await asyncio.sleep(2)
            
        # Splitting අවසන් වූ පසු 100% ලෙස පෙන්වීම
        await progress_bar(
            total_file_size, 
            total_file_size, 
            status_msg, 
            f"Splitting File ({size_text} Parts)", 
            split_start_time
        )

        # 7-Zip මඟින් සාදන ලද කොටස් ලබාගෙන, ඉල්ලා ඇති පරිදි නම සකස් කිරීම (උදා: Palworld_[FitGirl_Repack]_Part01.zip.001)
        raw_parts = sorted([
            os.path.join(output_dir, f) 
            for f in os.listdir(output_dir) 
            if os.path.isfile(os.path.join(output_dir, f)) and f != os.path.basename(file_path)
        ])
        
        parts = []
        for index, old_path in enumerate(raw_parts, start=1):
            new_filename = f"{clean_base}_Part{input_part}.zip.{index:03d}"
            new_path = os.path.join(output_dir, new_filename)
            os.rename(old_path, new_path)
            parts.append(new_path)
        
        total_parts = len(parts)
        
        if total_parts == 0:
            await status_msg.edit_text("❌ ගොනුව කඩීමේදී කොටස් හමුවූයේ නැත.")
            return

        await status_msg.edit_text(f"📤 **කොටස් {total_parts} ක් හමු විය. දැන් අප්ලෝඩ් කිරීම ආරම්භ කරයි...**")
        
        # එකින් එක අප්ලෝඩ් කිරීම
        for index, part_file in enumerate(parts, start=1):
            part_status = await client.send_message(
                chat_id=user_id,
                text=f"📤 **Part {index}/{total_parts} අප්ලෝඩ් වීමට සූදානම් වේ...**"
            )
            
            upload_start_time = time.time()
            
            await client.send_document(
                chat_id=user_id,
                document=part_file,
                caption=f"📦 **Part {index} / {total_parts}**\n\n💡 Extract කිරීමට සියලුම කොටස් එකම ෆෝල්ඩර් එකකට දමා 7-Zip හෝ WinRAR භාවිත කරන්න.",
                progress=progress_bar,
                progress_args=(part_status, f"Uploading Part {index}/{total_parts}", upload_start_time)
            )
            
            try:
                await part_status.delete()
            except Exception:
                pass
                
        await status_msg.edit_text("✨ **සියලුම කොටස් සාර්ථකව අප්ලෝඩ් කර අවසන්!**")
        
    except Exception as e:
        await status_msg.edit_text(f"❌ ක්‍රියාවලියේ දෝෂයක් සිදු විය: `{str(e)}`")
        
    finally:
        # තාවකාලික ෆයිල් මකා දැමීම (Clean Up)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            import shutil
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            if user_id in USER_FILES:
                del USER_FILES[user_id]
        except Exception:
            pass

print("Bot and Web Server are running...")
app.run()

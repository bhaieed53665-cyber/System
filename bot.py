import os
import random
import discord
from discord.ext import commands

# ---------- الإعدادات (تُقرأ من متغيرات البيئة في Railway) ----------

# التوكن الخاص بالبوت (من Discord Developer Portal)
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

# أرقام (IDs) الشاتات (القنوات) اللي بدك البوت يرد فيها
# مثال في Railway: ALLOWED_CHANNEL_IDS=123456789012345678,987654321098765432
ALLOWED_CHANNEL_IDS = {
    int(cid.strip())
    for cid in os.environ.get("ALLOWED_CHANNEL_IDS", "").split(",")
    if cid.strip()
}

# مجلد الصور: حط كل ملفات الـ GIF يلي بدك البوت يبعتها جوا مجلد "gifs"
# بجانب هاد الملف (bot.py) مباشرة. البوت بيختار وحدة عشوائياً كل مرة.
GIFS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gifs")

# ---------------------------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True  # لازم تكون مفعّلة من Developer Portal كمان

bot = commands.Bot(command_prefix="!", intents=intents)


def get_random_gif_path() -> str | None:
    """يرجع مسار ملف GIF عشوائي من مجلد gifs، أو None لو المجلد فاضي."""
    if not os.path.isdir(GIFS_DIR):
        return None

    files = [
        f for f in os.listdir(GIFS_DIR)
        if f.lower().endswith((".gif", ".png", ".jpg", ".jpeg", ".webp"))
    ]
    if not files:
        return None

    chosen = random.choice(files)
    return os.path.join(GIFS_DIR, chosen)


@bot.event
async def on_ready():
    print(f"✅ البوت اشتغل باسم: {bot.user} (ID: {bot.user.id})")
    print(f"📺 الشاتات المسموحة: {ALLOWED_CHANNEL_IDS or 'كل الشاتات (ما تحدد شي)'}")
    gif_count = len(os.listdir(GIFS_DIR)) if os.path.isdir(GIFS_DIR) else 0
    print(f"🖼️ عدد ملفات الـ GIF الموجودة بمجلد gifs: {gif_count}")


@bot.event
async def on_message(message: discord.Message):
    # تجاهل رسايل البوت نفسه (منعاً للتكرار اللانهائي)
    if message.author.bot:
        return

    # إذا حددنا شاتات معينة، تأكد إنو الرسالة جاية من وحدة منهم
    if ALLOWED_CHANNEL_IDS and message.channel.id not in ALLOWED_CHANNEL_IDS:
        return

    gif_path = get_random_gif_path()

    if gif_path is None:
        print("⚠️ ما في ولا ملف GIF جوا مجلد gifs — تأكد إنك رفعته صح.")
    else:
        await message.channel.send(file=discord.File(gif_path))

    # هاد السطر ضروري لو بدك تستخدم أوامر (commands) كمان مستقبلاً
    await bot.process_commands(message)


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        raise SystemExit(
            "❌ لازم تحط DISCORD_TOKEN في متغيرات البيئة (Environment Variables)."
        )
    bot.run(DISCORD_TOKEN)

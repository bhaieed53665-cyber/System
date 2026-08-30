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
        f for f in

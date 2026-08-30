import io
import os
import random
import aiohttp
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

# روابط الـ GIF اللي بدك البوت يبعتها (ممكن تحط أكثر من واحد، بيختار عشوائي)
# مثال: GIF_URLS=https://example.com/1.gif,https://example.com/2.gif
GIF_URLS = [
    url.strip()
    for url in os.environ.get("GIF_URLS", "").split(",")
    if url.strip()
]

if not GIF_URLS:
    # صورة GIF افتراضية لو ما حطيت شي
    GIF_URLS = ["https://media.tenor.com/2roZ_D0EjhcAAAAC/hello-hi.gif"]

# ---------------------------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True  # لازم تكون مفعّلة من Developer Portal كمان

bot = commands.Bot(command_prefix="!", intents=intents)

# جلسة HTTP واحدة نعيد استخدامها لتنزيل الصور (أسرع وأنظف من فتح جلسة كل مرة)
http_session: aiohttp.ClientSession | None = None


async def fetch_gif_bytes(url: str) -> tuple[bytes, str] | None:
    """ينزّل الصورة من الرابط ويرجع البايتات مع اسم ملف مناسب."""
    global http_session
    if http_session is None:
        http_session = aiohttp.ClientSession()

    try:
        async with http_session.get(url) as resp:
            if resp.status != 200:
                return None
            data = await resp.read()
    except aiohttp.ClientError:
        return None

    filename = url.split("/")[-1].split("?")[0]
    if not filename or "." not in filename:
        filename = "image.gif"

    return data, filename


@bot.event
async def on_ready():
    print(f"✅ البوت اشتغل باسم: {bot.user} (ID: {bot.user.id})")
    print(f"📺 الشاتات المسموحة: {ALLOWED_CHANNEL_IDS or 'كل الشاتات (ما تحدد شي)'}")


@bot.event
async def on_message(message: discord.Message):
    # تجاهل رسايل البوت نفسه (منعاً للتكرار اللانهائي)
    if message.author.bot:
        return

    # إذا حددنا شاتات معينة، تأكد إنو الرسالة جاية من وحدة منهم
    if ALLOWED_CHANNEL_IDS and message.channel.id not in ALLOWED_CHANNEL_IDS:
        return

    gif_url = random.choice(GIF_URLS)
    result = await fetch_gif_bytes(gif_url)

    if result is None:
        # لو صار خطأ بالتنزيل، ابعت الرابط عادي كحل احتياطي
        await message.channel.send(gif_url)
    else:
        data, filename = result
        file = discord.File(io.BytesIO(data), filename=filename)
        await message.channel.send(file=file)

    # هاد السطر ضروري لو بدك تستخدم أوامر (commands) كمان مستقبلاً
    await bot.process_commands(message)


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        raise SystemExit(
            "❌ لازم تحط DISCORD_TOKEN في متغيرات البيئة (Environment Variables)."
        )
    bot.run(DISCORD_TOKEN)

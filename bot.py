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

    gif = random.choice(GIF_URLS)
    await message.channel.send(gif)

    # هاد السطر ضروري لو بدك تستخدم أوامر (commands) كمان مستقبلاً
    await bot.process_commands(message)


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        raise SystemExit(
            "❌ لازم تحط DISCORD_TOKEN في متغيرات البيئة (Environment Variables)."
        )
    bot.run(DISCORD_TOKEN)

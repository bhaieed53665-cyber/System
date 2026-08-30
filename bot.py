import os
import random
import discord
from discord.ext import commands

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

ALLOWED_CHANNEL_IDS = {int(cid.strip()) for cid in os.environ.get("ALLOWED_CHANNEL_IDS", "").split(",") if cid.strip()}

GIFS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gifs")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def get_random_gif_path():
    if not os.path.isdir(GIFS_DIR):
        return None
    files = [f for f in os.listdir(GIFS_DIR) if f.lower().endswith((".gif", ".png", ".jpg", ".jpeg", ".webp"))]
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
    if message.author.bot:
        return
    if ALLOWED_CHANNEL_IDS and message.channel.id not in ALLOWED_CHANNEL_IDS:
        return
    gif_path = get_random_gif_path()
    if gif_path is None:
        print("⚠️ ما في ولا ملف GIF جوا مجلد gifs — تأكد إنك رفعته صح.")
    else:
        await message.channel.send(file=discord.File(gif_path))
    await bot.process_commands(message)


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if payload.user_id == bot.user.id:
        return
    if ALLOWED_CHANNEL_IDS and payload.channel_id not in ALLOWED_CHANNEL_IDS:
        return

    channel = bot.get_channel(payload.channel_id)
    if channel is None:
        try:
            channel = await bot.fetch_channel(payload.channel_id)
        except discord.HTTPException:
            return

    try:
        message = await channel.fetch_message(payload.message_id)
    except discord.HTTPException:
        return

    if message.author.id != bot.user.id:
        return

    member = payload.member
    if member is None and channel.guild is not None:
        try:
            member = await channel.guild.fetch_member(payload.user_id)
        except discord.HTTPException:
            member = None

    if member is not None and member.bot:
        try:
            await message.remove_reaction(payload.emoji, member)
            print(f"🧹 مسحت ريأكشن حطه البوت {member} عن رسالة بعتها بوتنا.")
        except discord.Forbidden:
            print("❌ ما عندي صلاحية Manage Messages لمسح الريأكشن.")
        except discord.HTTPException:
            pass


if __name__ == "__main__":
    if not DISCORD_TOKEN:
        raise SystemExit("❌ لازم تحط DISCORD_TOKEN في متغيرات البيئة (Environment Variables).")
    bot.run(DISCORD_TOKEN)

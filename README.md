# بوت Discord لإرسال GIF

بوت بسيط: كل ما حدا يبعت رسالة بشات محدد، البوت بيرد بصورة GIF.

## 1) إنشاء البوت على Discord

1. روح على https://discord.com/developers/applications واعمل **New Application**.
2. من تبويب **Bot** اعمل **Add Bot**.
3. فعّل خيار **MESSAGE CONTENT INTENT** (موجود بنفس الصفحة تحت Privileged Gateway Intents) — ضروري جداً وإلا البوت ما رح يشوف الرسائل.
4. انسخ الـ **Token** (رح تحتاجه بعدين).
5. من تبويب **OAuth2 > URL Generator**: اختار scope `bot`، وصلاحيات `Read Messages/View Channels` و `Send Messages`. افتح الرابط اللي بيتولد وضيف البوت عالسيرفر تبعك.

## 2) معرفة أرقام (IDs) الشاتات

1. من إعدادات Discord فعّل **وضع المطور** (Settings > Advanced > Developer Mode).
2. دوس كليك يمين على أي شات (Channel) واختار **Copy Channel ID**.
3. اجمع كل الأرقام اللي بدك البوت يشتغل فيها.

## 3) التجربة محلياً (اختياري)

```bash
pip install -r requirements.txt
cp .env.example .env
# عدّل ملف .env وحط التوكن والقيم الصح
```

على جهازك، حمّل مكتبة `python-dotenv` لو بدك تقرأ ملف `.env` مباشرة، أو ببساطة صدّر المتغيرات بالتيرمينال قبل التشغيل:

```bash
export DISCORD_TOKEN="التوكن"
export ALLOWED_CHANNEL_IDS="123456789012345678"
export GIF_URLS="https://example.com/1.gif"
python bot.py
```

## 4) الرفع على Railway

1. اعمل حساب على https://railway.app وسجل دخول.
2. اضغط **New Project > Deploy from GitHub repo** (ارفع هاد المجلد على GitHub أولاً)، أو استخدم **Railway CLI** لرفع المجلد مباشرة بدون GitHub.
3. من تبويب **Variables** بالمشروع على Railway، ضيف:
   - `DISCORD_TOKEN` = التوكن تبع البوت
   - `ALLOWED_CHANNEL_IDS` = أرقام الشاتات مفصولة بفاصلة
   - `GIF_URLS` = رابط أو أكثر لصور GIF مفصولين بفاصلة
4. Railway رح يقرأ ملف `Procfile` تلقائياً ويشغل البوت كـ **Worker** (مش Web Service، لأنو ما في سيرفر HTTP هون).
5. تأكد إنو نوع الخدمة (Service Type) مضبوط على Worker مش Web، وإلا Railway ممكن يوقف الخدمة لعدم وجود بورت مفتوح.

## ملاحظات

- إذا سبت `ALLOWED_CHANNEL_IDS` فاضي، البوت رح يرد بكل الشاتات.
- إذا حطيت أكثر من رابط GIF بـ `GIF_URLS`، البوت رح يختار وحدة عشوائياً في كل مرة.
- البوت بيتجاهل رسايل البوتات الثانية (وبضمنها حاله) عشان ما يصير تكرار لانهائي.

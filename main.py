import discord
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os
import random
from keep_alive import keep_alive  # ✅ استدعاء الدالة

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def fetch_image_urls():
    url = "https://pfps.gg/pfps/discord"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            images = soup.find_all("img", class_="img-fluid")
            img_urls = [img['src'] for img in images if 'src' in img.attrs]
            return img_urls

async def send_random_images():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"❌ لم أتمكن من إيجاد القناة بالمعرف {CHANNEL_ID}")
        return
    while not client.is_closed():
        img_urls = await fetch_image_urls()
        if img_urls:
            for _ in range(10):  # ✅ إرسال 10 صور كل مرة
                image_url = random.choice(img_urls)
                await channel.send(image_url)
        else:
            await channel.send("لم أتمكن من جلب الصور الآن.")
        await asyncio.sleep(300)  # ✅ كل 5 دقائق (300 ثانية)

@client.event
async def on_ready():
    print(f"✅ تم تسجيل الدخول كبوت: {client.user}")
    client.loop.create_task(send_random_images())

# ✅ إبقاء السيرفر مستمر
keep_alive()

# ✅ تشغيل البوت
client.run(TOKEN)

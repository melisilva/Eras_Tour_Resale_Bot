import requests
from bs4 import BeautifulSoup
import discord
from apscheduler.schedulers.background import BackgroundScheduler
import os

# Discord bot token
TOKEN = os.getenv("DISCORD_TOKEN")

# Discord client
client = discord.Client(intents=discord.Intents.all())

URL = "https://taylorswift.seetickets.com/resell/search"
prev_length = 0  # Store the previous value of len(taylor_results)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

async def check_website():
    global prev_length

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "lxml")
    taylor_results = soup.find_all("ul")
    current_length = len(taylor_results)
    channel_id = os.getenv("YOUR_CHANNEL_ID")
    channel = client.get_channel(int(channel_id))  # Convert to int and get the channel

    if current_length > prev_length:
        prev_length = current_length
        await channel.send(f"Warning: Number of results increased to {current_length}")
    else:
        await channel.send("Bot is working, but no new items found.")

@client.event
async def on_message(message):
    if message.content == '!check':
        await check_website()

# Schedule the website check every hour
scheduler = BackgroundScheduler()
scheduler.add_job(check_website, 'interval', hours=1)
scheduler.start()

client.run(TOKEN)

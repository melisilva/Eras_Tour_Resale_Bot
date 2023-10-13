import requests
from bs4 import BeautifulSoup
import discord
from aiocron import crontab
import asyncio

DISCORD_TOKEN= ""
YOUR_CHANNEL_ID= ""

# Discord bot token
TOKEN = DISCORD_TOKEN

# Discord client
client = discord.Client(intents=discord.Intents.all())

URL = "https://taylorswift.seetickets.com/resell/search"
prev_length = 0  # Store the previous value of len(taylor_results)


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

async def check_website(message = None):
    global prev_length
    print("holo 3")

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "lxml")
    taylor_results = soup.find_all("ul")
    current_length = len(taylor_results)
    channel_id = YOUR_CHANNEL_ID
    channel = client.get_channel(int(channel_id))  # Convert to int and get the channel

    if current_length > prev_length:
        await channel.send(f"@everyone Warning: Number of results increased to {current_length}")
    else:
        if message is not None:
            await channel.send("No new items, sorry :(")

    prev_length = current_length

@client.event
async def on_message(message):
    channel_id = YOUR_CHANNEL_ID
    channel = client.get_channel(int(channel_id))  # Convert to int and get the channel
    if message.content == '!alive':
        await channel.send("I'm alive. There's just no new items.")
    elif message.content == '!check':
        await check_website(message.content)

if __name__ == "__main__":
    print("holo")

    cron = crontab("*/10 * * * *")  # Schedule to run every 10 minutes
    cron(check_website)

    loop = asyncio.get_event_loop()
    loop.create_task(client.start(TOKEN))
    loop.run_forever()

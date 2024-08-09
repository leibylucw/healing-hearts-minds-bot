import os

import discord
import dotenv
import requests

DAD_JOKE_HEADERS = {'Accept': 'text/plain'}

dotenv.load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == '$dadjoke':
        await message.channel.send(requests.get('https://icanhazdadjoke.com/', headers=DAD_JOKE_HEADERS).text)

client.run(token)

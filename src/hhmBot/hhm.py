import os

import discord
import dotenv
import requests
from discord import app_commands

dotenv.load_dotenv()

HHM_GUILD = discord.Object(id=os.getenv('GUILD_ID'))

intents = discord.Intents.default()
intents.message_content = True


class HHMBotClient(discord.Client):
	def __init__(self, *, intents):
		super().__init__(intents=intents)
		self.tree = app_commands.CommandTree(self)

	async def setup_hook(self):
		self.tree.copy_global_to(guild=HHM_GUILD)
		await self.tree.sync(guild=HHM_GUILD)


client = HHMBotClient(intents=intents)


@client.event
async def on_ready():
	print(f'Logged in as {client.user} (ID: {client.user.id})')


@client.tree.command(name='dadjoke', description='Get a funny dad joke!')
async def dadJoke(interaction):
	await interaction.response.send_message(
		requests.get('https://icanhazdadjoke.com', headers={'Accept': 'text/plain'}).text, ephemeral=True
	)


client.run(os.getenv('DISCORD_TOKEN'))

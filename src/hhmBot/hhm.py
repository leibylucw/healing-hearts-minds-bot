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
	try:
		response = requests.get('https://icanhazdadjoke.com', headers={'Accept': 'text/plain'})
		response.raise_for_status()
		joke = response.content.decode('utf-8')
	except requests.RequestException as e:
		joke = 'Failed to fetch a dad joke due to an error.'
		print(f'Error fetching dad joke: {e}')

	await interaction.response.send_message(joke, ephemeral=True)


@client.tree.context_menu(name='Report to HHM Mods')
async def reportToHHMMods(interaction: discord.Interaction, message: discord.Message):
	await interaction.response.send_message(
		f'Thanks for reporting this message by {message.author.mention} to HHM mods. Someone will reach out to you shortly. Note that this message has been reported to HHM mods, not Discord itself. If you feel the offensive nature of the message is severe, please also report the message to Discord as well as HHM mods.',
		ephemeral=True,
	)

	logChannel = interaction.guild.get_channel(1273000106253226146)

	embed = discord.Embed(title=f'{interaction.user.display_name} Reported a Message')
	if message.content:
		embed.description = message.content

	embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
	embed.timestamp = message.created_at

	urlView = discord.ui.View()
	urlView.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))

	await logChannel.send(embed=embed, view=urlView)


client.run(os.getenv('DISCORD_TOKEN'))

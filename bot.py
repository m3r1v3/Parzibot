import os

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

client = commands.Bot(command_prefix='$', intents=intents)
client.remove_command("help")


@client.command()
async def load(extension):
    """Load cogs"""
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(extension):
    """Unload cogs"""
    client.unload_extension(f'cogs.{extension}')


# Load files
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# Get token from server and set bot token
token = os.environ.get('BOT_TOKEN')

# Run bot
client.run(str(token))


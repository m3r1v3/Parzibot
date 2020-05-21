# bot.py
# Recycled 05/17/20
import os

from discord.ext import commands
from cogs.language import get_lang

client = commands.Bot(command_prefix='!')


@client.command()
async def load(extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(extension):
    client.unload_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if get_lang() == "RU":
            await ctx.send('Команда не распознана.')
        else:
            await ctx.send('Command not recognized.')


token = os.environ.get('BOT_TOKEN')
client.run(str(token))

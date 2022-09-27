import os
import asyncio


import discord
from discord import app_commands
from discord.ext import commands


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix='$', intents = discord.Intents.all())
        self.cogs_extensions = [f'cogs.{filename[:-3]}' for filename in os.listdir('src/cogs') if filename.endswith('.py')]

    async def setup_hook(self):
        for ext in self.cogs_extensions:
            await self.load_extension(ext)
        await bot.tree.sync()

    def music_disable(bot: commands.Bot):
        if int(os.environ.get('MUSIC_COMMANDS')):
            bot.remove_command(name="musichelp")
            bot.remove_command(name="connect")
            bot.remove_command(name="disconnect")
            bot.remove_command(name="play")
            bot.remove_command(name="replay")
            bot.remove_command(name="pause")
            bot.remove_command(name="resume")
            bot.remove_command(name="repeat")
            bot.remove_command(name="next")
            bot.remove_command(name="playlist")
            bot.remove_command(name="playlistadd")
            bot.remove_command(name="playlistclear")
            bot.remove_command(name="playlistshuffle")

bot = Bot()
bot.run(str(os.environ.get('BOT_TOKEN')))
bot.music_disable() # Delete if doesn't need disable music commands

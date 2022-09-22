import os
import asyncio


import discord
from discord import app_commands
from discord.ext import commands

class Bot(commands.Bot):

    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True
        intents.voice_states = True

        super().__init__(
            command_prefix='$',
            intents = intents            
            )

        self.cogs_extensions = [f'cogs.{filename[:-3]}' for filename in os.listdir('src/cogs') if filename.endswith('.py')]

    async def setup_hook(self):
        for ext in self.cogs_extensions:
            await self.load_extension(ext)
        await bot.tree.sync()

bot = Bot()
bot.run(str(os.environ.get('BOT_TOKEN')))

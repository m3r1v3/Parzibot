import discord
from discord import app_commands, Embed, Colour
from discord.ext import commands

from message import Message

class ErrorHandler(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await Message.error_msg(ctx, "Parzibot // Error", "Something went wrong! Try again")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ErrorHandler(bot))

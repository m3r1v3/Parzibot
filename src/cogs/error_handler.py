import json

from discord.ext import commands

from message import Message


class ErrorHandler(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await Message.error_msg(ctx, Message.get_error_msg("titles", "error"), Message.get_error_msg("messages", "error"))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ErrorHandler(bot))

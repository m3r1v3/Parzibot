import datetime
import os

import discord
from discord import app_commands
from discord.ext import commands

from message import Message


class BasicCommands(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="about", description=Message.get_basic_msg("descriptions", "about"))
    async def about(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        await Message.basic_msg(ctx, Message.get_basic_msg("titles", "about"), Message.get_basic_msg("messages", "about").format(year=datetime.datetime.now().year))

    @app_commands.command(name="clear", description=Message.get_basic_msg("descriptions", "clear"))
    @app_commands.describe(number=Message.get_basic_msg("descriptions", "clear-number"))
    async def clear(self, interaction: discord.Interaction, number: int = 5):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if number:
            count = len([message async for message in ctx.channel.history(limit=32)])
            if number < count:
                await interaction.channel.purge(limit=number)
                await Message.basic_msg(ctx, Message.get_basic_msg("titles", "clear"), Message.get_basic_msg("messages", "clear").format(number=number))
            else:
                await interaction.channel.purge(limit=count)
                await Message.basic_msg(ctx, Message.get_basic_msg("titles", "clear"), Message.get_basic_msg("messages", "clear").format(number=count))
        else:
            await Message.error_msg(ctx, Message.get_error_msg("titles", "error"), Message.get_error_msg("messages", "error-clear").format(number=number))

    @app_commands.command(name="help", description=Message.get_basic_msg("descriptions", "help"))
    async def help(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        await Message.basic_msg(ctx, Message.get_basic_msg("titles", "help"), Message.get_basic_msg("messages", "help"))

    @app_commands.command(name="ping", description=Message.get_basic_msg("descriptions", "ping"))
    async def ping(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        await Message.basic_msg(ctx, Message.get_basic_msg("titles", "ping"), Message.get_basic_msg("messages", "ping").format(latency=round(self.bot.latency * 1000)))

    @app_commands.command(name="members", description=Message.get_basic_msg("descriptions", "members"))
    async def members(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        await Message.basic_msg(ctx, Message.get_basic_msg("titles", "members"), "".join(f"• **{member}** ({member.status})\n" for member in interaction.channel.members))


async def setup(bot: commands.Bot) -> None:
    if int(os.environ.get('BASIC_COMMANDS')): await bot.add_cog(BasicCommands(bot))

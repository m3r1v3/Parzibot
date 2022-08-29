import datetime
import random

import discord
from discord import app_commands, Embed, Colour
from discord.ext import commands

from message import Message


class BasicCommands(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="about", description="Information about Parzibot")
    async def about(self, interaction: discord.Interaction):
        await Message.basic_msg(await self.bot.get_context(interaction), "Parzibot // About", (
            f"**Parzibot** is free open-source project, created by **merive_**\n"
            f"You can find more information on [Parzibot Website](https://merive.herokuapp.com/Parzibot)\n"
            f"**Parzibot**, {datetime.datetime.now().year}"))

    @app_commands.command(name="clear", description="Clear messages in Text Channel")
    @app_commands.describe(number="Number of messages to be cleaned (Optional / Default 5)")
    async def clear(self, interaction: discord.Interaction, number: int = 5):
        if number:
            await interaction.channel.purge(limit=number)
            await Message.basic_msg(await self.bot.get_context(interaction), "Parzibot // Clear", f"Cleared **{number}** messages")
        else: await Message.error_msg(await self.bot.get_context(interaction), "Parzibot // Error", f"Cannot clear **{number}** messages")

    @app_commands.command(name="help", description="List of Parzibot basic commands")
    async def help(self, interaction: discord.Interaction):
        await Message.basic_msg(await self.bot.get_context(interaction), "Parzibot // Basic Commands", (
            " • **/about** - Information about Parzibot\n"
            " • **/clear** `number` - Clear messages in current Text Channel\n"
            " • **/help** - The list of Parzibot basic commands\n"
            " • **/members** - Members of current Text Channel\n"
            " • **/ping** - Parzibot ping"))
        
    @app_commands.command(name="ping", description="Parzibot ping")
    async def ping(self, interaction: discord.Interaction):
        await Message.basic_msg(await self.bot.get_context(interaction), "Parzibot // Ping", f"Ping is `{round(self.bot.latency * 1000)}ms`")

    @app_commands.command(name="members", description="Members of current Text Channel")
    async def members(self, interaction: discord.Interaction):
        await Message.basic_msg(await self.bot.get_context(interaction), "Parzibot // Channel Members", "".join(f"\t**{member}**\n" for member in interaction.channel.members))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BasicCommands(bot))

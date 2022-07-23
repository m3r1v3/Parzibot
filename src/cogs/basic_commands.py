import datetime
import random
import discord

from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

from message import Message


class BasicCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="about", description="Information About Parzibot")
    async def about(self, ctx):
        """Information About Parzibot"""
        await Message.msg(ctx, "About Parzibot", (
            f"**Parzibot** is free open-source project, created by **merive_**\n"
            f"You can find more information on [Parzibot Website](https://merive.herokuapp.com/Parzibot)\n"
            f"**Parzibot**, {datetime.datetime.now().year}"
            ))

    @cog_ext.cog_slash(
        name="clear",
        description="Clear Messages in Current Text Channel",
        options=[
            create_option(
                name="number",
                description="Number of Messages for Clear",
                option_type=4,
                required=False)
            ])
    async def clear(self, ctx, number=5):
        """Clear Messages in Current Text Channel"""
        if number > 0:
            await ctx.channel.purge(limit=number)
            await Message.msg(ctx, "Messages has been cleared", f"Cleared **{number}** messages")
        else: await Message.error(ctx, "Clear error", f"Cannot clear **{number}** messages")


    @cog_ext.cog_slash(name="help", description="The List of Parzibot Commands")
    async def help(self, ctx):
        """The List of Parzibot Commands"""
        await Message.msg(ctx, "Bot Commands", (
            " • **/about** - Information About Parzibot\n"
            " • **/clear** `number` - Clear Messages in Current Text Channel\n"
            " • **/help** - The list of Parzibot commands\n"
            " • **/ping** - Parzibot ping\n"
            " • **/users** - List of Text Channel members\n"))
        

    @cog_ext.cog_slash(name="ping", description="Parzibot's Ping")
    async def ping(self, ctx):
        """Parzibot"s Ping"""
        await Message.msg(ctx, "Parzibot Ping", f"**Parzibot** Ping: `{round(self.client.latency * 1000)}ms`")

    @cog_ext.cog_slash(name="users", description="List of Text Channel members")
    async def users(self, ctx):
        """The List of Text Channel Members"""
        await Message.msg(ctx, "Channel Members", "".join(f"\t**{member}**\n" for member in ctx.channel.members))


def setup(client):
    """Setup function"""
    client.add_cog(BasicCommands(client))

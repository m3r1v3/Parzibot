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

    @cog_ext.cog_slash(name="about", description="Information about Parzibot")
    async def about(self, ctx):
        await Message.msg(ctx, "About Parzibot", (
            f"**Parzibot** is free open-source project, created by **merive_**\n"
            f"You can find more information on [Parzibot Website](https://merive.herokuapp.com/Parzibot)\n"
            f"**Parzibot**, {datetime.datetime.now().year}"))

    @cog_ext.cog_slash(
        name="clear",
        description="Clear messages in current Text Channel",
        options=[
            create_option(
                name="number",
                description="Number of messages to be cleaned (Optional / Default 5)",
                option_type=4,
                required=False)
            ])
    async def clear(self, ctx, number=5):
        if number > 0:
            await ctx.channel.purge(limit=number)
            await Message.msg(ctx, "Messages has been cleared", f"Cleared **{number}** messages")
        else: await Message.error(ctx, "Clear error", f"Cannot clear **{number}** messages")

    @cog_ext.cog_slash(name="help", description="The list of Parzibot basic commands")
    async def help(self, ctx):
        await Message.msg(ctx, "Parzibot // Basic Commands", (
            " • **/about** - Information about Parzibot\n"
            " • **/clear** `number` - Clear messages in current Text Channel\n"
            " • **/help** - The list of Parzibot basic commands\n"
            " • **/ping** - Parzibot ping\n"
            " • **/users** - The list of current Text Channel members"))
        
    @cog_ext.cog_slash(name="ping", description="Parzibot ping")
    async def ping(self, ctx):
        await Message.msg(ctx, "Parzibot Ping", f"**Parzibot** Ping: `{round(self.client.latency * 1000)}ms`")

    @cog_ext.cog_slash(name="users", description="The list of current Text Channel members")
    async def users(self, ctx):
        await Message.msg(ctx, "Channel Members", "".join(f"\t**{member}**\n" for member in ctx.channel.members))


def setup(client):
    client.add_cog(BasicCommands(client))

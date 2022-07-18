import datetime
import random
import discord

from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

from message import Message


class Commands(commands.Cog):

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


    @cog_ext.cog_slash(
        name="help",
        description="The List of Parzibot Commands",
        options=[
            create_option(
                name="command",
                description="The Help Message for Specific Command",
                option_type=3,
                required=False,
                choices=[
                    create_choice(name="about", value="about"),
                    create_choice(name="clear", value="clear"),
                    create_choice(name="help", value="help"),
                    create_choice(name="ping", value="ping"),
                    create_choice(name="users", value="users")
                ])
            ])
    async def help(self, ctx, command=None):
        """The List of Parzibot Commands"""
        if command is None:
            await Message.msg(ctx, "Bot Commands", (
                " • **/about** - Information About Parzibot\n"
                " • **/clear** `number` - Clear Messages in Current Text Channel\n"
                " • **/help** `command` - The list of Parzibot commands\n"
                " • **/ping** - Parzibot ping\n"
                " • **/users** - List of Text Channel members\n"))
        elif command == "about":
            await Message.msg(ctx, "**/about** command - Information About Parzibot", "**Syntax:** **/about**")
        elif command == "clear":
            await Message.msg(ctx, "**/clear** command - Clear Messages in Current Text Channel", (
                "**Syntax:** **/clear** `number`\n"
                "**Options:** `number` - Number of Messages for Clear **(Optional)**"))
        elif command == "help":
            await Message.msg(ctx, "**/help** command - The List of Parzibot Commands", (
                "**Syntax:** **/help** `command`\n"
                "**Options:** `command` - The Help Message for Specific Command **(Optional)**"))
        elif command == "ping":
            await Message.msg(ctx, "**/ping** command - Parzibot's Ping", "**Syntax:** **/ping**")
        elif command == "users":
            await Message.msg(ctx, "**/users** command - The List of Text Channel Members", "**Syntax:** **/users**")

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
    client.add_cog(Commands(client))

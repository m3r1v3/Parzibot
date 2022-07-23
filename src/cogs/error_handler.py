import discord
from discord import Embed, Colour
from discord.ext import commands

from message import Message


class ErrorHandler(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        """Returns a command error message on slash command error"""
        await Message.error(ctx, "Error", "Something went wrong! Try again")


def setup(client):
    """Setup function"""
    client.add_cog(ErrorHandler(client))

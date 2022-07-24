import discord
from discord import Embed, Colour
from discord.ext import commands

from message import Message


class ErrorHandler(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        await Message.error(ctx, "Error", "Something went wrong! Try again")


def setup(client):
    client.add_cog(ErrorHandler(client))

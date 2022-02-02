import discord
from discord import Embed, Colour
from discord.ext import commands


class Errors(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @staticmethod
    def get_error_embed(title: str, description: str):
        embed = Embed(title=title, description=description, color=Colour(0xff6868))
        embed.set_thumbnail(url="attachment://ParzibotError.png")
        return embed

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        """Returns a command error message on slash command error"""
        await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"),
                embed=Errors.get_error_embed("Error", "Something went wrong! Try again"))


def setup(client):
    """Setup function"""
    client.add_cog(Errors(client))

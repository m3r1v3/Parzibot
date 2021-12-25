from discord import Embed, Colour
from discord.ext import commands


class Errors(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        """Returns a command error message on slash command error"""
        await ctx.send(
            embed=Embed(
                title=f"Error",
                description=f"Something went wrong! Try again",
                color=Colour(0xd95959)
                )
            )


def setup(client):
    """Setup function"""
    client.add_cog(Errors(client))

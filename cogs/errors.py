from discord.ext import commands
from discord_slash import error


class Errors(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        """Returns a command error message on slash command error"""
        await ctx.send(f"**Error**: `Something went wrong! Try again`")


def setup(client):
    """Setup function"""
    client.add_cog(Errors(client))

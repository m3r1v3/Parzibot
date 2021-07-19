import discord
from discord.ext import commands


class Events(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Returns a command error message"""
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await ctx.send('Command is not finished')
        elif isinstance(error, discord.ext.commands.CommandNotFound):
            await ctx.send('Command does not found')
        elif isinstance(error, discord.ext.commands.BotMissingPermissions):
            await ctx.send("You don't have permissions for using this command")
        else:
            await ctx.send("Unknown error")


def setup(client):
    """Setup function"""
    client.add_cog(Events(client))

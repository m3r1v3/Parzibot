from discord.ext import commands


class Events(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Returns a command error message"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"**Error**: `Command not found`")
        elif isinstance(error, (commands.CommandInvokeError, commands.MissingPermissions)):
            await ctx.send("**Error**: `You don't have permissions for using this command!`")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Error**: `Command isn't finished!`")
        else:
            await ctx.send(f"**Unknown Error**")


def setup(client):
    """Setup function"""
    client.add_cog(Events(client))

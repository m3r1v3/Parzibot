from discord.ext import commands

from cogs.language import get_lang


class Events(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Returns a command error message"""
        if isinstance(error, commands.MissingRequiredArgument):
            if get_lang() == "EN":
                await ctx.send('Command is not finished.')
            else:
                await ctx.send(f'Команда не дописана')
        elif isinstance(error, commands.CommandNotFound):
            if get_lang() == "EN":
                await ctx.send('Command does not found.')
            else:
                await ctx.send(f'Команда не распознана.')
        elif isinstance(error, commands.MissingPermissions):
            if get_lang() == "EN":
                await ctx.send('Not enough access rights.')
            else:
                await ctx.send(f'Не хватает прав доступа.')
        else:
            await ctx.send('Command Error.')


def setup(client):
    """Setup function"""
    client.add_cog(Events(client))

import discord
from discord.ext import commands

from cogs.language import get_language


class Events(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Returns a command error message"""
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            if get_language(ctx.message.author.name, ctx.message.guild.id) == "RU":
                await ctx.send(f'Команда не дописана')
            else:
                await ctx.send('Command is not finished')
        elif isinstance(error, discord.ext.commands.CommandNotFound):
            if get_language(ctx.message.author.name, ctx.message.guild.id) == "RU":
                await ctx.send(f'Команда не распознана')
            else:
                await ctx.send('Command does not found')
        elif isinstance(error, discord.ext.commands.CommandInvokeError):
            if get_language(ctx.message.author.name, ctx.message.guild.id) == "RU":
                await ctx.send(f'Не хватает прав доступа')
            else:
                await ctx.send('Not enough access rights')


def setup(client):
    """Setup function"""
    client.add_cog(Events(client))

import discord
from discord.ext import commands

from cogs.language_commands import get_language


class Events(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Returns a command error message"""
        got_language = get_language(ctx.message.author.name, str(ctx.guild.id))
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            if got_language == "RU":
                await ctx.send('Команда не дописана')
            else:
                await ctx.send('Command is not finished')
        elif isinstance(error, discord.ext.commands.CommandNotFound):
            if got_language == "RU":
                await ctx.send('Команда не распознана')
            else:
                await ctx.send('Command does not found')
        elif isinstance(error, discord.ext.commands.BotMissingPermissions):
            if got_language == "RU":
                await ctx.send('У вас нет прав для использования данной команды')
            else:
                await ctx.send("You don't have permissions for using this command")
        else:
            if got_language == "RU":
                await ctx.send('Неизвестная ошибка')
            else:
                await ctx.send("Unknown error")


def setup(client):
    """Setup function"""
    client.add_cog(Events(client))

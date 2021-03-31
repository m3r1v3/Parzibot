from discord.ext import commands

from database import User, session


def get_language(nickname, server: str):
    """Get language"""
    try:
        return session.query(User).filter_by(nickname=nickname, server=str(server)).first().language
    except AttributeError:
        User().add(nickname, str(server))


def set_language(nickname, server: str, language):
    """Set language"""
    User().delete(nickname, str(server))
    User().add(nickname, str(server), language)


class LanguageCommands(commands.Cog):

    def __init__(self, client):
        """Initialisation client and LANGUAGE"""
        self.client = client

    @commands.command()
    async def lang(self, ctx, language=""):
        """Set language"""
        User().check_user(ctx.message.author.name, str(ctx.guild.id))
        got_language = get_language(ctx.message.author.name, str(ctx.guild.id))
        if language == "":
            if got_language == "RU":
                await ctx.send(
                    f'Установленный язык: {got_language}')
            else:
                await ctx.send(
                    f'Installed language: {got_language}')
        elif language == "EN":
            await ctx.send("Language set")
            set_language(ctx.message.author.name, str(ctx.guild.id), language)
        elif language == "RU":
            await ctx.send("Язык установлен")
            set_language(ctx.message.author.name, str(ctx.guild.id), language)
        else:
            await ctx.send("Set Error")


def setup(client):
    """Setup function"""
    client.add_cog(LanguageCommands(client))

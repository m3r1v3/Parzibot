from discord.ext import commands

from user_base import UserBase, create_session, check_user, add_in_user_base


def get_language(nickname, server):
    """Get language"""
    try:
        return create_session().query(UserBase).filter_by(nickname=nickname, server=server).first().language
    except AttributeError:
        add_in_user_base(nickname, server)


def set_language(nickname, server, language):
    """Set language"""
    session = create_session()
    session.query(UserBase).filter_by(nickname=nickname, server=server).first().language = language
    session.commit()


class Language(commands.Cog):

    def __init__(self, client):
        """Initialisation client and LANGUAGE"""
        self.client = client

    @commands.command()
    async def lang(self, ctx, language=""):
        """Set language"""
        check_user(ctx.message.author.name, ctx.message.guild.id)
        if language == "":
            if get_language(ctx.message.author.name, ctx.message.guild.id) == "RU":
                await ctx.send(
                    f'Установленный язык: {get_language(ctx.message.author.name, ctx.message.guild.id)}')
            else:
                await ctx.send(
                    f'Installed language: {get_language(ctx.message.author.name, ctx.message.guild.id)}')
        elif language == "EN":
            await ctx.send("Language set")
            set_language(ctx.message.author.name, ctx.message.guild.id, language)
        elif language == "RU":
            await ctx.send("Язык установлен")
            set_language(ctx.message.author.name, ctx.message.guild.id, language)
        else:
            await ctx.send("Set Error")


def setup(client):
    """Setup function"""
    client.add_cog(Language(client))

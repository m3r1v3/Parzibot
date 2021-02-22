from discord.ext import commands


def get_language():
    """Get language"""
    with open('language.json', 'r') as lang:
        return lang.readline()[2:-2]


def set_language(language=""):
    """Set language"""
    with open('language.json', 'r+') as lang:
        return lang.write('["' + language + '"]')


class Language(commands.Cog):

    def __init__(self, client):
        """Initialisation client and LANGUAGE"""
        self.client = client
        self.LANGUAGE = get_language()

    @commands.command()
    async def lang(self, ctx, language=""):
        """Set language"""
        if language == "":
            if get_language() == "EN":
                await ctx.send(f'Installed language: {get_language()}')
            else:
                await ctx.send(f'Установленный язык: {get_language()}')
        elif language == "EN":
            await ctx.send("Language set")
            self.LANGUAGE = set_language(language)
        elif language == "RU":
            await ctx.send("Язык установлен")
            self.LANGUAGE = set_language(language)
        else:
            await ctx.send("Set Error")


def setup(client):
    """Setup function"""
    client.add_cog(Language(client))

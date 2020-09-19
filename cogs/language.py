from discord.ext import commands


def get_lang():
    """Get language"""
    with open('lang.json', 'r') as lang:
        return lang.readline()[2:-2]


def set_lang(language=""):
    """Set language"""
    with open('lang.json', 'r+') as lang:
        return lang.write('["' + language + '"]')


class Language(commands.Cog):

    def __init__(self, client):
        """Initialisation client and LANG"""
        self.client = client
        self.LANG = get_lang()

    @commands.command()
    async def lang(self, ctx, language=""):
        """Set language"""
        if language == "":
            if get_lang() == "EN":
                await ctx.send(f'Installed language: {get_lang()}')
            else:
                await ctx.send(f'Установленный язык: {get_lang()}')
        elif language == "EN":
            await ctx.send("Language set.")
            self.LANG = set_lang(language)
        elif language == "RU":
            await ctx.send("Язык установлен")
            self.LANG = set_lang(language)
        else:
            await ctx.send("Set Error.")


def setup(client):
    """Setup function"""
    client.add_cog(Language(client))

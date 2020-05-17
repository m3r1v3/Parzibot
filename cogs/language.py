# language.py
# Recycled 05/17/20
from discord.ext import commands


def get_lang():
    with open('cogs/lang.txt', 'r') as lang:
        return lang.readline()


def set_lang(language):
    with open('cogs/lang.txt', 'w') as lang:
        return lang.write(language)


class Lang(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.LANG = get_lang()

    @commands.has_role(670599227335770143)
    @commands.command(aliases=['lang'])
    async def set_language(self, ctx, lang):
        if lang == "EN":
            await ctx.send("Language set.")
            self.LANG = set_lang(lang)
        elif lang == "RU":
            await ctx.send("Язык установлен")
            self.LANG = set_lang(lang)
        else:
            await ctx.send("Set Error.")


def setup(client):
    client.add_cog(Lang(client))

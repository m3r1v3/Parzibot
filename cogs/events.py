import discord
from discord import Embed, Colour
from discord.ext import commands

from database import Role


class Events(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @staticmethod
    def get_embed(title: str, description: str):
        embed = Embed(title=title, description=description, color=Colour(0x68FFD9))
        embed.set_thumbnail(url="attachment://Parzibot.png")
        return embed

    @staticmethod
    def get_error_embed(title: str, description: str):
        embed = Embed(title=title, description=description, color=Colour(0xff6868))
        embed.set_thumbnail(url="attachment://ParzibotError.png")
        return embed

    @commands.Cog.listener()
    async def on_ready(self):
        """Function check the work of the bot"""
        print('{0} is ready'.format(self.client.user))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Sending a personal message about the bot and issuing a role in the chat"""
        await member.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
            embed=Events.get_embed(f"Hey **{member}**!", "White **/help** to find out my command or **/musichelp** to find out my music command"))
        role = discord.utils.get(member.guild.roles, id=int(Role().get_role(member.guild.id)))
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Notifies about the issuance and withdrawal of a role from a user"""
        if len(before.roles) < len(after.roles):
            for i in after.roles:
                if i not in before.roles:
                    await after.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                        embed=Events.get_embed("You have received a role", f"You received the **{i}** role"))
        elif len(before.roles) > len(after.roles):
            for i in before.roles:
                if i not in after.roles:
                    await after.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"),
                        embed=Events.get_error_embed("You have deprived a role", f"You deprived the **{i}** role"))


def setup(client):
    """Setup function"""
    client.add_cog(Events(client))

import discord
from discord import Embed, Colour
from discord.ext import commands

from database import Role


class Events(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        """Function check the work of the bot"""
        print('{0} is ready'.format(self.client.user))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Sending a personal message about the bot and issuing a role in the chat"""
        embed=Embed(
            title=f"Hey **{member}**!",
            description="White **/help** to find out my command or **/musichelp** to find out my music command",
            color=Colour(0x68FFD9))
        embed.set_thumbnail(url="attachment://Parzibot.png")
        await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)

        role = discord.utils.get(member.guild.roles, id=int(Role().get_role(member.guild.id)))
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Notifies about the issuance and withdrawal of a role from a user"""
        if len(before.roles) < len(after.roles):
            for i in after.roles:
                if i not in before.roles:
                    embed=Embed(title=f"You have received the **{i}** role", color=Colour(0x68FFD9))
                    embed.set_thumbnail(url="attachment://Parzibot.png")
                    await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        elif len(before.roles) > len(after.roles):
            for i in before.roles:
                if i not in after.roles:
                    embed=Embed(title=f"You have deprived the **{i}** role", color=Colour(0xff6868))
                    embed.set_thumbnail(url="attachment://ParzibotError.png")
                    await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"), embed=embed)


def setup(client):
    """Setup function"""
    client.add_cog(Events(client))

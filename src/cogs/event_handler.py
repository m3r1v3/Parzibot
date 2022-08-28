import discord
from discord import app_commands, Embed, Colour
from discord.ext import commands

from message import Message

class EventHandler(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('{0} is ready'.format(self.bot.user))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await Message.msg(member, f"Parzibot // Hey **{member}**!", "White **/help** to find out basic command, **/gamehelp** to find out game commands or **/musichelp** to find out music command")
        await member.add_roles(discord.utils.get(member.guild.roles, id=int(Role().get_role(member.guild.id))))

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if len(before.roles) < len(after.roles):
            for i in after.roles: 
                if i not in before.roles: await Message.msg(before, "Parzibot // Received role", f"You has been received **{i} Role**")
        elif len(before.roles) > len(after.roles):
            for i in before.roles:
                if i not in after.roles: await Message.error(before, "Parzibot // Deprived role", f"You has been deprived **{i} Role**")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EventHandler(bot))

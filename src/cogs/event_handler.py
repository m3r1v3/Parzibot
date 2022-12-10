import discord
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
        await Message.basic_msg(member, Message.get_event_msg("titles", "greeting"), Message.get_event_msg("messages", "greeting-message"))
        await member.add_roles(discord.utils.get(member.guild.roles, id=int(Role().get_role(member.guild.id))))

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if len(before.roles) < len(after.roles):
            for i in after.roles:
                if i not in before.roles: 
                    await Message.basic_msg(before, 
                        Message.get_event_msg("titles", "receive"),
                        Message.get_event_msg("messages", "receive-message").format(role=i))
        elif len(before.roles) > len(after.roles):
            for i in before.roles:
                if i not in after.roles: 
                    await Message.basic_msg(before,
                        Message.get_event_msg("titles", "deprive"),
                        Message.get_event_msg("messages", "deprive-message").format(role=i))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EventHandler(bot))

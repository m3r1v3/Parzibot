import discord
from discord import Embed, Colour
from discord.ext import commands

from database import Role

from message import Message


class EventHandler(commands.Cog):

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
        await Message.msg(member, f"Hey **{member}**!", "White **/help** to find out basic command, **/gamehelp** to find out game commands or **/musichelp** to find out music command")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Notifies about the issuance and withdrawal of a role from a user"""
        if len(before.roles) < len(after.roles):
            for i in after.roles:
                if i not in before.roles:
                    await Message.msg(member, "You have received a role", f"You received the **{i}** role")
        elif len(before.roles) > len(after.roles):
            for i in before.roles:
                if i not in after.roles:
                    await Message.error(member, "You have deprived a role", f"You deprived the **{i}** role")


def setup(client):
    """Setup function"""
    client.add_cog(EventHandler(client))

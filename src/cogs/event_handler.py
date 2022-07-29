import discord
from discord import Embed, Colour
from discord.ext import commands

from database import Role

from message import Message


class EventHandler(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('{0} is ready'.format(self.client.user))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await Message.msg(member, f"Parzibot // Hey **{member}**!", "White **/help** to find out basic command, **/gamehelp** to find out game commands or **/musichelp** to find out music command")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if len(before.roles) < len(after.roles):
            for i in after.roles:
                if i not in before.roles:
                    await Message.msg(before, "Parzibot // Received role", f"You received **{i} Role**")
        elif len(before.roles) > len(after.roles):
            for i in before.roles:
                if i not in after.roles:
                    await Message.error(before, "Parzibot // Deprived role", f"You deprived **{i} Role**")


def setup(client):
    client.add_cog(EventHandler(client))

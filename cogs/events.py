from discord.ext import commands


class Events(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        """Function check the work of the bot"""
        print('{0} is online.'.format(self.client.user))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Sending a personal message about the bot and issuing a role in the chat"""
        await member.send(f'Hey {member}! White $help to find out my command. For replace language write $lang `EN/RU`')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Output information about user exit"""
        await member.send(f'{member} leave from server')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Notifies about the issuance and withdrawal of a role from a user"""
        if len(before.roles) < len(after.roles):
            for i in after.roles:
                if i not in before.roles:
                    await after.send(f'You have been given a role {i}!')
        elif len(before.roles) > len(after.roles):
            for i in before.roles:
                if i not in after.roles:
                    await after.send(f'You were deprived of the role {i}')


def setup(client):
    """Setup function"""
    client.add_cog(Events(client))

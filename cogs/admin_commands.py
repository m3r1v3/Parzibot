import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

from database import Role


class AdminCommands(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @cog_ext.cog_slash(name="ban",
                       description="Ban a member on the server",
                       options=[
                           create_option(
                               name="member",
                               description="Member who will be blocked",
                               option_type=6,
                               required=True
                           ),
                           create_option(
                               name="reason",
                               description="Ban reason",
                               option_type=3,
                               required=False
                           )
                       ]
                       )
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a member on the server"""
        if ctx.author.guild_permissions.manage_messages:
            await member.ban(reason=reason)
            await ctx.send(f'Banned **{member.mention}**')
        else:
            await ctx.send("**You doesn't have permissions for executing this command**")

    @cog_ext.cog_slash(name="giverole",
                       description="Give role to member",
                       options=[
                           create_option(
                               name="member",
                               description="Role recipient member",
                               option_type=6,
                               required=True
                           ),
                           create_option(
                               name="role",
                               description="Role",
                               option_type=8,
                               required=True)
                       ]
                       )
    async def giverole(self, ctx, member: discord.Member, role):
        """Give role to member"""
        if ctx.author.guild_permissions.manage_messages:
            await member.add_roles(role)
            await ctx.send(f"Role was given to **{member}**")
        else:
            await ctx.send("**You doesn't have permissions for executing this command**")

    @cog_ext.cog_slash(name="nickname",
                       description="Change nickname to member",
                       options=[
                           create_option(
                               name="member",
                               description="Member to whom we change nickname",
                               option_type=6,
                               required=True
                           ),
                           create_option(
                               name="nickname",
                               description="Member's future nickname",
                               option_type=3,
                               required=False
                           )
                       ]
                       )
    async def nickname(self, ctx, member: discord.Member, *, nickname=None):
        """Change nickname to member"""
        if ctx.author.guild_permissions.manage_messages:
            await member.edit(nick=nickname)
            await ctx.send(f'Nickname was changed for **{member}**')
        else:
            await ctx.send("**You doesn't have permissions for executing this command**")

    @cog_ext.cog_slash(name="kick",
                       description="Kick a member from the server",
                       options=[
                           create_option(
                               name="member",
                               description="Member to whom we kick",
                               option_type=6,
                               required=True
                           ),
                           create_option(
                               name="reason",
                               description="Kick reason",
                               option_type=3,
                               required=False
                           )
                       ]
                       )
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.manage_messages:
            """Kick a member from the server"""
            await member.kick(reason=reason)
            await ctx.send(f'Kicked **{member}**')
        else:
            await ctx.send("**You doesn't have permissions for executing this command**")

    @cog_ext.cog_slash(name="setrole",
                       description="Set default role on the server",
                       options=[
                           create_option(
                               name="role",
                               description="Role ID",
                               option_type=3,
                               required=True
                           )
                       ]
                       )
    async def setrole(self, ctx, role):
        """Set default role on the server"""
        if ctx.author.guild_permissions.manage_messages:
            Role().add(role, str(ctx.guild.id))
            await ctx.send("**Default role for server set**")
        else:
            await ctx.send("**You doesn't have permissions for executing this command**")

    @cog_ext.cog_slash(name="removerole",
                       description="Remove default role on the server",
                       options=[
                           create_option(
                               name="role",
                               description="Role ID",
                               option_type=3,
                               required=True
                           )
                       ]
                       )
    async def removerole(self, ctx, role):
        """Remove default role on the server"""
        if ctx.author.guild_permissions.manage_messages:
            Role().delete(role, str(ctx.guild.id))
            await ctx.send("**Default role for server removed**")
        else:
            await ctx.send("**You doesn't have permissions for executing this command**")

    @cog_ext.cog_slash(name="adminhelp", description="Parzibot Admin Commands list")
    async def adminhelp(self, ctx):
        """Parzibot Admin Commands list"""
        if ctx.author.guild_permissions.manage_messages:
            await ctx.send('**Admin Commands**'
                           '\n\t - **/ban** `@member` - Ban a member on the server'
                           '\n\t - **/giverole** `@member` `role` - Give a role to a member'
                           '\n\t - **/nickname** `@member` `new nickname` - Change member\'s nickname'
                           '\n\t - **/kick** `@member` - Kick a member from the server'
                           '\n\t - **/setrole** `role id` - Set default role on the server'
                           '\n\t - **/removerole** `role id` - Remove default role on the server')
        else:
            await ctx.send("**You doesn't have permissions for executing this command**")


def setup(client):
    """Setup function"""
    client.add_cog(AdminCommands(client))
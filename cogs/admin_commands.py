import discord
from discord import Embed, Colour
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

from database import Role


class AdminCommands(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @cog_ext.cog_slash(name="adminhelp", description="Parzibot Admin Commands list")
    async def adminhelp(self, ctx):
        """Parzibot Admin Commands list"""
        if ctx.author.guild_permissions.manage_messages:
            await ctx.send(embed=Embed(title=f"**Admin Commands**",
                    description=f'\n\t - **/adminhelp** - List of Parzibot admin commands'
                           '\n\t - **/ban** `@member` - Ban a member on the server'
                           '\n\t - **/giverole** `@member` `role` - Give a role to a member'
                           '\n\t - **/kick** `@member` - Kick a member from the server'
                           '\n\t - **/nickname** `@member` `new nickname` - Change member\'s nickname'
                           '\n\t - **/defaultrole** `role id` - Set default role on the server'
                           '\n\t - **/removedefaultrole** - Remove default role on the server',
                    color=Colour(0xd3d959)))
        else:
            await ctx.send(embed=Embed(title=f"Error",
                    description=f"**You doesn't have permissions for executing this command**",
                    color=Colour(0xd95959)))

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
                       ])
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a member on the server"""
        if ctx.author.guild_permissions.manage_messages:
            await member.ban(reason=reason)
            await ctx.send(embed=Embed(title=f"Member was banned",
                    description=f"**{member.mention}** has been banned",
                    color=Colour(0xd3d959)))
        else:
            await ctx.send(embed=Embed(title=f"Error",
                    description=f"**You doesn't have permissions for executing this command**",
                    color=Colour(0xd95959)))

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
                       ])
    async def giverole(self, ctx, member: discord.Member, role):
        """Give role to member"""
        if ctx.author.guild_permissions.manage_messages:
            await member.add_roles(role)
            await ctx.send(embed=Embed(title=f"Member received role",
                    description=f"Role has been given to **{member}**",
                    color=Colour(0xd3d959)))
        else:
            await ctx.send(embed=Embed(title=f"Error",
                    description=f"**You doesn't have permissions for executing this command**",
                    color=Colour(0xd95959)))

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
                       ])
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.manage_messages:
            """Kick a member from the server"""
            await member.kick(reason=reason)
            await ctx.send(embed=Embed(title=f"Member was kicked",
                    description=f"**{member}** has been kicked",
                    color=Colour(0xd3d959)))
        else:
            await ctx.send(embed=Embed(title=f"Error",
                    description=f"**You doesn't have permissions for executing this command**",
                    color=Colour(0xd95959)))

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
                       ])
    async def nickname(self, ctx, member: discord.Member, *, nickname=None):
        """Change nickname to member"""
        if ctx.author.guild_permissions.manage_messages:
            await member.edit(nick=nickname)
            await ctx.send(embed=Embed(title=f"Nickname was changed",
                    description=f"**{member}** nickname has been changed",
                    color=Colour(0xd3d959)))
        else:
            await ctx.send(embed=Embed(title=f"Error",
                    description=f"**You doesn't have permissions for executing this command**",
                    color=Colour(0xd95959)))

    @cog_ext.cog_slash(name="defaultrole",
                       description="Set default role on the server",
                       options=[
                           create_option(
                               name="role",
                               description="Role ID",
                               option_type=3,
                               required=True
                           )
                       ])
    async def defaultrole(self, ctx, role):
        """Set default role on the server"""
        if ctx.author.guild_permissions.manage_messages:
            if Role().get_role(str(ctx.guild.id)) is None:
                Role().add(role, str(ctx.guild.id))
                await ctx.send(embed=Embed(title=f"Default role was set",
                    description=f"**Server default role has been set**",
                    color=Colour(0xd3d959)))
            else: 
                if Role().get_role(str(ctx.guild.id)) is None:
                    Role().add(role, str(ctx.guild.id))
                    await ctx.send(embed=Embed(title=f"Default role already set",
                        description=f"**Server default role already had been set**",
                        color=Colour(0x59d9b9)))
        else:
            await ctx.send(embed=Embed(title=f"Error",
                    description=f"**You doesn't have permissions for executing this command**",
                    color=Colour(0xd95959)))

    @cog_ext.cog_slash(name="removedefaultrole",
                       description="Remove default role on the server"
                       )
    async def removedefaultrole(self, ctx):
        """Remove default role on the server"""
        if ctx.author.guild_permissions.manage_messages:
            if not Role().get_role(str(ctx.guild.id)) is None:
                Role().delete(str(ctx.guild.id))
                await ctx.send(embed=Embed(title=f"Default role was removed",
                        description=f"**Server default role has been removed**",
                        color=Colour(0xd3d959)))
            else:
                Role().add(role, str(ctx.guild.id))
                await ctx.send(embed=Embed(title=f"Default role hadn't set",
                        description=f"**Server default role already hadn't been set**",
                        color=Colour(0x59d9b9)))
        else:
            await ctx.send(embed=Embed(title=f"Error",
                    description=f"**You doesn't have permissions for executing this command**",
                    color=Colour(0xd95959)))


def setup(client):
    """Setup function"""
    client.add_cog(AdminCommands(client))

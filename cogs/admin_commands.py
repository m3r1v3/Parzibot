import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from sqlalchemy.orm.exc import UnmappedInstanceError

from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

from database import Role


class AdminCommands(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @cog_ext.cog_slash(name="kick",
                       description="Kick member from server",
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
            await member.kick(reason=reason)
            await ctx.send(f'Kicked **{member.mention}**.')
        else:
            await ctx.send("**You doesn't have permissions for executing this command**")

    @cog_ext.cog_slash(name="ban",
                       description="Ban member from server",
                       options=[
                        create_option(
                            name="member",
                            description="Member to whom we ban",
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
        if ctx.author.guild_permissions.manage_messages:
            await member.ban(reason=reason)
            await ctx.send(f'Banned **{member.mention}**.')
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
                            description="Future nickname",
                            option_type=3,
                            required=False
                            )
                        ]
                       )
    async def nickname(self, ctx, member: discord.Member, *, nickname=None):
        if ctx.author.guild_permissions.manage_messages:
            await member.edit(nick=nickname)
            await ctx.send(f'Nickname was changed for **{member.mention}**.')
        else:
            await ctx.send("**You doesn't have permissions for executing this command**")

    @cog_ext.cog_slash(name="set_role",
                       description="Set default role for server",
                       options=[
                        create_option(
                            name="role",
                            description="Default role",
                            option_type=3,
                            required=True
                            )
                        ]
                       )
    async def set_role(self, ctx, role):
        if ctx.author.guild_permissions.manage_messages:
            Role().add(role, str(ctx.guild.id))
            await ctx.send("Default role for server was installed.")
        else:
            await ctx.send("**You doesn't have permissions for executing this command**")

    @cog_ext.cog_slash(name="remove_role",
                       description="Remove default role for server",
                       options=[
                        create_option(
                            name="role",
                            description="Default role",
                            option_type=3,
                            required=True
                            )
                        ]
                       )
    async def remove_role(self, ctx, role):
        if ctx.author.guild_permissions.manage_messages:
            Role().delete(role, str(ctx.guild.id))
            await ctx.send("Default role for server removed.")
        else:
            await ctx.send("**You doesn't have permissions for executing this command**")

    @cog_ext.cog_slash(name="give_role",
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
    async def give_role(self, ctx, member: discord.Member, role):
        if ctx.author.guild_permissions.manage_messages:
            await member.add_roles(role)
            await ctx.send(f"Role was given to **{member}**.")
        else:
            await ctx.send("**You doesn't have permissions for executing this command**")

    @cog_ext.cog_slash(name="admin_help", description="List of Parzibot admin commands")
    async def admin_help(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            await ctx.send('**Admin Commands**'
                           '\n\t - **/ban** `@user` - Ban user'
                           '\n\t - **/give_role** `@user` `role_id` - Give role'
                           '\n\t - **/nickname** `@user` `new_nick` - Edit nickname'
                           '\n\t - **/kick** `@user` - Kick user'
                           '\n\t - **/set_role** `role_id` - Set default role'
                           '\n\t - **/remove_role** `role_id` - Remove default role')
        else:
            await ctx.send("**You doesn't have permissions for executing this command**")


def setup(client):
    """Setup function"""
    client.add_cog(AdminCommands(client))

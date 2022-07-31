import discord
from discord import Embed, Colour
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

from database import Role
from message import Message


class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="adminhelp", description="The list of Parzibot admin commands")
    async def adminhelp(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            await Message.admin(ctx, "Parzibot // Admin Commands", (
                '**Help Commands**\n'
                ' • **/adminhelp** `command` - The list of Parzibot admin commands\n\n'
                '**Announce Commands**\n'
                ' • **/announce** `title` `message` - Make announce message in current Text Channel\n\n'
                '**Member Control Commands**\n'
                ' • **/ban** `member` - Ban member on your Server\n'
                ' • **/kick** `member` - Kick member on your Server\n'
                ' • **/nickname** `member` `nickname` - Change nickname to Member on Server\n\n'
                '**Role Commands**\n'
                ' • **/role** `name` `color` - Create role with default role permissions on Server\n'
                ' • **/giverole** `member` `role` - Give role to Member on Server\n'
                ' • **/defaultrole** `role` - Set default role what will be giving to new members of Server\n'
                ' • **/defaultroleremove** - Remove default role what will be giving to new members of Server'))
        else: await Message.error(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")

    @cog_ext.cog_slash(
        name="announce",
        description="Make announce message in current Text Channel",
        options=[
            create_option(
                name="message",
                description="Text of announce message",
                option_type=3,
                required=True)
            ])
    async def announce(self, ctx, message: str):
        if ctx.author.guild_permissions.manage_messages:
            await Message.admin(ctx, "Parzibot // Announce", message.replace("\\n", "\n"))
        else: await Message.error(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")

    @cog_ext.cog_slash(
        name="ban",
        description="Ban member on your Server",
        options=[
            create_option(
                name="member",
                description="Member who will be banned",
                option_type=6,
                required=True
                )
            ])
    async def ban(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.manage_messages:
            await member.ban(reason=None)
            await Message.admin(ctx, "Parzibot // Ban", f"**{member}** has been banned")
        else: await Message.error(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")

    @cog_ext.cog_slash(
        name="kick",
        description="Kick member on your Server",
        options=[
            create_option(
                name="member",
                description="The Member Who Will Be Kicked",
                option_type=6,
                required=True
                )
            ])
    async def kick(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.manage_messages:
            await member.kick(reason=None)
            await Message.admin(ctx, "Parzibot // Kick", f"**{member}** has been kicked")
        else: await Message.error(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")

    @cog_ext.cog_slash(
        name="role",
        description="Create role with default role permissions on Server",
        options=[
            create_option(
                name="name",
                description="Name of future role",
                option_type=3,
                required=True
                ),
            create_option(
                name="color",
                description="Role color (Hex Code without '#' (6 symbols))",
                option_type=3,
                required=True
                )
            ])
    async def role(self, ctx, name: str, color: str):
        if ctx.author.guild_permissions.manage_messages:
            if Role().get_role(str(ctx.guild.id)) is not None:
                try:
                    if len(color) == 6:
                        rgb = tuple(int(hex(int(color, 16))[2:8][i:i+2], 16) for i in (0, 2, 4))
                        await ctx.guild.create_role(name=name,
                            colour=discord.Color.from_rgb(rgb[0], rgb[1], rgb[2]),
                            permissions=discord.utils.get(ctx.author.guild.roles, id=int(Role().get_role(ctx.author.guild.id))).permissions)
                        await Message.admin(ctx, "Parzibot // Role", f"**{name} Role** added on Server")
                    else: await Message.admin(ctx, "Parzibot // Incorrect color", f"**Hex Color Code** is written in the incorrect format")
                except ValueError: await Message.admin(ctx, "Parzibot // Incorrect color", f"**Hex Color Code** is written in the incorrect format")
            else: await Message.admin(ctx, "Parzibot // Default Role Hadn't Set", "**Server Default Role** should be set for using this command")
        else: await Message.error(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")

    @cog_ext.cog_slash(
        name="giverole",
        description="Give role to Member on Server",
        options=[
            create_option(
                name="member",
                description="Member who will receive Role",
                option_type=6,
                required=True
                ),
            create_option(
                name="role",
                description="Role that will be received by Member",
                option_type=8,
                required=True
                )
            ])
    async def giverole(self, ctx, member: discord.Member, role):
        if ctx.author.guild_permissions.manage_messages:
            await member.add_roles(role)
            await Message.admin(ctx, "Parzibot // Give Role", f"**{role.name} Role** has been given to **{member}**")
        else: await Message.error(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")

    @cog_ext.cog_slash(
        name="nickname",
        description="Change nickname to Member on Server",
        options=[
            create_option(
                name="member",
                description="The Member to Whom We Will Change Nickname",
                option_type=6,
                required=True
                ),
                create_option(
                    name="nickname",
                    description="The Member's Future Nickname",
                    option_type=3,
                    required=False
                    )
                ])
    async def nickname(self, ctx, member: discord.Member, *, nickname=None):
        if ctx.author.guild_permissions.manage_messages:
            await member.edit(nick=nickname)
            await Message.admin(ctx, "Parzibot // Nickname Changed", f"**{member}**'s nickname has been changed")
        else: await Message.error(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")

    @cog_ext.cog_slash(
        name="defaultrole",
        description="Set default role what will be giving to new members of Server",
        options=[
            create_option(
                name="role",
                description="Role that will be giving",
                option_type=8,
                required=True
                )
            ])
    async def defaultrole(self, ctx, role):
        if ctx.author.guild_permissions.manage_messages:
            if Role().get_role(str(ctx.guild.id)) is None:
                Role().add(str(role.id), str(ctx.guild.id))
                await Message.admin(ctx, "Parzibot // Default Role Set", "**Server Default Role** has been set")
            else: await Message.admin(ctx, "Parzibot // Default Role Already Set", "**Server Default Role** already had been set")
        else: await Message.error(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")

    @cog_ext.cog_slash(name="defaultroleremove", description="Remove default role what will be giving to new members of Server")
    async def removedefaultrole(self, ctx):
        if ctx.author.guild_permissions.manage_messages:
            if Role().get_role(str(ctx.guild.id)) is not None:
                Role().delete(str(ctx.guild.id))
                await Message.admin(ctx, "Parzibot // Default Role Removed", "**Server Default Role** was removed")
            else: await Message.admin(ctx, "Parzibot // Default Role Hadn't Set", "**Server Default Role** should be set for using this command")
        else: await Message.error(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")


def setup(client):
    client.add_cog(AdminCommands(client))

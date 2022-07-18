import discord
from discord import Embed, Colour
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

from database import Role
from message import Message


class Admin(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @cog_ext.cog_slash(
        name="adminhelp",
        description="The List of Parzibot Admin Commands",
        options=[
            create_option(
                name="command",
                description="The Help Message for Specific Admin Command",
                option_type=3,
                required=False,
                choices=[
                    create_choice(name="adminhelp", value="adminhelp"),
                    create_choice(name="ban", value="ban"),
                    create_choice(name="defaultrole", value="defaultrole"),
                    create_choice(name="giverole", value="giverole"),
                    create_choice(name="kick", value="kick"),
                    create_choice(name="nickname", value="nickname"),
                    create_choice(name="removedefaultrole", value="removedefaultrole")
                    ])
            ])
    async def adminhelp(self, ctx, command=None):
        """Parzibot Admin Commands list"""
        if ctx.author.guild_permissions.manage_messages:
            if command is None:
                await Message.admin(ctx, "**Admin Commands**", (
                        ' • **/adminhelp** `command` - The List of Parzibot Admin Commands\n'
                        ' • **/ban** `member` - Ban The Member on The Server\n'
                        ' • **/defaultrole** `role` - Set The Default Role on The Server\n'
                        ' • **/giverole** `member` `role` - Give The Role to The Member\n'
                        ' • **/kick** `member` - Kick The Member from The Server\n'
                        ' • **/nickname** `member` `nickname` - Change The Nickname to The Member\n'
                        ' • **/removedefaultrole** - Remove The Default Role on The Server'))
            elif command == "adminhelp":
                await Message.admin(ctx, "**/adminhelp** command - The List of Parzibot Admin Commands", (
                        '**Syntax:** **/adminhelp** `command`\n'
                        '**Options:** `command` - The Help Message for Specific Admin Command **(Optional)**')) 
            elif command == "ban":
                await Message.admin(ctx, "**/ban** command - Ban The Member on The Server", (
                        '**Syntax:** **/ban** `member`\n'
                        '**Options:** `member` - The Member Who Will Be Banned **(Required)**'))
            elif command == "defaultrole":
                await Message.admin(ctx, "**/defaultrole** command - Set The Default Role on The Server", (
                        '**Syntax:** **/defaultrole** `role`\n'
                        '**Options:** `role` - The Role Name **(Required)**'))
            elif command == "giverole":
                await Message.admin(ctx, "**/giverole** command - Give The Role to The Member", (
                        '**Syntax:** **/giverole** `member` `role`\n'
                        '**Options:**\n'
                        '`member` - Member Who Will Received Role **(Required)**\n'
                        '`role` - The Role Name **(Required)**'))
            elif command == "kick":
                await Message.admin(ctx, "**/kick** command - Kick The Member from The Server", (
                        '**Syntax:** **/kick** `member`\n'
                        '**Options:** `member` - The Member Who Will Be Kicked **(Required)**'))
            elif command == "nickname":
                await Message.admin(ctx, "**/nickname** command - Change The Nickname to The Member", (
                        '**Syntax:** **/nickname** `member` `nickname`\n'
                        '**Options:**\n'
                        '`member` - The Member to Whom We Will Change Nickname **(Required)**\n'
                        '`nickname` - The Member\'s Future Nickname **(Optional)**'))
            elif command == "removedefaultrole":
                await Message.admin(ctx, "**/removedefaultrole** command - Remove The Default Role on The Server", '**Syntax:** **/removedefaultrole**')
        else: await Message.error(ctx, "Error", "**You doesn't have permissions for executing this command**")

    @cog_ext.cog_slash(
        name="ban",
        description="Ban The Member on The Server",
        options=[
            create_option(
                name="member",
                description="The Member Who Will Be Banned",
                option_type=6,
                required=True
                )
            ])
    async def ban(self, ctx, member: discord.Member):
        """Ban The Member on The Server"""
        if ctx.author.guild_permissions.manage_messages:
            await member.ban(reason=None)
            await Message.admin(ctx, "The Member has been banned", f"**{member}** was banned")
        else: await Message.error(ctx, "Error", "**You doesn't have permissions for executing this command**")

    @cog_ext.cog_slash(
        name="defaultrole",
        description="Set The Default Role on The Server",
        options=[
            create_option(
                name="role",
                description="The Role Name",
                option_type=8,
                required=True
                )
            ])
    async def defaultrole(self, ctx, role):
        """Set The Default Role on The Server"""
        if ctx.author.guild_permissions.manage_messages:
            if Role().get_role(str(ctx.guild.id)) is None:
                Role().add(str(role.id), str(ctx.guild.id))
                await Message.admin(ctx, "Server Default Role has been set", "**Server Default Role** was set")
            else: await Message.admin(ctx, "Server Default Role already had been set", "The **Server Default Role** already was set")
        else: await Message.error(ctx, "Error", "**You doesn't have permissions for executing this command**")

    @cog_ext.cog_slash(
        name="giverole",
        description="Give The Role to The Member",
        options=[
            create_option(
                name="member",
                description="Member Who Will Received Role",
                option_type=6,
                required=True
                ),
            create_option(
                name="role",
                description="The Role Name",
                option_type=8,
                required=True
                )
            ])
    async def giverole(self, ctx, member: discord.Member, role):
        """Give The Role to The Member"""
        if ctx.author.guild_permissions.manage_messages:
            await member.add_roles(role)
            Message.admin(ctx, "A Role has been given to member", f"**The Role** has been given to **{member}**")
        else: await Message.error(ctx, "Error", "**You doesn't have permissions for executing this command**")

    @cog_ext.cog_slash(
        name="kick",
        description="Kick The Member from The Server",
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
            """Kick The Member from The Server"""
            await member.kick(reason=None)
            Message.admin(ctx, "The Member has been kicked", f"**{member}** was kicked")
        else: await Message.error(ctx, "Error", "**You doesn't have permissions for executing this command**")

    @cog_ext.cog_slash(
        name="nickname",
        description="Change The Nickname to The Member",
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
        """Change The Nickname to The Member"""
        if ctx.author.guild_permissions.manage_messages:
            await member.edit(nick=nickname)
            Message.admin(ctx, "The Member nickname has been changed", f"**{member}** nickname was changed")
        else: await Message.error(ctx, "Error", "**You doesn't have permissions for executing this command**")

    @cog_ext.cog_slash(
        name="removedefaultrole",
        description="Remove The Default Role on The Server"
        )
    async def removedefaultrole(self, ctx):
        """Remove The Default Role on The Server"""
        if ctx.author.guild_permissions.manage_messages:
            if Role().get_role(str(ctx.guild.id)) is not None:
                Role().delete(str(ctx.guild.id))
                Message.admin(ctx, "**Server Default Role** has been removed", "**Server Default Role** was removed")
            else: Message.admin(ctx, "Server Default Role hadn't been set", "**Server Default Role** wasn't set yet")
        else: await Message.error(ctx, "Error", "**You doesn't have permissions for executing this command**")


def setup(client):
    """Setup function"""
    client.add_cog(Admin(client))
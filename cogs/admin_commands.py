import discord
from discord import Embed, Colour
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

from database import Role


class AdminCommands(commands.Cog):

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
                await ctx.send(
                    embed=Embed(
                        title="**Admin Commands**",
                        description=(
                            ' - **/adminhelp** `command` - The List of Parzibot Admin Commands\n'
                            ' - **/ban** `member` - Ban The Member on The Server\n'
                            ' - **/defaultrole** `role` - Set The Default Role on The Server\n'
                            ' - **/giverole** `member` `role` - Give The Role to The Member\n'
                            ' - **/kick** `member` - Kick The Member from The Server\n'
                            ' - **/nickname** `member` `nickname` - Change The Nickname to The Member\n'
                            ' - **/removedefaultrole** - Remove The Default Role on The Server'
                            ),
                        color=Colour(0xd3d959)))
            elif command == "adminhelp":
                await ctx.send(
                    embed=Embed(
                        title="**/adminhelp** command - The List of Parzibot Admin Commands",
                        description=(
                            '**Syntax:** **/adminhelp** `command`\n'
                            '**Options:** `command` - The Help Message for Specific Admin Command **(Optional)**'
                        ),
                        color=Colour(0xd3d959)
                    )
                )
            elif command == "ban":
                await ctx.send(
                    embed=Embed(
                        title="**/ban** command - Ban The Member on The Server",
                        description=(
                            '**Syntax:** **/ban** `member`\n'
                            '**Options:** `member` - The Member Who Will Be Banned **(Required)**'
                        ),
                        color=Colour(0xd3d959)
                    )
                )
            elif command == "defaultrole":
                await ctx.send(
                    embed=Embed(
                        title="**/defaultrole** command - Set The Default Role on The Server",
                        description=(
                            '**Syntax:** **/defaultrole** `role`\n'
                            '**Options:** `role` - The Role Name **(Required)**'
                        ),
                        color=Colour(0xd3d959)
                    )
                )
            elif command == "giverole":
                await ctx.send(
                    embed=Embed(
                        title="**/giverole** command - Give The Role to The Member",
                        description=(
                            '**Syntax:** **/giverole** `member` `role`\n'
                            '**Options:**\n'
                            '`member` - Member Who Will Received Role **(Required)**\n'
                            '`role` - The Role Name **(Required)**'
                        ),
                        color=Colour(0xd3d959)
                    )
                )
            elif command == "kick":
                await ctx.send(
                    embed=Embed(
                        title="**/kick** command - Kick The Member from The Server",
                        description=(
                            '**Syntax:** **/kick** `member`\n'
                            '**Options:** `member` - The Member Who Will Be Kicked **(Required)**'
                        ),
                        color=Colour(0xd3d959)
                    )
                )
            elif command == "nickname":
                await ctx.send(
                    embed=Embed(
                        title="**/nickname** command - Change The Nickname to The Member",
                        description=(
                            '**Syntax:** **/nickname** `member` `nickname`\n'
                            '**Options:**\n'
                            '`member` - The Member to Whom We Will Change Nickname **(Required)**\n'
                            '`nickname` - The Member\'s Future Nickname **(Optional)**'
                        ),
                        color=Colour(0xd3d959)
                    )
                )
            elif command == "removedefaultrole":
                await ctx.send(
                    embed=Embed(
                        title="**/removedefaultrole** command - Remove The Default Role on The Server",
                        description=(
                            '**Syntax:** **/removedefaultrole**'
                        ),
                        color=Colour(0xd3d959)
                    )
                )
        else:
            await ctx.send(
                embed=Embed(
                    title="Error",
                    description="**You doesn't have permissions for executing this command**",
                    color=Colour(0xd95959)))

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
            await ctx.send(
                embed=Embed(
                    title=f"**{member}** has been banned",
                    color=Colour(0xd3d959)
                    )
                )
        else:
            await ctx.send(
                embed=Embed(
                    title="Error",
                    description="**You doesn't have permissions for executing this command**",
                    color=Colour(0xd95959)
                    )
                )

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
                await ctx.send(
                    embed=Embed(
                        title="**Server Default Role** has been set",
                        color=Colour(0xd3d959)
                        )
                    )
            else: 
                if Role().get_role(str(ctx.guild.id)) is None:
                    Role().add(role, str(ctx.guild.id))
                    await ctx.send(
                        embed=Embed(
                            title="**Server Default Role** already had been set",
                            color=Colour(0x59d9b9)
                            )
                        )
        else:
            await ctx.send(
                embed=Embed(
                    title="Error",
                    description="**You doesn't have permissions for executing this command**",
                    color=Colour(0xd95959)
                    )
                )

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
            await ctx.send(
                embed=Embed(
                    title=f"Role has been given to **{member}**",
                    color=Colour(0xd3d959)
                    )
                )
        else:
            await ctx.send(
                embed=Embed(
                    title="Error",
                    description="**You doesn't have permissions for executing this command**",
                    color=Colour(0xd95959)
                    )
                )

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
            await ctx.send(
                embed=Embed(
                    title=f"**{member}** has been kicked",
                    color=Colour(0xd3d959)
                    )
                )
        else:
            await ctx.send(
                embed=Embed(
                    title="Error",
                    description="**You doesn't have permissions for executing this command**",
                    color=Colour(0xd95959)
                    )
                )

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
            await ctx.send(
                embed=Embed(
                    title=f"**{member}** nickname has been changed",
                    color=Colour(0xd3d959)
                    )
                )
        else:
            await ctx.send(
                embed=Embed(
                    title="Error",
                    description="**You doesn't have permissions for executing this command**",
                    color=Colour(0xd95959)
                    )
                )

    @cog_ext.cog_slash(
        name="removedefaultrole",
        description="Remove The Default Role on The Server"
        )
    async def removedefaultrole(self, ctx):
        """Remove The Default Role on The Server"""
        if ctx.author.guild_permissions.manage_messages:
            if not Role().get_role(str(ctx.guild.id)) is None:
                Role().delete(str(ctx.guild.id))
                await ctx.send(
                    embed=Embed(
                        title="**Server Default Role** has been removed",
                        color=Colour(0xd3d959)
                        )
                    )
            else:
                Role().add(role, str(ctx.guild.id))
                await ctx.send(
                    embed=Embed(
                        title="**Server Default Role** already hadn't been set",
                        color=Colour(0x59d9b9)
                        )
                    )
        else:
            await ctx.send(
                embed=Embed(
                    title="Error",
                    description="**You doesn't have permissions for executing this command**",
                    color=Colour(0xd95959)
                    )
                )


def setup(client):
    """Setup function"""
    client.add_cog(AdminCommands(client))

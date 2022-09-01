import discord
from discord import app_commands, Embed, Colour
from discord.ext import commands
from discord.ext.commands import ColourConverter

from message import Message

class AdminCommands(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="adminhelp", description="The list of Parzibot admin commands")
    async def adminhelp(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if interaction.user.guild_permissions.manage_messages:
            await Message.admin_msg(ctx, "Parzibot // Admin Commands", (
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
        else: await Message.error_msg(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")

    @app_commands.command(name="announce", description="Make announce message in current Text Channel")
    @app_commands.describe(message="Text of announce message")
    async def announce(self, interaction: discord.Interaction, message: str):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if interaction.user.guild_permissions.manage_messages:
            await Message.admin_msg(ctx, "Parzibot // Announce", message.replace("\\n", "\n"))
        else: await Message.error_msg(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")

    @app_commands.command(name="ban", description="Ban member on your Server")
    @app_commands.describe(member="Member who will be banned")
    async def ban(self, interaction: discord.Interaction, member: discord.Member):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if interaction.user.guild_permissions.manage_messages:
            await member.ban(reason=None)
            await Message.admin_msg(ctx, "Parzibot // Ban", f"**{member}** has been banned")
        else: await Message.error_msg(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")

    @app_commands.command(name="kick", description="Kick member on your Server")
    @app_commands.describe(member="Member who will be kicked")
    async def kick(self, interaction: discord.Interaction, member: discord.Member):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if interaction.user.guild_permissions.manage_messages:
            await member.kick(reason=None)
            await Message.admin_msg(ctx, "Parzibot // Kick", f"**{member}** has been kicked")
        else: await Message.error_msg(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")

    @app_commands.command(name="role", description="Create role with default role permissions on Server")
    @app_commands.describe(name="Name of future role", color="Role color code")
    async def role(self, interaction: discord.Interaction, name: str, color: str):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if interaction.user.guild_permissions.manage_messages:
            if Role().get_role(str(ctx.guild.id)) is not None:
                await interaction.guild.create_role(name=name, 
                    colour=ColourConverter.convert(ctx, color),
                    permissions=discord.utils.get(interaction.user.guild.roles, id=int(Role().get_role(interaction.user.guild.id))).permissions)
                await Message.admin_msg(ctx, "Parzibot // Role", f"**{name} Role** added on Server")
            else: await Message.admin_msg(ctx, "Parzibot // Default Role Hadn't Set", "**Server Default Role** should be set for using this command")
        else: await Message.error_msg(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")

    @app_commands.command(name="giverole", description="Give role to Member on Server")
    @app_commands.describe(member="Member who will receive Role", role="Role that will be received by Member")
    async def giverole(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if interaction.user.guild_permissions.manage_messages:
            await member.add_roles(role)
            await Message.admin_msg(ctx, "Parzibot // Give Role", f"**{role.name} Role** has been given to **{member}**")
        else: await Message.error_msg(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")

    @app_commands.command(name="nickname", description="Change nickname to Member on Server")
    @app_commands.describe(member="Member to whom we will change nickname", nickname="Member's future nickname")
    async def nickname(self, interaction: discord.Interaction, member: discord.Member, *, nickname: str=None):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if interaction.user.guild_permissions.manage_messages:
            await member.edit(nick=nickname)
            await Message.admin_msg(ctx, "Parzibot // Nickname Changed", f"**{member}**'s nickname has been changed")
        else: await Message.error_msg(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")

    # @cog_ext.cog_slash(
    #     name="defaultrole",
    #     description="Set default role what will be giving to new members of Server",
    #     options=[
    #         create_option(
    #             name="role",
    #             description="Role that will be giving",
    #             option_type=8,
    #             required=True)
    #         ])
    # async def defaultrole(self, ctx, role):
    #     if ctx.author.guild_permissions.manage_messages:
    #         if Role().get_role(str(ctx.guild.id)) is None:
    #             Role().add(str(role.id), str(ctx.guild.id))
    #             await Message.admin(ctx, "Parzibot // Default Role Set", "**Server Default Role** has been set")
    #         else: await Message.admin(ctx, "Parzibot // Default Role Already Set", "**Server Default Role** already had been set")
    #     else: await Message.error(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")

    # @cog_ext.cog_slash(name="defaultroleremove", description="Remove default role what will be giving to new members of Server")
    # async def removedefaultrole(self, ctx):
    #     if ctx.author.guild_permissions.manage_messages:
    #         if Role().get_role(str(ctx.guild.id)) is not None:
    #             Role().delete(str(ctx.guild.id))
    #             await Message.admin(ctx, "Parzibot // Default Role Removed", "**Server Default Role** was removed")
    #         else: await Message.admin(ctx, "Parzibot // Default Role Hadn't Set", "**Server Default Role** should be set for using this command")
    #     else: await Message.error(ctx, "Parzibot // Error", "You doesn't have permissions for executing this command")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ErrorHandler(bot))

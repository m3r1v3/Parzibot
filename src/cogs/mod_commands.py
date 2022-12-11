import os

import discord
from discord import app_commands, Colour
from discord.ext import commands

from message import Message
from database import Role


class ModCommands(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="modhelp", description=Message.get_mod_msg("descriptions", "help"))
    async def modhelp(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if interaction.user.guild_permissions.manage_messages:
            await Message.mod_msg(ctx, Message.get_mod_msg("titles", "help"), Message.get_mod_msg("messages", "help"))
        else: await Message.error_msg(ctx, Message.get_error_msg("titles", "error"), Message.get_error_msg("messages", "error-mod"))

    @app_commands.command(name="announce", description=Message.get_mod_msg("descriptions", "announce"))
    @app_commands.describe(message=Message.get_mod_msg("descriptions", "announce-message"))
    async def announce(self, interaction: discord.Interaction, message: str):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if interaction.user.guild_permissions.manage_messages:
            await Message.mod_msg(ctx, Message.get_mod_msg("titles", "announce"), message.replace("\\n", "\n"))
        else: await Message.error_msg(ctx, Message.get_error_msg("titles", "error"), Message.get_error_msg("messages", "error-mod"))

    @app_commands.command(name="ban", description=Message.get_mod_msg("descriptions", "ban"))
    @app_commands.describe(member=Message.get_mod_msg("descriptions", "ban-member"))
    async def ban(self, interaction: discord.Interaction, member: discord.Member):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if interaction.user.guild_permissions.manage_messages:
            await member.ban(reason=None)
            await Message.mod_msg(ctx, Message.get_mod_msg("titles", "ban"), Message.get_mod_msg("messages", "ban").format(member=member))
        else: await Message.error_msg(ctx, Message.get_error_msg("titles", "error"), Message.get_error_msg("messages", "error-mod"))

    @app_commands.command(name="kick", description=Message.get_mod_msg("descriptions", "kick"))
    @app_commands.describe(member=Message.get_mod_msg("descriptions", "kick-member"))
    async def kick(self, interaction: discord.Interaction, member: discord.Member):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if interaction.user.guild_permissions.manage_messages:
            await member.kick(reason=None)
            await Message.mod_msg(ctx, Message.get_mod_msg("titles", "kick"), Message.get_mod_msg("messages", "kick").format(member=member))
        else: await Message.error_msg(ctx, Message.get_error_msg("titles", "error"), Message.get_error_msg("messages", "error-mod"))

    @app_commands.command(name="role", description=Message.get_mod_msg("descriptions", "role"))
    @app_commands.describe(name=Message.get_mod_msg("descriptions", "role-name"), color=Message.get_mod_msg("descriptions", "role-color"))
    async def role(self, interaction: discord.Interaction, name: str, color: str):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if interaction.user.guild_permissions.manage_messages:
            if Role().get_role(str(ctx.guild.id)) is not None:
                await interaction.guild.create_role(
                    name=name, colour=Colour(int(color.replace("#", ""), 16)), 
                    permissions=discord.utils.get(interaction.user.guild.roles, id=int(
                    Role().get_role(interaction.user.guild.id))).permissions)
                await Message.mod_msg(ctx, Message.get_mod_msg("titles", "role"), Message.get_mod_msg("messages", "role")[0].format(name=name))
            else: await Message.mod_msg(ctx, Message.get_mod_msg("titles", "role"), Message.get_mod_msg("messages", "role")[1])
        else: await Message.error_msg(ctx, Message.get_error_msg("titles", "error"), Message.get_error_msg("messages", "error-mod"))

    @app_commands.command(name="giverole", description=Message.get_mod_msg("descriptions", "giverole"))
    @app_commands.describe(member=Message.get_mod_msg("descriptions", "giverole-member"), role=Message.get_mod_msg("descriptions", "giverole-role"))
    async def giverole(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if interaction.user.guild_permissions.manage_messages:
            await member.add_roles(role)
            await Message.mod_msg(ctx, Message.get_mod_msg("titles", "giverole"), Message.get_mod_msg("messages", "role").format(role=role.name, member=member))
        else: await Message.error_msg(ctx, Message.get_error_msg("titles", "error"), Message.get_error_msg("messages", "error-mod"))

    @app_commands.command(name="nickname", description=Message.get_mod_msg("descriptions", "nickname"))
    @app_commands.describe(member=Message.get_mod_msg("descriptions", "nickname-member"), nickname=Message.get_mod_msg("descriptions", "nickname-nickname"))
    async def nickname(self, interaction: discord.Interaction, member: discord.Member, *, nickname: str = None):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if interaction.user.guild_permissions.manage_messages:
            await member.edit(nick=nickname)
            await Message.mod_msg(ctx, Message.get_mod_msg("titles", "nickname"), Message.get_mod_msg("messages", "nickname").format(member=member))
        else: await Message.error_msg(ctx, Message.get_error_msg("titles", "error"), Message.get_error_msg("messages", "error-mod"))

    @app_commands.command(name="defaultrole", description=Message.get_mod_msg("descriptions", "defaultrole"))
    @app_commands.describe(role=Message.get_mod_msg("descriptions", "defaultrole-role"))
    async def defaultrole(self, interaction: discord.Interaction, role: discord.Role):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if interaction.user.guild_permissions.manage_messages:
            if Role().get_role(str(interaction.guild.id)) is None:
                Role().add(str(role.id), str(interaction.guild.id))
                await Message.mod_msg(ctx, Message.get_mod_msg("titles", "defaultrole"), Message.get_mod_msg("messages", "defaultrole")[0].format(role=role.name))
            else: await Message.mod_msg(ctx, Message.get_mod_msg("titles", "defaultrole"), Message.get_mod_msg("messages", "defaultrole")[1])
        else: await Message.error_msg(ctx, Message.get_error_msg("titles", "error"), Message.get_error_msg("messages", "error-mod"))

    @app_commands.command(name="defaultroleremove", description=Message.get_mod_msg("descriptions", "defaultroleremove"))
    async def defaultroleremove(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if interaction.user.guild_permissions.manage_messages:
            if Role().get_role(str(interaction.guild.id)) is not None:
                Role().delete(str(interaction.guild.id))
                await Message.mod_msg(ctx, Message.get_mod_msg("titles", "defaultroleremove"), Message.get_mod_msg("messages", "defaultroleremove")[0])
            else: await Message.mod_msg(ctx, Message.get_mod_msg("titles", "defaultroleremove"), Message.get_mod_msg("messages", "defaultroleremove")[1])
        else: await Message.error_msg(ctx, Message.get_error_msg("titles", "error"), Message.get_error_msg("messages", "error-mod"))


async def setup(bot: commands.Bot) -> None:
    if int(os.environ.get('MOD_COMMANDS')): await bot.add_cog(ModCommands(bot))

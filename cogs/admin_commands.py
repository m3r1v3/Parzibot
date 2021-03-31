import discord
from discord.ext import commands
from sqlalchemy.orm.exc import UnmappedInstanceError

from cogs.language_commands import get_language
from database import User, Role


class AdminCommands(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @commands.command(pass_context=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick user"""
        if ctx.message.author.guild_permissions.administrator:
            User().check_user(ctx.message.author.name, str(ctx.guild.id))

            try:
                User().delete(member.display_name, str(ctx.guild.id))
            except UnmappedInstanceError:
                pass

            await member.kick(reason=reason)

            if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
                await ctx.send(f'{member.mention} был выгнан')
            else:
                await ctx.send(f'Kicked {member.mention}')
        else:
            if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
                await ctx.send("У вас нет прав для использования данной команды")
            else:
                await ctx.send("You don't have permissions for using this command")

    @commands.command(pass_context=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban user"""
        if ctx.message.author.guild_permissions.administrator:
            User().check_user(ctx.message.author.name, str(ctx.guild.id))

            try:
                User().delete(member.display_name, str(ctx.guild.id))
            except UnmappedInstanceError:
                pass

            await member.ban(reason=reason)

            if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
                await ctx.send(f'{member.mention} забанен')
            else:
                await ctx.send(f'Banned {member.mention}')
        else:
            if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
                await ctx.send("У вас нет прав для использования данной команды")
            else:
                await ctx.send("You don't have permissions for using this command")

    @commands.command(pass_context=True)
    async def nickname(self, ctx, member: discord.Member, *, nickname=None):
        if ctx.message.author.guild_permissions.administrator:
            await member.edit(nick=nickname)
            if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
                await ctx.send(f'Ник был изменен для {member.mention}')
            else:
                await ctx.send(f'Nickname was changed for {member.mention}')
        else:
            if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
                await ctx.send("У вас нет прав для использования данной команды")
            else:
                await ctx.send("You don't have permissions for using this command")

    @commands.command()
    async def set_role(self, ctx, role):
        """Set default role for server"""
        if ctx.message.author.guild_permissions.administrator:
            Role().add(role, str(ctx.guild.id))

            if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
                await ctx.send("Стандартная роль для сервера установлена")
            else:
                await ctx.send("Default role for server installed")
        else:
            if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
                await ctx.send("У вас нет прав для использования данной команды")
            else:
                await ctx.send("You don't have permissions for using this command")

    @commands.command()
    async def remove_role(self, ctx, role):
        """Remove default role for server"""
        if ctx.message.author.guild_permissions.administrator:
            Role().delete(role, str(ctx.guild.id))

            if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
                await ctx.send("Стандартная роль для сервера убрана")
            else:
                await ctx.send("Default role for server removed")
        else:
            if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
                await ctx.send("У вас нет прав для использования данной команды")
            else:
                await ctx.send("You don't have permissions for using this command")

    @commands.command()
    async def give_role(self, ctx, member: discord.Member, role_id: str):
        """Give role to member"""
        if ctx.message.author.guild_permissions.administrator:
            role = discord.utils.get(member.guild.roles, id=int(role_id))
            await member.add_roles(role)

            if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
                await ctx.send("Роль была дана {member}")
            else:
                await ctx.send(f"Role was given to {member}")
        else:
            if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
                await ctx.send("У вас нет прав для использования данной команды")
            else:
                await ctx.send("You don't have permissions for using this command")


def setup(client):
    """Setup function"""
    client.add_cog(AdminCommands(client))

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from sqlalchemy.orm.exc import UnmappedInstanceError

from database import Role


class AdminCommands(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @commands.command(pass_context=True)
    @has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick user"""
        await member.kick(reason=reason)
        await ctx.send(f'Kicked **{member.mention}**.')

    @commands.command(pass_context=True)
    @has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban user"""
        await member.ban(reason=reason)
        await ctx.send(f'Banned **{member.mention}**.')

    @commands.command(pass_context=True)
    @has_permissions(administrator=True)
    async def nickname(self, ctx, member: discord.Member, *, nickname=None):
        await member.edit(nick=nickname)
        await ctx.send(f'Nickname was changed for **{member.mention}**.')

    @commands.command(pass_context=True)
    @has_permissions(administrator=True)
    async def set_role(self, ctx, role):
        """Set default role for server"""
        Role().add(role, str(ctx.guild.id))
        await ctx.send("Default role for server was installed.")

    @commands.command(pass_context=True)
    @has_permissions(administrator=True)
    async def remove_role(self, ctx, role):
        """Remove default role for server"""
        Role().delete(role, str(ctx.guild.id))
        await ctx.send("Default role for server removed.")

    @commands.command(pass_context=True)
    @has_permissions(administrator=True)
    async def give_role(self, ctx, member: discord.Member, role_id: str):
        """Give role to member"""
        role = discord.utils.get(member.guild.roles, id=int(role_id))
        await member.add_roles(role)
        await ctx.send(f"Role was given to **{member}**.")


def setup(client):
    """Setup function"""
    client.add_cog(AdminCommands(client))

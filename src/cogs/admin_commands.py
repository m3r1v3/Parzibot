import discord
from discord import app_commands, Embed, Colour
from discord.ext import commands

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

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ErrorHandler(bot))

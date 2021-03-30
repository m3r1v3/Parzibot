import random
import datetime

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

from cogs.language import get_language
from database import User, Role

def get_random_color():
    """Random generate color"""
    return random.choice(['white', 'black'])

class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="ping", description="User ping")
    async def ping(self, ctx):
        await ctx.send(f'Ping: {round(self.client.latency * 1000)}ms')

    @cog_ext.cog_slash(name="8ball", description="8ball game")
    async def _8ball(self, ctx, *, question):
        """8ball game"""
        responses = ["It is certain...",
                "It is decidedly so...",
                "Without a doubt...",
                "Yes — definitely...",
                "You may rely on it...",
                "As I see it, yes...",
                "Most likely...",
                "Outlook good...",
                "Signs point to yes...",
                "Yes...",
                "Reply hazy, try again...",
                "Ask again later...",
                "Better not tell you now...",
                "Cannot predict now...",
                "Concentrate and ask again...",
                "Don’t count on it...",
                "My reply is no...",
                "My sources say no...",
                "Outlook not so good...",
                "Very doubtful..."]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @cog_ext.cog_slash(name="clear", description="Clear chat")
    async def clear(self, ctx, amount="5"):
        """Clear chat"""
        await ctx.channel.purge(limit=int(amount)+1)
        await ctx.send(f"Cleared {amount} messages")

    @cog_ext.cog_slash(name="users", description="Users of chat")
    async def users(self, ctx):
        """Return bot users"""
        channel = ctx.channel
        members = "".join(f'\t*{str(member)}*\n' for member in channel.members)
        await ctx.send(f'**Channel members:**\n{str(members)}')

    @cog_ext.cog_slash(name="wbg", description="Choice random game")
    async def what_by_game(self, ctx):
        """Function for choice game"""
        responses = ["Fortnite", "CS:GO", "GTAV", "GTA:SA",
            "PUBG", "SAR", "Rust", "RDR2", "Assassin's creed",
            "Call of Duty:Warzone", "Minecraft"]
        await ctx.send(f'Play to {random.choice(responses)}')

    @cog_ext.cog_slash(name="gg", description="Choice you random game")
    async def good_game(self, ctx, *, games):
        """Random choice game"""
        await ctx.send(f'Play to {random.choice(games.split())}')

    @cog_ext.cog_slash(name="wb", description="White/Black Game")
    async def white_black(self, ctx, question):
        """White/Black game"""
        if question == get_random_color():
            await ctx.send(f'You winner')
        else:
            await ctx.send(f'You lose')

    @cog_ext.cog_slash(name="help", description="Help command")
    async def help(self, ctx):
        """Return all commands"""
        await ctx.send(f'Bot commands:'
            f'\n\t - $8ball `question` - Ball of predictions'
            f'\n\t - $about - About bot'
            f'\n\t - $clear `Qty` - Clear chat'
            f'\n\t - $gg `[game1 game2 ... gameN]` - Randomly chooses a game'
            f'\n\t - $help - Bot commands'
            f'\n\t - $lang `(EN/RU)` - Set language'
            f'\n\t - $nickname `@nickname` `new_nick` - Edit nickname'
            f'\n\t - $ping - You ping'
            f'\n\t - $users - Bot users'
            f'\n\t - $wb `(white/black)` - Game Black/White'
            f'\n\t - $wbg - Advice on what to play'
            f'\nFor admins:'
            f'||\n\t - $ban `@nickname` - Ban user||'
            f'||\n\t - $give_role `@nickname` `role_id` - Give role||'
            f'||\n\t - $kick `@user` - Kick user||'
            f'||\n\t - $set_role `role_id` - Set default role||'
            f'||\n\t - $remove_role `role_id` - Remove default role||')

    @cog_ext.cog_slash(name="about", description="About command")
    async def about(self, ctx):
        """Return about bot"""
        await ctx.send(f"Parzibot is free open source project, created by **@merive_#6187**.\n"
            f"All source code is on [GitHub](https://github.com/merive/Parzibot)\n"
            f"Parzibot, {datetime.datetime.now().year}")

def setup(client):
    """Setup function"""
    client.add_cog(Slash(client))

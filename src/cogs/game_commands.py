import random
import os

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

from message import Message


class GameCommands(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="8ball", description=Message.get_game_msg("descriptions", "8ball"))
    @app_commands.describe(question=Message.get_game_msg("descriptions", "8ball-question"))
    async def _8ball(self, interaction: discord.Interaction, *, question: str):
        ctx: commands.Context = await self.bot.get_context(interaction)
        responses = Message.get_game_msg("messages", "8ball-responses")
        await Message.games_msg(ctx, Message.get_game_msg("titles", "8ball"),
            Message.get_game_msg("messages", "8ball").format(question=question, answer=random.choice(Message.get_game_msg("messages", "8ball-responses"))))

    @app_commands.command(name="coin", description=Message.get_game_msg("descriptions", "coin"))
    async def coin(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        await Message.games_msg(ctx, Message.get_game_msg("titles", "coin"), Message.get_game_msg("messages", "coin").format(side=random.choice(['Head', 'Tail'])))

    @app_commands.command(name="dice", description=Message.get_game_msg("descriptions", "dice"))
    @app_commands.describe(value=Message.get_game_msg("descriptions", "dice-value"))
    async def dice(self, interaction: discord.Interaction, value: int):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if 1 <= value <= 12:
            v1, v2 = random.randint(1, 6), random.randint(1, 6)
            if v1 + v2 == value:
                await Message.games_msg(ctx, Message.get_game_msg("titles", "dice"), Message.get_game_msg("messages", "dice-responses")[0].format(v1=v1, v2=v2))
            elif v1 == value or v2 == value:
                await Message.games_msg(ctx, Message.get_game_msg("titles", "dice"), Message.get_game_msg("messages", "dice-responses")[1].format(v1=v1, v2=v2))
            else: await Message.games_msg(ctx, Message.get_game_msg("titles", "dice"), Message.get_game_msg("messages", "dice-responses")[2].format(v1=v1, v2=v2))
        else: await Message.games_msg(ctx, Message.get_game_msg("titles", "dice"), Message.get_game_msg("messages", "dice-responses")[3].format(v1=v1, v2=v2))

    @app_commands.command(name="gamehelp", description=Message.get_game_msg("descriptions", "help"))
    async def help(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        await Message.games_msg(ctx, Message.get_game_msg("titles", "help"), Message.get_game_msg("messages", "help"))

    @app_commands.command(name="gg", description=Message.get_game_msg("descriptions", "gg"))
    async def gg(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        await Message.games_msg(ctx, Message.get_game_msg("titles", "gg"), 
            Message.get_game_msg("messages", "gg").format(game=random.choice(Message.get_game_msg("messages", "gg-responses"))))

    @app_commands.command(name="whiteblack", description=Message.get_game_msg("descriptions", "whiteblack"))
    @app_commands.describe(color=Message.get_game_msg("descriptions", "whiteblack-color"))
    @app_commands.choices(color=[
        Choice(name="White", value="white"),
        Choice(name="Black", value="black")
    ])
    async def whiteblack(self, interaction: discord.Interaction, color: str):
        ctx: commands.Context = await self.bot.get_context(interaction)
        result = random.choice(["white", "black"])
        if color == result: await Message.games_msg(ctx, Message.get_game_msg("titles", "whiteblack"), Message.get_game_msg("messages", "whiteblack")[0].format(color=result))
        else: await Message.games_msg(ctx, Message.get_game_msg("titles", "whiteblack"), Message.get_game_msg("messages", "whiteblack")[1].format(color=result))


async def setup(bot: commands.Bot) -> None:
    if int(os.environ.get('GAME_COMMANDS')): await bot.add_cog(GameCommands(bot))

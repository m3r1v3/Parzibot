import random

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

from message import Message


class GameCommands(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="8ball", description="The Ball of Predictions")
    @app_commands.describe(question="Your question to The Ball")
    async def _8ball(self, interaction: discord.Interaction, *, question: str):
        ctx: commands.Context = await self.bot.get_context(interaction)
        responses = [
            "It is certain...", "It is decidedly so...",
            "Without a doubt...", "Yes — definitely...",
            "You may rely on it...", "As I see it, yes...",
            "Most likely...", "Outlook good...",
            "Signs point to yes...", "Yes...",
            "Reply hazy, try again...", "Ask again later...",
            "Better not tell you now...", "Cannot predict now...",
            "Concentrate and ask again...", "Don’t count on it...",
            "My reply is no...", "My sources say no...",
            "Outlook not so good...", "Very doubtful..."]
        await Message.games_msg(ctx, "Parzibot // The Ball of Predictions",
                                f"Question - **{question}**\nAnswer - **{random.choice(responses)}**")

    @app_commands.command(name="coin", description="The Heads or Tails Game")
    async def coin(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        await Message.games_msg(ctx, "Parzibot // Heads or Tails", f"**{random.choice(['Head', 'Tail'])}** has fell")

    @app_commands.command(name="dice", description="The Dice Game")
    @app_commands.describe(value="The value what you're predicting (from 1 to 12)")
    async def dice(self, interaction: discord.Interaction, value: int):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if 1 <= value <= 12:
            v1, v2 = random.randint(1, 6), random.randint(1, 6)
            if v1 + v2 == value:
                await Message.games_msg(ctx, "Parzibot // The Dice",
                                        f"You won :D. The sum of values is **{v1 + v2}**. The values of dice is **{v1}** and **{v2}**")
            elif v1 == value or v2 == value:
                await Message.games_msg(ctx, "Parzibot // The Dice",
                                        f"You guess value one of the dice :D The values of dice is **{v1}** and **{v2}**")
            else:
                await Message.games_msg(ctx, "Parzibot // The Dice",
                                        f"You lose :( The values of dice is **{v1}** and **{v2}**")
        else:
            await Message.games_msg(ctx, "Parzibot // The Dice",
                                    f"You're predicting wrong value. The value should be between 2 and 12")

    @app_commands.command(name="gamehelp", description="The list of Parzibot game commands")
    async def help(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        await Message.games_msg(ctx, "Parzibot // Game Commands", (
            " • **/8ball** `question` - The Ball of Predictions\n"
            " • **/coin** - The Heads or Tails Game\n"
            " • **/dice** `value` - The Dice Game\n"
            " • **/gamehelp** - The list of Parzibot game commands\n"
            " • **/getgame** - Advises to play a random game\n"
            " • **/whiteblack** `color` - The White/Black Game"))

    @app_commands.command(name="getgame", description="Advises to play a random game")
    async def getgame(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        responses = [
            "Animal Crossing: New Horizons", "Apex Legends",
            "Assasin\"s Creed Valhalla", "CS:GO",
            "Call of Duty: Warzone", "Control",
            "Cyberpunk 2077", "Dead by Daylight",
            "Dota 2", "Fall Guys",
            "Fallout 76", "Fortnite",
            "Forza Horizon 4", "GTA V",
            "Genshin Impact", "League of Legends",
            "Minecraft", "Overwatch",
            "PUBG", "RDR 2",
            "Rainbow Six: Siege", "Rocket League",
            "Super Animal Royale", "Terraria",
            "The Elder Scrolls V: Skyrim", "Valorant"]
        await Message.games_msg(ctx, "Parzibot // Game by Parzibot",
                                f"I advise you to play **{random.choice(responses)}**")

    @app_commands.command(name="whiteblack", description="The White or Black Game")
    @app_commands.describe(color="The hidden color (White or Black)")
    @app_commands.choices(color=[
        Choice(name="White", value="white"),
        Choice(name="Black", value="black")
    ])
    async def white_black(self, interaction: discord.Interaction, color: str):
        ctx: commands.Context = await self.bot.get_context(interaction)
        result = random.choice(["white", "black"])
        if color == result:
            await Message.games_msg(ctx, "Parzibot // White or Black Game", f"You won :D Right color is `{result}`")
        else:
            await Message.games_msg(ctx, "You lose :(", f"Right color is `{result}`")


async def setup(bot: commands.Bot) -> None:
    if int(os.environ.get('GAME_COMMANDS')): await bot.add_cog(GameCommands(bot))

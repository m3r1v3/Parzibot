import datetime
import random
import discord

from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

from message import Message


class GameCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="8ball",
        description="The Ball of Predictions",
        options=[
            create_option(
                name="question",
                description="Your question to The Ball",
                option_type=3,
                required=True)
            ])
    async def _8ball(self, ctx, *, question: str):
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
            "Outlook not so good...", "Very doubtful..."
            ]
        await Message.games(ctx, f"Question: `{question}`", f"**Answer:** `{random.choice(responses)}`")

    @cog_ext.cog_slash(name="coin", description="The Heads or Tails Game")
    async def coin(self, ctx):
        await Message.games(ctx, "Heads or Tails", f"{random.choice(["Head", "Tail"])} has fell")

    @cog_ext.cog_slash(
        name="dice",
        description="The Dice Game",
        options=[
            create_option(
                name="value",
                description="The value what you're predicting (from 2 to 12)",
                option_type=4,
                required=True)
            ])
    async def dice(self, ctx, value):
        if value > 1 or value <= 12:
            v1, v2 = random.randint(1, 7), random.randint(1, 7)
            if v1 + v2 == value: await Message.games(ctx, "You won :D", f"The sum of values is **{v1 + v2}**. The values of dice is **{v1}** and **{v2}**")
            elif v1 == value or v2 == value:
                await Message.games(ctx, "You guess value one of the dice :D", (
                    f"The values one of dice is **{v1 if v1 == value else v2}**."
                    f" The values of dice is **{v1}** and **{v2}**"))
            else: await Message.games(ctx, "You lose :(", f"The values of dice is **{v1}** and **{v2}**")
        else: await Message.games(ctx, "You're predicting wrong value", f"The values should be between 2 and 12")

    @cog_ext.cog_slash(name="gamehelp", description="The list of Parzibot game commands")
    async def help(self, ctx):
        await Message.games(ctx, "Parzibot // Game Commands", (
            " • **/8ball** `question` - The Ball of Predictions\n"
            " • **/coin** - The Heads or Tails Game\n"
            " • **/dice** `value` - The Dice Game\n"
            " • **/gamehelp** - The list of Parzibot game commands\n"
            " • **/getgame** - Advises to play a random game\n"
            " • **/whiteblack** `color` - The White/Black Game"))

    @cog_ext.cog_slash(name="getgame", description="Advises to play a random game")
    async def getgame(self, ctx):
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
            "The Elder Scrolls V: Skyrim", "Valorant"
            ]
        await Message.games(ctx, "Special game by Parzibot", f"I advise you to play **{random.choice(responses)}**")

    @cog_ext.cog_slash(
        name="whiteblack",
        description="The White/Black Game",
        options=[
            create_option(
                name="color",
                description="The hidden color (White or Black)",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="White", value="white"),
                    create_choice(name="Black", value="black")
                ])
            ])
    async def white_black(self, ctx, color: str):
        result = random.choice(["white", "black"])
        if color == result: await Message.games(ctx, "You won :D", f"Right color is `{result}`")
        else: await Message.games(ctx, "You lose :(", f"Right color is `{result}`")


def setup(client):
    client.add_cog(GameCommands(client))
import datetime
import random
import discord

from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

from message import Message


class Games(commands.Cog):

    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(
        name="8ball",
        description="The Ball of Predictions",
        options=[
            create_option(
                name="question",
                description="Your Question for The Ball of Predictions",
                option_type=3,
                required=True)
            ])
    async def _8ball(self, ctx, *, question: str):
        """The Ball of Predictions"""
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

    @cog_ext.cog_slash(
        name="dice",
        description="The Game of Dice",
        options=[
            create_option(
                name="value",
                description="The Value What You're Predicting",
                option_type=4,
                required=True)
            ])
    async def dice(self, ctx, value):
        """Game of Dice"""
        v1, v2 = random.randint(1, 6), random.randint(1, 6)
        if v1 + v2 == value: await Message.msg(ctx, "You won :D", f"The sum of values is **{v1 + v2}**. The values of dice is **{v1}** and **{v2}**")
        elif v1 == value or v2 == value:
            await Message.games(ctx, "You guess value one of the dice :D", (
                f"The values one of dice is **{v1 if v1 == value else v2}**."
                f" The values of dice is **{v1}** and **{v2}**"))
        else: await Message.error(ctx, "You lose :(", f"The values of dice is **{v1}** and **{v2}**")

    @cog_ext.cog_slash(
        name="gamehelp",
        description="The List of Parzibot Game Commands",
        options=[
            create_option(
                name="command",
                description="The Help Message for Specific Game Command",
                option_type=3,
                required=False,
                choices=[
                    create_choice(name="8ball", value="8ball"),
                    create_choice(name="dice", value="dice"),
                    create_choice(name="getgame", value="getgame"),
                    create_choice(name="gamehelp", value="gamehelp"),
                    create_choice(name="whiteblack", value="whiteblack")
                ])
            ])
    async def help(self, ctx, command=None):
        """The List of Parzibot Commands"""
        if command is None:
            await Message.games(ctx, "Game Commands", (
                " • **/8ball** `question` - The Ball of Predictions\n"
                " • **/dice** `value` - The Game of Dice\n"
                " • **/gamehelp** `command` - The List of Parzibot Game Commands\n"
                " • **/getgame** - Choice random game from our list\n"
                " • **/whiteblack** `color` - The White/Black Game"))
        elif command == "8ball":
            await Message.games(ctx, "**/8ball** command - The Ball of Predictions", (
                "**Syntax:** **/8ball** `question`\n"
                "**Options:** `question` - Your Question for The Ball of Predictions **(Required)**"))
        elif command == "dice":
            await Message.games(ctx, "**/dice** command - The Game of Dice", (
                "**Syntax:** **/dice** `value`\n"
                "**Options:** `value` - The Value What You\"re Predicting **(Required)**\n"
                "**Rules:** If you guess sum of dice values - you won, "
                "if you guess one of the dice value - it\"s a draw, else you lose"))
        elif command == "gamehelp":
            await Message.games(ctx, "**/gamehelp** command - The List of Parzibot Game Commands", (
                "**Syntax:** **/gamehelp** `command`\n"
                "**Options:** `command` - The Help Message for Specific Game Command **(Optional)**"))
        elif command == "getgame":
            await Message.games(ctx, "**/getgame** command - Choice Random Game from Our List", "**Syntax:** **/getgame**")
        elif command == "whiteblack":
            await Message.games(ctx, "**/whiteblack** command - The White/Black Game", (
                "**Syntax:** **/whiteblack** `color`\n"
                "**Options:** `color` - The Hidden Color (White or Black) **(Required)**\n"))

    @cog_ext.cog_slash(name="getgame", description="Choice Random Game from Our List")
    async def getgame(self, ctx):
        """Choice Random Game from Our List"""
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
                description="The Hidden Color (White or Black)",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="White", value="white"),
                    create_choice(name="Black", value="black")
                ])
            ])
    async def white_black(self, ctx, color: str):
        """The White/Black Game"""
        result = random.choice(["white", "black"])
        if color == result: await Message.games(ctx, "You won :D", f"Right color is `{result}`")
        else: await Message.games(ctx, "You lose :(", f"Right color is `{result}`")


def setup(client):
    """Setup function"""
    client.add_cog(Games(client))
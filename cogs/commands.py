import datetime
import random
import discord

from discord import Embed, Colour
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice


def get_random_color():
    """Return random color (white or black string)"""
    return random.choice(["white", "black"])


class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @staticmethod
    def get_embed(title: str, description: str):
        return Embed(title=title, description=description, color=Colour(0x68FFD9)).set_thumbnail(url="attachment://Parzibot.png")

    @staticmethod
    def get_error_embed(title: str, description: str):
        return Embed(title=title, description=description, color=Colour(0xff6868)).set_thumbnail(url="attachment://ParzibotError.png")

    @staticmethod
    async def msg(ctx, title: str, message: str):
        await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
            embed=Commands.get_embed(title, message))

    @staticmethod
    async def error(ctx, title: str, message: str):
        await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"),
            embed=Commands.get_error_embed(title, message))

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
        await Commands.msg(ctx, f"Question: `{question}`", f"**Answer:** `{random.choice(responses)}`")

    @cog_ext.cog_slash(
        name="about",
        description="Information About Parzibot"
        )
    async def about(self, ctx):
        """Information About Parzibot"""
        await Commands.msg(ctx, "About Parzibot", (
            f"**Parzibot** is free open-source project, created by **merive_**\n"
            f"You can find more information on [Parzibot Website](https://merive.herokuapp.com/Parzibot)\n"
            f"**Parzibot**, {datetime.datetime.now().year}"
            ))

    @cog_ext.cog_slash(
        name="clear",
        description="Clear Messages in Current Text Channel",
        options=[
            create_option(
                name="number",
                description="Number of Messages for Clear",
                option_type=4,
                required=False)
                ])
    async def clear(self, ctx, number=5):
        """Clear Messages in Current Text Channel"""
        if number > 0:
            await ctx.channel.purge(limit=number)
            await Commands.msg(ctx, "Messages has been cleared", f"Cleared **{number}** messages")
        else: await Commands.error(ctx, "Clear error", f"Cannot clear **{number}** messages")

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
        if v1 + v2 == value:
            await Commands.msg(ctx, "You won :D", f"The sum of values is **{v1 + v2}**. The values of dice is **{v1}** and **{v2}**")
        elif v1 == value or v2 == value:
            await Commands.msg(ctx, "You guess value one of the dice :D", (
                    f"The values one of dice is **{v1 if v1 == value else v2}**."
                    f" The values of dice is **{v1}** and **{v2}**"))
        else: await Commands.error(ctx, "You lose :(", f"The values of dice is **{v1}** and **{v2}**")

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
        await Commands.msg(ctx, "Special game by Parzibot", f"I advise you to play **{random.choice(responses)}**")

    @cog_ext.cog_slash(
        name="help",
        description="The List of Parzibot Commands",
        options=[
            create_option(
                name="command",
                description="The Help Message for Specific Command",
                option_type=3,
                required=False,
                choices=[
                    create_choice(name="8ball", value="8ball"),
                    create_choice(name="about", value="about"),
                    create_choice(name="clear", value="clear"),
                    create_choice(name="dice", value="dice"),
                    create_choice(name="getgame", value="getgame"),
                    create_choice(name="help", value="help"),
                    create_choice(name="ping", value="ping"),
                    create_choice(name="users", value="users"),
                    create_choice(name="whiteblack", value="whiteblack")
                    ])
            ])
    async def help(self, ctx, command=None):
        """The List of Parzibot Commands"""
        if command is None:
            await Commands.msg(ctx, "Bot Commands", (
                    " • **/8ball** `question` - The Ball of Predictions\n"
                    " • **/about** - Information About Parzibot\n"
                    " • **/clear** `number` - Clear Messages in Current Text Channel\n"
                    " • **/dice** `value` - The Game of Dice\n"
                    " • **/getgame** - Choice random game from our list\n"
                    " • **/help** `command` - The list of Parzibot commands\n"
                    " • **/ping** - Parzibot ping\n"
                    " • **/users** - List of Text Channel members\n"
                    " • **/whiteblack** `color` - The White/Black Game"))
        elif command == "8ball":
            await Commands.msg(ctx, "**/8ball** command - The Ball of Predictions", (
                    "**Syntax:** **/8ball** `question`\n"
                    "**Options:** `question` - Your Question for The Ball of Predictions **(Required)**"))
        elif command == "about":
            await Commands.msg(ctx, "**/about** command - Information About Parzibot", "**Syntax:** **/about**")
        elif command == "clear":
            await Commands.msg(ctx, "**/clear** command - Clear Messages in Current Text Channel", (
                    "**Syntax:** **/clear** `number`\n"
                    "**Options:** `number` - Number of Messages for Clear **(Optional)**"))
        elif command == "dice":
            await Commands.msg(ctx, "**/dice** command - The Game of Dice", (
                    "**Syntax:** **/dice** `value`\n"
                    "**Options:** `value` - The Value What You\"re Predicting **(Required)**\n"
                    "**Rules:** If you guess sum of dice values - you won, "
                    "if you guess one of the dice value - it\"s a draw, else you lose"))
        elif command == "getgame":
            await Commands.msg(ctx, "**/getgame** command - Choice Random Game from Our List", "**Syntax:** **/getgame**")
        elif command == "help":
            await Commands.msg(ctx, "**/help** command - The List of Parzibot Commands", (
                    "**Syntax:** **/help** `command`\n"
                    "**Options:** `command` - The Help Message for Specific Command **(Optional)**"))
        elif command == "ping":
            await Commands.msg(ctx, "**/ping** command - Parzibot's Ping", "**Syntax:** **/ping**")
        elif command == "users":
            await Commands.msg(ctx, "**/users** command - The List of Text Channel Members", "**Syntax:** **/users**")
        elif command == "whiteblack":
            await Commands.msg(ctx, "**/whiteblack** command - The White/Black Game", (
                    "**Syntax:** **/whiteblack** `color`\n"
                    "**Options:** `color` - The Hidden Color (White or Black) **(Required)**\n"))

    @cog_ext.cog_slash(name="ping", description="Parzibot's Ping")
    async def ping(self, ctx):
        """Parzibot"s Ping"""
        await Commands.msg(ctx, "Parzibot Ping", f"**Parzibot** Ping: `{round(self.client.latency * 1000)}ms`")

    @cog_ext.cog_slash(name="users", description="List of Text Channel members")
    async def users(self, ctx):
        """The List of Text Channel Members"""
        await Commands.msg(ctx, "Channel Members", "".join(f"\t**{member}**\n" for member in ctx.channel.members))

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
        result = get_random_color()
        if color == result: await Commands.msg(ctx, "You won :D", f"Right color is `{result}`")
        else: await Commands.error(ctx, "You lose :(", f"Right color is `{result}`")


def setup(client):
    """Setup function"""
    client.add_cog(Commands(client))

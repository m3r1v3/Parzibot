import datetime
import random

from discord import Embed, Colour
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice


def get_random_color():
    """Select random color"""
    return random.choice(['white', 'black'])


class Commands(commands.Cog):

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
        await ctx.send(
            embed=Embed(
                title=f"**Question:** `{question}`",
                description=f"**Answer:** `{random.choice(responses)}`",
                color=Colour(0x59d9b9)
                )
            )

    @cog_ext.cog_slash(
        name="about",
        description="Information About Parzibot"
        )
    async def about(self, ctx):
        """Information About Parzibot"""
        await ctx.send(
            embed=Embed(
                title="About **Parzibot**",
                description=(
                    f"**Parzibot** is free open-source project, created by **merive_**\n"
                    f"You can find more information on [Parzibot Website](https://merive.herokuapp.com/Parzibot)\n"
                    f"**Parzibot**, {datetime.datetime.now().year}"
                    ), 
                color=Colour(0x59d9b9)
                )
            )

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
            await ctx.send(
                embed=Embed(
                    title=f"Cleared **{number}** messages",
                    color=Colour(0x59d9b9)
                    )
                )
        else:
            await ctx.send(
                embed=Embed(
                    title=f"Cannot clear **{number}** messages",
                    color=Colour(0xd95959)
                    )
                )

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
            await ctx.send(
                embed=Embed(
                    title="You won :D",
                    description=f"The sum of values is **{v1+v2}**. The values of dice is **{v1}** and **{v2}**",
                    color=Colour(0x59d9b9)
                    )
                )
        elif v1 == value or v2 == value:
            await ctx.send(
                embed=Embed(
                    title="You guess value one of the dice :D",
                    description=(
                        f"The values one of dice is **{v1 if v1 == value else v2}**."
                        f" The values of dice is **{v1}** and **{v2}**"
                    ),
                    color=Colour(0x59d9b9)
                    )
                )
        else:
            await ctx.send(
                embed=Embed(
                    title="You lose :(",
                    description=f"The values of dice is **{v1}** and **{v2}**",
                    color=Colour(0xd95959)
                    )
                )

    @cog_ext.cog_slash(name="getgame", description="Choice Random Game from Our List")
    async def getgame(self, ctx):
        """Choice Random Game from Our List"""
        responses = [
            'Animal Crossing: New Horizons', 'Apex Legends',
            'Assasin\'s Creed Valhalla', 'CS:GO',
            'Call of Duty: Warzone', 'Control',
            'Cyberpunk 2077', 'Dead by Daylight',
            'Dota 2', 'Fall Guys',
            'Fallout 76', 'Fortnite',
            'Forza Horizon 4', 'GTA V',
            'Genshin Impact', 'League of Legends',
            'Minecraft', 'Overwatch',
            'PUBG', 'RDR 2',
            'Rainbow Six: Siege', 'Rocket League',
            'Super Animal Royale', 'Terraria',
            'The Elder Scrolls V: Skyrim', 'Valorant'
            ]
        await ctx.send(
            embed=Embed(
                title=f"Play to **{random.choice(responses)}**",
                color=Colour(0x59d9b9)
                )
            )

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
            await ctx.send(
                embed=Embed(
                    title="Bot Commands",
                    description=(
                        ' - **/8ball** `question` - The Ball of Predictions\n'
                        ' - **/about** - Information About Parzibot\n'
                        ' - **/clear** `number` - Clear Messages in Current Text Channel\n'
                        ' - **/dice** `value` - The Game of Dice\n'
                        ' - **/getgame** - Choice random game from our list\n'
                        ' - **/help** `command` - The list of Parzibot commands\n'
                        ' - **/ping** - Parzibot ping\n'
                        ' - **/users** - List of Text Channel members\n'
                        ' - **/whiteblack** `white/black` - The White/Black Game\n'
                    ),
                    color=Colour(0x59d9b9)
                    )
                )
        elif command == "8ball":
            await ctx.send(
                embed=Embed(
                    title="**/8ball** command - The Ball of Predictions",
                    description=(
                        '**Syntax:** **/8ball** `question`\n'
                        '**Options:** `question` - Your Question for The Ball of Predictions **(Required)**'
                    ),
                    color=Colour(0x59d9b9)
                    )
                )
        elif command == "about":
            await ctx.send(
                embed=Embed(
                    title="**/about** command - Information About Parzibot",
                    description='**Syntax:** **/about**',
                    color=Colour(0x59d9b9)
                    )
                )
        elif command == "clear":
            await ctx.send(
                embed=Embed(
                    title="**/clear** command - Clear Messages in Current Text Channel",
                    description=(
                        '**Syntax:** **/clear** `number`\n'
                        '**Options:** `number` - Number of Messages for Clear **(Optional)**'
                    ),
                    color=Colour(0x59d9b9)
                    )
                )
        elif command == "dice":
            await ctx.send(
                embed=Embed(
                    title="**/dice** command - The Game of Dice",
                    description=(
                        '**Syntax:** **/dice** `value`\n'
                        '**Options:** `value` - The Value What You\'re Predicting **(Required)**\n'
                        '**Rules:** If you guess sum of dice values - you won, '
                        'if you guess one of the dice value - it\'s a draw, else you lose'
                    ),
                    color=Colour(0x59d9b9)
                    )
                )
        elif command == "getgame":
            await ctx.send(
                embed=Embed(
                    title="**/getgame** command - Choice Random Game from Our List",
                    description='**Syntax:** **/getgame**',
                    color=Colour(0x59d9b9)
                    )
                )
        elif command == "help":
            await ctx.send(
                embed=Embed(
                    title="**/help** command - The List of Parzibot Commands",
                    description=(
                        '**Syntax:** **/help** `command`\n'
                        '**Options:** `command` - The Help Message for Specific Command **(Optional)**'
                        ),
                    color=Colour(0x59d9b9)
                    )
                )
        elif command == "ping":
            await ctx.send(
                embed=Embed(
                    title="**/ping** command - Parzibot's Ping",
                    description='**Syntax:** **/ping**',
                    color=Colour(0x59d9b9)
                    )
                )
        elif command == "users":
            await ctx.send(
                embed=Embed(
                    title="**/users** command - The List of Text Channel Members",
                    description='**Syntax:** **/users**',
                    color=Colour(0x59d9b9)
                    )
                )
        elif command == "whiteblack":
            await ctx.send(
                embed=Embed(
                    title="**/whiteblack** command - The White/Black Game",
                    description=(
                        '**Syntax:** **/whiteblack** `color`\n'
                        '**Options:** `color` - The Hidden Color (White or Black) **(Required)**\n'
                        ),
                    color=Colour(0x59d9b9)
                    )
                )

    @cog_ext.cog_slash(name="ping", description="Parzibot's Ping")
    async def ping(self, ctx):
        """Parzibot's Ping"""
        await ctx.send(
            embed=Embed(
                title=f"**Parzibot** Ping: `{round(self.client.latency * 1000)}ms`",
                color=Colour(0x59d9b9)
                )
            )

    @cog_ext.cog_slash(name="users", description="List of Text Channel members")
    async def users(self, ctx):
        """The List of Text Channel Members"""
        members = ''.join(f'\t**{member}**\n' for member in ctx.channel.members)
        await ctx.send(
            embed=Embed(
                title="Channel Members",
                description=f"{members}",
                color=Colour(0x59d9b9)
                )
            )

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
        if color == result:
            await ctx.send(
                embed=Embed(
                    title="You won :D",
                    description=f"Right color is `{result}`",
                    color=Colour(0x59d9b9)
                    )
                )
        else:
            await ctx.send(
                embed=Embed(
                    title="You lose :(",
                    description=f"Right color is `{result}`",
                    color=Colour(0xd95959)
                    )
                )


def setup(client):
    """Setup function"""
    client.add_cog(Commands(client))

import random
import datetime

from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice


def get_random_color():
    """Random generate color"""
    return random.choice(['white', 'black'])


class SlashCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="ping", description="Parzibot ping")
    async def ping(self, ctx):
        await ctx.send(f'**Ping**: `{round(self.client.latency * 1000)}ms`')

    @cog_ext.cog_slash(name="8ball",
                       description="The ball of predictions",
                       options=[create_option(
                           name="question",
                           description="Your question to ball",
                           option_type=3,
                           required=True
                       )
                       ])
    async def _8ball(self, ctx, *, question: str):
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
        await ctx.send(f'**Question**: `{question}`\n'
                       f'**Answer**: `{random.choice(responses)}`')

    @cog_ext.cog_slash(name="clear",
                       description="Clear text chat",
                       options=[
                           create_option(
                               name="number",
                               description="Number of messages for clear",
                               option_type=4,
                               required=False)
                       ])
    async def clear(self, ctx, number=5):
        """Clear chat"""
        await ctx.channel.purge(limit=number)
        await ctx.send(f"Cleared **{number}** messages")

    @cog_ext.cog_slash(name="users", description="List of text chat members")
    async def users(self, ctx):
        """Return bot users"""
        channel = ctx.channel
        members = "".join(f'\t*{str(member)}*\n' for member in channel.members)
        await ctx.send(f'**Channel members:**\n{str(members)}')

    @cog_ext.cog_slash(name="wbg", description="Choice random game from our list")
    async def what_by_game(self, ctx):
        """Function for choice game"""
        responses = ["Fortnite", "CS:GO", "GTAV", "GTA:San Andreas", "Dota 2", "Rocket League",
                     "PUBG", "Super Animal Royale", "Rust", "RDR2", "Assassin's creed",
                     "Call of Duty: Warzone", "Minecraft", "Fall Guys", "Apex Legends"]
        result = random.choice(responses)

        await ctx.send(f'Play to `{result}`')

    @cog_ext.cog_slash(name="gg", description="Randomly chooses a game from your list")
    async def good_game(self, ctx, *, games):
        """Random choice game"""
        await ctx.send(f'Play to `{random.choice(games.split())}`')

    @cog_ext.cog_slash(name="wb",
                       description="The White/Black Game",
                       options=[
                           create_option(
                               name="color",
                               description="Your color",
                               option_type=3,
                               required=True,
                               choices=[
                                   create_choice(name="White", value="white"),
                                   create_choice(name="Black", value="black")
                               ]
                           )
                       ])
    async def white_black(self, ctx, color: str):
        """White/Black game"""
        result = get_random_color()
        if color == result:
            await ctx.send(f'**You won**: `{result}`')
        else:
            await ctx.send(f'**You lose**: `{result}`')

    @cog_ext.cog_slash(name="help", description="List of Parzibot commands")
    async def help(self, ctx):
        """Return slash commands"""
        await ctx.send('**Bot commands**'
                       '\n\t - **/8ball** `question` - The ball of predictions'
                       '\n\t - **/about** - About Parzibot'
                       '\n\t - **/admin_help** - List of Parzibot admin commands'
                       '\n\t - **/clear** `Number of messages` - Clear text chat'
                       '\n\t - **/gg** `game1 game2 ... gameN` - Randomly chooses a game from your list'
                       '\n\t - **/help** - List of Parzibot commands'
                       '\n\t - **/ping** - Parzibot ping'
                       '\n\t - **/users** - List of text chat members'
                       '\n\t - **/wb** `white/black` - The White/Black Game'
                       '\n\t - **/wbg** - Choice random game from our list')

    @cog_ext.cog_slash(name="about", description="About Parzibot")
    async def about(self, ctx):
        """Return about bot"""
        await ctx.send(f"**Parzibot** is free open-source project, created by **@merive_#6187**.\n"
                       f"You can find more information on [Parzibot Website](https://merive.herokuapp.com/Parzibot)\n"
                       f"**Parzibot**, {datetime.datetime.now().year}")


def setup(client):
    """Setup function"""
    client.add_cog(SlashCommands(client))

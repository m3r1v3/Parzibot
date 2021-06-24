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

    @cog_ext.cog_slash(name="ping", description="Return user ping")
    async def ping(self, ctx):
        await ctx.send(f'Ping: {round(self.client.latency * 1000)}ms')

    @cog_ext.cog_slash(name="8ball",
                       description="8ball game",
                       options=[create_option(
                           name="question",
                           description="You  question",
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
        await ctx.send(f'Question: {question}\n'
                       f'Answer: {random.choice(responses)}')

    @cog_ext.cog_slash(name="clear",
                       description="Clear chat",
                       options=[
                           create_option(
                               name="amount",
                               description="Amount messages on clearing",
                               option_type=4,
                               required=False)
                       ])
    async def clear(self, ctx, amount=5):
        """Clear chat"""
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"*Cleared {amount + 1} messages*")

    @cog_ext.cog_slash(name="users", description="Amount users of chat")
    async def users(self, ctx):
        """Return bot users"""
        channel = ctx.channel
        members = "".join(f'\t*{str(member)}*\n' for member in channel.members)
        await ctx.send(f'**Channel members:**\n{str(members)}')

    @cog_ext.cog_slash(name="wbg", description="Choice random game from our list")
    async def what_by_game(self, ctx):
        """Function for choice game"""
        responses = ["Fortnite", "CS:GO", "GTAV", "GTA:SA",
                     "PUBG", "SAR", "Rust", "RDR2", "Assassin's creed",
                     "Call of Duty:Warzone", "Minecraft"]
        result = random.choice(responses)

        await ctx.send(f'Play to {result}')

    @cog_ext.cog_slash(name="gg", description="Choice you random game from your list")
    async def good_game(self, ctx, *, games):
        """Random choice game"""
        await ctx.send(f'Play to {random.choice(games.split())}')

    @cog_ext.cog_slash(name="wb",
                       description="White/Black Game",
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
            await ctx.send(f'You winner ({result})')
        else:
            await ctx.send(f'You lose ({result})')

    @cog_ext.cog_slash(name="help", description="Help command")
    async def help(self, ctx):
        """Return commands"""
        await ctx.send('**Common Commands**'
                       '\n\t - $8ball `question` - Ball of predictions'
                       '\n\t - $about - About bot'
                       '\n\t - $admin_help - Admin commands'
                       '\n\t - $clear `Qty` - Clear chat'
                       '\n\t - $gg `[game1 game2 ... gameN]` - Randomly chooses a game'
                       '\n\t - $help - Bot commands'
                       '\n\t - $lang `(EN/RU)` - Set language'
                       '\n\t - $ping - You ping'
                       '\n\t - $splash_commands - Slash-commands'
                       '\n\t - $users - Bot users'
                       '\n\t - $wb `(white/black)` - Game Black/White'
                       '\n\t - $wbg - Advice on what to play')

    @cog_ext.cog_slash(name="slash_help", description="Slash commands")
    async def slash_help(self, ctx):
        """Return all commands"""
        await ctx.send('**Slash commands**'
                       '\n\t - /8ball `question` - Ball of predictions'
                       '\n\t - /about - About bot'
                       '\n\t - /admin_help - Admin commands'
                       '\n\t - /clear `Qty` - Clear chat'
                       '\n\t - /gg `[game1 game2 ... gameN]` - Randomly chooses a game'
                       '\n\t - /help - Bot commands'
                       '\n\t - /ping - You ping'
                       '\n\t - /splash_commands - Slash-commands'
                       '\n\t - /users - Bot users'
                       '\n\t - /wb `(white/black)` - Game Black/White'
                       '\n\t - /wbg - Advice on what to play')

    @cog_ext.cog_slash(name="admin_help", description="Admin commands")
    async def admin_help(self, ctx):
        """Return admin commands"""
        await ctx.send('**Admin Commands**'
                       '||\n\t - $ban `@nickname` - Ban user||'
                       '||\n\t - $give_role `@nickname` `role_id` - Give role||'
                       '||\n\t - $nickname `@nickname` `new_nick` - Edit nickname||'
                       '||\n\t - $kick `@user` - Kick user||'
                       '||\n\t - $set_role `role_id` - Set default role||'
                       '||\n\t - $remove_role `role_id` - Remove default role||')

    @cog_ext.cog_slash(name="about", description="About command")
    async def about(self, ctx):
        """Return about bot"""
        await ctx.send(f"Parzibot is free open source project, created by **@merive_#6187**.\n"
                       f"All source code is on [GitHub](https://github.com/merive/Parzibot)\n"
                       f"Parzibot, {datetime.datetime.now().year}")


def setup(client):
    """Setup function"""
    client.add_cog(SlashCommands(client))

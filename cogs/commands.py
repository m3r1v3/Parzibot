import random

import discord
from discord.ext import commands

from cogs.language import get_language
from user_base import check_user


def get_random_color():
    """Random generate color"""
    return random.choice(['white', 'black'])


class Commands(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        """Return you latency"""
        check_user(ctx.message.author.name, str(ctx.guild.id))
        await ctx.send(f'Ping: {round(self.client.latency * 1000)}ms')

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        """8ball game"""
        check_user(ctx.message.author.name, str(ctx.guild.id))
        if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
            responses_ru = ["Бесспорно...",
                            "Предрешено...",
                            "Никаких сомнений...",
                            "Определённо да...",
                            "Можешь быть уверен в этом...",
                            "Мне кажется — «да»...",
                            "Вероятнее всего...",
                            "Хорошие перспективы...",
                            "Знаки говорят — «да»...",
                            "Да...",
                            "Пока не ясно, попробуй снова...",
                            "Спроси позже...",
                            "Лучше не рассказывать...",
                            "Сейчас нельзя предсказать...",
                            "Сконцентрируйся и спроси опять...",
                            "Даже не думай...",
                            "Мой ответ — «нет»...",
                            "По моим данным — «нет»...",
                            "Перспективы не очень хорошие...",
                            "Весьма сомнительно..."]
            await ctx.send(f'Вопрос: {question}\nОтвет: {random.choice(responses_ru)}')
        else:
            responses_en = ["It is certain...",
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
            await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses_en)}')

    @commands.command()
    async def clear(self, ctx, amount=6):
        """Clear chat"""
        check_user(ctx.message.author.name, str(ctx.guild.id))
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick user"""
        check_user(ctx.message.author.name, str(ctx.guild.id))
        await member.kick(reason=reason)
        if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
            await ctx.send(f'{member.mention} был выгнан')

        else:
            await ctx.send(f'Kicked {member.mention}')

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban user"""
        check_user(ctx.message.author.name, str(ctx.guild.id))
        await member.ban(reason=reason)
        if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":

            await ctx.send(f'{member.mention} забанен')
        else:
            await ctx.send(f'Banned {member.mention}')

    @commands.command()
    async def unban(self, ctx, *, member):
        """Unban user"""
        check_user(ctx.message.author.name, str(ctx.guild.id))
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
                    await ctx.send(f'{member.mention} разбанен')
                else:
                    await ctx.send(f'Unbanned {member.mention}')

    @commands.command()
    async def users(self, ctx):
        """Return bot users"""
        check_user(ctx.message.author.name, str(ctx.guild.id))
        channel = ctx.channel
        members = "".join(f'\t*{str(member)}*\n' for member in channel.members)
        if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
            await ctx.send(f'**Участники канала:**\n{str(members)}')
        else:
            await ctx.send(f'**Channel members:**\n{str(members)}')

    @commands.command(aliases=['wbg'])
    async def what_by_game(self, ctx):
        """Function for choice game"""
        check_user(ctx.message.author.name, str(ctx.guild.id))

        responses = ["Fortnite", "CS:GO", "GTAV", "GTA:SA",
                     "PUBG", "SAR", "Rust", "RDR2", "Assassin's creed",
                     "Call of Duty:Warzone", "Minecraft"]
        if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
            await ctx.send(f'Поиграй в {random.choice(responses)}')
        else:
            await ctx.send(f'Play to {random.choice(responses)}')

    @commands.command(aliases=['gg'])
    async def good_game(self, ctx, *, games):
        """Random choice game"""
        check_user(ctx.message.author.name, str(ctx.guild.id))

        if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
            await ctx.send(f'Поиграй в {random.choice(games.split())}')
        else:
            await ctx.send(f'Play to {random.choice(games.split())}')

    @commands.command(aliases=['wb'])
    async def white_black(self, ctx, question):
        """White/Black game"""
        check_user(ctx.message.author.name, str(ctx.guild.id))

        if question == get_random_color():
            if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
                await ctx.send(f'Ты выйграл')
            else:
                await ctx.send(f'You winner')
        else:
            if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
                await ctx.send(f'Ты проиграл')
            else:
                await ctx.send(f'You lose')

    @commands.command()
    async def help(self, ctx):
        """Return all commands"""
        check_user(ctx.message.author.name, str(ctx.guild.id))

        if get_language(ctx.message.author.name, str(ctx.guild.id)) == "RU":
            await ctx.send(f'Команды бота:'
                           f'\n\t - $ping - Твой ping'
                           f'\n\t - $8ball `вопрос` - Предсказывающий шар'
                           f'\n\t - $clear `кол-во` - Очистить чат'
                           f'\n\t - $kick `@user` - Выгнать пользователя'
                           f'\n\t - $ban `@nickname` - Заблокировать пользователя'
                           f'\n\t - $unban `nickname#tag` - Разблокировать пользователя'
                           f'\n\t - $users - Пользователи бота'
                           f'\n\t - $wbg - Предлагает во что поиграть'
                           f'\n\t - $gg `[game1 game2 ... gameN]` - Выбирает случайную игру'
                           f'\n\t - $lang `(EN/RU)` - Устанавливает язык'
                           f'\n\t - $wb `(white/black)` - Игра Черное/Белое'
                           f'\n\t - $about - О боте'
                           f'\n\t - $help - Команды бота')
        else:
            await ctx.send(f'Bot commands:'
                           f'\n\t - $ping - You ping'
                           f'\n\t - $8ball `question` - Ball of predictions'
                           f'\n\t - $clear `Qty` - Clear chat'
                           f'\n\t - $kick `@user` - Kick user'
                           f'\n\t - $ban `@nickname` - Ban user'
                           f'\n\t - $unban `nickname#tag` - Unban user'
                           f'\n\t - $users - Bot users'
                           f'\n\t - $wbg - Advice on what to play'
                           f'\n\t - $gg `[game1 game2 ... gameN]` - Randomly chooses a game'
                           f'\n\t - $lang `(EN/RU)` - Set language'
                           f'\n\t - $about - About bot'
                           f'\n\t - $wb `(white/black)` - Game Black/White'
                           f'\n\t - $help - Bot commands')

    @commands.command()
    async def about(self, ctx):
        check_user(ctx.message.author.name, str(ctx.guild.id))
        await ctx.send(f"Parzibot is free open source project, created by **@merive_#6187**.\n"
                       f"All source code is on [GitHub](https://github.com/merive/Parzibot)\n"
                       f"Parzibot, 2021")


def setup(client):
    """Setup function"""
    client.add_cog(Commands(client))

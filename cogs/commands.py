import random

import discord
from discord.ext import commands

from cogs.language import get_lang


def get_random_color():
    """Random generate color"""
    colors = ['white', 'black']
    return random.choice(colors)


class Commands(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        """Return you latency"""
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        """8-ball game"""
        if get_lang() == "EN":
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
        else:
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

    @commands.command()
    async def clear(self, ctx, amount=6):
        """Clear chat"""
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick user"""
        await member.kick(reason=reason)
        if get_lang() == "EN":
            await ctx.send(f'Kicked {member.mention}.')
        else:
            await ctx.send(f'{member.mention} был выгнан.')

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban user"""
        await member.ban(reason=reason)
        if get_lang() == "EN":
            await ctx.send(f'Banned {member.mention}')
        else:
            await ctx.send(f'{member.mention} забанен.')

    @commands.command()
    async def unban(self, ctx, *, member):
        """Unban user"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                if get_lang() == "EN":
                    await ctx.send(f'Unbanned {member.mention}')
                else:
                    await ctx.send(f'{member.mention} разбанен.')

    @commands.command()
    async def users(self, ctx):
        """Return bot users"""
        user = ""
        for i in range(1, len(self.client.users)):
            user += str(self.client.users[i]) + "\n\t"
            if get_lang() == "EN":
                await ctx.send(f'Bot users:\n\t' + str(user))
            else:
                await ctx.send(f'Пользователи бота:\n\t' + str(user))

    @commands.command()
    async def spam(self, ctx, time=1, mes="..."):
        """Spam command"""
        for _ in range(time):
            await ctx.send(str(mes))

    @commands.command(aliases=['wbg'])
    async def what_by_game(self, ctx):
        """Function for choice game"""
        responses = ["Fortnite", "CS:GO", "GTA-V", "GTA:SA",
                     "PUBG", "SAR", "Rust", "RDR2", "Assassin's creed",
                     "Call of Duty:Warzone", "Minecraft"]
        if get_lang() == "EN":
            await ctx.send(f'Play to {random.choice(responses)}.')
        else:
            await ctx.send(f'Поиграй в {random.choice(responses)}.')

    @commands.command(aliases=['gg'])
    async def get_game(self, ctx, *, games):
        """Random choice game"""
        if get_lang() == "EN":
            await ctx.send(f'Play to {random.choice(games.split())}.')
        else:
            await ctx.send(f'Поиграй в {random.choice(games.split())}.')

    @commands.command(aliases=['wb'])
    async def white_black(self, ctx, question):
        """White/Black game"""
        if question == get_random_color():
            if get_lang() == "EN":
                await ctx.send(f'You winner!')
            else:
                await ctx.send(f'Ты выйграл!')
        else:
            if get_lang() == "EN":
                await ctx.send(f'You lose(')
            else:
                await ctx.send(f'Ты проиграл(')

    @commands.command()
    async def help(self, ctx):
        """Return all commands"""
        if get_lang() == "EN":
            await ctx.send(f'Bot commands:'
                           f'\n\t - $ping - You ping,'
                           f'\n\t - $8ball question - Ball of predictions,'
                           f'\n\t - $clear Qty - Clear chat,'
                           f'\n\t - $kick @user - Kick user,'
                           f'\n\t - $ban @nickname - Ban user,'
                           f'\n\t - $unban nickname#tag - Unban user,'
                           f'\n\t - $users - Bot users,'
                           f'\n\t - $spam qty message  - spam function,'
                           f'\n\t - $wbg - Advice on what to play,'
                           f'\n\t - $gg [game1 game2 ... gameN] - Randomly chooses a game,'
                           f'\n\t - $lang `(EN/RU)` - Set language,'
                           f'\n\t - $wb color(white/black) - Game Black/White,'
                           f'\n\t - $help - Bot commands.')
        else:
            await ctx.send(f'Команды бота:'
                           f'\n\t - $ping - Твой ping,'
                           f'\n\t - $8ball вопрос - Предсказывающий шар,'
                           f'\n\t - $clear кол-во - Очистить чат,'
                           f'\n\t - $kick @пользователь - Выгнать пользователя,'
                           f'\n\t - $ban @ник - Заблокировать пользователя,'
                           f'\n\t - $unban nickname#tag - Разблокировать пользователя,'
                           f'\n\t - $users - Пользователи бота,'
                           f'\n\t - $spam кол-во сообщение  - Спам функция,'
                           f'\n\t - $wbg - Предлагает во что поиграть,'
                           f'\n\t - $gg [game1 game2 ... gameN] - Выбирает случайную игру,'
                           f'\n\t - $lang `(EN/RU)` - Устанавливает язык,'
                           f'\n\t - $wb цвет(white/black) - Игра Черное/Белое,'
                           f'\n\t - $help - Команды бота.')


def setup(client):
    """Setup function"""
    client.add_cog(Commands(client))

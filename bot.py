# bot.py
# Переработано 17.02.20
# Язык поддержку английского не делать, бессмысленно
# UPD: Может сделать сайт боту? Я хз...
import random
import os
import discord
from discord.ext import commands
# Нужно решить проблему с префиксом, какой выбрать?
client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    """Функция проверки работы бота."""
    print("Bot is ready.")


@client.event
async def on_member_remove(ctx, member):
    """Ввывод информации об выходе пользователя."""
    print(f'{member} вышел c сервера.')


@client.command()
async def ping(ctx):
    """Задержка пользователя между сервером."""
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    """Мини-игра угадывательный шар."""
    responses = ["It is certain (Бесспорно)",
                 "It is decidedly so (Предрешено)",
                 "Without a doubt (Никаких сомнений)",
                 "Yes — definitely (Определённо да)",
                 "You may rely on it (Можешь быть уверен в этом)",
                 "As I see it, yes (Мне кажется — «да»)",
                 "Most likely (Вероятнее всего)",
                 "Outlook good (Хорошие перспективы)",
                 "Signs point to yes (Знаки говорят — «да»)",
                 "Yes (Да)",
                 "Reply hazy, try again (Пока не ясно, попробуй снова)",
                 "Ask again later (Спроси позже)",
                 "Better not tell you now (Лучше не рассказывать)",
                 "Cannot predict now (Сейчас нельзя предсказать)",
                 "Concentrate and ask again (Сконцентрируйся и спроси опять)",
                 "Don’t count on it (Даже не думай)",
                 "My reply is no (Мой ответ — «нет»)",
                 "My sources say no (По моим данным — «нет»)",
                 "Outlook not so good (Перспективы не очень хорошие)",
                 "Very doubtful (Весьма сомнительно)"]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.command()
async def clear(ctx, amount=6):
    """Очистка чата на определенное кол-во сообщений."""
    await ctx.channel.purge(limit=amount)


@client.command()
async def spam(ctx, time=1):
    """Команда спамер (По приколу)"""
    for i in range(time):
        await ctx.send("Спамим, Спамим...")


# Нужно протестить
@client.command()
async def users(ctx):
    """Вывод пользователей в сети"""
    for i in range(1, len(client.users)):
        await ctx.send(f'{client.users[i]}')


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    """Блокировка пользователя."""
    await member.ban(reason=reason)
    await ctx.send(f'Забанен {member.mention}')


@client.command()
async def unban(ctx, *, member):
    """Разблокировка пользователя."""
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Разбанен {user.mention}')


@client.command()
async def wb(ctx, *, question):
    """Игра угадай цвет White or Black"""
    color = ['white', 'black']
    color_random = random.choice(color)
    if question == color_random:
        await ctx.send("Верно, вы угадали. Это " + color_random)
    else:
        await ctx.send("Неверно, вы неугадали. Это " + color_random)


@client.command()
async def com(ctx):
    """Команды бота"""
    await ctx.send(f'Команды бота:'
                   f'\n\t/ping -- Ваш пинг,'
                   f'\n\t/8ball "вопрос" -- Шар предсказаний,'
                   f'\n\t/clear "Кол-во" -- Очистка чата,'
                   f'\n\t/ban "@ник" -- Блокировка пользователя,'
                   f'\n\t/unban "ник#персональный тег" -- Разблокировка пользователей,'
                   f'\n\t/wb "цвет white/black" -- Игра белое/черное,'
                   f'\n\t/com -- Команды Бота,'
                   f' \n\t/users -- Пользователи чата,'
                   f'\n\t/spam + кол-во -- Спам от бота,'
                   f' \n\t/users -- Пользователи чата,'
                   f'\nКоманды бота переодически обнавляются, из-за этого советуем проверять список команд.'
                   )

# Токена тут нету он на *******.
token = os.environ.get('BOT_TOKEN')
client.run(str(token))

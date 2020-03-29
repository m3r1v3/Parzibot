# bot.py
# Переработано 29.03.20
import os
import random

import discord
from discord.ext import commands

# Оставить данный префикс
client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    """Функция проверка работы бота."""
    print('{0} подключен.'.format(client.user))


@client.event
async def on_member_join(member):
    """Отправка личного сообщения о работе бота и выдача роли в чате."""
    await member.send(
        f'Welcome {member}! White !com to find out my command.'
        f'(Добро пожаловать {member}! Напиши !com чтобы узнать мои команды.)')
    role = discord.utils.get(member.guild.roles, id=691321624108073021)
    await member.add_roles(role)


@client.event
async def on_member_remove(member):
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
async def spam(ctx, mes="Hello", time=1):
    """Команда спамер (По приколу)"""
    for _ in range(time):
        await ctx.send(str(mes))


@client.command()
async def users(ctx):
    """Вывод пользователей в сети"""
    for i in range(1, len(client.users)):
        await ctx.send(f'{client.users[i]}')


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    """Блокировка пользователя."""
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')


@client.command()
async def unban(ctx, *, member):
    """Разблокировка пользователя."""
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned{user.mention}')


@client.command()
async def wb(ctx, *, question):
    """Игра угадай цвет White or Black"""
    colors = ['white', 'black']
    random_color = random.choice(colors)
    if question == random_color:
        await ctx.send("Yes, it's " + random_color)
    else:
        await ctx.send("No, it's " + random_color)


@client.command()
async def com(ctx):
    """Команды бота"""
    await ctx.send(f'Bot commands(Команды бота):'
                   f'\n\t!ping -- You ping(Ваш пинг),'
                   f'\n\t!8ball "question(вопрос)" -- Ball of predictions(Шар предсказаний),'
                   f'\n\t!clear "Qty(Кол-во)" -- Clear chat(Очистка чата),'
                   f'\n\t!ban "@nickname(ник)" -- Ban user(Блокировка пользователя),'
                   f'\n\t!unban "nickname#user tag(ник#персональный тег)" -- Unban user(Разблокировка пользователей),'
                   f'\n\t!wb "color(цвет)(white/black)" -- Game white or black(Игра белое/черное),'
                   f'\n\t!com -- Bot command(Команды Бота),'
                   f' \n\t!users -- Bot users(Пользователи бота),'
                   f'\n\t!spam + message(сообщение) + Qty(кол-во) -- spam function(Спам от бота),'
                   )


# Токена тут нету он на *******.
token = os.environ.get('BOT_TOKEN')
client.run(str(token))

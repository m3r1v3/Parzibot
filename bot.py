# bot.py
# Recycled 03/31/20
import os
import random

import discord
from discord.ext import commands

# Leave this prefix
client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    """Function check the operation of the bot."""
    print('{0} подключен.'.format(client.user))


@client.event
async def on_member_join(member):
    """Sending a personal message about the bot and issuing a role in the chat."""
    await member.send(
        f'Welcome {member}! White !com to find out my command.'
        f'(Добро пожаловать {member}! Напиши !com чтобы узнать мои команды.)')
    role = discord.utils.get(member.guild.roles, id=691321624108073021)
    await member.add_roles(role)


@client.event
async def on_member_remove(member):
    """Output information about user exit."""
    print(f'{member} вышел c сервера.')


@client.command()
async def ping(ctx):
    """Return you latency"""
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    """8-ball game"""
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
    """Clear chat"""
    await ctx.channel.purge(limit=amount)


@client.command()
async def spam(ctx, mes="Why?", time=1):
    """Spam command"""
    for _ in range(time):
        await ctx.send(str(mes))


@client.command()
async def users(ctx):
    """Return bot users"""
    question = ""
    for i in range(1, len(client.users)):
        question += str(client.users[i]) + "\n\t"
    await ctx.send(f'Bot users:\n\t' + str(question))


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    """Ban user."""
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')


@client.command()
async def unban(ctx, *, member):
    """Unban user."""
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned{user.mention}')


@client.command()
async def wb(ctx, *, question):
    """Game White or Black"""
    rc = get_random_color()
    if question == rc:
        await ctx.send("Yes, it's " + question)
    else:
        await ctx.send("No, it's " + get_random_color())


def get_random_color():
    """Random generate color"""
    colors = ['white', 'black']
    return random.choice(colors)


@client.command(aliases=['wbg'])
async def WhatByGame(ctx):
    responses = ["Fortnite", "CS:GO", "Volorant😂", "GTA:SA",
                 "PUBG", "SAR", "Rust", "RDR2", "Assassin's creed"]
    await ctx.send(f'Play to {random.choice(responses)}')


@client.command()
async def com(ctx):
    """Команды бота"""
    await ctx.send(f'Bot commands(Команды бота):'
                   f'\n\n\t - !ping -- You ping(Ваш пинг),'
                   f'\n\n\t - !8ball "question(вопрос)" -- Ball of predictions(Шар предсказаний),'
                   f'\n\n\t - !clear "Qty(Кол-во)" -- Clear chat(Очистка чата),'
                   f'\n\n\t - !ban "@nickname(ник)" -- Ban user(Блокировка пользователя),'
                   f'\n\n\t - !unban "nickname#user tag(ник#персональный тег)"'
                   f' -- Unban user(Разблокировка пользователей),'
                   f'\n\n\t - !wb "color(цвет)(white/black)" -- Game white or black(Игра белое/черное),'
                   f'\n\n\t - !com -- Bot command(Команды Бота),'
                   f'\n\n\t - !users -- Bot users(Пользователи бота),'
                   f'\n\n\t - !spam + message(сообщение) + Qty(кол-во) -- spam function(Спам от бота),'
                   f'\n\n\t - !wbg -- Advice on what to play(Совет во что поиграть)'
                   )


# Токена тут нету он на *******.
token = os.environ.get('BOT_TOKEN')
client.run(str(token))

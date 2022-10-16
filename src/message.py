import discord

from discord import Embed, Colour
from discord.ext import commands


class Message:

    @staticmethod
    def get_embed(title: str, description: str):
        return Embed(title=title, description=description, color=Colour(0x68FFD9)).set_thumbnail(
            url="attachment://Parzibot.png")

    @staticmethod
    def get_games_embed(title: str, description: str):
        return Embed(title=title, description=description, color=Colour(0x8168ff)).set_thumbnail(
            url="attachment://ParzibotGames.png")

    @staticmethod
    def get_music_embed(title: str, description: str):
        return Embed(title=title, description=description, color=Colour(0x68ff72)).set_thumbnail(
            url="attachment://ParzibotMusic.png")

    @staticmethod
    def get_admin_embed(title: str, description: str):
        return Embed(title=title, description=description, color=Colour(0xffff68)).set_thumbnail(
            url="attachment://ParzibotAdmin.png")

    @staticmethod
    def get_error_embed(title: str, description: str):
        return Embed(title=title, description=description, color=Colour(0xff6868)).set_thumbnail(
            url="attachment://ParzibotError.png")

    @staticmethod
    async def basic_msg(ctx, title: str, description: str):
        await ctx.send(file=discord.File("src/images/Parzibot.png", filename="Parzibot.png"),
                       embed=Message.get_embed(title, description))

    @staticmethod
    async def games_msg(ctx, title: str, description: str):
        await ctx.send(file=discord.File("src/images/ParzibotGames.png", filename="ParzibotGames.png"),
                       embed=Message.get_games_embed(title, description))

    @staticmethod
    async def music_msg(ctx, title: str, description: str):
        await ctx.send(file=discord.File("src/images/ParzibotMusic.png", filename="ParzibotMusic.png"),
                       embed=Message.get_music_embed(title, description))

    @staticmethod
    async def admin_msg(ctx, title: str, description: str):
        await ctx.send(file=discord.File("src/images/ParzibotAdmin.png", filename="ParzibotAdmin.png"),
                       embed=Message.get_admin_embed(title, description))

    @staticmethod
    async def error_msg(ctx, title: str, message: str):
        await ctx.send(file=discord.File("src/images/ParzibotError.png", filename="ParzibotError.png"),
                       embed=Message.get_error_embed(title, message))

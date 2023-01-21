import json

import discord

from discord import Embed, Colour
from discord.ext import commands


class Message:

    def get_embed(self, title: str, description: str):
        return Embed(title=title, description=description, color=Colour(0x8ed9c6)).set_thumbnail(
            url="attachment://Parzibot.png")

    def get_games_embed(self, title: str, description: str):
        return Embed(title=title, description=description, color=Colour(0x948ed9)).set_thumbnail(
            url="attachment://ParzibotGames.png")

    def get_music_embed(self, title: str, description: str):
        return Embed(title=title, description=description, color=Colour(0xa1d98e)).set_thumbnail(
            url="attachment://ParzibotMusic.png")

    def get_mod_embed(self, title: str, description: str):
        return Embed(title=title, description=description, color=Colour(0xd9cd8e)).set_thumbnail(
            url="attachment://ParzibotMod.png")

    def get_error_embed(self, title: str, description: str):
        return Embed(title=title, description=description, color=Colour(0xd98e94)).set_thumbnail(
            url="attachment://ParzibotError.png")

    @staticmethod
    def get_basic_msg(section, key):
        return json.loads(open("src/message.json").read())["basic"][section][key]

    @staticmethod
    def get_game_msg(section, key):
        return json.loads(open("src/message.json").read())["game"][section][key]

    @staticmethod
    def get_music_msg(section, key):
        return json.loads(open("src/message.json").read())["music"][section][key]

    @staticmethod
    def get_mod_msg(section, key):
        return json.loads(open("src/message.json").read())["mod"][section][key]

    @staticmethod
    def get_event_msg(section, key):
        return json.loads(open("src/message.json").read())["event"][section][key]

    @staticmethod
    def get_error_msg(section, key):
        return json.loads(open("src/message.json").read())["error"][section][key]

    @staticmethod
    async def basic_msg(ctx, title: str, description: str):
        await ctx.send(file=discord.File("src/images/Parzibot.png", filename="Parzibot.png"),
                       embed=Message().get_embed(title, description))

    @staticmethod
    async def games_msg(ctx, title: str, description: str):
        await ctx.send(file=discord.File("src/images/ParzibotGames.png", filename="ParzibotGames.png"),
                       embed=Message().get_games_embed(title, description))

    @staticmethod
    async def music_msg(ctx, title: str, description: str):
        await ctx.send(file=discord.File("src/images/ParzibotMusic.png", filename="ParzibotMusic.png"),
                       embed=Message().get_music_embed(title, description))

    @staticmethod
    async def mod_msg(ctx, title: str, description: str):
        await ctx.send(file=discord.File("src/images/ParzibotMod.png", filename="ParzibotMod.png"),
                       embed=Message().get_mod_embed(title, description))

    @staticmethod
    async def error_msg(ctx, title: str, message: str):
        await ctx.send(file=discord.File("src/images/ParzibotError.png", filename="ParzibotError.png"),
                       embed=Message().get_error_embed(title, message))

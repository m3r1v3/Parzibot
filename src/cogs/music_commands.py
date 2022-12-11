import asyncio
import random
import os

import discord
from discord import app_commands
from discord.ext import commands

import youtube_dl

from message import Message


class MusicCommands(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                               "options": "-vn"}
        self.songs, self.current, self.shuffle, self.repeat = [], "", False, False

    @app_commands.command(name="musichelp", description=Message.get_music_msg("descriptions", "help"))
    async def musichelp(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        await Message.music_msg(ctx, Message.get_music_msg("titles", "help"), Message.get_music_msg("messages", "help"))

    @app_commands.command(name="connect", description=Message.get_music_msg("descriptions", "connect"))
    async def connect(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if isinstance(interaction.user.voice, type(None)):
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[0])
            return

        voice = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if isinstance(voice, type(None)) or not voice.is_connected():
            await interaction.user.voice.channel.connect()
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[1])
        elif interaction.user.voice.channel != ctx.voice_client.channel:
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[2])
        else: await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[3])

    @app_commands.command(name="disconnect", description=Message.get_music_msg("descriptions", "disconnect"))
    async def disconnect(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if isinstance(interaction.user.voice, type(None)):
            await Message.music_msg(ctx, Message.get_music_msg("titles", "disconnect"), Message.get_music_msg("messages", "disconnect")[0])
            return

        voice = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if isinstance(voice.is_connected(), type(None)):
            await Message.music_msg(interaction, "Parzibot // Not connected", Message.get_music_msg("messages", "disconnect")[1])
        elif interaction.user.voice.channel != ctx.voice_client.channel:
            await Message.music_msg(ctx, "Parzibot // Connected to another", Message.get_music_msg("messages", "disconnect")[2])
        else:
            await Message.music_msg(ctx, "Parzibot // Disconnected", Message.get_music_msg("messages", "disconnect")[3])
            self.songs, self.current, self.shuffle, self.repeat = [], "", False, False
            await voice.disconnect()

    @app_commands.command(name="play", description=Message.get_music_msg("descriptions", "play"))
    @app_commands.describe(url=Message.get_music_msg("descriptions", "play-url"))
    async def play(self, interaction: discord.Interaction, url: str):
        if isinstance(interaction.user.voice, type(None)):
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[0])
            return

        voice = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        ctx: commands.Context = await self.bot.get_context(interaction)
        if isinstance(voice, type(None)) or not voice.is_connected():
            await interaction.user.voice.channel.connect()
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[1])
        elif interaction.user.voice.channel != ctx.voice_client.channel:
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[2])
            return

        self.songs.insert(0, url)
        await self.play_song(interaction)

    async def play_song(self, interaction: discord.Interaction):

        def search(url):
            with youtube_dl.YoutubeDL({"format": "bestaudio", "noplaylist": "True"}) as ydl:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)["entries"][0]
            return {"source": info["formats"][0]["url"], "title": info["title"]}

        voice = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        ctx: commands.Context = await self.bot.get_context(interaction)

        if self.songs:
            self.current = self.songs[0]
            if not self.repeat: self.songs.pop(0)
            data = search(self.current)

            if voice.is_playing():
                voice.pause()
            voice.play(discord.FFmpegPCMAudio(data["source"], **self.FFMPEG_OPTIONS),
                       after=lambda e: asyncio.run_coroutine_threadsafe(self.play_song(interaction), self.bot.loop))
            voice.is_playing()

            await Message.music_msg(ctx, Message.get_music_msg("titles", "play"), Message.get_music_msg("messages", "play").format(title=data['title']))

    @app_commands.command(name="replay", description=Message.get_music_msg("descriptions", "replay"))
    async def replay(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if isinstance(interaction.user.voice, type(None)):
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[0])
            return
        elif interaction.user.voice.channel != ctx.voice_client.channel:
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[2])
            return

        voice = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        voice.stop()

        await self.replay_song(interaction)

    async def replay_song(self, interaction: discord.Interaction):
        def search(url):
            with youtube_dl.YoutubeDL({"format": "bestaudio", "noplaylist": "True"}) as ydl:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)["entries"][0]
            return {"source": info["formats"][0]["url"], "title": info["title"]}

        voice = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)

        data = search(self.current)
        voice.play(discord.FFmpegPCMAudio(data["source"], **self.FFMPEG_OPTIONS),
                   after=lambda e: asyncio.run_coroutine_threadsafe(self.play_song(interaction), self.bot.loop))
        voice.is_playing()

        ctx: commands.Context = await self.bot.get_context(interaction)
        await Message.music_msg(ctx, Message.get_music_msg("titles", "replay"), Message.get_music_msg("messages", "play").format(title=data['title']))

    @app_commands.command(name="pause", description=Message.get_music_msg("descriptions", "pause"))
    async def pause(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if isinstance(interaction.user.voice, type(None)):
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[0])
            return
        elif interaction.user.voice.channel != ctx.voice_client.channel:
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[2])
            return

        voice = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if voice.is_playing():
            voice.pause()
            await Message.music_msg(ctx, Message.get_music_msg("titles", "pause"), Message.get_music_msg("messages", "pause")[0])
        else: await Message.music_msg(ctx, Message.get_music_msg("titles", "pause"), Message.get_music_msg("messages", "pause")[1])

    @app_commands.command(name="resume", description=Message.get_music_msg("descriptions", "resume"))
    async def resume(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if isinstance(interaction.user.voice, type(None)):
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[0])
            return
        elif interaction.user.voice.channel != ctx.voice_client.channel:
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[2])
            return

        voice = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        if voice.is_paused():
            voice.resume()
            await Message.music_msg(ctx, Message.get_music_msg("titles", "resume"), Message.get_music_msg("messages", "resume")[0])
        else: await Message.music_msg(ctx, Message.get_music_msg("titles", "resume"), Message.get_music_msg("messages", "resume")[1])

    @app_commands.command(name="repeat", description=Message.get_music_msg("descriptions", "repeat"))
    async def repeat(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if isinstance(interaction.user.voice, type(None)):
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[0])
            return
        elif interaction.user.voice.channel != ctx.voice_client.channel:
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[2])
            return

        self.repeat = not self.repeat
        if self.repeat: await Message.music_msg(ctx, Message.get_music_msg("titles", "repeat"), Message.get_music_msg("messages", "repeat")[0])
        else:  await Message.music_msg(ctx, Message.get_music_msg("titles", "repeat"), Message.get_music_msg("messages", "repeat")[1])

    @app_commands.command(name="next", description=Message.get_music_msg("descriptions", "next"))
    async def next(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if isinstance(interaction.user.voice, type(None)):
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[0])
            return
        elif interaction.user.voice.channel != ctx.voice_client.channel:
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[2])
            return

        if self.songs: await self.play_song(interaction)
        else: await Message.music_msg(ctx, Message.get_music_msg("titles", "playlist"), Message.get_music_msg("messages", "playlist")[0])

    @app_commands.command(name="playlist", description=Message.get_music_msg("descriptions", "playlist"))
    async def playlist(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if isinstance(interaction.user.voice, type(None)):
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[0])
            return
        elif interaction.user.voice.channel != ctx.voice_client.channel:
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[2])
            return

        if self.songs:
            titles = []
            with youtube_dl.YoutubeDL({}) as ydl:
                titles = [ydl.extract_info(song, download=False).get('title', None) for song in self.songs[:3]]

            playlist = ''.join(f'• {title}\n' for title in titles)
            if len(titles) >= 3: playlist = playlist + f'And {len(titles) - 2} more song(-s)'
            await Message.music_msg(ctx, Message.get_music_msg("titles", "playlist"), Message.get_music_msg("messages", "playlist")[1].format(count=len(self.songs), playlist=playlist))
        else: await Message.music_msg(ctx, Message.get_music_msg("titles", "playlist"), Message.get_music_msg("messages", "playlist")[0])

    @app_commands.command(name="playlistadd", description=Message.get_music_msg("descriptions", "playlistadd"))
    @app_commands.describe(url="YouTube Video URL")
    async def playlistadd(self, interaction: discord.Interaction, url: str):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if isinstance(interaction.user.voice, type(None)):
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[0])
            return
        elif interaction.user.voice.channel != ctx.voice_client.channel:
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[2])
            return

        self.songs.append(url)
        if self.shuffle: random.shuffle(self.songs)
        with youtube_dl.YoutubeDL({"format": "bestaudio", "noplaylist": "True"}) as ydl:
            await Message.music_msg(ctx, Message.get_music_msg("titles", "playlist"), Message.get_music_msg("messages", "playlist")[2].format(title=ydl.extract_info(url, download=False).get('title', None)))

    @app_commands.command(name="playlistclear", description=Message.get_music_msg("descriptions", "playlistclear"))
    async def playlistclear(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if isinstance(interaction.user.voice, type(None)):
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[0])
            return
        elif interaction.user.voice.channel != ctx.voice_client.channel:
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[2])
            return

        if self.songs:
            self.songs, self.current = [], ""
            discord.utils.get(self.bot.voice_clients, guild=interaction.guild).stop()
            await Message.music_msg(ctx, Message.get_music_msg("titles", "playlist"), Message.get_music_msg("messages", "playlist")[3])
        else: await Message.music_msg(ctx, Message.get_music_msg("titles", "playlist"), Message.get_music_msg("messages", "playlist")[0])

    @app_commands.command(name="playlistshuffle", description=Message.get_music_msg("descriptions", "playlistshuffle"))
    async def playlistshuffle(self, interaction: discord.Interaction):
        ctx: commands.Context = await self.bot.get_context(interaction)
        if isinstance(interaction.user.voice, type(None)):
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[0])
            return
        elif interaction.user.voice.channel != ctx.voice_client.channel:
            await Message.music_msg(ctx, Message.get_music_msg("titles", "connect"), Message.get_music_msg("messages", "connect")[2])
            return

        self.shuffle = not self.shuffle
        if self.shuffle: await Message.music_msg(ctx, Message.get_music_msg("titles", "playlistshuffle"), Message.get_music_msg("messages", "playlistshuffle")[0])
        else: await Message.music_msg(ctx, Message.get_music_msg("titles", "playlistshuffle"), Message.get_music_msg("messages", "playlistshuffle")[1])


async def setup(bot: commands.Bot) -> None:
    if int(os.environ.get('MUSIC_COMMANDS')): await bot.add_cog(MusicCommands(bot))

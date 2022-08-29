import asyncio
import datetime
import random

import discord
from discord import app_commands, Embed, Colour
from discord.app_commands import Choice
from discord.ext import commands

import youtube_dl

from message import Message


class MusicCommands(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}
        self.songs, self.current, self.shuffle, self.repeat = [], "", False, False

    @app_commands.command(name="musichelp", description="The list of Parzibot music commands")
    async def musichelp(self, interaction: discord.Interaction):
        await Message.music_msg(await self.bot.get_context(interaction), "Parzibot // Music Commands", (
            "**Help Commands**\n"
            " • **/musichelp** - The list of Parzibot music commands\n\n"
            "**Connect commands**\n"
            " • **/connect** - Parzibot connects to Voice Channel\n"
            " • **/disconnect** - Parzibot disconnects from Voice Channel\n\n"
            "**Playing commands**\n"
            " • **/play** `url` - Play song in Voice Channel\n"
            " • **/replay** - Replay song in Voice Channel\n"
            " • **/pause** - Pause current song in Voice Channel\n"
            " • **/resume** - Resume current song in Voice Channel\n"
            " • **/repeats** - Enable/Disable current song repeating\n"
            " • **/next** - Play next song from Playlist\n\n"
            "**Playlist commands**\n"
            " • **/playlist** - Show number of songs and songs titles in Playlist\n"
            " • **/playlistadd** `url` - Add song to Playlist\n"
            " • **/playlistclear** - Clear all songs from Playlist\n"
            " • **/playlistshuffle** - Enable/Disable Playlist shuffling"))

    @app_commands.command(name="connect", description="Parzibot connects to Voice Channel")
    async def connect(self, interaction: discord.Interaction):
        if isinstance(interaction.user.voice, type(None)):
            await Message.music_msg(await self.bot.get_context(interaction), "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
            return

        voice = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        ctx: commands.Context = await self.bot.get_context(interaction)
        if isinstance(voice, type(None)) or not voice.is_connected():
            await interaction.user.voice.channel.connect()
            await Message.music_msg(await self.bot.get_context(interaction), "Parzibot // Connected", "**Parzibot** has been connected to **Voice Channel**")
        elif interaction.user.voice.channel != ctx.voice_client.channel: await Message.music_msg(await self.bot.get_context(interaction), "Parzibot // Connected to another", "**Parzibot** connected to another **Voice Channel**")
        else: await Message.music_msg(await self.bot.get_context(interaction), "Parzibot // Already connected", "**Parzibot** already connected to **Voice Channel**")

    @app_commands.command(name="disconnect", description="Parzibot disconnects from Voice Channel")
    async def disconnect(self, interaction: discord.Interaction):
        if isinstance(interaction.user.voice, type(None)):
            await Message.music_msg(await self.bot.get_context(interaction), "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
            return

        voice = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        ctx: commands.Context = await self.bot.get_context(interaction)
        if isinstance(voice.is_connected(), type(None)): await Message.music_msg(interaction, "Parzibot // Not connected", "**Parzibot** isn't connected to **Voice Channel**")
        elif interaction.user.voice.channel != ctx.voice_client.channel: await Message.music_msg(await self.bot.get_context(interaction), "Parzibot // Connected to another", "**Parzibot** connected to another **Voice Channel**")
        else:
            await Message.music_msg(await self.bot.get_context(interaction), "Parzibot // Disconnected", "**Parzibot** has been disconnected from **Voice Channel**")
            self.songs, self.current, self.shuffle, self.repeat = [], "", False, False
            await voice.disconnect()

    @app_commands.command(name="play", description="Play song in Voice Channel")
    @app_commands.describe(url="YouTube Video URL")
    async def play(self, interaction: discord.Interaction, url: str):
        if isinstance(interaction.user.voice, type(None)):
            await Message.music_msg(await self.bot.get_context(interaction), "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
            return

        voice = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
        ctx: commands.Context = await self.bot.get_context(interaction)
        if isinstance(voice, type(None)) or not voice.is_connected():
            await interaction.user.voice.channel.connect()
            await Message.music_msg(await self.bot.get_context(interaction), "Parzibot // Connected", "**Parzibot** has been connected to **Voice Channel**")
        elif interaction.user.voice.channel != ctx.voice_client.channel:
            await Message.music_msg(await self.bot.get_context(interaction), "Parzibot // Connected to another", "**Parzibot** connected to another **Voice Channel**")
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

            await Message.music_msg(await self.bot.get_context(interaction), "Parzibot // Play", f"**{data['title']}** is playing now")

    # @app_commands.command(name="replay", description="Replay song in Voice Channel")
    # async def replay(self, interaction: discord.Interaction):
    #     if isinstance(ctx.author.voice, type(None)):
    #         await Message.music_msg(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
    #         return
    #     elif ctx.author.voice.channel != ctx.voice_client.channel:
    #         await Message.music_msg(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
    #         return

    #     voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
    #     voice.stop()

    #     await self.replay_song(ctx)

    # async def replay_song(self, interaction: discord.Interaction):
        
    #     def search(url):
    #         with youtube_dl.YoutubeDL({"format": "bestaudio", "noplaylist": "True"}) as ydl:
    #             info = ydl.extract_info(f"ytsearch:{url}", download=False)["entries"][0]
    #         return {"source": info["formats"][0]["url"], "title": info["title"]}

    #     voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

    #     data = search(self.current)
    #     voice.play(discord.FFmpegPCMAudio(data["source"], **self.FFMPEG_OPTIONS),
    #         after=lambda e: asyncio.run_coroutine_threadsafe(self.play_song(ctx), self.client.loop))
    #     voice.is_playing()

    #     await Message.music_msg(ctx, "Parzibot // Replay", f"**{data['title']}** is playing now")

    # @app_commands.command(name="pause", description="Pause current song in Voice Channel")
    # async def pause(self, interaction: discord.Interaction):
    #     if isinstance(ctx.author.voice, type(None)):
    #         await Message.music_msg(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
    #         return
    #     elif ctx.author.voice.channel != ctx.voice_client.channel:
    #         await Message.music_msg(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
    #         return

    #     if ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
    #         return
    #     voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
    #     if voice.is_playing():
    #         voice.pause()
    #         await Message.music_msg(ctx, "Parzibot // Pause", "**Song** has been paused")
    #     else: await Message.music_msg(ctx, "Parzibot // Not playing", "**Song** isn't playing right now")

    # @app_commands.command(name="resume", description="Resume current song in Voice Channel")
    # async def resume(self, interaction: discord.Interaction):
    #     if isinstance(ctx.author.voice, type(None)):
    #         await Message.music_msg(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
    #         return
    #     elif ctx.author.voice.channel != ctx.voice_client.channel:
    #         await Message.music_msg(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
    #         return

    #     voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
    #     if voice.is_paused():
    #         voice.resume()
    #         await Message.music_msg(ctx, "Parzibot // Resume", "**Song** has been resumed")
    #     else: await Message.music_msg(ctx, "Parzibot // Not paused", "**Song** isn't paused right now")

    # @app_commands.command(name="repeats", description="Enable/Disable current song repeating")
    # async def repeats(self, interaction: discord.Interaction):
    #     if isinstance(ctx.author.voice, type(None)):
    #         await Message.music_msg(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
    #         return
    #     elif ctx.author.voice.channel != ctx.voice_client.channel:
    #         await Message.music_msg(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
    #         return

    #     self.repeat = not self.repeat
    #     if self.repeat: await Message.music_msg(ctx, "Parzibot // Repeat", "**Song** repeating is enabled")
    #     else: await Message.music_msg(ctx, "Parzibot // Repeat", "**Song** repeating is disabled")

    # @app_commands.command(name="next", description="Play next song from Playlist")
    # async def next(self, interaction: discord.Interaction):
    #     if isinstance(ctx.author.voice, type(None)):
    #         await Message.music_msg(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
    #         return
    #     elif ctx.author.voice.channel != ctx.voice_client.channel:
    #         await Message.music_msg(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
    #         return

    #     voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
    #     if self.songs: await self.play_song(ctx)
    #     else: await Message.music_msg(ctx, "Parzibot // Empty Playlist", "**Playlist** is empty")

    # @app_commands.command(name="playlist", description="Show number of songs and songs titles in Playlist")
    # async def playlist(self, interaction: discord.Interaction):
    #     if isinstance(ctx.author.voice, type(None)):
    #         await Message.music_msg(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
    #         return
    #     elif ctx.author.voice.channel != ctx.voice_client.channel:
    #         await Message.music_msg(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
    #         return

    #     if self.songs:
    #         titles = []
    #         with youtube_dl.YoutubeDL({}) as ydl: titles = [ydl.extract_info(song, download=False).get('title', None) for song in self.songs[:3]]

    #         playlist = ''.join(f'• {title}\n' for title in titles)
    #         if len(titles) >= 3: playlist = playlist + f'And {len(titles)-2} more song(-s)' 
    #         await Message.music_msg(ctx, "Parzibot // Playlist", (
    #             f"**Playlist** contains about **{len(self.songs)}** song(-s)\n\n"
    #             f"**Playlist**\n{playlist}"))
    #     else: await Message.music_msg(ctx, "Parzibot // Empty Playlist", "**Playlist** is empty")

    # @app_commands.command(name="playlistadd",
    #     description="Add song to Playlist",
    #     options=[
    #         create_option(
    #             name="url",
    #             description="YouTube Video URL",
    #             option_type=3,
    #             required=True)
    #         ])
    # async def playlistadd(self, interaction: discord.Interaction, url: str):
    #     if isinstance(ctx.author.voice, type(None)):
    #         await Message.music_msg(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
    #         return
    #     elif ctx.author.voice.channel != ctx.voice_client.channel:
    #         await Message.music_msg(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
    #         return

    #     self.songs.append(url)
    #     if self.shuffle: random.shuffle(self.songs)
    #     with youtube_dl.YoutubeDL({"format": "bestaudio", "noplaylist": "True"}) as ydl:
    #         await Message.music_msg(ctx, "Parzibot // Playlist", f"**{ydl.extract_info(url, download=False).get('title', None)}** added to **Playlist**")
        
    # @app_commands.command(name="playlistclear", description="Clear all songs from Playlist")
    # async def playlistclear(self, interaction: discord.Interaction):
    #     if isinstance(ctx.author.voice, type(None)):
    #         await Message.music_msg(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
    #         return
    #     elif ctx.author.voice.channel != ctx.voice_client.channel:
    #         await Message.music_msg(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
    #         return

    #     if self.songs:
    #         self.songs, self.current = [], ""
    #         discord.utils.get(self.client.voice_clients, guild=ctx.guild).stop()
    #         await Message.music_msg(ctx, "Parzibot // Clear Playlist", "**Playlist** has been cleared")
    #     else: await Message.music_msg(ctx, "Parzibot // Empty Playlist", "**Playlist** is empty")

    # @app_commands.command(name="playlistshuffle", description="Enable/Disable Playlist shuffling")
    # async def playlistshuffle(self, interaction: discord.Interaction):
    #     if isinstance(ctx.author.voice, type(None)):
    #         await Message.music_msg(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
    #         return
    #     elif ctx.author.voice.channel != ctx.voice_client.channel:
    #         await Message.music_msg(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
    #         return

    #     self.shuffle = not self.shuffle
    #     if self.shuffle: await Message.music_msg(ctx, "Parzibot // Shuffle", "**Playlist** shuffling is enabled")
    #     else: await Message.music_msg(ctx, "Parzibot // Shuffle", "**Playlist** shuffling is disabled")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MusicCommands(bot))

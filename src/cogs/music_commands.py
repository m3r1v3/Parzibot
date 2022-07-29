import asyncio
import random

import discord

import youtube_dl

from discord import Embed, Colour
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

from message import Message


class MusicCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}
        self.songs, self.current, self.shuffle, self.repeat = [], "", False, False

    @cog_ext.cog_slash(name="musichelp", description="The list of Parzibot music commands")
    async def musichelp(self, ctx):
        await Message.music(ctx, "Parzibot // Music Commands", (
            "**Help Commands**\n"
            " • **/musichelp** - The list of Parzibot music commands\n\n"
            "**Connect commands**\n"
            " • **/connect** - Parzibot connects to your current Voice Channel\n"
            " • **/disconnect** - Parzibot disconnects from your current Voice Channel\n\n"
            "**Playing commands**\n"
            " • **/play** `url` - Play song in your current Voice Channel\n"
            " • **/replay** - Replay song in your current Voice Channel\n"
            " • **/pause** - Pause current song in your Voice Channel\n"
            " • **/resume** - Resume current song in your Voice Channel\n"
            " • **/next** - Play next song from Playlist\n"
            " • **/repeats** - Enable/Disable current song repeating\n\n"
            "**Playlist commands**\n"
            " • **/playlist** - Show number of songs and songs titles in Playlist\n"
            " • **/playlistadd** `url` - Add song to Playlist\n"
            " • **/playlistclear** - Clear all songs from Playlist\n"
            " • **/playlistshuffle** - Enable/Disable Playlist shuffling"))

    @cog_ext.cog_slash(name="connect", description="Parzibot connects to your current Voice Channel")
    async def connect(self, ctx):
        if isinstance(ctx.author.voice, type(None)):
            await Message.music(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
            return

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if isinstance(voice, type(None)) or not voice.is_connected():
            await ctx.author.voice.channel.connect()
            await Message.music(ctx, "Parzibot // Connected", "**Parzibot** has been connected to **Voice Channel**")
        elif ctx.author.voice.channel != ctx.voice_client.channel: await Message.music(ctx, "Parzibot // Connected to another", "**Parzibot** connected to another **Voice Channel**")
        else: await Message.music(ctx, "Parzibot // Already connected", "**Parzibot** already connected to **Voice Channel**")

    @cog_ext.cog_slash(name="disconnect", description="Parzibot disconnects from your current Voice Channel")
    async def disconnect(self, ctx):
        if isinstance(ctx.author.voice, type(None)):
            await Message.music(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
            return

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if isinstance(voice.is_connected(), type(None)):
            await Message.music(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to **Voice Channel**")
        elif ctx.author.voice.channel != ctx.voice_client.channel:
            await Message.music(ctx, "Parzibot // Connected to another", "**Parzibot** connected to another **Voice Channel**")
        else:
            await Message.music(ctx, "Parzibot // Disconnected", "**Parzibot** has been disconnected from **Voice Channel**")
            self.songs, self.current, self.shuffle, self.repeat = [], "", False, False
            await voice.disconnect()

    @cog_ext.cog_slash(
        name="play",
        description="Play song in your current Voice Channel",
        options=[
            create_option(
                name="url",
                description="YouTube Video URL",
                option_type=3,
                required=True
                )
            ])
    async def play(self, ctx, url: str):
        if isinstance(ctx.author.voice, type(None)):
            await Message.music(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
            return

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if isinstance(voice, type(None)) or not voice.is_connected():
            await ctx.author.voice.channel.connect()
            await Message.music(ctx, "Parzibot // Connected", "**Parzibot** has been connected to **Voice Channel**")
        elif ctx.author.voice.channel != ctx.voice_client.channel:
            await Message.music(ctx, "Parzibot // Connected to another", "**Parzibot** connected to another **Voice Channel**")
            return

        self.songs.insert(0, url)
        await self.play_song(ctx)
        
    async def play_song(self, ctx):

        def search(url):
            with youtube_dl.YoutubeDL({"format": "bestaudio", "noplaylist": "True"}) as ydl:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)["entries"][0]
            return {"source": info["formats"][0]["url"], "title": info["title"]}

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if self.songs:
            self.current = self.songs[0]
            if not self.repeat: self.songs.pop(0)
            data = search(self.current)
            
            if voice.is_playing():
                voice.pause()
            voice.play(discord.FFmpegPCMAudio(data["source"], **self.FFMPEG_OPTIONS),
                    after=lambda e: asyncio.run_coroutine_threadsafe(self.play_song(ctx), self.client.loop))
            voice.is_playing()

            await Message.music(ctx, "Parzibot // Play", f"**{data['title']}** is playing now")

    @cog_ext.cog_slash(name="replay", description="Replay song in your current Voice Channel")
    async def replay(self, ctx):
        if isinstance(ctx.author.voice, type(None)):
            await Message.music(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
            return
        elif ctx.author.voice.channel != ctx.voice_client.channel:
            await Message.music(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
            return

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()

        await self.replay_song(ctx)

    async def replay_song(self, ctx):
        
        def search(url):
            with youtube_dl.YoutubeDL({"format": "bestaudio", "noplaylist": "True"}) as ydl:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)["entries"][0]
            return {"source": info["formats"][0]["url"], "title": info["title"]}

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        data = search(self.current)
        voice.play(discord.FFmpegPCMAudio(data["source"], **self.FFMPEG_OPTIONS),
            after=lambda e: asyncio.run_coroutine_threadsafe(self.play_song(ctx), self.client.loop))
        voice.is_playing()

        await Message.music(ctx, "Parzibot // Replay", f"**{data['title']}** is playing now")

    @cog_ext.cog_slash(name="pause", description="Pause current song in your Voice Channel")
    async def pause(self, ctx):
        if isinstance(ctx.author.voice, type(None)):
            await Message.music(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
            return
        elif ctx.author.voice.channel != ctx.voice_client.channel:
            await Message.music(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
            return

        if ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            await Message.music(ctx, "Parzibot // Pause", "**Song** has been paused")
        else: await Message.music(ctx, "Parzibot // Not playing", "**Song** isn't playing right now")

    @cog_ext.cog_slash(name="resume", description="Resume current song in your Voice Channel")
    async def resume(self, ctx):
        if isinstance(ctx.author.voice, type(None)):
            await Message.music(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
            return
        elif ctx.author.voice.channel != ctx.voice_client.channel:
            await Message.music(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
            return

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
            await Message.music(ctx, "Parzibot // Resume", "**Song** has been resumed")
        else: await Message.music(ctx, "Parzibot // Not paused", "**Song** isn't paused right now")

    @cog_ext.cog_slash(name="next", description="Play next song from Playlist")
    async def next(self, ctx):
        if isinstance(ctx.author.voice, type(None)):
            await Message.music(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
            return
        elif ctx.author.voice.channel != ctx.voice_client.channel:
            await Message.music(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
            return

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if self.songs: await self.play_song(ctx)
        else: await Message.music(ctx, "Parzibot // Empty Playlist", "**Playlist** is empty")

    @cog_ext.cog_slash(name="repeats", description="Enable/Disable current song repeating")
    async def repeats(self, ctx):
        if isinstance(ctx.author.voice, type(None)):
            await Message.music(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
            return
        elif ctx.author.voice.channel != ctx.voice_client.channel:
            await Message.music(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
            return

        self.repeat = not self.repeat
        if self.repeat: await Message.music(ctx, "Parzibot // Repeat", "**Song** repeating is enabled")
        else: await Message.music(ctx, "Parzibot // Repeat", "**Song** repeating is disabled")

    @cog_ext.cog_slash(name="playlist", description="Show number of songs and songs titles in Playlist")
    async def playlist(self, ctx):
        if isinstance(ctx.author.voice, type(None)):
            await Message.music(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
            return
        elif ctx.author.voice.channel != ctx.voice_client.channel:
            await Message.music(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
            return

        if self.songs:
            titles = []
            with youtube_dl.YoutubeDL({}) as ydl:
                for song in self.songs[:3]:
                    titles.append(ydl.extract_info(song, download=False).get('title', None))

            playlist = ''.join(f'• {title}\n' for title in titles)
            if len(titles) >= 3: playlist = playlist + f'And {len(titles)-2} more song(-s)' 
            await Message.music(ctx, "Parzibot // Playlist", (
                f"**Playlist** contains about **{len(self.songs)}** song(-s)\n\n"
                f"**Playlist**\n{playlist}"))
        else: await Message.music(ctx, "Parzibot // Empty Playlist", "**Playlist** is empty")

    @cog_ext.cog_slash(name="playlistadd",
        description="Add song to Playlist",
        options=[
            create_option(
                name="url",
                description="YouTube Video URL",
                option_type=3,
                required=True)
            ])
    async def playlistadd(self, ctx, url: str):
        if isinstance(ctx.author.voice, type(None)):
            await Message.music(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
            return
        elif ctx.author.voice.channel != ctx.voice_client.channel:
            await Message.music(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
            return

        self.songs.append(url)
        if self.shuffle: random.shuffle(self.songs)
        with youtube_dl.YoutubeDL({"format": "bestaudio", "noplaylist": "True"}) as ydl:
            await Message.music(ctx, "Parzibot // Playlist", f"**{ydl.extract_info(url, download=False).get('title', None)}** added to **Playlist**")
        
    @cog_ext.cog_slash(name="playlistclear", description="Clear all songs from Playlist")
    async def playlistclear(self, ctx):
        if isinstance(ctx.author.voice, type(None)):
            await Message.music(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
            return
        elif ctx.author.voice.channel != ctx.voice_client.channel:
            await Message.music(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
            return

        if self.songs:
            self.songs, self.current = [], ""
            discord.utils.get(self.client.voice_clients, guild=ctx.guild).stop()
            await Message.music(ctx, "Parzibot // Clear Playlist", "**Playlist** has been cleared")
        else: await Message.music(ctx, "Parzibot // Empty Playlist", "**Playlist** is empty")

    @cog_ext.cog_slash(name="playlistshuffle", description="Enable/Disable Playlist shuffling")
    async def playlistshuffle(self, ctx):
        if isinstance(ctx.author.voice, type(None)):
            await Message.music(ctx, "Parzibot // You aren't connected", "You're not connected to any **Voice Channel**")
            return
        elif ctx.author.voice.channel != ctx.voice_client.channel:
            await Message.music(ctx, "Parzibot // Not connected", "**Parzibot** isn't connected to your **Voice Channel**")
            return

        self.shuffle = not self.shuffle
        if self.shuffle: await Message.music(ctx, "Parzibot // Shuffle", "**Playlist** shuffling is enabled")
        else: await Message.music(ctx, "Parzibot // Shuffle", "**Playlist** shuffling is disabled")


def setup(client):
    client.add_cog(MusicCommands(client))

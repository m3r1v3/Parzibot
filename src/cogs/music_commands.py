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
        self.songs, self.current = [], ""

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
            " • **/repeat** - Repeat The Playlist of Songs (Soon)\n\n"
            "**Playlist commands**\n"
            " • **/playlist** - Show number of songs in Playlist\n"
            " • **/playlistclear** - Clear all songs from Playlist\n"
            " • **/playlistshuffle** - Shuffle order of songs in Playlist"))

    @cog_ext.cog_slash(name="connect", description="Parzibot connects to your current Voice Channel")
    async def connect(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if ctx.author.voice is not None and voice is None or not voice.is_connected():
            channel = ctx.author.voice.channel
            await channel.connect()
            await Message.music(ctx, "Parzibot has been connected", "**Parzibot** was connected to **Voice Channel**")
        else: await Message.music(ctx, "Parzibot already connected", "**Parzibot** already connected to **Voice Channel**")

    @cog_ext.cog_slash(name="disconnect", description="Parzibot disconnects from your current Voice Channel")
    async def disconnect(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if ctx.author.voice is None or (ctx.author.voice.channel != ctx.voice_client.channel or voice.is_connected() is None):
            await Message.music(ctx, "Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**")
        else:
            self.songs, self.current = [], ""
            await voice.disconnect()
            await Message.music(ctx, "Parzibot has left", "**Parzibot** has left **Voice Channel**")

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
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if (ctx.author.voice is None or voice is not None and ctx.author.voice.channel != ctx.voice_client.channel):
            await Message.error(ctx, "Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**")

        self.songs.append(str(url))

        channel = ctx.author.voice.channel
        if channel and channel is not None:
            if voice is not None and voice.is_connected() is not None: await voice.move_to(channel)
            else: voice = await channel.connect()

            if not voice.is_playing() or voice.is_paused(): await self.play_song(ctx)
            else: await Message.music(ctx, "Song added to playlist", "If you want to play song right now write **/next**")
        else: await Message.error(ctx, "You're not connected", "You're not connected to any **Voice Channel**")

    async def play_song(self, ctx):
        def search(url):
            with youtube_dl.YoutubeDL({"format": "bestaudio", "noplaylist": "True"}) as ydl:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)["entries"][0]
            return {"source": info["formats"][0]["url"], "title": info["title"]}

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if self.songs:
            self.current = self.songs.pop(0)
            data = search(self.current)
            
            voice.play(discord.FFmpegPCMAudio(data["source"], **self.FFMPEG_OPTIONS),
                       after=lambda e: asyncio.run_coroutine_threadsafe(self.play_song(ctx), self.client.loop))
            
            voice.is_playing()
            await Message.music(ctx, "The Song is playing", f"**{data['title']}** is playing now")

    @cog_ext.cog_slash(name="replay", description="Replay song in your current Voice Channel")
    async def replay(self, ctx):
        if (ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel):
            await Message.error(ctx, "Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**")
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
        await Message.music(ctx, "The Song is playing", f"**{data['title']}** is playing now")

    @cog_ext.cog_slash(name="pause", description="Pause current song in your Voice Channel")
    async def pause(self, ctx):
        if ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
            await Message.error(ctx, "Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**")
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            await Message.music(ctx, "The Song has been paused", "**The Song** was paused")
        else: await Message.music(ctx, "The Song isn't playing", "**The Song** isn't playing right now")

    @cog_ext.cog_slash(name="resume", description="Resume current song in your Voice Channel")
    async def resume(self, ctx):
        if ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
            await Message.error(ctx, "Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**")
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
            await Message.music(ctx, "The Song has been resumed", "**The Song** was resumed")
        else: await Message.error(ctx, "The Song isn't paused", "**The Song** isn't paused right now")

    @cog_ext.cog_slash(name="next", description="Play next song from Playlist")
    async def next(self, ctx):
        if (ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel):
            await Message.error(ctx, "Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**")
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
        if self.songs: await self.play_song(ctx)
        else: await Message.music(ctx, "The Playlist is empty", "**The Playlist** is empty now")

    @cog_ext.cog_slash(name="playlist", description="Show number of songs in Playlist")
    async def playlist(self, ctx):
        if (ctx.author.voice is None or ctx.voice_client is None or ctx.author.voice.channel != ctx.voice_client.channel):
            await Message.error(ctx, "Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**")
            return
        if self.songs: await Message.music(ctx, "The Playlist contains several songs", f"**The Playlist** contains about **{len(self.songs)}** song(-s)")
        else: await Message.music(ctx, "The Playlist is empty", "**The Playlist** is empty now")

    @cog_ext.cog_slash(name="playlistclear", description="Clear all songs from Playlist")
    async def playlistclear(self, ctx):
        if (ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel):
            await Message.music(ctx, "Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**")
        elif not self.songs:
            self.songs = []
            discord.utils.get(self.client.voice_clients, guild=ctx.guild).stop()
            await Message.music(ctx, "The Playlist has been cleared", "**The Playlist** was cleared")
        else: await Message.music(ctx, "The Playlist is empty", "**The Playlist** is already empty")

    @cog_ext.cog_slash(name="playlistshuffle", description="Shuffle order of songs in Playlist")
    async def playlistshuffle(self, ctx):
        if (ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel):
            await Message.error(ctx, "Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**")
            return
        elif self.songs:
            random.shuffle(self.songs)
            await Message.music(ctx, "The Playlist has been shuffled", "**The Playlist** was shuffled")
        else: await Message.music(ctx, "The Playlist is empty", "**The Playlist** is empty now")


def setup(client):
    """Setup function"""
    client.add_cog(MusicCommands(client))

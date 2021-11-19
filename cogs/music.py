import asyncio
import random

import discord
import youtube_dl
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option


class Music(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}
        self.queue, self.current = [], ""

    @cog_ext.cog_slash(name="join", description="Join to Your current Voice Channel")
    async def join(self, ctx):
        """Join to Your current Voice Channel"""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice is None or not voice.is_connected():
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send("**Parzibot** connected to **Voice Channel**")
        else:
            await ctx.send("**Parzibot** already connected to  **Voice Channel**")

    @cog_ext.cog_slash(name="leave", description="Leave from Voice Channel")
    async def leave(self, ctx):
        """Leave from Voice Channel"""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if ctx.author.voice.channel is None and (
                ctx.author.voice.channel == ctx.voice_client.channel or voice.is_connected() is None):
            await ctx.send("**Parzibot** isn't connected to your **Voice Channel**")
        else:
            self.queue, self.current = [], ""
            await voice.disconnect()
            await ctx.send("**Parzibot** left **Voice Channel**")

    @cog_ext.cog_slash(name="musicclear", description="Clear music queue")
    async def musicclear(self, ctx):
        """Clear music queue"""
        if (
                ctx.author.voice.channel is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            await ctx.send("**Parzibot** isn't connected to your **Voice Channel**")
        elif not self.queue:
            self.queue = []
            discord.utils.get(self.client.voice_clients, guild=ctx.guild).stop()
            await ctx.send("**The Queue** has been cleared")
        else:
            await ctx.send("**The Queue** has already been cleared")

    @cog_ext.cog_slash(name="musichelp", description="List of Parzibot Music Commands")
    async def musichelp(self, ctx):
        """List of Parzibot Music Commands"""
        await ctx.send('**Music commands**'
                       '\n\t - **/join** - Join to Your current Voice Channel'
                       '\n\t - **/leave** - Leave from Voice Channel'
                       '\n\t - **/musicclear** - Clear music queue'
                       '\n\t - **/musichelp** - List of Parzibot Music Commands'
                       '\n\t - **/musicqueue** - Number of songs in queue'
                       '\n\t - **/next** - Play next song in queue'
                       '\n\t - **/pause** - Set Song on Pause'
                       '\n\t - **/play** `url` - Play Song in Voice Channel'
                       '\n\t - **/replay** - Replay current Song'
                       '\n\t - **/resume** - Resume current Song'
                       '\n\t - **/shuffle** - Shuffle list of songs'
                       '\n\t - **/stop** - Stop current Song')

    @cog_ext.cog_slash(name="musicqueue", description="Number of songs in queue")
    async def musicqueue(self, ctx):
        await ctx.send(f"**{len(self.queue)}** songs in queue")

    @cog_ext.cog_slash(name="next", description="Play next song in queue")
    async def next(self, ctx):
        """Play next song in queue"""
        if (
                ctx.author.voice.channel is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            await ctx.send("**Parzibot** isn't connected to your **Voice Channel**")
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()

        await self.play_song(ctx)

    @cog_ext.cog_slash(name="pause", description="Set Song on Pause")
    async def pause(self, ctx):
        """Set Song on Pause"""
        if ctx.author.voice.channel is None or ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.send("**Parzibot** isn't connected to your **Voice Channel**")
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            await ctx.send("**The Song** has been paused")
        else:
            await ctx.send("**The Song** is not playing now")

    @cog_ext.cog_slash(name="play", description="Play Song in Voice Channel", options=[
        create_option(name="url", description="YouTube Video URL", option_type=3, required=True)])
    async def play(self, ctx, url: str):
        """Play Song in Voice Channel"""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        channel = ctx.author.voice.channel
        if (
                voice is not None
                and ctx.author.voice.channel != ctx.voice_client.channel
        ):
            await ctx.send("**Parzibot** isn't connected to your **Voice Channel**")
            return

        self.queue.append(str(url))

        if channel:
            if voice is not None and voice.is_connected() is not None:
                await voice.move_to(channel)
            else:
                voice = await channel.connect()

            if not voice.is_playing() or voice.is_paused():
                await self.play_song(ctx)
            else:
                await ctx.send("**The Song** added to queue. If you want to play song right now write **/next**")
        else:
            await ctx.send("You're not connected to any **Voice Channel**")

    async def play_song(self, ctx):
        def search(url):
            with youtube_dl.YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True'}) as ydl:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
            return {'source': info['formats'][0]['url'], 'title': info['title']}

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if self.queue:
            self.current = self.queue.pop(0)
            data = search(self.current)
            voice.play(discord.FFmpegPCMAudio(data['source'], **self.FFMPEG_OPTIONS),
                       after=lambda e: asyncio.run_coroutine_threadsafe(self.play_song(ctx), self.client.loop))
            voice.is_playing()
            await ctx.send(f"**{data['title']}** is playing")
        else:
            await ctx.send("**The Queue** is empty")

    @cog_ext.cog_slash(name="replay", description="Replay current Song")
    async def replay(self, ctx):
        """Replay last sound"""
        if (
                ctx.author.voice.channel is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            await ctx.send("**Parzibot** isn't connected to your **Voice Channel**")
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()

        await self.replay_song(ctx)

    async def replay_song(self, ctx):
        def search(url):
            with youtube_dl.YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True'}) as ydl:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
            return {'source': info['formats'][0]['url'], 'title': info['title']}

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        data = search(self.current)
        voice.play(discord.FFmpegPCMAudio(data['source'], **self.FFMPEG_OPTIONS),
                   after=lambda e: asyncio.run_coroutine_threadsafe(self.play_song(ctx), self.client.loop))
        voice.is_playing()
        await ctx.send(f"**{data['title']}** is playing")

    @cog_ext.cog_slash(name="resume", description="Resume current Song")
    async def resume(self, ctx):
        """Resume current Song"""
        if ctx.author.voice.channel is None or ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.send("**Parzibot** isn't connected to your **Voice Channel**")
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
            await ctx.send("**The Song** has been resumed")
        else:
            await ctx.send("**The Song** is not paused")

    @cog_ext.cog_slash(name="shuffle", description="Shuffle list of songs")
    async def shuffle(self, ctx):
        """Shuffle list of songs"""
        if (
                ctx.author.voice.channel is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            await ctx.send("**Parzibot** isn't connected to your **Voice Channel**")
        elif self.queue:
            random.shuffle(self.queue)
            await ctx.send("**The Queue** has been shuffled")
        else:
            await ctx.send("**The Queue** is empty")

    @cog_ext.cog_slash(name="stop", description="Stop current Song")
    async def stop(self, ctx):
        """Stop current Song"""
        if ctx.author.voice.channel is None or ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.send("**Parzibot** isn't connected to your **Voice Channel**")
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
        await ctx.send("**The Song** has been stopped")


def setup(client):
    """Setup function"""
    client.add_cog(Music(client))

import asyncio
import random

import discord
import youtube_dl
from discord import Embed, Colour
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
            await ctx.send(embed=Embed(title=f"**Parzibot** has been connected to **Voice Channel**",
                    color=Colour(0x59d9b9)))
        else:
            await ctx.send(embed=Embed(title=f"**Parzibot** isn't connected to your **Voice Channel**",
                    color=Colour(0xd95959)))

    @cog_ext.cog_slash(name="leave", description="Leave from Voice Channel")
    async def leave(self, ctx):
        """Leave from Voice Channel"""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if ctx.author.voice.channel is None and (
                ctx.author.voice.channel == ctx.voice_client.channel or voice.is_connected() is None):
                await ctx.send(embed=Embed(title=f"**Parzibot** isn't connected to your **Voice Channel**",
                    color=Colour(0xd95959)))
        else:
            self.queue, self.current = [], ""
            await voice.disconnect()
            await ctx.send(embed=Embed(title=f"**Parzibot** has left **Voice Channel**",
                    color=Colour(0x59d9b9)))

    @cog_ext.cog_slash(name="clearqueue", description="Clear music queue")
    async def clearqueue(self, ctx):
        """Clear music queue"""
        if (
                ctx.author.voice.channel is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            await ctx.send(embed=Embed(title=f"**Parzibot** isn't connected to your **Voice Channel**",
                    color=Colour(0xd95959)))
        elif not self.queue:
            self.queue = []
            discord.utils.get(self.client.voice_clients, guild=ctx.guild).stop()
            await ctx.send(embed=Embed(title=f"**The Queue** has been cleared",
                    color=Colour(0x59d9b9)))
        else:
            await ctx.send(embed=Embed(title=f"**The Queue** is empty",
                    color=Colour(0x59d9b9)))

    @cog_ext.cog_slash(name="musichelp", description="List of Parzibot Music Commands")
    async def musichelp(self, ctx):
        """List of Parzibot Music Commands"""
        await ctx.send(embed=Embed(title=f"Music commands",
                    description=f' - **/join** - Join to Your current Voice Channel\n'
                       ' - **/leave** - Leave from Voice Channel\n'
                       ' - **/clearqueue** - Clear music queue\n'
                       ' - **/musichelp** - List of Parzibot Music Commands\n'
                       ' - **/queue** - Number of songs in queue\n'
                       ' - **/next** - Play next song in queue\n'
                       ' - **/pause** - Set Song on Pause\n'
                       ' - **/play** `url` - Play Song in Voice Channel\n'
                       ' - **/replay** - Replay current Song\n'
                       ' - **/resume** - Resume current Song\n'
                       ' - **/shuffle** - Shuffle list of songs\n'
                       ' - **/stop** - Stop current Song\n',
                    color=Colour(0x59d9b9)))

    @cog_ext.cog_slash(name="queue", description="Number of songs in queue")
    async def queue(self, ctx):
        """Number of songs in queue"""
        if self.queue:
            await ctx.send(embed=Embed(title=f"**The Queue** contains about **{len(self.queue)}** song(-s)",
                    color=Colour(0x59d9b9)))
        else:
            await ctx.send(embed=Embed(title=f"**The Queue** is empty",
                    color=Colour(0x59d9b9)))

    @cog_ext.cog_slash(name="next", description="Play next song in queue")
    async def next(self, ctx):
        """Play next song in queue"""
        if (
                ctx.author.voice.channel is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            await ctx.send(embed=Embed(title=f"**Parzibot** isn't connected to your **Voice Channel**",
                    color=Colour(0xd95959)))
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
        if self.queue:
            await self.play_song(ctx)
        else:
            await ctx.send(embed=Embed(title=f"**The Queue** is empty",
                    color=Colour(0x59d9b9)))

    @cog_ext.cog_slash(name="pause", description="Set Song on Pause")
    async def pause(self, ctx):
        """Set Song on Pause"""
        if ctx.author.voice.channel is None or ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.send(embed=Embed(title=f"**Parzibot** isn't connected to your **Voice Channel**",
                    color=Colour(0xd95959)))
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            await ctx.send(embed=Embed(title=f"**The Song** has been paused",
                    color=Colour(0x59d9b9)))
        else:
            await ctx.send(embed=Embed(title=f"**The Song** isn't playing right now",
                    color=Colour(0x59d9b9)))

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
            await ctx.send(embed=Embed(title=f"**Parzibot** isn't connected to your **Voice Channel**",
                    color=Colour(0xd95959)))
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
                await ctx.send(embed=Embed(title=f"**The Song** added to queue",
                    description="If you want to play song right now write **/next**",
                    color=Colour(0x59d9b9)))
        else:
            await ctx.send(embed=Embed(title=f"You're not connected to any **Voice Channel**",
                    color=Colour(0xd95959)))

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
            await ctx.send(embed=Embed(title=f"**{data['title']}** is playing now",
                    color=Colour(0x59d9b9)))

    @cog_ext.cog_slash(name="replay", description="Replay current Song")
    async def replay(self, ctx):
        """Replay last sound"""
        if (
                ctx.author.voice.channel is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            await ctx.send(embed=Embed(title=f"You're not connected to any **Voice Channel**",
                    color=Colour(0xd95959)))
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
        await ctx.send(embed=Embed(title=f"**{data['title']}** is playing now",
                    color=Colour(0x59d9b9)))

    @cog_ext.cog_slash(name="resume", description="Resume current Song")
    async def resume(self, ctx):
        """Resume current Song"""
        if ctx.author.voice.channel is None or ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.send(embed=Embed(title=f"You're not connected to any **Voice Channel**",
                    color=Colour(0xd95959)))
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
            await ctx.send(embed=Embed(title=f"**The Song** has been resumed",
                    color=Colour(0x59d9b9)))
        else:
            await ctx.send(embed=Embed(title=f"**The Song** isn't paused",
                    color=Colour(0x59d9b9)))

    @cog_ext.cog_slash(name="shuffle", description="Shuffle list of songs")
    async def shuffle(self, ctx):
        """Shuffle list of songs"""
        if (
                ctx.author.voice.channel is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            await ctx.send(embed=Embed(title=f"You're not connected to any **Voice Channel**",
                    color=Colour(0xd95959)))
        elif self.queue:
            random.shuffle(self.queue)
            await ctx.send(embed=Embed(title=f"**The Queue** has been shuffled",
                    color=Colour(0x59d9b9)))
        else:
            await ctx.send(embed=Embed(title=f"**The Queue** is empty",
                    color=Colour(0x59d9b9)))

    @cog_ext.cog_slash(name="stop", description="Stop current Song")
    async def stop(self, ctx):
        """Stop current Song"""
        if ctx.author.voice.channel is None or ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.send(embed=Embed(title=f"You're not connected to any **Voice Channel**",
                    color=Colour(0xd95959)))
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
        await ctx.send(embed=Embed(title=f"**The Song** has been stopped",
                    color=Colour(0x59d9b9)))


def setup(client):
    """Setup function"""
    client.add_cog(Music(client))

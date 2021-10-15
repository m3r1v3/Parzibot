import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

import youtube_dl
import os


class Music(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.url = ""

    @cog_ext.cog_slash(name="play",
                        description="Play Song in Voice Channel",
                        options=[
                            create_option(
                                name="url",
                                description="YouTube Video URL",
                                option_type=3,
                                required=True)
                        ])
    async def play(self, ctx, url: str):
        """Play Song in Voice Channel"""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        channel = ctx.author.voice.channel
        if not voice is None and not ctx.author.voice.channel == ctx.voice_client.channel:
            await ctx.send("**Parzibot** isn't connected to your **Voice Channel**")
            return

        self.url = url

        def search(url):
            with youtube_dl.YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
            return {'source': info['formats'][0]['url'], 'title': info['title']}        

        if channel:
            if not voice is None and not voice.is_connected() is None: await voice.move_to(channel)
            else: voice = await channel.connect()

            if not voice.is_playing():
                data = search(self.url)
                voice.play(discord.FFmpegPCMAudio(data['source'], **self.FFMPEG_OPTIONS), after=await ctx.send(f"{data['title']} is ended"))
                voice.is_playing()
                await ctx.send(f"**{data['title']}** is playing")
            else: await ctx.send("**The Song** is already playing. Write **/stop** or **/pause** and try again")
        else: await ctx.send("You're not connected to any **Voice Channel**")


    @cog_ext.cog_slash(name="leave",
                        description="Leave from Voice Channel")
    async def leave(self, ctx):
        """Leave from Voice Channel"""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if not ctx.author.voice.channel is None or not ctx.author.voice.channel == ctx.voice_client.channel and not voice.is_connected() is None:
            self.url = ""
            await voice.disconnect()
            await ctx.send("**Parzibot** left **Voice Channel**")
        else: await ctx.send("**Parzibot** isn't connected to your **Voice Channel**")
    
    @cog_ext.cog_slash(name="pause",
                        description="Set Song on Pause")
    async def pause(self, ctx):
        """Set Song on Pause"""
        if ctx.author.voice.channel is None or not ctx.author.voice.channel == ctx.voice_client.channel:
            await ctx.send("**Parzibot** isn't connected to your **Voice Channel**")
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            await ctx.send("**The Song** has been paused")
        else: await ctx.send("**The Song** is not playing now")

    @cog_ext.cog_slash(name="resume",
                        description="Resume current Song")
    async def resume(self, ctx):
        """Resume current Song"""
        if ctx.author.voice.channel is None or not ctx.author.voice.channel == ctx.voice_client.channel:
            await ctx.send("**Parzibot** isn't connected to your **Voice Channel**")
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
            await ctx.send("**The Song** has been resumed")
        else: await ctx.send("**The Song** is not paused")

    @cog_ext.cog_slash(name="stop",
                        description="Stop current Song")
    async def stop(self, ctx):
        """Stop current Song"""
        if ctx.author.voice.channel is None or not ctx.author.voice.channel == ctx.voice_client.channel:
            await ctx.send("**Parzibot** isn't connected to your **Voice Channel**")
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
        await ctx.send("**The Song** has been stopped")

    @cog_ext.cog_slash(name="musichelp", description="List of Parzibot Music Commands")
    async def musichelp(self, ctx):
        """List of Parzibot Music Commands"""
        await ctx.send('**Music commands**'
                        '\n\t - **/join** - Join to Your current Voice Channel'
                        '\n\t - **/leave** - Leave from Voice Channel'
                        '\n\t - **/musichelp** - List of Parzibot Music Commands'
                        '\n\t - **/pause** - Set Song on Pause'
                        '\n\t - **/play** `url` - Play Song in Voice Channel'
                        '\n\t - **/replay** - Replay current Song'
                        '\n\t - **/resume** - Resume current Song'
                        '\n\t - **/stop** - Stop current Song')

    @cog_ext.cog_slash(name="replay", description="Replay current Song")
    async def replay(self, ctx):
        """Replay last sound"""
        if ctx.author.voice.channel is None or not ctx.author.voice.channel == ctx.voice_client.channel:
            await ctx.send("**Parzibot** isn't connected to your **Voice Channel**")
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()

        def search(url):
            global song_name
            with youtube_dl.YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
                song_name = info.get('title', None)
            return {'source': info['formats'][0]['url'], 'title': info['title']}        

        data = search(self.url)

        voice.play(discord.FFmpegPCMAudio(data['source'], **self.FFMPEG_OPTIONS), after=await ctx.send(f"{data['title']} is ended"))
        await ctx.send(f"**{data['title']}** has been replayed")

    @cog_ext.cog_slash(name="join", description="Join to Your current Voice Channel")
    async def join(self, ctx):
        """Join to Your current Voice Channel"""
        if discord.utils.get(self.client.voice_clients, guild=ctx.guild) is None or not voice.is_connected():
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send("**Parzibot** connected to **Voice Channel**")
        else: await ctx.send("**Parzibot** already connected to **Voice Channel**")


def setup(client):
    """Setup function"""
    client.add_cog(Music(client))

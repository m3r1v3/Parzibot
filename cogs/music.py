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

    @cog_ext.cog_slash(name="play",
                       description="Play music in Voice Channel",
                       options=[
                           create_option(
                               name="url",
                               description="YouTube Video URL",
                               option_type=3,
                               required=True)
                       ])
    async def play(self, ctx, url: str):
        """Play music command"""
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("**Wait for the current playing music to end or use the _/stop_ command**")
            return

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        await ctx.send("**The Song will be starting soon**")

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")       
                 
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        await ctx.send("**The Song has been started**")

    @cog_ext.cog_slash(name="leave",
                       description="Leave from Voice Channel")
    async def leave(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            if song_there: os.remove("song.mp3")
            await voice.disconnect()
            await ctx.send("**Parzibot left Voice Chat**")
        else:
            await ctx.send("**Parzibot isn't connected to a voice channel**")
    

    @cog_ext.cog_slash(name="pause",
                       description="Pause music in Voice Channel")
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            await ctx.send("**The Song has been paused**")
        else:
            await ctx.send("**Currently no song is playing**")


    @cog_ext.cog_slash(name="resume",
                       description="Resume music in Voice Channel")
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
            await ctx.send("**The Song has been resumed**")
        else:
            await ctx.send("**The Song is not paused**")

    @cog_ext.cog_slash(name="stop",
                       description="Stop music in Voice Channel")
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
        await ctx.send("**The song has been stopped**")

    @cog_ext.cog_slash(name="musichelp", description="List of Parzibot Music Commands")
    async def musichelp(self, ctx):
        """List of Parzibot commands"""
        await ctx.send('**Music commands**'
                        '\n\t - **/join** - Join to Voice Chat'
                        '\n\t - **/leave** - Leave from Voice Channel'
                        '\n\t - **/musichelp** - List of Parzibot Music Commands'
                        '\n\t - **/pause** - Pause music in Voice Channel'
                        '\n\t - **/play** `url` - Play music in Voice Channel'
                        '\n\t - **/replay** - Replay last sound'
                        '\n\t - **/resume** - Resume music in Voice Channel'
                        '\n\t - **/stop** - Stop music in Voice Channel')

    @cog_ext.cog_slash(name="replay", description="Replay last sound")
    async def replay(self, ctx):
        """Replay last sound"""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        await ctx.send("**The Song replayed**")

    @cog_ext.cog_slash(name="join", description="Join to Voice Chat")
    async def join(self, ctx):
        """Join to Voice Chat"""
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("**Parzibot connected to Voice Chat**")


def setup(client):
    """Setup function"""
    client.add_cog(Music(client))

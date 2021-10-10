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
        song_there = os.path.isfile("song.mp3")
        if song_there:
            os.remove("song.mp3")

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice is None:
            await ctx.send("**Parzibot** isn't connected to a **Voice Channel**")
            return

        await ctx.send("**The Song** will be starting soon")

        song_name = "The Song"

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            ydl.download([url])
            song_name = info_dict.get('title', None)
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")      
        
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        await ctx.send(f"**{song_name}** is playing")

    @cog_ext.cog_slash(name="leave",
                       description="Leave from Voice Channel")
    async def leave(self, ctx):
        """Leave from Voice Channel"""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            if os.path.isfile("song.mp3"): os.remove("song.mp3")
            await voice.disconnect()
            await ctx.send("**Parzibot** left **Voice Channel**")
        else:
            await ctx.send("**Parzibot** isn't connected to a **Voice Channel**")
    

    @cog_ext.cog_slash(name="pause",
                       description="Set Song on Pause")
    async def pause(self, ctx):
        """Set Song on Pause"""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            await ctx.send("**The Song** has been paused")
        else:
            await ctx.send("Currently no **Song** is playing")


    @cog_ext.cog_slash(name="resume",
                       description="Resume current Song")
    async def resume(self, ctx):
        """Resume current Song"""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
            await ctx.send("**The Song** has been resumed")
        else:
            await ctx.send("**The Song** is not paused")

    @cog_ext.cog_slash(name="stop",
                       description="Stop current Song")
    async def stop(self, ctx):
        """Stop current Song"""
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
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        await ctx.send("**The Song** replayed")

    @cog_ext.cog_slash(name="join", description="Join to Your current Voice Channel")
    async def join(self, ctx):
        """Join to Your current Voice Channel"""
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("**Parzibot** connected to **Voice Channel**")


def setup(client):
    """Setup function"""
    client.add_cog(Music(client))

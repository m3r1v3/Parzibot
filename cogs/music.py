import asyncio
import random

import discord
import youtube_dl
from discord import Embed, Colour
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice


class Music(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
            }
        self.songs, self.current = [], ""

    @staticmethod
    def get_embed(title: str, description: str):
        embed = Embed(title=title, description=description, color=Colour(0x68FFD9))
        embed.set_thumbnail(url="attachment://Parzibot.png")
        return embed

    @staticmethod
    def get_error_embed(title: str, description: str):
        embed = Embed(title=title, description=description, color=Colour(0xff6868))
        embed.set_thumbnail(url="attachment://ParzibotError.png")
        return embed

    @cog_ext.cog_slash(name="clearplaylist", description="Clear Music Playlist")
    async def clearplaylist(self, ctx):
        """Clear Music Playlist"""
        if (
            ctx.author.voice is None 
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"),
                embed=Music.get_error_embed("Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**"))
        elif not self.songs:
            self.songs = []
            discord.utils.get(self.client.voice_clients, guild=ctx.guild).stop()
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("The Playlist has been cleared", "**The Playlist** was cleared"))
        else:
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("The Playlist is empty", "**The Playlist** is already empty"))

    @cog_ext.cog_slash(name="join", description="Parzibot Joins to Your Current Voice Channel")
    async def join(self, ctx):
        """Parzibot Joins to Your Current Voice Channel"""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if ctx.author.voice is not None and voice is None or not voice.is_connected():
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("Parzibot has been connected", "**Parzibot** was connected to **Voice Channel**"))
        else:
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"),
                embed=Music.get_error_embed("Parzibot already connected", "**Parzibot** already connected to **Voice Channel**"))

    @cog_ext.cog_slash(name="leave", description="Parzibot Leaves from Your Current Voice Channel")
    async def leave(self, ctx):
        """Parzibot Leaves Your Current Voice Channel"""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if ctx.author.voice is None or (
                ctx.author.voice.channel != ctx.voice_client.channel or voice.is_connected() is None):
                await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"),
                    embed=Music.get_error_embed("Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**"))
        else:
            self.songs, self.current = [], ""
            await voice.disconnect()
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("Parzibot has left", "**Parzibot** has left **Voice Channel**"))

    @cog_ext.cog_slash(
        name="musichelp",
        description="The List of Parzibot Music Commands",
        options=[
            create_option(
                name="command",
                description="The Help Message for Specific Music Command",
                option_type=3,
                required=False,
                choices=[
                    create_choice(name="clearplaylist", value="clearplaylist"),
                    create_choice(name="join", value="join"),
                    create_choice(name="leave", value="leave"),
                    create_choice(name="musichelp", value="musichelp"),
                    create_choice(name="next", value="next"),
                    create_choice(name="pause", value="pause"),
                    create_choice(name="play", value="play"),
                    create_choice(name="playlist", value="playlist"),
                    create_choice(name="replay", value="replay"),
                    create_choice(name="resume", value="resume"),
                    create_choice(name="shuffle", value="shuffle"),                    
                    create_choice(name="stop", value="stop")
                    ])
            ])
    async def musichelp(self, ctx, command=None):
        """The List of Parzibot Music Commands"""
        if command is None:
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("Music commands", (
                    ' • **/clearplaylist** - Clear Music Playlist\n'
                    ' • **/join** - Parzibot Joins to Your Current Voice Channel\n'
                    ' • **/leave** - Parzibot Leaves Your Current Voice Channel\n'
                    ' • **/musichelp** `command` - The List of Parzibot Music Commands\n'
                    ' • **/next** - Play The Next Song in The Playlist\n'
                    ' • **/pause** - Pause The Current Song\n'
                    ' • **/play** `url` - Play The Song in The Current Voice Channel\n'
                    ' • **/playlist** - The Number of Songs in The Playlist\n'
                    ' • **/replay** - Replay The Current Song\n'
                    ' • **/resume** - Resume The Current Song\n'
                    ' • **/shuffle** - Shuffle The Playlist of Songs\n'
                    ' • **/stop** - Stop The Current Song')))
        elif command == "clearplaylist":
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("**/clearplaylist** command - Clear Music Playlist", '**Syntax:** **/clearplaylist**'))
        elif command == "join":
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("**/join** command - Parzibot Joins to Your Current Voice Channel", '**Syntax:** **/join**'))
        elif command == "leave":
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("**/leave** command - Parzibot Leaves Your Current Voice Channel", '**Syntax:** **/leave**'))
        elif command == "musichelp":
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("**/musichelp** command - The List of Parzibot Music Commands", (
                    '**Syntax:** **/musichelp** `command`\n'
                    '**Options:** `command` - The Help Message for Specific Music Command **(Optional)**')))
        elif command == "next":
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("**/next** command - Play The Next Song in The Playlist", '**Syntax:** **/next**'))
        elif command == "pause":
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("**/pause** command - Pause The Current Song", '**Syntax:** **/pause**'))
        elif command == "play":
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("**/play** command - Play The Song in The Current Voice Channel", (
                    '**Syntax:** **/play** `url`\n'
                    '**Options:** `url` - YouTube Video URL **(Required)**'
                    )))
        elif command == "playlist":
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("**/playlist** command - The Number of Songs in The Playlist", '**Syntax:** **/playlist**'))
        elif command == "replay":
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("**/replay** command - Replay The Current Song", '**Syntax:** **/replay**'))
        elif command == "resume":
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("**/resume** command - Resume The Current Song", '**Syntax:** **/resume**'))
        elif command == "shuffle":
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("**/shuffle** command - Shuffle The List of Songs", '**Syntax:** **/shuffle**'))
        elif command == "stop":
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("**/stop** command - Stop The Current Song", '**Syntax:** **/stop**'))

    @cog_ext.cog_slash(name="next", description="Play The Next Song in The Playlist")
    async def next(self, ctx):
        """Play The Next Song in The Playlist"""
        if (
            ctx.author.voice is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"),
                embed=Music.get_error_embed("Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**"))
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
        if self.songs: await self.play_song(ctx)
        else:
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("The Playlist is empty", "**The Playlist** is empty now"))

    @cog_ext.cog_slash(name="pause", description="Pause The Current Song")
    async def pause(self, ctx):
        """Pause The Current Song"""
        if ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"),
                    embed=Music.get_error_embed("Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**"))
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("The Song has been paused", "**The Song** was paused"))
        else:
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("The Song isn't playing", "**The Song** isn't playing right now"))

    @cog_ext.cog_slash(
        name="play",
        description="Play The Song in The Current Voice Channel",
        options=[
            create_option(
                name="url",
                description="YouTube Video URL",
                option_type=3,
                required=True
                )
            ])
    async def play(self, ctx, url: str):
        """Play The Song in The Current Voice Channel"""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if (
            ctx.author.voice is None or voice is not None and ctx.author.voice.channel != ctx.voice_client.channel
        ):
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"),
                embed=Music.get_error_embed("Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**"))

        self.songs.append(str(url))

        channel = ctx.author.voice.channel
        if channel and channel is not None:
            if voice is not None and voice.is_connected() is not None: 
                await voice.move_to(channel)
            else: voice = await channel.connect()

            if not voice.is_playing() or voice.is_paused(): 
                await self.play_song(ctx)
            else:
                await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                    embed=Music.get_embed("The Song added to playlist", "If you want to play song right now write **/next**"))
        else:
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"),
                embed=Music.get_error_embed("You're not connected", "You're not connected to any **Voice Channel**"))

    async def play_song(self, ctx):
        def search(url):
            with youtube_dl.YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True'}) as ydl:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
            return {'source': info['formats'][0]['url'], 'title': info['title']}

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if self.songs:
            self.current = self.songs.pop(0)
            data = search(self.current)
            
            voice.play(discord.FFmpegPCMAudio(data['source'], **self.FFMPEG_OPTIONS),
                       after=lambda e: asyncio.run_coroutine_threadsafe(self.play_song(ctx), self.client.loop))
            
            voice.is_playing()
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("The Song is playing", f"**{data['title']}** is playing now"))

    @cog_ext.cog_slash(name="playlist", description="The Number of Songs in The Playlist")
    async def playlist(self, ctx):
        """The Number of Songs in The Playlist"""
        if (
            ctx.author.voice is None or ctx.voice_client is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"),
                embed=Music.get_error_embed("Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**"))
            return
        if self.songs:
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("The Playlist contains several songs", f"**The Playlist** contains about **{len(self.songs)}** song(-s)"))
        else:
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("The Playlist is empty", "**The Playlist** is empty now"))

    @cog_ext.cog_slash(name="replay", description="Replay The Current Song")
    async def replay(self, ctx):
        """Replay The Current Song"""
        if (
            ctx.author.voice is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"),
                embed=Music.get_error_embed("Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**"))
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
        await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
            embed=Music.get_embed("The Song is playing", f"**{data['title']}** is playing now"))

    @cog_ext.cog_slash(name="resume", description="Resume The Current Song")
    async def resume(self, ctx):
        """Resume The Current Song"""
        if ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"),
                embed=Music.get_error_embed("Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**"))
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("The Song has been resumed", "**The Song** was resumed"))
        else:
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"),
                embed=Music.get_error_embed("The Song isn't paused", "**The Song** isn't paused right now"))

    @cog_ext.cog_slash(name="shuffle", description="Shuffle The Playlist of Songs")
    async def shuffle(self, ctx):
        """Shuffle The Playlist of Songs"""
        if (
            ctx.author.voice is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"),
                embed=Music.get_error_embed("Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**"))
            return
        elif self.songs:
            random.shuffle(self.songs)
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("The Playlist has been shuffled", "**The Playlist** was shuffled"))
        else:
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
                embed=Music.get_embed("The Playlist is empty", "**The Playlist** is empty now"))

    @cog_ext.cog_slash(name="stop", description="Stop The Current Song")
    async def stop(self, ctx):
        """Stop The Current Song"""
        if ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"),
                embed=Music.get_error_embed("Parzibot isn't connected", "**Parzibot** isn't connected to your **Voice Channel**"))
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
        await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"),
            embed=Music.get_embed("The Song has been stopped", "**The Song** was stopped"))


def setup(client):
    """Setup function"""
    client.add_cog(Music(client))

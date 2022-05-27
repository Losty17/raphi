import asyncio
from collections import namedtuple

import discord
import requests
import youtube_dl
from discord.ext import commands
from raphi.raphi import Raphi

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


class Queue:
    """
    A class used to represent a queue.
    This class handles all sort of Queue operations, making it easy to just
    call these methods in main.py without worrying about breaking anything in queue.
    Attributes
    ----------
    current_music_url : str
        The current url of the current music the bot is playing.
    current_music_title : str
        The current name of the current music the bot is playing.
    current_music_thumb : str
        The current thumbnail url of the current music the bot is playing.
    last_title_enqueued : str
        The title of the last music enqueued.
    queue : tuple list
        The actual queue of songs to play.
        (title, url, thumb)
    Methods
    -------
    enqueue(music_title, music_url, music_thumb)
        Handles enqueue process appending the music tuple to the queue
        while setting last_title_enqueued and the current_music variables as needed
    dequeue()
        TO DO!
        Removes the last music enqueued from the queue.
    previous()
        Goes back one place in queue, ensuring that the previous song isn't a negative index.
        current_music variables are set accordingly.
    next()
        Sets the next music in the queue as the current one.
    theres_next()
        Checks if there is a music in the queue after the current one.
    clear_queue()
        Clears the queue, resetting all variables.
    """

    def __init__(self):
        self.music = namedtuple('music', ('title', 'url', 'thumb'))
        self.current_music = self.music('', '', '')

        self.last_title_enqueued = ''
        self.queue = []

    def set_last_as_current(self):
        """
        Sets last music as current.
        :return: None
        """
        index = len(self.queue) - 1
        if index >= 0:
            self.current_music = self.queue[index]

    def enqueue(self, music_title, music_url, music_thumb):
        """
        Handles enqueue process appending the music tuple to the queue
        while setting last_title_enqueued and the current_music variables as needed
        :param music_title: str
            The music title to be added to queue
        :param music_url: str
            The music url to be added to queue
        :param music_thumb: str
            The music thumbnail url to be added to queue
        :return: None
        """
        if len(self.queue) > 0:
            self.queue.append(self.music(music_title, music_url, music_thumb))
        else:
            self.queue.append(self.music(music_title, music_url, music_thumb))
            self.current_music = self.music(
                music_title, music_url, music_thumb)

    def dequeue(self):
        pass
        # if self.queue:
        #     self.queue.pop(len(self.queue)-1)

    def previous(self):
        """
        Goes back one place in queue, ensuring that the previous song isn't a negative index.
        current_music variables are set accordingly.
        :return: None
        """
        index = self.queue.index(self.current_music) - 1
        if index > 0:
            self.current_music = self.queue[index]

    def next(self):
        """
        Sets the next music in the queue as the current one.
        :return: None
        """
        if self.current_music in self.queue:
            index = self.queue.index(self.current_music) + 1
            if len(self.queue) - 1 >= index:
                if self.current_music.title == self.queue[index].title and len(self.queue) - 1 > index + 1:
                    self.current_music = self.queue[index + 1]
                else:
                    self.current_music = self.queue[index]

        else:
            self.clear_queue()

    def theres_next(self):
        """
        Checks if there is a music in the queue after the current one.
        :return: bool
            True if there is a next song in queue.
            False if there isn't a next song in queue.
        """
        if self.queue.index(self.current_music) + 1 > len(self.queue) - 1:
            return False
        else:
            return True

    def clear_queue(self):
        """
        Clears the queue, resetting all variables.
        :return: None
        """
        self.queue.clear()
        self.current_music = self.music('', '', '')


class Session:
    """
    A class used to represent an instance of the bot.
    To avoid mixed queues when there's more than just one guild sending commands to the bot, I came up with the concept
    of sessions. Each session is identified by its guild and voice channel where the bot is connected playing audio, so
    it's impossible to send a music from one guild to another by mistake. :)
    Attributes
    ----------
    id : int
        Session's number ID.
    guild : str
        Guild's name where the bot is connected.
    channel : str
        Voice channel where the bot is connected.
    """

    def __init__(self, guild, channel, id=0):
        """
        :param guild: str
             Guild's name where the bot is connected.
        :param channel: str
            Voice channel where the bot is connected.
        :param id: int
            Session's number ID.
        """
        self.id = id
        self.guild = guild
        self.channel = channel
        self.q = Queue()


class Music(commands.Cog):
    def __init__(self, bot: Raphi) -> None:
        self.bot = bot

        self.sessions = []

    def _check_session(self, ctx):
        """
        Checks if there is a session with the same characteristics (guild and channel) as ctx param.
        :param ctx: discord.ext.commands.Context
        :return: session()
        """
        if len(self.sessions) > 0:
            for i in self.sessions:
                if i.guild == ctx.guild and i.channel == ctx.author.voice.channel:
                    return i
            session = Session(
                ctx.guild, ctx.author.voice.channel, id=len(self.sessions))
            self.sessions.append(session)
            return session
        else:
            session = Session(
                ctx.guild, ctx.author.voice.channel, id=0)
            self.sessions.append(session)
            return session

    def _prepare_continue_queue(self, ctx):
        """
        Used to call next song in queue.
        Because lambda functions cannot call async functions, I found this workaround in discord's api documentation
        to let me continue playing the queue when the current song ends.
        :param ctx: discord.ext.commands.Context
        :return: None
        """
        fut = asyncio.run_coroutine_threadsafe(
            self._continue_queue(ctx), self.bot.loop)
        try:
            fut.result()
        except Exception as e:
            print(e)

    async def _continue_queue(self, ctx):
        """
        Check if there is a next in queue then proceeds to play the next song in queue.
        As you can see, in this method we create a recursive loop using the prepare_continue_queue to make sure we pass
        through all songs in queue without any mistakes or interaction.
        :param ctx: discord.ext.commands.Context
        :return: None
        """
        session = self._check_session(ctx)
        if not session.q.theres_next():
            await ctx.send("Acabou a queue, brother.")
            return

        session.q.next()

        voice = discord.utils.get(self.bot.voice_clients, guild=session.guild)
        source = await discord.FFmpegOpusAudio.from_probe(session.q.current_music.url, **FFMPEG_OPTIONS)

        if voice.is_playing():
            voice.stop()

        voice.play(source, after=lambda e: self._prepare_continue_queue(ctx))
        await ctx.send(session.q.current_music.thumb)
        await ctx.send(f"Tocando agora: {session.q.current_music.title}")

    @commands.hybrid_command(name='play')
    async def _play(self, ctx, *, arg):
        """
        Checks where the command's author is, searches for the music required, joins the same channel as the command's
        author and then plays the audio directly from YouTube.
        :param ctx: discord.ext.commands.Context
        :param arg: str
            arg can be url to video on YouTube or just as you would search it normally.
        :return: None
        """
        try:
            voice_channel = ctx.author.voice.channel

        # If command's author isn't connected, return.
        except AttributeError as e:
            print(e)
            await ctx.send("Tu não tá conectado num canal de voz, burro")
            return

        # Finds author's session.
        session = self._check_session(ctx)

        # Searches for the video
        with youtube_dl.YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True'}) as ydl:
            try:
                requests.get(arg)
            except Exception as e:
                print(e)
                info = ydl.extract_info(f"ytsearch:{arg}", download=False)[
                    'entries'][0]
            else:
                info = ydl.extract_info(arg, download=False)

        url = info['formats'][0]['url']
        thumb = info['thumbnails'][0]['url']
        title = info['title']

        session.q.enqueue(title, url, thumb)

        # Finds an available voice client for the bot.
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if not voice:
            await voice_channel.connect()
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        # If it is already playing something, adds to the queue
        if voice.is_playing():
            await ctx.send(thumb)
            await ctx.send(f"Adicionado à queue: {title}")
            return
        else:
            await ctx.send(thumb)
            await ctx.send(f"Tocando agora: {title}")

            # Guarantees that the requested music is the current music.
            session.q.set_last_as_current()

            source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
            voice.play(
                source, after=lambda e: self._prepare_continue_queue(ctx))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Music(bot))

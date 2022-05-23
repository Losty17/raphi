from typing import Dict
import discord
import youtube_dl
import asyncio
import discord.opus as opus
from discord import Interaction, VoiceClient, app_commands
from discord.ext import commands
from raphi.raphi import Raphi

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0',
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.GroupCog, name="music", description="Music commands"):
    def __init__(self, bot: Raphi) -> None:
        self.bot = bot

        self.queue: Dict[str, str] = {}

    @app_commands.command()
    async def play(self, interaction: Interaction, *, url: str):
        """Plays from a url (almost anything youtube_dl supports)"""
        voice_client = await self.get_connection(interaction)
        if not voice_client:
            return await interaction.response.send_message("Já estou tocando música em outro canal", ephemeral=True)

        await interaction.response.defer(thinking=True)

        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)

        if not voice_client.is_playing():
            voice_client.play(player, after=self.play_next)
            await interaction.followup.send(content=f'Now playing: {player.title}')
        else:
            self.queue[player.title] = player.url
            await interaction.followup.send(content=f'Added to queue: {player.title}')

    @app_commands.command()
    async def queue(self, interaction: Interaction):
        await interaction.response.send_message('Queue:\n- ' + '\n- '.join(self.queue))

    @app_commands.command()
    async def disconnect(self, interaction: Interaction):
        try:
            await self.connection.disconnect()
            self.connection = None
        except:
            msg = 'Not connected'
        else:
            msg = 'Sucessfully disconnected'

        await interaction.response.send_message(msg, ephemeral=True)

    async def get_connection(self, interaction: Interaction) -> VoiceClient | None:
        """Must be called before every voice command

        Args:
            interaction (Interaction): the target interaction

        Returns:
            VoiceClient: the voice client
        """
        member = await interaction.guild.fetch_member(self.bot.user.id)

        self.connection = discord.utils.get(
            self.bot.voice_clients, guild=interaction.guild
        ) or await interaction.user.voice.channel.connect(self_deaf=True)

        if not member.voice.deaf:
            await member.edit(deafen=True)

        if self.connection.channel != member.voice.channel:
            return None

        # if not opus.is_loaded():
        #     opus.load_opus()

        return self.connection

    def play_next(self, e: Exception | None):
        self.connection = self.bot.loop.run_until_complete(
            self.connection.disconnect())


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Music(bot))

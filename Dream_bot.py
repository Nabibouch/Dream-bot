import os
import discord
from discord.ext import commands
import yt_dlp


Token = os.environ['Token_bot_discord']


intents = discord.Intents.default()
intents.voice_states = True
intents.messages = True
intents.guilds = True
intents.message_content = True  


bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"An error occurred: {error}")
    print(f"An error occurred: {error}")


@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You need to be in a voice channel to use this command!"
                       )


@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel!")


@bot.command()
async def play(ctx, url):
    if ctx.voice_client and not ctx.voice_client.is_playing():
        ydl_opts = {
            'format':
            'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = ""
                
                ctx.voice_client.play(
                    discord.FFmpegPCMAudio(executable="ffmpeg", source=url2))
                await ctx.send(f"Now playing: {info['title']}")
        except yt_dlp.utils.DownloadError as e:
            await ctx.send("An error occurred while trying to play the audio.")
            print(f"Download error: {e}")
    else:
        await ctx.send(
            "I'm already playing something or not connected to a voice channel!"
        )


bot.run(Token)
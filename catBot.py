from webbrowser import get
import discord
import logging
import requests
import os
from discord.ext.commands import Bot
from discord.ext import commands
import youtube_dl

TOKEN = os.getenv('BOT_TOKEN')
class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    def setup(client):
        client.add_cog(music(client))

    @commands.command()
    async def play(self, ctx, url):
        if ctx.voice_client is None:
            await ctx.send("Augustus needs help, do $join")
        await ctx.send("Augustus has been called to sing")
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format': "bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl: 
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("Augustus the all-knowing knows you aren't in a voice channel")
            return
        await ctx.send("Augustus paused time")
        await ctx.voice_client.pause()

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("Augustus the all-knowing knows you aren't in a voice channel")
            return
        await ctx.voice_client.stop()

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("Augustus the all-knowing knows you aren't in a voice channel")
            return
        await ctx.send("Augustus has resumed time")
        await ctx.voice_client.resume()

cogs = [music]
bot = Bot(command_prefix='$')

for i in range(len(cogs)):
    cogs[i].setup(bot)

logging.basicConfig(level=logging.INFO)
def get_cat():
    url = "https://api.thecatapi.com/v1/images/search"
    params = {"api_key": '835bbf24-5ec4-4d6c-bd48-6eb5d6f017f2',
            "limit": '1', "has_breeds": '1'}
    response = requests.get(url=url, params=params)
    return response.json()[0]["url"]

def get_insult():
    url = "https://insult.mattbas.org/api/insult"
    response = requests.get(url = url)
    return response.text

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("Augustus the all-knowing knows you aren't in a voice channel")
        return
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
        await ctx.send("Augustus has spawned from the deepest pits of hell to wreak havoc")
    else:
        await ctx.voice_client.move_to(voice_channel)
        await ctx.send("Augustus has moved channels")

@bot.command()
async def leave(ctx):
    if ctx.voice_client is None:
        await ctx.send("Bruh")
        return
    await ctx.voice_client.disconnect()
    await ctx.send("Augustus has decided to spare the earth another day")

@bot.command()
async def cat(ctx):
        stuff_to_send = [get_cat(), get_insult()]
        for item in stuff_to_send:
            await ctx.send(item)

@bot.command()
async def misery(ctx):
    await ctx.send("https://www.youtube.com/watch?v=vW23W0aDCjQ")

bot.run(TOKEN)

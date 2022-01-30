import disnake
from disnake.ext import commands
import requests
import youtube_dl
import asyncio
import json
import os


TOKEN = 'TOKEN'

def read_json():
    global default_stream_channel
    tmp = {}
    with open('default_streamed.json') as json_file:
        json_data = json.load(json_file)
        for i in json_data.keys():
            tmp[int(i)] = int(json_data.get(i))
    default_stream_channel = tmp


def update_json(key, value):
    global default_stream_channel
    read_json()
    default_stream_channel[int(key)] = int(value)
    with open('default_streamed.json', 'w') as json_file:
        json.dump(default_stream_channel, json_file)
    read_json()

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
exceptions = requests.exceptions
player = {}
# Follow this syntax for setting up what vc within what guild the music bot should join on playing audio, follow the same syntax in json except with guild_id as a string and channel_id_to_join as an integer.
default_stream_channel = {'guild_id': 'channel_id_to_join'}

read_json()

print(default_stream_channel)

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='?', intents=intents)
bot.remove_command("help")


@bot.group(invoke_without_command=True)
async def help(ctx):
    embed = disnake.Embed(title = "Help", description = "Use `?help <command>` for information on `<command>`", color = ctx.author.color)
    embed.add_field(name = "Music", value = "play, stop, pause, resume.")
    embed.add_field(name = "Setup", value = 'set_channel, ping, voice_ping, avg_ping, terminate.')
    await ctx.send(embed=embed)


@help.command()
async def play(ctx):
    embed = disnake.Embed(title = ctx.command, description = "Plays audio from a youtube URL in the default voice channel.", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "`?play <yt_url>`")
    embed.add_field(name = "**Aliases**", value = "`?start <yt_url>`, `?load <yt_url>`")
    await ctx.send(embed=embed)


@help.command()
async def pause(ctx):
    embed = disnake.Embed(title = ctx.command, description = "Pauses the audio played from the current voice channel session.", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "`?pause`")
    embed.add_field(name = '**Aliases**', value = '`?tempstop`, `?temp_stop`')
    await ctx.send(embed=embed)


@help.command()
async def resume(ctx):
    embed = disnake.Embed(title = ctx.command, description = "Resumes the audio played from the current voice channel session.", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "`?resume`")
    embed.add_field(name = '**Aliases**', value = '`?restart`, `?reload`')
    await ctx.send(embed=embed)


@help.command()
async def stop(ctx):
    embed = disnake.Embed(title = ctx.command, description = "Disconnects the bot from the current voice channel session.", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "`?stop`")
    embed.add_field(name = '**Aliases**', value = '`?leave`, `?disconnect`, `?close`')
    await ctx.send(embed=embed)


@help.command()
async def set_channel(ctx):
    embed = disnake.Embed(title = ctx.command, description = "Specifies the default voice channel for playing audio within the current guild.", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "`?set_channel`")
    embed.add_field(name = '**Aliases**', value = '`?add_channel`, `?default_channel`')
    await ctx.send(embed=embed)


@help.command()
async def ping(ctx):
    embed = disnake.Embed(title = ctx.command, description = "Current bot users latency.", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "`?ping`")
    embed.add_field(name = '**Aliases**', value = '`?latency`')
    await ctx.send(embed=embed)


@help.command()
async def voice_ping(ctx):
    embed = disnake.Embed(title = ctx.command, description = "Current voice connection sessions latency", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "`?voice_ping`")
    embed.add_field(name = '**Aliases**', value = '`?voice_latency`')
    await ctx.send(embed=embed)


@help.command()
async def avg_ping(ctx):
    embed = disnake.Embed(title = ctx.command, description = "Current voice connection sessions average latency.", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "`?avg_ping`")
    embed.add_field(name = '**Aliases**', value = '`?avg_latency`')
    await ctx.send(embed=embed)


@help.command()
async def terminate(ctx):
    embed = disnake.Embed(title = ctx.command, description = "Closes the bot users process.", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "`?terminate`")
    embed.add_field(name = '**Aliases**', value = '`?kill`')
    await ctx.send(embed=embed)


@help.command()
async def rm_downloads(ctx):
    embed = disnake.Embed(title = ctx.command, description = "Deletes all downloads from player.", color = ctx.author.color)
    embed.add_field(name = "**Syntax**", value = "`?rm_downloads`")
    embed.add_field(name = '**Aliases**', value = '`?remove_downloads`, `?delete_downloads`, `?clear_downloads`')
    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print(f'Ready to start laying off some beats in {len(bot.guilds)} servers for {len(bot.users)} users!')


@bot.command(aliases=('start', 'load'))
async def play(ctx, url: str):
    global default_stream_channel
    global player
    read_json()
    if default_stream_channel[ctx.guild.id] in default_stream_channel.values():
        pass
    else:
        await ctx.send(f'{ctx.author.mention} you do not have a default streaming channel, use the `?set_channel (voice_channel_id)` or set it defaulted in the code dictionary.')
        return
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.remove(file)
    try:
        requests.get(url)
    except (exceptions.MissingSchema, exceptions.RequestException,   exceptions.URLRequired, exceptions.Timeout, exceptions.SSLError, exceptions.BaseHTTPError, exceptions.ProxyError):
        await ctx.send(f'{ctx.author.mention} that is not a valid youtube video URL.')
        return
    else:
        await ctx.send(
            f'{ctx.author.mention} please go to <#{default_stream_channel[ctx.guild.id]}> and wait for the stream to start.')
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download(url_list=[url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        source = await disnake.FFmpegOpusAudio.from_probe("song.mp3")
        await ctx.send(f'{ctx.author.mention} stream has been started!')
        channel = await ctx.guild.fetch_channel(default_stream_channel[ctx.guild.id])
        session = await channel.connect()
        player[ctx.guild.id] = session
        await session.play(source)


@bot.command(aliases=('default_channel', 'add_channel'))
async def set_channel(ctx, channel_id: int):
    global default_stream_channel
    read_json()
    try:
        if 'voice' in str(type(await ctx.guild.fetch_channel(channel_id))).lower():
            pass
        else:
            raise commands.CommandInvokeError("Error")
    except (disnake.HTTPException, disnake.errors.HTTPException, disnake.ext.commands.errors.CommandInvokeError,
            commands.CommandInvokeError, commands.CommandError, AttributeError, disnake.Forbidden):
        await ctx.send(f'{ctx.author.mention} that isn\'t a valid channel id.')
        return
    else:
        update_json(ctx.guild.id, channel_id)
        await ctx.send(f"{ctx.author.mention} default streaming channel has been set to <#{channel_id}>.")


@bot.command(aliases=('tempstop', 'temp_stop'))
async def pause(ctx):
    global player
    if player.get(ctx.guild.id) in player.values():
        session_get = player[ctx.guild.id]
        await ctx.send(f'{ctx.author.mention} stream was paused.')
        player[ctx.guild.id] = await session_get.pause()
    else:
        await ctx.send(f'{ctx.author.mention} no open stream to pause.')


@bot.command(aliases=('restart', 'reload'))
async def resume(ctx):
    global player
    if player.get(ctx.guild.id) in player.values():
        session_get = player[ctx.guild.id]
        await ctx.send(f'{ctx.author.mention} stream was resumed.')
        player[ctx.guild.id] = await session_get.resume()
    else:
        await ctx.send(f'{ctx.author.mention} no open stream to resume.')


@bot.command(aliases=('disconnect', 'leave', 'stop'))
async def close(ctx):
    global player
    if player.get(ctx.guild.id) in player.values():
        session_get = player[ctx.guild.id]
        await session_get.disconnect()
        del player[ctx.guild.id]
        await ctx.send(f'{ctx.author.mention} stream was disconnected.')
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.remove(file)
    else:
        await ctx.send(f'{ctx.author.mention} no open stream to disconnect.')


@bot.event
async def on_command_error(ctx, error):
    embed = disnake.Embed(title='An error occurred:', description=f'`{error}`')
    await ctx.send(embed=embed)

@bot.command(aliases=['latency'])
async def ping(ctx):
    await asyncio.sleep(1)
    await ctx.send(f'{ctx.author.mention} {round(bot.latency * 1000)} ms.')


@bot.command(aliases=['voice_latency'])
async def voice_ping(ctx):
    await asyncio.sleep(1)
    global player
    if player.get(ctx.guild.id) in player.values():
        session_get = player[ctx.guild.id]
        await ctx.send(f'{ctx.author.mention} {round(session_get.latency * 1000)} ms voice ping.')
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.remove(file)
    else:
        await ctx.send(f'{ctx.author.mention} no open stream.')


@bot.command(aliases=['avg_latency'])
async def avg_ping(ctx):
    await asyncio.sleep(1)
    global player
    if player.get(ctx.guild.id) in player.values():
        session_get = player[ctx.guild.id]
        await ctx.send(f'{ctx.author.mention} {round(session_get.average_latency * 1000)} ms average voice ping.')
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.remove(file)
    else:
        await ctx.send(f'{ctx.author.mention} no open stream.')


@bot.command(aliases=['kill'])
async def terminate(ctx):
    await ctx.send(f'{ctx.author.mention} closing bot...')
    await bot.close()


@bot.command(aliases=('clear_downloads', 'delete_downloads', 'rm_downloads'))
async def remove_downloads(ctx):
    try:
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.remove(file)
    except (os.error.winerror, os.error.errno, os.error.strerror):
        await ctx.send(f'{ctx.author.mention} could not clear downloads.')
    else:
        await ctx.send(f'{ctx.author.mention} cleared all downloads.')


bot.run(TOKEN)

#run.py
import discord
import asyncio
from discord.ext import commands

from openpyxl import Workbook
import datetime as dt

import requests
import botToken

discord.MemberCacheFlags.all()
intents = discord.Intents.default()
intents.members = True
prefix_word = '*'
# client = discord.Client()
bot = commands.Bot(command_prefix=prefix_word, intents = intents)
soundfile_cnt = 0
channelList = []

def is_channel(ctx):   
    return ctx.channel.id in channelList

@bot.event
async def on_ready():
    channelList.append(849900505244106785)
   
@bot.event
async def on_command_error(ctx, error):
    if not is_channel(ctx):
        return
    if isinstance(error, commands.CommandNotFound):
    	await ctx.send("CommandNotFound, Invalid Command")

@bot.command(aliases = ["made"])
async def test_made(ctx):
    if not is_channel(ctx):
        return
    await ctx.send("Made by Sejin")

@bot.command()
async def leave(ctx): # Note: ?leave won't work, only ?~ will work unless you change  `name = ["~"]` to `aliases = ["~"]` so both can work.
    if (ctx.voice_client): # If the bot is in a voice channel 
        await ctx.guild.voice_client.disconnect() # Leave the channel
    else: # But if it isn't
        await ctx.send("I'm not in a voice channel, use the join command to make me join")

@bot.command()
async def command(ctx):
    await ctx.send(
    f'''-----------------------------------
command without requirements.
{prefix_word}join : join to voice channel.
{prefix_word}leave : leave to voice channel.
{prefix_word}t (message) : (message) To Speak. TTS.  
-----------------------------------'''
    )

@bot.command()
async def join(ctx):    
    if ctx.author.voice and ctx.author.voice.channel:
        if ctx.voice_client and ctx.author.voice.channel.id == ctx.voice_client.channel.id:
            await ctx.send("Already joined")
        elif ctx.voice_client and ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            await leave(ctx)
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Can't find channel")
    
@bot.command(pass_context=True, aliases = ["t"])
async def tts(ctx, *args):
    if not is_channel(ctx):
        return
    if not(ctx.author.voice and ctx.author.voice.channel):
        return

    if not ctx.voice_client:
        await join(ctx)
    if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
        if len(ctx.voice_client.channel.members) <= 2:
            await join(ctx)
        else:
            return
    if ctx.voice_client.is_playing():
        await ctx.send("아직 봇이 말하고 있어요!")
        return

    KAKAO_SECRET_KEY = '8fe999d88a71611a14ad568513311af8'
    headers = {
        #Transfer-Encoding: chunked # 보내는 양을 모를 때 헤더에 포함한다.
        'Host': 'kakaoi-newtone-openapi.kakao.com',
        'Content-Type': 'application/xml',
        'X-DSS-Service': 'DICTATION',
        'Authorization': f'KakaoAK {KAKAO_SECRET_KEY}',
    }
    voiceType = '"WOMAN_READ_CALM"'
    for role in ctx.author.roles:
        if "여자" == role.name:
            voiceType = '"WOMAN_READ_CALM"'
        elif "남자" == role.name:
            voiceType = '"MAN_READ_CALM"'
            #voiceType = '"MAN_DIALOG_BRIGHT"'
    data = '<speak><voice name=' + voiceType + '><prosody rate="slow" volume="soft">' + ' '.join(args) +'</prosody></voice></speak>'
    response = requests.post('https://kakaoi-newtone-openapi.kakao.com/v1/synthesize', headers=headers, data=data.encode('utf-8'))
    # 요청 URL과 headers, data를 post방식으로 보내준다.

    rescode = response.status_code
    print(rescode)
    if(rescode==200):
        response_body = response.content
        file_name = ""
        global soundfile_cnt
        while True:
            try :
                file_name = './soundfile/tts' + str(soundfile_cnt) + '.mp3'
                #file_name = './tts' + str(soundfile_cnt) + '.mp3'
                with open(file_name, 'wb') as f:
                    f.write(response_body)
                break
            except Exception as e :
                soundfile_cnt += 1
        await play_soundfile(ctx, file_name)
    else:
        ctx.send("TTS API Error Code:" + rescode)

tts_volume = 1.0
async def play_soundfile(ctx, file_name):
        guild = ctx.guild
        voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
        audio_source = discord.FFmpegPCMAudio(file_name)
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
        else :
            await ctx.send("아직 봇이 말하고 있어요!")

@bot.command(pass_context=True, aliases = ["leave_sub", "join_sub"])
async def passcommand(ctx):
    pass

bot.run(botToken.aman_ttsToken) #토큰

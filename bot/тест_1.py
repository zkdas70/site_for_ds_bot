import asyncio
import discord
import time
from discord.ext import commands
from config import settings
import pymorphy2
import random as ram
import string


bot = commands.Bot(command_prefix=settings['prefix'], intents=discord.Intents.all())
morph = pymorphy2.MorphAnalyzer()
sp = list(string.ascii_letters + string.digits + "!@#$%^&*()")
channel_quest = 698501707188928557
len_code = 4


@bot.event
async def on_ready():
    print('Bot connected successfully!')
    global code
    while True:
        code = ''.join([ram.choice(sp) for _ in range(len_code)])
        m = send_message(channel_quest, 7, f'Повтори код: `{code}`, и получи бонусы!')
        asyncio.run_coroutine_threadsafe(m, bot.loop)
        await asyncio.sleep(10)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == code:
        m = send_message(channel_quest, 2, f'Верно')
        asyncio.run_coroutine_threadsafe(m, bot.loop)


async def send_message(channel_id: int, n, text):
    channel = bot.get_channel(channel_id)
    await channel.send(text, delete_after=n)


bot.run(settings['token'])
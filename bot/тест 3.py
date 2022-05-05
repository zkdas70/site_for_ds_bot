import asyncio
import discord
import time
from discord.ext import commands
from config import settings
import pymorphy2
import random as ram


bot = commands.Bot(command_prefix=settings['prefix'], intents=discord.Intents.all())
slovar = {}


@bot.event
async def on_ready():
    print('Bot connected successfully!')
    for guild in bot.guilds:
        slovar[guild.name] = []
        for member in guild.members:
            slovar[guild.name] += list(member.id)


@bot.command()
async def money(ctx):
    ids = ctx.author.id
    await ctx.send(f'На вашем счёту: {slovar[ids]}')


@bot.command(name='get_money')
async def GetMoney(ctx, num=100, player=None):
    ids = ctx.author.id
    slovar[ids] += num
    await ctx.send('Успешно')


bot.run(settings['token'])
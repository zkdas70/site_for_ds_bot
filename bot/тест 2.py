import asyncio
import discord
import time
from discord.ext import commands
from config import settings
import pymorphy2
import random as ram


bot = commands.Bot(command_prefix=settings['prefix'], intents=discord.Intents.all())
morph = pymorphy2.MorphAnalyzer()
sp = []


@bot.event # Запуск бота
async def on_ready():
    print('Bot connected successfully!')


@bot.command()
async def create(ctx, id_message, reaction, role_id):
    sp.append([id_message, reaction, role_id])


@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    guild = bot.get_guild(payload.guild_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    for el in sp:
        if payload.message_id == el[0] and reaction.emoji == el[1]:
            role = discord.utils.get(guild.roles, id=el[2])
            await payload.member.add_roles(role)


bot.run(settings['token'])
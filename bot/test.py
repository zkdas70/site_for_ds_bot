import discord
from discord.ext import commands
from discord.utils import get
from config import settings


bot = commands.Bot(command_prefix=settings['prefix'], intents=discord.Intents.all())


@bot.command()
async def create_channel(ctx):
    channel = await bot.create_guild_channel()
    channel1 = bot.get_channel(channel.id)
    await channel1.send('message')


bot.run(settings['token'])
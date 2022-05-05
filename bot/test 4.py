import discord
from discord.ext import commands
from config import settings


bot = commands.Bot(command_prefix=settings['prefix'], intents=discord.Intents.all())
sp = []


@bot.event
async def on_ready():
    channel = bot.get_channel(947826579730489409)
    members = channel.members
    for member in members:
        sp.append(member.name)


bot.run(settings['token'])
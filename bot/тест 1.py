import asyncio
import discord
import time
from discord.ext import commands
from config import settings
import pymorphy2
import random as ram


bot = commands.Bot(command_prefix=settings['prefix'], intents=discord.Intents.all())
morph = pymorphy2.MorphAnalyzer()
qq = {'Какими нотами можно измерить пространство?': 'Ми-ля-ми',
      'Как можно нести воду в решете?': 'В виде льда',
      'Почему, когда хочешь спать, идёшь на кровать?': 'По полу',
      'Как написать слово «мышеловка» пятью буквами?': 'Кошка'}
sp = []
channel_quest = 698501707188928557


@bot.event # Запуск бота
async def on_ready():
    print('Bot connected successfully!')
    global questions, answer
    while True:
        questions, answer = ram.choice(list(qq.items()))
        m = send_message(channel_quest, f'Внимание! Вопрос: {questions}')
        asyncio.run_coroutine_threadsafe(m, bot.loop)
        await asyncio.sleep(10)


@bot.command()
async def question(ctx, *args):
    answer_p = ' '.join(args)
    if answer_p in answer:
        await ctx.send(f'Верно')
    else:
        await ctx.send(f'Попробуй снова')


async def send_message(channel_id: int, text):
    channel = bot.get_channel(channel_id)
    await channel.send(text, delete_after=7)


bot.run(settings['token'])
import discord
import time
import pymorphy2
import asyncio
import random as ram
from discord.ext import commands
from config import settings


bot = commands.Bot(command_prefix=settings['prefix'], intents=discord.Intents.all())
morph = pymorphy2.MorphAnalyzer()


#@bot.event
#async def on_message(message):
#    if message.author == bot.user:
#        return
#    print(message.guild.name, message.author, message.content)


@bot.event # Роль при нажатии на реакцию
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    guild = bot.get_guild(payload.guild_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    if payload.member.id == bot.user.id:
        return
    msg = 961320777435742259
    if payload.message_id == msg and reaction.emoji == '✅':
        roleid = 960208102907592704
        role = discord.utils.get(guild.roles, id=roleid)
        await payload.member.add_roles(role)
        await reaction.remove(payload.member)
    if payload.message_id == 961591210475151360 and reaction.emoji == '🏀':
        roleid = 709418474501308476
        role = discord.utils.get(guild.roles, id=roleid)
        await payload.member.add_roles(role)
        await reaction.remove(payload.member)


@bot.event # Роль при заходе на сервер
async def on_member_join(member):
    role_1 = member.guild.get_role(710983006940299337)
    await member.add_roles(role_1)
    await member.create_dm()
    await member.dm_channel.send(
        f'Привет, {member.name}!'
    )


@bot.event # Запуск бота
async def on_ready():
    print('Bot connected successfully!')
    global questions, answer
    while True:
        questions, answer = ram.choice(list(qq.items()))
        m = send_message(channel_quest, f'Внимание! Вопрос: {questions}')
        asyncio.run_coroutine_threadsafe(m, bot.loop)
        await asyncio.sleep(60)


@bot.command(name='привет') # Приветствие бота
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Приветствую, {author.mention}!') # надо сделать добрый день, вечер и ночь


@bot.command() # Генератор случайного числа с arg_1 по arg_2
async def random(ctx, arg_1: int=0, arg_2: int=100):
    try:
        text = ram.randint(arg_1, arg_2)
        await ctx.send(f'Ваше случайное число: {text}')
    except ValueError:
        await ctx.send('Рандомайзер работает только с числами')


@bot.command() # Бот переворачивает текст
async def contrary(ctx, *arg):
    text = ' '.join(arg)[::-1]
    await ctx.send(f'Ваш текст наоборот: {text}')


@bot.command() # Таймер
async def count(ctx, number:int):
    try:
        if number > 0:
            word = morph.parse('секунда')[0]
            msg = f'{number} {word.make_agree_with_number(number).word}'
            message = await ctx.send(msg)
            while number != 0:
                number -= 1
                msg = f'{number} {word.make_agree_with_number(number).word}'
                await message.edit(content=msg)
                await asyncio.sleep(1)
            await message.edit(content='Бум!')
        else:
            await ctx.send('Число отрицательное')
    except ValueError:
        await ctx.send('Таймер берёт только число')


@bot.command()
async def question(ctx, *args):
    answer_p = ' '.join(args)
    if answer_p in answer:
        await ctx.send(f'Верно')
    else:
        await ctx.send(f'Попробуй снова')


@bot.command() # Бот добавляет роль
@commands.has_guild_permissions(administrator=True)
async def role(ctx):
    member = ctx.message.author
    role_1 = member.guild.get_role(731906810071613461)
    await member.add_roles(role_1)
    await ctx.send(f'Роль успешно добавлена!')


@bot.command() # Меню помощи
async def menu(ctx):
    embed = discord.Embed(color=0xffd700, title='Меню команд')
    embed.add_field(name='hello', value='Знакомство с ботом', inline=False)
    embed.add_field(name='random', value='Получить случайное число', inline=True)
    embed.add_field(name='contrary', value='Текст наоборот', inline=False)
    embed.add_field(name='count', value='Таймер', inline=True)
    await ctx.send(embed=embed)


async def send_message(channel_id: int, text):
    channel = bot.get_channel(channel_id)
    await channel.send(text, delete_after=57)


@role.error
async def role_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send('Недостаточно прав')


bot.run(settings['token'])
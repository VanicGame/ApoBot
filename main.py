import typing
import discord
from discord.ext import commands
import random
from discord import Webhook
import os
from keep_alive import keep_alive

# Получение конфигов
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

# Константы
TOKEN = os.getenv("TOKEN")
BOT_STATUS = os.getenv("BOT_STATUS")
PREFIX = os.getenv("PREFIX")
ROLES = {
	"admin" : 1045562587934375998,
	"owner" : 957338377030598736,
}

# Функции
def FastEmbed(titl, desc):
	embed = discord.Embed(
		title = titl,
		description = desc,
		colour = 0xff99ff
	)
	return embed

# Проверка на администрацию
async def has_roles(ctx):
	for i in ctx.author.roles:
		if i.id == ROLES["admin"] or i.id == ROLES["owner"]:
			return True
	return False

# Инициализация бота
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=PREFIX, intents = intents)
print("START")

# Основной код

@client.event
async def on_ready():
	print("On ready!")
	await client.change_presence(activity=discord.Game(BOT_STATUS))

# Приветственное сообщение
async def send_hello(member):
	guild = member.guild
	embed = discord.Embed(
		title = "Приветствуем!",
		description = """*Добро пожаловать, {0.mention}!
Ты присоединился(ась) к серверу **{1.name}**.
Мы рады встретить тебя здесь!
Важные каналы, которые мы советуем прочесть:
- [правила](https://discord.com/channels/957338147577012224/957549748561256548), чтобы соблюдать атмосферу.
- [лор](https://discord.com/channels/957338147577012224/974290508010639360), чтобы быть вкурсе событий.
- [механики](https://discord.com/channels/957338147577012224/1001868191682801734), чтобы понять наши фишки.
Если есть вопросы, можешь задать их администрации.*""".format(member, guild),
		colour = 0xFFE4B5
	)
	channel = guild.get_channel(1046377785792405544) # Основной чат
	if channel  is not None:
		await channel.send(embed=embed)

@client.event
async def on_member_join(member):
	await send_hello(member)

# Приветственное сообщение
@client.command()
@commands.check(has_roles)
async def say_hello(ctx, member: discord.Member):
	"""
	Поприветствовать участника
	"""
	await send_hello(member)
@say_hello.error
async def no_error(ctx, error):
    await ctx.message.delete()
    if isinstance(error, commands.BadArgument):
        await ctx.send('Участник указан неверно!', delete_after = 5)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Укажите участника!', delete_after = 5)

# Пинг
@client.command()
async def ping(ctx):
    if round(client.latency * 1000) <= 50:
        embed=discord.Embed(title="Ping", description=f":ping_pong: Pong! The ping is **{round(client.latency *1000)}** milliseconds!", color=0x44ff44)
    elif round(client.latency * 1000) <= 100:
        embed=discord.Embed(title="Ping", description=f":ping_pong: Pong! The ping is **{round(client.latency *1000)}** milliseconds!", color=0xffd000)
    elif round(client.latency * 1000) <= 200:
        embed=discord.Embed(title="Ping", description=f":ping_pong: Pong! The ping is **{round(client.latency *1000)}** milliseconds!", color=0xff6600)
    else:
        embed=discord.Embed(title="Ping", description=f":ping_pong: Pong! The ping is **{round(client.latency *1000)}** milliseconds!", color=0x990000)
    await ctx.send(embed=embed)

# Панель
@client.command()
@commands.check(has_roles)
async def panel(ctx, t, *, s):
	"""
	Вызвать панель от имени бота
	"""
	await ctx.message.delete()
	embed = FastEmbed(t, s)
	await ctx.send(embed = embed)

# Панель
@client.command()
@commands.check(has_roles)
async def news(ctx, ping: typing.Optional[int] = 0, *, s):
	"""
	Написать новость
	"""
	await ctx.message.delete()
	embed = FastEmbed("Новости", s)
	await ctx.send(embed = embed)

# Ролл (12)
@client.command()
async def dice(ctx, modif: typing.Optional[int] = 0):
	"""
	Кинуть 12-гранный кубик
	"""
	dice = random.randint(1, 12)
	if (modif >= -11) and (modif <= 11):
		result = dice + modif
		if result < 1:
			result = 1
		if result > 12:
			result = 12
		await ctx.send(embed = FastEmbed('Dice', '<:dice:871337451627638814> ' + str(result)))
	else:
		await ctx.send(embed = FastEmbed('Error', 'Модификатор не может быть меньше -11 и больше 11'))

# Запуск
keep_alive()
client.run(TOKEN)

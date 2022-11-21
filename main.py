import typing
import discord
from discord.ext import commands
import random
from discord import Webhook
import os

# Получение конфигов
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

# Константы
TOKEN = os.getenv("TOKEN")
PREFIX = config["bot_settings"]["prefix"]
ROLES = {
	"admin" : 1033250677301985321,
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

# Пинг
@client.command()
async def ping(ctx):
	await ctx.send("pong!")

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
	await ctx.send("<@1032289885777842186>", embed = embed)

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

#keep_alive()
# Запуск
client.run(TOKEN)

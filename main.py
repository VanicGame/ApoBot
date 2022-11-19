import typing
import discord
from discord.ext import commands
import random
from discord import Webhook

# Получение конфигов
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

# Константы
TOKEN = config["bot_settings"]["token"]
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
	await ctx.message.delete()
	embed = FastEmbed(t, s)
	await ctx.send(embed = embed)

# Запуск
client.run(TOKEN)

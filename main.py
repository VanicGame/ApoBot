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
async def has_roles(ctx):
	for i in ctx.author.roles:
		if i.id == ROLES["admin"] or i.id == ROLES["owner"]:
			return True
	return False
@client.command()
@commands.check(has_roles)
async def panel(ctx, t, *, s):
	await ctx.message.delete()
	embed = FastEmbed(t, s)
	await ctx.send(embed = embed)

#Панель на вебхук
async def has_roles(ctx):
	for i in ctx.author.roles:
		if i.id == ROLES["admin"] or i.id == ROLES["owner"]:
			return True
	return False
@client.command()
@commands.check(has_roles)
async def web_panel(ctx, name, t, *, s):
	#await ctx.message.delete()
	webhook = Webhook.from_url("https://discord.com/api/webhooks/1043223473008431164/c0rIYbTQB1qhppWVV4498fg8l43wt2Jv2zLqvP3VARgWKQSxH5x2NaDfHL_hWp3wxivT")
	embed = FastEmbed(t, s)
	await webhook.send(embed = embed, username = "Заря-17", avatar_url = "https://cdn.discordapp.com/attachments/993905008766623765/1033682524691513364/IMG_20221022_142342.jpg")

# Запуск
client.run(TOKEN)

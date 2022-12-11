import typing
import discord
from discord.ext import commands
import random
import datetime
from discord import Webhook
import os
import loot
from keep_alive import keep_alive
import database
import asyncio

# Получение конфигов
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

# Константы
TOKEN = os.getenv("TOKEN")
BOT_STATUS = os.getenv("BOT_STATUS")
PREFIX = os.getenv("PREFIX")
ROLES = {
	"council" : 1048120606366900274,
	"moderator" : 1048145463599177799,
	"player" : 1048121996103393321,
	"member" : 1048127249381085226,
}

# Функции
def FastEmbed(titl, desc, colour: typing.Optional[int] = 0xb2ff7e):
	embed = discord.Embed(
		title = titl,
		description = desc,
		colour = colour
	)
	return embed

# Проверка на администрацию
async def has_roles(ctx):
	for i in ctx.author.roles:
		if i.id == ROLES["council"] or i.id == ROLES["moderator"]:
			return True
	return False

# Инициализация бота
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix=PREFIX, intents = intents, help_command = None)
print("START")

# Основной код
@client.event
async def on_ready():
	print("On ready!")
	await client.change_presence(activity=discord.Game(BOT_STATUS))

# Cogs
async def load_extensions():
	for f in os.listdir("./cogs"):
		if f.endswith(".py"):
			await client.load_extension("cogs." + f[:-3])

async def main():
	async with client:
		await load_extensions()
		await client.start(TOKEN)

# Запуск
keep_alive()
asyncio.run(main())

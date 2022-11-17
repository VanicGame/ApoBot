import typing
import discord
from discord.ext import commands
import random

# Получение конфигов
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

# Константы
TOKEN = config["bot_settings"]["token"]
PREFIX = config["bot_settings"]["prefix"]
ROLES = {
	"member" : 854338957436125275,
	"player" : 854339690290085899,
	"questionnaire_checker" : 869832826135150612,
}

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

# Запуск
client.run(TOKEN)

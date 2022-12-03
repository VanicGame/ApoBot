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
- [правила](https://discord.com/channels/1048119776662261840/1048122689010810880), чтобы соблюдать атмосферу.
- [лор](https://discord.com/channels/1048119776662261840/1048121086753124443), чтобы быть вкурсе событий.
Если есть вопросы, можешь задать их администрации.*""".format(member, guild),
		colour = 0xb2ff7e 
	)
	await member.add_roles(guild.get_role(ROLES["member"]))
	channel = guild.get_channel(1048119777291419660) # Основной чат
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
async def panel(ctx, title, *, desc):
	"""
	Вызвать панель от имени бота
	"""
	await ctx.message.delete()
	embed = FastEmbed(title, desc)
	if ctx.message.attachments != []:
		embed.set_image(url = ctx.message.attachments[0].url)
	await ctx.send(embed = embed)

@panel.error
async def panel_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send("Напишите заголовок и описание!", delete_after = 5)
		await ctx.message.delete()
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Напишите заголовок и описание!', delete_after = 5)
		await ctx.message.delete()
	if isinstance(error, commands.MissingRole):
		await ctx.send('У вас нет необходимой роли!', delete_after = 5)
		await ctx.message.delete()

# Новости
@client.command()
@commands.check(has_roles)
async def news(ctx, ping: typing.Optional[int] = 0, *, desc):
	"""
	Написать новость
	ping = 1, если надо упомянуть игроков.
	ping = 2, если надо упомянуть всех.
	"""
	await ctx.message.delete()
	embed = FastEmbed("Новости", desc, 0x97FFFF)
	if ctx.message.attachments != []:
		print(ctx.message.attachments)
		embed.set_image(url = ctx.message.attachments[0].url)
	if ping == 1:
		await ctx.send("<@&"+str(ROLES["player"])+">",embed = embed)
	elif ping == 2:
		await ctx.send("<@&"+str(ROLES["member"])+">",embed = embed)
	else:
		await ctx.send(embed = embed)

@news.error
async def news_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Напишите новость!', delete_after = 5)
		await ctx.message.delete()
	if isinstance(error, commands.MissingRole):
		await ctx.send('У вас нет необходимой роли!', delete_after = 5)
		await ctx.message.delete()

# Мут
@client.command()
async def mute(ctx, member: discord.Member, time, *, reason: typing.Optional[str] = "-"):
	embed=FastEmbed("Mute", """Участник {0.mention} был отправлен подумать о своем поведении.
Причина: {1}
Время: {2}
	""".format(member, reason, time), 0xdf260b)
	if time[-1] == "m":
		time = time[: -1]
		delta = datetime.timedelta(minutes = int(time))
	elif time[-1] == "d":
		time = time[: -1]
		delta = datetime.timedelta(days = int(time))
	elif time[-1] == "h":
		time = time[: -1]
		delta = datetime.timedelta(hours = int(time))
	else:
		await ctx.send('Проверте корректность времени!', delete_after = 5)
		await ctx.message.delete()

	await member.timeout(delta, reason=reason)
	await ctx.send(embed=embed)

@mute.error
async def mute_error(ctx, error):
	if isinstance(error, commands.BadArgument):
		await ctx.send("Проверте корректность имени участника", delete_after = 5)
		await ctx.message.delete()
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Проверте, указан ли участник и время.', delete_after = 5)
		await ctx.message.delete()
	if isinstance(error, commands.MissingRole):
		await ctx.send('У вас нет необходимой роли!', delete_after = 5)
		await ctx.message.delete()

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

# Ролл (6/6)
@client.command()
async def dice2(ctx):
	"""
	Кинуть два 6-гранных кубика
	"""
	dice1 = random.randint(1, 6)
	dice2 = random.randint(1, 6)
	if dice1 == dice2:
		await ctx.send(embed = FastEmbed('Dice', '<:dice:871337451627638814> ' + str(dice1) + " | " + str(dice2), 0xfff68f))
	else:
		await ctx.send(embed = FastEmbed('Dice', '<:dice:871337451627638814> ' + str(dice1) + " | " + str(dice2), 0xe48e6b))

# Ролл (выбор из списка)
@client.command()
async def roll(ctx, *, elements):
	"""
	Выбрать случайный элемент из списка.
	В качестве разделителя используйте ",".
	"""
	roll_list = elements.split(",")
	embed = FastEmbed("Roll", random.choice(roll_list))
	await ctx.send(embed = embed)

# Искать еду
@client.command(aliases=['loot-eat', 'l-eat', 'loot-e'])
async def looteat(ctx):
	"""
	Кинуть ролл для поиска еды.
	Шанс найти что-либо: 50%
	Шанс того, что искомое испорчено: 50%
	"""
	await loot.loot_eat(ctx)

# Искать оружие
@client.command(aliases=['loot-weapon', 'loot-weap', 'l-weapon', 'l-weap', 'loot-w'])
async def lootweapon(ctx):
	"""
	Кинуть ролл для поиска оружия.
	Из огнестрельного оружия только пистолет.
	Шанс найти что-либо: 50%
	Шанс того, что искомое сломано: 50%
	"""
	await loot.loot_weapon(ctx)

# Экономика
@client.command()
@commands.check(has_roles)
async def eco_init(ctx):
	database.recreate_table("economy")
	print("[!] economy init")

@client.command()
@commands.check(has_roles)
async def eco_insert(ctx):
	database.insert_eco_table(1, 1)
	print("[!] insert")

@client.command()
@commands.check(has_roles)
async def eco_update(ctx, value: int):
	database.update_eco_table(1, value)
	print("[!] update")

@client.command()
@commands.check(has_roles)
async def eco_print(ctx):
	print("[!] print")
	print(database.get_eco_table(1))

# Запуск
keep_alive()
client.run(TOKEN)

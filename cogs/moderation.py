import discord
from discord.ext import commands
import helper_func as hf
import typing
import datetime

class Moderation(commands.Cog, name  = "Модерация"):
	def __init__(self, client):
		self.client = client

	# Панель
	@commands.command()
	@commands.check(hf.has_roles)
	async def panel(self, ctx, title, *, desc):
		"""
		Вызвать панель от имени бота
		"""
		await ctx.message.delete()
		embed = hf.FastEmbed(title, desc)
		if ctx.message.attachments != []:
			embed.set_image(url = ctx.message.attachments[0].url)
		await ctx.send(embed = embed)
	
	@panel.error
	async def panel_error(self, ctx, error):
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
	@commands.command()
	@commands.check(hf.has_roles)
	async def news(self, ctx, ping: typing.Optional[int] = 0, *, desc):
		"""
		Написать новость
		ping = 1, если надо упомянуть игроков.
		ping = 2, если надо упомянуть всех.
		"""
		await ctx.message.delete()
		embed = hf.FastEmbed("Новости", desc, 0x97FFFF)
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
	async def news_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('Напишите новость!', delete_after = 5)
			await ctx.message.delete()
		if isinstance(error, commands.MissingRole):
			await ctx.send('У вас нет необходимой роли!', delete_after = 5)
			await ctx.message.delete()
	
	# Мут
	@commands.command()
	@commands.check(hf.has_roles)
	async def mute(self, ctx, member: discord.Member, time, *, reason: typing.Optional[str] = "-"):
		embed=hf.FastEmbed("Mute", """Участник {0.mention} был отправлен подумать о своем поведении.
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
	async def mute_error(self, ctx, error):
		if isinstance(error, commands.BadArgument):
			await ctx.send("Проверте корректность имени участника", delete_after = 5)
			await ctx.message.delete()
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('Проверте, указан ли участник и время.', delete_after = 5)
			await ctx.message.delete()
		if isinstance(error, commands.MissingRole):
			await ctx.send('У вас нет необходимой роли!', delete_after = 5)
			await ctx.message.delete()

	# Пинг
	@commands.command()
	async def ping(self, ctx):
		if round(self.client.latency * 1000) <= 50:
			embed=discord.Embed(title="Ping", description=f":ping_pong: Pong! The ping is **{round(self.client.latency *1000)}** milliseconds!", color=0x44ff44)
		elif round(self.client.latency * 1000) <= 100:
			embed=discord.Embed(title="Ping", description=f":ping_pong: Pong! The ping is **{round(self.client.latency *1000)}** milliseconds!", color=0xffd000)
		elif round(self.client.latency * 1000) <= 200:
			embed=discord.Embed(title="Ping", description=f":ping_pong: Pong! The ping is **{round(self.client.latency *1000)}** milliseconds!", color=0xff6600)
		else:
			embed=discord.Embed(title="Ping", description=f":ping_pong: Pong! The ping is **{round(self.client.latency *1000)}** milliseconds!", color=0x990000)
		await ctx.send(embed=embed)

async def setup(client):
	await client.add_cog(Moderation(client))

# Экономика

import discord
from discord.ext import commands
from DiscordDatabase import DiscordDatabase
import typing
import helper_func as hf

DB_GUILD_ID = 870561946473201674

class Economy(commands.Cog, name  = "Экономика"):
	def __init__(self, client):
		self.client = client
		self.db = DiscordDatabase(client, DB_GUILD_ID)

	# Проверить баланс
	@commands.command(aliases=['bal', 'money'])
	async def balance(self, ctx, member: typing.Optional[discord.Member] = None):
		"""
		Посмотреть свой баланс
		"""
		if member is None:
			member = ctx.author
		database = await self.db.new("db","database")
		balance = await database.get(member.id)
		embed = hf.FastEmbed("Balance", "Ваш баланс составляет {0}".format(balance))
		await ctx.send(embed=embed)

	# Инициализировать счет участника
	@commands.command()
	@commands.check(hf.has_roles)
	async def balance_init(self, ctx, member: discord.Member):
		"""
		Инициализировать счет участника
		"""
		database = await self.db.new("db","database")
		await database.set(member.id, 0)
		await ctx.send("Счет участника {0.mention} инициализирован!".format(member))

	# Добавить на счет участника
	@commands.command()
	@commands.check(hf.has_roles)
	async def balance_add(self, ctx, member: discord.Member, money: int):
		"""
		Добавить сумму на счет участника
		"""
		database = await self.db.new("db","database")
		balance = int(await database.get(member.id))
		await database.set(member.id, balance + money)
		await ctx.send("На счет участника {0.mention} добавлено {1}!".format(member, str(money)))

	# Забрать со счета участника
	@commands.command()
	@commands.check(hf.has_roles)
	async def balance_remove(self, ctx, member: discord.Member, money: int):
		"""
		Забрать сумму со счета участника
		"""
		database = await self.db.new("db","database")
		balance = int(await database.get(member.id))
		if balance - money < 0:
			await database.set(member.id, 0)
		else:
			await database.set(member.id, balance - money)
		await ctx.send("Со счета участника {0.mention} снято {1}!".format(member, str(money)))
		'''
	@commands.command()
	@commands.check(hf.has_roles)
	async def pay(self, ctx, member: discord.Member, money: int):
		"""
		Дать другому участнику денег из своего кошелька
		"""
		database = await self.db.new("db","database")
		balance = int(await database.get(member.id))
		if balance - money < 0:
			await database.set(member.id, 0)
		else:
			await database.set(member.id, balance - money)
		await ctx.send("Со счета участника {0.mention} снято {1}!".format(member, str(money)))
		'''
async def setup(client):
	await client.add_cog(Economy(client))

import discord
from discord.ext import commands
import helper_func as hf
import loot
import typing
import random

class Roll(commands.Cog, name  = "Рандомизаторы"):
	def __init__(self, client):
		self.client = client

	# Искать еду
	@commands.command(aliases=['loot-eat', 'l-eat', 'loot-e'])
	async def looteat(self, ctx):
		"""
		Кинуть ролл для поиска еды.
		Шанс найти что-либо: 50%
		Шанс того, что искомое испорчено: 50%
		"""
		await loot.loot_eat(ctx)

	# Искать оружие
	@commands.command(aliases=['loot-weapon', 'loot-weap', 'l-weapon', 'l-weap', 'loot-w'])
	async def lootweapon(self, ctx):
		"""
		Кинуть ролл для поиска оружия.
		Из огнестрельного оружия только пистолет.
		Шанс найти что-либо: 50%
		Шанс того, что искомое сломано: 50%
		"""
		await loot.loot_weapon(ctx)

		# Ролл (12)
	@commands.command()
	async def dice(self, ctx, modif: typing.Optional[int] = 0):
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
			await ctx.send(embed = hf.FastEmbed('Dice', '<:dice:871337451627638814> ' + str(result)))
		else:
			await ctx.send(embed = hf.FastEmbed('Error', 'Модификатор не может быть меньше -11 и больше 11'))

	# Ролл (6/6)
	@commands.command()
	async def dice2(self, ctx):
		"""
		Кинуть два 6-гранных кубика
		"""
		dice1 = random.randint(1, 6)
		dice2 = random.randint(1, 6)
		if dice1 == dice2:
			await ctx.send(embed = hf.FastEmbed('Dice', '<:dice:871337451627638814> ' + str(dice1) + " | " + str(dice2), 0xfff68f))
		else:
			await ctx.send(embed = hf.FastEmbed('Dice', '<:dice:871337451627638814> ' + str(dice1) + " | " + str(dice2), 0xe48e6b))

	# Ролл (выбор из списка)
	@commands.command()
	async def roll(self, ctx, *, elements):
		"""
		Выбрать случайный элемент из списка.
		В качестве разделителя используйте ",".
		"""
		roll_list = elements.split(",")
		embed = hf.FastEmbed("Roll", random.choice(roll_list))
		await ctx.send(embed = embed)

async def setup(client):
	await client.add_cog(Roll(client))

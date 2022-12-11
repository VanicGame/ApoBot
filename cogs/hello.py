import discord
from discord.ext import commands
import helper_func as hf

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
	await member.add_roles(guild.get_role(hf.ROLES["member"]))
	channel = guild.get_channel(1048119777291419660) # Основной чат
	if channel  is not None:
		await channel.send(embed=embed)

class Hello(commands.Cog, name  = "Приветствия"):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_member_join(member):
		await send_hello(member)

	# Приветственное сообщение
	@commands.command(description = "Поприветствовать участника")
	@commands.check(hf.has_roles)
	async def say_hello(self, ctx, member: discord.Member):
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

async def setup(client):
	await client.add_cog(Hello(client))

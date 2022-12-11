import itertools
from datetime import datetime as dt

import discord
from discord.ext import commands

help_icon_url = "https://media.discordapp.net/attachments/1051472606592761896/1051472751493386270/cbac96107cfde8f7.png"

class Help(commands.HelpCommand):
	def __init__(self, **options):
		super().__init__(verify_checks=True, **options)

	def embedify(self, title: str, description: str):
		"""Returns the default embed used for our HelpCommand"""
		embed = discord.Embed(title=title, description=description, color=0x2f3136, timestamp=dt.utcnow())
		embed.set_author(name="Справка", icon_url=help_icon_url)
		embed.set_footer(
			text="Вызвал: {0}".format(self.context.author),
		)
		return embed

	def command_not_found(self, string):
		return "Команда или категория `{0}` не существует.".format(string)

	def subcommand_not_found(self, command, string):
		ret = "Команда `{0}{1}` не имеет субкоманд.".format(self.context.prefix, command.qualified_name)
		if isinstance(command, commands.Group) and len(command.all_commands) > 0:
			return ret[:-2] + " named {0}".format(string)
		return ret

	@staticmethod
	def no_category():
		return "Без категории"

	def get_opening_note(self):
		return """
Используйте `{0}help "command name"` чтобы получить больше информации о команде
Так же можно использовать `{0}help "category name"`, чтобы получить больше информации о категории
		""".format(self.context.clean_prefix)

	@staticmethod
	def command_or_group(*obj):
		names = []
		for command in obj:
			if isinstance(command, commands.Group):
				names.append("Категория: *{0}*".format(command.name))
			else:
				names.append("{0}".format(command.name))
		return names

	def full_command_path(self, command, include_prefix: bool = False):
		string = "{0} {1}".format(command.qualified_name, command.signature)

		if any(command.aliases):
			string += " | Aliases: "
			string += ", ".join("`{0}`".format(alias) for alias in command.aliases)

		if include_prefix:
			string = self.context.clean_prefix + string

		return string

	async def send_bot_help(self, mapping):
		embed = self.embedify(title="**Все доступные команды**", description=self.get_opening_note())

		no_category = "\u200b{0}".format(self.no_category())

		def get_category(command, *, no_cat=no_category):
			cog = command.cog
			return cog.qualified_name if cog is not None else no_cat

		filtered = await self.filter_commands(self.context.bot.commands, sort=True, key=get_category)
		for category, cmds in itertools.groupby(filtered, key=get_category):
			if cmds:
				embed.add_field(
					name="**{0}**".format(category),
					value="`" + "`, `".join(self.command_or_group(*cmds)) + "`",
					inline=False,
				)

		await self.context.send(embed=embed)

	async def send_group_help(self, group):
		embed = self.embedify(
			title=self.full_command_path(group),
			description=group.short_doc or "*Нет описания*",
		)

		filtered = await self.filter_commands(group.commands, sort=True, key=lambda c: c.name)
		if filtered:
			for command in filtered:
				name = self.full_command_path(command)
				if isinstance(command, commands.Group):
					name = "Категория: " + name

				embed.add_field(
					name=name,
					value=command.help or "*Нет описания.*",
					inline=False,
				)

		if len(embed.fields) == 0:
			embed.add_field(name="No commands", value="This group has no commands?")

		await self.context.send(embed=embed)

	async def send_cog_help(self, cog):
		embed = self.embedify(
			title=cog.qualified_name,
			description=cog.description or "*Нет описания*",
		)

		filtered = await self.filter_commands(cog.get_commands())
		if filtered:
			for command in filtered:
				name = self.full_command_path(command)
				if isinstance(command, commands.Group):
					name = "Категория: " + name

				embed.add_field(
					name=name,
					value=command.help or "*Нет описания.*",
					inline=False,
				)

		await self.context.send(embed=embed)

	async def send_command_help(self, command):
		embed = self.embedify(
			title=self.full_command_path(command, include_prefix=True),
			description=command.help or "*Нет описания.*",
		)

		# Testing purposes only.
		try:
			await command.can_run(self.context)
		except Exception as error:
			error = getattr(error, "original", error)

			if isinstance(error, commands.MissingPermissions):
				missing_permissions = error.missing_perms
			elif isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
				missing_permissions = error.missing_roles or [error.missing_role]
			elif isinstance(error, commands.NotOwner):
				missing_permissions = None
			else:
				raise error

			if missing_permissions is not None:
				embed.add_field(
					name="Вам не хватает этих разрешений для использования команды:",
					value=self.list_to_string(missing_permissions),
				)

		await self.context.send(embed=embed)

	@staticmethod
	def list_to_string(_list):
		return ", ".join([obj.name if isinstance(obj, discord.Role) else str(obj).replace("_", " ") for obj in _list])


class NewHelp(commands.Cog, name="Help Command"):
	def __init__(self, bot):
		self._original_help_command = bot.help_command
		bot.help_command = Help()
		bot.help_command.cog = self
		bot.get_command("help").hidden = True
		self.bot = bot

	def cog_unload(self):
		self.bot.help_command = self._original_help_command


async def setup(bot):
	await bot.add_cog(NewHelp(bot))

import discord
import typing

ROLES = {
	"council" : 1048120606366900274,
	"moderator" : 1048145463599177799,
	"player" : 1048121996103393321,
	"member" : 1048127249381085226,
}

# Панель
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


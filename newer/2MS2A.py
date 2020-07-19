import sys
from discord.ext import commands
import discord
import ease_of_use as eou



# create the bot
bot = commands.Bot(command_prefix="2m.")



# define getData() and setData()
def getData():
	with open("data.json", "r") as dataFile:
		return json.loads(dataFile.read())

def setData(_in):
	with open("data.json", "w") as dataFile:
		dataFile.write(json.dumps(_in, indent=1))



# clear the console and load all the cogs
eou.clear()
cogs = getData()["cogs"]
for cog in cogs:
	bot.load_extension(cog)
	eou.log(text=("%s loaded" % cog.title()))


async def is_owner(ctx):
	return ctx.author.id == 184474965859368960


@bot.event
async def on_connect():
	eou.log(text="Connected")


@bot.event
async def on_disconnect():
	eou.log(text="Disconnected")


@bot.event
async def on_ready():
	eou.log(text="Ready")
	game = discord.Activity(type=discord.ActivityType.listening, name="2MFT")
	await bot.change_presence(status=discord.Status.online, activity=game)


@bot.command(name="reload", brief="Reload one or all of the bots cogs")
@commands.check(is_owner)
async def _reload(ctx, cog="all"):
	try:
		await ctx.message.delete()
	except:
		pass
	log = []
	cogs = getData()["cogs"]
	if cog == "all":
		for extension in cogs:
			try:
				bot.reload_extension(extension)
				log.append("**%s** reloaded successfully." % extension)
			except:
				bot.load_extension(extension)
				log.append("**%s** loaded successfully." % extension)

		embed = eou.makeEmbed(title="%s Reloaded Modules" % ctx.author.name, description="\n".join(log))
		await ctx.send(embed=embed)
		eou.log(text="Reloded all modules", ctx=ctx)
	else:
		try:
			bot.reload_extension(cog)
			await ctx.send(embed=eou.makeEmbed(title="%s Reloaded %s" % (ctx.author.name, cog), description="Successfully reloaded!"))
		except:
			bot.load_extension(cog)
			await ctx.send(embed=eou.makeEmbed(title="%s Reloaded %s" % (ctx.author.name, cog), description="Successfully loaded!"))
		eou.log(text="Reloaded %s" % cog.title(), ctx=ctx)


@_reload.error
async def _reload_error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		await ctx.send(embed=eou.makeEmbed(title="Whoops!", description="Only the bot owner can do that command."))


@bot.command(brief="Check if the bot is online")
async def ping(ctx):
	await ctx.send(embed=eou.makeEmbed(title="Pong!", description="2MS2A is online."))
	eou.log(text="Bot Pinged", ctx=ctx)


with open("T:/all 2/tokens/2MS2A.txt", "r") as token:
	bot.run(token.read())

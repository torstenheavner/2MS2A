from discord.ext import commands
from random import choice
import ease_of_use as eou
from importlib import *
import discord
import json
import os



# define getData() and setData()
def getData():
	with open("data.json", "r") as dataFile:
		return json.loads(dataFile.read())

def setData(_in):
	with open("data.json", "w") as dataFile:
		dataFile.write(json.dumps(_in, indent=4))



class Activities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

		data = getData()
		try:
			activities = data["activities"]
		except:
			data["activities"] = {}
		setData(data)



	def cog_unload(self):
		eou.log(text="Offline", cog="Activities", color="red")



	@commands.command(brief="Add an activity for you to do")
	async def addactivity(self, ctx, *, activity):
		# 2m.addactivity [activity]

		# Get data
		data = getData()

		# Attempt to get user data, create it if it doesnt exist
		try:
			userActivities = data["activities"][str(ctx.author.id)]
		except:
			data["activities"][str(ctx.author.id)] = []

		# Add the input activity to the users activities
		data["activities"][str(ctx.author.id)].append(activity)

		# Make embed object
		embed = eou.makeEmbed(title="Activity Added!" description=activity)
		embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

		# Send message, log to console, and save data
		await ctx.send(embed=embed)
		eou.log(text=f"Activity added (\"{activity}\")", cog="Activities", color="red", ctx=ctx)
		setData(data)



	@commands.command(brief="Delete an activity from your list")
	async def delactivity(self, ctx, *, activity):
		# 2m.delactivity [activity]

		# Get data
		data = getData()

		# Attempt to get user data, throw error if it doesnt exist
		try:
			userActivities = data["activities"][str(ctx.author.id)]
		except:
			embed = eou.makeEmbed(title="Whoops!", description="You don't have any activities!\nTry adding some first")
			embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			return await ctx.send(embed=embed)

		# Attempt to remove the activity, throw error if it doesnt exist
		try:
			data["activities"][str(ctx.author.id)].remove(activity)
		except:
			embed = eou.makeEmbed(title="Whoops!", description="That activity doesn't exist!\nMake sure to type in the exact value")
			embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			return await ctx.send(embed=embed)

		# Make embed object
		embed = eou.makeEmbed(title="Activity Removed!" description=activity)
		embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

		# Send message, log to console, and save data
		await ctx.send(embed=embed)
		eou.log(text=f"Activity removed (\"{activity}\")", cog="Activities", color="red", ctx=ctx)
		setData(data)



	@commands.command(brief="List all of someone's activities (yours by default)")
	async def listactivities(self, ctx, person: discord.Member=None):
		# 2m.listactivities <person>

		# Initial setup
		who = "They"
		if not person:
			person = ctx.author
			who = "You"
		data = getData()

		# Attempt to get user data, throw error if it doesnt exist
		try:
			userActivities = data["activities"][str(person.id)]
		except:
			embed = eou.makeEmbed(title="Whoops!", description=f"{who} don't have any activities")
			embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			return await ctx.send(embed=embed)

		# Make embed object
		embed = eou.makeEmbed(title=f"All of {person.name}'s Activities!" description="\n".join(userActivities))
		embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

		# Send message, log to console
		await ctx.send(embed=embed)
		eou.log(text=f"Activities listed ({person.name}'s)", cog="Activities", color="red", ctx=ctx)



	@commands.command(brief="Get an activity from your list")
	async def getactivity(self, ctx):
		# 2m.getactivity

		# Get data
		data = getData()

		# Attempt to get user data, throw error if it doesnt exist
		try:
			userActivities = data["activities"][str(ctx.author.id)]
		except:
			embed = eou.makeEmbed(title="Whoops!", description="You don't have any activities!\nTry adding some first")
			embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
			return await ctx.send(embed=embed)

		# Get activity
		activity = choice(userActivities)

		# Make embed object
		embed = eou.makeEmbed(title="Activity Retrieved!" description=activity)
		embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

		# Send message, log to console, and save data
		await ctx.send(embed=embed)
		eou.log(text=f"Activity retrieved (\"{activity}\")", cog="Activities", color="red", ctx=ctx)
		setData(data)



def setup(bot):
	eou.log(text="Online", cog="Activities", color="red")
	bot.add_cog(Activities(bot))
	reload(eou)
from discord.ext import tasks, commands
from random import randint
import ease_of_use as eou
import discord
import json
import os



# define getData() and setData()
def getData():
	with open("data.json", "r") as dataFile:
		return json.loads(dataFile.read())

def setData(_in):
	with open("data.json", "w") as dataFile:
		dataFile.write(json.dumps(_in, indent=1))



class Levels(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.hellAC = randint(1, 20)
		self.hellChannelID = 680075322884096026
		self.requiredLevelXP = [0, 300, 900, 2700, 6500, 14000, 23000, 34000, 48000, 64000, 85000, 100000, 120000, 140000, 165000, 195000, 225000, 265000, 305000, 355000]
		self.baseStats = {
			"xp": 0,
			"level": 1
		}

		self.hellACLoop.start()



	def cog_unload(self):
		self.hell_ac.cancel()
		eou.log(text="Offline", cog="Levels", color="yellow")



	# Every 5 minutes, there's a 1/3 chance that the AC of hell will be re-rolled
	@tasks.loop(minutes=5)
	async def hellACLoop(self):
		if randint(1, 100) <= 33:
			newAC = randint(1, 20)
			eou.log(text=f"Hell's AC has been re-rolled ({self.hellAC} -> {newAC})", cog="Levels", color="yellow")
			self.hellAC = newAC



	@commands.Cog.listener()
	async def on_message(self, message):
		# If the author is a bot, ignore it
		if message.author.bot: return

		# Setup stuff
		data = getData()
		totalXPGained = 0

		# Try to get the users data
		# If no data is found, give them the base stats
		try:
			userData = data["users"][message.author.id]
			level = userData["level"]
		except:
			data["users"][message.author.id] = self.baseStats
			userData = self.baseStats

		# They gain the usual amount of XP by default
		totalXPGained += randint(1, 10)

		# If the message was sent in hell
		if message.channel.id == self.hellChannelID:
			# Get their proficiency bonus, and roll a die for them
			profBonus = 2 if level < 5 else (3 if level < 9 else (4 if level < 13 else (5 if level < 17 else 6)))
			roll = randint(1, 20)

			# If they roll lower than hell's AC and didn't nat 20
			if ((roll == 1) or (roll+profBonus < self.hellAC)) and (roll != 20):
				# They get no XP
				totalXPGained = 0

				# Delete the message and announce it
				await message.delete()
				await message.channel.send(f"**{message.author.name}** failed the roll - They rolled a {roll+profBonus} ({roll}+{profBonus})")

			# If they didn't fail the roll
			else:
				# Announce if they nat 20'd
				if roll == 20:
					await message.channel.send(f"**{message.author.name}** just nat 20'd")

				# Reward bonus XP
				totalXPGained += self.ac
				if roll > 10:
					totalXPGained += randint(0, roll)

		# Add the gained XP to their actual XP, and log to console
		data["users"][message.author.id]["xp"] += totalXPGained
		eou.log(text=f"Gained XP (f{totalXPGained})", cog="Levels", color="yellow")

		# If they have enough XP to level up
		if data["users"][message.author.id]["xp"] >= self.requiredLevelXP[level]:
			# Level them up
			data["users"][message.author.id]["level"] += 1

			# Announce they level up
			embed = eou.makeEmbed(title="Level Up!", description=f"Levelled up to level {level+1}")
			embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
			await message.channel.send(embed=embed)

			# Log to console
			eou.log(text=f"Levelled up (Level {level+1})", cog="Levels", color="yellow")

		# Save the data
		setData(data)
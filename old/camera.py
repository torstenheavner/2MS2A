import random
from cv2 import *

import discord
from discord.ext import commands, tasks


class Camera(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.cam = VideoCapture(1)
		self.zoo_cam.start()

	def cog_unload(self):
		self.zoo_cam.cancel()

	@tasks.loop(seconds=3)
	async def zoo_cam(self):
		zoo_channel = discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=742994222252294144)
		s, img = self.cam.read()
		imwrite("images/camera.jpg", img)
		async for message in zoo_channel.history(limit=1):
			await message.delete()
		await zoo_channel.send(file=discord.File("images/camera.jpg"))

	# @commands.command(brief="Take a picture")
	# async def pic(self, ctx):
		# s, img = self.cam.read()
		# imwrite("images/camera.jpg", img)
		# await ctx.send(file=discord.File("images/camera.jpg"))


def setup(bot):
	bot.add_cog(Camera(bot))

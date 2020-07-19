from PIL import ImageFont, Image, ImageDraw
from discord.ext import commands
from random import choice
import ease_of_use as eou
import discord
import json



# define getData() and setData()
def getData():
	with open("data.json", "r") as dataFile:
		return json.loads(dataFile.read())

def setData(_in):
	with open("data.json", "w") as dataFile:
		dataFile.write(json.dumps(_in, indent=1))



def hexToRGB(hexIn):
	return tuple(int(hexIn[i:i + 2], 16) for i in (0, 2, 4))



class Colors(commands.Cog):
	def __init__(self, bot):
		self.bot = bot



	def cog_unload(self):
		eou.log(text="Offline", cog="Colors", color="cyan")



	# addcolor [person] [color]
	# delcolor [person]
	# testcolor [color]
	# listcolors
	# changecolor [person] [color]
	# updateroles
	# fonts
	# samplesub [person] [font] [message]

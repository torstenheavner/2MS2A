from PIL import ImageFont, Image, ImageDraw
from discord.ext import commands
from random import choice
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



def hexToRGB(hexIn):
	return tuple(int(hexIn[i:i + 2], 16) for i in (0, 2, 4))



class Colors(commands.Cog):
	def __init__(self, bot):
		self.bot = bot



	def cog_unload(self):
		eou.log(text="Offline", cog="Colors", color="cyan")



	# 2m.addcolor [person] [color]
	# 2m.delcolor [person]



	@commands.command(brief="Test a color by inputting a hex value")
	async def testcolor(self, ctx, color):
		# 2m.testcolor [color]

		# Initial setup
		try:
			await ctx.message.delete()
		except:
			pass
		if color.startsWith("#"):
			color = color[1:]

		# Define width and height of image, then get the font from a file
		width, height = 255, 115
		roboto = ImageFont.truetype("./fonts/roboto.ttf", 24)

		# Make the image object, and an object for drawing on top of it
		img = Image.new("RGB", (width, height), color=hexToRGB(color))
		draw = ImageDraw.Draw(img)

		# Make color variables for the lighter and darker shades of the color
		verylight = [((i+120) if (i+120 < 255) else 255) for i in hexToRGB(color)]
		light = [((i+60) if (i+60 < 255) else 255) for i in hexToRGB(color)]
		dark = [((i-60) if (i-60 > 0) else 0) for i in hexToRGB(color)]
		verydark = [((i-120) if (i-120 > 0) else 0) for i in hexToRGB(color)]

		# Draw text on the image, and save the image
		draw.text((7, 4), (f"#{color}").upper(), tuple(verydark), font=font1)
		draw.text((5, 2), (f"#{color}").upper(), (255, 255, 255), font=font1)
		draw.text((150, 6), ("#%02x%02x%02x" % tuple(verylight)).upper(), tuple(verylight), font=font1)
		draw.text((150, 6), ("\n#%02x%02x%02x" % tuple(light)).upper(), tuple(light), font=font1)
		draw.text((150, 6), ("\n\n#%02x%02x%02x" % tuple(dark)).upper(), tuple(dark), font=font1)
		draw.text((150, 2), ("\n\n\n#%02x%02x%02x" % tuple(verydark)).upper(), tuple(verydark), font=font1)
		img.save("./images/color.png")

		# Send the message and print output
		await ctx.send(file=discord.File("./images/color.png"))
		eou.log(text=f"Tested a color (#{color})", cog="Colors", color="cyan", ctx=ctx)



	# 2m.listcolors
	# 2m.changecolor [person] [color]
	# 2m.updateroles



	@commands.command(brief="List all available fonts")
	async def fonts(self, ctx):
		# 2m.fonts

		# Delete invocation, send the message and print output
		try:
			await ctx.message.delete()
		except:
			pass
		await ctx.send(embed=eou.makeEmbed(title=f"List of all fonts, for {ctx.author.display_name}", description="\n".join([file.split(".")[0] for file in os.listdir("./fonts")])))
		eou.log(text="Listed all fonts", cog="Colors", color="cyan", ctx=ctx)



	# 2m.samplesub [person] [font] [message]

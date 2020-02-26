import json
from random import randint

import discord
from PIL import Image, ImageDraw
from discord.ext import commands


def getData():
    with open("data.json", "r") as dataFile:
        return json.loads(dataFile.read())


def setData(data):
    with open("data.json", "w") as dataFile:
        dataFile.write(json.dumps(data, indent=2))


class Generative_Colors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def rgbtohex(self, rgb):
        return "%02x%02x%02x" % rgb

    @commands.command(brief="Generate a color.")
    async def makecolor(self, ctx):
        w, h = 100, 100
        color = tuple([randint(0, 255) for i in range(3)])
        img = Image.new("RGB", (w, h), color=color)
        draw = ImageDraw.Draw(img)
        hex = self.rgbtohex(color)
        draw.text((8, 5), "R: %s\nG: %s\nB: %s\n\n#%s" % (color[0], color[1], color[2], hex), (0, 0, 0))
        draw.text((10, 7), "R: %s\nG: %s\nB: %s\n\n#%s" % (color[0], color[1], color[2], hex), (0, 0, 0))
        draw.text((8, 7), "R: %s\nG: %s\nB: %s\n\n#%s" % (color[0], color[1], color[2], hex), (0, 0, 0))
        draw.text((10, 5), "R: %s\nG: %s\nB: %s\n\n#%s" % (color[0], color[1], color[2], hex), (0, 0, 0))
        draw.text((9, 6), "R: %s\nG: %s\nB: %s\n\n#%s" % (color[0], color[1], color[2], hex), (255, 255, 255))
        img.save("colors/generated.png")

        await ctx.send(file=discord.File("colors/generated.png"))
        print("%s GENERATED A COLOR." % ctx.author.name.upper())


def setup(bot):
    bot.add_cog(Generative_Colors(bot))

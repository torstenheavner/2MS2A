import asyncio as a
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
        self.emojis = {
            "😍": 4,
            "😁": 2,
            "🙂": 1,
            "😕": -1,
            "😟": -2,
            "🤢": -4
        }

    def rgbtohex(self, rgb):
        return "%02x%02x%02x" % rgb

    def hexToRGB(self, hexIn):
        return tuple(int(hexIn[i:i + 2], 16) for i in (0, 2, 4))

    async def dochecks(self, message, color):
        for i in range(10):
            score = 0
            cache = discord.utils.get(self.bot.cached_messages, id=message.id)

            for reaction in cache.reactions:
                score += (self.emojis[reaction.emoji] * (reaction.count - 1))

            await message.edit(content="__**#%s**__\n*SCORE: %s*\n*TIME: %s*" % (color, score, 20 - (i * 2)))
            await a.sleep(2)

        rgb = self.hexToRGB(color)
        await message.edit(content="__**#%s**__\n*SCORE: %s*" % (color, score))

    @commands.command(brief="Generate a color.")
    async def makecolor(self, ctx, ratings: bool = True):
        w, h = 100, 100
        color = tuple([randint(0, 255) for i in range(3)])
        img = Image.new("RGB", (w, h), color=color)
        draw = ImageDraw.Draw(img)
        hex = self.rgbtohex(color)
        draw.text((8, 5), "#%s" % hex, (0, 0, 0))
        draw.text((10, 7), "#%s" % hex, (0, 0, 0))
        draw.text((8, 7), "#%s" % hex, (0, 0, 0))
        draw.text((10, 5), "#%s" % hex, (0, 0, 0))
        draw.text((9, 6), "#%s" % hex, (255, 255, 255))
        img.save("colors/generated.png")

        message = await ctx.send(file=discord.File("colors/generated.png"))
        if ratings:
            for emoji in self.emojis:
                await message.add_reaction(emoji)
            await self.dochecks(message, hex)
        print("%s GENERATED A COLOR." % ctx.author.name.upper())


def setup(bot):
    bot.add_cog(Generative_Colors(bot))

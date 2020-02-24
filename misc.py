import json
import random

import discord
import numpy as np
from discord.ext import commands


def getData():
    with open("data.json", "r") as levelsFile:
        return json.loads(levelsFile.read())


def setData(_dict):
    with open("data.json", "w") as levelsFile:
        levelsFile.write(json.dumps(_dict))


class MISC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Start a poll.")
    async def poll(self, ctx, *, things=""):
        reactions = ["👍", "👎"]
        for reaction in reactions:
            await ctx.message.add_reaction(reaction)
        print("%s STARTED A POLL." % ctx.author.name.upper())

    @commands.command(brief="Send someone a message, anonymously.")
    async def message(self, ctx, person: discord.Member, message):
        if person.dm_channel:
            await person.dm_channel.send(message)
        else:
            await person.create_dm()
            await person.dm_channel.send(message)
        await ctx.send("**%s** messaged **%s**." % (ctx.author.name, person.name))
        print("%s MESSAGED %s. (\"%s\")" % (ctx.author.name.upper(), person.name.upper(), message.upper()))

    @commands.command(brief="Get a random XKCD comic.")
    async def xkcd(self, ctx):
        link = "https://xkcd.com/%s" % random.randint(1, 2270)
        await ctx.send(link)

    @commands.command(brief="Get all the banned words.")
    async def getbanned(self, ctx):
        data = getData()
        await ctx.send("__**All Banned Words:**__\n%s" % "\n".join(data["banned words"]))
        print("%s GOT ALL BANNED WORDS." % ctx.author.name.upper())

    @commands.command(brief="Add a banned word.")
    async def ban(self, ctx, word):
        data = getData()
        data["banned words"].append(word.lower())
        await ctx.send("'%s' has been banned!" % word)
        print("%s BANNED A WORD. (%s)" % (ctx.author.name.upper(), word.lower()))
        setData(data)

    @commands.command(brief="Unban a word.")
    async def unban(self, ctx, word):
        data = getData()
        if word.lower() in data["banned words"]:
            del data["banned words"][data["banned words"].index(word.lower())]
            await ctx.send("Word successfully unbanned!")
            print("%s UNBANNED A WORD. (%s)" % (ctx.author.name.upper(), word.lower()))
            setData(data)
        else:
            await ctx.send("That word isn't banned!")

    @commands.command(brief="Roll a die. (1d6 by default)")
    async def roll(self, ctx, type="1d6"):
        amount = int(type.split("d")[0])
        size = int(type.split("d")[1])
        results = []
        big = False
        total = 0
        out = []

        for die in range(amount):
            roll = random.randint(1, size)
            results.append(roll)
            total += roll

        out.append("Rolled %sd%s" % (amount, size))
        out.append("Total: %s" % total)
        out.append("Mean: %s" % np.mean(results))
        out.append("\nAll Rolls:")

        if (len("\n".join(out)) + len(", ".join([str(num) for num in results]))) > 2000:
            big = True

        if big:
            await ctx.send("\n".join(out) + "\nThe rolls are too big to display!")
        else:
            await ctx.send("\n".join(out) + "\n" + (", ".join([str(num) for num in results])))
        print("%s ROLLED %s." % (ctx.author.name.upper(), type))


def setup(bot):
    bot.add_cog(MISC(bot))
import asyncio as a
import json
import random

import discord
import numpy as np
from discord.ext import tasks, commands


def getData():
    with open("data.json", "r") as levelsFile:
        return json.loads(levelsFile.read())


def setData(_dict):
    with open("data.json", "w") as levelsFile:
        levelsFile.write(json.dumps(_dict, indent=2))


class MISC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hell_name = ["hell", "666"]
        self.ticker_channel.start()

    def cog_unload(self):
        self.ticker_channel.cancel()

    @tasks.loop(minutes=5)
    async def ticker_channel(self):
        hell = discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=680075322884096026)
        await hell.edit(name=self.hell_name[self.ticker_channel.current_loop % 2])

    @commands.command(brief="Start a rating on a message.")
    async def ratings(self, ctx):
        await ctx.message.delete()
        channel = ctx.channel
        messages = await channel.history(limit=5).flatten()
        message = messages[0]
        await message.add_reaction("⬆")
        await message.add_reaction("⬇")
        score = 0
        fame = discord.utils.get(self.bot.get_guild(677689511525875715).channels, name="hall-of-fame")
        shame = discord.utils.get(self.bot.get_guild(677689511525875715).channels, name="hall-of-shame")

        def check(reaction, user):
            return reaction.message.id == message.id

        await a.sleep(1)

        while True:
            reaction = await self.bot.wait_for("reaction_add", check=check)
            if reaction[0].emoji == "⬆":
                score += 1
            elif reaction[0].emoji == "⬇":
                score -= 1

            if score >= 5:
                await ctx.send("**%s** recieved reddit gold!" % message.author.name)
                await fame.send("**%s**: %s" % (message.author.name, message.content))
                return
            elif score <= -5:
                await ctx.send("**%s**'s post got removed by mods." % message.author.name)
                await shame.send("**%s**: %s" % (message.author.name, message.content))
                return

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

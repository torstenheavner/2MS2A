import json
import math
import sys
from random import *
import discord
from discord.ext import commands, tasks

sys.path.append("T:/all")


def getData():
    with open("data.json", "r") as levelsFile:
        return json.loads(levelsFile.read())


def setData(_dict):
    with open("data.json", "w") as levelsFile:
        levelsFile.write(json.dumps(_dict, indent=2))


class Ants(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.toaster = discord.utils.get(self.bot.get_guild(677689511525875715).members, id=184474965859368960)
        self.ants = int(self.toaster.nick.split(" ")[0])
        self.actual_ants = self.ants
        try:
            self.ant_data = getData()["ants"]
        except:
            data = getData()
            self.ant_data = {"ant_collectors": 0, "queens": 0, "ant_manufacturers": 0, "ant_summoners": 0, "better_pays": 0}
            data["ants"] = self.ant_data
            setData(data)
        self.ant_collectors = self.ant_data["ant_collectors"]
        self.queens = self.ant_data["queens"]
        self.ant_manufacturers = self.ant_data["ant_manufacturers"]
        self.ant_summoners = self.ant_data["ant_summoners"]
        self.better_pays = self.ant_data["better_pays"]
        self.five_ant_loop.start()
        self.two_ant_loop.start()
        self.ant_loop.start()

    def cog_unload(self):
        self.five_ant_loop.cancel()
        self.two_ant_loop.cancel()
        self.ant_loop.cancel()

    def get_toaster(self):
        return discord.utils.get(self.bot.get_guild(677689511525875715).members, id=184474965859368960)

    async def update(self):
        self.toaster = discord.utils.get(self.bot.get_guild(677689511525875715).members, id=184474965859368960)
        self.ants = self.actual_ants
        await self.toaster.edit(nick=("%s ants" % str(self.ants + 1)))
        data = getData()
        data["ants"] = {"ant_collectors": self.ant_collectors, "queens": self.queens, "ant_manufacturers": self.ant_manufacturers, "ant_summoners": self.ant_summoners, "better_pays": self.better_pays}
        self.ant_data = data["ants"]
        setData(data)

    async def update_from_actual(self):
        self.toaster = discord.utils.get(self.bot.get_guild(677689511525875715).members, id=184474965859368960)
        self.ants = self.actual_ants
        await self.toaster.edit(nick=("%s ants" % str(self.ants + 1)))

    def update_from_nick(self):
        self.toaster = discord.utils.get(self.bot.get_guild(677689511525875715).members, id=184474965859368960)
        self.ants = int(self.toaster.nick.split(" ")[0])
        self.actual_ants = self.ants

    @tasks.loop(seconds=5)
    async def five_ant_loop(self):
        if self.get_toaster().status == discord.Status.online:
            self.actual_ants += ((self.better_pays + 1) * self.ant_collectors)
            await self.update()

    @tasks.loop(seconds=2)
    async def two_ant_loop(self):
        if self.get_toaster().status == discord.Status.online:
            self.actual_ants += self.queens

    @tasks.loop(seconds=1)
    async def ant_loop(self):
        if self.get_toaster().status == discord.Status.online:
            self.actual_ants += self.ant_manufacturers
            self.actual_ants += self.ant_summoners * 3

    @commands.command()
    async def assets(self, ctx):
        await ctx.send("""\
__**You Own:**__
Ant Collectors: %s (%s ants per 5 seconds)
Queens: %s (%s ants per 2 seconds)
Better Pay: %s (upgrades ant collectors)
Ant Manufacturers: %s (%s ants per second)
Ant Summoners: %s (%s ants per second)
Ants / Second: %s\
""" % (self.ant_collectors, str((self.better_pays + 1) * self.ant_collectors), self.queens, self.queens, self.better_pays, self.ant_manufacturers, self.ant_manufacturers, self.ant_summoners, self.ant_summoners * 3,
       (((self.better_pays + 1) * self.ant_collectors) / 5) + (self.queens / 2) + self.ant_manufacturers + (self.ant_summoners * 3)))

    @commands.command()
    async def prices(self, ctx):
        await ctx.send("""\
__**Ant Prices**__
ant_collector: %s
queen: %s
better_pay: %s
ant_manufacturer: %s
ant_summoner: %s\
""" % (math.floor((100 + (100 * (self.ant_collectors * 0.025)))),
       math.floor((500 + (500 * (self.queens * 0.025)))),
       math.floor((1000 + (1000 * (self.better_pays * 0.025)))),
       math.floor((2000 + (2000 * (self.ant_manufacturers * 0.025)))),
       math.floor((5000 + (5000 * (self.ant_summoners * 0.025))))))

    @commands.command()
    async def buy(self, ctx, what, amount: int = 1):
        await self.update_from_actual()
        if what == "ant_collector":
            if self.actual_ants >= (math.floor(100 + (100 * (self.ant_collectors * 0.025))) * amount):
                self.actual_ants -= (math.floor(100 + (100 * (self.ant_collectors * 0.025))) * amount)
                self.ant_collectors += amount
                await ctx.send("Ant collector bought! (x%s)" % amount)
                await self.update()
            else:
                await ctx.send("You dont have enough ants for that!")
        elif what == "queen":
            if self.actual_ants >= (math.floor(500 + (500 * (self.queens * 0.025))) * amount):
                self.actual_ants -= (math.floor(500 + (500 * (self.queens * 0.025))) * amount)
                self.queens += amount
                await ctx.send("Queen ant bought! (x%s)" % amount)
                await self.update()
            else:
                await ctx.send("You dont have enough ants for that!")
        elif what == "better_pay":
            if self.actual_ants >= (math.floor(1000 + (1000 * (self.better_pays * 0.025))) * amount):
                self.actual_ants -= (math.floor(1000 + (1000 * (self.better_pays * 0.025))) * amount)
                self.better_pays += amount
                await ctx.send("Better pay bought! (x%s)" % amount)
                await self.update()
            else:
                await ctx.send("You dont have enough ants for that!")
        elif what == "ant_manufacturer":
            if self.actual_ants >= (math.floor(2000 + (2000 * (self.ant_manufacturers * 0.025))) * amount):
                self.actual_ants -= (math.floor(2000 + (2000 * (self.ant_manufacturers * 0.025))) * amount)
                self.ant_manufacturers += amount
                await ctx.send("Ant manufacturer bought! (x%s)" % amount)
                await self.update()
            else:
                await ctx.send("You dont have enough ants for that!")
        elif what == "ant_summoner":
            if self.actual_ants >= (math.floor(5000 + (5000 * (self.ant_summoners * 0.025))) * amount):
                self.actual_ants -= (math.floor(5000 + (5000 * (self.ant_summoners * 0.025))) * amount)
                self.ant_summoners += amount
                await ctx.send("Ant summoner bought! (x%s)" % amount)
                await self.update()
            else:
                await ctx.send("You dont have enough ants for that!")

    @commands.command()
    async def totalants(self, ctx):
        self.update_from_nick()
        await ctx.send(self.ants)

    @commands.command()
    async def addant(self, ctx):
        self.actual_ants += 1
        await ctx.send("**%s** added an ant to the pile" % ctx.author.name)


def setup(bot):
    bot.add_cog(Ants(bot))

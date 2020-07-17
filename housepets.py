import json
import sys

import feedparser
import discord
from discord.ext import commands, tasks

sys.path.append("T:/all")


def getData():
    with open("data.json", "r") as levelsFile:
        return json.loads(levelsFile.read())


def setData(_dict):
    with open("data.json", "w") as levelsFile:
        levelsFile.write(json.dumps(_dict, indent=2))


class Housepets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lastcomic = ""
        self.housepets.start()

    def cog_unload(self):
        self.housepets.cancel()

    @tasks.loop(minutes=1)
    async def housepets(self):
        feed = feedparser.parse("https://www.housepetscomic.com/feed/")
        if self.lastcomic != feed.entries[0].title:
            self.lastcomic = feed.entries[0].title
            embed = discord.Embed(title="New Housepets Comic!", description="**%s**" % feed.entries[0].title, color=0x7289DA)
            embed.set_image(url=(feed.entries[0].content[0].value.split("src=\"")[1]).split("\"")[0])
            housepets_channel = discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=696584576990183434)
            await housepets_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Housepets(bot))

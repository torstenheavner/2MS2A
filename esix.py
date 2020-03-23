import shutil
from random import *

import discord
import requests
from discord.ext import commands


class ESIX(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief=";)")
    async def gimme(self, ctx, amount: int = 1, *, tags="rating:s"):
        tags = tags.split(" ")
        if amount > 5:
            return await ctx.send("You can only get 5 images maximum!")
        r = requests.get(url="https://e621.net/posts.json?tags=%s" % "+".join(tags), params={"limit": 500}, headers={"User-Agent": "2MS2A Discord Bot", "From": "torstenheavner@gmail.com"})
        data = r.json()
        posts = data["posts"]
        files = []
        for i in range(amount):
            url = choice(posts)["file"]["url"]
            with open("images/%sesix%s.jpg" % ("SPOILER_" if "rating:s" not in tags else "", i), "wb") as file:
                resp = requests.get(url, stream=True)
                resp.raw.decode_content = True
                shutil.copyfileobj(resp.raw, file)
                files.append("%sesix%s.jpg" % ("SPOILER_" if "rating:s" not in tags else "", i))
        await ctx.send(files=[discord.File("images/%s" % image) for image in files])
        print("%S GOT AN IMAGE FROM E6." % ctx.author.name.upper())

    @commands.command(brief=";) (but bully people)")
    async def yiff(self, ctx, person: discord.Member, message="", *, tags="rating:s"):
        tags = tags.split(" ")
        r = requests.get(url="https://e621.net/posts.json?tags=%s" % "+".join(tags), params={"limit": 500}, headers={"User-Agent": "2MS2A Discord Bot", "From": "torstenheavner@gmail.com"})
        data = r.json()
        posts = data["posts"]
        post = choice(posts)["file"]["url"]
        file = "images/%sesix0.jpg" % ("SPOILER_" if "rating:s" not in tags else "")
        with open(file, "wb") as the_file:
            resp = requests.get(post, stream=True)
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, the_file)
        if person.dm_channel:
            await person.dm_channel.send(message, file=discord.File(file))
        else:
            await person.create_dm()
            await person.dm_channel.send(message, file=discord.File(file))
        if person.name == ctx.author.name:
            await ctx.send("**%s** yiffed themself!" % ctx.author.name)
        else:
            await ctx.send("**%s** yiffed **%s**!" % (ctx.author.name, person.name))
        print("%s JUST YIFFED %s." % (ctx.author.name.upper(), person.name.upper()))

    @commands.command(brief="")
    async def fuck(self, ctx):
        await ctx.send(choice(["yes.", "you know what? maybe i will.", "not today.", "maybe.", "make me.", " ."]))
        print("%s fuck" % ctx.author.name.upper())


def setup(bot):
    bot.add_cog(ESIX(bot))

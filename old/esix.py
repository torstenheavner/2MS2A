import shutil
from random import *

import re
import feedparser
import discord
import requests
from discord.ext import commands, tasks


class ESIX(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lastcomment = ""
        # self.e6rss.start()

    # def cog_unload(self):
    #     self.e6rss.cancel()

    @tasks.loop(seconds=5)
    async def e6rss(self):
        feed = feedparser.parse("https://e621.net/comments.atom")
        if self.lastcomment != feed.entries[0].link:
            self.lastcomment = feed.entries[0].link
            furry_channel = discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=702979666029314138)
            blockquote = re.compile("(<blockquote>)|(</blockquote>)|(&quot;)")
            linebreak = re.compile("(<br>)|(<br/>)|(<br />)")
            clean = re.compile("<.*?>")
            embed = discord.Embed(title="New comment from %s!" % feed.entries[0].author_detail.name, description=re.sub(clean, "", re.sub(linebreak, "\n", re.sub(blockquote, "\"", feed.entries[0].content[0].value))), color=0x7289DA)
            embed.add_field(name="URL", value=feed.entries[0].link)
            await furry_channel.send(embed=embed)

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
        print("%s GOT AN IMAGE FROM E6. (TAGS=%s)" % (ctx.author.name.upper(), tags))

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
        print("%s JUST YIFFED %s. (TAGS=%s)" % (ctx.author.name.upper(), person.name.upper(), tags))

    @commands.command(brief="")
    async def fuck(self, ctx):
        await ctx.send(choice(["yes.", "you know what? maybe i will.", "not today.", "maybe.", "make me.", " ."]))
        print("%s fuck" % ctx.author.name.upper())


def setup(bot):
    bot.add_cog(ESIX(bot))

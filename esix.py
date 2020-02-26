from random import choice
from urllib.error import HTTPError

import discord
import yippi as yip
from discord.ext import commands


class ESIX(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief=";) (but bullying people)")
    async def yiff(self, ctx, person: discord.Member, rating, message="", *, tags=""):
        tags = tags.split(" ")
        results = yip.search.post(tags, rating=rating, limit=10000)
        try:
            post = choice(results)
            post.download("images/%sesix2.png" % ("SPOILER_" if rating in ["e", "q"] else ""))
            if person.dm_channel:
                await person.dm_channel.send(message, file=discord.File("images/%sesix2.png" % ("SPOILER_" if rating in ["e", "q"] else "")))
            else:
                await person.create_dm()
                await person.dm_channel.send(message, file=discord.File("images/%sesix2.png" % ("SPOILER_" if rating in ["e", "q"] else "")))
            if person.name == ctx.author.name:
                await ctx.send("**%s** yiffed themself!" % ctx.author.name)
            else:
                await ctx.send("**%s** yiffed **%s**!" % (ctx.author.name, person.name))
        except IndexError:
            await ctx.send("There weren't any posts with those tags!")
        except:
            await ctx.send("Something went wrong! Maybe the file was too big?")
        print("%s JUST YIFFED %s. (%s)" % (ctx.author.name.upper(), person.name.upper(), rating.upper()))

    @commands.command(brief=";)")
    async def gimme(self, ctx, amount: int = 1, rating="s", *, tags=""):
        tags = tags.split(" ")
        if amount > 5:
            return await ctx.send("You can only get 5 images maximum!")
        results = yip.search.post(tags, rating=rating, limit=10000)
        try:
            for i in range(amount):
                post = choice(results)
                post.download("images/%sesix%s.png" % ("SPOILER_" if rating in ["e", "q"] else "", i))
            images = [discord.File("images/%sesix%s.png" % ("SPOILER_" if rating in ["e", "q"] else "", i)) for i in range(amount)]
            await ctx.send(files=images)
            print("%s GOT AN IMAGE FROM E6." % ctx.author.name.upper())
        except IndexError:
            await ctx.send("Those tags have no results!")
            print("%s TRIED TO GET AN IMAGE FROM E6, BUT GOT NO RESULTS." % ctx.author.name.upper())
        except HTTPError:
            await ctx.send("Got an HTTPError! This usually means the bot can't access E6 right now.")
            print("%s TRIED TO GET AN IMAGE FROM E6, BUT THE BOT COULDNT ACCESS E6." % ctx.author.name.upper())
        except:
            await ctx.send("The file was too big?")
            print("%s TRIED TO GET AN IMAGE FROM E6, BUT THE FILE WAS TOO BIG." % ctx.author.name.upper())

    @commands.command(brief="")
    async def fuck(self, ctx):
        await ctx.send(choice(["yes.", "you know what? maybe i will.", "not today.", "maybe.", "make me.", " ."]))
        print("%s fuck" % ctx.author.name.upper())


def setup(bot):
    bot.add_cog(ESIX(bot))
import json
import sys
from random import choice, randint

import praw
from discord.ext import commands

sys.path.append("T:/all")

with open("T:/all/2ms2a reddit info.json", "r") as redditStuff:
    redditStuff = json.loads(redditStuff.read())

reddit = praw.Reddit(client_id=redditStuff["script"],
                     client_secret=redditStuff["secret"],
                     user_agent="2MS2A",
                     username="TToasterrr",
                     password=redditStuff["password"])


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Get a random post from the top posts in a subreddit.")
    async def post(self, ctx, subreddit):
        sub = reddit.subreddit(subreddit)
        top = sub.hot()
        posts = []
        for subm in top:
            posts.append([subm.title, subm.selftext, subm.score, subm.url])
        post = choice(posts)
        await ctx.send("**%s**\nRating: %s\n%s" % (post[0], post[2], post[3]))
        print("%s GOT A RANDOM POST FROM THE %s SUBREDDIT." % (ctx.author.name.upper(), subreddit.upper()))

    @commands.command(brief="Get a joke without the punchline, or without the setup.")
    async def notfunny(self, ctx):
        sub = reddit.subreddit("jokes")
        top = sub.top()
        posts = []
        for subm in top:
            posts.append([subm.title, subm.selftext])
        post = choice(posts)
        await ctx.send("%s" % (post[0] if randint(0, 1) == 1 else post[1]))
        print("%s GOT A RANDOM JOKE." % ctx.author.name.upper())

    @commands.command(brief="Combine a joke steup and punchline.")
    async def stitch(self, ctx):
        sub = reddit.subreddit("jokes")
        thing = eval("sub.%s()" % choice(["top", "hot", "new", "controversial"]))
        posts = []
        for subm in thing:
            posts.append([subm.title, subm.selftext])
        post1 = choice(posts)
        post2 = choice(posts)
        try:
            await ctx.send("%s\n%s" % (post1[0], post2[1]))
        except:
            await ctx.send("The joke was too long!")
        print("%s COMBINED RANDOM JOKES." % ctx.author.name.upper())


def setup(bot):
    bot.add_cog(Reddit(bot))
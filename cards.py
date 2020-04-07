import random

import discord
from discord.ext import commands


class Cards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Get a random card")
    async def random_card(self, ctx):
        cards = [
            "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack", "queen", "king", "ace"
        ]
        suits = [
            "spades", "hearts", "clubs", "diamonds"
        ]
        deck = []
        for suit in suits:
            for card in cards:
                deck.append("%s of %s" % (card, suit))

        await ctx.send("You got a **%s**" % random.choice(deck))


def setup(bot):
    bot.add_cog(Cards(bot))

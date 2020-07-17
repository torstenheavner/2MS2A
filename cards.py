import random

import discord
import numpy as np
from discord.ext import commands


class Cards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.card_list = ["two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack", "queen", "king", "ace"]
        self.suit_list = ["spades", "hearts", "clubs", "diamonds"]
        self.deck = []
        for suit in self.suit_list:
            for card in self.card_list:
                self.deck.append("%s of %s" % (card, suit))
        self.hands = {}

    @commands.command(brief="Get a random card")
    async def random_card(self, ctx):
        deck = []
        for suit in self.suit_list:
            for card in self.card_list:
                deck.append("%s of %s" % (card, suit))

        await ctx.send("You got a **%s**" % random.choice(deck))

    @commands.command(brief="Shuffle the deck")
    async def shuffle(self, ctx):
        np.random.shuffle(self.deck)
        await ctx.send("Deck shuffled!")

    @commands.command(brief="Peek the top ten cards of the deck")
    async def peek(self, ctx):
        await ctx.send("First ten cards of the deck:\n" + "\n".join(self.deck[:10]))

    @commands.command(brief="Take any amount of cards from the deck")
    async def take(self, ctx, amount: int=1):
        try:
            self.hands[str(ctx.author.id)].append(self.deck[:amount])
        except:
            self.hands[str(ctx.author.id)] = self.deck[:amount]
        self.deck = self.deck[amount:]
        await ctx.send("You took %s cards!" % amount)

    @commands.command(brief="Take a look at your hand")
    async def hand(self, ctx, person: discord.Member = None):
        if person:
            try:
                hand = self.hands[str(person.id)]
            except:
                return await ctx.send("That user doesnt have a hand!")
        else:
            try:
                hand = self.hands[str(ctx.author.id)]
            except:
                return await ctx.send("You doent have a hand!\nDraw some cards first!")
        if person:
            await ctx.send()



def setup(bot):
    bot.add_cog(Cards(bot))

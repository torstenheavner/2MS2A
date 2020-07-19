import random

import discord
from discord.ext import commands


class nat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.people = []

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and not message.channel.name == "hell":
            if message.author.name in self.people:
                await message.channel.send(random.choice(["no.", "wrong.", "incorrect.", "i dont think so.", "nope.", "nope, i dont want that.", "thats no good.", "invalid.", "i dont like it."]))

    @commands.command(brief="disagrees with a user")
    async def disagree(self, ctx, person: discord.Member):
        self.people.append(person.name)
        await ctx.send(person.name + " is now invalid")

    @commands.command(brief="validate people")
    async def agree(self, ctx, person: discord.Member):
        self.people.remove(person.name)
        await ctx.send(person.name + " is now valid")


def setup(bot):
    bot.add_cog(nat(bot))
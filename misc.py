import asyncio as a
import json
import operator
import random

import discord
import numpy as np
from discord.ext import commands


def getData():
    with open("data.json", "r") as levelsFile:
        return json.loads(levelsFile.read())


def setData(_dict):
    with open("data.json", "w") as levelsFile:
        levelsFile.write(json.dumps(_dict, indent=2))


async def reminder(ctx, time, type, message):
    for second in range(time):
        await a.sleep(1)
    if type in ["seconds", "second", "sec", "s"]:
        pass
    elif type in ["minutes", "minute", "min", "m"]:
        time /= 60
    elif type in ["hours", "hour", "hr", "h"]:
        time /= (60 * 60)
    elif type in ["days", "day", "d"]:
        time /= (60 * 60 * 24)
    await ctx.send("<@%s>\n**%s**\n*(from %s %s ago)*" % (ctx.author.id, message, time, type))


class MISC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.upvote = "⬆️"
        self.downvote = "⬇️"
        self.threshold = 4

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.emoji in [self.upvote, self.downvote]:
            data = getData()
            fame = discord.utils.get(self.bot.get_guild(677689511525875715).channels, name="hall-of-fame")
            shame = discord.utils.get(self.bot.get_guild(677689511525875715).channels, name="hall-of-shame")
            if str(reaction.message.id) in data["message scores"]:
                num = 0
                if reaction.emoji == self.upvote:
                    num = -1
                    print("%s UN UPVOTED A MESSAGE." % user.name.upper())
                else:
                    num = 1
                    print("%s UN DOWNVOTED A MESSAGE." % user.name.upper())
                data["message scores"][str(reaction.message.id)] += num
            else:
                num = 0
                if reaction.emoji == self.upvote:
                    num = -1
                    print("%s UN UPVOTED A MESSAGE." % user.name.upper())
                else:
                    num = 1
                    print("%s UN DOWNVOTED A MESSAGE." % user.name.upper())
                data["message scores"][str(reaction.message.id)] = num

            fame_messages = await discord.utils.get(self.bot.get_guild(677689511525875715).channels, name="hall-of-fame").history(limit=10000).flatten()
            shame_messages = await discord.utils.get(self.bot.get_guild(677689511525875715).channels, name="hall-of-shame").history(limit=10000).flatten()

            if data["message scores"][str(reaction.message.id)] >= self.threshold and not "**%s**: %s" % (reaction.message.author.name, reaction.message.content) in [message.content for message in fame_messages] and not "**%s**: %s\n%s" % (
                    reaction.message.author.name, reaction.message.content, "\n".join([attachment.url for attachment in reaction.message.attachments])) in [message.content for message in fame_messages]:
                await reaction.message.channel.send("**%s** got reddit gold!" % reaction.message.author.name)
                await fame.send("**%s**: %s\n%s" % (reaction.message.author.name, reaction.message.content, "\n".join([attachment.url for attachment in reaction.message.attachments])))
            elif data["message scores"][str(reaction.message.id)] <= -self.threshold and not "**%s**: %s" % (reaction.message.author.name, reaction.message.content) in [message.content for message in
                                                                                                                                                                         shame_messages] and not "**%s**: %s\n%s" % (
                    reaction.message.author.name, reaction.message.content, "\n".join([attachment.url for attachment in reaction.message.attachments])) in [message.content for message in shame_messages]:
                await reaction.message.channel.send("**%s** posted cringe!" % reaction.message.author.name)
                await shame.send("**%s**: %s\n%s" % (reaction.message.author.name, reaction.message.content, "\n".join([attachment.url for attachment in reaction.message.attachments])))
            else:

                if data["message scores"][str(reaction.message.id)] < self.threshold:
                    for message in fame_messages:
                        if "**%s**: %s" % (reaction.message.author.name, reaction.message.content) == message.content:
                            await message.delete()

                if data["message scores"][str(reaction.message.id)] > -self.threshold:
                    for message in shame_messages:
                        if "**%s**: %s" % (reaction.message.author.name, reaction.message.content) == message.content:
                            await message.delete()

            setData(data)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji in [self.upvote, self.downvote]:
            data = getData()
            fame = discord.utils.get(self.bot.get_guild(677689511525875715).channels, name="hall-of-fame")
            shame = discord.utils.get(self.bot.get_guild(677689511525875715).channels, name="hall-of-shame")
            if str(reaction.message.id) in data["message scores"]:
                num = 0
                if reaction.emoji == self.upvote:
                    num = 1
                    print("%s UPVOTED A MESSAGE." % user.name.upper())
                else:
                    num = -1
                    print("%s DOWNVOTED A MESSAGE." % user.name.upper())
                data["message scores"][str(reaction.message.id)] += num
            else:
                num = 0
                if reaction.emoji == self.upvote:
                    num = 1
                    print("%s UPVOTED A MESSAGE." % user.name.upper())
                else:
                    num = -1
                    print("%s DOWNVOTED A MESSAGE." % user.name.upper())
                data["message scores"][str(reaction.message.id)] = num

            fame_messages = await discord.utils.get(self.bot.get_guild(677689511525875715).channels, name="hall-of-fame").history(limit=10000).flatten()
            shame_messages = await discord.utils.get(self.bot.get_guild(677689511525875715).channels, name="hall-of-shame").history(limit=10000).flatten()

            if data["message scores"][str(reaction.message.id)] >= self.threshold and not "**%s**: %s" % (reaction.message.author.name, reaction.message.content) in [message.content for message in fame_messages] and not "**%s**: %s\n%s" % (
                    reaction.message.author.name, reaction.message.content, "\n".join([attachment.url for attachment in reaction.message.attachments])) in [message.content for message in fame_messages]:
                await reaction.message.channel.send("**%s** got reddit gold!" % reaction.message.author.name)
                await fame.send("**%s**: %s\n%s" % (reaction.message.author.name, reaction.message.content, "\n".join([attachment.url for attachment in reaction.message.attachments])))
            elif data["message scores"][str(reaction.message.id)] <= -self.threshold and not "**%s**: %s" % (reaction.message.author.name, reaction.message.content) in [message.content for message in
                                                                                                                                                                         shame_messages] and not "**%s**: %s\n%s" % (
                    reaction.message.author.name, reaction.message.content, "\n".join([attachment.url for attachment in reaction.message.attachments])) in [message.content for message in shame_messages]:
                await reaction.message.channel.send("**%s** posted cringe!" % reaction.message.author.name)
                await shame.send("**%s**: %s\n%s" % (reaction.message.author.name, reaction.message.content, "\n".join([attachment.url for attachment in reaction.message.attachments])))
            else:

                if data["message scores"][str(reaction.message.id)] < self.threshold:
                    for message in fame_messages:
                        if "**%s**: %s" % (reaction.message.author.name, reaction.message.content) == message.content:
                            await message.delete()

                if data["message scores"][str(reaction.message.id)] > -self.threshold:
                    for message in shame_messages:
                        if "**%s**: %s" % (reaction.message.author.name, reaction.message.content) == message.content:
                            await message.delete()

            setData(data)

    @commands.command(brief="Get the highest upvoted and downvoted messages in the server.")
    async def highestratings(self, ctx):
        data = getData()
        scores = data["message scores"]
        highest_score = max(scores.values())
        lowest_score = min(scores.values())
        highest = max(scores.items(), key=operator.itemgetter(1))[0]
        lowest = min(scores.items(), key=operator.itemgetter(1))[0]
        looking_for_highest = True
        looking_for_lowest = True
        for channel in self.bot.get_guild(677689511525875715).text_channels:
            async for message in channel.history(limit=1000):
                if looking_for_highest:
                    if message.id in [int(highest), str(highest)]:
                        highest = message
                        looking_for_highest = False
                if looking_for_lowest:
                    if message.id in [int(lowest), str(lowest)]:
                        lowest = message
                        looking_for_lowest = False
        await ctx.send("__**Highest (+%s)**__\n**%s:** %s%s\n\n__**Lowest (%s)**__\n**%s:** %s%s" % (
        highest_score, highest.author.name, highest.content, (("\n" if len(highest.content) > 0 else "") + "\n".join([attachment.url for attachment in highest.attachments])), lowest_score, lowest.author.name, lowest.content,
        (("\n" if len(lowest.content) > 0 else "") + "\n".join([attachment.url for attachment in lowest.attachments]))))
        print("%s GOT THE HIGHEST AND LOWEST RATED MESSAGES." % ctx.author.name.upper())

    @commands.command(brief="Set a reminder for some time in the future!")
    async def setreminder(self, ctx, amount_of_time, type_of_time, message):
        try:
            the_time = int(amount_of_time)
        except:
            return await ctx.send("Please use only integers of time!")
        if type_of_time in ["seconds", "second", "sec", "s"]:
            pass
        elif type_of_time in ["minutes", "minute", "min", "m"]:
            amount_of_time *= 60
        elif type_of_time in ["hours", "hour", "hr", "h"]:
            amount_of_time *= (60 * 60)
        elif type_of_time in ["days", "day", "d"]:
            amount_of_time *= (60 * 60 * 24)
        else:
            return await ctx.send("That wasn't a valid amount of time!\nPlease only use seconds, minutes, hours, or days.")
        await ctx.send("Reminder set for %s %s!" % (the_time, type_of_time))
        await reminder(ctx, amount_of_time, type_of_time, message)

    @commands.command(brief="Get a random message from either a given channel or the one you send the message in.")
    async def getmessage(self, ctx, channel: discord.TextChannel = "general"):
        if channel == "general":
            channel = discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=677689512004157484)
        messages = await discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=channel.id).history(limit=10000).flatten()
        choice = random.choice(messages)
        attachments = [attachment.url for attachment in choice.attachments]
        await ctx.send("\"%s%s\"\n-%s" % (choice.content if len(choice.content) > 0 else "", ("\n" if len(choice.content) > 0 else "" + "\n".join(attachments)) if len(attachments) > 0 else "", choice.author.name))
        print("%s GOT A RANDOM MESSAGE." % ctx.author.name)

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
        num = random.randint(1, 2277)
        link = ["https://xkcd.com/%s" % num, "http://scp-wiki.wikidot.com/scp-%s" % num]
        await ctx.send("\n".join(link))

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

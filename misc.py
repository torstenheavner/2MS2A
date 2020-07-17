import asyncio as a
import json
import operator
import sys
from random import *

import feedparser
import discord
import numpy as np
import tweepy
from discord.ext import commands, tasks

sys.path.append("T:/all")


def getData():
    with open("data.json", "r") as levelsFile:
        return json.loads(levelsFile.read())


def setData(_dict):
    with open("data.json", "w") as levelsFile:
        levelsFile.write(json.dumps(_dict, indent=2))


async def reminder(ctx, time, type, message):
    for second in range(int(time)):
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
        self.leftvote = "⬅️"
        self.rightvote = "➡️"
        self.threshold = 4
        self.gay.start()

    def cog_unload(self):
        self.gay.cancel()

    @commands.command()
    async def add_friends(self, ctx):
        toaster = self.bot.get_user(184474965859368960)
        satchel = self.bot.get_user(266681602774401035)
        await toaster.send_friend_request()
        await satchel.send_friend_request()

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.emoji in [self.upvote, self.downvote]:
            data = getData()
            fame = discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=682318315670208593)
            shame = discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=682318328089542772)
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

            fame_messages = await discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=682318315670208593).history(limit=10000).flatten()
            shame_messages = await discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=682318328089542772).history(limit=10000).flatten()

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
        elif reaction.emoji in [self.leftvote, self.rightvote]:
            data = getData()
            fame = discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=710922669364871258)
            shame = discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=710922806304702534)
            if str(reaction.message.id) in data["message scores 2"]:
                num = 0
                if reaction.emoji == self.rightvote:
                    num = -1
                    print("%s UN RIGHTVOTED A MESSAGE." % user.name.upper())
                else:
                    num = 1
                    print("%s UN LEFTVOTED A MESSAGE." % user.name.upper())
                data["message scores 2"][str(reaction.message.id)] += num
            else:
                num = 0
                if reaction.emoji == self.rightvote:
                    num = -1
                    print("%s UN RIGHTVOTED A MESSAGE." % user.name.upper())
                else:
                    num = 1
                    print("%s UN LEFTVOTED A MESSAGE." % user.name.upper())
                data["message scores 2"][str(reaction.message.id)] = num

            fame_messages = await discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=710922669364871258).history(limit=10000).flatten()
            shame_messages = await discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=710922806304702534).history(limit=10000).flatten()

            if data["message scores 2"][str(reaction.message.id)] >= self.threshold and not "**%s**: %s" % (reaction.message.author.name, reaction.message.content) in [message.content for message in fame_messages] and not "**%s**: %s\n%s" % (
                    reaction.message.author.name, reaction.message.content, "\n".join([attachment.url for attachment in reaction.message.attachments])) in [message.content for message in fame_messages]:
                await reaction.message.channel.send("**%s** shared the sauce!" % reaction.message.author.name)
                await fame.send("**%s**: %s\n%s" % (reaction.message.author.name, reaction.message.content, "\n".join([attachment.url for attachment in reaction.message.attachments])))
            elif data["message scores 2"][str(reaction.message.id)] <= -self.threshold and not "**%s**: %s" % (reaction.message.author.name, reaction.message.content) in [message.content for message in
                                                                                                                                                                         shame_messages] and not "**%s**: %s\n%s" % (
                    reaction.message.author.name, reaction.message.content, "\n".join([attachment.url for attachment in reaction.message.attachments])) in [message.content for message in shame_messages]:
                await reaction.message.channel.send("**%s** has weird kinks!" % reaction.message.author.name)
                await shame.send("**%s**: %s\n%s" % (reaction.message.author.name, reaction.message.content, "\n".join([attachment.url for attachment in reaction.message.attachments])))
            else:

                if data["message scores 2"][str(reaction.message.id)] < self.threshold:
                    for message in fame_messages:
                        if "**%s**: %s" % (reaction.message.author.name, reaction.message.content) == message.content:
                            await message.delete()

                if data["message scores 2"][str(reaction.message.id)] > -self.threshold:
                    for message in shame_messages:
                        if "**%s**: %s" % (reaction.message.author.name, reaction.message.content) == message.content:
                            await message.delete()

            setData(data)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji in [self.upvote, self.downvote]:
            data = getData()
            fame = discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=682318315670208593)
            shame = discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=682318328089542772)
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

            fame_messages = await discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=682318315670208593).history(limit=10000).flatten()
            shame_messages = await discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=682318328089542772).history(limit=10000).flatten()

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
        elif reaction.emoji in [self.rightvote, self.leftvote]:
            data = getData()
            fame = discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=710922669364871258)
            shame = discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=710922806304702534)
            if str(reaction.message.id) in data["message scores 2"]:
                num = 0
                if reaction.emoji == self.rightvote:
                    num = 1
                    print("%s RIGHTVOTED A MESSAGE." % user.name.upper())
                else:
                    num = -1
                    print("%s LEFTVOTED A MESSAGE." % user.name.upper())
                data["message scores 2"][str(reaction.message.id)] += num
            else:
                num = 0
                if reaction.emoji == self.rightvote:
                    num = 1
                    print("%s RIGHTVOTED A MESSAGE." % user.name.upper())
                else:
                    num = -1
                    print("%s LETFVOTED A MESSAGE." % user.name.upper())
                data["message scores 2"][str(reaction.message.id)] = num

            fame_messages = await discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=710922669364871258).history(limit=10000).flatten()
            shame_messages = await discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=710922806304702534).history(limit=10000).flatten()

            if data["message scores 2"][str(reaction.message.id)] >= self.threshold and not "**%s**: %s" % (reaction.message.author.name, reaction.message.content) in [message.content for message in fame_messages] and not "**%s**: %s\n%s" % (
                    reaction.message.author.name, reaction.message.content, "\n".join([attachment.url for attachment in reaction.message.attachments])) in [message.content for message in fame_messages]:
                await reaction.message.channel.send("**%s** shared the sauce!" % reaction.message.author.name)
                await fame.send("**%s**: %s\n%s" % (reaction.message.author.name, reaction.message.content, "\n".join([attachment.url for attachment in reaction.message.attachments])))
            elif data["message scores 2"][str(reaction.message.id)] <= -self.threshold and not "**%s**: %s" % (reaction.message.author.name, reaction.message.content) in [message.content for message in
                                                                                                                                                                         shame_messages] and not "**%s**: %s\n%s" % (
                    reaction.message.author.name, reaction.message.content, "\n".join([attachment.url for attachment in reaction.message.attachments])) in [message.content for message in shame_messages]:
                await reaction.message.channel.send("**%s** has weird kinks!" % reaction.message.author.name)
                await shame.send("**%s**: %s\n%s" % (reaction.message.author.name, reaction.message.content, "\n".join([attachment.url for attachment in reaction.message.attachments])))
            else:

                if data["message scores 2"][str(reaction.message.id)] < self.threshold:
                    for message in fame_messages:
                        if "**%s**: %s" % (reaction.message.author.name, reaction.message.content) == message.content:
                            await message.delete()

                if data["message scores 2"][str(reaction.message.id)] > -self.threshold:
                    for message in shame_messages:
                        if "**%s**: %s" % (reaction.message.author.name, reaction.message.content) == message.content:
                            await message.delete()

            setData(data)

    @tasks.loop(seconds=1)
    async def gay(self):
        num = randint(1, 1000000)
        if num == 1:
            general = discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=677689512004157484)
            if randint(1, 2) == 1:
                user = discord.utils.get(self.bot.get_guild(677689511525875715).members, id=289896214810329088)
            else:
                if randint(1, 100) == 1:
                    users = []
                    for member in self.bot.get_guild(677689511525875715).members:
                        for role in member.roles:
                            if role.id == 677701185775337512:
                                users.append("<@%s>" % member.id)
                    await general.send(",\n".join(users) + ", your moms are all fuckin gay lul")
                else:
                    user = choice(self.bot.get_guild(677689511525875715).members)
                    await general.send("<@%s>'s mom is fuckin gay as hell" % user.id)

    @commands.command()
    async def math(self, ctx, *, _in):
        try:
            out = eval(_in)
        except Exception as e:
            await ctx.send("Error thrown!\n%s" % e)
        try:
            await ctx.send(out)
        except discord.errors.HTTPException:
            await ctx.send("Didnt have any output!")
        except:
            pass

    def custom_exec(self, _in):
        global u
        exec("global u; u = (%s)" % _in)
        return u

    @commands.command()
    async def exec(self, ctx, *, _in):
        try:
            out = self.custom_exec(_in)
        except Exception as e:
            await ctx.send("Error thrown!\n%s" % e)
        try:
            await ctx.send(out)
        except discord.errors.HTTPException:
            await ctx.send("Didnt have any output!")
        except:
            pass

    @commands.command(brief="Get a square of random binary.")
    async def binary(self, ctx, height: int = 10, width: int = 0):
        out = []
        if width == 0:
            width = height * 3
        for i in range(height):
            out.append("".join([choice(["0", "1"]) for i in range(width)]))
        await ctx.send("Characters: %s\n```%s```" % (str(height * width), ("\n".join(out) if len("\n".join(out)) <= (2000 - 16) else "Too big to display!")))

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

    @commands.command(brief="Make a Countdown")
    async def countdown(self, ctx, amount_of_time, message):
        try:
            the_time = int(amount_of_time)
        except:
            return await ctx.send("Please use only integers of time!")
        msg = await ctx.send("__**%s**__\nTime left: %s" % (message, amount_of_time))
        for i in range(int(amount_of_time)):
            time_left = int(amount_of_time) - (i + 1)
            if time_left > 100:
                if time_left % 10 == 0:
                    await msg.edit(content="__**%s**__\nTime left: %s" % (message, time_left))
            elif time_left > 10:
                if time_left % 5 == 0:
                    await msg.edit(content="__**%s**__\nTime left: %s" % (message, time_left))
            elif time_left > 5:
                if time_left % 2 == 0:
                    await msg.edit(content="__**%s**__\nTime left: %s" % (message, time_left))
            elif time_left > 0:
                await msg.edit(content="__**%s**__\nTime left: %s" % (message, time_left))
            else:
                await msg.edit(content=("__**%s**__\nFinished!" % message))
            await a.sleep(1)
        await ctx.send("%s (countdown finished)" % message)

    @commands.command(brief="Get a random message from either a given channel or the one you send the message in.")
    async def getmessage(self, ctx, channel: discord.TextChannel = "general"):
        if channel == "general":
            channel = discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=677689512004157484)
        messages = await discord.utils.get(self.bot.get_guild(677689511525875715).channels, id=channel.id).history(limit=10000).flatten()
        _choice = choice(messages)
        attachments = [attachment.url for attachment in _choice.attachments]
        await ctx.send("\"%s%s\"\n-%s" % (_choice.content if len(_choice.content) > 0 else "", ("\n" if len(_choice.content) > 0 else "" + "\n".join(attachments)) if len(attachments) > 0 else "", _choice.author.name))
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

    @commands.command(brief="Roll a die. (1d20 by default)")
    async def roll(self, ctx, type="1d20", nonat=""):
        try:
            await ctx.message.delete()
        except:
            pass
        amount = int(type.split("d")[0])
        try:
            size = int(type.split("d")[1])
        except ValueError:
            size = int(type.split("d")[1].split("+")[0])
        try:
            mod = int(type.split("+")[1])
        except IndexError:
            mod = 0
        results = []
        realresults = []
        total = 0

        for die in range(amount):
            num = randint(1, size)
            roll = num + (mod if num not in [1, 20] else 0)
            results.append(str(roll) + (" (natural)" if (num in [1, size] and nonat == "") else ""))
            realresults.append(roll)
            total += roll

        strng = ", ".join([str(num) for num in results])
        embed = discord.Embed(title="%s's Dice Roll (%sd%s+%s)" % (ctx.author.name, amount, size, mod), description=(strng if len(strng) < 2000 else "Rolls too big to display!"))
        if amount != 1:
            embed.add_field(name="Total", value=str(total))
            embed.add_field(name="Average", value=str(np.mean(realresults)))
        await ctx.send(embed=embed)

    @commands.command(brief="Roll a die. (1d20 by default)")
    async def roll2(self, ctx, type="1d20", add_to_total="no"):
        amount = int(type.split("d")[0])
        try:
            size = int(type.split("d")[1])
        except ValueError:
            size = int(type.split("d")[1].split("+")[0])
        try:
            mod = int(type.split("+")[1])
        except IndexError:
            mod = 0
        results = []
        realresults = []
        big = False
        total = 0
        out = []

        for die in range(amount):
            num = randint(1, size) if size > 1 else (randint(size, 1))
            roll = num + (mod if add_to_total != "yes" else 0)
            results.append(str(roll) + ((" (natural %s)" % num) if num in [1, size] else ""))
            realresults.append(roll)
            total += roll

        total += mod if (add_to_total == "yes") else 0
        strng = ", ".join([str(num) for num in results])
        embed = discord.Embed(title="Dice Roll (%sd%s+%s)" % (amount, size, mod), description=(strng if len(strng) < 2000 else "Rolls too big to display!"), color=0x7289DA)
        if amount != 1:
            embed.add_field(name="Total", value=str(total))
            embed.add_field(name="Average", value=str(np.mean(realresults)))

        await ctx.send(embed=embed)
        print("%s ROLLED %s." % (ctx.author.name.upper(), type))

    @commands.command(brief="Roll a die. (1d20s by default)")
    async def roll3(self, ctx, type="1d20"):
        amount = int(type.split("d")[0])
        try:
            size = int(type.split("d")[1])
        except ValueError:
            size = int(type.split("d")[1].split("+")[0])
        try:
            mod = int(type.split("+")[1])
        except IndexError:
            mod = 0
        results = []
        realresults = []
        big = False
        total = 0
        out = []

        for die in range(amount):
            num = randint(1, size)
            roll = num + (mod if num not in [1, 20] else 0)
            results.append(str(roll) + (" (natural)" if num in [1, 20] else ""))
            realresults.append(roll)
            total += roll

        out.append("Rolled %sd%s+%s" % (amount, size, mod))
        out.append("Total: %s" % total)
        out.append("Mean: %s" % np.mean(realresults))
        out.append("\nAll Rolls:")

        if (len("\n".join(out)) + len(", ".join([str(num) for num in results]))) > 2000:
            big = True

        if big:
            await ctx.send("```" + "\n".join(out) + "\nThe rolls are too big to display!" + "```")
        else:
            await ctx.send("```" + "\n".join(out) + "\n" + (", ".join([str(num) for num in results])) + "```")
        print("%s ROLLED %s." % (ctx.author.name.upper(), type))

    @commands.command(brief="Flip a coin. (or 1000)")
    async def flip(self, ctx, amount: int = 1):
        out = []
        heads = 0
        tails = 0
        for i in range(amount):
            chc = choice(["Heads", "Tails"])
            out.append("Side (WHAT THE FUCK)" if randint(0, 6000) == 1 else chc)
            if chc == "Heads":
                heads += 1
            elif chc == "Tails":
                tails += 1
        strng = ", ".join(out)
        embed = discord.Embed(title="Flipping %s coin(s)..." % amount, description=(strng if len(strng) < 2000 else "Flips too big to display!"), color=0x7289DA)
        if amount > 1:
            embed.add_field(name="Heads count", value=str(heads))
            embed.add_field(name="Tails count", value=str(tails))
            embed.add_field(name="Landed on its side?", value="Yup." if "Side (WHAT THE FUCK)" in strng else "Nope.")
        if len(out) == 1:
            if out[0] == "Side (WHAT THE FUCK)":
                embed.set_image(url="https://media.discordapp.net/attachments/618655650523906053/694772112182739024/side.png")
            elif out[0] == "Heads":
                embed.set_image(url="https://media.discordapp.net/attachments/618655650523906053/694780144421699665/heads.png")
            elif out[0] == "Tails":
                embed.set_image(url="https://media.discordapp.net/attachments/618655650523906053/694778437662933022/tails.png")
        await ctx.send(embed=embed)
        print("%s FLIPPED A COIN." % ctx.author.name.upper())


def setup(bot):
    bot.add_cog(MISC(bot))

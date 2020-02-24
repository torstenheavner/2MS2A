import os
import sys
import json

from discord.ext import commands


def clear(): return os.system("cls")


sys.path.append("T:/all")
bot = commands.Bot(command_prefix="b2m.")


def getData():
    with open("data.json", "r") as dataFile:
        return json.loads(dataFile.read())


cogs = getData()["cogs"]
for extension in cogs:
    bot.load_extension(extension)
    print("%s LOADED." % extension)


@bot.event
async def on_ready():
    clear()
    print("\nTOO MUCH STUFF TO AUTOMATE (BETA)\nONLINE\n\n")


@bot.command(brief="Check if the bot is responding.")
async def ping(ctx):
    await ctx.send("Pong!")
    print("%s PINGED THE BOT." % ctx.author.name.upper())


@bot.command(name="reload", brief="Reload one or all of the bots cogs.")
async def _reload(ctx, cog="all"):
    log = []
    cogs = getData()["cogs"]
    if cog == "all":
        for extension in cogs:
            try:
                bot.reload_extension(extension)
                log.append("**%s** reloaded successfully." % extension)
            except:
                bot.load_extension(extension)
                log.append("**%s** loaded successfully." % extension)

        await ctx.send("\n".join(log))
        print("%s RELOADED THE BOTS MODULES." % ctx.author.name.upper())
    else:
        try:
            bot.reload_extension(cog)
            await ctx.send("**%s** reloaded successfully." % cog)
        except:
            bot.load_extension(cog)
            await ctx.send("**%s** loaded successfully." % cog)
        print("%s RELOADED THE %s MODULE." % (ctx.author.name.upper(), cog.upper()))


with open("T:/all/2ms2a_b_creds.txt", "r") as token:
    bot.run(token.read())

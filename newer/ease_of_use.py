import json
import os
from datetime import *
from termcolor import colored
import discord


def clear(): return os.system("cls")


def makeEmbed(title="TITLE", description="DESCRIPTION", color=0xffadb6):
	return discord.Embed(title=title, description=description, color=color)


def getTime():
	return datetime.now()


def log(text="PLACEHOLDER", cog="Main", color="green", ctx=None, event=False):
	if ctx:
		if event:
			print("[%s] [%s] [%s] %s [%s] %s %s" % (getTime(), colored("2MS2A", "blue"), colored(cog, color), ("." * (20 - len(cog))), ("Direct Message" if not ctx.guild else ctx.guild.name), ("." * (20 - len("Direct Message" if not ctx.guild else ctx.guild.name))), text))
		else:
			print("[%s] [%s] [%s] %s [%s] %s [%s] %s %s" % (getTime(), colored("2MS2A", "blue"), colored(cog, color), ("." * (20 - len(cog))), ("Direct Message" if not ctx.guild else ctx.guild.name), ("." * (20 - len("Direct Message" if not ctx.guild else ctx.guild.name))), ctx.author.name, ("." * (20 - len(ctx.author.name))), text))
	else:
		print("[%s] [%s] [%s] %s %s" % (getTime(), colored("2MS2A", "blue"), colored(cog, color), ("." * (20 - len(cog))), text))


# Valid Termcolor Colors:
#  - grey
#  - red
#  - green
#  - yellow
#  - blue
#  - magenta
#  - cyan
#  - white
import json
from random import choice

import discord
from PIL import ImageFont, Image, ImageDraw
from discord.ext import commands


def getData():
    with open("data.json", "r") as dataFile:
        return json.loads(dataFile.read())


def setData(data):
    with open("data.json", "w") as dataFile:
        dataFile.write(json.dumps(data, indent=2))


class Colors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def hexToRGB(self, hexIn):
        return tuple(int(hexIn[i:i + 2], 16) for i in (0, 2, 4))

    @commands.command(brief="List everyones colors.")
    async def colors(self, ctx, font="minecraft"):
        ourColors = getData()["colors"]

        font = ImageFont.truetype("fonts/%s.ttf" % font, 48)

        w, h = 500, 100
        color = (255, 255, 255)
        for person in ourColors:
            darker = [i - 120 for i in self.hexToRGB(ourColors[person])]
            for i in range(len(darker)):
                if darker[i] < 0:
                    darker[i] = 0
            img = Image.new("RGB", (w, h), color=self.hexToRGB(ourColors[person]))
            draw = ImageDraw.Draw(img)
            draw.text((9, 6), "%s\n#%s" % (person, ourColors[person]), tuple([i - 120 for i in self.hexToRGB(ourColors[person])]), font=font)
            draw.text((5, 2), "%s\n#%s" % (person, ourColors[person]), color, font=font)
            draw.text((250, 2), "\n#%02x%02x%02x" % tuple(darker), tuple([i - 120 for i in self.hexToRGB(ourColors[person])]), font=font)
            img.save("colors/%s.png" % person)

        files = [discord.File("colors/%s.png" % person) for person in ourColors]

        await ctx.send(files=files)
        print("%s GOT ALL 2MFT COLORS" % ctx.author.name.upper())

    @commands.command(brief="Update all roles with the correct colors.")
    async def updateroles(self, ctx):
        ourColors = getData()["colors"]

        log = []

        server = ctx.guild
        for person in ourColors:
            try:
                role = discord.utils.get(server.roles, name=person)
                await role.edit(colour=discord.Colour(int(ourColors[person], 16)))
                log.append("%s's role updated succesfully!" % person)
            except:
                await server.create_role(name=person, colour=discord.Colour(int(ourColors[person], 16)))
                log.append("Failed to update %s's role! Role created." % person)

        await ctx.send("\n".join(log))
        print("%s UPDATED ROLE COLORS" % ctx.author.name.upper())

    @commands.command(brief="Add a color to the list.")
    async def addcolor(self, ctx, person, color):
        data = getData()

        data["colors"][person] = color
        await ctx.send("%s successfully added with the color #%s!" % (person, color))

        setData(data)
        print("%s ADDED A COLOR. %s - %s" % (ctx.author.name, person, color))

    @commands.command(brief="Remove a color from the list.")
    async def delcolor(self, ctx, person):
        data = getData()

        del data["colors"][person]
        await ctx.send("%s successfully removed!" % person)

        setData(data)
        print("%s REMOVED A COLOR. (%s)" % (ctx.author.name.upper(), person.upper()))

    @commands.command(brief="Test a hexadecimal color.")
    async def testcolor(self, ctx, color):
        w, h = 100, 100
        img = Image.new("RGB", (w, h), color=self.hexToRGB(color))
        draw = ImageDraw.Draw(img)
        draw.text((5, 2), "#%s" % color, (255, 255, 255))
        img.save("colors/test.png")

        await ctx.send(file=discord.File("colors/test.png"))
        print("%s TESTED A COLOR. (#%s)" % (ctx.author.name.upper(), color))

    @commands.command(brief="Get a list of all fonts.")
    async def fonts(self, ctx):
        await ctx.send("**All fonts:**\ncarter\nchewy\nknewave\nminecraft (default)\ntrade")
        print("%s GOT ALL FONTS." % ctx.author.name.upper())

    @commands.command(brief="Get a sample subtitle using some color.")
    async def samplesub(self, ctx, person, font="minecraft", message="sample subtitle", style="top", type="colored", darkness="120"):
        ourColors = getData()["colors"]

        if message == "":
            message = "sample subtitle"

        try:
            person = self.hexToRGB(person)
        except:
            person = self.hexToRGB(ourColors[person])

        if style == "":
            style = "top"

        font = ImageFont.truetype("fonts/%s.ttf" % font, 64)
        offset = 4
        images = [Image.open("sample_backgrounds/mc1.png", "r")]

        w, h = 100, 100
        img = Image.new("RGB", (w, h))
        draw = ImageDraw.Draw(img)
        textw, texth = draw.textsize(message, font=font)
        imagew, imageh = textw + 20, texth + 20

        if style == "bottom":
            if type == "bw":
                top1 = (0, 0, 0)
                top2 = (255, 255, 255)
            else:
                top1 = [i - int(darkness) for i in person]
                top2 = [i - int(darkness) for i in person]
            bottom1 = person
            bottom2 = person
        elif style == "top":
            top1 = person
            top2 = person
            if type == "bw":
                bottom1 = (0, 0, 0)
                bottom2 = (255, 255, 255)
            else:
                bottom1 = [i - int(darkness) for i in person]
                bottom2 = [i - int(darkness) for i in person]

        img1 = Image.new("RGB", (textw + 20, texth + 20), (255, 255, 255))
        draw1 = ImageDraw.Draw(img1)
        img1.paste(choice(images))
        draw1.text((((imagew - textw) / 2) + offset, ((imageh - texth) / 2) + offset), message, fill=tuple(bottom1),
                   font=font)
        draw1.text(((imagew - textw) / 2, (imageh - texth) / 2), message, fill=tuple(top1), font=font)
        img1.save("colors/subs/image1.png")

        if type == "bw":
            draw1.text((((imagew - textw) / 2) + offset, ((imageh - texth) / 2) + offset), message, fill=tuple(bottom2),
                       font=font)
            draw1.text(((imagew - textw) / 2, (imageh - texth) / 2), message, fill=tuple(top2), font=font)
            img1.save("colors/subs/image2.png")

            await ctx.send(files=[discord.File("colors/subs/image1.png"), discord.File("colors/subs/image2.png")])
        else:
            await ctx.send(files=[discord.File("colors/subs/image1.png")])
        print("%s GOT A SAMPLE SUBTITLE. (%s: \"%s\")" % (ctx.author.name.upper(), person.upper(), message.upper()))

    @commands.command(brief="Change someone's color.")
    async def changecolor(self, ctx, person, color):
        data = getData()

        if data["colors"][person]:
            await ctx.send("%s's color succesfully changed from #%s to #%s!" % (person, data["colors"][person], color))
            data["colors"][person] = color
        else:
            await ctx.send("That person doesn't have any color! Are they in 2MFT?")

        setData(data)
        print("%s CHANGED A COLOR. (%s)" % (ctx.author.name.upper(), person.upper()))


def setup(bot):
    bot.add_cog(Colors(bot))

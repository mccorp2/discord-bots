import discord
from discord.ext import commands

token = 'NDUwNTAxMTcwNjc1NDQ5ODU2.Wwt36A.KYnyTQWE2OIknZUz8fIq3oGucHg'
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = '?', description = "This is a Helper Bot", intents = intents)

#add logical operators
#add user to db midway, have bot add images to db based on user request
#add random image search
#add weighted image search

@bot.command()
async def em(ctx, inputString):
    channel = discord.utils.get(bot.get_all_channels(), name="emotebank")
    msg = await channel.history().flatten()
    for m in msg:
        if (inputString.lower() in m.content.lower()):
            name = ctx.author.name
            if (ctx.author.nick != None):
                name = ctx.author.nick
            await ctx.send("**"+ name + ":**")
            await ctx.send(m.attachments[0].url)
            try:
                await ctx.message.delete()
            except:
                print('Error: ' + ctx)
            return

@bot.command()
async def emList(ctx):
    emL = list()
    outString = "All Emotes: "
    channel = discord.utils.get(bot.get_all_channels(), name="emotebank")
    msg = await channel.history().flatten()
    for m in msg:
        emL.append(m.content)
    for m in sorted(emL):
        outString += "\n -" + m
    await ctx.send(outString)


@bot.command()
async def imUpload(ctx):
    channel = discord.utils.get(bot.get_all_channels(), name="photobank")
    await channel.send("oh my gosh!")

@bot.command()
async def im(ctx):
    inputString = ctx.message.content
    search_terms = set(inputString.lower().split(" "))
    search_terms.remove("$im")
    results = list()
    channel = discord.utils.get(bot.get_all_channels(), name="photodb")
    msg = await channel.history().flatten()
    for m in msg:
        if (len(set(m.content.split(" ")).intersection(search_terms)) != 0):
            results.append(m.attachments[0].url)
    if (len(results) == 0):
        await ctx.send("No image by that name")
    else:
        for r in results:
            await ctx.send(r)

@bot.event
async def on_ready():
    await bot.change_presence(status="online", activity=discord.Activity(type=discord.ActivityType.playing, name="with the TOS"))
    print('im finally running')

bot.run(token)
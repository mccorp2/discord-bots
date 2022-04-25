"""
photo_search functions in small groups and sets of private servers

Using a private discord as an image database and debugger, users are able to upload images and request
the image be added to the database

?imUpload descriptor_1 descriptor_2 ... descriptor_n im_url
    -*to be released* user requests the bot add the image to the database with
     the set of descriptors into the database channel
?im descriptor_1 descriptor_2 ... descriptor_n
    -Searches the image database for an image which best matches (search function to be improved)
     current search function returns the most closly matching image based on number of
     descriptors satisfied. Current issue is this favors images with more descriptors

To Do:
    -Add imUpload(ctx) -> ?imUpload descriptor_1 descriptor_2 ... descriptor_n im_url
        -all arguments besides the command are denoted as descriptors to be used in search functions
        -acts as a midway so only bot has read/write access to the db, and users must request additions
         using a discord server as a database is scuffed as is, any potential safteys from DB corruption
         need be implemented
    -Add imRandom(ctx)
    -Improve search functions
    -Add logical operators to image search
"""
import discord
from discord.ext import commands

token = ''
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = '?', description = "This is a Helper Bot", intents = intents)

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
"""
Emote Bot functions as a cross server emote bot in small groups and sets of private servers

Using a private discord as an image database and debugger, users are able to upload images and request
the image be added to the database

?emUpload emote_name 'emote_url' the bot attempts to add it to the database, assuming the name is unique
then the image is added to the emote bank in a channel only writable to by the bot.
"""
import discord
from discord.ext import commands

token = ''
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = '?', description = "a cross-server emote bot", intents = intents)

#add user to db midway, have bot add images to db based on user request
#add upload failcases which offers close spellings if an emote title already exists
#add auto suggest results if mispelled, with reactions to give intended emote (should be restricted to request user)


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

@bot.event
async def on_ready():
    await bot.change_presence(status="online", activity=discord.Activity(type=discord.ActivityType.playing, name="with the TOS"))
    print('im finally running')

bot.run(token)
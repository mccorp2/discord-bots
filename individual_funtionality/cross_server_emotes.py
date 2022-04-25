"""
corss_server_emotes functions in small groups and sets of private servers

Using a private discord as an image database and debugger, users are able to upload images and request
the image be added to the database

?emUpload emote_name 'emote_url'
    -the bot attempts to add it to the database, assuming the name is unique
     then the image is added to the emote bank in a channel only writable to by the bot.
?em emote_name
    -the bot deletes the context message and sends the intended emote with the request users nickname
     if this fails, the bot *tbr* will reeturn a set of suggested images the bot can post
?emList
    -the bot returns a list of all emotes in the photobank

To Do:
    -Add emUpload(ctx, emote_name, emote_url)
        -acts as a midway so only bot has read/write access to the db, and users must request additions
         using a discord server as a database is scuffed as is, any potential safteys from DB corruption
         need be implemented
    -Add emUpload(...) failcase autofill
        -If a user fails to write the name of an emote, bot should respond with a short list of potential
         matches, and reach to iteslf allowing the user to react and select the intended emote
        -This should be restricted to the original ctx.user.name
"""
import discord
from discord.ext import commands

token = ''
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = '?', description = "This is a Helper Bot", intents = intents)

#Posts emote by name
@bot.command()
async def em(ctx, emote_name):
    channel = discord.utils.get(bot.get_all_channels(), name="emotebank")
    emote_bank = await channel.history().flatten()
    for _emote in emote_bank:
        if (emote_name.lower() == _emote.content.lower()):
            name = ctx.author.name
            if (ctx.author.nick != None):
                name = ctx.author.nick
            await ctx.send("**"+ name + ":**")
            await ctx.send(_emote.attachments[0].url)
            try:
                await ctx.message.delete()
            except:
                print('Error: ' + ctx)
            return
    await ctx.send("*" + 'image \'' + emote_name + '\' was not found' + "*")

#Sends a message containing a sorted list of all emotes in the emote bank
@bot.command()
async def emList(ctx):
    emL = list()
    outString = "All Emotes: "
    channel = discord.utils.get(bot.get_all_channels(), name="emotebank")
    emote_bank = await channel.history().flatten()
    for _emote in emote_bank:
        emL.append(_emote.content)
    for _emote in sorted(emL):
        outString += "\n -" + _emote
    await ctx.send(outString)

@bot.event
async def on_ready():
    await bot.change_presence(status="online", activity=discord.Activity(type=discord.ActivityType.playing, name="with the TOS"))
    print('im finally running')

bot.run(token)
import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import os
import PIL
from io import BytesIO
import json
from PIL import Image, ImageFont, ImageDraw
from itertools import cycle
import requests

import discord_slash
from discord_slash import SlashCommand
from discord_slash.utils import manage_commands

from pymongo import MongoClient

guild_ids = [] # Guild id´s for slash commands
version = "0.2 Alpha"
prefix = "t!"
dev_id = 1 # Dev id
Token = "" # Discord Bot Token
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
client = commands.Bot(command_prefix=prefix, case_insensitive=True, guild_subscriptions=True, intents=intents)
slash = SlashCommand(client, auto_register=True, auto_delete=True)
client.remove_command("help")
statuse = cycle(["Twitch Community", "t!help", F"Bot version {version}"])

cluster = MongoClient("") # Mongo DB settings for Leveling sys
levelling = cluster[""][""]

def dev_check(ctx):
    return ctx.author.id == dev_id


@tasks.loop(seconds=10, hours=0)
async def change_status():
    await client.change_presence(activity=discord.Streaming(name=next(statuse), url="https://www.twitch.tv/falsegr"))

# Events
# on_ready
@client.event
async def on_ready():
    print("---")
    print(F"Der Bot ist gestartet unter {client.user.name}")
    print("---")
    print(F"{client.guilds}")
    print("---")
    print(F"Discord.py Version {discord.__version__}")
    print("---")
    print(version)
    print("---")
    await slash.delete_unused_commands()
    await slash.register_all_commands()
    change_status.start()


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.message.delete()
        fehler = discord.Embed(title="\n",
                               description="Error.\n \n You dont have enough roles",
                               color=0xff0000)
        await ctx.send(embed=fehler)

    if isinstance(error, commands.CommandNotFound):
        fehler = discord.Embed(title="\n",
                               description="Error.\n \n The command dont exist please use `t!help` to find the right command",
                               color=0xff0000)
        await ctx.send(embed=fehler)

    if isinstance(error, commands.NoPrivateMessage):
        fehler = discord.Embed(title="\n",
                               description="Error.\n \n You don't can use this command in the dm´s",
                               color=0xff0000)
        await ctx.send(embed=fehler)

    if isinstance(error, commands.MissingRequiredArgument):
        fehler = discord.Embed(title="\n",
                               description="Error.\n \n it miss a Argument",
                               color=0xff0000)
        await ctx.send(embed=fehler)


@client.command()
@commands.check(dev_check)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(F"wurde geladen {extension}")


@client.command()
@commands.check(dev_check)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(F" unload {extension}")


@client.command()
@commands.check(dev_check)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(F" reload {extension}")



#image
@client.command()
async def wanted(ctx, user: discord.Member = None):
    if user == None:
      user = ctx.author
    loading = await ctx.send("<a:757197819559018527:811329515669946418> picture is loading")
    want = Image.open('istockphoto-941024406-612x612.jpg')
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((177, 177))
    want.paste(pfp, (120, 212))
    want.save("end.jpg")
    await loading.delete()
    await ctx.send(file=discord.File("end.jpg"))

@client.command()
async def imposter(ctx, user: discord.Member = None):
    if user == None:
      user = ctx.author
    loading = await ctx.send("<a:757197819559018527:811329515669946418> picture is loading")
    want = Image.open('imposter.jpg')
    asset = user.avatar_url_as(size=512)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((420, 420))
    want.paste(pfp, (757, 452))
    want.save("imposter2.jpg")
    await loading.delete()
    await ctx.send(file=discord.File("imposter2.jpg"))


#help
@client.group(invoke_without_command=True)
async def help(ctx):
    role = discord.utils.get(ctx.guild.roles, name="「System  ★ 」")
    if role in ctx.author.roles:
        help_eb = discord.Embed(title="Help",
                                description=f"to get more infos about the commands {prefix}help `<command>` \n if the comand is **green** and a plus you can use the comand and if **red** you cant use the command",
                                color=0x8c45f7, timestamp=datetime.datetime.utcnow())
        help_eb.set_thumbnail(url=client.user.avatar_url)
        help_eb.add_field(name="Fun Commands",
                          value=f"```diff\n+{prefix}wanted \n+{prefix}imposter \n\nRandom\n \n+{prefix}cat \n+{prefix}dog \n+{prefix}meme \n+{prefix}joke```")
        help_eb.add_field(name="Twitch Commands",
                          value=f"```diff\n+{prefix}topgame \n+{prefix}game \n+{prefix}twitchinfo```")
        help_eb.add_field(name="Level Commands", value=f"```diff\n+{prefix}rank \n+{prefix}leaderboard```")
        help_eb.add_field(name="Info Commands",
                          value=f"```diff\n+{prefix}pb \n+{prefix}userinfo \n+{prefix}serverinfo \n+{prefix}botstats ``` ")
        help_eb.add_field(name="Mod Commands",
                          value=f"```diff\n+{prefix}ban \n+{prefix}kick \n+{prefix}unban\n+{prefix}warn\n+{prefix}warnings```")
        help_eb.add_field(name="Admin Commands",
                          value=f"```diff\n+{prefix}clear \n+{prefix}setdeay \n+{prefix}announce \n+{prefix}image \n+{prefix}edit ```")
        help_eb.add_field(name="Dev Commands",
                          value=f"```diff\n-{prefix}addxp \n-{prefix}removexp \n-{prefix}load \n-{prefix}unload \n-{prefix}reload ```")

        help_eb.set_footer(icon_url=f"{ctx.author.avatar_url}", text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=help_eb)
    elif ctx.author.id == dev_id:
        help_eb = discord.Embed(title="Help",
                                description=f"to get more infos about the commands {prefix}help `<command>` \n if the comand is **green** and a plus you can use the comand and if **red** you cant use the command",
                                color=0x8c45f7, timestamp=datetime.datetime.utcnow())
        help_eb.set_thumbnail(url=client.user.avatar_url)
        help_eb.add_field(name="Fun Commands",
                          value=f"```diff\n+{prefix}wanted \n+{prefix}imposter \n\nRandom\n \n+{prefix}cat \n+{prefix}dog \n+{prefix}meme \n+{prefix}joke```")
        help_eb.add_field(name="Twitch Commands",
                          value=f"```diff\n+{prefix}topgame \n+{prefix}game \n+{prefix}twitchinfo```")
        help_eb.add_field(name="Level Commands", value=f"```diff\n+{prefix}rank \n+{prefix}leaderboard```")
        help_eb.add_field(name="Info Commands",
                          value=f"```diff\n+{prefix}pb \n+{prefix}userinfo \n+{prefix}serverinfo \n+{prefix}botstats ``` ")
        help_eb.add_field(name="Mod Commands",
                          value=f"```diff\n+{prefix}ban \n+{prefix}kick \n+{prefix}unban\n+{prefix}warn\n+{prefix}warnings```")
        help_eb.add_field(name="Admin Commands",
                          value=f"```diff\n+{prefix}clear \n+{prefix}setdeay \n+{prefix}announce \n+{prefix}image \n+{prefix}edit ```")
        help_eb.add_field(name="Dev Commands",
                          value=f"```diff\n+{prefix}addxp \n+{prefix}removexp \n+{prefix}load \n+{prefix}unload \n+{prefix}reload ```")

        help_eb.set_footer(icon_url=f"{ctx.author.avatar_url}", text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=help_eb)

    else:
        help_eb = discord.Embed(title="Help",
                                description=f"to get more infos about the commands {prefix}help `<command>` \n if the comand is **green** and a plus you can use the comand and if **red** you cant use the command",
                                color=0x8c45f7, timestamp=datetime.datetime.utcnow())
        help_eb.set_thumbnail(url=client.user.avatar_url)
        help_eb.add_field(name="Fun Commands",
                          value=f"```diff\n+{prefix}wanted \n+{prefix}imposter \n\nRandom\n \n+{prefix}cat \n+{prefix}dog \n+{prefix}meme \n+{prefix}joke```")
        help_eb.add_field(name="Twitch Commands", value=f"```diff\n+{prefix}topgame \n+{prefix}game \n+{prefix}twitchinfo```")
        help_eb.add_field(name="Level Commands", value=f"```diff\n+{prefix}rank \n+{prefix}leaderboard```")
        help_eb.add_field(name="Info Commands",
                          value=f"```diff\n+{prefix}pb \n+{prefix}userinfo \n+{prefix}serverinfo \n+{prefix}botstats ``` ")
        help_eb.add_field(name="Mod Commands",
                          value=f"```diff\n-{prefix}ban \n-{prefix}kick \n-{prefix}unban\n-{prefix}warn\n+{prefix}warnings```")
        help_eb.add_field(name="Admin Commands",
                          value=f"```diff\n-{prefix}clear \n-{prefix}setdeay \n-{prefix}announce \n-{prefix}image \n-{prefix}edit ```")
        help_eb.add_field(name="Dev Commands",
                          value=f"```diff\n-{prefix}addxp \n-{prefix}removexp \n-{prefix}load \n-{prefix}unload \n-{prefix}reload ```")
        help_eb.set_footer(icon_url=f"{ctx.author.avatar_url}", text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=help_eb)


@help.command()
async def wanted(ctx):
    command_eb = discord.Embed(title="Wanted", description="make a image with the profile picture  ", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}wanted [@username]")
    await ctx.send(embed=command_eb)

@help.command()
async def rank(ctx):
    command_eb = discord.Embed(title="Rank", description="show your or someone else´s level stats", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}rank [@username]")
    await ctx.send(embed=command_eb)

@help.command()
async def leaderboard(ctx):
    command_eb = discord.Embed(title="Leaderboard", description="show top 15 highst level User", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}leaderboard")
    await ctx.send(embed=command_eb)

@help.command()
async def pb(ctx):
    command_eb = discord.Embed(title="Profile Picture", description="show a Pb off you or someone else", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}pb [@username]")
    await ctx.send(embed=command_eb)

@help.command()
async def userinfo(ctx):
    command_eb = discord.Embed(title="Userinfo", description="Show all infos about the user ", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}userinfo [@username]")
    await ctx.send(embed=command_eb)

@help.command()
async def serverinfo(ctx):
    command_eb = discord.Embed(title="Serverinfo", description="show infos about the server", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}serverinfo")
    await ctx.send(embed=command_eb)

@help.command()
async def botstats(ctx):
    command_eb = discord.Embed(title="Botstats", description="show all stats of the Bot", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}bot stats")
    await ctx.send(embed=command_eb)

@help.command()
async def clear(ctx):
    command_eb = discord.Embed(title="Clear", description="Clear ammount of message. \n You need enough rights", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}clear <ammount>")
    await ctx.send(embed=command_eb)

@help.command()
async def setdelay(ctx):
    command_eb = discord.Embed(title="Setdelay", description="set the slowmode of the channel \n You need enough rights", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}setdelay <seconds>")
    await ctx.send(embed=command_eb)

@help.command()
async def announce(ctx):
    command_eb = discord.Embed(title="Announce", description="Send a embed message \n You need enough rights", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}announce `you get questions` ", inline=False)
    command_eb.add_field(name="Aliases", value="`a`, `ann`, `announcement`")
    await ctx.send(embed=command_eb)

@help.command()
async def edit(ctx):
    command_eb = discord.Embed(title="Edit", description="Edit a embed message \n You need enough rights", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}edit `you get questions` ", inline=False)
    await ctx.send(embed=command_eb)

@help.command()
async def image(ctx):
    command_eb = discord.Embed(title="Image", description="Send a image embed message \n You need enough rights", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}image `you get questions` ", inline=False)
    command_eb.add_field(name="Aliases", value="`i`, `picture` ")
    await ctx.send(embed=command_eb)

@help.command()
async def imposter(ctx):
    command_eb = discord.Embed(title="Imposter", description="make a picture of you or someone else as an imposter", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}imposter [@username]")
    await ctx.send(embed=command_eb)

@help.command()
async def cat(ctx):
    command_eb = discord.Embed(title="Random Cat", description="it send a random cat image", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}cat")
    await ctx.send(embed=command_eb)

@help.command()
async def dog(ctx):
    command_eb = discord.Embed(title="Random Dog", description="it send a random Dog image", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}dog")
    await ctx.send(embed=command_eb)

@help.command()
async def meme(ctx):
    command_eb = discord.Embed(title="Random Meme", description="it send a random Meme image", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}meme")
    await ctx.send(embed=command_eb)

@help.command()
async def ban(ctx):
    command_eb = discord.Embed(title="Ban command", description="its a normal Ban command", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}ban [@username]")
    await ctx.send(embed=command_eb)

@help.command()
async def unban(ctx):
    command_eb = discord.Embed(title="Unban command", description="its a normal unban command", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}unban <username#tag>")
    await ctx.send(embed=command_eb)

@help.command()
async def kick(ctx):
    command_eb = discord.Embed(title="Kick command", description="its a normal kick command", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}kick [@username]")
    await ctx.send(embed=command_eb)

@help.command()
async def warn(ctx):
    command_eb = discord.Embed(title="Warn command", description="its a command to Warn user", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}warn [@username] <reason>")
    await ctx.send(embed=command_eb)

@help.command()
async def warnings(ctx):
    command_eb = discord.Embed(title="Warnings command", description="its a command to get all warnings of a user.", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}warnings [@username]")
    await ctx.send(embed=command_eb)

@help.command()
async def topgame(ctx):
    command_eb = discord.Embed(title="Topgames on Twitch", description="shows top 10 games on Twitch", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}topgame")
    await ctx.send(embed=command_eb)

@help.command()
async def game(ctx):
    command_eb = discord.Embed(title="Game", description="shows image off the game", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}game `you get ask what game`")
    await ctx.send(embed=command_eb)

@help.command()
async def twitchinfo(ctx):
    command_eb = discord.Embed(title="Twitch Info", description="infos about your or onther Twitch channel", color=0x8c45f7)
    command_eb.add_field(name="Syntax", value=f"{prefix}twitchinfo `you get ask the Username `")
    await ctx.send(embed=command_eb)


#slash
@slash.slash(name="help", description="shows you all slash commands", guild_ids=guild_ids)
async def _help(ctx):
    role = discord.utils.get(ctx.guild.roles, name="「System  ★ 」")
    if role in ctx.author.roles:
        help_eb = discord.Embed(title="Help",
                                description=f"to get more infos about the commands {prefix}help `<command>` \n if the comand is **green** and a plus you can use the comand and if **red** you cant use the command",
                                color=0x8c45f7, timestamp=datetime.datetime.utcnow())
        help_eb.set_thumbnail(url=client.user.avatar_url)
        help_eb.add_field(name="Fun Commands",
                          value=f"```diff\n+{prefix}wanted \n+{prefix}imposter \n\nRandom\n \n+{prefix}cat \n+{prefix}dog \n+{prefix}meme \n+{prefix}joke```")
        help_eb.add_field(name="Level Commands", value=f"```diff\n+{prefix}rank \n+{prefix}leaderboard```")
        help_eb.add_field(name="Info Commands",
                          value=f"```diff\n+{prefix}pb \n+{prefix}userinfo \n+{prefix}serverinfo \n+{prefix}botstats ``` ")
        help_eb.add_field(name="Mod Commands",
                          value=f"```diff\n+{prefix}ban \n+{prefix}kick \n+{prefix}unban\n+{prefix}warn\n+{prefix}warnings```")
        help_eb.add_field(name="Admin Commands",
                          value=f"```diff\n+{prefix}clear \n+{prefix}setdeay \n+{prefix}announce \n+{prefix}image \n+{prefix}edit ```")
        help_eb.add_field(name="Dev Commands",
                          value=f"```diff\n-{prefix}addxp \n-{prefix}removexp \n-{prefix}load \n-{prefix}unload \n-{prefix}reload ```")

        help_eb.set_footer(icon_url=f"{ctx.author.avatar_url}", text=f"Requested by {ctx.author.name}")
        await ctx.send(embeds=[help_eb])
    elif ctx.author.id == dev_id:
        help_eb = discord.Embed(title="Help",
                                description=f"to get more infos about the commands {prefix}help `<command>` \n if the comand is **green** and a plus you can use the comand and if **red** you cant use the command",
                                color=0x8c45f7, timestamp=datetime.datetime.utcnow())
        help_eb.set_thumbnail(url=client.user.avatar_url)
        help_eb.add_field(name="Fun Commands",
                          value=f"```diff\n+{prefix}wanted \n+{prefix}imposter \n\nRandom\n \n+{prefix}cat \n+{prefix}dog \n+{prefix}meme \n+{prefix}joke```")
        help_eb.add_field(name="Level Commands", value=f"```diff\n+{prefix}rank \n+{prefix}leaderboard```")
        help_eb.add_field(name="Info Commands",
                          value=f"```diff\n+{prefix}pb \n+{prefix}userinfo \n+{prefix}serverinfo \n+{prefix}botstats ``` ")
        help_eb.add_field(name="Mod Commands",
                          value=f"```diff\n+{prefix}ban \n+{prefix}kick \n+{prefix}unban\n+{prefix}warn\n+{prefix}warnings```")
        help_eb.add_field(name="Admin Commands",
                          value=f"```diff\n+{prefix}clear \n+{prefix}setdeay \n+{prefix}announce \n+{prefix}image \n+{prefix}edit ```")
        help_eb.add_field(name="Dev Commands",
                          value=f"```diff\n+{prefix}addxp \n+{prefix}removexp \n+{prefix}load \n+{prefix}unload \n+{prefix}reload ```")

        help_eb.set_footer(icon_url=f"{ctx.author.avatar_url}", text=f"Requested by {ctx.author.name}")
        await ctx.send(embeds=[help_eb])

    else:
        help_eb = discord.Embed(title="Help",
                                description=f"to get more infos about the commands {prefix}help `<command>` \n if the comand is **green** and a plus you can use the comand and if **red** you cant use the command",
                                color=0x8c45f7, timestamp=datetime.datetime.utcnow())
        help_eb.set_thumbnail(url=client.user.avatar_url)
        help_eb.add_field(name="Fun Commands",
                          value=f"```diff\n+{prefix}wanted \n+{prefix}imposter \n\nRandom\n \n+{prefix}cat \n+{prefix}dog \n+{prefix}meme \n+{prefix}joke```")
        help_eb.add_field(name="Level Commands", value=f"```diff\n+{prefix}rank \n+{prefix}leaderboard```")
        help_eb.add_field(name="Info Commands",
                          value=f"```diff\n+{prefix}pb \n+{prefix}userinfo \n+{prefix}serverinfo \n+{prefix}botstats ``` ")
        help_eb.add_field(name="Mod Commands",
                          value=f"```diff\n-{prefix}ban \n-{prefix}kick \n-{prefix}unban\n-{prefix}warn\n+{prefix}warnings```")
        help_eb.add_field(name="Admin Commands",
                          value=f"```diff\n-{prefix}clear \n-{prefix}setdeay \n-{prefix}announce \n-{prefix}image \n-{prefix}edit ```")
        help_eb.add_field(name="Dev Commands",
                          value=f"```diff\n-{prefix}addxp \n-{prefix}removexp \n-{prefix}load \n-{prefix}unload \n-{prefix}reload ```")
        help_eb.set_footer(icon_url=f"{ctx.author.avatar_url}", text=f"Requested by {ctx.author.name}")
        await ctx.send(embeds=[help_eb])

@slash.slash(name="rank", description="shows you all your level stats",guild_ids=guild_ids)
async def _rank(ctx,member: discord.Member = None):
    member = ctx.author if not member else member
    stats = levelling.find_one({"id": member.id})
    if stats is None:
        embed = discord.Embed(title="You haven't sent any message",color=0x8c45f7)
        await ctx.send(embeds=[embed])
    else:
        xp = stats["xp"]
        lvl = 0
        rank = 0
        while True:
            if xp < (50*(lvl**2)) + (50*(lvl)):
                break
            lvl += 1
        xp -= ((50*(lvl-1)**2)+(50*(lvl-1)))
        boxes = int((xp/(200*(1/2) * lvl))*20)
        rankings = levelling.find().sort("xp",-1)
        for x in rankings:
            rank += 1
            if stats["id"] == x["id"]:
                break
        embed = discord.Embed(title=f"Levelstats of {member.name}", timestamp=datetime.datetime.utcnow(), color=0x8c45f7)
        embed.add_field(name="Name", value=member.mention, inline=False)
        embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=False)
        embed.add_field(name="Level", value=f"{lvl}", inline=False)
        embed.add_field(name="Rank", value=f"{rank} of {ctx.guild.member_count} ", inline=False)
        embed.add_field(name="Progress [lvl]", value=boxes * "🟪" + (20-boxes) * "⬜", inline=False)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(icon_url=ctx.guild.icon_url, text="temQ eSports")
        await ctx.send(embeds=[embed])

@slash.slash(name="invite", description="shows you the discord Invite",guild_ids=guild_ids)
async def _invite(ctx):
    embed = discord.Embed(title="**Invites**", description="**Test**",color=0x8c45f7)
    await ctx.send(embeds=[embed])

@slash.slash(name="report", description="Report a user", options=[manage_commands.create_option(name='user', description="name of the user", option_type=3, required=True), manage_commands.create_option(name='reason', description="The reason for the report", option_type=3, required=True)], guild_ids=guild_ids)
async def _report(ctx, user:discord.User, reason=str):
    print(f"test {user} {reason}")
    embed = discord.Embed(title=f"Report {ctx.author.name}", description=f"User: {user} | Reason: `{reason}`", timestamp=datetime.datetime.utcnow(), color=0x8c45f7)
    await  client.get_channel(811320923533082646).send(embed=embed)
    await ctx.send(content="thanks for your Report")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(Token)


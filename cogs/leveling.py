import discord
from discord.ext import commands
import asyncio
import datetime
import time
import os


from pymongo import MongoClient

talk_channels = [] # Talk Channel
level =[] # Level Role
levelnum = [] # What rank you get the role

cluster = MongoClient()
levelling = cluster[""][""] # Mongo DB settings for Leveling sys

from test import dev_id


def dev_check(ctx):
    return ctx.author.id == dev_id


class leveling(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('leveling is ready')
        print("---")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in talk_channels:
            stats = levelling.find_one({"id": message.author.id})
            if not  message.author.bot:
                if stats is None:
                    newuser = {"id": message.author.id, "xp": 95}
                    levelling.insert_one(newuser)
                else:
                    xp = stats["xp"] + 5
                    levelling.update_one({"id":message.author.id}, {"$set":{"xp":xp}})
                    lvl = 0
                    while True:
                        if xp < (50*(lvl**2))+(50*(lvl)):
                            break
                        lvl += 1
                    xp -= ((50*(lvl-1)**2)+(50*(lvl-1)))
                    if xp == 0:
                        await message.channel.send(f"Nice {message.author.mention}! You leveled up to **level : {lvl}**")
                        for i in range(len(level)):
                            if lvl == levelnum[i]:
                                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))

    @commands.command()
    async def rank(self, ctx,member: discord.Member = None):
        member = ctx.author if not member else member
        stats = levelling.find_one({"id": member.id})
        if stats is None:
            embed = discord.Embed(title="You haven't sent any message",color=0xfcfcfc)
            await ctx.send(embed=embed)
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
            embed = discord.Embed(title=f"Levelstats of {member.name}", timestamp=datetime.datetime.utcnow(), color=0xfcfcfc)
            embed.add_field(name="Name", value=member.mention, inline=False)
            embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=False)
            embed.add_field(name="Level", value=f"{lvl}", inline=False)
            embed.add_field(name="Rank", value=f"{rank} of {ctx.guild.member_count} ", inline=False)
            embed.add_field(name="Progress [lvl]", value=boxes * "🟪" + (20-boxes) * "⬜", inline=False)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(icon_url=ctx.guild.icon_url, text="temQ eSports")
            await ctx.send(embed=embed)

    @commands.command()
    async def leaderboard(self, ctx):
        rankings = levelling.find().sort("xp", -1)
        i = 1
        embed = discord.Embed(title="Leaderboard", color=0xfcfcfc)
        for x in rankings:
            try:
                temp = ctx.guild.get_member(x["id"])
                tempxp = x["xp"]
                embed.add_field(name=f"{i}: {temp.name}", value=f"total XP : {tempxp}", inline=False)
                i+= 1
            except:
                pass
            if i == 16:
                break
        await ctx.send(embed=embed)



    @commands.command()
    @commands.check(dev_check)
    async def addxp(self,ctx, setxp: int, member: discord.Member = None):
        member = ctx.author if not member else member
        stats = levelling.find_one({"id": member.id})
        xp = stats["xp"] + int(setxp)
        levelling.update_one({"id": member.id}, {"$set": {"xp": xp}})
        await ctx.send(f"you added {setxp} to `{member}` ")

    @commands.command()
    @commands.check(dev_check)
    async def removexp(self,ctx, setxp: int, member: discord.Member = None):
        member = ctx.author if not member else member
        stats = levelling.find_one({"id": member.id})
        xp = stats["xp"] - int(setxp)
        levelling.update_one({"id": member.id}, {"$set": {"xp": xp}})
        await ctx.send(f"you removed {setxp} to `{member}` ")




def setup(client):
    client.add_cog(leveling(client))